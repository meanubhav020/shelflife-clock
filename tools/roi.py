import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# [REF-FIN-02] Planning recovery rates, as a share of batch value.
RECOVERY_RATES = {
    "TRANSFER": 0.90,
    "RETURN TO SUPPLIER": {"FOOD_AMBIENT": 0.80, "FOOD_CHILLED": 0.80, "HEALTHCARE": 0.90},
    "MARKDOWN": 0.60,
    "DISPOSE": 0.0,
    "MONITOR": 0.0,
}


def recovery_rate(action, product_class):
    if not action or action not in RECOVERY_RATES:
        return 0.0
    rate = RECOVERY_RATES[action]
    if isinstance(rate, dict):
        return rate.get(product_class, 0.0)
    return rate


def main():
    with open(ROOT / "notes" / "sample.txt") as f:
        sample = [line.strip() for line in f if line.strip()]

    with open(ROOT / "action_queue.csv", newline="") as f:
        queue = {r["batch_id"]: r for r in csv.DictReader(f)}

    with open(ROOT / "scored.csv", newline="") as f:
        scored = {r["batch_id"]: r for r in csv.DictReader(f)}

    with open(ROOT / "inventory_clean.csv", newline="") as f:
        inventory = {r["batch_id"]: r for r in csv.DictReader(f)}

    with open(ROOT / "sku_master.csv", newline="") as f:
        sku_master = {r["sku"]: r for r in csv.DictReader(f)}

    total_recovered = 0.0
    total_at_risk = 0.0
    rows = []

    for batch_id in sample:
        q = queue.get(batch_id)
        s = scored.get(batch_id)
        inv = inventory.get(batch_id)
        if q is None or s is None or inv is None:
            print(f"WARNING: {batch_id} missing from one of the inputs, skipping.")
            continue

        trust_flag = inv["trust_flag"]
        batch_value = float(s["batch_value"])
        unsold_share = float(s["unsold_share"]) if s["unsold_share"] else 0.0
        value_at_risk = batch_value * unsold_share

        if trust_flag != "OK":
            rate = 0.0
            recovered = 0.0
        else:
            sku_row = sku_master.get(inv["sku"], {})
            product_class = sku_row.get("product_class", "")
            action = q["action"]
            rate = recovery_rate(action, product_class)
            recovered = value_at_risk * rate

        total_at_risk += value_at_risk
        total_recovered += recovered

        rows.append({
            "batch_id": batch_id,
            "trust_flag": trust_flag,
            "action": q["action"] or "(none)",
            "batch_value": batch_value,
            "unsold_share": unsold_share,
            "value_at_risk": value_at_risk,
            "recovery_rate": rate,
            "recovered": recovered,
        })

    r = total_recovered / total_at_risk if total_at_risk else 0.0

    print(f"Batches: {len(rows)}")
    print(f"Total value at risk: ${total_at_risk:,.2f}")
    print(f"Total value recovered: ${total_recovered:,.2f}")
    print(f"R = {r:.4f} ({r*100:.2f}%)")
    print()
    print(f"{'batch_id':<10} {'trust':<7} {'action':<20} {'value':>10} {'unsold':>7} {'at_risk':>10} {'rate':>6} {'recovered':>10}")
    for row in rows:
        print(f"{row['batch_id']:<10} {row['trust_flag']:<7} {row['action']:<20} "
              f"{row['batch_value']:>10,.2f} {row['unsold_share']:>7.4f} {row['value_at_risk']:>10,.2f} "
              f"{row['recovery_rate']:>6.2f} {row['recovered']:>10,.2f}")


if __name__ == "__main__":
    main()
