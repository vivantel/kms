---
id: improvement-harness
title: Incremental automatic KMS improvement harness
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "procedural"]
operationalizes: ["improvement-harness-free-models-only", "improvement-harness-token-economy", "improvement-harness-lint-gate", "improvement-harness-eval-gate", "improvement-harness-subagent-structure"]
---

# Improvement Harness

The incremental automatic KMS improvement harness continuously improves the knowledge base and shipped skills by running improvement cycles that detect issues, apply fixes, verify them, and commit changes.

## What It Does

The harness addresses three improvement dimensions:
1. **Lint auto-fix** — mechanical fixes for guardrail violations (token economy, verbosity, cross-reference drift, formatting)
2. **Skill rewrites** — substantive improvements to `SKILL.md` bodies for clarity, structure, and effectiveness
3. **Knowledge base repairs** — fixing contradictions, stale facts, missing derivations, and gaps

A fourth dimension, **guardrail re-derivation**, occurs automatically when source decisions/facts change.

## How It Works

### Trigger Modes
- **Scheduled**: Daily via GitHub Actions (full repo scan)
- **Event-driven**: On push/PR to skills, docs, or shared (targeted scan)
- **Manual**: `opencode agent improve-harness` on demand

### Execution Model
- Runs in an isolated git worktree pinned to a known-good baseline (`0060`)
- Uses OpenCode recursively — improvement skills are OpenCode subagents (`.opencode/agent/improve/*.md`)
- Zero API keys required — uses OpenCode's free tier models (`0015`)

### Data Flow
A continuous convergence loop per improvement type (`0066`):
```
for each type in priority order:
  while not converged and passes < max:
    discover queue items from all signals (lint, evals, capture)
    dispatch to subagent → fix → verify → commit/stage
    re-discover queue from new state
```

### Verification Gates (all fixes)
1. **Lint gate** (mandatory): `lint` skill passes on modified files
2. **Eval gate** (skill-rewrite): eval harness pass rate maintained/improved
3. **Sampling gate** (subjective): 20% of KB repairs flagged for human review

### Loop Prevention
Four layered mechanisms (`0061`): semantic idempotency, max 3 passes, convergence detection (1% threshold), human gate for subjective changes.

## Configuration

`.opencode/improvement.yaml` controls all behavior: baseline ref, triggers, improvement types, loop prevention, verification thresholds, observability, safety.

## Observability

- Structured auto-commits (Conventional Commits + Refs: trailers)
- Append-only `docs/improvement-log.md` with per-run metrics
- CI verification gate on every run
- Optional dashboard from log data

## Invocation

```bash
# Scheduled (via GitHub Actions)
./plugins/kms/hooks/improvement-runner.sh --mode=scheduled

# Event-driven (via GitHub Actions)
./plugins/kms/hooks/improvement-runner.sh --mode=event --changed-files="..."

# Manual
opencode agent improve-harness
```

## Safety

- Auto-commits attributed to `kms-improvement-bot`
- Kill switch in config (`safety.kill_switch: true`)
- Max 50 files per run
- All fixes revertible via `git revert`
