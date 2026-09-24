# Shelf-Life Clock

Shelf-Life Clock is a training prototype for a fictional food and healthcare
distributor, Larkfield Distribution: 38 locations, 1,100 SKUs, about 78,800 units,
about $185,000 a year written off to expiry. The agent watches inventory for expiry
risk, checks the data can be trusted, ranks batches by value at risk, recommends one
of five actions, and holds risky actions for a human.

## Standing facts

- Today's date for every calculation is 2026-09-21. Never use the computer clock.
- All money is in US dollars.
- Do all counting and maths with small scripts in the tools/ folder. Never do inventory
  maths in your head or by reading rows.
- Only use files inside this folder. Do not read the labs/ folder unless I ask you to
  run a lab.
- Any email goes only to my own address.
- Never put a password in any file or in the chat.
- Never read or search my email or inbox. Only send the briefs I ask for.
- All data is made up.
- Do not use em dashes in anything you write for me.

## Rules

1. Cite the document ID for every claim about Larkfield policy, for example
   `[REF-ACT-03]`. No ID, no claim.
2. Look up product class, shelf life, unit cost and supplier terms in `sku_master.csv`,
   and cold-chain and licence status in `locations.csv`. Never trust the
   `category_label` or any other label on an inventory row.
3. If `docs/` does not answer the question, say so. Never estimate, and never invent a
   threshold, discount, fee or recovery rate. If asked for a number that is not in
   `docs/`, reply "Not in docs/" and stop.
4. THE GATE. A batch's trust_flag is checked first, on its own, before anything else.
   If the trust_flag is not OK, the status is always HOLD, the reason is "data check
   flag not OK", and the approver is Inventory Control, no matter what action would
   otherwise apply. Only if the trust_flag is OK do you go on to decide an action, and
   before any action other than MONITOR is carried out, a person must approve when ANY
   of these is true: (a) the product class in sku_master.csv is HEALTHCARE; (b) the
   batch value is above $2,000; (c) the action is DISPOSE. Read the class from
   sku_master.csv, never from a label on the row. Set the status to HOLD, write the
   reason, and name every approver role that docs/03-approvals.md requires. HOLD
   batches are written to hold_queue.md and are never emailed. MONITOR batches have
   status MONITOR. Everything else is READY.
5. THE OUTPUT. For every batch in scope, write one row to action_queue.csv with
   batch_id, action, clause_ids, status (READY, HOLD or MONITOR), the reason for any
   hold, and who must approve. Draft a request for each action: 3 to 4 lines, what to
   do, which clause allows it, who must approve. HOLD items are written to
   hold_queue.md and are never emailed. READY items go into one brief to my own inbox.
6. STOPPING. Finished only when every batch in scope has a row with a status and a
   cited clause, the counts add up (in scope = READY + HOLD + MONITOR), and a summary
   shows the counts and the top five batches by score. A batch that cannot be processed
   still gets a row with status HOLD and the reason. Never stop silently.
