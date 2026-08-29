---
id: commit-pr-attribution-skills
title: Implement the attribute and changelog skills
status: done (all 6 steps complete — see commit 58b6f4c for the smoke test)
date: 2026-07-29
---

# Implement the attribute and changelog skills

## Context for a fresh session

This repo (`/home/ubuntu/projects/sergemso/dev_skills`) is a Claude Code
plugin marketplace. It contains one plugin, `kms`
(`plugins/kms/.claude-plugin/plugin.json`, currently version `2.0.0`),
which currently has two skills: `clarify`
(`plugins/kms/skills/clarify/SKILL.md`) and `roadmap`
(`plugins/kms/skills/roadmap/SKILL.md`).

A `roadmap`-skill interview (2026-07-29) designed two new skills for that
plugin, covering commit/PR attribution and changelog generation. The
design decisions, including every tradeoff and rationale, are already
written down as knowledge artifacts:

- `docs/decisions/0001-knowledge-artifact-storage-convention.md`
- `docs/decisions/0002-commit-pr-attribution-skill-design.md`
- `docs/decisions/0003-commit-trailer-traceability.md`
- `docs/decisions/0004-conventional-commits-adoption.md`
- `docs/decisions/0005-changelog-generation-design.md`
- `docs/facts/0001-kms-skill-names.md`
- `docs/guardrails/commit-attribution-format.md`
- `docs/skills/attribute-skill-behavior.md` (procedural spec for the `attribute` skill)
- `docs/skills/changelog-skill-behavior.md` (procedural spec for the `changelog` skill)

This plan file is the only thing that turns those artifacts into working
plugin skills. A cold session should be able to execute every step below
by reading only this file plus the two `docs/skills/*.md` procedural specs
it points to — no other prior context is required. **Nothing below has
been executed yet.** Writing this plan (and the artifacts above) was the
`roadmap` skill's deliverable; running it is a separate, later action, per
that skill's own hard limit ("never execute the changeset plan yourself").

## Steps

### 1. [done] Create `plugins/kms/skills/attribute/SKILL.md`

Create the directory `plugins/kms/skills/attribute/` and a `SKILL.md`
inside it, with YAML frontmatter:

```yaml
---
name: attribute
description: Write commit messages and PR descriptions that lead with intent (why, not what), using Conventional Commits type prefixes and Refs: trailers linking to docs/{facts,decisions,guardrails,skills}/ artifacts. Use when the user wants to commit changes with attribution, or generate a PR description, e.g. "commit this with attribution", "write a PR description for this branch".
---
```

Body content: transcribe the full procedure from
`docs/skills/attribute-skill-behavior.md` (Trigger, Writing a commit
message, Writing a PR description sections) into skill-instruction prose,
and fold in the exact format requirements from
`docs/guardrails/commit-attribution-format.md` (allowed types, Why-body
requirement, `Refs:` trailer syntax). Follow the existing style of
`plugins/kms/skills/clarify/SKILL.md` and
`plugins/kms/skills/roadmap/SKILL.md` (imperative instructions, no filler).

**Done when**: the file exists, has valid YAML frontmatter (verify with
`python3 -c "import yaml,sys; yaml.safe_load(open('plugins/kms/skills/attribute/SKILL.md').read().split('---')[1])"` or equivalent),
and its body covers every rule in
`docs/skills/attribute-skill-behavior.md` and
`docs/guardrails/commit-attribution-format.md` without contradicting
either.

### 2. [done] Create `plugins/kms/skills/changelog/SKILL.md`

Create the directory `plugins/kms/skills/changelog/` and a `SKILL.md`
inside it, with YAML frontmatter:

```yaml
---
name: changelog
description: Generate a CHANGELOG.md entry from git commit history (since the last tag, or full history if none exists), grouped Keep a Changelog style from Conventional Commit type prefixes and Why-bodies. Use when the user wants a changelog produced or updated, e.g. "generate a changelog", "update the changelog for this release".
---
```

Body content: transcribe the full procedure from
`docs/skills/changelog-skill-behavior.md` (Determining the commit range,
Rendering entries, Output sections) into skill-instruction prose. Make
sure it explicitly states the type→category mapping table and that it
must ask the user for a version/date before writing (never invent a
version, never write `[Unreleased]`).

**Done when**: the file exists, has valid YAML frontmatter, and its body
covers every rule in `docs/skills/changelog-skill-behavior.md`.

### 3. [done] Bump the kms plugin version

`plugins/kms/.claude-plugin/plugin.json` currently has `"version": "2.0.0"`.
Adding two new skills is a minor (additive, non-breaking) change — bump to
`"version": "2.1.0"` following the semver precedent already visible in the
file (major bump was used for the earlier plugin rename in commit
`aa357b7`, per `git log`; this change is additive, not a rename/break, so
minor is appropriate).

**Done when**: `plugins/kms/.claude-plugin/plugin.json`'s `version` field
reads `2.1.0` and the file is still valid JSON (`python3 -m json.tool plugins/kms/.claude-plugin/plugin.json`).

### 4. [done] Update the marketplace description (optional, judgment call)

`.claude-plugin/marketplace.json`'s `kms` entry description currently
reads "Everyday development skills for Claude Code: rigorously clarify a
plan through interrogation, or turn one into durable knowledge artifacts
and a standalone roadmap." Consider extending it to mention the new
commit/PR/changelog capability, e.g. append "; attribute commits and PRs
to their underlying intent, and generate changelogs from commit history."
This step is optional — skip it if the description is judged long enough
already — but if skipped, leave this step marked `[blocked: skipped by
choice]` rather than silently deleting it, so a re-read of this file shows
it was considered.

**Done when**: either the description is updated and
`.claude-plugin/marketplace.json` is still valid JSON
(`python3 -m json.tool .claude-plugin/marketplace.json`), or the step is
explicitly marked skipped.

### 5. [done] Update CLAUDE.md's plugin/skill inventory

`/home/ubuntu/projects/sergemso/dev_skills/CLAUDE.md`'s "What this repo
is" section currently names `clarify` and `roadmap` explicitly by path
and one-line purpose ("Currently there is one plugin, `kms` ... containing
two skills: `clarify` ... and `roadmap` ..."). Update this sentence to
also name `attribute` (`plugins/kms/skills/attribute/SKILL.md`) and
`changelog` (`plugins/kms/skills/changelog/SKILL.md`) with equally short
one-line purposes, consistent with the existing style.

**Done when**: CLAUDE.md's plugin/skill inventory sentence names all four
skills with their paths.

### 6. [done] Manual smoke test

After steps 1–2, invoke `/kms:attribute` on a trivial staged change (e.g.
this very plan file being marked done) and confirm: the proposed commit
message has a Conventional Commit type prefix, a Why-body, and (if an
artifact was touched) a `Refs:` trailer with a correct repo-relative path.
This is a manual verification step, not something to automate.

**Done when**: a real `/kms:attribute` invocation produces a message
matching `docs/guardrails/commit-attribution-format.md`.

## Explicitly out of scope for this plan

- Auto-versioning or release automation for `changelog` (see
  `docs/decisions/0005-changelog-generation-design.md`).
- Making `attribute`'s conventions apply automatically to every commit in
  this repo (see `docs/decisions/0004-conventional-commits-adoption.md`).
- Backlinking commits into artifact frontmatter (see
  `docs/decisions/0003-commit-trailer-traceability.md`).
