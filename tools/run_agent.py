"""Run the Shelf-Life Clock decision step through the Anthropic API, outside Claude Code.

Data lookups, the data-trust gate, approver rules and clause checks are code.
The model only chooses an action from docs/ and (in a second call that sees three
inputs only) drafts the request.

Needs: pip install anthropic, and ANTHROPIC_API_KEY set in the environment.
Never put the key in a file.
"""
import argparse
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MODEL = "claude-opus-5"
FALLBACK_MODEL = "claude-opus-4-8"
FALLBACK_BETA = "server-side-fallback-2026-06-01"
QUEUE_COLUMNS = ["batch_id", "action", "clause_ids", "status", "hold_reason", "approver"]
DECISION_COLUMNS = ["batch_id", "ruled_out_clauses", "reason", "notes"]
ACTIONS = ["MONITOR", "TRANSFER", "RETURN TO SUPPLIER", "MARKDOWN", "DISPOSE", "ESCALATE"]

RULES = """You choose ONE action for ONE inventory batch for Larkfield Distribution, a
fictional food and healthcare distributor. All data and policy are made up.

Rules:
- Use only the policy documents below. If they do not answer something, do not invent
  a threshold, discount, fee or recovery rate. Never estimate.
- Cite the document ID for every claim, for example REF-ACT-03. Only use IDs that
  appear in the documents.
- The batch facts were computed by scripts. Use them as given and do not recompute
  days, values or scores.
- Product class in the facts comes from the master file. It is the only class to use.
- Actions: MONITOR, TRANSFER, RETURN TO SUPPLIER, MARKDOWN, DISPOSE, or ESCALATE.
  ESCALATE means the batch must go to a person with no disposition proposed, and is
  only for the case REF-HC-04 describes.
- If more than one action is eligible, follow the order of preference in the documents.
- For TRANSFER, name the target location_id from candidate_transfer_targets. If no
  candidate satisfies every transfer clause, TRANSFER is not eligible.
- Do not decide approvals. Code applies the approval rules afterwards.

Reply with one JSON object and nothing else:
{"action": "<one of the actions>", "allowing_clauses": ["REF-..."], "ruled_out_clauses": ["REF-..."], "transfer_target": "<location_id or null>", "reason": "<one or two sentences>"}

allowing_clauses: ONLY the clauses that make the chosen action allowed (for MONITOR, the
clause that names why MONITOR applies, plus any clause that states that reason, such as
scope). Never put a clause here for an action you did not choose.
ruled_out_clauses: clauses of other actions you considered and found NOT satisfied.
"""

DRAFTER_SYSTEM = """You write a short action request for one batch. You are given only
batch facts, the product class and the exact policy clause text. Write 3 to 4 lines:
what to do, which clause allows it, who must approve. Cite clause IDs exactly as given.
Do not add numbers, fees, discounts or rules that are not in the input. All money is in
US dollars: write it with a $ sign. If a transfer target is given, name it. Only mention
clauses that apply to this batch. No em dashes."""


def read_csv(name, key):
    with open(ROOT / name, newline="", encoding="utf-8") as f:
        return {r[key]: r for r in csv.DictReader(f)}


def load_docs():
    text = {}
    ids = {}
    for path in sorted((ROOT / "docs").glob("*.md")):
        body = path.read_text(encoding="utf-8")
        text[path.name] = body
        for m in re.finditer(r"^\[(REF-[A-Z]+-\d+)\]\s*(.*)$", body, re.M):
            ids[m.group(1)] = m.group(0)
    return text, ids


def build_facts(batch_id, inv, scored, skus, locs, all_inv):
    row = inv[batch_id]
    s = scored[batch_id]
    sku = skus[row["sku"]]
    loc = locs[row["location_id"]]
    targets = []
    for r in all_inv:
        if r["sku"] == row["sku"] and r["batch_id"] != batch_id:
            ol = locs[r["location_id"]]
            targets.append({
                "location_id": r["location_id"],
                "units_sold_last_30d": r["units_sold_last_30d"],
                "cold_chain": ol["cold_chain"],
                "healthcare_licensed": ol["healthcare_licensed"],
            })
    return {
        "batch_id": batch_id,
        "description": sku["description"],
        "product_class": sku["product_class"],
        "trust_flag": row["trust_flag"],
        "location_id": row["location_id"],
        "units_on_hand": row["units_on_hand"],
        "units_sold_last_30d": row["units_sold_last_30d"],
        "supplier_accepts_returns": sku["supplier_accepts_returns"],
        "days_to_expiry": s["days_to_expiry"],
        "in_scope": s["in_scope"],
        "unsold_share": s["unsold_share"],
        "batch_value": s["batch_value"],
        "score": s["score"],
        "band": s["band"],
        "candidate_transfer_targets": targets,
    }


