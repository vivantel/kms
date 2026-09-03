---
id: 0002-commit-pr-attribution-skill-design
title: Split commit/PR/changelog work into two skills, added to the kms plugin
status: active
date: 2026-07-29
tags: [kms, git, commit-messages, pull-requests]
track: process
---

## Decision

The request to (1) write intent-first commit/PR messages, (2) keep
knowledge artifacts traceable through commit history, and (3) produce a
changelog from that history is split into two skills, both added to the
existing `kms` plugin (`plugins/kms/skills/`):

- **`attribute`** — authoring-time skill. Writes commit messages and PR
  descriptions, and embeds the artifact-traceability links (see
  `docs/decisions/0003-commit-trailer-traceability.md`).
- **`changelog`** — retrospective skill. Reads commit history after the
  fact and renders a changelog from it (see
  `docs/decisions/0005-changelog-generation-design.md`).

## Why

Splitting by *when* each runs (authoring vs. retrospective) avoids
conflating two different workflows in one SKILL.md. A three-way split
(commit / PR / changelog) was rejected because commit-message and
PR-description authoring share almost everything (the Why-first framing,
the traceability trailers) — splitting them would just duplicate that
logic across two files. A single skill covering all three was rejected
because it would mix an authoring-time flow with a retrospective one in a
single, overly long SKILL.md.

Both skills live inside the `kms` plugin rather than a new plugin, because
they are meaningless without the `docs/{facts,decisions,guardrails,skills}/`
artifact structure that `kms` (specifically `roadmap`) owns — a separate
plugin would introduce a cross-plugin dependency for no real benefit at
this repo's current size.

## Tradeoffs considered

- **Three skills (commit, PR, changelog)**: finest granularity, but
  commit-message and PR-description authoring overlap heavily.
- **One skill for all three**: simplest to discover, but conflates
  authoring-time and retrospective-time workflows in one long file.
- **Chosen: two skills, split by authoring vs. retrospective** — `attribute`
  and `changelog`.
- **New plugin vs. kms plugin**: a new plugin would be cleaner in isolation
  but adds a dependency on kms's artifact structure. Chosen: kms plugin.
