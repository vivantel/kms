---
id: every-skill-ships-examples
title: Every skill must ship a colocated examples.md
status: active
date: 2026-08-30
tags: [kms, packaging, documentation, guardrail]
governed-by: 0018-per-skill-examples-convention
grounded-in: TBD
derivation-note: >
  Given decision 0018 (every skill ships worked usage examples,
  applied to all skills, not just new ones), a skill added without a
  colocated examples.md is incomplete, the same way a guardrail
  missing its derivation fields is incomplete.
---

## Guardrail

Every skill directory `plugins/kms/skills/<skill>/` MUST contain an
`examples.md` with 2-3 worked usage examples (a realistic trigger
prompt plus a sketch of the resulting interaction or output). A new
skill added without one is incomplete at the same review gate as a
missing `SKILL.md` frontmatter field. The README's skill table MUST
link each skill's `examples.md` from its "Examples" column; a skill row
without that link is stale the same way a manifest with a stale version
is stale.

## Derivation

- **Axiomatic basis**: `docs/decisions/0018-per-skill-examples-convention.md`
  — the team committed to every skill shipping worked examples,
  applied retroactively to the whole set, not just new additions.
- **Descriptive basis**: TBD — no existing fact currently documents the
  full skill roster; `bootstrap`/`capture` would generate one
  (`docs/facts/0001-kms-skill-names.md`-style) as the natural grounding
  fact for this guardrail once the roster changes again.
- **Normative conclusion**: therefore any skill added to this plugin
  going forward ships `examples.md` in the same change that adds
  `SKILL.md`. This is `kms`'s own packaging-layer convention
  (`plugins/kms/skills/*/`), out of `lint`/`capture`'s scope
  (`docs/{facts,guardrails,skills}/`, not `plugins/kms/skills/`) per
  `docs/skills/scoping-shipped-vs-repo-rules.md` — checked by review via
  `AGENTS.md`/`CONTRIBUTING.md`'s "Adding a new skill" instructions, not
  by an automated `lint` check.
