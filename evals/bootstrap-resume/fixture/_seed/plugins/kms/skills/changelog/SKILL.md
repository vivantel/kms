---
name: changelog
description: Generate a CHANGELOG.md entry from git commit history (since the last tag, or full history if none exists), grouped Keep a Changelog style from Conventional Commit type prefixes and Why-bodies. Use when the user wants a changelog produced or updated, e.g. "generate a changelog", "update the changelog for this release".
---

Generate a `CHANGELOG.md` entry from git commit history. This skill only runs when explicitly invoked — never automatically.

## Determining the commit range

1. Find the most recent tag with `git tag --list` (or `git describe --tags --abbrev=0`).
2. If a tag exists, use `git log <tag>..HEAD`.
3. If no tag exists, use the full history (`git log`).

## Rendering entries

1. For each commit in range, parse the Conventional Commit type prefix from the summary line and the Why-body from the message.
2. Map type to category:
   - `feat` → **Added**
   - `fix` → **Fixed**
   - `docs` → **Documentation**
   - `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore` → **Changed**
3. Under each category heading, list one bullet per commit using its Why-summary — not its raw Conventional Commits subject line.
4. Ask the user for a version number and date before writing anything. Write the section heading as `## [x.y.z] - date`. Never write to or invent an `[Unreleased]` section, and never infer the version number yourself.

## Output

Prepend the new section to `CHANGELOG.md` at the repo root. If the file doesn't exist yet, create it with a top-level `# Changelog` heading.

## Explicitly out of scope

No auto-versioning, no release automation, no enforced release cadence. This skill only renders what's already in commit history when asked.
