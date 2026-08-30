---
id: 0007-claude-md-agents-md-symlink
title: Rewrite CLAUDE.md as AGENTS.md, keep CLAUDE.md as a symlink
status: accepted
date: 2026-07-29
tags: [kms, agent-agnostic, claude-md, agents-md]
track: process
---

## Decision

`CLAUDE.md`'s content moves to a new `AGENTS.md` (the emerging
cross-agent convention for project instructions), rewritten in
agent-neutral language — no "guidance to Claude Code" framing, no
assumption that the reading agent is Claude Code specifically. The repo's
factual description (it *is* a Claude Code plugin marketplace — see
`docs/decisions/0006-agent-agnostic-scope.md`) is preserved, just phrased
as information any agent can use rather than as an address to Claude Code.

`CLAUDE.md` itself is replaced with a symlink to `AGENTS.md`, so Claude
Code (which looks for `CLAUDE.md` specifically) keeps working with zero
behavior change, while any other agent/tool that knows the `AGENTS.md`
convention also finds the same content under its own expected filename.
There is exactly one copy of the text on disk.

## Why

`CLAUDE.md` as a *filename* is a Claude-Code-only convention, independent
of what its prose says — an agent that only knows to look for `AGENTS.md`
would never find it. A symlink gets both conventions covered from a
single source file, avoiding the drift risk of maintaining two prose
copies by hand.

## Tradeoffs considered

- **Add AGENTS.md, keep CLAUDE.md as a separate file**: no risk of the
  symlink behaving unexpectedly in some environment, but two files with
  overlapping prose will drift the first time either is edited without
  the other.
- **Rename CLAUDE.md to AGENTS.md outright, no CLAUDE.md left**: simplest
  single-file option, but risks Claude Code no longer auto-loading project
  instructions if it looks specifically for `CLAUDE.md` and doesn't follow
  `AGENTS.md`. Rejected — don't regress the existing Claude Code experience
  to gain agent-neutrality.
- **Chosen: rewrite content into AGENTS.md, make CLAUDE.md a symlink to
  it.** One source of truth, both filenames resolve to it, no drift risk,
  no regression for Claude Code. The implementation plan
  (`docs/plans/agent-agnostic-repo.md`) includes verifying Claude Code
  still reads project instructions correctly through the symlink before
  calling this done.
