---
id: 0005-changelog-generation-design
title: Thin, on-demand changelog skill reading from commit trailers
status: accepted
date: 2026-07-29
tags: [kms, git, changelog]
track: process
---

## Decision

The `changelog` skill is a separate, thin, on-demand skill (not folded
into `attribute`, and not dropped) with this behavior:

- **Range**: commits since the last git tag; falls back to full history
  if no tags exist (true for this repo today).
- **Source data**: each commit's Conventional Commit type prefix, Why-body
  (see `docs/decisions/0004-conventional-commits-adoption.md`), and `Refs:`
  trailers (see `docs/decisions/0003-commit-trailer-traceability.md`).
- **Grouping**: Keep a Changelog style, via a type → category mapping:
  `feat` → Added, `fix` → Fixed, `docs` → Documentation, everything else
  (`style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`) → Changed.
  Each entry is the commit's Why-summary, not its raw subject line.
- **Output**: a single `CHANGELOG.md` at the repo root (not per-plugin).
- **Heading**: the skill asks the user for a version number and date at
  invocation time, and writes `## [x.y.z] - date`. It does not write to an
  `[Unreleased]` section and does not infer or bump the version itself.

Explicitly out of scope: auto-versioning, release automation, enforced
release cadence.

## Why

The user questioned whether a changelog skill was over-engineering for a
repo with no release process, no tags, and no CHANGELOG.md yet. The
resolution: it's justified because (a) the `kms` plugin already has a
`version` field in `plugin.json` that consumers see when installing/
updating, and (b) once `attribute` puts structured Why-bodies and `Refs:`
trailers on commits, generating a changelog from them is nearly free — the
skill only has to render already-structured data, not infer intent. The
scope stays deliberately thin (no auto-versioning, no automated releases)
to avoid inventing process the repo doesn't have.

A single repo-root `CHANGELOG.md` was chosen over per-plugin changelogs
because the repo currently has exactly one plugin and no independent
per-plugin release cadence — per-plugin changelogs were judged speculative
for the marketplace's current size.

Asking for the version/date at invocation (rather than writing to
`[Unreleased]`) keeps versioning a human decision, consistent with the
"no auto-versioning" scope — an `[Unreleased]` heading would need a
separate manual rename step later that this skill doesn't own.

## Tradeoffs considered

- **Fold into `attribute` as a mode**: avoids a second SKILL.md, but mixes
  an authoring-time and a retrospective-time skill. Rejected — see
  `docs/decisions/0002-commit-pr-attribution-skill-design.md`.
- **Drop for now**: avoids building for a workflow that doesn't exist yet,
  but the marginal cost is low once commits already carry structured
  trailers. Rejected in favor of a thin version.
- **Range: since last CHANGELOG.md entry** vs. **since last tag**: the
  tag-based approach was chosen as the standard convention, with a
  full-history fallback for this repo's current no-tags state.
- **Flat list by raw commit type** vs. **Keep a Changelog category
  mapping**: the mapped/grouped form was chosen as more readable to a
  human consumer.
