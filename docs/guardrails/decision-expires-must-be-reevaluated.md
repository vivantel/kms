---
id: decision-expires-must-be-reevaluated
title: An artifact past its expires date or condition must be re-evaluated
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: 0039-unify-lifecycle-and-drop-scope
grounded-in: TBD
derivation-note: >
  Given decision 0039 (expires extends from decision-only to all four
  artifact types), any fact/decision/guardrail/procedure past its bound
  must be re-evaluated, not left standing as current.
---

## Guardrail

Any fact, decision, guardrail, or procedure carrying an `expires` field
whose date has passed, or whose condition has plausibly been met, MUST
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
