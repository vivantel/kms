---
id: 0018-per-skill-examples-convention
title: Every skill ships a colocated examples.md with 2-3 worked usage examples
status: accepted
date: 2026-08-30
tags: [kms, packaging, documentation]
track: process
---

## Decision

Every skill in `plugins/kms/skills/` ships a colocated
`plugins/kms/skills/<skill>/examples.md`: 2-3 worked usage examples,
each a realistic trigger prompt plus a sketch of the resulting
interaction or output. The README's skill table links to each skill's
`examples.md` from a dedicated "Examples" column.

This applies retroactively to all 8 skills that predate this decision
(`clarify`, `roadmap`, `bootstrap`, `steward`, `lint`, `query`,
`attribute`, `changelog`), not just the 3 skills
(`docs/decisions/0019-brainstorm-skill.md`,
`docs/decisions/0020-onboard-skill.md`,
`docs/decisions/0021-refactor-plan-skill.md`) whose addition prompted
this decision, so the plugin doesn't ship in a state where some skills
have worked examples and others don't.
`docs/guardrails/every-skill-ships-examples.md` enforces it going
forward.

## Why

A skill's `description` frontmatter states *when* to use it in one
line; nothing in this plugin previously showed *what actually happens*
when it runs — a concrete before/after a new user or contributor could
skim instead of inferring behavior from the skill body's prose alone.
This became visible while adding `brainstorm`/`onboard`/`refactor-plan`:
each needed worked examples to be usable at a glance, and shipping that
only for the newest three would leave the other 8 looking unfinished by
comparison the moment a reader compared them side by side.

Colocating `examples.md` with `SKILL.md` (rather than a central
`examples/` directory keyed by skill name) matches this repo's existing
one-skill-one-directory layout, and keeps a skill's whole definition —
behavior plus what using it looks like — in one place.

## Tradeoffs considered

- **Scope to the 3 new skills only, retrofit the other 8 later**:
  smaller immediate diff, but leaves the plugin inconsistent in the
  meantime with no forcing function to close the gap. Rejected — chosen
  explicitly over this option when the decision was interviewed.
- **Inline `## Examples` section inside each SKILL.md** instead of a
  separate file: fewer files, but SKILL.md is what's loaded into every
  invocation's context; examples add length to that hot path for
  content only needed when a user is deciding *whether* to invoke the
  skill, not while running it. A separate file keeps SKILL.md as lean
  as `docs/decisions/0009-bootstrap-and-steward-skills.md` already
  argued ongoing-load skills should be.
- **Central `docs/examples/` or `plugins/kms/examples/` directory**,
  one file per skill: breaks the existing one-skill-one-directory
  layout for no benefit at this plugin's size.
- **Chosen: colocated `examples.md` per skill, applied to all 11 skills
  now, enforced by a new guardrail.**
