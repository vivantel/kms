---
id: 0006-agent-agnostic-scope
title: '"Agent-agnostic" pass is scoped to skill content, not packaging'
status: superseded
superseded-by: 0008-native-codex-plugin-support
date: 2026-07-29
tags: [kms, agent-agnostic, scope]
track: product
---

> **Superseded 2026-07-29** by
> `docs/decisions/0008-native-codex-plugin-support.md`: the "packaging
> stays Claude-Code-specific" half of this decision no longer holds now
> that we ship a native Codex plugin manifest for the same skills. The
> "skill *content* must stay agent-neutral" half (and the guardrail it
> produced) is unaffected and still stands. Kept below for historical
> record — do not treat the packaging section as current.

## Decision

The request to "make the repo agent-agnostic" is scoped to the *content*
of skill instructions — the prose in each `plugins/kms/skills/*/SKILL.md`
body — not to the repo's packaging or distribution mechanism.

The Claude Code plugin scaffolding (`.claude-plugin/marketplace.json`,
`plugins/kms/.claude-plugin/plugin.json`, the `SKILL.md` file convention,
`/kms:skillname` invocation) stays exactly as it is. This repo remains,
and is described as, a Claude Code plugin marketplace (see `CLAUDE.md` /
`docs/decisions/0007-claude-md-agents-md-symlink.md`).

What "agent-agnostic" means in practice: skill instruction bodies should
not hardcode assumptions that only hold for Claude Code specifically —
no references to Claude/Anthropic by name, no Claude-Code-only tool names,
no slash-command-specific syntax baked into the instructions themselves —
so the instructional text would still make sense if read or adapted by a
different agent. See `docs/facts/0002-skill-bodies-already-agent-neutral.md`
for the audit that confirmed the current four skills already meet this bar,
and `docs/guardrails/agent-agnostic-skill-content.md` for the resulting
standing rule for future skills.

## Why

The repo's entire distribution mechanism (marketplace manifest, plugin
manifest, `SKILL.md` discovery, slash-command invocation) is inherently a
Claude Code convention — there is no other consumer of that scaffolding
today, and replacing or duplicating it was judged to be solving a problem
that doesn't exist yet (no second agent/tool has asked to consume these
skills). Scoping the effort to content keeps the change small, reversible,
and immediately verifiable, while still delivering the actual goal:
skill instructions that don't lock in Claude-Code-specific assumptions.

## Tradeoffs considered

- **Content-level only (chosen)**: keep the Claude Code plugin packaging
  as-is; audit and, where needed, rewrite skill bodies to avoid
  Claude-Code-only assumptions. Cheapest, lowest risk, and matches that
  packaging has exactly one real consumer today.
- **Add a parallel generic format**: also publish skill instructions as
  plain markdown under a non-plugin directory any tool could load
  directly. Rejected as premature — no second consumer exists yet, and it
  would mean maintaining two copies of every skill in sync.
- **Replace the packaging entirely**: drop or de-emphasize the Claude Code
  plugin marketplace format in favor of a more universal spec. Rejected —
  this repo's whole reason for existing (per `CLAUDE.md`) is to be a
  Claude Code plugin marketplace; replacing that would be a much larger,
  differently-motivated project than "make the skill content portable."
