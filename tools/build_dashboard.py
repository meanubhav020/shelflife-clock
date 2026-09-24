import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name, key):
    path = ROOT / name
    if not path.exists():
        return {}
    with open(path, newline="", encoding="utf-8") as f:
        return {r[key]: r for r in csv.DictReader(f)}


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def parts(value):
    return {x.strip() for x in re.split(r"[;,]", value or "") if x.strip()}


def shape(q):
    return {
        "action": q["action"] or "None",
        "clauses": sorted(parts(q["clause_ids"])),
        "status": q["status"],
        "reason": q["hold_reason"],
        "approvers": sorted(parts(q["approver"])),
    }


def main():
    scored = load("scored.csv", "batch_id")
    inventory = load("inventory_clean.csv", "batch_id")
    skus = load("sku_master.csv", "sku")
    queue = load("action_queue.csv", "batch_id")
    api = load("action_queue_api.csv", "batch_id")
    decisions = load("decisions_api.csv", "batch_id")

    rows = []
    for b, q in queue.items():
        s = scored.get(b, {})
        inv = inventory.get(b, {})
        sku = skus.get(inv.get("sku", ""), {})
        cc = shape(q)
        a = shape(api[b]) if b in api else None
        row = {
            "batch_id": b,
            "description": sku.get("description", ""),
            "product_class": sku.get("product_class", ""),
            "location_id": inv.get("location_id", ""),
            "trust_flag": inv.get("trust_flag", ""),
            "days_to_expiry": num(s.get("days_to_expiry")),
            "batch_value": num(s.get("batch_value")),
            "score": num(s.get("score")),
            "band": s.get("band", ""),
            "cc": cc,
            "api": a,
        }
        if a:
            row["action_status_match"] = (cc["action"], cc["status"]) == (a["action"], a["status"])
            row["approver_match"] = cc["approvers"] == a["approvers"]
            row["only_cc"] = sorted(set(cc["clauses"]) - set(a["clauses"]))
            row["only_api"] = sorted(set(a["clauses"]) - set(cc["clauses"]))
            row["identical"] = row["action_status_match"] and row["approver_match"] and not row["only_cc"] and not row["only_api"]
            d = decisions.get(b)
            row["ruled_out"] = sorted(parts(d["ruled_out_clauses"])) if d else []
        rows.append(row)

    counts = Counter(r["cc"]["status"] for r in rows)
    summary = {
        "in_scope": len(rows),
        "READY": counts.get("READY", 0),
        "HOLD": counts.get("HOLD", 0),
        "MONITOR": counts.get("MONITOR", 0),
    }
    summary["adds_up"] = summary["in_scope"] == summary["READY"] + summary["HOLD"] + summary["MONITOR"]

    compared = [r for r in rows if r["api"]]
    summary["compared"] = len(compared)
    summary["action_status_match"] = sum(r["action_status_match"] for r in compared)
    summary["approver_match"] = sum(r["approver_match"] for r in compared)
    summary["identical"] = sum(r["identical"] for r in compared)

    scored_rows = [r for r in rows if r["score"] is not None]
    top_five = [r["batch_id"] for r in sorted(scored_rows, key=lambda r: r["score"], reverse=True)[:5]]

    data = json.dumps({"rows": rows, "summary": summary, "top_five": top_five})
    data = data.replace("</", "<\\/")

    template = (ROOT / "tools" / "dashboard_template.html").read_text(encoding="utf-8")
    (ROOT / "dashboard.html").write_text(template.replace("__DATA__", data), encoding="utf-8")
    print(f"Wrote dashboard.html: {summary}")


if __name__ == "__main__":
    main()
