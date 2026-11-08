# Fact `kind`: rater agreement before and after (2026-11-08)

14 facts (12 live, 2 archived), `kind` removed from the text, labelled from the definitions plus the fact text only. Two raters per condition, same two models in both: R1 = Sonnet-class subagent, R2 = Haiku-class subagent. No repository access. Raters are models, so this measures whether the definitions are unambiguous to a reader, not human agreement.

Before: `environmental | decision | derived | mixed`, with the definitions then in `artifact-model.md`. After: `environmental | decision`, defined by verification method (decision 0064).

| Condition | R1 vs R2 agreement | Cohen's kappa | Matches recorded label (R1, R2) |
|---|---|---|---|
| Before | 11 / 14 = 0.79 | 0.58 | 11/14, 14/14 |
| After | 14 / 14 = 1.00 | 1.00 | 14/14, 14/14 |

Before, R1 labelled facts 0002, 0013 and 0014 `derived` (an audit of repository state, a history count, a count of guardrails); R2 labelled them `environmental`. No fact used `derived` or `mixed`, so no file was relabelled. The recorded labels were not changed by the ratings.

Caveats: 14 facts from one project; kappa after is 1.00 on a skewed set (3 decision, 11 environmental); the two models are the same family, so errors can be correlated. The "after" definitions were written after seeing the "before" disagreement, so this is a fit to these facts, not a held-out result.
