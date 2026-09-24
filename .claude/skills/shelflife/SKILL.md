---
name: shelflife
description: Assess one at-risk batch against docs/ and the master files, with citations and a gate decision
---

For the batch ID I give you:
1. Look it up in inventory_clean.csv and read its trust_flag.
2. Look up the SKU in sku_master.csv and the location in locations.csv. Ignore any label on the row.
3. Get days to expiry, value, score and band from scored.csv. If scored.csv is missing or older than
   inventory_clean.csv, run tools/score.py first. Never calculate these yourself.
4. Using only docs/, choose MONITOR, TRANSFER, RETURN TO SUPPLIER, MARKDOWN or DISPOSE using the order of
   preference in REF-ACT-06, and name the clause that makes it allowed. If none is allowed, the action is
   MONITOR and you say why.
5. Say who must approve and which clause says so. If the trust_flag is not OK, take no action, say so, and
   cite REF-APR-04.
6. If docs/ does not answer something, write "Not in docs/". Never estimate.
7. Once the action, clause and approver are settled, hand the writing of the request to the
   action-drafter subagent. Give it only three things: the batch facts (id, description, units, days to
   expiry, value, score, band), the product class, and the exact clause text (the action clause and, if
   approval is needed, the approval clause). Do not give it docs/, the CSV files, or this conversation.
   Show me exactly what you gave it before showing its output.
8. Show: batch, class, trust flag, days to expiry, value, score, band, action, clause IDs, approvers, and
   the action-drafter's request.
