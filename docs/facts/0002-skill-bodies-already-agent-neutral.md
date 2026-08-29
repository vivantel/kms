---
id: 0002-skill-bodies-already-agent-neutral
title: The four SKILL.md bodies contain no Claude/Anthropic/tool-specific language
status: current
date: 2026-07-29
tags: [kms, agent-agnostic, audit]
---

As of 2026-07-29, an audit of all four skill instruction bodies —
`plugins/kms/skills/{clarify,roadmap,attribute,changelog}/SKILL.md` —
found no occurrences of "Claude", "Claude Code", "Anthropic", specific
tool names (e.g. "Bash tool", "Read tool"), slash-command syntax
(`/kms:...`), or any other agent-product-specific term, in either the
YAML frontmatter (`name`, `description`) or the instruction body.

Search performed: `grep -rniE "claude|anthropic|slash command|/kms:|bash
tool|read tool|edit tool|write tool|tool use" plugins/kms/skills/*/SKILL.md`
— zero matches.

Where the skills reference tooling at all (e.g. `clarify` and `roadmap`'s
"Use a selectable-question tool if the environment provides one, ...
Otherwise present as plain numbered text"), the language is already
phrased generically, conditional on tool availability rather than naming
a specific tool.

This is the descriptive baseline behind
`docs/decisions/0006-agent-agnostic-scope.md` and the guardrail in
`docs/guardrails/agent-agnostic-skill-content.md`: no rewrite of existing
skill bodies was needed to meet the agent-agnostic bar, only a standing
rule to keep meeting it going forward.
