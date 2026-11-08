---
id: pr-before-merge
title: Never push directly to main
status: active
date: '2026-10-01'
tags: [git]
governed-by: 0003-pr-before-merge
grounded-in: [0002-ci-runs-on-pr, 0003-pr-before-merge]
derivation-note: PR-only merges plus CI-on-PR imply CI gates every merge.
---
## Guardrail

Open a pull request; CI must pass before merge.

## Derivation

PRs are the only path to main (decision) and CI runs on them (fact).
