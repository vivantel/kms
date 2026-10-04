#!/usr/bin/env bash
# Improvement harness orchestrator — runs incremental automatic KMS improvement cycles.
# Modes: scheduled (full scan), event (targeted), manual (on demand).
# See docs/plans/improvement-harness.md, docs/decisions/0056-0072.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CONFIG_FILE="${REPO_ROOT}/.opencode/improvement.yaml"
LINT_SCRIPT="${REPO_ROOT}/plugins/kms/hooks/lint_check.py"
PARSE_LINT_SCRIPT="${REPO_ROOT}/plugins/kms/hooks/parse_lint.py"

MODE="${1:-manual}"
CHANGED_FILES="${2:-}"

# Retry configuration for 503 errors
MAX_RETRIES=3
BASE_DELAY=2  # seconds

# Fallback model (set via env or use default)
FALLBACK_MODEL="${FALLBACK_MODEL:-openrouter/~anthropic/claude-haiku-latest}"

# Run opencode with retry on 503 (model unavailable), with fallback model
run_with_retry() {
  local agent="$1"
  local prompt="$2"
  local attempt=1
  local delay=$BASE_DELAY
  local model_override=""

  while [[ $attempt -le $MAX_RETRIES ]]; do
    echo "Attempt $attempt/$MAX_RETRIES: opencode run --agent $agent ${model_override:+--model $model_override} ..."
    # Use timeout to prevent indefinite hangs (5 minutes max per attempt)
    if timeout 300 opencode run --agent "$agent" ${model_override:+--model "$model_override"} "$prompt" --print-logs 2>&1; then
      return 0
    fi

    local exit_code=$?
    # Check if it was a timeout (124) or other error
    if [[ $exit_code -eq 124 ]]; then
      echo "Attempt $attempt timed out after 300s."
    else
      echo "Attempt $attempt failed (exit code: $exit_code)."
    fi

    if [[ $attempt -lt $MAX_RETRIES ]]; then
      echo "Retrying in ${delay}s..."
      sleep $delay
      delay=$((delay * 2))  # Exponential backoff
      attempt=$((attempt + 1))
      # On last retry before fallback, switch to fallback model
      if [[ $attempt -eq $MAX_RETRIES && -n "$FALLBACK_MODEL" ]]; then
        echo "Switching to fallback model: $FALLBACK_MODEL"
        model_override="$FALLBACK_MODEL"
      fi
    else
      echo "All $MAX_RETRIES attempts failed."
      return $exit_code
    fi
  done
}

usage() {
  cat <<EOF
Usage: $0 [scheduled|event|manual] [--changed-files="file1,file2"]

Modes:
  scheduled  - Full repo scan (daily cron)
  event      - Targeted scan on changed files (CI push/PR)
  manual     - On-demand run (default)

Environment:
  BASELINE_REF  - Override baseline_ref from config (tag/commit/SHA)
  DRY_RUN       - If "true", don't commit, just log what would happen
EOF
  exit 1
}

[[ "$MODE" =~ ^(scheduled|event|manual)$ ]] || usage

# Parse config (requires yq or python)
parse_config() {
  python3 -c "
import yaml, sys, os
with open('$CONFIG_FILE') as f:
    cfg = yaml.safe_load(f)
# Print key values as shell exports
print(f'BASELINE_REF={os.environ.get(\"BASELINE_REF\", cfg.get(\"baseline_ref\", \"latest-tag\"))}')
print(f'KILL_SWITCH={cfg.get(\"safety\", {}).get(\"kill_switch\", False)}')
print(f'MAX_FILES_PER_RUN={cfg.get(\"safety\", {}).get(\"max_files_per_run\", 10)}')
print(f'LOG_FILE={cfg.get(\"observability\", {}).get(\"log_file\", \"docs/improvement-log.md\")}')
print(f'BOT_NAME={cfg.get(\"observability\", {}).get(\"commit_attribution\", {}).get(\"name\", \"kms-improvement-bot\")}')
print(f'BOT_EMAIL={cfg.get(\"observability\", {}).get(\"commit_attribution\", {}).get(\"email\", \"kms-improvement@vivantel.dev\")}')
print(f'MAX_PASSES={cfg.get(\"loop_prevention\", {}).get(\"max_passes_per_type\", 3)}')
print(f'CONVERGENCE_THRESHOLD={cfg.get(\"loop_prevention\", {}).get(\"convergence_threshold\", 0.01)}')
print(f'LINT_GATE_ENABLED={cfg.get(\"verification\", {}).get(\"lint_gate\", {}).get(\"enabled\", True)}')
print(f'LINT_GATE_REQUIRE_CLEAN={cfg.get(\"verification\", {}).get(\"lint_gate\", {}).get(\"require_clean\", True)}')
print(f'EVAL_GATE_ENABLED={cfg.get(\"verification\", {}).get(\"eval_gate\", {}).get(\"enabled\", True)}')
print(f'EVAL_GATE_MIN_IMPROVEMENT={cfg.get(\"verification\", {}).get(\"eval_gate\", {}).get(\"min_score_improvement\", 0.05)}')
"
}

