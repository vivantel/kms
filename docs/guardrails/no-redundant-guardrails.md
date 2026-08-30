---
id: no-redundant-guardrails
title: A guardrail true only "whenever skill X does Y" belongs in skill X's own body
status: active
date: 2026-08-30
tags: [knowledge-management, guardrail]
governed-by: 0027-baseline-guardrail-seeding
grounded-in: TBD
kms-seeded: true
kms-template-version: 1
derivation-note: >
  Seeded from kms's shipped guardrail templates, per
  docs/decisions/0027-baseline-guardrail-seeding.md.
---

## Guardrail

A guardrail only ever true "whenever skill/prescription X does Y," with
no claim broader than X's own procedure, belongs in X's own body, not a
separate guardrail file — unless the underlying policy was never meant
to be specific to X, in which case reword it as a system-wide invariant.

## Derivation

- **Axiomatic basis**: `docs/decisions/0027-baseline-guardrail-seeding.md`
  — kms's own copy of a guardrail it also ships as a template to every
  adopting project. Originally established for this repo by
  `docs/decisions/0012-no-redundant-guardrails.md`.
- **Descriptive basis**: TBD.
- **Normative conclusion**: therefore any guardrail found only true
  "whenever skill X does Y" is flagged, matching `lint` check 5.

## Note

This file was seeded from a `kms` template and is kept in sync
(updated or removed) as that template changes. To adopt it permanently
in its current form and stop future sync from touching it, delete its
`kms-seeded` and `kms-template-version` frontmatter fields.
