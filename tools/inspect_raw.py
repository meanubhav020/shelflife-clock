import csv
import re
from collections import Counter, defaultdict

rows = []
with open("inventory_raw.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

print(f"Total rows: {len(rows)}")

# duplicate batch_id
ids = Counter(r["batch_id"] for r in rows)
dupes = [b for b, c in ids.items() if c > 1]
print(f"\nDuplicate batch_id values: {len(dupes)}")
for b in dupes[:20]:
    print(" ", b)

# date format check on received_date and expiry_date
def date_shape(v):
    if v == "":
        return "blank"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", v):
        return "iso"
    if re.fullmatch(r"\d{2}/\d{2}/\d{4}", v):
        return "slash"
    return "other:" + v

for col in ("received_date", "expiry_date", "last_counted_date"):
    shapes = Counter(date_shape(r[col]) for r in rows)
    print(f"\n{col} shapes: {dict(shapes)}")
    if shapes.get("blank"):
        blanks = [r["batch_id"] for r in rows if r[col] == ""]
        print(f"  blank {col} batch_ids ({len(blanks)}):", blanks[:20])

# negative units_on_hand
neg = [r["batch_id"] for r in rows if r["units_on_hand"] not in ("",) and float(r["units_on_hand"]) < 0]
print(f"\nNegative units_on_hand rows: {len(neg)}")
print(" ", neg[:20])

# category_label values seen
labels = Counter(r["category_label"] for r in rows)
print(f"\ncategory_label values: {dict(labels)}")

# stale last_counted_date (more than 45 days before 2026-09-21)
from datetime import date
AS_OF = date(2026, 9, 21)
stale = []
for r in rows:
    y, m, d = map(int, r["last_counted_date"].split("-"))
    age = (AS_OF - date(y, m, d)).days
    if age > 45:
        stale.append((r["batch_id"], age))
print(f"\nlast_counted_date more than 45 days old: {len(stale)}")
print(" ", [b for b, a in stale][:20])

# category_label vs sku_master.csv product_class
sku_class = {}
with open("sku_master.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        sku_class[r["sku"]] = r["product_class"]

def broad(pc):
    return "HEALTHCARE" if pc == "HEALTHCARE" else "FOOD"

mismatches = [r["batch_id"] for r in rows if r["sku"] in sku_class and broad(sku_class[r["sku"]]) != r["category_label"]]
print(f"\ncategory_label disagrees with sku_master.csv product_class (FOOD vs HEALTHCARE): {len(mismatches)}")
print(" ", mismatches[:20])
