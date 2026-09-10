#!/usr/bin/env bash
# Builds a base commit, then stages one clear, unambiguous change on top of it —
# the diff `attribute` is asked to write a commit message for.
set -eu
git init -q --initial-branch=main
git config user.email "eval-fixture@example.invalid"
git config user.name "kms eval fixture"
git add docs/decisions/0001-cap-retry-backoff.md
git commit -q -m "docs: record the retry-backoff decision"
git add src/client.py
git commit -q -m "feat: add retry-with-backoff client helper"

# The staged, uncommitted change: raise max_attempts from 3 to 5 to actually match
# decision 0001's "capped at 5 attempts" — the fixture's one clear, unambiguous change.
sed -i 's/max_attempts=3/max_attempts=5/' src/client.py
git add src/client.py
