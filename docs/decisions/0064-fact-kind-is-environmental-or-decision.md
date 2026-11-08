---
id: 0064-fact-kind-is-environmental-or-decision
title: Fact kind is environmental or decision, chosen by how the fact is verified
status: active
date: 2026-11-08
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

`kind` on a fact takes two values, defined by the verification method: `environmental` (checked by observing the world, including a figure recomputed from observations) and `decision` (checked by confirming the governing decision still says so). `derived` and `mixed` are removed. A claim that needs both is written as two facts. `shared/lint_check.py` rejects any other value (check 2).

## Why

`derived` had no definition in the artifact model and overlapped `environmental` (a recomputed count is an observation) and `decision`. `mixed` named the overlap itself. Two raters given the old definitions agreed on 11 of 14 facts (kappa 0.58); they split on 0002, 0013 and 0014, where one chose `derived`. With the new definitions the same two models agreed on all 14 (kappa 1.00), and both matched the recorded labels (`evals/lint-matrix/kind-agreement.md`). No existing fact used `derived` or `mixed`, so nothing is relabelled.

## Tradeoffs considered

- **Keep four values and define them**: `derived` stays ambiguous against `environmental` for any fact that counts or audits repository state, which is what drew the disagreement.
- **Split into two orthogonal fields** (subject and verification): more expressive, but one more field for 14 facts, none of which needs it.
- **Chosen: two values, by verification method.** Sample is 14 facts from one project, rated by models; the result shows the definitions are unambiguous on these facts, not on others.
