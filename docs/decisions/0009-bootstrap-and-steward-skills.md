---
id: 0009-bootstrap-and-steward-skills
title: Add bootstrap and steward as two skills, not one combined skill
status: accepted
date: 2026-08-29
tags: [kms, knowledge-management]
track: process
---

## Decision

Establishing and maintaining a project's fact/decision/guardrail/skill
knowledge system is added to `kms` as two skills, split by *when* each
runs — the same axis `docs/decisions/0002-commit-pr-attribution-skill-design.md`
already used to split `attribute` from `changelog`:

- **`bootstrap`** — one-time (or occasional gap-fill) setup: detect or
  create the `docs/{facts,decisions,guardrails,skills}/` structure,
  extract decision/fact stubs from git history and existing docs, audit
  existing guardrails for missing derivation, bootstrap a doc-drift
  manifest, and propose skill-gap domains.
- **`steward`** — the ongoing six-check pass (new decision? fact changed?
  automatable rule? contradiction? doc drift? guardrail stale?) run after
  a work session. Assumes the structure `bootstrap` sets up already
  exists; points to `bootstrap` when it doesn't.

`bootstrap` carries the material that runs once (directory creation,
git-history mining, the full skill-gap-detection table); `steward` carries
only what matters on every single invocation (the six checks, the artifact
frontmatter formats, the derivation recipe), kept as lean as the four
existing skills. See `docs/facts/0004-kms-skill-names-steward-bootstrap.md`
for how these two names were settled.

## Why

`steward`'s six checks run every session a project has adopted this
system — the same "loaded repeatedly, so keep it thin" pressure that
shaped `clarify`, `roadmap`, `attribute`, and `changelog`. `bootstrap`'s
git-mining and directory-setup steps run once (or rarely, as a gap-fill).
One combined skill would force the common case to carry the rare case's
weight on every load, same reasoning as
`docs/decisions/0002-commit-pr-attribution-skill-design.md`'s
authoring-vs-retrospective split for `attribute`/`changelog`.

Both land in the existing `kms` plugin rather than a new one, for the
same reason `attribute`/`changelog` did: they're meaningless without the
`docs/{facts,decisions,guardrails,skills}/` structure `roadmap` already
establishes (`docs/decisions/0001-knowledge-artifact-storage-convention.md`)
— in fact `roadmap`'s own structure-detection step already names "a
knowledge-steward-style skill file" as the first thing to look for, so
`steward` formalizes exactly what `roadmap` was already deferring to.

The artifact frontmatter these two skills introduce (`kind`,
`governed-by`, `grounded-in`, `derivation-note`, `last-verified`,
`governed-facts`, `fitness-functions`) is additive to this repo's own
`id/title/status/date/tags` base — extending, not replacing, the format
`docs/decisions/0001-knowledge-artifact-storage-convention.md` set.

## Tradeoffs considered

- **One combined skill covering both setup and maintenance**: simplest
  single file, but forces every ongoing invocation to load one-time-only
  setup material. Rejected — same reasoning that already split
  `attribute`/`changelog`.
- **New plugin for these two skills**: cleaner in isolation, but adds a
  cross-plugin dependency on `kms`'s own artifact structure for no
  benefit at this repo's size. Rejected, matching
  `docs/decisions/0002-commit-pr-attribution-skill-design.md`'s reasoning.
- **Chosen: two skills, `bootstrap` (one-time) and `steward` (ongoing),
  in the existing `kms` plugin.**