eval "$(parse_config)"

if [[ "$KILL_SWITCH" == "true" ]]; then
  echo "Kill switch enabled — exiting"
  exit 0
fi

# Resolve baseline_ref to a commit SHA
resolve_baseline() {
  local ref="$1"
  if [[ "$ref" == "latest-tag" ]]; then
    git -C "$REPO_ROOT" describe --tags --abbrev=0 2>/dev/null || echo "HEAD"
  else
    git -C "$REPO_ROOT" rev-parse "$ref" 2>/dev/null || echo "HEAD"
  fi
}

BASELINE_SHA="$(resolve_baseline "$BASELINE_REF")"
echo "Baseline: $BASELINE_SHA"

# Create worktree
WORKTREE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/kms-improve-XXXXXX")"
trap 'rm -rf "$WORKTREE_DIR"' EXIT
trap 'rm -rf "$WORKTREE_DIR"; exit 1' INT TERM

git -C "$REPO_ROOT" worktree add "$WORKTREE_DIR" "$BASELINE_SHA" >/dev/null
echo "Worktree: $WORKTREE_DIR"

# Copy agents for fixing phase
mkdir -p "$WORKTREE_DIR/.opencode/agent"
cp -a "$REPO_ROOT/.opencode/agent/." "$WORKTREE_DIR/.opencode/agent/"

mkdir -p "$WORKTREE_DIR/.opencode"
cp "$CONFIG_FILE" "$WORKTREE_DIR/.opencode/improvement.yaml"
cp "$REPO_ROOT/.opencode/opencode.json" "$WORKTREE_DIR/.opencode/opencode.json"

# Copy lint scripts
cp "$LINT_SCRIPT" "$WORKTREE_DIR/plugins/kms/hooks/lint_check.py"
cp "$PARSE_LINT_SCRIPT" "$WORKTREE_DIR/plugins/kms/hooks/parse_lint.py"

# Copy shipped skills and shared for context
mkdir -p "$WORKTREE_DIR/plugins/kms/skills"
cp -a "$REPO_ROOT/plugins/kms/skills/." "$WORKTREE_DIR/plugins/kms/skills/"

for sibling in shared templates; do
  if [[ -d "$REPO_ROOT/plugins/kms/$sibling" ]]; then
    mkdir -p "$WORKTREE_DIR/plugins/kms/$sibling"
    cp -a "$REPO_ROOT/plugins/kms/$sibling/." "$WORKTREE_DIR/plugins/kms/$sibling/"
  fi
done

# Copy docs for lint/capture context
mkdir -p "$WORKTREE_DIR/docs"
cp -a "$REPO_ROOT/docs/." "$WORKTREE_DIR/docs/"

cd "$WORKTREE_DIR"

# Initialize queue file
QUEUE_FILE="$WORKTREE_DIR/.improvement-queue.json"
echo '{"items":[],"metadata":{"created":"'$(date -Iseconds)'","mode":"'$MODE'","baseline":"'$BASELINE_SHA'"}}' > "$QUEUE_FILE"

RUN_DATE=$(date -Iseconds)
RUN_NUMBER=$(date +%s)
LINT_VIOLATIONS_BEFORE=0
LINT_VIOLATIONS_AFTER=0
PROCESSED=0
COMMITTED=0
ESCALATED=0
SKIPPED=0
ESCALATED_ITEMS=()

