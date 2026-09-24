# Baseline: LF-70006 (Step 1, before subagent)

- Batch: LF-70006
- SKU: SKU-1096, Long-life greek yoghurt 4 pack
- Class: FOOD_CHILLED (from sku_master.csv, not the row label)
- Location: LOC-20, West Store 20 (cold_chain Y)
- Trust flag: OK
- Days to expiry: 24
- Batch value: $1800.0
- Score: 828.0, band P3

## Action

TRANSFER to LOC-12 (West Store 12).

- LOC-12 already stocks SKU-1096 with higher recent sales (150 units sold in last 30
  days vs 30 for this batch's location) [REF-ACT-02].
- 24 days remain, at or above the 21-day minimum for transfer [REF-ACT-02].
- LOC-12 has cold_chain = Y, required for FOOD_CHILLED [REF-CC-01].
- TRANSFER is first in the order of preference when more than one action is eligible
  [REF-ACT-06].

(RETURN TO SUPPLIER was also possible in principle, but TRANSFER outranks it under
REF-ACT-06, so it was not pursued further.)

## Approval

No human approval required. Not HEALTHCARE, batch value $1800 is not above $2,000,
not a DISPOSE action, and trust flag is OK, so none of REF-APR-01 to REF-APR-04 apply.
Released under REF-APR-05.

## Status

READY
