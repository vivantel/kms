---
id: 0061-label-lint-checks-structural-or-judgment
title: Each lint check carries a structural or judgment label, checked by a second rater
status: active
date: 2026-11-08
tags: [kms, eval-harness, knowledge-management]
track: process
---

## Decision

Every check in the lint skill's `## What to check` list is tagged `[structural]` or `[judgment]` right after its name.

- **structural**: a violation is decided by a fixed rule over file contents or existence (frontmatter, id or path existence, string or date comparison, set comparison). Two programs implementing the text would agree on every input.
- **judgment**: deciding needs reading meaning, weighing intent, or a threshold the text leaves relative. A judgment clause that can change the verdict makes the whole check judgment.

Ten checks are structural (1, 2, 3, 7, 9, 12, 15, 19, 20, 21), the ones `shared/lint_check.py` runs; fourteen are judgment.

## Why

The paper's claim that checks are mechanical applies only to the structural set, and the lint matrix (0059) reports the two sets apart. A label set by the person who wrote the checker could just mirror the checker, so a second rater classified the 24 check texts alone. Agreement was 22 of 24 (kappa 0.83); details in `evals/lint-matrix/label-agreement.md`.

## Tradeoffs considered

- **Label by "has a checker"**: simple, but circular. Check 9 shows the gap: the checker covers it, yet its exemptions are judged by the model.
- **Relabel after the second rater**: would raise agreement artificially. The labels stay as fixed beforehand; the two disagreements (9, 24) are recorded.
- **Chosen**: pre-fixed labels, one independent model rater, disagreements published. One rater is a model, so this shows the text is classifiable, not that people would agree.
