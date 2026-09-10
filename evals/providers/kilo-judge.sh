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
TIMEOUT_SECONDS="${KMS_EVAL_JUDGE_TIMEOUT_SECONDS:-60}"

# Run in an isolated, empty scratch directory so the judge model has no filesystem to explore
# and no reason to reach for a tool — a plain grading answer only.
SCRATCH="$(mktemp -d "${TMPDIR:-/tmp}/kms-eval-judge-XXXXXX")"
trap 'rm -rf "$SCRATCH"' EXIT
cd "$SCRATCH" || exit 1

timeout "${TIMEOUT_SECONDS}s" kilo run --auto -m "kilo/${JUDGE_MODEL}" "$PROMPT" 2>&1
exit 0
