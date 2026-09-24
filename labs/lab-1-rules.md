# Lab 1: The rulebook

**30 minutes. Three decisions (pick a letter each).**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-1-rules.md`

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
2. **Decisions come as options.** Show each decision card as written. If the student
   says "you pick" or is unsure, choose A and say so. Never pressure them. Record each
   choice under Decisions in `notes/journal.md`.
3. **Write CLAUDE.md only from the wording in this file.** Do not improvise rules.
4. **Step 4 must really be run twice.** Do not describe what would happen with and
   without the rulebook. The student runs the second version in a fresh conversation
   and brings both answers back. Ask what changed before you say anything.
5. Short replies. Never show code unless a step contains it.
6. **Do not use em dashes** in anything you write, including CLAUDE.md.
7. If a step fails twice, stop retrying and point to the rescue kit (below).
8. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** Lab 0 gave you a workspace. **After this:** Lab 2 relies on rule 2 (the master file beats a label on a row) when it cleans the data, and every later
lab reads this rulebook.

**Why these steps:** you draft first so you can see what an auto-generated rulebook misses (it describes files, not what you want). Three rules are given because
they make answers trustworthy (cite a document, use the master file, never invent a number). Three are yours because they are policy choices. You then break rule 3
on purpose to see where rules fail, and run the on/off test to prove the rulebook really changes behaviour.

## Why this lab exists

An agent with no rules is a slot machine: a good answer, then a different good answer,
then a confident wrong one, and you cannot tell which is which.

`CLAUDE.md` is a text file the agent reads at the start of every session. It is the
rulebook: what the project is, what must always happen, what must never happen. Every
other lab sits on it.

## Step 1: Get a first draft

If this session already has a CLAUDE.md loaded, start a new session. The student types:

```
Create a CLAUDE.md with instructions for this codebase
```

The agent writes a draft by looking at the files. Have the student skim it. It describes
the **files**. It says nothing about what the student **wants**. The next steps fix that.

## Step 2: Three decisions

Show these one at a time.

### DECISION 1.1: Which batches must a person approve before anything happens to them?

*In plain English:* Some actions are risky: they involve money, safety rules, or cannot
be undone. The rulebook must say when the agent stops and asks a person.

| | Option | What it means |
|---|---|---|
| **A** | **Balanced (recommended)** | A person approves: healthcare products, batches worth more than $2,000, any disposal (throwing away or destroying stock), and any batch whose data looks wrong. |
| B | Stricter | Everything in A, plus any batch worth more than $500. Safer, but more work for the people who approve. |
| C | Looser | Only healthcare products and disposals. Faster, but a big or badly recorded batch could be acted on without a person looking. |

*If you are unsure, choose A.* (Lab 5 locks this rule to version A whatever you pick. Choosing
B or C here lets you see the difference for now.)

### DECISION 1.2: How long should the agent's written request be for each action?

*In plain English:* For each action, the agent writes a note for the person who will carry
it out.

| | Option | What it means |
|---|---|---|
| **A** | **Short (recommended)** | 3 to 4 lines: what to do, which clause allows it, who must approve. |
| B | Medium | A short paragraph that also explains why this action was chosen over the others. |
| C | One line | Just the action and the clause. |

*If you are unsure, choose A.*

### DECISION 1.3: When does the agent count as finished?

*In plain English:* An agent that stops too early gives you half a job, and one that
never knows when it is done keeps going.

| | Option | What it means |
|---|---|---|
| **A** | **Full check (recommended)** | Every batch has a row and a cited clause, the counts add up, and the agent lists the top five batches by score. |
| B | Simple | Every batch has a row and a cited clause, and the counts add up. |
| C | Full check plus holds | As A, plus a list of every held batch and why it was held. |

*If you are unsure, choose A.*

## Step 3: Write the rulebook

Tell the agent to write `CLAUDE.md` so it holds exactly the text below, using the
student's choices for rules 4, 5 and 6. Read the whole file back to the student
afterwards.

**Project statement (given)**

> Shelf-Life Clock is a training prototype for a fictional food and healthcare
> distributor, Larkfield Distribution: 38 locations, 1,100 SKUs, about 78,800 units,
> about $185,000 a year written off to expiry. The agent watches inventory for expiry
> risk, checks the data can be trusted, ranks batches by value at risk, recommends one
> of five actions, and holds risky actions for a human.

**Standing facts (given)**

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

**Rules 1 to 3 (given)**

1. Cite the document ID for every claim about Larkfield policy, for example
   `[REF-ACT-03]`. No ID, no claim.
2. Look up product class, shelf life, unit cost and supplier terms in `sku_master.csv`,
   and cold-chain and licence status in `locations.csv`. Never trust the
   `category_label` or any other label on an inventory row.
3. If `docs/` does not answer the question, say so. Never estimate, and never invent a
   threshold, discount, fee or recovery rate. If asked for a number that is not in
   `docs/`, reply "Not in docs/" and stop.

**Rule 4, the gate (from Decision 1.1)**

- A: THE GATE. A human must approve before any action other than MONITOR is carried out
  when the product is HEALTHCARE according to sku_master.csv, the batch value is above
  $2,000, the action is DISPOSE, or the batch's data check flag (trust_flag) is not OK.
  Never use the label on the row.
- B: as A, but with "above $500" instead of "above $2,000".
- C: THE GATE. A human must approve before any action other than MONITOR is carried out
  when the product is HEALTHCARE according to sku_master.csv or the action is DISPOSE.
  Never use the label on the row.

**Rule 5, the output (from Decision 1.2)**

THE OUTPUT. For every batch in scope, write one row to action_queue.csv with batch_id,
action, clause_ids, status (READY, HOLD or MONITOR), the reason for any hold, and who
must approve. Draft a request for each action: (A) 3 to 4 lines / (B) a short paragraph
that includes why this action was chosen over the others / (C) one line. HOLD items are
written to hold_queue.md and are never emailed. READY items go into one brief to my own
inbox.

**Rule 6, stopping (from Decision 1.3)**

- A: STOPPING. Finished only when every batch in scope has a row with a status and a
  cited clause, the counts add up (in scope = READY + HOLD + MONITOR), and a summary
  shows the counts and the top five batches by score. A batch that cannot be processed
  still gets a row with status HOLD and the reason. Never stop silently.
- B: as A, without the top-five summary.
- C: as A, and the summary also lists every HOLD batch with its reason.

## Step 4: Make rule 3 fail (on purpose)

Rule 3 is the one that breaks first. The student types:

```
What does our destruction vendor charge per pallet, and what discount should we run on frozen desserts?
```

The documents answer neither. If the agent gives a plausible number, the rule is not strong
enough. Say so, add the sentence "If asked for a number that is not in docs/, reply 'Not in
docs/' and stop" to rule 3 if it is not already there, and test again.

## Step 5: Prove the rulebook changes the answers

1. In this conversation the student types:

   ```
   Triage batch LF-70003: what should we do with it, and does a human need to see it before anything happens?
   ```

   Save the answer (paper, or a file outside the project).
2. Turn the rulebook off. In the **side window** (PowerShell in the project folder) type:

   ```
   Rename-Item CLAUDE.md CLAUDE.md.off
   ```
3. In the app, click **+ New session** in the sidebar, choose **Local**, click **Select folder** and pick `shelflife-clock`
   (this is the test session). Ask it the same question. Save the answer. Then click back to the coach session in the
   sidebar.
4. Put the rulebook back (side window):

   ```
   Rename-Item CLAUDE.md.off CLAUDE.md
   ```
5. Look at the folder and confirm `CLAUDE.md` is back and `CLAUDE.md.off` is gone.

Put the two answers side by side. Ask (as a pick-one, not a blank question) what differed most:
A. it cited documents, B. it took the product class from the master file, C. it asked for a
person, D. it invented a discount, E. other. More than one can apply.

---

## If this does not work

If `CLAUDE.md` is wrong or the agent cannot write it, use the rescue kit: copy
`CLAUDE.lab1.md` from the rescue folder into the project as `CLAUDE.md` (exact command in
`RESCUE.md`). It has all choices set to A. Then tell the coach "I restored CLAUDE.md from the
rescue kit".

## DONE WHEN

- [ ] `CLAUDE.md` holds the project statement, the standing facts and six rules
- [ ] Rule 3 refused both questions about the destruction fee and the frozen desserts
- [ ] You ran LF-70003 with the rulebook on and off, and can say how the answers differ
- [ ] `CLAUDE.md` is back in place, not `CLAUDE.md.off`
- [ ] Your three choices are written under Decisions in `notes/journal.md`
