# Lab 4: Manager and writer

**75 minutes. No letter decisions; a simple scorecard instead.**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-4-subagents.md`

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

1. **One step at a time.** Say what and why first, in one line. Explain any new word once.
2. **Step 1 is a baseline and must be saved.** Before anything changes, run `/shelflife LF-70006`
   and save the output so it can be compared later.
3. **In Step 2 you must really delegate.** Start a real helper agent (a "subagent") for the writing
   job and give it only three things: the batch facts, the product class, and the exact clause text.
   Not the docs folder, not the CSV files, not this conversation. If you shortcut it and write the
   request yourself, say so out loud. Never pretend a helper ran.
4. **Step 3 is the student's judgement,** guided by the scorecard. Show both versions plainly and let
   the student score them before you give any view.
5. Do not tell the student the expected answer for any batch.
6. Short replies. Never show code unless a step contains it.
7. **Do not use em dashes** in anything you write.
8. If a step fails twice, stop retrying and point to the rescue kit (below).
9. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** the /shelflife shortcut works. **After this:** Lab 5 turns the pattern of "who needed a person" into the gate.

**Why these steps:** you save a baseline first so there is something to compare against. You add the helper, then score both versions with a simple scorecard, because the
helper does not always win. You run five batches chosen to cover different situations, and the pattern in who needed a person is what Lab 5 formalises.

## What you have built, and the problem with it

One agent that does everything in one conversation: reads the batch, checks the data, finds the
policy, picks an action, writes the request. Writing the request pulls every policy document into the
same working space. The space fills up, and the agent gets slower and starts losing the thread.

The fix is what a good manager does: hand the writing to a helper, and brief them with only what they
need.

- **The main agent is the manager.** It reads the batch, checks the data check flag, works out the
  product class, finds the action and the exact clause. It does not write the request.
- **The helper (subagent) is the writer.** It gets the batch facts, the product class and the clause
  text. Nothing else. It writes the request and hands it back.

The skill is in what you **leave out**.

## Step 1: Baseline on one batch

The student types:

```
/shelflife LF-70006
```

LF-70006 is chilled food (food that must be kept cold). The right answer depends on facts about other
locations in the master files, not only on the batch. Save it:

```
save your full answer to notes/baseline-LF-70006.md
```

## Step 2: Add the helper

First create the writer:

```
Create a subagent named action-drafter as .claude/agents/action-drafter.md. Its job: write a short action request for one batch from exactly three inputs: the batch facts, the product class, and the policy clause text I give it. It must not read files, run commands or send anything. Give it no tools if the setup allows it. It may only use the clause text it is given, must cite the clause ID, and must write "not provided" for anything it does not have instead of inventing it.
```

Then connect the manager to it:

```
Update the /shelflife skill so that, once you have chosen the action and found the clause, you hand the writing to the action-drafter subagent. Give it only: the batch facts (id, description, units, days to expiry, value, score, band), the product class, and the exact clause text (the action clause and, if approval is needed, the approval clause). Nothing else: not docs/, not the CSV files, not this conversation. Show me exactly what you gave it.
```

Then start a **new session** (so the updated shortcut loads) and set the **Transcript view** dropdown (next to the send button) to
**Verbose**, so every step is visible. In the new session type "run the lab in labs/lab-4-subagents.md and continue from Step 2" to
bring the coach back, and when it is ready for it, run:

```
/shelflife LF-70006
```

**Check the helper really ran.** In the Verbose transcript you should see a separate agent call naming
`action-drafter`, and you can open the **Views** menu and choose the **Tasks** pane to watch it. You should also be
shown what it was given. If the main agent wrote the request itself,
the student says: "You did not hand this over. Call the subagent and show me the call."

## Step 3: Score the two versions

Put `notes/baseline-LF-70006.md` next to the new output. For **each** version the student answers yes or
no to:

1. Does it name the right action and cite the clause for it?
2. Does it stay inside the policy it was given (nothing invented)?
3. Is the request clear enough for a person to act on?
4. Does it say who must approve, if anyone?
5. Does it say "not provided" or "Not in docs/" instead of filling a gap?

Then ask the student to pick: **A.** the helper's version is better, **B.** the baseline is better,
**C.** about the same. (The helper does not always win. Sometimes a starved helper writes something
thinner.) Ask which one thing the manager no longer had to carry: A. the policy documents, B. the
writing, C. both.

## Step 4: Run five batches

**LF-70002, LF-70003, LF-70004, LF-70006, LF-70009**

They are not random: between them there is a clean batch, a row whose label contradicts the master file,
a batch with no expiry date, a chilled batch, and one already past its date.

```
Run /shelflife on each of these five batches, one at a time: LF-70002, LF-70003, LF-70004, LF-70006, LF-70009. After each one add a row to notes/lab4-log.md with: batch id, data check flag, class from the master file, action, clause IDs, exactly what you gave the subagent, whether a person must see it before anything happens, and which clause says so.
```

The student counts how many needed a person, then picks the pattern that fits: A. all of them, B. the
regulated, doubtful-data and cannot-be-undone ones, C. none of them. (Check the answer key.) That pattern
is the gate you will lock in during Lab 5.

---

## If this does not work

- **The helper is not created, or `/shelflife` does not call it:** copy `action-drafter.md` into
  `.claude/agents/` and `SKILL.lab4.md` into `.claude/skills/shelflife/` (rename it `SKILL.md`) from the
  rescue folder (exact commands in `RESCUE.md`), then start a new session.
Tell the coach what you restored.

## DONE WHEN

- [ ] `.claude/agents/action-drafter.md` exists, and a real helper call appears in the transcript
- [ ] The LF-70006 output cites a clause and takes class and cold-chain facts from the master files
- [ ] You scored both versions and picked A, B or C
- [ ] `notes/lab4-log.md` has five rows
- [ ] You picked the right pattern for who needed a person (check the answer key)
