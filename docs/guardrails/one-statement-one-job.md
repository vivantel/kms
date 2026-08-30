---
id: one-statement-one-job
title: A fact, guardrail, or derivation-note doing two things must be split
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

A fact, guardrail, or derivation-note that does two distinct things
gets split into two files — one statement, one job, so each can be
governed, verified, or superseded independently.

## Derivation

- **Axiomatic basis**: `docs/decisions/0027-baseline-guardrail-seeding.md`
  — kms's own copy of a guardrail it also ships as a template to every
  adopting project.
- **Descriptive basis**: TBD.
- **Normative conclusion**: therefore any fact/guardrail/derivation-note
  found doing two jobs in this repo is split, matching `lint` check 11.

## Note

This file was seeded from a `kms` template and is kept in sync
(updated or removed) as that template changes. To adopt it permanently
in its current form and stop future sync from touching it, delete its
`kms-seeded` and `kms-template-version` frontmatter fields.
