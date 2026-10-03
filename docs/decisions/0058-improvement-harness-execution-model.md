---
id: 0058-improvement-harness-execution-model
title: Improvement harness uses OpenCode recursively for agent execution
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "opencode", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall execute improvement skills using OpenCode itself (recursive invocation), not Kilo Code CLI or Claude Code SDK.

- The external orchestrator (`improvement-runner.sh`) invokes `opencode agent improve-harness` (or subagents directly) in a git worktree.
- Improvement skills are implemented as OpenCode subagents (`.opencode/agent/improve/*.md`).
- The harness uses OpenCode's native tool access (read, write, edit, grep, glob, bash) for all file operations.
- No external API keys required — relies on OpenCode's built-in model access.

## Rationale

- OpenCode is already the host environment; recursive use dogfoods the platform and avoids a second agent runtime.
- Kilo Code CLI (`0043`) is optimized for eval-style "run skill, check output" — not for multi-step, tool-using improvement workflows that need to read context, edit files, run lint, verify, commit.
- Claude Code SDK would require API keys and a separate auth model; OpenCode's built-in access is zero-config.
- The bootstrap problem (`0060`) is solved by running in a git worktree with pinned skill versions, so the harness never depends on skills it might modify.
- Self-improvement (`0070`) becomes natural: the harness improves its own subagent definitions.

## Consequences

- Requires OpenCode to support headless/subagent invocation from a script (verify CLI flags).
- The orchestrator must manage OpenCode's working directory, model selection, and permissions.
- Token economy (`0016`) applies to the harness's own prompts — subagent definitions must be concise.
- CI runs need OpenCode installed (add to GitHub Actions setup).
