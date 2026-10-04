#!/usr/bin/env bash
# Improvement harness orchestrator — runs incremental automatic KMS improvement cycles.
# Modes: scheduled (full scan), event (targeted), manual (on demand).
# Uses inline Python fixes instead of spawning opencode agents.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CONFIG_FILE="${REPO_ROOT}/.opencode/improvement.yaml"
LINT_SCRIPT="${REPO_ROOT}/plugins/kms/hooks/lint_check.py"
PARSE_LINT_SCRIPT="${REPO_ROOT}/plugins/kms/hooks/parse_lint.py"
FIX_SCRIPT="${REPO_ROOT}/plugins/kms/hooks/inline_fix.py"

MODE="${1:-manual}"
CHANGED_FILES="${2:-}"

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
print(f'KILL_SWITCH={str(cfg.get("safety", {}).get("kill_switch", False)).lower()}')
print(f'MAX_FILES_PER_RUN={cfg.get("safety", {}).get("max_files_per_run", 50)}')
print(f'LOG_FILE={cfg.get("observability", {}).get("log_file", "docs/improvement-log.md")}')
print(f'BOT_NAME={cfg.get("observability", {}).get("commit_attribution", {}).get("name", "kms-improvement-bot")}')
print(f'BOT_EMAIL={cfg.get("observability", {}).get("commit_attribution", {}).get("email", "kms-improvement@vivantel.dev")}')
print(f'MAX_PASSES={cfg.get("loop_prevention", {}).get("max_passes_per_type", 3)}')
print(f'CONVERGENCE_THRESHOLD={cfg.get("loop_prevention", {}).get("convergence_threshold", 0.01)}')
print(f'LINT_GATE_ENABLED={str(cfg.get("verification", {}).get("lint_gate", {}).get("enabled", True)).lower()}')
print(f'LINT_GATE_REQUIRE_CLEAN={str(cfg.get("verification", {}).get("lint_gate", {}).get("require_clean", True)).lower()}')
print(f'EVAL_GATE_ENABLED={str(cfg.get("verification", {}).get("eval_gate", {}).get("enabled", True)).lower()}')
print(f'EVAL_GATE_MIN_IMPROVEMENT={cfg.get("verification", {}).get("eval_gate", {}).get("min_score_improvement", 0.05)}')
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

# Copy lint scripts and fix script
cp "$LINT_SCRIPT" "$WORKTREE_DIR/plugins/kms/hooks/lint_check.py"
cp "$PARSE_LINT_SCRIPT" "$WORKTREE_DIR/plugins/kms/hooks/parse_lint.py"
cp "$FIX_SCRIPT" "$WORKTREE_DIR/plugins/kms/hooks/inline_fix.py"

# Copy docs for lint/fix context - selective copy to avoid large worktrees
mkdir -p "$WORKTREE_DIR/docs/skills"
cp "$REPO_ROOT/docs/skills/tags.md" "$WORKTREE_DIR/docs/skills/" 2>/dev/null || true

# Copy artifact directories (facts, decisions, guardrails, skills) - only .md files, no archive
for type_dir in facts decisions guardrails skills; do
  mkdir -p "$WORKTREE_DIR/docs/$type_dir"
  # Copy all .md files (excluding archive subdirectory)
  find "$REPO_ROOT/docs/$type_dir" -maxdepth 1 -name "*.md" -exec cp {} "$WORKTREE_DIR/docs/$type_dir/" \; 2>/dev/null || true
  # Copy INDEX.md from archive if exists
  if [[ -f "$REPO_ROOT/docs/$type_dir/archive/INDEX.md" ]]; then
    mkdir -p "$WORKTREE_DIR/docs/$type_dir/archive"
    cp "$REPO_ROOT/docs/$type_dir/archive/INDEX.md" "$WORKTREE_DIR/docs/$type_dir/archive/"
  fi
done

