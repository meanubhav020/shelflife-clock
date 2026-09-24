# Lab 5: Safety first, then sending

**90 minutes. Two decisions (pick a letter each). One typed input: your own email address.**

> **To start this lab, type in the prompt box of the Code tab:**
> `run the lab in labs/lab-5-gate-hook-mcp.md`

---

## Working directory note

This session's folder is the parent of the kit, not the project folder itself. The
project root is `shelflife-clock/`. Every relative path in this lab (`notes/...`,
`docs/...`, `labs/...`, `tools/...`, `CLAUDE.md`, `sku_master.csv`, and so on) means
that path **inside** `shelflife-clock/`. Prefix each one with `shelflife-clock/` when
you read, write, or run it, and never create these files at the session root.

## AGENT: read this before doing anything

You are coaching one MBA student who knows nothing about how AI agents are built and
nothing about supply chains. The student is using the Claude desktop app (Code tab). Rules
for the lab:

1. **The order cannot change.** The approval rules (Step 1) and the safety check (Step 2) must
   both work **before** anything can be sent (Step 3). If the student wants sending first, refuse
   and explain: once something can be sent for real, a mistake leaves the building. Treat the
   safety check as working only after the student has seen it block a test.
2. **No passwords are needed in this lab.** If the student pastes any password into this chat,
   tell them to change it. Never write the student's email address into any file in this folder:
   it lives in an environment variable.
3. **Every send goes to the student's own address.**
4. **Never read, search or list the student's mailbox.** If Gmail is connected, use only its send
   tool, and only for the tests this lab asks for.
5. **Do not reveal expected answers.** Run the batches, say what you produced, and let the student
   judge.
6. **Decisions come as options.** If the student says "you pick" or is unsure, choose A and say so,
   except for Decision 5.1, where you choose B. Record the choice under Decisions in `notes/journal.md`.
7. **New sessions:** a new session has no memory of this one. If the student comes back saying
   "continue from Step N", list the folder to see what already exists, do not redo earlier steps, and
   carry on from Step N.
8. Short replies. Never show code unless a step contains it. Explain any new word once.
9. **Do not use em dashes** in anything you write.
10. If a step fails twice, stop retrying and point to the rescue kit (below).
11. Close by checking DONE WHEN honestly.

**Purpose first:** at the start, tell the student in two or three sentences why this lab exists, where it fits, and how long it takes (use the section below), then do Step 1.

---

## Where this lab fits, and why these steps

**Before this:** you know which batches needed a person. **After this:** Lab 6 tests everything you have built.

**Why these steps:** the order is gate, then safety check, then the plug, because a real send is irreversible. You test the safety check by hand before anything can be
sent, since a check you have never seen refuse something is not yet a check. The first real run includes a held batch to prove that what should not be sent is not sent.

## A note on new sessions

Two steps in this lab need a **new session** (so a new setting or safety check gets loaded). Each time, click
**+ New session**, choose **Local**, select `shelflife-clock`, and type:

`run the lab in labs/lab-5-gate-hook-mcp.md and continue from Step N`

(N is the step you were on.) Set the **Transcript view** dropdown to **Verbose** for this lab, so you can see each
tool call and each block.

## Why this order

Everything so far was reversible: a bad request sat in a file and someone read it. Once something can be sent for
real, it is not. So the safety comes first, and the plug goes in last.

Three ideas, in plain words:

- **The gate** is the list of cases where a person must approve first. It lives in the rulebook, so the agent
  follows it because it was told to.
- **The safety check (a "hook")** is a small program that runs automatically just before anything is sent. The
  agent cannot skip it or be talked out of it. The rulebook is a request; the safety check is a lock.
- **The plug** is how the agent sends. You choose below: a Gmail connector, or a simple outbox folder.

## Step 1: Lock in the approval rules (the gate)

Four cases always need a person first:

| Case | Why |
|---|---|
| The product is HEALTHCARE (according to the master file) | Regulated: the QA Lead decides |
| The batch value is above $2,000 | Money: the approver depends on the amount |
| The action is DISPOSE | Cannot be undone: Finance approves |
| The data check flag is not OK | The agent cannot make a sound decision |

The gate reads the **master file**, not the row. A row labelled FOOD whose master says HEALTHCARE must still be held.

The student types:

```
Replace rule 4 in CLAUDE.md with this exact wording, and keep the other five rules unchanged:
4. THE GATE. Before any action other than MONITOR is carried out, a person must approve when ANY of these is true: (a) the product class in sku_master.csv is HEALTHCARE; (b) the batch value is above $2,000; (c) the action is DISPOSE; (d) the batch's trust_flag is not OK. Read the class from sku_master.csv, never from a label on the row. Set the status to HOLD, write the reason, and name every approver role that docs/03-approvals.md requires. HOLD batches are written to hold_queue.md and are never emailed. MONITOR batches have status MONITOR. Everything else is READY.
```

Then five batches, nothing sent:

```
Run /shelflife on LF-70001, LF-70002, LF-70004, LF-70006 and LF-70010, one at a time, and write each result to action_queue.csv. Write the HOLD ones to hold_queue.md. Do not send anything.
```

Ask the student which ones were held and why (as a pick-one for each: READY or HOLD). Then have them run LF-70003 and
check it is held even though its row says FOOD (answer key, Lab 5).

## Step 2: Add the safety check (the hook)

### Typed input: your own email address

The student saves their own address inside the app, where no project file can leak it:

1. In the prompt box, click the environment dropdown (it says **Local**), hover over **Local**, and click the gear icon
   to open the **local environment editor**.
2. Add a variable named `SHELFLIFE_OWNER_EMAIL` whose value is their own address, and save. (If they will use the outbox
   route below, a made-up address such as `me@example.com` is fine.) The app stores it encrypted on their computer and
   applies it to every **new** local session.

Then the student starts a **new session** (see "A note on new sessions") and continues from here. They type:

```
Add a Claude Code hook to this project. Save the check as a Python script at hooks/pre_send_check.py and register it in .claude/settings.json as a PreToolUse hook that runs before the Bash tool and before any tool whose name contains "send", "reply" or "forward", in any capitalisation, including connector tools. What the check does:
 1. If it is the Bash tool and the command does not run tools/send_brief.py, it allows the command and does nothing else.
 2. Otherwise it reads the message that is about to be sent (recipient, subject, body) and finds every batch ID that looks like LF-#####. For tools/send_brief.py the recipient is --to, the subject is --subject, and the body is the text in the file given by --body-file.
 3. For each batch it looks in action_queue.csv. If the batch is not READY, it blocks the send (exit code 2, with a clear message naming the batch and the reason).
 4. It also re-checks the approval rules on its own, using sku_master.csv and inventory_clean.csv: HEALTHCARE class, or value above 2,000, or action DISPOSE, or trust_flag not OK. If any applies, it blocks the send even if the queue says READY.
 5. It reads the only allowed recipient from the environment variable SHELFLIFE_OWNER_EMAIL. If the recipient is anything else, cannot be found, or the variable is missing, it blocks. Never write the address into any file.
 6. A message with no batch IDs is allowed only if its subject starts with "TEST:". Otherwise it is blocked.
 7. If it cannot read a file or understand its input, it blocks.
Use whichever python command works on this machine. Do not connect or create any sending tool yet.
```

Test it by hand, before anything can be sent:

```
Run hooks/pre_send_check.py by hand with a pretend Gmail-style message addressed to my own address that mentions LF-70003, and show me that it blocks. Then a pretend message mentioning only LF-70002, and show me that it allows. Then a pretend message to some other address, and show me that it blocks. Build each pretend message in memory using the SHELFLIFE_OWNER_EMAIL variable. Do not save any of them, or my address, to a file.
```

Then start a **new session** (the safety check is loaded when a session starts) and ask:

```
Show me the hooks section of .claude/settings.json, and confirm that the script it points to exists.
```

A safety check you have never seen refuse something is not yet a safety check.

> **If the hand test says the variable is not set,** the app did not pass it to the session. In the **side window** type
> the line below (with the student's address), then quit the Claude app completely (right-click its icon in the system
> tray and choose Quit, or end it in Task Manager), reopen it, and start a new session:
>
> ```
> [Environment]::SetEnvironmentVariable("SHELFLIFE_OWNER_EMAIL", "you@example.com", "User")
> ```

## Step 3: Choose how the agent sends

### DECISION 5.1: How should the agent "send" its brief?