def approvals(action, product_class, value):
    """REF-APR-01 to REF-APR-05, applied in code."""
    roles, clauses = [], []
    if action == "MONITOR":
        return roles, clauses
    if product_class == "HEALTHCARE":
        roles.append("QA Lead")
        clauses.append("REF-APR-01")
    if value > 10000:
        roles.append("Finance Director")
        clauses.append("REF-APR-02")
    elif value > 2000:
        roles.append("Regional Manager")
        clauses.append("REF-APR-02")
    if action == "DISPOSE":
        roles.append("Finance")
        clauses.append("REF-APR-03")
    return roles, clauses


def extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object in reply")
    return json.loads(m.group(0))


def text_of(response):
    return "".join(b.text for b in response.content if b.type == "text")


class Model:
    def __init__(self, model, docs_text):
        import anthropic
        self.anthropic = anthropic
        self.client = anthropic.Anthropic()
        self.model = model
        self.system = [{
            "type": "text",
            "text": RULES + "\n\nPOLICY DOCUMENTS\n\n" + "\n\n".join(
                f"### {name}\n{body}" for name, body in docs_text.items()),
            "cache_control": {"type": "ephemeral"},
        }]

    def call(self, system, user, effort):
        return self.client.beta.messages.create(
            model=self.model,
            max_tokens=4000,
            betas=[FALLBACK_BETA],
            fallbacks=[{"model": FALLBACK_MODEL}],
            output_config={"effort": effort},
            system=system,
            messages=[{"role": "user", "content": user}],
        )

    def decide(self, facts):
        return self.call(self.system, "Batch facts:\n" + json.dumps(facts, indent=1), "medium")

    def draft(self, facts, product_class, clause_text, approvers):
        shown = {k: facts[k] for k in ("batch_id", "description", "units_on_hand",
                                       "days_to_expiry", "batch_value", "score", "band")}
        shown["currency"] = "USD"
        if facts.get("transfer_target"):
            shown["transfer_target"] = facts["transfer_target"]
        payload = (
            "Batch facts:\n" + json.dumps(shown, indent=1)
            + f"\n\nProduct class: {product_class}\n\nClause text:\n" + "\n".join(clause_text)
            + "\n\nApprover roles (decided by code): " + (", ".join(approvers) or "none")
        )
        return self.call(DRAFTER_SYSTEM, payload, "low")


