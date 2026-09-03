---
id: agent-agnostic-skill-content
title: Skill instruction bodies must stay agent-neutral
status: active
date: 2026-07-29
tags: [kms, agent-agnostic, guardrail]
governed-by: 0006-agent-agnostic-scope
grounded-in: 0002-skill-bodies-already-agent-neutral
derivation-note: >
  Given decision 0006 (skill content stays agent-neutral across agents)
  and fact 0002 (bodies already meet that bar), future skill bodies must
  not regress it.
---

## Guardrail

Any new or edited `SKILL.md` body (frontmatter `description` included)
in this repo MUST NOT:

1. Name a specific agent/AI product ("Claude", "Claude Code", "Anthropic",
   or any other vendor/agent name) as the actor the instructions are
   addressed to.
2. Hardcode a specific tool name (e.g. "the Bash tool", "the Read tool")
   as a requirement, where a generic description of the capability
   ("run a shell command", "read the file") would do instead.
3. Bake in invocation syntax specific to one host (e.g. `/kms:skillname`
   slash-command syntax) as part of the instructional content itself.

Where a skill needs to branch on tool availability (e.g. a
selectable-question UI element that may or may not exist), phrase it
conditionally — "if the environment provides X, do A; otherwise do B" —
rather than assuming a specific tool is present.

This does not extend to the repo's packaging/metadata layer
(`.claude-plugin/marketplace.json`, `plugins/kms/.claude-plugin/plugin.json`),
which is allowed to name Claude Code explicitly since that packaging format
is inherently Claude-Code-specific — see
`docs/decisions/archive/0006-agent-agnostic-scope.md`.

## Derivation

- **Descriptive basis**: `docs/facts/0002-skill-bodies-already-agent-neutral.md`
  — the four existing skill bodies were audited and already meet this bar.
- **Axiomatic basis**: `docs/decisions/archive/0006-agent-agnostic-scope.md` — the
  team committed to keeping skill *content* portable across agents even
  though the packaging stays Claude-Code-specific.
- **Normative conclusion**: therefore every future skill body must be
  checked against the three rules above before being merged, so the
  agent-neutral property confirmed today doesn't regress as skills are
  added or edited.
