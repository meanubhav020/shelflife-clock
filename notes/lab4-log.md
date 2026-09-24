# Lab 4 Step 4 log: five batches

## LF-70002
- Data check flag: OK
- Class (master file): FOOD_AMBIENT
- Action: MARKDOWN (up to 30% off)
- Clause IDs: REF-ACT-03 (action), REF-APR-05 (no approval needed)
- Given to subagent: batch facts (id LF-70002, description "Instant oats sachet box", 100 units, 25 days to expiry, $400 value, score 150, band P3), product class FOOD_AMBIENT, clause text of REF-ACT-03
- Needs a person before anything happens: No
- Clause that says so: REF-APR-05 (none of REF-APR-01 to REF-APR-04 trigger: not HEALTHCARE, value under $2,000, not DISPOSE, trust flag OK)

## LF-70003
- Data check flag: OK
- Class (master file): HEALTHCARE
- Action: MONITOR (re-check in 7 days; no other action eligible)
- Clause IDs: REF-ACT-01
- Given to subagent: batch facts (id LF-70003, description "Vitamin D3 tablets 60 ct", 300 units, 12 days to expiry, $1500 value, score 1104, band P2), product class HEALTHCARE, clause text of REF-ACT-01 plus the reason MONITOR applies
- Needs a person before anything happens: No
- Clause that says so: THE GATE (CLAUDE.md rule 4) only triggers for actions other than MONITOR

## LF-70004
- Data check flag: MISSING_EXPIRY (not OK)
- Class (master file): FOOD_AMBIENT
- Action: MONITOR only (no other action allowed while data is untrustworthy)
- Clause IDs: REF-APR-04
- Given to subagent: batch facts (id LF-70004, description "Cooking sauce jar", 400 units, days to expiry not provided, $1200 value, score/band not provided), product class FOOD_AMBIENT, clause text of REF-APR-04
- Needs a person before anything happens: Yes
- Clause that says so: REF-APR-04 (trust flag not OK; batch goes to Inventory Control for correction)

## LF-70006
- Data check flag: OK
- Class (master file): FOOD_CHILLED
- Action: TRANSFER (to LOC-12, cold_chain=Y, higher sales)
- Clause IDs: REF-ACT-02, REF-CC-01
- Given to subagent: batch facts (id LF-70006, description "Long-life greek yoghurt 4 pack", 300 units, 24 days to expiry, $1800 value, score 828, band P3), product class FOOD_CHILLED, clause text of REF-ACT-02 and REF-CC-01, plus target location facts (LOC-12, cold_chain Y, units_sold_last_30d 150)
- Needs a person before anything happens: No
- Clause that says so: REF-APR-05 (not HEALTHCARE, value under $2,000, not DISPOSE, trust flag OK)

## LF-70009
- Data check flag: OK
- Class (master file): HEALTHCARE
- Action: DISPOSE (quarantine and destroy via licensed vendor; expired 3 days ago)
- Clause IDs: REF-ACT-05, REF-HC-03
- Given to subagent: batch facts (id LF-70009, description "Antacid syrup 200 ml", 200 units, days to expiry -3, $2400 value, score 2400, band P2), product class HEALTHCARE, clause text of REF-ACT-05, REF-HC-03, REF-APR-01, REF-APR-02, REF-APR-03
- Needs a person before anything happens: Yes
- Clause that says so: REF-APR-01 (HEALTHCARE, QA Lead), REF-APR-02 (value above $2,000, Regional Manager), REF-APR-03 (DISPOSE always needs Finance)
