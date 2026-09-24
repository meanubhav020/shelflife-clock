# Hold queue

## LF-70001
- Action: MARKDOWN [REF-ACT-03]
- Reason: batch value $12,000 is above $2,000 [REF-APR-02]
- Approver: Finance Director (value above $10,000)

## LF-70003
- Action: none proposed, escalated [REF-HC-04]
- Reason: HEALTHCARE per sku_master.csv (row label says FOOD), 12 days remaining,
  cannot transfer (fewer than 21 days) or return to supplier
  (supplier_accepts_returns is N)
- Approver: QA Lead [REF-APR-01]

## LF-70004
- Action: not decided, trust check stops before an action is chosen
- Reason: data check flag not OK (MISSING_EXPIRY) [REF-APR-04]
- Approver: Inventory Control

## LF-70009
- Action: DISPOSE, destruction and write-off [REF-ACT-05]
- Reason: HEALTHCARE (sku_master.csv), 3 days past expiry, batch value $2,400
  (above $2,000)
- Approver: QA Lead [REF-APR-01]; Regional Manager [REF-APR-02]; Finance [REF-APR-03]

## LF-70010
- Action: not decided, trust check stops before an action is chosen
- Reason: data check flag not OK (STALE_COUNT) [REF-APR-04]
- Approver: Inventory Control
