# Lab 3: Answer only from the documents, and save a shortcut

**60 minutes. One decision (pick a letter).**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-3-grounding-skills.md`

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
2. **Do not open the `docs/` folder before Step 2.** Step 1 must genuinely be run without the
   documents. You cannot run it for the student: they hide the files and run it in a separate
   new conversation. Do not skip or soften it.
3. **Before Step 2, look at the folder** and confirm `CLAUDE.md` and `docs/` are back (not
   `CLAUDE.md.off`, not `docs_hidden`). If not, stop and tell the student to put them back.
4. **Ask before you tell.** When the student checks an answer, ask what they see first. Check
   their reading against the clauses in `docs/` yourself and ask questions rather than giving
   verdicts.
5. **Step 3: the student checks the maths by hand** with a calculator. Show the inputs when they
   ask. Never give the answer and never say "it matches" for them.
6. **Decisions come as options.** If the student says "you pick" or is unsure, choose A and say
   so. Record the choice under Decisions in `notes/journal.md`.
7. Short replies. Never show code unless a step contains it.
8. **Do not use em dashes** in anything you write.
9. If a step fails twice, stop retrying and point to the rescue kit (below).
10. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** clean data and the rulebook. **After this:** Lab 4 hands writing to a helper, which needs the clause-finding and scoring done reliably first.

**Why these steps:** you ask without the documents first so you see fluent guessing with your own eyes. You then ask again with them, to see the same questions answered
with citations. The scoring lives in a script because an AI should not do arithmetic on about 2,000 rows, and you check one score by hand so you trust the script. Finally
you save your prompt as a shortcut so the agent behaves the same way every time.

## Why this lab exists

A **grounded** answer traces to a specific document. An **ungrounded** answer traces to nothing.
The agent knows a lot from training, but its training is the internet, not Larkfield's policy.
When it answers from memory instead of from `docs/`, it is guessing fluently.

## Step 1: Ask three questions without the documents

The student hides the rulebook and the documents so the test is real. In the **side window** they type:

```
Rename-Item CLAUDE.md CLAUDE.md.off
Rename-Item docs docs_hidden
```

Then, in the app, they click **+ New session** in the sidebar, choose **Local**, select the `shelflife-clock` folder (this is the
test session, not the coach session), and type:

```
For batches LF-70001, LF-70003 and LF-70009: look each one up in inventory_clean.csv and sku_master.csv, then tell me what should be done with it, what discount or disposal fee applies if any, and who has to approve it. You have no policy documents. Use your general knowledge.
```

The answers will sound confident and well organised. The student writes down every specific figure, time limit,
fee or approver the agent named. They are about to check whether Larkfield's policy agrees.

Then they put everything back in the side window (do not forget this) and click back to the coach session in the
sidebar:

```
Rename-Item CLAUDE.md.off CLAUDE.md
Rename-Item docs_hidden docs
```

## Step 2: Ask again, with the documents

Confirm the folder is back (Agent rule 3). The student types, in this conversation:

```
For batches LF-70001, LF-70003 and LF-70009: look each one up in inventory_clean.csv and sku_master.csv, then tell me what should be done with it and who has to approve it. docs/ is the only source of truth. Cite the [REF-xx] ID for every policy claim. If docs/ does not answer, say so.
```

For each batch the student checks:

- Does every claim carry a `[REF-xx]` ID that, when they open the document, really says that?
- Where did the product class come from: the master file, or the row?
- Did it refuse to state anything the documents are silent on?

Compare with what Step 1 invented. Any answer without an ID is a guess in a suit.

## Step 3: Build the scoring tool

The maths must come from a script, not from the agent reading rows. The student types:

```
Write tools/score.py. It reads inventory_clean.csv and sku_master.csv and writes scored.csv, following REF-SCORE-01 to REF-SCORE-04 exactly. Use the date 2026-09-21. Columns: batch_id, sku, location_id, product_class, trust_flag, units_on_hand, unit_cost_usd, days_to_expiry, in_scope, days_weight, unsold_share, batch_value, score, band. A row with a missing or unclear expiry date gets a blank score and band, never zero. A row outside the 60-day window gets in_scope = N and a blank score. Sort by score, highest first. Run it, and show me the first ten rows and how many batches are in scope.
```

**Check one by hand.** The student picks LF-70002. They ask the agent to show its inputs (units, unit
cost, days to expiry, units sold). Then, with a calculator and the four REF-SCORE clauses, they work
out the score themselves. Only then do they compare with `scored.csv`. Then repeat for one more batch.

## Step 4: Save your prompt as a shortcut

A **skill** is a saved prompt you can call by name. It makes the agent behave the same way every time.

### DECISION 3.1: How should the shortcut work?

| | Option | What it means |
|---|---|---|
| **A** | **Standard (recommended)** | Seven steps, shows the full result. |
| B | Short | Fewer steps, a compact result. |
| C | Detailed | As A, and also explains why each other action was ruled out. |

*If you are unsure, choose A.*

Create `.claude/skills/shelflife/SKILL.md`. It must start with exactly this front matter, then the
text for the chosen option underneath:

```
---
name: shelflife
description: Assess one at-risk batch against docs/ and the master files, with citations and a gate decision
---
```

**Text for A**

> For the batch ID I give you:
> 1. Look it up in inventory_clean.csv and read its trust_flag.
> 2. Look up the SKU in sku_master.csv and the location in locations.csv. Ignore any label on the row.
> 3. Get days to expiry, value, score and band from scored.csv. If scored.csv is missing or older than
>    inventory_clean.csv, run tools/score.py first. Never calculate these yourself.
> 4. Using only docs/, choose MONITOR, TRANSFER, RETURN TO SUPPLIER, MARKDOWN or DISPOSE using the order of
>    preference in REF-ACT-06, and name the clause that makes it allowed. If none is allowed, the action is
>    MONITOR and you say why.
> 5. Say who must approve and which clause says so. If the trust_flag is not OK, take no action, say so, and
>    cite REF-APR-04.
> 6. If docs/ does not answer something, write "Not in docs/". Never estimate.
> 7. Show: batch, class, trust flag, days to expiry, value, score, band, action, clause IDs, approvers.

**Text for B**

> For the batch ID I give you: look it up in inventory_clean.csv and sku_master.csv (ignore any label on the row).
> Get the score from scored.csv; never calculate it. Using only docs/, choose the action in the order in REF-ACT-06
> and cite the clause. Say who must approve and cite the clause. If the trust_flag is not OK, take no action and
> cite REF-APR-04. If docs/ is silent, write "Not in docs/". Show: batch, class, days to expiry, value, score,
> action, clauses, approvers.

**Text for C:** the text for A, plus:

> 8. For each action you did NOT choose, say in one line why it was not allowed, citing the clause.

> **It must be a folder called `shelflife` with a file called `SKILL.md` inside it.** A single file called
> `shelflife.md` will not work, and `/shelflife` will not appear.

## Step 5: Check the shortcut

The student starts a new session (**+ New session**, Local, `shelflife-clock`), types `/` in the prompt box (or clicks **+** and chooses
**Slash commands**) and confirms `/shelflife` appears, then types:

```
/shelflife LF-70002
```

The result should match what their manual prompt gives for the same batch. If not, the shortcut is
missing something. Find it.

---

## If this does not work

- **Scoring tool wrong or failing after two tries:** copy `tools/score.py` from the rescue folder into
  `tools` and run it (exact commands in `RESCUE.md`).
- **`/shelflife` does not appear:** copy `SKILL.lab3.md` from the rescue folder into
  `.claude/skills/shelflife/` and rename it `SKILL.md`, then start a new session.
Tell the coach what you restored.

## DONE WHEN

- [ ] You saw three ungrounded answers and wrote down the figures they invented
- [ ] `CLAUDE.md` and `docs/` are back in place
- [ ] The three grounded answers carry `[REF-xx]` IDs that you checked against the documents
- [ ] `tools/score.py` exists, and a score you worked out by hand agrees with it
- [ ] `/shelflife` appears when you type `/`, and `/shelflife LF-70002` works with citations
- [ ] Your choice is under Decisions in `notes/journal.md`
