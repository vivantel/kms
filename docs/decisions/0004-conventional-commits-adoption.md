---
id: 0004-conventional-commits-adoption
title: Adopt Conventional Commits type prefixes, applied only when the attribute skill is invoked
status: accepted
date: 2026-07-29
tags: [kms, git, commit-messages]
track: process
---

## Decision

Commit messages written by the `attribute` skill use a Conventional
Commits type prefix on the summary line (`type: summary`), drawn from the
full standard type set: `feat`, `fix`, `docs`, `style`, `refactor`,
`perf`, `test`, `build`, `ci`, `chore`.

This convention applies **only when the `attribute` skill is explicitly
invoked** (e.g. "/kms:attribute", or "write this commit with
attribution") — it is not baked into this repo's default commit
behavior via CLAUDE.md, and does not retroactively apply to existing
history.

## Why

This is a deliberate departure from this repo's existing commit history,
which uses plain imperative summaries with no type prefix (e.g. "Redesign
interview skill for scannable, comparable options" — see `git log`,
commits `08a849a` through `aa357b7`). The recommendation going into this
decision was to keep the existing plain style and only add a Why-body;
the user chose to switch to Conventional Commits instead, for the
tooling/taxonomy benefit, accepting the discontinuity with prior commits.

The full standard type set (including `test`, `ci`, `build`, `perf`,
`style`) was chosen over a trimmed-down set even though this repo
currently has no test suite, CI, or build step — the recommendation to
trim to `feat`/`fix`/`docs`/`refactor`/`chore` was declined in favor of
the complete, immediately-recognizable standard list.

Explicit-invocation-only (rather than a standing CLAUDE.md instruction)
was chosen to keep `attribute` consistent with how `clarify` and
`roadmap` already work — both require explicit invocation rather than
firing automatically.

## Tradeoffs considered

- **Keep plain imperative summary + Why body** (recommended): zero
  migration cost, but no type taxonomy.
- **Chosen: Conventional Commits, full standard type set**: enables
  type-based tooling (e.g. this repo's own `changelog` skill, see
  `docs/decisions/0005-changelog-generation-design.md`), at the cost of
  breaking continuity with the last 5 commits.
- **Automatic for every commit vs. explicit invocation**: automatic would
  guarantee consistency but overrides default git-commit behavior for
  every future session without being asked each time. Chosen: explicit
  invocation only.
