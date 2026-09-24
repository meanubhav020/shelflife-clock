# Shelf-Life Clock

## The problem

Every year about $185,000 of stock is written off because it expired before it sold
(notes/roi.md). Nobody catches every at-risk batch in time by looking at spreadsheets
by hand. This project is a training prototype for an agent that watches the stock file,
flags what is about to expire, and recommends what to do about it before it is too
late.

All data and policy in this project are made up. Nothing here describes a real
company or a real product.

## The loop

1. Watch the stock: read the inventory file.
2. Check the data can be trusted: look at each batch's data check flag before doing
   anything else.
3. Rank by value at risk: score each batch by how much money is exposed and how soon
   it expires.
4. Recommend an action: pick one of five moves (transfer, return to supplier,
   markdown, dispose, or just keep watching) using only the written rulebook, and hold
   it for a person to approve if the rules say so.

## How the pieces fit

```
inventory_raw.csv
      |
      v
  clean.py  --> inventory_clean.csv (dedupes, fixes dates, sets the data check flag)
      |
      v
  score.py  --> scored.csv (value at risk, score, priority band)
      |
      v
  /shelflife skill, one batch at a time
      |
      |-- reads docs/ (the rulebook) and sku_master.csv / locations.csv (the master
      |   files, never the row's own label)
      |-- decides action, clause, approver
      |-- hands three facts only to the action-drafter helper: batch facts, product
      |   class, clause text
      v
  action_queue.csv  and  hold_queue.md
      |
      v
  pre_send_check.py (the safety check)  --> outbox/ (only READY items, only to the
                                              owner's own address)
```

## Why each design choice was made

- **Scripts do the maths.** Counting, scoring and totals are done by small scripts in
  tools/, never worked out by reading rows. A wrong sum by eye is easy to miss; a
  script gives the same answer every time and can be checked.
- **The helper agent sees only three inputs.** The action-drafter that writes each
  request is given only the batch facts, the product class, and the exact clause text,
  never the full rulebook, the CSV files, or the conversation. This keeps its output
  tied to what it was actually told, not to guesses filled in from context it should
  not have.
- **The gate reads the master file, not the row.** A batch's own label (on the
  inventory row) is never trusted for its product class. The class always comes from
  sku_master.csv. This is because rows can carry the wrong label, and getting a
  healthcare item marked down like food is a real risk in that world.
- **The safety check is separate from the rulebook.** Whether a batch is allowed to be
  sent lives in its own script (hooks/pre_send_check.py), not inside the rules the
  agent reasons with in plain language. A check that runs as code every time is harder
  to talk an agent past than a rule in a prompt.
- **Only READY items can be sent.** HOLD items go to hold_queue.md and are never
  emailed or put in the outbox. The safety check enforces this by re-checking status,
  trust flag, class, value and action before anything is sent, even if the agent's own
  reasoning already said READY.

## Choices made (notes/journal.md)

- Approval gate: healthcare, batch value above $2,000, DISPOSE, or a bad data check
  flag all need a person to approve.
- Action requests are short: 3 to 4 lines, the action, the clause, who approves.
- Stopping rule: every batch needs a row, a cited clause, counts that add up, and a
  top-five-by-score summary.
- Duplicate rows: keep the one with the latest count date.
- Ambiguous dates: work them out from the received date and shelf life if exactly one
  reading fits within 3 days, otherwise flag it rather than guess.
- Stale count threshold: 45 days.
- The agent sends through an outbox folder (a saved text file), not a real email
  account.
- The READY brief is a plain list: one line per batch with its action and clause ID.
- The ROI sample size started at 20 (the recommended option) and was rerun at 50
  batches on request.
- Base case acting rate (the share of recommendations people actually carry out): 60
  percent.
- The assumption most likely to break the ROI number: people not acting in time.

## How to run it

- Run `/shelflife LF-XXXXX` on one batch at a time to get its action, clause and
  approver.
- Run `tools/score.py` after the inventory changes to refresh scored.csv.
- Run `tools/roi.py` to work out the recovery rate R for a sample of batches listed in
  notes/sample.txt.
- Sends only happen through `tools/send_brief.py`, and only to the owner's own
  address; hooks/pre_send_check.py blocks anything that should not go out.

## Results (notes/lab6-failures.md, notes/roi.md)

- Ten batches were built to each trip up one specific mistake. All ten matched the
  answer key: right action, right clause, right status, right score. No fixes were
  needed.
- The READY-only brief arrived correctly. A brief listing every batch, including
  HOLD ones, was blocked by the safety check, which named the first batch that broke
  the rules.
- A random sample of 50 in-scope batches (seed 7) was run for the ROI. This is a small
  sample: 50 batches out of the wider stock file.
- Recovery rate R across that sample: 55.09 percent.
- At the base case acting rate of 60 percent, R x E is 33.05 percent, and the yearly
  saving is about $61,150. That clears the break-even bar for a $50,000-a-year cost
  (27.03 percent) but not for a $100,000-a-year cost (54.05 percent).
- One wrong action on a high-value batch (the $12,000 batch, LF-70001) would wipe out
  about 2.35 months of savings at the base case rate.

## Known limits

- The ROI number rests on a 50-batch sample, not the full stock file. It is more
  reliable than the recommended 20-batch sample, but it is still a sample.
- The acting rate E is an assumption (60 percent, the recommended base case), not a
  measured number. If it is much lower in practice, the savings shrink a lot, since
  the saving is R times E times the baseline.
- Recovery rates and the $185,000 baseline come from the finance documents in docs/,
  which are made up for this training project, not measured figures from a real
  distributor.
- One process gap was found and fixed during testing: the safety check hook only
  triggers on the Bash tool. A send attempted through a different tool bypassed it
  once during testing, before being caught and redone correctly.

## What would come next

- Measure the acting rate E from real approval and action logs instead of assuming it.
- Run the ROI sample against the full stock file, not just a sample, once that is
  practical.
- Check whether the safety check can be made to catch a send regardless of which tool
  or shell issues the command.

## A note on privacy

All data and policy in this project are made up for training. No real company,
product or person is described here.
