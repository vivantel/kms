---
id: 0058-deterministic-structural-lint-checks
title: Run lint's structural checks in a script, not through the model
status: active
date: 2026-11-08
tags: [kms, knowledge-management, eval-harness]
track: process
---

## Decision

`plugins/kms/shared/lint_check.py` performs lint checks 1, 2, 3, 7, 9, 12, 15, 19, 20 and 21 from frontmatter, file names and file text. The `lint` skill runs it first and reports its lines as those checks' findings. Checks 4, 5, 6, 8, 10, 11, 13, 14, 16, 17, 18, 22, 23 and 24 stay judgment-based. The script needs PyYAML, which the author accepted.

Checks 7, 9 and 12 join the deterministic set because each reduces to a lookup: an id or path searched across files (7, 9) or a template compared by `id` and version (12). Two exemptions in check 9 (a conditionally-optional file, a reference a plan marks as preserved history) cannot be decided from text, so the script reports those and the skill tells the model to dismiss them.

## Why

Until now `lint` had no code, so every check, including "does this id exist", depended on a model reading files. That made "mechanically checked" false for the system and made the lint eval measure the model's attention rather than the checks. A script is repeatable and testable (`evals/lint/unit/`).

The script is new code, not the `hooks/lint_check.py` on `harness/impl/step_01`. That file was reviewed and not reused: it parses `tags.md` and `INDEX.md` in formats this repository does not use (every tag would be flagged), excludes `archive/` when resolving ids (contradicting check 1), keeps one index per type (live and archive rows overwrite each other), and splits frontmatter at the first `---` anywhere. Its verbose-artifact heuristic was dropped as non-structural.

## Tradeoffs considered

- **Keep checks 7, 9 and 12 judgment-based**: avoids the two residual exemptions in check 9, but leaves lookups to the model's attention.
- **A stricter check 9 that drops reports inside decision files**: fewer false positives, but a stale path in a decision is still a finding under check 20's own wording.
- **Chosen: script all ten, document the check 9 limit.**
