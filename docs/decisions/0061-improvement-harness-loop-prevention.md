---
id: 0061-improvement-harness-loop-prevention
title: Improvement harness uses layered loop prevention (idempotency + max iterations + convergence + human gate)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "safety", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall prevent runaway improvement loops through four layered mechanisms:

1. **Idempotency checks (semantic diff)**: Before committing, compute a semantic hash of the changed content (AST-aware for Markdown/YAML, ignoring whitespace/formatting). If the semantic hash matches the pre-run state, skip the commit. This catches no-op "improvements" that only reformat.

2. **Max iterations per cycle**: Hard limit of 3 passes per improvement type per run. If a skill still produces changes on pass 3, the harness stops, logs the unconverged file, and escalates to the improvement log for human review.

3. **Convergence detection**: Track a per-file improvement metric (lint violation count, eval score, semantic similarity to previous version). Stop when marginal improvement < 1% over two consecutive passes.

4. **Human gate for subjective changes**: Mechanical fixes (lint auto-fix) can auto-commit freely. Substantive rewrites (skill body, KB repairs) require a "high confidence" threshold (eval score improvement > 5% AND semantic diff < 20%) to auto-commit; otherwise they are staged and logged for human review.

## Rationale

- Idempotency alone is insufficient: a skill might oscillate between two semantically different but equally "valid" states.
- Max iterations alone is insufficient: it doesn't distinguish "still improving" from "stuck in a loop".
- Convergence detection alone is insufficient: metrics can be gamed or misleading.
- Human gate alone is insufficient: it doesn't scale for mechanical fixes.
- Layered defense means any single mechanism failing is caught by the others.

## Consequences

- Each improvement skill must implement a `verify()` function that returns the semantic hash and metrics.
- The orchestrator maintains per-file state across passes (in the worktree's `.improvement-state/`).
- The improvement log (`0064`) records every pass, metric, and commit decision for audit.
- Configurable thresholds in `.opencode/improvement.yaml` (max_passes, convergence_threshold, confidence_threshold).
