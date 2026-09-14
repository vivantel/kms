---
id: fact-governance-fields
title: Facts must declare their kind and governing decision
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
---

## Guardrail

Any fact file the `bootstrap` or `steward` skill writes or updates MUST
carry `kind` (`environmental | decision | derived | mixed`) and
`governed-by` (a decision id, or `TBD` when no decision has been recorded
yet — itself debt, but declared debt).

## Derivation

- **Axiomatic basis**: `docs/decisions/0009-bootstrap-and-steward-skills.md`
  — the team committed to every fact being traceable to whether it's
  observed from the world or chosen by the team, and to the decision that
  governs it.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base `id/title/status/date/tags` frontmatter this
  guardrail extends.
- **Normative conclusion**: therefore any fact `bootstrap`/`steward`
  produces carries `kind` and `governed-by`.