# ============ LINT-FIX PHASE ============
echo "=== Phase 1: Lint Discovery (fast Python) ==="
LINT_OUTPUT_FILE="$WORKTREE_DIR/lint_output.json"
echo "Running lint script from $(pwd)..."
echo "Lint script: $(ls -la plugins/kms/hooks/lint_check.py)"
echo "Docs dir: $(ls -d docs/ 2>/dev/null || echo 'NOT FOUND')"
echo "Python version: $(python3 --version)"

# Disable exit on error for timeout command (timeout returns 124 on timeout, 1 if command fails)
set +e
timeout 60 python3 plugins/kms/hooks/lint_check.py --scope all > /tmp/lint_test.json 2>&1
LINT_EXIT=$?
set -e
echo "Lint exit code: $LINT_EXIT" >&2
cat /tmp/lint_test.json | head -5
cp /tmp/lint_test.json "$LINT_OUTPUT_FILE"
echo "Lint completed with exit code $LINT_EXIT, output size: $(wc -c < "$LINT_OUTPUT_FILE")" >&2

# Parse violations and group by file using external script
echo "Running lint discovery Python..."
LINT_DISCOVERY_OUT=$(QUEUE_FILE="$QUEUE_FILE" LINT_OUTPUT_FILE="$LINT_OUTPUT_FILE" MAX_FILES_PER_RUN="$MAX_FILES_PER_RUN" python3 "$WORKTREE_DIR/plugins/kms/hooks/parse_lint.py")
echo "Lint discovery output: $LINT_DISCOVERY_OUT"

eval "$LINT_DISCOVERY_OUT"

echo "Queue depth: $QUEUE_DEPTH"
echo "Lint violations before: $LINT_VIOLATIONS_BEFORE"

if [[ "$QUEUE_DEPTH" -eq 0 ]]; then
  echo "No lint violations to fix"
else
  echo "=== Phase 2: Lint Fix (via opencode agent) ==="
  
  # Use a temporary file to store items for proper iteration
  ITEMS_FILE="$WORKTREE_DIR/.items.json"
  jq -c '.items[]' "$QUEUE_FILE" > "$ITEMS_FILE"
  
  while IFS= read -r item; do
    [[ -z "$item" ]] && continue
    
    FILE=$(echo "$item" | jq -r '.file')
    VIOLATIONS=$(echo "$item" | jq -c '.violations')
    
    echo "Processing: $FILE"
    PROCESSED=$((PROCESSED + 1))
    
    # Create prompt for improve-lint-fix
    PROMPT=$(jq -n \
      --arg file "$FILE" \
      --argjson violations "$VIOLATIONS" \
      --arg repo_root "$WORKTREE_DIR" \
      '{file: $file, violations: $violations, context: {repo_root: $repo_root, tags_list: "docs/skills/tags.md"}}')
    
    # Run improve-lint-fix
    FIX_RESULT=$(run_with_retry improve-lint-fix "$PROMPT" 2>&1 | tail -1)
    
    # Parse result
    FIXED=$(echo "$FIX_RESULT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('fixed', False))")
    
    if [[ "$FIXED" == "True" ]]; then
      echo "  Fixed: $(echo "$FIX_RESULT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('changes', ''))")"
      
      # Verify with lint gate (fast Python)
      if [[ "$LINT_GATE_ENABLED" == "True" ]]; then
        LINT_VERIFY=$(cd "$WORKTREE_DIR" && python3 plugins/kms/hooks/lint_check.py --scope file --target "$FILE" 2>/dev/null)
        LINT_PASSED=$(echo "$LINT_VERIFY" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('summary', {}).get('total_violations', 1) == 0)")
        
        if [[ "$LINT_PASSED" == "True" ]]; then
          echo "  Lint gate passed"
          
          if [[ "${DRY_RUN:-false}" != "true" ]]; then
            git -C "$WORKTREE_DIR" add "$FILE"
            git -C "$WORKTREE_DIR" -c user.name="$BOT_NAME" -c user.email="$BOT_EMAIL" commit -m "fix: auto-fix lint violations in $(basename "$FILE")" -m "Refs: $FILE"
            COMMITTED=$((COMMITTED + 1))
            echo "  Committed"
          fi
        else
          echo "  Lint gate failed - escalating"
          ESCALATED=$((ESCALATED + 1))
          ESCALATED_ITEMS+=("{\"file\": \"$FILE\", \"reason\": \"lint gate failed after fix\"}")
        fi
      else
        if [[ "${DRY_RUN:-false}" != "true" ]]; then
          git -C "$WORKTREE_DIR" add "$FILE"
          git -C "$WORKTREE_DIR" -c user.name="$BOT_NAME" -c user.email="$BOT_EMAIL" commit -m "fix: auto-fix lint violations in $(basename "$FILE")" -m "Refs: $FILE"
          COMMITTED=$((COMMITTED + 1))
          echo "  Committed (lint gate disabled)"
        fi
      fi
    else
      REASON=$(echo "$FIX_RESULT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('reason', 'unknown'))")
      echo "  Fix failed: $REASON"
      ESCALATED=$((ESCALATED + 1))
      ESCALATED_ITEMS+=("{\"file\": \"$FILE\", \"reason\": \"$REASON\"}")
    fi
  done < "$ITEMS_FILE"
