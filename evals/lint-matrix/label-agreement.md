# Structural vs judgment labels: second-rater agreement (2026-11-08)

Rater 1 (author's labels, fixed before rater 2 answered): structural = 1, 2, 3, 7, 9, 12, 15, 19, 20, 21 (the checks `shared/lint_check.py` runs); judgment = the other 14.

Rater 2: a fresh subagent with no repository access, given only the 24 check texts (`## What to check`, no labels) and the two definitions in decision 0061. Structural = 1, 2, 3, 7, 12, 15, 19, 20, 21, 24.

| Measure | Value |
|---|---|
| Checks rated | 24 |
| Agreement | 22 / 24 = 0.917 |
| Cohen's kappa | 0.83 |

Disagreements:
- Check 9 (stale prose references): rater 1 structural, rater 2 judgment. The checker finds the missing paths by rule, but the check text exempts "conditionally-optional" files and "annotated as preserved history" references, which need reading. The skill tells the model to dismiss those cases by hand.
- Check 24 (completed plan not archived): rater 1 judgment, rater 2 structural. Detection reads a plan's self-reported legend, which a rule can do if the legend format is fixed; rater 1 kept it judgment because the text does not fix that format and the check has no checker.

Rater 2 flagged as borderline: 3, 6, 7, 9, 12, 20, 24.

The labels in the skill are rater 1's and were not changed after rater 2 answered. The label means "decided by a fixed rule as written", and 9 and 24 are the two places where the rule as written and the rule as implemented differ.
