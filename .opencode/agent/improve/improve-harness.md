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
# Fallback models (used if primary returns 503) — must stay on free tiers (0015, improvement-harness-free-models-only):
# model: openrouter/~meta-llama/llama-3-70b:free
# model: openrouter/~google/gemini-flash:free
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

```bash
python3 -c "
import yaml, json, sys, os
with open('${config}') as f:
    cfg = yaml.safe_load(f)
verification = cfg.get('verification', {})
safety = cfg.get('safety', {})
print(f'LINT_GATE_ENABLED={verification.get(\"lint_gate\", {}).get(\"enabled\", True)}')
print(f'LINT_GATE_REQUIRE_CLEAN={verification.get(\"lint_gate\", {}).get(\"require_clean\", True)}')
print(f'EVAL_GATE_ENABLED={verification.get(\"eval_gate\", {}).get(\"enabled\", True)}')
print(f'EVAL_GATE_MIN_IMPROVEMENT={verification.get(\"eval_gate\", {}).get(\"min_score_improvement\", 0.05)}')
print(f'MAX_PASSES={cfg.get(\"loop_prevention\", {}).get(\"max_passes_per_type\", 3)}')
print(f'CONVERGENCE_THRESHOLD={cfg.get(\"loop_prevention\", {}).get(\"convergence_threshold\", 0.01)}')
print(f'MAX_FILES_PER_RUN={safety.get(\"max_files_per_run\", 10)}')
print(f'DRY_RUN={os.environ.get(\"DRY_RUN\", \"false\").lower()}')
"
```

### Step 2: Initialize Queue

Queue file already created by runner at the path in `queue_file`. Confirm it exists with `read`.

### Step 3: Discover Queue Items (Limited)

Run discovery for each enabled signal, but limit total items to `MAX_FILES_PER_RUN`.

#### 3a. Lint Discovery (lint-fix items)

Run the lint agent to get violations:
- Use `bash` tool to run: `opencode run --agent lint '{"scope": "all"}' --print-logs`

Parse the lint output and convert violations to queue items, grouped by file (batch all violations in a file together). Limit to `MAX_FILES_PER_RUN` files.

Queue item format (per file, not per violation):
```json
{
  "type": "lint-fix",
  "file": "path/to/file.md",
  "violations": [
    {"type": "token-economy|structure|xref|format|derivation|tags", "message": "desc", "line": 42, "suggestion": "hint"}
  ],
  "priority": 10,
  "source": "lint"
}
```

#### 3b. Eval Discovery (skill-rewrite items)

For each skill in `plugins/kms/skills/` that has an eval case:
- Use `glob` to find skills with eval directories
- Use `bash` to run promptfoo eval for each
- Parse results and create queue items for skills with pass rate < 1.0 or score below baseline
- Limit to `MAX_FILES_PER_RUN` skills

### Step 4: Prioritize Queue

Sort queue items by: severity, impact, confidence, age. Use `bash` with `jq` or `python` to sort and update queue file.

### Step 5: Convergence Loop (Batched Processing)

For each improvement type in priority order [lint-fix, skill-rewrite]:

