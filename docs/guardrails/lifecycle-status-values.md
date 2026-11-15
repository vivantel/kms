---
id: lifecycle-status-values
title: status must be draft, active, superseded, or deprecated — for any of the four artifact types
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: [0039-unify-lifecycle-and-drop-scope, 0073-lifecycle-words-defined]
derivation-note: >
  Given decisions 0039 (one status enum across all four artifact types) and
  0073 (what each word means), any artifact's `status` must be one of the
  four defined values.
pinned:
  0039-unify-lifecycle-and-drop-scope: "47bb511d9633"
  0073-lifecycle-words-defined: "f0001b479b5e"
---

## Guardrail

Any fact, decision, guardrail, or procedure file's `status` field MUST
be exactly one of `draft`, `active`, `superseded`, or `deprecated`. A
file with `status: accepted`, `status: current`, or free text of any
other kind is out of sync with the unified vocabulary and MUST be
flagged. Plans are exempt —
`docs/decisions/0037-plans-not-a-governed-artifact-type.md` excludes
them from this lifecycle model; their own per-step legend is unaffected.

## Derivation

- **Axiomatic basis**: `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`
  — the team committed to one shared lifecycle vocabulary across the
  four governed types.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base frontmatter (including `status`) this guardrail's
  enum constrains.
- **Normative conclusion**: therefore any of the four governed types'
  `status` value is checked against the 4-value enum, matching `lint`
  check 2.
