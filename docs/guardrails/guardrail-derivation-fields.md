---
id: guardrail-derivation-fields
title: Guardrails must declare their derivation
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
governed-by: 0009-bootstrap-and-steward-skills
grounded-in: TBD
derivation-note: >
  Given decision 0009 (every normative artifact must trace to its
  sources), every guardrail must declare governed-by, grounded-in, and
  derivation-note.
---

## Guardrail

Any guardrail file MUST carry `governed-by`, `grounded-in`, and
`derivation-note` frontmatter — whether written by `bootstrap`/`steward`
or by hand. Missing any of the three makes the guardrail undeclared — a
norm with no stated basis — and it MUST be flagged as debt rather than
left silent.

## Derivation

- **Axiomatic basis**: `docs/decisions/0009-bootstrap-and-steward-skills.md`
  — the team committed to a knowledge system where every normative
  artifact traces to the axiomatic and descriptive artifacts that
  produced it.
- **Descriptive basis**: this repo's own guardrails (`docs/guardrails/*.md`)
  already carry `## Derivation` sections in prose — this makes that
  existing pattern a structured, machine-checkable frontmatter
  requirement rather than only a prose convention.
- **Normative conclusion**: therefore any guardrail file carries these
  three fields, regardless of how it was created.
