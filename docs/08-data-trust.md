FICTIONAL POLICY, FOR TRAINING USE ONLY

# Data trust

[REF-DATA-01] Duplicates. If a batch_id appears more than once in inventory_raw.csv, keep the copy with the latest last_counted_date and remove the others.

[REF-DATA-02] Product class. product_class always comes from sku_master.csv, never from the category_label on the inventory row. Any row where the label disagreed with the master file is logged.

[REF-DATA-03] Date formats. Convert DD/MM/YYYY to YYYY-MM-DD. If the first number is 13 or more, the reading is unambiguous and is converted. If the first number is 12 or less, convert it only if exactly one reading (day-month or month-day) falls within 3 days of received_date plus the SKU's shelf_life_days from sku_master.csv. Otherwise leave the original text and flag DATE_AMBIGUOUS.

[REF-DATA-04] Blank expiry dates. A blank expiry_date is left blank and flagged MISSING_EXPIRY. It is never worked out from shelf life.

[REF-DATA-05] Negative quantities and old counts. A negative units_on_hand is flagged QTY_SUSPECT and never changed. A last_counted_date more than 45 days before 2026-09-21 is flagged STALE_COUNT.