fi

# ============ SKILL-REWRITE PHASE (placeholder for MVP) ============
echo "=== Phase 3: Skill Rewrite Discovery ==="
SKILL_REWRITE_COUNT=0

# ============ LOG RUN SUMMARY ============
echo "=== Phase 4: Logging ==="

# Count lint violations after (fast Python)
if [[ "$LINT_VIOLATIONS_BEFORE" -gt 0 ]]; then
  LINT_AFTER_OUTPUT=$(cd "$WORKTREE_DIR" && python3 plugins/kms/hooks/lint_check.py --scope all 2>/dev/null)
  LINT_VIOLATIONS_AFTER=$(echo "$LINT_AFTER_OUTPUT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('summary', {}).get('total_violations', 0))")
else
  LINT_VIOLATIONS_AFTER=0
fi

# Build escalated items JSON
ESCALATED_JSON="[]"
if [[ ${#ESCALATED_ITEMS[@]} -gt 0 ]]; then
  ESCALATED_JSON=$(printf '%s\n' "${ESCALATED_ITEMS[@]}" | jq -s .)
fi

# Append to improvement log
LOG_ENTRY=$(cat <<EOF

---
date: $RUN_DATE
mode: $MODE
run_number: $RUN_NUMBER
baseline_ref: "$BASELINE_REF"
baseline_sha: "$BASELINE_SHA"
queue_depth: $QUEUE_DEPTH
processed: $PROCESSED
committed: $COMMITTED
escalated: $ESCALATED
skipped: $SKIPPED
lint_violations_before: $LINT_VIOLATIONS_BEFORE
lint_violations_after: $LINT_VIOLATIONS_AFTER
eval_scores: {}
escalated_items: $ESCALATED_JSON
---

Automated run via $MODE mode. $COMMITTED commit(s) applied, $ESCALATED escalated.

EOF
)

if [[ "${DRY_RUN:-false}" != "true" ]]; then
  WORKTREE_COMMITS=$(git -C "$WORKTREE_DIR" log --oneline "$BASELINE_SHA"..HEAD 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$WORKTREE_COMMITS" -gt 0 ]]; then
    echo "Applying $WORKTREE_COMMITS commit(s) to main worktree..."
    BRANCH="improvement-harness-$(date +%s)"
    git -C "$REPO_ROOT" fetch "$WORKTREE_DIR" main:"$BRANCH" 2>/dev/null || true
    git -C "$REPO_ROOT" merge --ff-only "$BRANCH" 2>/dev/null || {
      echo "Fast-forward failed; manual review needed"
      exit 1
    }
    
    echo "$LOG_ENTRY" >> "$REPO_ROOT/docs/improvement-log.md"
    git -C "$REPO_ROOT" -c user.name="$BOT_NAME" -c user.email="$BOT_EMAIL" add docs/improvement-log.md
    git -C "$REPO_ROOT" -c user.name="$BOT_NAME" -c user.email="$BOT_EMAIL" commit -m "docs: update improvement log for run $RUN_NUMBER" -m "Refs: docs/improvement-log.md"
  fi
else
  echo "DRY RUN - would have logged:"
  echo "$LOG_ENTRY"
fi

echo "Done"
echo "Summary: processed=$PROCESSED, committed=$COMMITTED, escalated=$ESCALATED, skipped=$SKIPPED"