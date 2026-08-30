---
id: fact-not-audit-log
title: A fact must not be an ungrounded audit-log record
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
---

## Guardrail

Any fact file MUST describe something that grounds, or could plausibly
ground, a decision or guardrail. A fact that only records a timestamped
event with no forward-looking derivational purpose, and that nothing
references, is log noise and MUST be flagged for removal or rewrite —
not left standing as knowledge.

## Derivation

- **Axiomatic basis**: `docs/decisions/0015-facts-must-not-be-audit-log-records.md`
  — the team committed to kms staying a knowledge base, not a dashboard,
  log, or monitoring tool.
- **Descriptive basis**: `docs/guardrails/fact-governance-fields.md`
  already requires every fact to declare `governed-by`; an ungrounded,
  unreferenced event record fails this test in spirit even when the
  field is technically present.
- **Normative conclusion**: therefore any fact file found to be
  audit-log noise, regardless of who wrote it, is flagged rather than
  left standing.
