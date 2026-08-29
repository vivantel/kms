---
id: commit-attribution-format
title: Commits written by the attribute skill must follow the attribution format
status: active
date: 2026-07-29
tags: [kms, git, commit-messages, guardrail]
---

## Guardrail

Whenever the `attribute` skill writes a commit message, it MUST:

1. Prefix the summary line with a Conventional Commit type from the set
   `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`,
   `ci`, `chore` (`type: summary`).
2. Include a body paragraph explaining the intent — not merely what
   changed — before any trailers.
3. Reference any related knowledge artifact using a `Refs:
   <repo-relative-path>` git trailer — never an issue number, never a
   prose mention in the body. One `Refs:` trailer per referenced artifact.

This guardrail applies only to commits produced through the `attribute`
skill, not to every commit in the repo (see
`docs/decisions/0004-conventional-commits-adoption.md` — the convention is
explicit-invocation-only, not a standing CLAUDE.md rule).

## Derivation

- **Axiomatic basis**: the team committed to Conventional Commits
  (`docs/decisions/0004-conventional-commits-adoption.md`) and to
  `Refs:` trailers as the sole traceability mechanism
  (`docs/decisions/0003-commit-trailer-traceability.md`).
- **Descriptive basis**: the `attribute` skill is the only place these
  conventions are enforced (explicit-invocation-only, per
  `docs/facts/0001-kms-skill-names.md` and the skills it names).
- **Normative conclusion**: therefore, any commit the `attribute` skill
  produces must carry a typed prefix, a Why-body, and path-based `Refs:`
  trailers — consistently, every time the skill runs.
