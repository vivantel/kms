---
id: no-unenforced-guardrail
title: A guardrail describing shipped behavior is incomplete until that behavior's own body says so too
status: active
date: 2026-08-30
tags: [knowledge-management, guardrail]
governed-by: [0027-baseline-guardrail-seeding]
grounded-in: [0008-kilo-code-skills-spec]
kms-seeded: true
kms-template-version: 1
derivation-note: >
  Given decision 0027 (baseline guardrails) and fact 0008-kilo-code-skills-spec (skills are the unit an agent loads), a guardrail on shipped behaviour is incomplete until the skill's body says so.
pinned:
  0027-baseline-guardrail-seeding: "6145614bf934"
  0008-kilo-code-skills-spec: "b3a953909e58"
---

## Guardrail

A guardrail describing behavior a shipped skill or prescription should
perform is incomplete until that skill/prescription's own body actually
says so too — a guardrail alone in `docs/guardrails/` never reaches
whoever only reads or runs the skill itself.

## Derivation

- **Axiomatic basis**: `docs/decisions/0027-baseline-guardrail-seeding.md`
  — kms's own copy of a guardrail it also ships as a template to every
  adopting project. This principle first appeared in `steward` without
  a dedicated decision of its own; this is its first governing record.
- **Descriptive basis**: `docs/facts/0008-kilo-code-skills-spec.md` —
  agents load a skill from its own `SKILL.md`; nothing loads
  `docs/guardrails/` for someone who only runs the skill.
- **Normative conclusion**: therefore any guardrail found describing
  shipped behavior a skill's own body doesn't state is flagged, matching
  `lint` check 8.

## Note

This file was seeded from a `kms` template and is kept in sync
(updated or removed) as that template changes. To adopt it permanently
in its current form and stop future sync from touching it, delete its
`kms-seeded` and `kms-template-version` frontmatter fields.
