import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load(name, key):
    with open(ROOT / name, newline="", encoding="utf-8") as f:
        return {r[key]: r for r in csv.DictReader(f)}


def num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def main():
    scored = load("scored.csv", "batch_id")
    inventory = load("inventory_clean.csv", "batch_id")
    skus = load("sku_master.csv", "sku")

    with open(ROOT / "action_queue.csv", newline="", encoding="utf-8") as f:
        queue = list(csv.DictReader(f))

    rows = []
    for q in queue:
        b = q["batch_id"]
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
            "clause_ids": q["clause_ids"].replace(";", ", "),
            "status": q["status"],
            "reason": q["hold_reason"],
            "approver": q["approver"],
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
    top_five = sorted(scored_rows, key=lambda r: r["score"], reverse=True)[:5]
    top_five_ids = [r["batch_id"] for r in top_five]

    data = json.dumps({"rows": rows, "summary": summary, "top_five": top_five_ids})
    data = data.replace("</", "<\\/")

    template = (ROOT / "tools" / "dashboard_template.html").read_text(encoding="utf-8")
    out = template.replace("__DATA__", data)
    (ROOT / "dashboard.html").write_text(out, encoding="utf-8")
    print(f"Wrote dashboard.html: {summary}")


if __name__ == "__main__":
    main()
