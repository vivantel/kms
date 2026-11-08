---
id: 0056-eval-gate-covers-study-base
title: Run the eval gate on pull requests into study/base as well as master
status: active
date: 2026-11-08
tags: [kms, eval-harness, automation]
track: process
---

## Decision

`.github/workflows/eval-skills.yml` triggers on pull requests into `study/base` as well as `master` (`branches: [master, study/base]`). `types: [opened]` is unchanged; a re-run after a push is the `/eval` comment, as `docs/decisions/0044-eval-harness-ci-safety-gates.md` already provides.

## Why

Pre-registration changes to the skills land on `study/base`, not `master`. With a `master`-only filter, those changes would merge with no eval gate, and the frozen version would be unmeasured against the `master` baseline.

## Tradeoffs considered

- **Add `synchronize` to `types`**: re-runs on every push, but `0044` requires `opened` only so that the free-tier eval budget is not spent per push. The `/eval` comment already covers re-runs.
- **Chosen: add the branch only**, leaving the frequency limit and fork guard of `0044` as they are.
