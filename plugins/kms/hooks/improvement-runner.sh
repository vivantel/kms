#!/usr/bin/env bash
# Improvement harness orchestrator — runs incremental automatic KMS improvement cycles.
# Modes: scheduled (full scan), event (targeted), manual (on demand).
# See docs/plans/improvement-harness.md, docs/decisions/0056-0072.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
CONFIG_FILE="${REPO_ROOT}/.opencode/improvement.yaml"
HOOK_DIR="${REPO_ROOT}/plugins/kms/hooks"

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
print(f'MAX_FILES={cfg.get(\"safety\", {}).get(\"max_files_per_run\", 50)}')
print(f'LOG_FILE={cfg.get(\"observability\", {}).get(\"log_file\", \"docs/improvement-log.md\")}')
print(f'BOT_NAME={cfg.get(\"observability\", {}).get(\"commit_attribution\", {}).get(\"name\", \"kms-improvement-bot\")}')
print(f'BOT_EMAIL={cfg.get(\"observability\", {}).get(\"commit_attribution\", {}).get(\"email\", \"kms-improvement@vivantel.dev\")}')
print(f'MAX_PASSES={cfg.get(\"loop_prevention\", {}).get(\"max_passes_per_type\", 3)}')
print(f'CONVERGENCE_THRESHOLD={cfg.get(\"loop_prevention\", {}).get(\"convergence_threshold\", 0.01)}')
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

# Copy pinned skills to worktree
mkdir -p "$WORKTREE_DIR/.opencode/agent/improve"
cp -a "$REPO_ROOT/.opencode/agent/improve/." "$WORKTREE_DIR/.opencode/agent/improve/"

mkdir -p "$WORKTREE_DIR/.opencode"
cp "$CONFIG_FILE" "$WORKTREE_DIR/.opencode/improvement.yaml"
cp "$REPO_ROOT/.opencode/opencode.json" "$WORKTREE_DIR/.opencode/opencode.json"

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

# Build prompt for orchestrator subagent
# Handle trailing comma from tr '\n' ','
CHANGED_FILES_CLEAN="${CHANGED_FILES%,}"
CHANGED_JSON=$(printf '%s' "$CHANGED_FILES_CLEAN" | python3 -c "import sys, json; data = sys.stdin.read().strip(); print(json.dumps(data.split(',')) if data else '[]')")

PROMPT=$(cat <<EOF
{
  "mode": "$MODE",
  "changed_files": $CHANGED_JSON,
  "config": ".opencode/improvement.yaml",
  "repo_root": "$WORKTREE_DIR",
  "queue_file": ".improvement-queue.json",
  "baseline_sha": "$BASELINE_SHA",
  "max_passes": $MAX_PASSES,
  "convergence_threshold": $CONVERGENCE_THRESHOLD,
  "dry_run": ${DRY_RUN:-false}
}
EOF
)

echo "Running improvement harness..."
run_with_retry improve-harness "$PROMPT"

# If not dry run and there are commits, push back to main worktree
if [[ "${DRY_RUN:-false}" != "true" ]]; then
  # Collect commits made in worktree
  COMMITS=$(git -C "$WORKTREE_DIR" log --oneline "$BASELINE_SHA"..HEAD 2>/dev/null | wc -l | tr -d ' ')
  if [[ "$COMMITS" -gt 0 ]]; then
    echo "Applying $COMMITS commit(s) to main worktree..."
    BRANCH="improvement-harness-$(date +%s)"
    git -C "$REPO_ROOT" fetch "$WORKTREE_DIR" main:"$BRANCH" 2>/dev/null || true
    git -C "$REPO_ROOT" merge --ff-only "$BRANCH" 2>/dev/null || {
      echo "Fast-forward failed; manual review needed"
      exit 1
    }
  fi
fi

echo "Done"
