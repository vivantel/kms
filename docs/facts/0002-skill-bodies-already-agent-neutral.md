---
id: 0002-skill-bodies-already-agent-neutral
title: The fourteen SKILL.md bodies contain no Claude/Anthropic/tool-specific language
status: active
date: 2026-08-30
tags: [kms, agent-agnostic, audit]
kind: environmental
governed-by: 0006-agent-agnostic-scope
---

As of 2026-08-30, an audit of all fourteen skill instruction bodies —
`plugins/kms/skills/{clarify,roadmap,bootstrap,capture,lint,query,attribute,changelog,quickstart,brainstorm,onboard,refactor-plan,conform,uninstall}/SKILL.md`
— found no occurrences of "Claude", "Claude Code", "Anthropic", specific
tool names (e.g. "Bash tool", "Read tool"), slash-command syntax
(`/kms:...`), or any other agent-product-specific term, in either the
YAML frontmatter (`name`, `description`) or the instruction body.
Re-verified after every round of edits to these bodies since the
original 2026-07-29 audit (originally four skills; `bootstrap`/`steward`
added from `0009` onward, `lint`/`query` from `0016`/`0017`,
`quickstart`/`brainstorm`/`onboard`/`refactor-plan` from `0019`-`0023`,
`uninstall` from `0030`, `steward` renamed `capture` and `conform` added
from `0031`/`0032`) — including catching and fixing real violations
twice: `lint`'s own "Out of scope" note first, then `bootstrap` and
`uninstall` both naming "Claude Code"/"CLAUDE.md" while describing the
AGENTS.md-wiring mechanism, in the very next round of edits after the
first fix.

Search performed: `grep -rniE "claude|anthropic|slash command|/kms:|bash
tool|read tool|edit tool|write tool|tool use" plugins/kms/skills/*/SKILL.md`
— zero matches.

Where the skills reference tooling at all (e.g. `clarify` and `roadmap`'s
"Selectable-question tool available? Use it; ... No tool: number each
option with plain digits..."), the language is already phrased
generically, conditional on tool availability rather than naming a
specific tool.

This is the descriptive baseline behind
`docs/decisions/archive/0006-agent-agnostic-scope.md` and the guardrail in
`docs/guardrails/agent-agnostic-skill-content.md`: no rewrite of existing
skill bodies was needed to meet the agent-agnostic bar, only a standing
rule to keep meeting it going forward.
