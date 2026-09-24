import csv
from collections import defaultdict, Counter

with open("inventory_raw.csv", newline="") as f:
    rows = list(csv.DictReader(f))

with open("sku_master.csv", newline="") as f:
    sku_master = {r["sku"]: r for r in csv.DictReader(f)}

print(f"Total rows: {len(rows)}")

# 1. Duplicate batch_id
by_batch = defaultdict(list)
for r in rows:
    by_batch[r["batch_id"]].append(r)
dupes = {b: rs for b, rs in by_batch.items() if len(rs) > 1}
print(f"\nDuplicate batch_id groups: {len(dupes)}")
for b in list(dupes)[:5]:
    print(f"  {b}: {len(dupes[b])} copies")

# 2. Product class mismatch vs sku_master
mismatch = []
for r in rows:
    master = sku_master.get(r["sku"])
    if master and r["category_label"] != master["product_class"]:
        mismatch.append(r["batch_id"])
print(f"\ncategory_label vs sku_master product_class mismatches: {len(mismatch)}")

# 3. Date format check - look for DD/MM/YYYY style dates in any date column
import re
slash_date = re.compile(r"^\d{2}/\d{2}/\d{4}$")
date_cols = ["received_date", "expiry_date", "last_counted_date"]
slash_rows = defaultdict(list)
for r in rows:
    for c in date_cols:
        if slash_date.match(r[c] or ""):
            slash_rows[c].append(r["batch_id"])
for c, bs in slash_rows.items():
    print(f"\n{c} in DD/MM/YYYY format: {len(bs)} rows, e.g. {bs[:5]}")

# 4. Blank expiry_date
blank_expiry = [r["batch_id"] for r in rows if not r["expiry_date"].strip()]
print(f"\nBlank expiry_date: {len(blank_expiry)} rows, e.g. {blank_expiry[:5]}")

# 5. Negative units_on_hand
neg_units = [r["batch_id"] for r in rows if r["units_on_hand"].strip().startswith("-")]
print(f"\nNegative units_on_hand: {len(neg_units)} rows, e.g. {neg_units[:5]}")

# 6. sku not in master
missing_sku = [r["batch_id"] for r in rows if r["sku"] not in sku_master]
print(f"\nSKUs not found in sku_master.csv: {len(missing_sku)}")
