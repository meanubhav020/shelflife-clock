FICTIONAL POLICY, FOR TRAINING USE ONLY

# Expiry scoring

[REF-SCORE-01] Scope. As of the as-of date, a batch with 60 days or fewer to expiry (including already expired) is in scope. A batch with more than 60 days to expiry is outside scope and is monitor-only.

[REF-SCORE-02] Days weight. Expired, or 7 days or fewer to expiry: 1.0. 8 to 14 days: 0.8. 15 to 30 days: 0.5. 31 to 60 days: 0.2.

[REF-SCORE-03] Unsold share = max(0, 1 minus ((units_sold_last_30d divided by 30) times days to expiry, divided by units on hand)). If the batch is expired, unsold share is 1.

[REF-SCORE-04] Batch value = units on hand x unit cost. Score = batch value x days weight x unsold share. Priority band: P1 if score is 5,000 or more; P2 if score is 1,000 to 4,999.99; P3 if score is below 1,000.
