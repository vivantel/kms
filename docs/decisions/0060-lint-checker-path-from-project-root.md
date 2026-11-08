---
id: 0060-lint-checker-path-from-project-root
title: The lint skill names the checker path so it resolves from the project root
status: active
date: 2026-11-08
tags: [kms, eval-harness, knowledge-management]
track: process
---

## Decision

The lint skill describes the checker's location as `shared/lint_check.py` two directories above the skill's own directory, gives the `.kilo/` layout as an example, and says to resolve it from the project root.

## Why

The skill said `python3 ../../shared/lint_check.py`, which resolves against the shell's working directory, not the skill file. In a probe on 2026-11-08 the model ran it from the project root, got "No such file", and fell back to reading files by hand, so structural-check results would have measured whether the model found the script. Decision 0058 assumed the relative path would work.

## Tradeoffs considered

- **A hook or wrapper that exports the path**: deterministic, but needs per-agent wiring this plugin does not otherwise have.
- **Copy the checker into each project**: resolves the path, but forks the code.
- **Chosen: say where it is and how to find it.** It still depends on the model following the instruction; the matrix measures how often it does.
