# Journal

## Decisions

- Lab 1, Decision 1.1 (approval gate): A, Balanced (healthcare, >$2,000, DISPOSE, or bad data check need a person).
- Lab 1, Decision 1.2 (request length): A, Short (3 to 4 lines: action, clause, who approves).
- Lab 1, Decision 1.3 (stopping rule): A, Full check (rows, clauses, counts, top five by score).
- Lab 2, Decision 2.1 (duplicates): A, keep most recent count (latest last_counted_date).
- Lab 2, Decision 2.2 (ambiguous dates): A, work it out via received date + shelf life if exactly one reading fits within 3 days, else flag DATE_AMBIGUOUS.
- Lab 2, Decision 2.3 (stale count threshold): A, 45 days.
- Lab 3, Decision 3.1 (shelflife skill format): A, Standard (seven steps, full result).
- Lab 5, Decision 5.1 (how the agent sends): B, Outbox folder (saves the brief as a text file, no account needed).
- Lab 5, Decision 5.2 (READY brief format): A, Plain list (one line per batch with action and clause ID).
- Lab 6, Decision 6.1 (sample size): started with A (20 batches), then the student asked for 50 batches instead (not one of options A/B/C; a custom choice, more reliable than C's 30 but using more of the plan allowance). Final sample size: 50.
- Lab 6, Decision 6.2 (base case acting rate E): A, 60% typical.
- Lab 6, Decision 6.3 (biggest breaking assumption): A, people do not act in time (E much lower than assumed).

## Surprises

- Lab 1, Step 5: on LF-70003, the rulebook-on and rulebook-off answers were nearly identical (both caught the FOOD/HEALTHCARE mismatch, cited REF-HC-04, escalated to QA Lead, no invented numbers). The rulebook's value looked like consistency across the whole dataset, not correctness on this one question.

## Questions
