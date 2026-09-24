# Lab 6: Test it, fix it, price it

**75 minutes. Three decisions (pick a letter each).**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-6-test-set-roi.md`

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

1. **Do not reveal expected answers.** Run the ten batches, say what you produced, and let the student
   mark it against their own answer key. The key lives outside this folder. Never ask them to paste it
   here. If they do, tell them this conversation is contaminated: they should close it and continue in a
   new one, and results produced after the paste do not count.
2. **The fix loop has strict rules.** Change one thing at a time. Re-run only the failed batch. Then
   re-run two batches that passed before, to make sure nothing else broke. Log one line per fix. Do not
   combine fixes, even if asked.
3. **Decisions come as options.** If the student says "you pick" or is unsure, choose A and say so. Record
   each choice under Decisions in `notes/journal.md`. Do not argue with a choice, but do say plainly when
   one is weaker.
4. **Be honest about small samples.** Wherever a result is quoted, say how many batches are behind it.
5. Short replies. Never show code unless a step contains it. Explain any new word once.
6. **Do not use em dashes** in anything you write.
7. If a step fails twice, stop retrying and point to the rescue kit (below).
8. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** a complete agent. **After this:** Lab 7 wraps up.

**Why this is its own lab:** in the Fernway labs testing and ROI were the tail end of a 90-minute lab. Here they are separate because testing, fixing and pricing is a
different skill from building, and the ROI needs a random sample rather than the tricky designed batches.

**Why these steps:** the ten batches each trap one mistake, so failures point at a cause. The fix loop changes one thing at a time and re-checks earlier passes, so a fix
cannot silently break something else. The random sample gives a fairer ROI. The ROI itself is kept simple, with its assumptions named, because the honest question is which
assumption would break it.

## Why this lab exists

A demo that works once proves nothing. This lab checks the agent on cases built to break it, fixes what
breaks without breaking what worked, and puts an honest number on the value.

## Step 1: Run the ten (nothing sent yet)

Each of the ten batches tests one thing:

| # | Batch | What it tests |
|---|---|---|
| 1 | LF-70001 | The value approval level, when little can be done in the time left |
| 2 | LF-70002 | A clean case, and a tempting action the rules do not allow |
| 3 | LF-70003 | The row's label against the master file's class |
| 4 | LF-70004 | A missing date, and whether the agent guesses |
| 5 | LF-70005 | A row that was entered twice: is it handled once? |
| 6 | LF-70006 | A transfer where the best-looking location is the wrong one |
| 7 | LF-70007 | No action is allowed, and one is tempting |
| 8 | LF-70008 | High value but outside the time window: does it over-act? |
| 9 | LF-70009 | Expired stock, and a fee the documents do not state |
| 10 | LF-70010 | A valuable batch with an old count |

The student types:

```
Move the current action_queue.csv and hold_queue.md into notes/ with today's date added to their names, then start new empty copies. Then run /shelflife on each of these ten batches, one at a time, in this order: LF-70001, LF-70002, LF-70003, LF-70004, LF-70005, LF-70006, LF-70007, LF-70008, LF-70009, LF-70010. Write each result to action_queue.csv and hold_queue.md as your rules say. Do not send anything. At the end print one table: batch, class, data check flag, score, band, action, clause IDs, status, approvers.
```

## Step 2: Mark it

For each batch the student marks four things on paper, using their answer key:

- **Right action or route?**
- **Real clause?** They opened the document, and the clause really says what the agent claims.
- **Right status?** (READY, HOLD or MONITOR)
- **Right score?**

Write every failure in `notes/lab6-failures.md`.

> **An agent that holds all ten is not a good agent.** It has just handed the work back to a person. An
> agent that lets all ten through is worse.

## Step 3: Test the real send

Use the same route as Lab 5 (email, or the outbox script).

```
Send me one brief with the subject "ACTION READY: ten-batch test" listing every batch from this run that is READY, with actions and clause IDs. Send it only to my own address.
```

Check it arrives (or the file appears) and lists only what the student believes is READY. Then:

```
Now send me a brief with the subject "ACTION READY: everything" that lists all ten batches.
```

The safety check must block it and name the first batch that breaks the rules.

## Step 4: Fix what failed

For each failure, work out which part was wrong:

| What went wrong | What to fix |
|---|---|
| A rule was vague | `CLAUDE.md` |
| A document was silent or unclear | `docs/` |
| A number was wrong | `tools/score.py` |
| The safety check let something through | `hooks/pre_send_check.py` |
| The helper wandered or was starved | `.claude/agents/action-drafter.md` |

The loop:

1. Change **one** thing.
2. Re-run only the batch that failed.
3. Re-run two batches that passed before.
4. Write one line in `notes/lab6-failures.md`: what failed, what you changed, what the re-run showed.

Stop when every batch matches your key, or when you can honestly say a remaining failure is a limit of the
design and not a bug. If a fix fails twice, use the rescue kit (below).

## Step 5: Run a random sample

The ten batches are built to be tricky, so they say nothing about a normal stock file. Use a random sample
for the ROI.

### DECISION 6.1: How big should the sample be?

| | Option | What it means |
|---|---|---|
| **A** | **20 batches (recommended)** | A good balance of effort and usefulness. |
| B | 12 batches | Use this if your usage allowance is running low. Noisier. |
| C | 30 batches | More reliable, uses more of your allowance. |

The student types (replace 20 with their choice):

```
Using scored.csv, pick 20 batches at random (seed 7) that are in scope and are not LF-70001 to LF-70010. Write their IDs to notes/sample.txt. Then run /shelflife on each one, one at a time, adding rows to action_queue.csv. Send nothing. At the end print how many are READY, HOLD and MONITOR, and for each action how many batches and their total batch value.
```

## Step 6: Work out the ROI

*ROI* means: is what the agent saves worth what it costs? Four numbers:

- **Value at risk** of a batch = batch value x unsold share (stock expected to go unsold).
- **R, the recovery rate** = total value recovered by the recommended actions divided by total value at
  risk, over the sample. Each action recovers a share (REF-FIN-02). A batch with a data problem counts as
  recovering nothing.
- **E, the acting rate** = the share of recommendations people actually carry out before the stock expires.
- **Baseline** = $185,000 a year written off (from Case 06).

The student types:

```
Write tools/roi.py that reads action_queue.csv, scored.csv and the recovery rates in docs/06-finance.md, and works out R for the batches in notes/sample.txt: R = total value recovered by the recommended actions divided by total value at risk, where value at risk = batch value x unsold share and a batch with a data problem recovers nothing. Print R, the number of batches, and the inputs for each batch so I can check two by hand.
```

The student checks two batches by hand before trusting it.

### DECISION 6.2: What is your "base case" acting rate E?

*In plain English:* An agent can recommend a markdown, but somebody still has to do it in time. E is the
share of recommendations that actually happen.

| | Option | What it means |
|---|---|---|
| **A** | **60%, typical (recommended)** | Busy people, but a decent process. |
| B | 40%, cautious | Slow approvals, competing priorities. |
| C | 80%, optimistic | Strong follow-up from management. |

Whatever they pick, show all three in a small table.

Then, on paper:

- **Yearly saving** = $185,000 x R x E
- **Break-even:** R x E must be above 27% if running the agent costs $50,000 a year (50,000 / 185,000), and
  above 54% if it costs $100,000.
- **Build cost:** the difference between the plan usage now and the plan usage you wrote down in Lab 0. Just record
  it.

### DECISION 6.3: Which one assumption, if wrong, would break your number the most?

| | Option | What it means |
|---|---|---|
| **A** | **People do not act in time (recommended)** | If E is much lower than assumed, the recommendations recover almost nothing. |
| B | Not all of the $185,000 is preventable | Some expiry losses could never have been avoided. |
| C | Real stock data is messier than this practice data | More batches would be flagged and held. |
| D | The recovery rates are too optimistic | The finance document's rates (transfer 90%, markdown 60%, and so on) might not hold. |

Then the student finishes one sentence in `notes/roi.md`: "I picked this because ...". Also work out
together: **what does one wrong action cost?** Take the value of a wrong high-value batch and divide it by
the monthly saving. That is how many months of savings one mistake wipes out.

> The cost is not the risk. The error rate is the risk.

## Step 7: Read the meter

Click the usage ring next to the model picker and write down the plan usage and the time, next to the numbers from Lab 0.
(Context usage belongs to one session, so it is not comparable.) Set the **Transcript view** to **Verbose** during this lab so you can
see each batch being processed.

---

## If this does not work

- **Batches keep failing the same way after two fixes:** ask the coach to re-check the rulebook against
  the answer-key row, or restore `CLAUDE.lab5.md`, `SKILL.lab4.md`, `action-drafter.md`, `score.py` and
  `pre_send_check.py` from the rescue kit (exact commands in `RESCUE.md`) and re-run the failing batch.
- **The ROI script fails:** copy `tools/roi.py` from the rescue kit and run it with
  `python tools\roi.py`.

## DONE WHEN

- [ ] All ten batches were run and marked against your key, and failures written down
- [ ] Every failure has a fix line, and the re-run check was done
- [ ] The READY brief arrived, and the "everything" brief was blocked
- [ ] A random sample was run, and R was checked by hand on two batches
- [ ] `notes/roi.md` has your acting rate, the break-even comparison, your one breaking assumption and the
      cost of one wrong action
- [ ] The plan usage from Lab 0 and now are side by side
- [ ] Your three choices are under Decisions in `notes/journal.md`
