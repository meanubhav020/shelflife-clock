# Lab 0: Setup and first question

**25 minutes. No decisions in this lab.**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-0-setup.md`

---

## Working directory note

This session's folder is the parent of the kit, not the project folder itself. The
project root is `shelflife-clock/`. Every relative path in this lab (`notes/...`,
`docs/...`, `labs/...`, `tools/...`, `CLAUDE.md`, `sku_master.csv`, and so on) means
that path **inside** `shelflife-clock/`. Prefix each one with `shelflife-clock/` when
you read, write, or run it, and never create these files at the session root.

## AGENT: read this before doing anything

You are coaching one MBA student who knows nothing about how AI agents are built and
nothing about supply chains. Your job is to hold their hand through building a
working agent. The student is using the Claude desktop app (Code tab, Local session).
Rules for the whole lab:

1. **One step at a time.** Present a step, wait for the student to do it, then move
   on. Never run ahead.
2. **Say what and why first.** Before each step, tell the student in one line what
   we are about to do and why. The first time you use a technical or supply-chain
   word, explain it in one plain sentence.
3. **Decisions come as options.** Show a decision card exactly as written, options
   in order. If the student says "you pick" or is unsure, choose A and say so.
   Never pressure them. Record each choice as one line under Decisions in
   `notes/journal.md` (for example "D1.1: A, balanced").
4. **Short replies.** A few lines. Never show code unless a step contains it.
5. **Do not use em dashes** in anything you write.
6. **If a step fails twice,** stop retrying. Tell the student to use the rescue kit
   (section "If this does not work" in the lab) and carry on.
7. Do not open any other lab file, and do not open anything in `docs/` during this
   lab. Do not say or hint that any data problems exist.
8. At the end, walk through DONE WHEN item by item and say plainly which are met.
   Do not congratulate them on unmet items.

**New sessions:** a new session has no memory of this one. If the student comes back
saying "continue from Step N", list the folder to see what already exists, do not redo
earlier steps, and carry on from Step N.

**Purpose first:** start with one friendly line, then tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Why this lab exists:** before building anything you need a safe place to work, a way to measure what building costs, and a first look at what makes
this an agent rather than a chatbot.

**Before this:** nothing except `PRIMER.md`. **After this:** Lab 1 writes the agent's rulebook.

**Why these steps:** the two places to type and the permission questions come first, so nothing surprises you later. The folder check keeps the answer key
out of the agent's reach. The usage numbers are written down now because the cost cannot be reconstructed afterwards. The first question lets you watch the
agent choose its own files. The notes file exists because the README in Lab 7 may only claim what is written down.

## Step 1: Have you read the primer?

The student's kit has a short file called `PRIMER.md` (10 minutes) that explains the
supply-chain words and the agent words used in these labs. Ask whether they have read
it. If not, ask them to do so now and come back. You cannot see the file, and you do
not need to.

## Step 2: Your two places to type

The student works in **two places** for the whole build. Explain this plainly:

- **The coach session** is this conversation in the Code tab of the Claude desktop app.
  Everything typed here is seen by the agent. Each conversation in the Code tab is called
  a **session**, and the sidebar lists them.
- **The side window** is an ordinary PowerShell window, opened in the project folder. It is
  for the few commands the labs give you (renaming a file, copying a rescue file). **The
  agent never sees what you type there.**

Ask the student to open the side window now:

1. Open the project folder (`shelflife-clock`) in File Explorer.
2. Click the address bar at the top, type `powershell` and press Enter. A PowerShell window
   opens in that folder. (On Windows 11 you can also right-click empty space in the folder and
   choose "Open in Terminal".)
3. In the side window type `dir`. They should see the same files you are about to list.
4. In the side window type `python --version`. It should say 3.10 or higher. If it says the
   command is not found, they type `py --version`; if that works, tell them to use `py` wherever
   a lab says `python`. (If neither works, they install Python from python.org and tick "Add
   python.exe to PATH".)

Also explain **how to start a new session:** in the sidebar click **+ New session** (or press
Ctrl+N), make sure **Local** is selected, click **Select folder** and choose `shelflife-clock`
again, then type what the lab tells them. Sessions are independent: a new session is a fresh
conversation, and the old one stays in the sidebar. Suggest they rename each session (click its
title) to "Lab 0", "Lab 1", and so on.

## Step 3: Permission mode, and what the questions mean

Point to the **permission mode** selector next to the send button. For these labs the student
should choose **Accept edits**. Explain the modes in one line each:

- **Manual:** asks before every edit or command. Safe but slow.
- **Accept edits (use this):** applies file edits itself and shows a summary like `+12 -1`, but
  still asks before running other commands (for example a Python script).
- **Plan:** explores and proposes, but does not change anything.
- **Auto / Bypass permissions:** do **not** use these in this build. They reduce the questions that
  keep you in control.

When a question appears, give the student this table:

| The question is about... | Answer |
|---|---|
| Changing a file **inside this project** (notes, tools, docs, CLAUDE.md) | Allow |
| Running a `python tools\...` script that a lab asked for | Allow |
| Anything **outside the project folder** | Deny |
| Deleting files they did not expect | Deny, and ask the coach why it wants to |
| Anything involving a password, or installing a program, that the lab did not ask for | Deny |

If they are unsure about a question, they can type what it says into the prompt box and ask. The
stop button (or the Esc key) stops the agent if it heads somewhere wrong.

## Step 4: Check the folder

You do this one. List the file names in this folder (top level, and inside `docs/` and `labs/`).
Do not open any of them.

You should see: `sku_master.csv`, `locations.csv`, `inventory_raw.csv`, a `docs/` folder with seven
files, and a `labs/` folder.

You should NOT see any file with "answer", "expected", "planted" or "rescue" in its name. If you do,
stop. Tell the student to move it out of this folder (into their `shelflife-build-tools` folder) and to
start a **new session**, because this one has seen it.

## Step 5: Write down two numbers

Next to the model picker at the bottom of the prompt box there is a small **usage ring**. The student
clicks it and writes down, with the current time:

- the **context usage** (how full this session's working memory is), and
- the **plan usage** for the period (how much of their usage allowance is used).

Explain: context usage belongs to one session, so it starts again in every lab. Plan usage is shared
across everything they do with Claude, so the difference in **plan usage** between now and the end of
Lab 6 is roughly what building this agent cost. (If they also chat on claude.ai in between, that counts
too; they should note it.)

## Step 6: Ask your first question

The student types:

```
look at the files in this folder and tell me what Larkfield is and what problem I am about to solve
```

Nobody pasted anything in: the agent chose which files to open. **That choosing is what "agentic"
means.**

## Step 7: Start a notes file

The student types:

```
create notes/journal.md with three headings: Decisions, Surprises, Questions
```

Tell them: the coach will write their choices under Decisions. They can add a line under Surprises
whenever something surprises them. Lab 7 builds the README from these notes.

If they hit the usage limit at any point: write down which step they were on, wait for the reset, and
continue in a new session.

---

## If this does not work

Nothing in this lab needs the rescue kit. If the app shows an error, or asks for Git, the student updates
the app (Help > Check for Updates) and tries again; if it still asks for Git, they install Git for Windows
from git-scm.com. If they cannot see a **Code** tab, they need a paid Claude plan; the Chat and Cowork tabs
will not work for these labs.

## DONE WHEN

- [ ] You have read `PRIMER.md`
- [ ] Your side window is open in the project folder, and `python --version` works
- [ ] The permission mode is **Accept edits**, and you know what the permission questions mean
- [ ] The folder has the three data files, a `docs/` folder with seven files, and a `labs/` folder, and
      no answer file
- [ ] Your context usage and plan usage are on paper, with a time
- [ ] The agent described the folder correctly: a fictional food and healthcare distributor, expiry risk,
      stock files, policy documents
- [ ] `notes/journal.md` exists
