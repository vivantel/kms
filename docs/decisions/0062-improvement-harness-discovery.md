---
id: 0062-improvement-harness-discovery
title: Improvement harness uses a unified queue from all signals (lint, evals, capture, drift)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "discovery", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall discover work via a unified priority queue fed by all signal sources:

- **Lint violations** (from `lint` skill): each violation → queue item with type `lint-fix`, severity = violation level (error > warn > info), file = violating file, context = violation details.
- **Eval regressions/failures** (from eval harness `0043`): each failed case → queue item with type `skill-rewrite`, severity = high, file = skill under test, context = failure diff.
- **Capture drift** (from `capture` skill): each detected human-doc drift, contradiction, or stale fact → queue item with type `kb-repair`, severity = medium, file = affected artifact, context = drift details.
- **Guardrail derivation staleness** (from `lint` check `guardrail-re-derivation-on-source-change`): each stale guardrail → queue item with type `guardrail-update`, severity = medium, file = guardrail, context = source decision/fact that changed.
- **Scheduled full scan**: periodic `lint` + `query` sweep for gaps, missing cross-references, orphaned artifacts → queue items with type `kb-repair`, severity = low.

Queue items are prioritized by: (1) severity, (2) impact scope (number of dependent artifacts), (3) confidence (signal source reliability), (4) age (older issues first). The orchestrator drains the queue in priority order, dispatching to the appropriate improvement subagent.

## Rationale

- Siloed signal handling misses cross-cutting issues: a lint violation in a skill might be caused by a stale guardrail; fixing the guardrail first prevents the lint violation from recurring.
- Unified prioritization ensures the highest-leverage fixes happen first (e.g., a single guardrail update that resolves 10 lint violations).
- The queue is the single source of truth for "what needs improving" — observable, auditable, and configurable.
- Existing skills (`lint`, `capture`, eval harness) already produce structured output; the harness just normalizes and merges them.

## Consequences

- The orchestrator must implement a queue data structure (JSON file in worktree) with priority ordering.
- Each signal source needs a normalization adapter (lint → queue, evals → queue, capture → queue).
- Dependency tracking: when a queue item is processed, the harness must check if it invalidates or resolves other queued items (re-prioritize or dedupe).
- Configurable signal weights in `.opencode/improvement.yaml` (e.g., `lint_weight: 1.0`, `eval_weight: 2.0`).
