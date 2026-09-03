---
id: decision-track-field
title: Every decision must declare its track
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
governed-by: 0010-decision-track-field
grounded-in: TBD
derivation-note: >
  Given decision 0010 (decisions distinguish product from process),
  every decision must declare which, or the distinction has no teeth.
---

## Guardrail

Every decision file MUST carry a `track` field: `product` or `process`.
A decision missing this field is incomplete and MUST be flagged, the
same way a guardrail missing `governed-by`/`grounded-in`/`derivation-note`
is flagged as undeclared.

`track` MUST be exactly one of `product`/`process` — never a literal
`both` or `mixed`. A summary spanning several decisions' tracks (e.g.
describing a plan by the decisions it implements) is computed at read
time from those decisions' own values, never written into any file's
frontmatter as a stored third value.

## Derivation

- **Axiomatic basis**: `docs/decisions/0010-decision-track-field.md` —
  the team committed to distinguishing decisions about what kms is for
  from decisions about how it's built. `docs/decisions/0038-track-field-mutual-exclusivity.md`
  makes that distinction's mutual exclusivity explicit and enforced.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base `id/title/status/date/tags` frontmatter this
  guardrail extends.
- **Normative conclusion**: therefore any decision written or edited
  going forward carries exactly one `track` value, and a decision found
  without one, or with a stored `both`/`mixed`, is debt to resolve, not
  a silent gap.
