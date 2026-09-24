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
