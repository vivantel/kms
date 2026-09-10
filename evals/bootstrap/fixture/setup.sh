#!/usr/bin/env bash
# Builds synthetic git history containing genuine decision language, so `bootstrap`
# has something real to extract decision stubs from.
set -eu
git init -q --initial-branch=main
git config user.email "eval-fixture@example.invalid"
git config user.name "kms eval fixture"
git add README.md
git commit -q -m "chore: initial scaffold"
git add src/config.py
git commit -q -m "feat: switch sync interval from 60s to 30s

Warehouse outage in March showed 60s left a window where stale inventory
reached checkout. Retries capped at 5 to avoid hammering the warehouse API
during an outage rather than backing off indefinitely."
