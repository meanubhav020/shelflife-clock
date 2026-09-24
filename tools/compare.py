import csv

with open("inventory_raw.csv", newline="", encoding="utf-8") as f:
    raw_rows = list(csv.DictReader(f))
with open("inventory_clean.csv", newline="", encoding="utf-8") as f:
    clean_rows = list(csv.DictReader(f))

raw_by_id = {}
for r in raw_rows:
    raw_by_id.setdefault(r["batch_id"], []).append(r)

clean_by_id = {r["batch_id"]: r for r in clean_rows}

removed = sum(len(variants) - 1 for variants in raw_by_id.values() if len(variants) > 1)

changed = 0
unchanged = 0
for bid, r in clean_by_id.items():
    raw_variants = raw_by_id.get(bid, [])
    if not raw_variants:
        continue
    raw_r = raw_variants[-1] if len(raw_variants) > 1 else raw_variants[0]
    is_changed = (
        raw_r["expiry_date"] != r["expiry_date"]
        or r["trust_flag"] != "OK"
    )
    if is_changed:
        changed += 1
    else:
        unchanged += 1

flagged = sum(1 for r in clean_rows if r["trust_flag"] != "OK")

print(f"raw rows: {len(raw_rows)}")
print(f"clean rows: {len(clean_rows)}")
print(f"rows removed (duplicates): {removed}")
print(f"rows changed (expiry date rewritten or flagged): {changed}")
print(f"rows unchanged: {unchanged}")
print(f"rows with trust_flag != OK: {flagged}")
