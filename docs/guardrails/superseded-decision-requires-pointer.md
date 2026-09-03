---
id: superseded-decision-requires-pointer
title: A decision marked superseded must name what superseded it
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: 0039-unify-lifecycle-and-drop-scope
grounded-in: TBD
derivation-note: >
  Given decision 0039 (supersession moves from free text in status to a
  dedicated field), a decision with status: superseded must carry
  superseded-by pointing at the decision that replaced it.
---

## Guardrail

Any decision file with `status: superseded` MUST also carry
`superseded-by: <decision-id>`, naming the decision that replaced it. A
decision found `superseded` with no `superseded-by`, or a
`superseded-by` value pointing at a decision id that doesn't exist,
MUST be flagged — matching `lint` check 1's existing dangling-reference
test, extended to this field.

## Derivation

- **Axiomatic basis**: `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`
  — the team committed to a structured supersession pointer instead of
  prose glued onto `status`.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base frontmatter this guardrail's field extends;
  `plugins/kms/shared/artifact-model.md`'s table establishes decisions as
  the only type immutable once accepted, which is why only decisions
  carry this field.
- **Normative conclusion**: therefore any decision found `superseded`
  without a valid `superseded-by` pointer is debt to resolve, not a
  silent gap.
