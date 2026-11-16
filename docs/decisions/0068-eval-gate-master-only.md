---
id: 0068-eval-gate-master-only
title: Run the eval gate on pull requests into master only
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-12
tags: [kms, eval-harness, automation]
---

## Decision

`.github/workflows/eval-skills.yml` triggers on pull requests into `master` only (`branches: [master]`). `types: [opened]` and the `/eval` re-run comment of `docs/decisions/0044-eval-harness-ci-safety-gates.md` are unchanged. This supersedes `0056-eval-gate-covers-study-base`.

## Why

0056 existed because pre-registration changes landed on `study/base`. The study is merged and `study/base` is deleted, so the extra branch filter has no purpose.

## Tradeoffs considered

- **Keep both branches**: harmless but dead; would need a decision again if a new long-lived branch appears. Rejected.
