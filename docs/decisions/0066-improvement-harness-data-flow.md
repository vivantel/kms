---
id: 0066-improvement-harness-data-flow
title: Improvement harness uses a continuous convergence loop (detect → fix → verify → repeat)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "data-flow", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

A single improvement run shall execute a continuous convergence loop per improvement type, not a linear pipeline:

```
for each improvement_type in priority_order:
  passes = 0
  while passes < max_passes:
    queue_items = discover(improvement_type)  # from unified queue (0062)
    if queue_items.empty: break
    
    for item in queue_items:
      result = invoke_subagent(improvement_type, item)  # detect → fix
      verified = verify(result, improvement_type)       # verify
      if verified:
        commit(result)  # or stage for human review
      else:
        escalate(item, result)
    
    if converged(improvement_type):  # metrics + semantic hash (0061)
      break
    passes += 1
```

The outer loop processes improvement types in priority order (lint-fix → guardrail-update → skill-rewrite → kb-repair), because earlier types may resolve later types' queue items. The inner loop repeats until convergence or max passes.

## Rationale

- A linear pipeline (scan → queue → prioritize → execute → verify → commit) assumes one pass is enough. In practice, fixing a guardrail may resolve lint violations that then reveal skill clarity issues that then require another guardrail update.
- The convergence loop naturally handles this: each pass re-discovers the queue from current state, so newly created or resolved items are handled.
- Priority ordering ensures high-leverage, mechanical fixes (lint, guardrails) run first, reducing noise for subjective passes.
- This matches how `lint` + `capture` already work in practice: humans run lint, fix, run lint again, until clean.

## Consequences

- The orchestrator must maintain per-type state across passes (queue, metrics, semantic hashes).
- `discover()` must be idempotent and fast — it runs every pass.
- `verify()` must be deterministic and fast — it runs every fix.
- Max passes (`0061`) bounds total runtime; typical runs converge in 1-2 passes.
- The worktree model (`0060`) ensures each pass sees a clean slate (only committed changes persist).