```bash
passes=0
prev_hash=""
prev_metrics=""
MAX_ITEMS_PER_PASS=5  # Process max 5 items per pass

while [[ $passes -lt $max_passes ]]; do
  # Filter queue for this type using jq, limit to MAX_ITEMS_PER_PASS
  items=$(jq -c '.items[] | select(.type=="lint-fix")' "$queue_file" | head -$MAX_ITEMS_PER_PASS)
  
  if [[ -z "$items" ]]; then
    break
  fi
  
  committed_this_pass=0
  for item in $items; do
    # Invoke appropriate subagent ONCE PER FILE (not per violation)
    if [[ "$item_type" == "lint-fix" ]]; then
      result=$(opencode run --agent improve-lint-fix --prompt "$item" --print-logs --format json)
    elif [[ "$item_type" == "skill-rewrite" ]]; then
      result=$(opencode run --agent improve-skill-rewrite --prompt "$item" --print-logs --format json)
    fi
    
    # THREE-LAYER VERIFICATION
    verified=false
    
    # Layer 1: Lint Gate (all types)
    if [[ "$LINT_GATE_ENABLED" == "True" ]]; then
      if [[ "$item_type" == "lint-fix" ]]; then
        file=$(echo "$item" | jq -r '.file')
        lint_result=$(cd "${repo_root}" && opencode run --agent lint "{\"scope\": \"file\", \"target\": \"$file\"}" --print-logs 2>&1)
      else
        skill_dir=$(echo "$item" | jq -r '.skill_dir')
        lint_result=$(cd "${repo_root}" && opencode run --agent lint "{\"scope\": \"file\", \"target\": \"${skill_dir}/SKILL.md\"}" --print-logs 2>&1)
        lint_result2=$(cd "${repo_root}" && opencode run --agent lint "{\"scope\": \"file\", \"target\": \"${skill_dir}/examples.md\"}" --print-logs 2>&1)
      fi
      if echo "$lint_result" | jq -e '.violations | length == 0' >/dev/null; then
        lint_passed=true
      else
        lint_passed=false
      fi
    else
      lint_passed=true
    fi
    
    # Layer 2: Eval Gate (skill-rewrite only)
    if [[ "$item_type" == "skill-rewrite" && "$EVAL_GATE_ENABLED" == "True" ]]; then
      skill_dir=$(echo "$item" | jq -r '.skill_dir')
      skill_name=$(basename "$skill_dir")
      eval_result=$(cd "${repo_root}" && promptfoo eval -c "evals/${skill_name}/promptfooconfig.yaml" -o json 2>&1)
      eval_pass_rate=$(echo "$eval_result" | jq -r '.pass_rate // 0')
      eval_score=$(echo "$eval_result" | jq -r '.score // 0')
      baseline_pass_rate=$(echo "$item" | jq -r '.eval_details.pass_rate // 0')
      baseline_score=$(echo "$item" | jq -r '.eval_details.score // 0')
      
      if [[ $(echo "$eval_pass_rate >= $baseline_pass_rate" | bc -l) -eq 1 ]] && \
         [[ $(echo "$eval_score - $baseline_score >= $EVAL_GATE_MIN_IMPROVEMENT" | bc -l) -eq 1 ]]; then
        eval_passed=true
      else
        eval_passed=false
      fi
    else
      eval_passed=true
    fi
    
    # Layer 3: Sampling Gate (deferred to v0.2, placeholder)
    sampling_passed=true
    
    # Combined verification
    if [[ "$lint_passed" == "true" && "$eval_passed" == "true" && "$sampling_passed" == "true" ]]; then
      verified=true
    fi
    
    if [[ "$verified" == "true" ]]; then
      # Commit or stage
      if [[ "$dry_run" == "false" ]]; then
        # Use attribute-format commit with Refs trailers
        file=$(echo "$item" | jq -r '.file')
        git add "$file"
        git commit -m "fix: auto-fix lint violations in $(basename "$file")" -m "Refs: $file"
      fi
      committed_this_pass=$((committed_this_pass + 1))
      
      # Remove from queue
      jq "del(.items[] | select(.file==\"$file\"))" "$queue_file" > "$queue_file.tmp" && mv "$queue_file.tmp" "$queue_file"
    else
      # Escalate: add to escalated list in queue metadata
      # Log reason for escalation
      echo "Escalated: $(echo "$item" | jq -r '.file') - verification failed"
    fi
  done
  
  # Check convergence
  current_hash=$(git -C "${repo_root}" diff --name-only HEAD~${committed_this_pass} HEAD 2>/dev/null | sort | sha256sum | cut -d' ' -f1)
  current_metrics="commits=$committed_this_pass"
  
  if [[ $passes -gt 0 ]]; then
    if [[ "$current_hash" == "$prev_hash" ]]; then
      break
    fi
  fi
  
  prev_hash="$current_hash"
  prev_metrics="$current_metrics"
  passes=$((passes + 1))
  
  # Re-discover queue (state may have changed) - but limit to avoid infinite loop
  if [[ $passes -lt $max_passes ]]; then
    # Re-run lint discovery for remaining items
    break  # For MVP, only one pass per run
  fi
done
```

Use `bash` tool for the loop, `read`/`write` for queue operations, `bash` for subagent invocation.

### Step 6: Log Run Summary

Append structured entry to `docs/improvement-log.md` using `edit` or `write`:

```markdown
---
date: 2026-01-15T10:30:00Z
mode: scheduled
run_number: 42
baseline_ref: "0.15.0"
baseline_sha: "abc123"
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
# lint-fix (per file, not per violation)
opencode run --agent improve-lint-fix --prompt '<json>' --print-logs --format json

# skill-rewrite
opencode run --agent improve-skill-rewrite --prompt '<json>' --print-logs --format json
```

## Verification Gates (Three-Layer)

1. **Lint Gate** (all types): Run lint on fixed files, require clean (no violations)
2. **Eval Gate** (skill-rewrite): Require pass_rate >= baseline AND score improvement >= 5%
3. **Sampling Gate** (v0.2+): Random sample of changes for human review

## Loop Prevention

- Max 3 passes per type (configurable)
- Max 10 files per run (configurable)
- Max 5 items per pass
- Convergence: no new changes detected
- Human gate: skill-rewrite requires high confidence

## Output

Structured log entry appended to `docs/improvement-log.md` with:
- Timestamp, mode, run number, baseline
- Queue depth, processed, committed, escalated, skipped
- Metrics (lint violations before/after, eval scores)
- Escalated items requiring human review