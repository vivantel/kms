#!/usr/bin/env bash
# Materializes this repo's own real commit history (up to tag 0.15.0, 67 commits) from a
# checked-in git bundle, instead of the tiny 2-commit synthetic history evals/bootstrap/fixture
# uses. Unlike lint's docs/ tree (where INDEX.md is a cheap shortcut a model can read instead of
# every file — see docs/plans/scale-bootstrap-and-lint-chunked-checkpointing.md's lint-resume
# update), there is no equivalent shortcut for git-history mining: extracting decision stubs
# genuinely requires walking real commit messages/diffs, so a real, moderate-sized history should
# force genuine multi-page paging far more reliably than fixture size alone ever could for lint.
#
# The working tree is then reset to near-empty (everything except a placeholder README) — not just
# docs/{facts,decisions,guardrails,skills}/ — so bootstrap faces a genuine from-scratch extraction
# against real history, and so kilo-resume-runner.sh's own final file listing stays small. A first
# version of this fixture left the whole historical repo tree (plugins/, evals/, etc.) in place:
# hundreds of files in that listing made promptfoo's grading subprocess spawn fail outright
# ("Error: spawn E2BIG" — the OS's own argument-list-too-long limit, not a grading judgment at all)
# — workflow 34882535896.
set -eu
git clone -q kms-history-0.15.0.bundle _clone
shopt -s dotglob
mv _clone/* .
rmdir _clone
rm -f kms-history-0.15.0.bundle
git checkout -q -b master tags/0.15.0
git rm -rq -- .
echo "# eval fixture" > README.md
git add README.md
git -c user.email="eval-fixture@example.invalid" -c user.name="kms eval fixture" \
  commit -q -m "chore: reset working tree for eval fixture, keep git history for mining"
