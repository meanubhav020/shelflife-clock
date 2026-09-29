# ROI (Lab 6)

## Inputs
- R (recovery rate, 50-batch random sample, seed 7): 0.5509 (55.09%)
- Baseline: $185,000/year written off (Case 06)
- Acting rate E (base case, Decision 6.2): 60%

## Yearly saving = $185,000 x R x E

| E | R x E | Yearly saving |
|---|---|---|
| B, 40% cautious | 22.04% | $40,766.60 |
| A, 60% typical (base case) | 33.05% | $61,149.90 |
| C, 80% optimistic | 44.07% | $81,533.20 |

## Break-even
- Cost $50,000/year: R x E must exceed 27.03%. Base case (33.05%) clears it.
- Cost $100,000/year: R x E must exceed 54.05%. Base case does not clear it; even the optimistic case (44.07%) falls short.

## Build cost
Plan usage at Lab 0: 4%. Plan usage now (end of Lab 6): 55%. Difference: 51 percentage points of the plan used to build and test this agent through Lab 6.

## Biggest breaking assumption (Decision 6.3)
A, people do not act in time (E much lower than assumed).

I picked this because if E is much lower than assumed, recommendations recover almost nothing.

## Cost of one wrong action
Wrong high-value batch: LF-70001, $12,000.
Monthly saving (base case): $5,095.82.
Months of savings wiped out by one wrong action: 2.35.

The cost is not the risk. The error rate is the risk.

## Update: full in-scope population (2026-09-29)

The numbers above were a 50-batch random sample, chosen because that was what Lab 6 asked
for. The agent has since been run over the full in-scope inventory instead of a sample: 370
batches (every in-scope batch except the ten designed test batches, excluded the same way
the original sample excluded them, since they are built to be tricky and would bias the
estimate). This replaces the sample estimate with the full population, computed by
tools/roi.py (via tools/build_dashboard.py, which calls the same function) and shown live on
the dashboard.

### Inputs
- R (recovery rate, full 370-batch in-scope population): 0.4678 (46.78%), down from the
  55.09% sample estimate.
- Total value at risk: $88,741.19. Total value recovered: $41,514.17.
- Baseline: $185,000/year written off (Case 06). Acting rate E: same three cases as before.

### Yearly saving = $185,000 x R x E

| E | R x E | Yearly saving |
|---|---|---|
| B, 40% cautious | 18.71% | $34,618.06 |
| A, 60% typical (base case) | 28.07% | $51,927.10 |
| C, 80% optimistic | 37.42% | $69,236.13 |

### Break-even
- Cost $50,000/year: R x E must exceed 27.03%. Base case (28.07%) clears it, but only by
  about one point, not the six-point margin the sample suggested.
- Cost $100,000/year: R x E must exceed 54.05%. No case clears it, including optimistic
  (37.42%).

### Cost of one wrong action, recalculated
LF-70001 ($12,000) is still the highest-value batch in the full run. Monthly saving at the
base case is now $4,327.26 (185,000 x 0.4678 x 0.6 / 12), so one wrong action on that batch
wipes out about 2.77 months of savings, not 2.35.

The direction of the finding does not change: the cost of a mistake is not the risk, the
error rate is. But the fuller number is more fragile than the sample made it look, and that
is itself the finding worth leading with.
