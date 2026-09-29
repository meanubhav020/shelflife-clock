import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUEUE_FILE = "action_queue_api.csv"


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

    rows = []
    for b, q in queue.items():
        s = scored.get(b, {})
        inv = inventory.get(b, {})
        sku = skus.get(inv.get("sku", ""), {})
        rows.append({
            "batch_id": b,
            "description": sku.get("description", ""),
            "product_class": sku.get("product_class", ""),
            "location_id": inv.get("location_id", ""),
            "trust_flag": inv.get("trust_flag", ""),
            "days_to_expiry": num(s.get("days_to_expiry")),
            "batch_value": num(s.get("batch_value")),
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

    return {"rows": rows, "summary": summary, "top_five": top_five, "source": QUEUE_FILE}


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
