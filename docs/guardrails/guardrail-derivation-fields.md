---
id: guardrail-derivation-fields
title: Guardrails must declare their derivation
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
governed-by: [0009-bootstrap-and-steward-skills, 0072-guardrail-derivation-edges-are-honest]
derivation-note: >
  Given decisions 0009 (every normative artifact traces to its sources) and
  0072 (edges are decision lists plus optional fact grounding), every
  guardrail must declare governed-by and derivation-note, and grounded-in
  only when an independent fact exists.
pinned:
  0009-bootstrap-and-steward-skills: "2d4a963a7104"
  0072-guardrail-derivation-edges-are-honest: "e88736350c53"
---

## Guardrail

Any guardrail file MUST carry `governed-by` (a list of decision ids) and `derivation-note`, and `grounded-in` (fact ids) when an independent fact exists — whether written by `bootstrap`/`capture` or by hand. Missing either required field makes the guardrail undeclared — a norm with no stated basis — and it MUST be flagged as debt rather than left silent.

## Derivation

- **Axiomatic basis**: `docs/decisions/0009-bootstrap-and-steward-skills.md`
  — the team committed to a knowledge system where every normative
  artifact traces to the axiomatic and descriptive artifacts that
  produced it.
- **Axiomatic basis (edges)**: `docs/decisions/0072-guardrail-derivation-edges-are-honest.md` — `grounded-in` is optional and fact-only.
- **Normative conclusion**: therefore any guardrail file carries these fields, regardless of how it was created.
