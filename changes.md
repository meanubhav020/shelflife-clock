# Change log

Every row removed, changed or flagged while cleaning inventory_raw.csv into inventory_clean.csv.

| batch_id | field | was | now | why |
|---|---|---|---|---|
| LF-11409 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-70005 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10176 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10663 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10850 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10425 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10938 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-11326 | row | duplicate row present | removed | DECISION 2.1: kept copy with latest last_counted_date |
| LF-10738 | expiry_date | 10/01/2027 | 2027-01-10 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-11196 | expiry_date | 13/10/2026 | 2026-10-13 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-11762 | last_counted_date | 2026-07-11 | 2026-07-11 | count is 72 days old, more than 45 days, flagged STALE_COUNT |
| LF-11623 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-11918 | units_on_hand | -9 | -9 | negative, flagged QTY_SUSPECT, not changed |
| LF-11048 | expiry_date | 12/01/2027 | 12/01/2027 | ambiguous DD/MM vs MM/DD, no single shelf-life match, flagged DATE_AMBIGUOUS |
| LF-70010 | last_counted_date | 2026-07-21 | 2026-07-21 | count is 62 days old, more than 45 days, flagged STALE_COUNT |
| LF-10214 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-10887 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11855 | expiry_date | 06/01/2027 | 2027-01-06 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10834 | expiry_date | 21/08/2027 | 2027-08-21 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-11905 | expiry_date | 19/10/2027 | 2027-10-19 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10553 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-10464 | expiry_date | 20/11/2026 | 2026-11-20 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-11916 | expiry_date | 04/12/2026 | 2026-12-04 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-70003 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-11228 | expiry_date | 03/08/2027 | 03/08/2027 | ambiguous DD/MM vs MM/DD, no single shelf-life match, flagged DATE_AMBIGUOUS |
| LF-10626 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-10242 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-11246 | units_on_hand | -24 | -24 | negative, flagged QTY_SUSPECT, not changed |
| LF-11382 | units_on_hand | -18 | -18 | negative, flagged QTY_SUSPECT, not changed |
| LF-11692 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-10723 | last_counted_date | 2026-07-25 | 2026-07-25 | count is 58 days old, more than 45 days, flagged STALE_COUNT |
| LF-10867 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11920 | last_counted_date | 2026-07-08 | 2026-07-08 | count is 75 days old, more than 45 days, flagged STALE_COUNT |
| LF-11307 | expiry_date | 12/04/2027 | 2027-04-12 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10900 | expiry_date | 26/10/2027 | 2027-10-26 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-11479 | expiry_date | 12/09/2027 | 2027-09-12 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10407 | last_counted_date | 2026-07-09 | 2026-07-09 | count is 74 days old, more than 45 days, flagged STALE_COUNT |
| LF-70004 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11606 | last_counted_date | 2026-06-30 | 2026-06-30 | count is 83 days old, more than 45 days, flagged STALE_COUNT |
| LF-11546 | expiry_date | 28/09/2027 | 2027-09-28 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10844 | last_counted_date | 2026-07-26 | 2026-07-26 | count is 57 days old, more than 45 days, flagged STALE_COUNT |
| LF-10934 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11637 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-10232 | last_counted_date | 2026-06-14 | 2026-06-14 | count is 99 days old, more than 45 days, flagged STALE_COUNT |
| LF-10706 | expiry_date | 07/01/2027 | 07/01/2027 | ambiguous DD/MM vs MM/DD, no single shelf-life match, flagged DATE_AMBIGUOUS |
| LF-11740 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-10612 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
| LF-11555 | units_on_hand | -5 | -5 | negative, flagged QTY_SUSPECT, not changed |
| LF-11498 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11357 | expiry_date |  |  | blank, flagged MISSING_EXPIRY, not guessed |
| LF-11742 | units_on_hand | -27 | -27 | negative, flagged QTY_SUSPECT, not changed |
| LF-11507 | expiry_date | 07/12/2026 | 2026-12-07 | slash date converted to ISO (unambiguous, or matched received date + shelf life) |
| LF-10400 | product_class | FOOD | HEALTHCARE | label disagreed with sku_master.csv, master file used |
