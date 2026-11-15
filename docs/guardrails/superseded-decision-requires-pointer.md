---
id: superseded-decision-requires-pointer
title: An artifact marked superseded must name what superseded it
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: [0039-unify-lifecycle-and-drop-scope, 0073-lifecycle-words-defined]
derivation-note: >
  Given decisions 0039 (supersession is a dedicated field) and 0073 (the
  field applies to all four types), any artifact with status: superseded
  must carry superseded-by pointing at its successor.
pinned:
  0039-unify-lifecycle-and-drop-scope: "47bb511d9633"
  0073-lifecycle-words-defined: "f0001b479b5e"
---

## Guardrail

Any artifact with `status: superseded` MUST also carry
`superseded-by: <id>`, naming what replaced it. An artifact found `superseded` with no `superseded-by`, or a
`superseded-by` value pointing at an id that doesn't exist,
MUST be flagged — matching `lint` check 1's existing dangling-reference
test, extended to this field.

## Derivation

- **Axiomatic basis**: `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`
  — the team committed to a structured supersession pointer instead of
  prose glued onto `status`.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base frontmatter this guardrail's field extends; `docs/decisions/0073-lifecycle-words-defined.md` extends the field to all four types.
- **Normative conclusion**: therefore any artifact found `superseded`
  without a valid `superseded-by` pointer is debt to resolve, not a
  silent gap.