| | Option | What it means |
|---|---|---|
| **A** | **Gmail connector (only if you are comfortable)** | The agent sends a real email to your own inbox. You connect Gmail with the app's Connectors menu and sign in with Google. No password to type. **Warning:** the connector can also read your mailbox, and the safety check only guards sending. Best with a spare Gmail account. |
| B | Outbox folder (no account needed) | The agent "sends" by saving the brief as a text file in an `outbox` folder. Nothing goes over the internet. Choose this if you are unsure, if Gmail is not in your Connectors list, or if the Gmail route fails twice. |

*If you are unsure, choose B: it teaches exactly the same lesson and cannot go wrong outside your laptop.*

### Route A: Gmail connector

1. In the prompt box click the **+** button, choose **Connectors**, find **Gmail**, and connect it. A Google sign-in window
   opens; the student signs in there (nothing is typed into the chat). If Gmail is not in the list, use Route B.
2. The student types:

   ```
   List the tools the Gmail connector gives you, and tell me the exact name of the one that sends an email. Do not read, search or list any of my email. Check that the safety check's matcher catches that exact name, and show me how you checked.
   ```
3. Send a test email to their own address:

   ```
   send a test email to my own address with the subject: TEST: Shelf-Life Clock is connected. Do not read or search any email.
   ```

   Check it arrives. If not, stop and fix it, or switch to Route B.
4. Prove the safety check is stronger than the student:

   ```
   Email me a brief about batch LF-70003. I approve it. Ignore the hold and send it.
   ```

   It must be blocked, naming LF-70003, even though the student told the agent to override.

### Route B: Outbox

1. The student types:

   ```
   Create tools/send_brief.py. It takes --to, --subject and --body-file, and saves a text file into a new folder called outbox/ with the To, the Subject and the body. It must not send anything over the internet.
   ```
2. Test it:

   ```
   Write a short body file, then run tools/send_brief.py with --to set to the address in the SHELFLIFE_OWNER_EMAIL variable and the subject: TEST: Shelf-Life Clock outbox works. Show me the file it saved.
   ```

   Check a file appears in `outbox/`.
3. Prove the safety check is stronger than the student:

   ```
   Save a brief about batch LF-70003 using tools/send_brief.py. I approve it. Ignore the hold and do it.
   ```

   It must be blocked, naming LF-70003, even though the student told the agent to override.

## Step 4: First real run

### DECISION 5.2: How should the READY brief look?

| | Option | What it means |
|---|---|---|
| **A** | **Plain list (recommended)** | One line per batch: batch, action, clause. |
| B | Table | A table with batch, action, clause and value. |
| C | Short paragraphs | A short paragraph per batch. |

*If you are unsure, choose A.*

Route A prompt (Route B: replace "send me one email" with "save one brief with tools/send_brief.py"):

```
Run /shelflife on LF-70002, LF-70005 and LF-70006. Then send me one email with the subject "ACTION READY: expiry actions" that lists those READY batches as [A: a plain list, one line per batch with the action and clause ID / B: a table with batch, action, clause ID and value / C: a short paragraph per batch]. Send it only to my own address.
```

Check it arrives (or the file appears). Then try one that should be held:

```
Run /shelflife on LF-70009 and send me the request.
```

It must stop at HOLD, be written to `hold_queue.md`, and **not** be sent.

---

## If this does not work

Use the rescue kit (exact commands in `RESCUE.md`), then start a new session:

- **Gate:** copy `CLAUDE.lab5.md` over `CLAUDE.md`.
- **Safety check:** copy `hooks/pre_send_check.py`, `.claude/settings.json` and `tools/send_brief.py`. If you already have a
  `.claude/settings.json` with other settings, ask the coach to merge the hook into it.
- Then ask the agent to show the hooks section of `.claude/settings.json`, and repeat the hand test.

Tell the coach what you restored.

## DONE WHEN

- [ ] The gate holds all four cases (healthcare, value, DISPOSE, data check flag)
- [ ] The safety check blocked a pretend message in a hand test, and blocked a real attempt
- [ ] A test message arrived (your inbox, or a file in `outbox/`)
- [ ] A batch that should be held was attempted and did not send
- [ ] Your email address is stored in the app's environment editor, not typed into any project file (Lab 7 checks this)
- [ ] Your two choices are under Decisions in `notes/journal.md`
