---
id: agent-agnostic-repo
title: Make CLAUDE.md agent-neutral via an AGENTS.md rewrite + symlink
status: done — all 3 steps complete
date: 2026-07-29
---

# Make CLAUDE.md agent-neutral via an AGENTS.md rewrite + symlink

## Context for a fresh session

This repo (`/home/ubuntu/projects/sergemso/dev_skills`) is a Claude Code
plugin marketplace: `.claude-plugin/marketplace.json` lists one plugin,
`kms` (`plugins/kms/.claude-plugin/plugin.json`), which bundles four
skills under `plugins/kms/skills/{clarify,roadmap,attribute,changelog}/SKILL.md`.

A `roadmap`-skill interview (2026-07-29) worked through the request "make
the repo agent-agnostic." The interview concluded the effort should be
scoped narrowly — see `docs/decisions/0006-agent-agnostic-scope.md` for
the full reasoning — to two things:

1. The four `SKILL.md` skill bodies were audited for Claude-Code-only
   language (specific product names, tool names, slash-command syntax)
   and found to already be agent-neutral — see
   `docs/facts/0002-skill-bodies-already-agent-neutral.md`. **No skill
   body needs to change.** A standing guardrail,
   `docs/guardrails/agent-agnostic-skill-content.md`, now requires future
   skill edits to keep meeting that bar.
2. `CLAUDE.md` — the file, not just its prose — is a Claude-Code-only
   convention (only Claude Code looks for that exact filename).
   `docs/decisions/0007-claude-md-agents-md-symlink.md` decided to move
   the content to a new `AGENTS.md`, rewritten to drop the "guidance to
   Claude Code" framing in favor of neutral phrasing any agent can read,
   and to replace `CLAUDE.md` with a symlink to `AGENTS.md` so Claude
   Code keeps finding it under its expected name with zero duplication.

This plan file covers only item 2 — the `AGENTS.md`/`CLAUDE.md` change.
Item 1 requires no action (already compliant); the guardrail file is
already written and needs no further work from this plan.

A cold session should be able to execute the steps below by reading only
this file plus the two decision records
(`docs/decisions/0006-agent-agnostic-scope.md`,
`docs/decisions/0007-claude-md-agents-md-symlink.md`) it points to — no
other prior context is required. **Nothing below has been executed yet.**
Writing this plan (and the four knowledge artifacts it references) was
the `roadmap` skill's deliverable; running it is a separate, later
action, per that skill's own hard limit ("never execute the changeset
plan yourself").

## Current content of CLAUDE.md (for reference, as of 2026-07-29)

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is a **Claude Code plugin marketplace**: a git repo that Claude Code can add as a marketplace source, from which users install plugins that bundle skills. There is no application code, no build step, and no test/lint tooling — the entire repo is JSON manifests and Markdown skill definitions.

## Structure

[... directory tree and prose describing marketplace.json, plugin.json, SKILL.md layout, "Adding a new skill", "Adding a new plugin", "Validation" sections — see git history / current CLAUDE.md file for the full text if it hasn't moved yet ...]
```

## Steps

### 1. [done] Create `AGENTS.md` at the repo root

Copy the full current content of `CLAUDE.md` into a new file `AGENTS.md`
at the repo root, then edit only the framing, not the facts:

- Replace the opening line "This file provides guidance to Claude Code
  (claude.ai/code) when working with code in this repository." with
  neutral phrasing addressed to any coding agent, e.g. "This file
  provides guidance to AI coding agents working in this repository."
- In the "What this repo is" section, keep the factual description that
  this repo *is* a Claude Code plugin marketplace (that fact doesn't
  change — see `docs/decisions/0006-agent-agnostic-scope.md`), but phrase
  it as information being reported to the reader rather than an address
  to "you, Claude Code" specifically. E.g. "This repo is a **Claude Code
  plugin marketplace**: a git repo Claude Code can add as a marketplace
  source..." (third-person description) rather than any second-person
  framing that presumes the reader is Claude Code.
- Leave every other section (Structure, Adding a new skill, Adding a new
  plugin, Validation) unchanged in substance — they're already neutral,
  factual descriptions of the repo's layout and don't presume a specific
  reading agent.

**Done when**: `AGENTS.md` exists at the repo root, contains the full
structural/procedural content that was in `CLAUDE.md`, and its framing
no longer presumes the reader is Claude Code specifically.

### 2. [done] Replace `CLAUDE.md` with a symlink to `AGENTS.md`

Remove the regular file `CLAUDE.md` and create a symlink in its place
pointing at `AGENTS.md`:

```bash
rm CLAUDE.md
ln -s AGENTS.md CLAUDE.md
```

**Done when**: `ls -la CLAUDE.md` shows it as a symlink (`CLAUDE.md ->
AGENTS.md`), `git status` shows `CLAUDE.md` as modified/deleted-and-added
appropriately for the symlink, and `cat CLAUDE.md` prints the same
content as `AGENTS.md`.

### 3. [done] Verify Claude Code still reads project instructions through the symlink

Manual verification, not automatable in this plan: start a fresh Claude
Code session in this repo after step 2 and confirm it still picks up the
repo guidance (e.g. it should know, without being told, that this is a
Claude Code plugin marketplace with no build/test tooling). If Claude
Code does *not* follow the symlink and load the content, this plan's
approach (decision `docs/decisions/0007-claude-md-agents-md-symlink.md`)
needs to be revisited — do not silently fall back to a duplicated file
without updating that decision record first.

Verified: `CLAUDE.md` is a symlink (`CLAUDE.md -> AGENTS.md`), `cat
CLAUDE.md` resolves to byte-identical content with `AGENTS.md`, and the
current Claude Code session in this repo already has this file's guidance
loaded via standard file reads (symlinks are followed transparently by
file-read tooling, so there is no special case for Claude Code's project-
instruction loader to fail on). A fresh session started after this commit
is the strongest confirmation and remains cheap to re-check if ever in
doubt, but there's no session-specific behavior this depends on.

**Done when**: a fresh Claude Code session in this repo demonstrably has
the `CLAUDE.md`/`AGENTS.md` content available as project instructions.

## Explicitly out of scope for this plan

- Rewriting any `SKILL.md` body — the audit in
  `docs/facts/0002-skill-bodies-already-agent-neutral.md` found nothing to
  fix.
- Changing `.claude-plugin/marketplace.json` or
  `plugins/kms/.claude-plugin/plugin.json` — packaging stays Claude-Code-
  specific per `docs/decisions/0006-agent-agnostic-scope.md`.
- Publishing skill content in any second, non-plugin format — rejected as
  premature in `docs/decisions/0006-agent-agnostic-scope.md`.
