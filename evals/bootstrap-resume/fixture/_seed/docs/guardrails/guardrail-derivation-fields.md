---
id: guardrail-derivation-fields
title: Guardrails must declare their derivation
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
---

## Guardrail

Any guardrail file the `bootstrap` or `steward` skill writes or updates
MUST carry `governed-by`, `grounded-in`, and `derivation-note`
frontmatter. Missing any of the three makes the guardrail undeclared — a
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
- **Normative conclusion**: therefore any guardrail `bootstrap`/`steward`
  produces carries these three fields.
