#!/usr/bin/env bash
# promptfoo `exec:` provider wrapper — runs one eval case's invocation prompt through
# Kilo Code CLI (`kilo run --auto`), against a fresh copy of the case's fixture project.
#
# Invoked by promptfoo as: kilo-runner.sh <rendered-prompt> <options-json> <context-json>
# (see https://www.promptfoo.dev/docs/providers/custom-script/). Per-case config (fixture_dir,
# model, timeout_seconds) travels in <options-json>, i.e. each case's `providers[].config` block.
#
# Prints, to stdout, the plain-text kilo transcript followed by a listing of every file present
# in the scratch project afterward — the shape promptfoo's `contains`/`regex`/`llm-rubric`/
# `javascript` assertions grade against. Never fails the promptfoo run itself on a kilo error;
# an error is folded into the graded output instead, so a broken case shows up as a failed
# assertion, not a harness crash.
#
# A fixture directory may include an executable `setup.sh`, run once inside the fresh scratch
# copy (cwd) before kilo starts — e.g. to build real git history (`bootstrap`) or stage an
# uncommitted diff (`attribute`). A tracked `.git/` can't live in a fixture directory directly
# (this repo would see it as a nested repo, not fixture content), so `setup.sh` is how a case
# gets git state at all.
#
# Runs through Kilo's own built-in gateway (`kilo/<vendor>/<model>:free`) — free, and requiring
# no account or API key at all (confirmed by testing: `hasToken=false`, still completes) — rather
# than a separately-configured OpenRouter provider. See the amendment on
# docs/decisions/0043-eval-harness-for-shipped-skill-changes.md.
#
# Repo context: docs/decisions/0043-eval-harness-for-shipped-skill-changes.md,
# docs/decisions/0044-eval-harness-ci-safety-gates.md.
set -u

PROMPT="${1:-}"
OPTIONS_JSON="${2:-}"
[ -z "$OPTIONS_JSON" ] && OPTIONS_JSON='{}'

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

json_get() {
  # json_get <json> <python-expr-on-d> <default>
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
TIMEOUT_SECONDS="$(json_get "$CONFIG_JSON" "d.get('timeout_seconds', 180)" '180')"

if [ -n "$FIXTURE_DIR" ]; then
  FIXTURE_DIR="$REPO_ROOT/$FIXTURE_DIR"
fi

SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/kms-eval-XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT

if [ -n "$FIXTURE_DIR" ] && [ -d "$FIXTURE_DIR" ]; then
  cp -a "$FIXTURE_DIR"/. "$SCRATCH"/
fi

cd "$SCRATCH" || exit 1

# Project-level `.kilo/skills/` is Kilo's highest-priority local skill source
# (docs/facts/0008-kilo-code-skills-spec.md) — copying this checkout's own skills/ there, rather
# than relying on this repo's published `skills.urls` (which always serves master), is what makes
# a before/after comparison of an uncommitted skill-body change possible at all. `shared/` and
# `templates/` are mirrored alongside it (not nested under `skills/`) because skill bodies
# reference them by relative path (e.g. `../../shared/artifact-model.md`, two levels up from a
# skill's own directory) — confirmed by testing: omitting this broke that Read for `capture`.
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

BEFORE_FILES="$(find . -type f -not -path './.git/*' | LC_ALL=C sort)"

TRANSCRIPT="$(timeout "${TIMEOUT_SECONDS}s" kilo run --auto -m "kilo/${MODEL}" "$PROMPT" 2>&1)"
KILO_EXIT=$?

AFTER_FILES="$(find . -type f -not -path './.git/*' | LC_ALL=C sort)"
CHANGED_FILES="$(LC_ALL=C comm -13 <(echo "$BEFORE_FILES") <(echo "$AFTER_FILES"))"
GIT_LOG="$(git log --format='%s' -n 5 2>/dev/null)"

echo "=== KILO TRANSCRIPT (exit ${KILO_EXIT}) ==="
echo "$TRANSCRIPT"
echo
echo "=== FILES CREATED/MODIFIED ==="
if [ -n "$CHANGED_FILES" ]; then
  echo "$CHANGED_FILES"
else
  echo "(none)"
fi
echo
echo "=== RECENT GIT LOG (subject lines) ==="
echo "$GIT_LOG"

exit 0
