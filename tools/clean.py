import csv
from datetime import date, timedelta

AS_OF = date(2026, 9, 21)
STALE_DAYS = 45

sku_master = {}
with open("sku_master.csv", newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        sku_master[r["sku"]] = r


def broad_class(product_class):
    return "HEALTHCARE" if product_class == "HEALTHCARE" else "FOOD"


def parse_iso(s):
    y, m, d = map(int, s.split("-"))
    return date(y, m, d)


def parse_slash(s, received, shelf_life_days):
    """Returns (iso_string_or_None, ambiguous_bool)."""
    a, b, y = (int(x) for x in s.split("/"))
    if a >= 13:
        return date(y, b, a).isoformat(), False
    candidates = []
    for cand in ((a, b), (b, a)):  # (day, month) readings: DMY, MDY
        day, month = cand
        try:
            candidates.append(date(y, month, day))
        except ValueError:
            pass
    candidates = list(set(candidates))
    expected = received + timedelta(days=shelf_life_days)
    matches = [c for c in candidates if abs((c - expected).days) <= 3]
    if len(matches) == 1:
        return matches[0].isoformat(), False
    return None, True


with open("inventory_raw.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

log_lines = []


def log(batch_id, field, was, now, why):
    log_lines.append((batch_id, field, was, now, why))


# 1. Duplicates: keep the copy with the latest last_counted_date
by_id = {}
removed_dupes = []
for r in rows:
    bid = r["batch_id"]
    if bid not in by_id:
        by_id[bid] = r
    else:
        prev = by_id[bid]
        if r["last_counted_date"] >= prev["last_counted_date"]:
            removed_dupes.append(prev)
            by_id[bid] = r
        else:
            removed_dupes.append(r)

for r in removed_dupes:
    log(r["batch_id"], "row", "duplicate row present", "removed", "DECISION 2.1: kept copy with latest last_counted_date")

rows = list(by_id.values())

out_rows = []
for r in rows:
    row = dict(r)
    flags = []

    # 2. Product class from sku_master.csv, drop category_label
    sku = row["sku"]
    master = sku_master.get(sku)
    product_class = master["product_class"] if master else ""
    if master and broad_class(product_class) != row["category_label"]:
        log(row["batch_id"], "product_class", row["category_label"], product_class,
            "label disagreed with sku_master.csv, master file used")
    row["product_class"] = product_class
    del row["category_label"]

    # 3. Dates: convert DD/MM/YYYY to YYYY-MM-DD
    expiry = row["expiry_date"]
    if expiry == "":
        flags.append("MISSING_EXPIRY")
        log(row["batch_id"], "expiry_date", "", "", "blank, flagged MISSING_EXPIRY, not guessed")
    elif "/" in expiry:
        received = parse_iso(row["received_date"])
        shelf_life = int(master["shelf_life_days"]) if master else None
        converted, ambiguous = (None, True)
        if shelf_life is not None:
            converted, ambiguous = parse_slash(expiry, received, shelf_life)
        if ambiguous:
            flags.append("DATE_AMBIGUOUS")
            log(row["batch_id"], "expiry_date", expiry, expiry,
                "ambiguous DD/MM vs MM/DD, no single shelf-life match, flagged DATE_AMBIGUOUS")
        else:
            log(row["batch_id"], "expiry_date", expiry, converted,
                "slash date converted to ISO (unambiguous, or matched received date + shelf life)")
            row["expiry_date"] = converted

    # 5. Quantities
    units = row["units_on_hand"]
    if units != "" and float(units) < 0:
        flags.append("QTY_SUSPECT")
        log(row["batch_id"], "units_on_hand", units, units, "negative, flagged QTY_SUSPECT, not changed")

    counted = parse_iso(row["last_counted_date"])
    age = (AS_OF - counted).days
    if age > STALE_DAYS:
        flags.append("STALE_COUNT")
        log(row["batch_id"], "last_counted_date", row["last_counted_date"], row["last_counted_date"],
            f"count is {age} days old, more than {STALE_DAYS} days, flagged STALE_COUNT")

    row["trust_flag"] = "+".join(flags) if flags else "OK"
    out_rows.append(row)

fieldnames = ["batch_id", "sku", "product_class", "location_id", "units_on_hand",
              "received_date", "expiry_date", "units_sold_last_30d", "last_counted_date",
              "trust_flag"]

with open("inventory_clean.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in out_rows:
        writer.writerow({k: row[k] for k in fieldnames})

with open("changes.md", "w", encoding="utf-8") as f:
    f.write("# Change log\n\n")
    f.write("Every row removed, changed or flagged while cleaning inventory_raw.csv into inventory_clean.csv.\n\n")
    f.write("| batch_id | field | was | now | why |\n")
    f.write("|---|---|---|---|---|\n")
    for bid, field, was, now, why in log_lines:
        f.write(f"| {bid} | {field} | {was} | {now} | {why} |\n")

print(f"Wrote inventory_clean.csv with {len(out_rows)} rows")
print(f"Wrote changes.md with {len(log_lines)} log lines")
