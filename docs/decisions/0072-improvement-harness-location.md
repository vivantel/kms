---
id: 0072-improvement-harness-location
title: Improvement harness code lives under .opencode/agent/improve/ and plugins/kms/hooks/
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "location", "packaging", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness artifacts shall be located as follows:

| Artifact | Location | Type |
|----------|----------|------|
| Subagent definitions | `.opencode/agent/improve/*.md` | Infrastructure |
| Orchestrator script | `plugins/kms/hooks/improvement-runner.sh` | Infrastructure (hook) |
| Configuration | `.opencode/improvement.yaml` | Config |
| Skill interface | `plugins/kms/skills/improvement-harness/SKILL.md` | Plugin skill |
| Skill examples | `plugins/kms/skills/improvement-harness/examples.md` | Plugin skill |
| KB procedure | `docs/skills/improvement-harness.md` | Governed procedure |
| Improvement log | `docs/improvement-log.md` | Runtime artifact |

## Rationale

- `.opencode/agent/improve/` is the native location for OpenCode subagents — discoverable by `opencode agent list` and invocable by name.
- `plugins/kms/hooks/` is the established location for plugin automation (capture-nudge.sh, lint-nudge.sh). The orchestrator is a hook-style script.
- `.opencode/improvement.yaml` follows OpenCode's config convention (like `.opencode.json`, `.opencode/agent/`).
- The skill interface in `plugins/kms/skills/` makes the harness installable as part of the kms plugin (users get the skill via plugin install).
- The KB procedure in `docs/skills/` makes the harness queryable and lintable within this repo's dogfooded KB.
- `docs/improvement-log.md` is a runtime artifact in the KB directory, append-only, not governed by `lint` (like plans per `0037`).

## Consequences

- The plugin manifest (`plugins/kms/.claude-plugin/plugin.json`) doesn't need to change — the skill is discovered by directory scan.
- The Codex manifest (`plugins/kms/.codex-plugin/plugin.json`) similarly picks up the skill automatically.
- The Kilo remote-skills index (`plugins/kms/skills/index.json`) must be updated to include the new skill.
- `uninstall` skill must remove `.opencode/agent/improve/`, `plugins/kms/hooks/improvement-runner.sh`, and the skill directory.
- The hooks.json must be updated to register the improvement-runner (optional, for auto-activation on install).
