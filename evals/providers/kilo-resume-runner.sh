#!/usr/bin/env bash
# promptfoo `exec:` provider wrapper for a *resume* case: runs the same invocation prompt through
# Kilo Code CLI twice against the same scratch project — the first run under a deliberately short
# timeout (forcing a kill mid-chunk, per docs/plans/scale-bootstrap-and-lint-chunked-checkpointing.md
# step 4), the second run under a normal budget, against whatever state (including any checkpoint
# file under docs/.kms-checkpoints/) the first run left behind.
#
# Invoked by promptfoo as: kilo-resume-runner.sh <rendered-prompt> <options-json> <context-json>
# Config (travels in <options-json>'s config block): fixture_dir, model, first_timeout_seconds
# (short — expected to kill the first run mid-page), second_timeout_seconds (the case's normal
# budget, matching its non-resume sibling case's timeout_seconds).
#
# If the first run leaves no checkpoint behind (it completed cleanly inside its own short
# budget), the second invocation is skipped rather than burning its full timeout for no
# additional signal — a mis-tuned first_timeout_seconds should show up as a clearly-labeled skip,
# not a silently-meaningless pass.
#
# Prints both runs' transcripts (labeled), then a listing of every file present afterward and
# whether docs/.kms-checkpoints/ is empty — the shape this case's assertions grade against.
# Shares kilo-runner.sh's scratch-setup logic (fixture copy, .kilo/skills+shared+templates mirror,
# setup.sh); see that script's own comments for why each of those exists.
set -u

PROMPT="${1:-}"
OPTIONS_JSON="${2:-}"
[ -z "$OPTIONS_JSON" ] && OPTIONS_JSON='{}'

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

json_get() {
  python3 -c "
import json, sys
try:
    d = json.loads(sys.argv[1])
    print(eval(sys.argv[2]))
except Exception:
    print(sys.argv[3])
" "$1" "$2" "$3"
}

CONFIG_JSON="$(json_get "$OPTIONS_JSON" "json.dumps(d.get('config', {}))" '{}')"
FIXTURE_DIR="$(json_get "$CONFIG_JSON" "d.get('fixture_dir', '')" '')"
MODEL="$(json_get "$CONFIG_JSON" "d.get('model', 'poolside/laguna-s-2.1:free')" 'poolside/laguna-s-2.1:free')"
FIRST_TIMEOUT="$(json_get "$CONFIG_JSON" "d.get('first_timeout_seconds', 60)" '60')"
SECOND_TIMEOUT="$(json_get "$CONFIG_JSON" "d.get('second_timeout_seconds', 1440)" '1440')"

if [ -n "$FIXTURE_DIR" ]; then
  FIXTURE_DIR="$REPO_ROOT/$FIXTURE_DIR"
fi

SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/kms-eval-resume-XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT

if [ -n "$FIXTURE_DIR" ] && [ -d "$FIXTURE_DIR" ]; then
  cp -a "$FIXTURE_DIR"/. "$SCRATCH"/
fi

cd "$SCRATCH" || exit 1

mkdir -p .kilo/skills
cp -a "$REPO_ROOT/plugins/kms/skills/." .kilo/skills/
for sibling in shared templates; do
  if [ -d "$REPO_ROOT/plugins/kms/$sibling" ]; then
    mkdir -p ".kilo/$sibling"
    cp -a "$REPO_ROOT/plugins/kms/$sibling/." ".kilo/$sibling/"
  fi
done

export REPO_ROOT
if [ -x "./setup.sh" ]; then
  ./setup.sh
  rm -f ./setup.sh
fi

FIRST_TRANSCRIPT="$(timeout "${FIRST_TIMEOUT}s" kilo run --auto -m "kilo/${MODEL}" "$PROMPT" 2>&1)"
FIRST_EXIT=$?

CHECKPOINT_AFTER_FIRST="$(find docs/.kms-checkpoints -type f 2>/dev/null | LC_ALL=C sort)"

echo "=== FIRST RUN (exit ${FIRST_EXIT}, ${FIRST_TIMEOUT}s budget) ==="
echo "$FIRST_TRANSCRIPT"
echo
echo "=== CHECKPOINT FILES AFTER FIRST RUN ==="
if [ -n "$CHECKPOINT_AFTER_FIRST" ]; then echo "$CHECKPOINT_AFTER_FIRST"; else echo "(none)"; fi
echo

if [ -z "$CHECKPOINT_AFTER_FIRST" ]; then
  # Nothing to resume: the first run completed cleanly inside its own short budget, so there's
  # no interruption for the second invocation to demonstrate anything about. Skip it rather than
  # spending up to $SECOND_TIMEOUT seconds of CI time re-running the same prompt for no
  # additional signal — this also keeps a mis-tuned first_timeout_seconds from silently passing
  # for the wrong reason (see docs/plans/scale-bootstrap-and-lint-chunked-checkpointing.md step 4).
  echo "=== SECOND RUN SKIPPED: first run left no checkpoint to resume ==="
  echo
  echo "=== FINAL FILE LISTING ==="
  find . -type f -not -path './.git/*' | LC_ALL=C sort
  echo
  echo "=== CHECKPOINT FILES AFTER SECOND RUN ==="
  echo "(none — second run skipped)"
  exit 0
fi

SECOND_TRANSCRIPT="$(timeout "${SECOND_TIMEOUT}s" kilo run --auto -m "kilo/${MODEL}" "$PROMPT" 2>&1)"
SECOND_EXIT=$?

FINAL_FILES="$(find . -type f -not -path './.git/*' | LC_ALL=C sort)"
CHECKPOINT_AFTER_SECOND="$(find docs/.kms-checkpoints -type f 2>/dev/null | LC_ALL=C sort)"

echo "=== SECOND RUN (exit ${SECOND_EXIT}, ${SECOND_TIMEOUT}s budget, resuming) ==="
echo "$SECOND_TRANSCRIPT"
echo
echo "=== FINAL FILE LISTING ==="
echo "$FINAL_FILES"
echo
echo "=== CHECKPOINT FILES AFTER SECOND RUN ==="
if [ -n "$CHECKPOINT_AFTER_SECOND" ]; then echo "$CHECKPOINT_AFTER_SECOND"; else echo "(none)"; fi

exit 0
