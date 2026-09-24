import csv
import re
from collections import defaultdict

with open("inventory_raw.csv", newline="") as f:
    rows = list(csv.DictReader(f))

with open("sku_master.csv", newline="") as f:
    sku_master = {r["sku"]: r for r in csv.DictReader(f)}

with open("locations.csv", newline="") as f:
    locations = {r["location_id"]: r for r in csv.DictReader(f)}

print(f"Total rows: {len(rows)}")

# 1. Duplicate batch_id
by_batch = defaultdict(list)
for r in rows:
    by_batch[r["batch_id"]].append(r)
dupes = {b: rs for b, rs in by_batch.items() if len(rs) > 1}
print(f"\nDuplicate batch_id: {len(dupes)} batch_ids appear more than once, {sum(len(v) for v in dupes.values())} rows total")
print(f"  batch_ids: {', '.join(sorted(dupes))}")

# 2. category_label vs sku_master.product_class mismatch
mismatches = []
for r in rows:
    sku = sku_master.get(r["sku"])
    if sku and r["category_label"] != sku["product_class"]:
        mismatches.append(r["batch_id"])
print(f"\ncategory_label disagrees with sku_master.product_class: {len(mismatches)} rows")
print(f"  batch_ids (first 20 of {len(mismatches)}): {', '.join(sorted(mismatches)[:20])}")

# 3. Slash-style dates (DD/MM/YYYY) in date columns
slash_date = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")
date_cols = ["received_date", "expiry_date", "last_counted_date"]
slash_hits = defaultdict(list)
for r in rows:
    for col in date_cols:
        if slash_date.match(r[col] or ""):
            slash_hits[col].append(r["batch_id"])
for col, ids in slash_hits.items():
    print(f"\nSlash-format dates in {col}: {len(ids)} rows")
    print(f"  batch_ids: {', '.join(sorted(ids))}")

# 4. Blank expiry_date
blanks = [r["batch_id"] for r in rows if not r["expiry_date"].strip()]
print(f"\nBlank expiry_date: {len(blanks)} rows")
print(f"  batch_ids: {', '.join(sorted(blanks))}")

# 5. Negative units_on_hand
neg = [r["batch_id"] for r in rows if r["units_on_hand"].strip().startswith("-")]
print(f"\nNegative units_on_hand: {len(neg)} rows")
print(f"  batch_ids: {', '.join(sorted(neg))}")

# 6. Unknown sku / location references
bad_sku = [r["batch_id"] for r in rows if r["sku"] not in sku_master]
bad_loc = [r["batch_id"] for r in rows if r["location_id"] not in locations]
print(f"\nSKU not found in sku_master: {len(bad_sku)} rows")
print(f"location_id not found in locations: {len(bad_loc)} rows")

# 7. last_counted_date staleness check (relative to 2026-09-21), just flag old ones for visibility
old_counted = []
from datetime import date
today = date(2026, 9, 21)
for r in rows:
    d = r["last_counted_date"].strip()
    if re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        y, m, dd = map(int, d.split("-"))
        age = (today - date(y, m, dd)).days
        if age > 45:
            old_counted.append((r["batch_id"], age))
print(f"\nlast_counted_date more than 45 days before {today}: {len(old_counted)} rows")
print(f"  batch_ids: {', '.join(sorted(b for b, a in old_counted))}")
