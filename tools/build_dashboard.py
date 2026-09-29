import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from roi import BASELINE, compute_roi  # noqa: E402

QUEUE_FILE = "action_queue_api.csv"
# The ten designed test batches are built to be tricky (Lab 6); they bias an ROI
# estimate, so the panel excludes them the same way the original random sample did.
DESIGNED_TEST_BATCHES = {f"LF-{i}" for i in range(70001, 70011)}
ACTING_RATES = [("cautious", 0.40), ("typical", 0.60), ("optimistic", 0.80)]


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
    return sorted({x.strip() for x in re.split(r"[;,]", value or "") if x.strip()})


def build_data():
    scored = load("scored.csv", "batch_id")
    inventory = load("inventory_clean.csv", "batch_id")
    skus = load("sku_master.csv", "sku")
    queue = load(QUEUE_FILE, "batch_id")
    locations = load("locations.csv", "location_id")

    rows = []
    for b, q in queue.items():
        s = scored.get(b, {})
        inv = inventory.get(b, {})
        sku = skus.get(inv.get("sku", ""), {})
        batch_value = num(s.get("batch_value"))
        unsold_share = num(s.get("unsold_share"))
        value_at_risk = batch_value * unsold_share if batch_value is not None and unsold_share is not None else None
        rows.append({
            "batch_id": b,
            "description": sku.get("description", ""),
            "product_class": sku.get("product_class", ""),
            "location_id": inv.get("location_id", ""),
            "trust_flag": inv.get("trust_flag", ""),
            "days_to_expiry": num(s.get("days_to_expiry")),
            "batch_value": batch_value,
            "value_at_risk": value_at_risk,
            "score": num(s.get("score")),
            "band": s.get("band", ""),
            "action": q["action"] or "None",
            "clauses": parts(q["clause_ids"]),
            "status": q["status"],
            "reason": q["hold_reason"],
            "approvers": parts(q["approver"]),
        })

    counts = Counter(r["status"] for r in rows)
    summary = {
        "in_scope": len(rows),
        "READY": counts.get("READY", 0),
        "HOLD": counts.get("HOLD", 0),
        "MONITOR": counts.get("MONITOR", 0),
    }
    summary["adds_up"] = summary["in_scope"] == summary["READY"] + summary["HOLD"] + summary["MONITOR"]

    scored_rows = [r for r in rows if r["score"] is not None]
    top_five = [r["batch_id"] for r in sorted(scored_rows, key=lambda r: r["score"], reverse=True)[:5]]

    roi_batch_ids = [b for b in queue if b not in DESIGNED_TEST_BATCHES and scored.get(b, {}).get("in_scope") == "Y"]
    roi_result = compute_roi(roi_batch_ids, queue, scored, inventory, skus)
    r = roi_result["r"]
    roi = {
        "batches": len(roi_result["rows"]),
        "excluded_test_batches": len(DESIGNED_TEST_BATCHES & set(queue)),
        "total_at_risk": roi_result["total_at_risk"],
        "total_recovered": roi_result["total_recovered"],
        "r": r,
        "baseline": BASELINE,
        "acting_rates": [{"label": label, "e": e, "yearly_saving": BASELINE * r * e} for label, e in ACTING_RATES],
    }

    by_location = {}
    for r in rows:
        loc_id = r["location_id"]
        agg = by_location.setdefault(loc_id, {
            "location_id": loc_id,
            "name": locations.get(loc_id, {}).get("name", loc_id or "(unknown)"),
            "region": locations.get(loc_id, {}).get("region", ""),
            "type": locations.get(loc_id, {}).get("type", ""),
            "cold_chain": locations.get(loc_id, {}).get("cold_chain", ""),
            "healthcare_licensed": locations.get(loc_id, {}).get("healthcare_licensed", ""),
            "batches": 0, "total_value": 0.0, "total_at_risk": 0.0,
            "READY": 0, "HOLD": 0, "MONITOR": 0,
        })
        agg["batches"] += 1
        agg["total_value"] += r["batch_value"] or 0.0
        agg["total_at_risk"] += r["value_at_risk"] or 0.0
        agg[r["status"]] = agg.get(r["status"], 0) + 1
    locations_out = sorted(by_location.values(), key=lambda a: a["total_at_risk"], reverse=True)

    return {"rows": rows, "summary": summary, "top_five": top_five, "source": QUEUE_FILE, "roi": roi,
            "locations": locations_out}


def render_page(data, live=False):
    blob = json.dumps(data).replace("</", "<\\/")
    template = (ROOT / "tools" / "dashboard_template.html").read_text(encoding="utf-8")
    return template.replace("__LIVE__", "true" if live else "false").replace("__DATA__", blob)


def main():
    data = build_data()
    if not data["rows"]:
        print(f"No rows in {QUEUE_FILE}. Run tools/run_agent.py first.")
        return
    (ROOT / "dashboard.html").write_text(render_page(data), encoding="utf-8")
    print(f"Wrote dashboard.html from {QUEUE_FILE}: {data['summary']}")


if __name__ == "__main__":
    main()