def process(batch_id, data, docs_ids, model, dry_run):
    inv, scored, skus, locs, all_inv = data
    facts = build_facts(batch_id, inv, scored, skus, locs, all_inv)

    if facts["trust_flag"] != "OK":  # THE GATE, in code, before any model call
        row = dict(batch_id=batch_id, action="", clause_ids="REF-APR-04", status="HOLD",
                   hold_reason="data check flag not OK", approver="Inventory Control")
        return row, "", [], {}

    if dry_run:
        print(f"--- {batch_id} decision input ---\n{json.dumps(facts, indent=1)}\n")
        return None, "", [], {}

    notes = []
    try:
        resp = model.decide(facts)
        if resp.stop_reason == "refusal":
            raise ValueError("model refused")
        d = extract_json(text_of(resp))
    except Exception as e:  # rule 6: never stop silently
        row = dict(batch_id=batch_id, action="", clause_ids="", status="HOLD",
                   hold_reason=f"agent could not process this batch: {e}", approver="Inventory Control")
        return row, "", [str(e)], {}

    action = str(d.get("action", "")).upper()
    target = d.get("transfer_target")
    valid_targets = {t["location_id"] for t in facts["candidate_transfer_targets"]}
    if action == "TRANSFER":
        if target in valid_targets:
            facts["transfer_target"] = target
        else:
            notes.append(f"transfer target {target!r} is not a candidate")
    clauses = [c for c in d.get("allowing_clauses", []) if isinstance(c, str)]
    ruled_out = [c for c in d.get("ruled_out_clauses", []) if isinstance(c, str)]
    bad = [c for c in clauses + ruled_out if c not in docs_ids]
    if bad:
        notes.append(f"unknown clause IDs from model: {bad}")
    overlap = sorted(set(clauses) & set(ruled_out))
    if overlap:
        notes.append(f"clauses listed as both allowing and ruled out: {overlap}")
    if not clauses:
        notes.append("model gave no allowing clause")
    extra = {"ruled_out_clauses": ";".join(ruled_out), "reason": d.get("reason", ""), "notes": " | ".join(notes)}
    if action not in ACTIONS:
        row = dict(batch_id=batch_id, action="", clause_ids=";".join(clauses), status="HOLD",
                   hold_reason=f"model returned an invalid action: {action!r}", approver="Inventory Control")
        return row, "", notes, extra

    value = float(facts["batch_value"] or 0)
    if action == "ESCALATE" and facts["product_class"] != "HEALTHCARE":
        row = dict(batch_id=batch_id, action="", clause_ids=";".join(clauses), status="HOLD",
                   hold_reason="model escalated a non-healthcare batch, which no clause allows",
                   approver="Inventory Control")
        return row, "", notes, extra
    if action == "ESCALATE":
        roles, ap_clauses = ["QA Lead"], ["REF-APR-01"]
        status, action_out = "HOLD", ""
        reason = d.get("reason", "escalated")
    else:
        roles, ap_clauses = approvals(action, facts["product_class"], value)
        action_out = action
        if action == "MONITOR":
            status, reason = "MONITOR", ""
        elif roles:
            status, reason = "HOLD", "approval required: " + ", ".join(roles)
        else:
            status, reason = "READY", ""
            ap_clauses = ["REF-APR-05"]
    all_clauses = list(dict.fromkeys(clauses + ap_clauses))
    row = dict(batch_id=batch_id, action=action_out, clause_ids=";".join(all_clauses), status=status,
               hold_reason=reason, approver="; ".join(roles))

    request = ""
    if action != "ESCALATE":
        clause_text = [docs_ids[c] for c in all_clauses if c in docs_ids]
        try:
            request = text_of(model.draft(facts, facts["product_class"], clause_text, roles)).strip()
        except Exception as e:
            notes.append(f"drafter failed: {e}")
            extra["notes"] = " | ".join(notes)
    return row, request, notes, extra


