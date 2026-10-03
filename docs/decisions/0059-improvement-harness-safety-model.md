---
id: 0059-improvement-harness-safety-model
title: Improvement harness applies fixes via fully automatic commits
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "safety", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall commit fixes directly to the working branch without human review (fully automatic). Safety is achieved through layered loop prevention (`0061`) and verification gates (`0068`), not through a PR gate.

- Each improvement skill, after verifying its fix, stages changes and commits with a Conventional Commit message using the `attribute` skill's format (type prefix, Why-body, Refs: trailers).
- Commits are attributed to a bot identity (e.g., `kms-improvement-bot <kms-improvement@vivantel.dev>`).
- No PR is opened; changes land directly on the branch that triggered the run (or `main` for scheduled runs).

## Rationale

- The improvement harness is a background maintenance process, not a feature development flow. PR overhead for mechanical fixes (token economy, verbosity) is disproportionate.
- Layered verification (lint gate + eval gate + convergence detection) provides stronger safety than human review of hundreds of small fixes.
- Human review doesn't scale: a daily scheduled run might produce 50+ mechanical fixes. Reviewing each defeats the purpose.
- The `attribute` skill already produces traceable commit messages; auto-commits inherit this traceability.
- If a fix is wrong, `git revert` is trivial. The cost of a false positive is low; the cost of a false negative (missed fix) is accumulating technical debt.

## Consequences

- Branch protection rules must allow the bot identity to push (or the orchestrator runs with elevated permissions in CI).
- The improvement log (`0064`) is the primary audit trail — every auto-commit is logged with before/after diff summary.
- CI must verify that auto-commits only touch expected files and pass all checks (`0068`).
- A "kill switch" config option (`.opencode/improvement.yaml`) must exist to disable auto-commit globally or per improvement type.
