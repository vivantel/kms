#!/usr/bin/env bash
# promptfoo grading provider — used as `provider: "exec:evals/providers/kilo-judge.sh"` on
# llm-rubric assertions. Unlike kilo-runner.sh (which runs a whole eval case against a fixture
# project), this answers one grading prompt promptfoo constructs internally (a rubric plus the
# candidate output) and returns the model's raw text response — no fixture, no scratch project,
# no skill injection.
#
# Runs through Kilo's own free gateway (`kilo/<vendor>/<model>:free`, no account or API key
# needed — confirmed by testing) on a *different* model than any case's runner, to avoid a model
# grading its own class of mistakes. See docs/decisions/0043-eval-harness-for-shipped-skill-changes.md.
set -u

PROMPT="${1:-}"
JUDGE_MODEL="${KMS_EVAL_JUDGE_MODEL:-nvidia/nemotron-3-ultra-550b-a55b:free}"
TIMEOUT_SECONDS="${KMS_EVAL_JUDGE_TIMEOUT_SECONDS:-90}"

# Run in an isolated, empty scratch directory so the judge model has no filesystem to explore
# and no reason to reach for a tool — a plain grading answer only.
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/kms-eval-judge-XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT
cd "$SCRATCH" || exit 1

RAW="$(timeout "${TIMEOUT_SECONDS}s" kilo run --auto -m "kilo/${JUDGE_MODEL}" "$PROMPT" 2>&1)"

# promptfoo's llm-rubric grader needs a response it can extract a {"pass":...} JSON object
# from. Kilo's own decorative banner ("> code · <model>") and ANSI color codes sometimes broke
# that extraction — confirmed the hard way (workflow run 34451326313: "Could not extract JSON
# from llm-rubric response"), even though a plain manual test of this same script worked fine.
# Strip ANSI escapes, then hand back only the last balanced {...} object found, so promptfoo
# sees just the JSON regardless of what Kilo prints around it. Falls back to the raw
# (de-ANSI'd) text if no valid JSON object is found, so a real extraction failure is still
# visible in the graded output rather than silently swallowed.
python3 -c "
import re, sys, json
text = sys.argv[1]
text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
best = None
depth = 0
start = None
for i, ch in enumerate(text):
    if ch == '{':
        if depth == 0:
            start = i
        depth += 1
    elif ch == '}':
        if depth > 0:
            depth -= 1
            if depth == 0 and start is not None:
                candidate = text[start:i+1]
                try:
                    json.loads(candidate)
                    best = candidate
                except Exception:
                    pass
print(best if best is not None else text)
" "$RAW"
exit 0
