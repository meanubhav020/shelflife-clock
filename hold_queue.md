# Hold queue

## LF-70001
- Action: MARKDOWN
- Clauses: REF-ACT-03, REF-ACT-06, REF-APR-02
- Reason: Batch value $12,000 is above $2,000
- Approver: Finance Director

## LF-70003
- Action: none (escalated, no disposition proposed)
- Clauses: REF-HC-04, REF-APR-01
- Reason: HEALTHCARE (sku_master.csv; row label says FOOD) with 12 days remaining, cannot transfer (fewer than 21 days) or return (supplier_accepts_returns is N)
- Approver: QA Lead

## LF-70004
- Action: none
- Clauses: REF-APR-04
- Reason: data check flag not OK (MISSING_EXPIRY)
- Approver: Inventory Control

## LF-70009
- Action: DISPOSE (quarantine and destroy through licensed disposal vendor)
- Clauses: REF-HC-03, REF-ACT-05, REF-APR-01, REF-APR-02, REF-APR-03
- Reason: HEALTHCARE, expired (3 days past expiry), batch value $2,400 (above $2,000); disposal fee not in docs/
- Approvers: QA Lead, Regional Manager, Finance

## LF-70010
- Action: none
- Clauses: REF-APR-04
- Reason: data check flag not OK (STALE_COUNT)
- Approver: Inventory Control

## LF-11887
- Action: DISPOSE (destruction and write-off, expired stock)
- Clauses: REF-ACT-05, REF-APR-03
- Reason: action is DISPOSE (expired, 9 days past expiry)
- Approver: Finance

## LF-10729
- Action: DISPOSE (destruction and write-off, expired stock)
- Clauses: REF-ACT-05, REF-APR-03
- Reason: action is DISPOSE (expired, 4 days past expiry)
- Approver: Finance

## LF-10629
- Action: none (escalated, no disposition proposed)
- Clauses: REF-HC-04, REF-APR-01
- Reason: HEALTHCARE with 13 days remaining, cannot transfer (no target location with higher sales) or return (fewer than 30 days remain)
- Approver: QA Lead
