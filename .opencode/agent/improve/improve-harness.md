---
name: improve-harness
description: Main improvement harness orchestrator - runs convergence loop across all improvement types
tools:
  read: {}
  write: {}
  edit: {}
  grep: {}
  glob: {}
  bash: {}
model: free
---

# Improvement Harness Orchestrator

Main entry point for the improvement harness. Invoked by `improvement-runner.sh` or manually via `opencode agent improve-harness`.

## Input (via prompt)

```json
{
  "mode": "scheduled|event|manual",
  "changed_files": [],
  "config": ".opencode/improvement.yaml",
  "repo_root": "/abs/path/to/repo"
}
```

## Workflow

1. **Parse config** (`.opencode/improvement.yaml`)
2. **Bootstrap** worktree from `baseline_ref` (git worktree + pinned skills copy)
3. **Initialize** unified queue (empty JSON file in worktree)
4. **Discover** queue items from all enabled signals:
   - Lint violations → `lint-fix` items
   - Eval failures → `skill-rewrite` items
   - (v0.2+) Capture drift → `kb-repair` items
   - (v0.2+) Guardrail staleness → `guardrail-update` items
5. **Prioritize** queue by severity, impact, confidence, age
6. **Convergence loop** per improvement type (priority order):
   ```
   for type in [lint-fix, skill-rewrite]:
     passes = 0
     while passes < max_passes:
       items = queue.filter(type)
       if items.empty: break
       
       for item in items:
         result = invoke_subagent(type, item)
         verified = verify(result, type)
         if verified:
           commit_or_stage(result, type)
         else:
           escalate(item, result)
       
       if converged(type): break
       passes += 1
       re-discover queue (state may have changed)
   ```
7. **Commit** all staged changes with attribute-format messages
8. **Log** run summary to `docs/improvement-log.md`
9. **Cleanup** worktree

## Subagent Invocation

```bash
opencode agent improve-lint-fix --prompt '<json-input>'
opencode agent improve-skill-rewrite --prompt '<json-input>'
```

## Verification Gates

- `lint-fix`: lint gate only
- `skill-rewrite`: lint gate + eval gate (5% threshold for auto-commit)

## Loop Prevention

- Semantic hash (markdown AST) for idempotency
- Max 3 passes per type
- Convergence: <1% marginal improvement over 2 passes
- Human gate: skill-rewrite requires high confidence

## Output

Structured log entry appended to `docs/improvement-log.md` with:
- Timestamp, mode, run number
- Queue depth, processed, committed, escalated, skipped
- Metrics (lint violations before/after, eval scores)
- Escalated items requiring human review
