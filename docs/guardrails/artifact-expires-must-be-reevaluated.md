---
id: artifact-expires-must-be-reevaluated
title: An artifact past its expires date or condition must be re-evaluated
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: [0039-unify-lifecycle-and-drop-scope, 0073-lifecycle-words-defined]
derivation-note: >
  Given decisions 0039 (expires applies to all four types) and 0073
  (`expires` is a date, `expires-when` a condition), any artifact past its
  bound must be re-evaluated, not left standing as current.
pinned:
  0039-unify-lifecycle-and-drop-scope: "47bb511d9633"
  0073-lifecycle-words-defined: "f0001b479b5e"
---

## Guardrail

Any fact, decision, guardrail, or procedure carrying `expires` (a date) that has passed, or `expires-when` (a condition) that has plausibly been met, MUST
be re-evaluated — its `status` updated (`active`, `superseded`,
`deprecated`, or re-affirmed with a new `expires`) — not left standing
as `active`. Plans are exempt — they don't carry `expires`
(`docs/decisions/0037-plans-not-a-governed-artifact-type.md`).

## Derivation

- **Axiomatic basis**: originally `docs/decisions/0014-decision-scope-and-expires-fields.md`
  — the team committed to decisions that are explicitly time-boxed or
  conditional not being treated as permanent once their bound is
  reached. `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`
  extends that commitment to facts/guardrails/procedures too.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base frontmatter this guardrail's field extends.
- **Normative conclusion**: therefore any of the four governed types
  past its `expires` bound is re-evaluated, regardless of whether `lint`
  or a human catches it.
