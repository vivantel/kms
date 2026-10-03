---
name: improve-harness
description: Main improvement harness orchestrator - runs convergence loop across all improvement types
tools:
  read: true
  write: true
  edit: true
  grep: true
  glob: true
  bash: true
model: opencode/nemotron-3-ultra-free
---

# Improvement Harness Orchestrator

Main entry point for the improvement harness. Invoked by `improvement-runner.sh` or manually via `opencode run --agent improve-harness`.

## Input (via prompt)

```json
{
  "mode": "scheduled|event|manual",
  "changed_files": [],
  "config": ".opencode/improvement.yaml",
  "repo_root": "/abs/path/to/repo",
  "queue_file": ".improvement-queue.json",
  "baseline_sha": "abc123",
  "max_passes": 3,
  "convergence_threshold": 0.01,
  "dry_run": false
}
```

## Workflow

Execute the following steps in order. Use your tools (read, write, edit, grep, glob, bash) for all operations.

### Step 1: Parse Config

Read the config file using the `read` tool, then extract settings with a bash command.

### Step 2: Initialize Queue

Queue file already created by runner at the path in `queue_file`. Confirm it exists with `read`.

### Step 3: Discover Queue Items

Run discovery for each enabled signal using your tools:

#### 3a. Lint Discovery (lint-fix items)

Run the lint skill to get violations:
- Use `bash` tool to run: `opencode run --agent lint "lint the knowledge base and output violations as JSON" --print-logs --format json`

Parse the lint output and convert each violation to a queue item. Add items to queue file using `edit` or `bash` with `jq`/`python`.

Queue item format:
```json
{
  "type": "lint-fix",
  "file": "path/to/file.md",
  "violation": {
    "type": "token-economy|structure|xref|format|derivation|tags",
    "message": "description",
    "line": 42,
    "suggestion": "fix hint"
  },
  "priority": 10,
  "source": "lint"
}
```

#### 3b. Eval Discovery (skill-rewrite items)

For each skill in `plugins/kms/skills/` that has an eval case:
- Use `glob` to find skills with eval directories
- Use `bash` to run promptfoo eval for each
- Parse results and create queue items for skills with pass rate < 1.0 or score below baseline

### Step 4: Prioritize Queue

Sort queue items by: severity, impact, confidence, age. Use `bash` with `jq` or `python` to sort and update queue file.

### Step 5: Convergence Loop

For each improvement type in priority order [lint-fix, skill-rewrite]:

```bash
passes=0
while [[ $passes -lt $max_passes ]]; do
  # Filter queue for this type using jq
  # For each item, invoke appropriate subagent
  # Verify result
  # If verified, commit or stage
  # If not, escalate
  # Check convergence
  # Re-discover queue
  passes=$((passes + 1))
done
```

Use `bash` tool for the loop, `read`/`write` for queue operations, `bash` for subagent invocation.

### Step 6: Commit Changes

For verified fixes, create commits with attribute-format messages using `bash`:
```bash
git add <files>
git commit -m "fix: <why>" -m "Refs: docs/facts/..."
```

### Step 7: Log Run Summary

Append structured entry to `docs/improvement-log.md` using `edit` or `write`:

```markdown
---
date: 2026-01-15T10:30:00Z
mode: scheduled
run_number: 42
queue_depth: 15
processed: 12
committed: 10
escalated: 2
skipped: 1
lint_violations_before: 25
lint_violations_after: 5
eval_scores:
  bootstrap: {before: 0.72, after: 0.89}
escalated_items:
  - file: plugins/kms/skills/roadmap/SKILL.md
    reason: eval regression
---
```

## Subagent Invocation

Use `bash` tool to invoke subagents:

```bash
# lint-fix
opencode run --agent improve-lint-fix --prompt '<json>' --print-logs --format json

# skill-rewrite
opencode run --agent improve-skill-rewrite --prompt '<json>' --print-logs --format json
```

## Verification Gates

- `lint-fix`: lint gate only (run lint on fixed files)
- `skill-rewrite`: lint gate + eval gate (5% score improvement threshold for auto-commit)

## Loop Prevention

- Semantic hash (markdown AST) for idempotency
- Max 3 passes per type (configurable)
- Convergence: <1% marginal improvement over 2 passes
- Human gate: skill-rewrite requires high confidence

## Output

Structured log entry appended to `docs/improvement-log.md` with:
- Timestamp, mode, run number
- Queue depth, processed, committed, escalated, skipped
- Metrics (lint violations before/after, eval scores)
- Escalated items requiring human review
