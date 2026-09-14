#!/usr/bin/env bash
# Materializes this repo's own real commit history (up to tag 0.15.0, 67 commits) from a
# checked-in git bundle, instead of the tiny 2-commit synthetic history evals/bootstrap/fixture
# uses. Unlike lint's docs/ tree (where INDEX.md is a cheap shortcut a model can read instead of
# every file — see docs/plans/scale-bootstrap-and-lint-chunked-checkpointing.md's lint-resume
# update), there is no equivalent shortcut for git-history mining: extracting decision stubs
# genuinely requires walking real commit messages/diffs, so a real, moderate-sized history should
# force genuine multi-page paging far more reliably than fixture size alone ever could for lint.
#
# The existing docs/{facts,decisions,guardrails,skills}/ tree is removed after checkout (as one
# final synthetic commit) so bootstrap faces a genuine from-scratch extraction against this real
# history, not a gap-fill pass against an already-complete knowledge base.
set -eu
git clone -q kms-history-0.15.0.bundle _clone
shopt -s dotglob
mv _clone/* .
rmdir _clone
rm -f kms-history-0.15.0.bundle
git checkout -q -b master tags/0.15.0
rm -rf docs/facts docs/decisions docs/guardrails docs/skills
git add -A
git -c user.email="eval-fixture@example.invalid" -c user.name="kms eval fixture" \
  commit -q -m "chore: reset knowledge base for eval fixture"
