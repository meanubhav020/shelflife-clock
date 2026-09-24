import csv
from datetime import date

AS_OF = date(2026, 9, 21)


def parse_date(s):
    if not s:
        return None
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)


def days_weight(days_to_expiry):
    if days_to_expiry <= 7:
        return 1.0
    if days_to_expiry <= 14:
        return 0.8
    if days_to_expiry <= 30:
        return 0.5
    return 0.2


sku_cost = {}
with open("sku_master.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        sku_cost[r["sku"]] = float(r["unit_cost_usd"])

with open("inventory_clean.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

out_rows = []
for r in rows:
    unit_cost = sku_cost.get(r["sku"], 0.0)
    units = float(r["units_on_hand"])
    batch_value = units * unit_cost

    expiry_str = r["expiry_date"]
    unclear_expiry = expiry_str == "" or "DATE_AMBIGUOUS" in r["trust_flag"]

    row = {
        "batch_id": r["batch_id"],
        "sku": r["sku"],
        "location_id": r["location_id"],
        "product_class": r["product_class"],
        "trust_flag": r["trust_flag"],
        "units_on_hand": r["units_on_hand"],
        "unit_cost_usd": unit_cost,
        "days_to_expiry": "",
        "in_scope": "",
        "days_weight": "",
        "unsold_share": "",
        "batch_value": round(batch_value, 2),
        "score": "",
        "band": "",
    }

    if unclear_expiry:
        out_rows.append(row)
        continue

    expiry = parse_date(expiry_str)
    days_to_expiry = (expiry - AS_OF).days
    row["days_to_expiry"] = days_to_expiry

    in_scope = days_to_expiry <= 60
    row["in_scope"] = "Y" if in_scope else "N"

    if not in_scope:
        out_rows.append(row)
        continue

    weight = days_weight(days_to_expiry)
    row["days_weight"] = weight

    sold = float(r["units_sold_last_30d"])
    if days_to_expiry <= 0:
        unsold_share = 1.0
    else:
        unsold_share = max(0.0, 1 - ((sold / 30) * days_to_expiry / units))
    row["unsold_share"] = round(unsold_share, 4)

    score = batch_value * weight * unsold_share
    row["score"] = round(score, 2)

    if score >= 5000:
        band = "P1"
    elif score >= 1000:
        band = "P2"
    else:
        band = "P3"
    row["band"] = band

    out_rows.append(row)


def sort_key(r):
    return r["score"] if r["score"] != "" else -1


out_rows.sort(key=sort_key, reverse=True)

fieldnames = ["batch_id", "sku", "location_id", "product_class", "trust_flag",
              "units_on_hand", "unit_cost_usd", "days_to_expiry", "in_scope",
              "days_weight", "unsold_share", "batch_value", "score", "band"]

with open("scored.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(out_rows)

in_scope_count = sum(1 for r in out_rows if r["in_scope"] == "Y")
print(f"Wrote scored.csv with {len(out_rows)} rows")
print(f"In scope: {in_scope_count}")
print()
for r in out_rows[:10]:
    print(r)