# Copy plugins/kms for tags.md and translation_table.yaml
mkdir -p "$WORKTREE_DIR/plugins/kms/hooks"
cp "$REPO_ROOT/plugins/kms/hooks/translation_table.yaml" "$WORKTREE_DIR/plugins/kms/hooks/" 2>/dev/null || true
mkdir -p "$WORKTREE_DIR/plugins/kms/skills"
cp -a "$REPO_ROOT/plugins/kms/skills/." "$WORKTREE_DIR/plugins/kms/skills/"

for sibling in shared templates; do
  if [[ -d "$REPO_ROOT/plugins/kms/$sibling" ]]; then
    mkdir -p "$WORKTREE_DIR/plugins/kms/$sibling"
    cp -a "$REPO_ROOT/plugins/kms/$sibling/." "$WORKTREE_DIR/plugins/kms/$sibling/"
  fi
done

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
timeout 60 python3 plugins/kms/hooks/lint_check.py --scope all > /tmp/lint_test.json 2>/tmp/lint_test_stderr.log
LINT_EXIT=$?
set -e
echo "Lint exit code: $LINT_EXIT" >&2
cat /tmp/lint_test_stderr.log >&2
head -5 /tmp/lint_test.json
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
  echo "=== Phase 2: Lint Fix (inline Python) ==="
  
  # Use a temporary file to store items for proper iteration
  ITEMS_FILE="$WORKTREE_DIR/.items.json"
  jq -c '.items[]' "$QUEUE_FILE" > "$ITEMS_FILE"
  
  while IFS= read -r item; do
    [[ -z "$item" ]] && continue
    
    FILE=$(echo "$item" | jq -r '.file')
    VIOLATIONS=$(echo "$item" | jq -c '.violations')
    
    echo "Processing: $FILE"
    PROCESSED=$((PROCESSED + 1))
    
    # Run inline fix
    FIX_RESULT=$(python3 plugins/kms/hooks/inline_fix.py --repo-root "$WORKTREE_DIR" --file "$FILE" --violations "$VIOLATIONS" 2>&1)
    FIX_EXIT=$?
    
    if [[ $FIX_EXIT -ne 0 ]]; then
      echo "  Fix script failed with exit code $FIX_EXIT"
      echo "  Output: $FIX_RESULT"
      ESCALATED=$((ESCALATED + 1))
      ESCALATED_ITEMS+=("{\"file\": \"$FILE\", \"reason\": \"fix script failed\"}")
      continue
    fi
    
# Parse result
    FIXED=$(echo "$FIX_RESULT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(str(d.get('fixed', False)).lower())")

    if [[ "$FIXED" == "true" ]]; then
      CHANGES=$(echo "$FIX_RESULT" | python3 -c "import json, sys; d=json.load(sys.stdin); print(d.get('changes', ''))")
      echo "  Fixed: $CHANGES"
      
# Verify with lint gate (fast Python)
        if [[ "$LINT_GATE_ENABLED" == "true" ]]; then
          set +e
          python3 plugins/kms/hooks/lint_check.py --scope file --target "$FILE" > /tmp/lint_verify.json 2>/tmp/lint_verify_stderr.log
          LINT_EXIT=$?
          set -e
          cat /tmp/lint_verify_stderr.log >&2
          LINT_VERIFY=$(cat /tmp/lint_verify.json)
LINT_PASSED=$(echo "$LINT_VERIFY" | python3 -c "import json, sys; d=json.load(sys.stdin); print(str(d.get('summary', {}).get('total_violations', 1) == 0).lower())")

        if [[ "$LINT_PASSED" == "true" ]]; then
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
  set +e
  timeout 120 python3 plugins/kms/hooks/lint_check.py --scope all > /tmp/lint_after.json 2>/tmp/lint_after_stderr.log
  LINT_EXIT=$?
  set -e
  cat /tmp/lint_after_stderr.log >&2
  LINT_AFTER_OUTPUT=$(cat /tmp/lint_after.json)
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