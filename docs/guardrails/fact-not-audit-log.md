---
id: fact-not-audit-log
title: A fact must not be an ungrounded audit-log record
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
governed-by: [0015-facts-must-not-be-audit-log-records]
derivation-note: >
  Given decision 0015 (kms stays a knowledge base, not a log), a fact that
  records an event rather than a lasting claim is noise, not knowledge.
pinned:
  0015-facts-must-not-be-audit-log-records: "64aa7cc47a97"
---

## Guardrail

A fact MUST state a lasting claim about the environment or process. A fact that only records a timestamped event is log noise and MUST be flagged for removal or rewrite — not left standing as knowledge. A fact is not noise merely for being unreferenced when it carries a `source`.

## Derivation

- **Axiomatic basis**: `docs/decisions/0015-facts-must-not-be-audit-log-records.md`
  — the team committed to kms staying a knowledge base, not a dashboard,
  log, or monitoring tool.
- **Amendment**: `docs/decisions/0071-facts-carry-no-outgoing-edges.md` bounds the orphan test to facts without a `source`.
- **Normative conclusion**: therefore any fact file found to be
  audit-log noise, regardless of who wrote it, is flagged rather than
  left standing.
