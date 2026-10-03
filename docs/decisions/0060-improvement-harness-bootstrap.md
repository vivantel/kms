---
id: 0060-improvement-harness-bootstrap
title: Improvement harness uses git worktree with pinned skills for bootstrap isolation
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "bootstrap", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall bootstrap each run in an isolated git worktree with pinned (frozen) skill versions:

1. The orchestrator (`improvement-runner.sh`) creates a temporary git worktree from a known-good commit (e.g., the latest tagged release or a configured `baseline_ref`).
2. It copies the pinned skill definitions (`.opencode/agent/improve/*.md`, `plugins/kms/skills/**/SKILL.md`, `plugins/kms/shared/**`) into the worktree.
3. The improvement run executes entirely within this worktree using the pinned skills.
4. Only after verification passes are changes committed back to the original worktree (or a target branch).
5. The temporary worktree is discarded.

## Rationale

- The harness modifies skills (including its own subagent definitions). Running with live skills creates a circular dependency: the harness needs skills to run, but the run modifies those skills.
- Git worktrees provide filesystem isolation without a full clone — fast, cheap, and native to git.
- Pinning to a known-good commit (tag or `baseline_ref` in config) ensures reproducibility and prevents a broken harness from breaking its own next run.
- This mirrors the eval harness pattern (`kilo-runner.sh` lines 57-80) which copies skills into a scratch directory before running.

## Consequences

- The orchestrator must manage worktree lifecycle (create, populate, run, commit back, cleanup).
- `baseline_ref` in `.opencode/improvement.yaml` defaults to the latest semver tag; can be overridden to a specific commit for bisecting.
- Pinned skills include both the harness's own subagents (`.opencode/agent/improve/`) and the shipped KMS skills (`plugins/kms/skills/`), since improvement skills may read shipped skills as context.
- The worktree must have a clean git state before the run; the orchestrator asserts this.
