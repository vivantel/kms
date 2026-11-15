---
id: 0073-lifecycle-words-defined
title: Lifecycle words (immutability, deprecated, superseded, draft, expires) are defined once
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

Rules, as they will appear in the model:

1. **Immutability scope.** `## Decision`, `## Why` and `## Tradeoffs considered` are frozen once `status: active`. `status`, `superseded-by`, `accepted-by`, `tags`, `expires`, `expires-when`, `fitness-functions` and dated, additive `## Amendment <date>` sections stay editable.
2. **`date`** is the creation date and never moves.
3. **`deprecated`** means retired without replacement; the body's first line after the frontmatter states why (no new field). **`superseded`** means replaced by a named successor.
4. **`superseded-by`** is allowed on all four types and required when `status: superseded`.
5. **`draft`** means proposed, not binding (`conform` and `query` report it as "proposed").
6. **`expires: <date>`** (structural) and **`expires-when: <condition>`** (judgment), either or both. Files retired by 3 or 4 move to `docs/<type>/archive/`, with its own `INDEX.md`.

## Why

Eight `## Amendment` sections in four accepted decisions, `fitness-functions` rewritten after acceptance, and `capture` check 1 itself editing an accepted decision's `status`, yet the model says "immutable once accepted" and `CONTRIBUTING.md` says "never an edit to the original". `date`, `deprecated` and `draft` are undefined; 0066 used `deprecated` for facts still true. `superseded-by` is decision-only in 0039 while the checker demands it on all four types and a replaced fact has no pointer. `expires` is "a date or condition" in one field, which is why check 4 is judgment. `archive/` is described in an archived decision, not the model.

## Tradeoffs considered

- **Strict immutability**: contradicts practice and `capture` itself.
- **Chosen: freeze the reasoning sections, allow lifecycle edits and dated amendments.**

## Dispositions

0039 amended (rules 3, 4, 6). 0053 left active. Guardrails `lifecycle-status-values`, `superseded-decision-requires-pointer`, `decision-expires-must-be-reevaluated` re-derived in 2.10. `CONTRIBUTING.md` Governance paragraph rewritten in 5.3. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.3.
