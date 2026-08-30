---
id: guardrail-re-derivation-on-source-change
title: A guardrail must be re-derived when its governing decision or grounding fact changes
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
governed-by: 0009-bootstrap-and-steward-skills
grounded-in: TBD
derivation-note: >
  Given decision 0009 (norms must not outlive the decisions that
  justified them), a guardrail's source changing must trigger
  re-derivation, not silence.
---

## Guardrail

Whenever a guardrail's `governed-by` decision or `grounded-in` fact
changes, the guardrail's text MUST be re-derived and updated in the same
pass — never left standing unchanged against a moved source.

## Derivation

- **Axiomatic basis**: `docs/decisions/0009-bootstrap-and-steward-skills.md`
  — the team committed to a knowledge system where norms never outlive
  the decisions that justified them.
- **Descriptive basis**: `docs/guardrails/guardrail-derivation-fields.md`
  — every guardrail already declares which decision and facts it derives
  from, so a source change can be traced to the guardrails it invalidates.
- **Normative conclusion**: therefore a changed source triggers
  re-derivation of every guardrail grounded in it, in the same pass.
