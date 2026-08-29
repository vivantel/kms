---
id: changelog-skill-behavior
title: Procedural spec for the changelog skill
status: active
date: 2026-07-29
tags: [kms, git, procedural]
---

## Procedure

This describes how the `changelog` skill (to be implemented at
`plugins/kms/skills/changelog/SKILL.md`, see
`docs/plans/commit-pr-attribution-skills.md`) should decide and act. It is
the procedural counterpart to
`docs/decisions/0005-changelog-generation-design.md`.

### Trigger

Explicit invocation only (e.g. "/kms:changelog", "generate a changelog").

### Determining the commit range

1. Run `git tag --list` (or `git describe --tags --abbrev=0`) to find the
   most recent tag.
2. If a tag exists, use `git log <tag>..HEAD`.
3. If no tag exists, use the full history (`git log`).

### Rendering entries

1. For each commit in range, parse the Conventional Commit type prefix
   from the summary line and the Why-body from the message.
2. Map type → category:
   - `feat` → **Added**
   - `fix` → **Fixed**
   - `docs` → **Documentation**
   - `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore` →
     **Changed**
3. Under each category heading, list one bullet per commit using its
   Why-summary (not the raw Conventional Commits subject line).
4. Ask the user for a version number and date before writing anything.
   Write the section heading as `## [x.y.z] - date`. Do not write to or
   invent an `[Unreleased]` section, and do not infer the version number.

### Output

Prepend the new section to `CHANGELOG.md` at the repo root (create the
file with a top-level `# Changelog` heading if it doesn't exist yet).

## Why this is procedural, not axiomatic

These are "how to decide/act" rules that operationalize
`docs/decisions/0005-changelog-generation-design.md`; they don't carry
independent tradeoffs of their own beyond what that decision already
settled.
