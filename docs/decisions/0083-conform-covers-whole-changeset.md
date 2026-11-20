---
id: 0083-conform-covers-whole-changeset
title: conform checks the whole changeset, including knowledge-base files and the facts a diff may falsify
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-16
tags: [kms, knowledge-management]
---

## Decision

Amends `0032-conform-skill` in part: its exclusion of knowledge-base changes is lifted. `conform` gains three read-only passes:

1. **Docs pass.** When the diff touches the knowledge directory, run `lint_check.py` on the post-diff tree (working tree for a staged diff, a temporary checkout of the head for a range) and report its lines in the same output.
2. **Structural fact pass.** List facts whose `source` or `scope.component` path-overlaps the diff as "re-verify".
3. **Advisory fact pass.** Flag a fact whose body names a value the diff changes as "may be falsified", without claiming it is.

A `status: draft` guardrail or decision is reported as proposed, never as a violation. `conform` stays read-only; the `SKILL.md` grows by at most 120 words.

## Why

A PR that touches code and a guardrail gets a split review today: `conform` skips the knowledge-base half and defers it to `lint`/`capture`, and nothing asks whether a fact the diff falsifies is now wrong. The checker already exists and runs on any tree, so the docs pass costs one command.

## Tradeoffs considered

- **Keep the exclusion:** consistent with 0032, but leaves the split review and the unasked fact question.
- **Do it in `capture`:** `capture` runs after a session, `conform` before commit; the fact question is a pre-commit one.
- **Judge every fact against the diff:** noisy; only path overlap is structural, the value-named pass is labelled advisory.

Owner to accept; on acceptance 0032 gets a dated `## Amendment` pointing here.
