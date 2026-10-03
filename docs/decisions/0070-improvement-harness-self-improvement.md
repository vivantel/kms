---
id: 0070-improvement-harness-self-improvement
title: Improvement harness improves itself (full dogfooding)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "dogfooding", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall improve its own artifacts:

- Its skill interface (`plugins/kms/skills/improvement-harness/SKILL.md` and `docs/skills/improvement-harness.md`)
- Its subagent definitions (`.opencode/agent/improve/*.md`)
- Its orchestrator script (`plugins/kms/hooks/improvement-runner.sh`)
- Its configuration schema (`.opencode/improvement.yaml`)

These are treated as any other target: they appear in the unified queue when `lint`, `capture`, or evals detect issues, and the appropriate improvement subagent fixes them.

## Rationale

- Dogfooding is the ultimate test: if the harness can't improve itself, it can't improve anything.
- The harness's own code is the most frequently exercised and most critical to get right.
- Self-improvement creates a virtuous cycle: as the harness improves, it gets better at improving, including improving itself.
- The bootstrap isolation (`0060`) makes this safe: the harness runs in a worktree with pinned skills, so a self-improvement that breaks the harness only affects that run's worktree, not the baseline.

## Consequences

- The harness's subagents must be able to edit their own source files (`.opencode/agent/improve/*.md`).
- The orchestrator must exclude the currently-running subagent from its own improvement queue (to avoid modifying the agent that's executing).
- Self-improvement changes go through the same verification gates (`0068`) — lint, eval (if applicable), sampling.
- The improvement log will show "harness improved harness" entries — a key health metric.
- Configurable `exclude_self_improvement: false` in `.opencode/improvement.yaml` for emergency disable.
