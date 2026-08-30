---
id: token-economy
title: Every fact, guardrail, and skill prescription must be maximally economical
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
governed-by: 0026-token-economy-guardrail
grounded-in: TBD
kms-seeded: true
kms-template-version: 1
derivation-note: >
  Given decision 0026 (token economy is a real, checked guardrail, not
  unenforced prose), any fact, guardrail, or skill prescription more
  verbose than needed is incomplete, the same way one missing a required
  field is incomplete.
---

## Guardrail

Every fact, guardrail, and skill prescription (`docs/facts/`,
`docs/guardrails/`, `docs/skills/`) in a project using this knowledge
system MUST use the shortest phrasing that preserves meaning and avoids
ambiguity — these get read into an agent's context, so unnecessary
length is a real, recurring cost. Decisions and plans are exempt —
their job is to carry rationale a cold reader needs in full.

`kms`'s own Claude Code packaging layer
(`plugins/<plugin-name>/skills/*/SKILL.md`) is out of scope here — that's
governed by `AGENTS.md`/`CONTRIBUTING.md` for `kms` contributors instead,
the same scope boundary `docs/guardrails/every-skill-ships-examples.md`
already draws.

## Derivation

- **Axiomatic basis**: `docs/decisions/0026-token-economy-guardrail.md`
  — the team committed to enforcing this as a real, checked guardrail
  rather than leaving it as unenforced aspiration.
- **Descriptive basis**: TBD — no existing fact documents why this
  matters specifically; a future fact could ground this more precisely.
- **Normative conclusion**: therefore any fact, guardrail, or skill
  prescription in a project's own `docs/{facts,guardrails,skills}/` found
  more verbose than needed is flagged by `lint`'s full-repo sweep, which
  restates this rule inline (a shipped check can't safely reference this
  file, which only exists in the `kms` marketplace repo itself, not in
  an adopting project).

## Note

This file was seeded from a `kms` template and is kept in sync
(updated or removed) as that template changes. To adopt it permanently
in its current form and stop future sync from touching it, delete its
`kms-seeded` and `kms-template-version` frontmatter fields.
