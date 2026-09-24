# Lab 2: Data problems

**45 minutes. Three decisions (pick a letter each).**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-2-data.md`

---

## Working directory note

This session's folder is the parent of the kit, not the project folder itself. The
project root is `shelflife-clock/`. Every relative path in this lab (`notes/...`,
`docs/...`, `labs/...`, `tools/...`, `CLAUDE.md`, `sku_master.csv`, and so on) means
that path **inside** `shelflife-clock/`. Prefix each one with `shelflife-clock/` when
you read, write, or run it, and never create these files at the session root.

## AGENT: read this before doing anything

You are coaching one MBA student who knows nothing about how AI agents are built and
nothing about supply chains. Rules for the lab:

1. **One step at a time.** Say what and why first, in one line. Explain any new word
   once, in plain English.
2. **Step 1 is a hunt, not a handout.** When asked to look for problems, write and run a
   small script and report what you actually find. Do not read rows by eye. Do **not** say
   how many problems exist and do not group them as "the five". Let the student count.
3. **Do not clean anything in Step 1.**
4. **Decisions come as options.** Show each decision card as written. If the student says
   "you pick" or is unsure, choose A and say so. Record each choice under Decisions in
   `notes/journal.md`.
5. **In Step 3 build the cleaning prompt only from the student's choices** and the fixed
   rules in this file. If anything is unclear, stop and ask.
6. **Log every change. Never fix anything silently.** Prove results with a script and show
   its output.
7. Short replies. Never show code unless a step contains it.
8. **Do not use em dashes** in anything you write.
9. If a step fails twice, stop retrying and point to the rescue kit (below).
10. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** the rulebook. **After this:** Lab 3 scores the clean data, so wrong data here would mean wrong scores there.

**Why these steps:** you look for problems without fixing them so you see the mess first. Then you decide what "clean" means, clean with a log (the log is your audit
trail), check the result with a script rather than trusting "done", list every guess the agent made, and turn your cleaning rules into a policy document so the agent
can cite them later. The five kinds of problem are the five that real stock files commonly carry.

## Why this lab exists

Real stock files are messy. You do not clean the data yourself: you decide what "clean" means
and the agent does it. The **change log** is the real product. The clean file is just what you
use. The log is what you show someone who asks why a batch got the answer it got.

## Step 1: Look for problems (do not fix)

The student types:

```
look through inventory_raw.csv and list every data problem you find. Do not fix anything yet. Write and run a small script for this; do not read the rows by eye.
```

Then:

```
for each problem, how many rows are affected, and which batch IDs?
```

> **Five kinds of problem are planted in this file on purpose.** They are the same five that
> real stock files carry. If you have found three, look harder, particularly at the columns
> you would normally skim past, and at whether every row is really a different batch.

## Step 2: Three decisions

### DECISION 2.1: If the same batch appears twice, which copy do we keep?

*In plain English:* Sometimes a system exports the same row twice. (In this file the copies are
identical, so this choice does not change any numbers. It is here so you see how a rule is
decided.)

| | Option | What it means |
|---|---|---|
| **A** | **Most recent count (recommended)** | Keep the copy with the latest count date. |
| B | First one | Keep whichever appears first in the file. |
| C | Bigger quantity | Keep the copy with more units. |

### DECISION 2.2: Some dates are written like 03/04/2027. Is that 3 April or 4 March?

*In plain English:* If the day is 13 or more (like 27/04/2027) there is only one way to read it.
If the day is 12 or less, it is genuinely unclear. Guessing puts made-up dates into your data, so
guessing is not an option.

| | Option | What it means |
|---|---|---|
| **A** | **Work it out, else flag (recommended)** | Every product has a shelf life (how long it lasts). If exactly one reading matches "received date plus shelf life" (within 3 days), use it. Otherwise flag the row for a person. |
| B | Flag every unclear date | Never work anything out; a person fixes all unclear dates. Safer, more work (more flagged rows). |

### DECISION 2.3: How old can a stock count be before we stop trusting it?

*In plain English:* A count made two months ago may not match what is on the shelf today.

| | Option | What it means |
|---|---|---|
| **A** | **45 days (recommended)** | Older than 45 days is flagged. |
| B | 30 days | Stricter. In this file it flags exactly the same rows as A. |
| C | 60 days | Looser. Fewer rows flagged; an old count could slip through. |

### Not choices (explain these to the student in two lines)

- **Product class:** the master file always wins over the label typed on a row.
- **Blank expiry date:** flag it; never make one up from the shelf life.
- **Negative units:** flag it; never change the number.

The file names and flag names below are fixed because later labs use them.

## Step 3: Clean it

Build the prompt below from the student's choices and give it to the student to paste (or
paste it for them if they say so). Replace the bracketed parts.

```
Create inventory_clean.csv from inventory_raw.csv using a script saved as tools/clean.py, following exactly these rules. Change nothing else. If any instruction is unclear, stop and ask me first.
1. Duplicates: if a batch_id appears more than once, keep [A: the copy with the latest last_counted_date / B: the first copy in the file / C: the copy with more units_on_hand] and remove the others.
2. Product class: add a column product_class taken from sku_master.csv and drop category_label. Log every row where the label disagreed with the master file.
3. Dates: convert DD/MM/YYYY to YYYY-MM-DD. If the day is 13 or more, convert it. If the day is 12 or less, [A: convert it only if exactly one reading falls within 3 days of received_date plus the SKU's shelf_life_days from sku_master.csv, otherwise leave the original text and flag DATE_AMBIGUOUS / B: leave the original text and flag DATE_AMBIGUOUS].
4. Blank expiry_date: leave it blank and flag MISSING_EXPIRY. Never work an expiry out from shelf life.
5. Quantities: flag negative units_on_hand as QTY_SUSPECT and a last_counted_date more than [45 / 30 / 60] days before 2026-09-21 as STALE_COUNT. Do not change the numbers.
6. Add a column trust_flag: OK for clean rows, otherwise the flag name (joined with a plus sign if there is more than one).
```

Then:

```
write a change log to changes.md: every row you removed, changed or flagged, with the batch_id, the field, what it was, what it is now, and why
```

## Step 4: Check the result (do not trust "done")

```
compare inventory_raw.csv and inventory_clean.csv with a script. How many rows were removed, how many changed, how many are unchanged, and how many have a trust_flag other than OK? Show the script and its output.
```

The student compares the numbers with their answer key (`expected-results.md`, Lab 2, which has
a column for each option). If they differ, find out whether the agent or the data is wrong
before going on.

Then:

```
list every assumption you made where information was missing, and what I would need to tell you for you to stop guessing
```

Ask the student, as a pick-one: what would have gone wrong if a blank expiry date were treated as
"no risk"? A. Those batches would score zero and quietly disappear from the ranking. B. The agent
would email the wrong person. C. Nothing, blank dates are harmless. (The answer is A.)

## Step 5: Turn the rules into policy

What the student just decided is now policy, so make it something the agent can cite. Write the
five clauses to match the choices, then have the student paste:

```
Create docs/08-data-trust.md, starting with the line "FICTIONAL POLICY, FOR TRAINING USE ONLY", with one clause per cleaning rule, stating exactly the rules used in tools/clean.py and nothing more. Use these IDs in this order: [REF-DATA-01] duplicates, [REF-DATA-02] where product class comes from, [REF-DATA-03] date formats and dates that could be read two ways, [REF-DATA-04] blank expiry dates, [REF-DATA-05] negative quantities and old counts.
```

Have them read it and confirm nothing new was added.

---

## If this does not work

If the agent's cleaning script fails or gives numbers you cannot explain after two tries, use the
rescue kit: copy `tools/clean.py` from the rescue folder into the project's `tools` folder and run it
with the options that match your choices (exact commands in `RESCUE.md`). Then copy
`docs/08-data-trust.md` only if you chose A for every decision. Tell the coach "I restored clean.py
from the rescue kit".

## DONE WHEN

- [ ] `inventory_clean.csv` exists with `product_class` and `trust_flag` columns
- [ ] `changes.md` lists every removed, changed and flagged row with a reason
- [ ] The Step 4 numbers match the answer key column for your choices, or you know why not
- [ ] The agent's guesses are written out, not hidden
- [ ] `docs/08-data-trust.md` exists and matches what the script does
- [ ] You can name all five kinds of problem out loud
- [ ] Your three choices are under Decisions in `notes/journal.md`
