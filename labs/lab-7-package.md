# Lab 7: Wrap up

**15 minutes. No decisions.**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-7-package.md`

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

1. **One step at a time.** Plain English, short replies.
2. **Every claim in the README must come from a file in `notes/`.** If it does not, remove it or ask the
   student to support it.
3. **Do not use em dashes** in anything you write, including the README.
4. **Never claim the project uses or is built for any real company's product.** It is a training prototype
   on made-up data.
5. In Step 2, check the folder yourself for secrets and personal data. Report exactly what you find.
6. Close by checking DONE WHEN honestly.

**New sessions:** a new session has no memory of this one. If the student comes back saying "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and carry on from Step N.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Why this lab exists, and why these steps

**Why this lab exists:** to capture what you built and make sure nothing private leaks before you show it to anyone. It began as a longer packaging lab and was cut down when
you asked for the resume and interview material to be removed.

**Before this:** everything. **After this:** you are done.

**Why these steps:** the README may only say what your notes support, so it stays honest. The folder check searches for passwords, email addresses and answer files, because
those are the mistakes people make when they share a project.

## Step 1: A one-page README

The student types:

```
Write README.md for this project: the problem in three sentences; the loop (watch the stock, check the data, rank by value at risk, recommend an action); a simple text diagram of how the pieces fit; why each design choice was made (scripts do the maths, the helper agent sees only three inputs, the gate reads the master file and not the row, the safety check is separate from the rulebook, only READY items can be sent); the choices made in notes/journal.md; how to run it; the results in notes/lab6-failures.md and notes/roi.md, including the sample size; the known limits; and what would come next. Say clearly that all data and policy are made up. Do not use em dashes. Do not claim anything that is not in the notes.
```

The student reads it and deletes any sentence they could not explain to a friend.

## Step 2: Safety check of the folder

Together, check:

- No `.env` file and no password anywhere in this folder.
- No answer key, rescue kit or expected-results file inside this folder.
- No email address in any file. (If the student used the outbox route, the `outbox` folder contains their address by
  design: they should delete it, or keep it out of anything they share.)

You do this by searching the folder and reporting the results. The student also does one search themselves. In the side
window (PowerShell in the project folder), they replace `myname` with the part of their email address before the "@" and type:

```
Get-ChildItem -Recurse -File -Force | Select-String -Pattern "myname" -List | Select-Object Path
```

Only the `outbox` files (if any) should be listed. Then repeat with the part after the "@".

---

## If this does not work

Nothing here needs the rescue kit. If a search lists a file, open it, remove the item, and search again.

## DONE WHEN

- [ ] `README.md` exists and every claim in it traces to `notes/`
- [ ] The folder check found no password, no address (other than the outbox) and no answer key
- [ ] The student's own searches found nothing unexpected