def compare(rows, path):
    with open(path, newline="", encoding="utf-8") as f:
        ref = {r["batch_id"]: r for r in csv.DictReader(f)}
    def split(value):
        return {x.strip() for x in re.split(r"[;,]", value or "") if x.strip()}

    checked = action_diff = approver_diff = clause_diff = all_match = 0
    for r in rows:
        o = ref.get(r["batch_id"])
        if o is None:
            continue
        checked += 1
        issues = []
        if (o["action"], o["status"]) != (r["action"], r["status"]):
            action_diff += 1
            issues.append(f"action/status existing {o['action'] or '-'}/{o['status']} api {r['action'] or '-'}/{r['status']}")
        if split(o["approver"]) != split(r["approver"]):
            approver_diff += 1
            issues.append(f"approver existing [{'; '.join(sorted(split(o['approver']))) or 'none'}] "
                          f"api [{'; '.join(sorted(split(r['approver']))) or 'none'}]")
        oc, rc = split(o["clause_ids"]), split(r["clause_ids"])
        if oc != rc:
            clause_diff += 1
            only_old, only_new = sorted(oc - rc), sorted(rc - oc)
            issues.append(f"clauses only in existing {only_old or '-'}, only in api {only_new or '-'}")
        if issues:
            print(f"DIFF {r['batch_id']}: " + " | ".join(issues))
        else:
            all_match += 1
    print(f"\nCompared {checked} batches against {path}")
    print(f"  action and status differ: {action_diff}")
    print(f"  approver differs:         {approver_diff}")
    print(f"  clause IDs differ:        {clause_diff}")
    print(f"  identical on all three:   {all_match}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("batches", nargs="*", help="batch IDs, e.g. LF-70001")
    p.add_argument("--sample", help="file with one batch ID per line, e.g. notes/sample.txt")
    p.add_argument("--out", default="action_queue_api.csv")
    p.add_argument("--model", default=DEFAULT_MODEL)
    p.add_argument("--dry-run", action="store_true", help="print the model inputs, call nothing")
    p.add_argument("--compare", metavar="CSV", help="compare against an existing queue, e.g. action_queue.csv")
    p.add_argument("--resume", action="store_true", help="keep rows already in --out and only run the rest")
    a = p.parse_args()

    ids = list(a.batches)
    if a.sample:
        ids += [l.strip() for l in (ROOT / a.sample).read_text().splitlines() if l.strip()]
    if not ids:
        p.error("give batch IDs or --sample")

    inv = read_csv("inventory_clean.csv", "batch_id")
    scored = read_csv("scored.csv", "batch_id")
    skus = read_csv("sku_master.csv", "sku")
    locs = read_csv("locations.csv", "location_id")
    with open(ROOT / "inventory_clean.csv", newline="", encoding="utf-8") as f:
        all_inv = list(csv.DictReader(f))
    data = (inv, scored, skus, locs, all_inv)
    docs_text, docs_ids = load_docs()

    model = None if a.dry_run else Model(a.model, docs_text)

    out_path = ROOT / a.out
    if a.out == "action_queue_api.csv":
        req_path, dec_path = ROOT / "requests_api.md", ROOT / "decisions_api.csv"
    else:
        stem = Path(a.out).stem
        req_path, dec_path = ROOT / f"{stem}_requests.md", ROOT / f"{stem}_decisions.csv"
    done = set()
    if not a.dry_run:
        if a.resume and out_path.exists():
            with open(out_path, newline="", encoding="utf-8") as f:
                done = {r["batch_id"] for r in csv.DictReader(f)}
            print(f"Resuming: {len(done)} batches already in {a.out}", flush=True)
        else:
            with open(out_path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=QUEUE_COLUMNS).writeheader()
            req_path.write_text("# Drafted requests (API run)\n\n", encoding="utf-8")
            with open(dec_path, "w", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=DECISION_COLUMNS).writeheader()

    def save(row, request, extra):
        with open(out_path, "a", newline="", encoding="utf-8") as f:
            csv.DictWriter(f, fieldnames=QUEUE_COLUMNS).writerow(row)
        if extra:
            with open(dec_path, "a", newline="", encoding="utf-8") as f:
                csv.DictWriter(f, fieldnames=DECISION_COLUMNS).writerow({"batch_id": row["batch_id"], **extra})
        if request:
            with open(req_path, "a", encoding="utf-8") as f:
                f.write(f"## {row['batch_id']}\n\n{request}\n\n")

    for b in ids:
        if b in done:
            continue
        if b not in inv:
            print(f"{b}: not in inventory_clean.csv", file=sys.stderr, flush=True)
            row, request, notes, extra = dict(batch_id=b, action="", clause_ids="", status="HOLD",
                                              hold_reason="batch not found in inventory_clean.csv",
                                              approver="Inventory Control"), "", [], {}
        else:
            row, request, notes, extra = process(b, data, docs_ids, model, a.dry_run)
        if row is None:
            continue
        save(row, request, extra)  # written immediately, so a cut-off keeps finished work
        print(f"{b}: {row['action'] or '-'} {row['status']}" + (f"  NOTE {notes}" if notes else ""), flush=True)

    if a.dry_run:
        return
    with open(out_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    counts = {s: sum(r["status"] == s for r in rows) for s in ("READY", "HOLD", "MONITOR")}
    print(f"\n{a.out}: {len(rows)} in scope = {counts['READY']} READY + {counts['HOLD']} HOLD + {counts['MONITOR']} MONITOR", flush=True)
    if a.compare:
        compare(rows, ROOT / a.compare)


if __name__ == "__main__":
    main()
