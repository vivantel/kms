---
id: decision-expires-must-be-reevaluated
title: A decision past its expires date or condition must be re-evaluated
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
---

## Guardrail

Any decision carrying an `expires` field whose date has passed, or whose
condition has plausibly been met, MUST be re-evaluated — its `status`
updated (accepted, superseded, or re-affirmed with a new `expires`) —
not left standing as current.

## Derivation

- **Axiomatic basis**: `docs/decisions/0014-decision-scope-and-expires-fields.md`
  — the team committed to decisions that are explicitly time-boxed or
  conditional not being treated as permanent once their bound is reached.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base frontmatter this guardrail's field extends.
- **Normative conclusion**: therefore any decision past its `expires`
  bound is re-evaluated, regardless of whether `steward` or a human
  catches it.
