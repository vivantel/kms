---
id: 0089-opt-in-ci-recipes-ship-in-plugin-ci-dir
title: Ship opt-in pre-commit and GitHub Actions recipes in plugins/kms/ci/; they run only the deterministic checker
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-22
tags: [kms, packaging, automation]
---

## Decision

`plugins/kms/ci/` ships two copy-paste files, `pre-commit` and `kms-lint.yml`, that run `lint_check.py --strict` and nothing else (no model, no key). They sit beside `shared/` and `templates/`, not inside `templates/`: `templates/` holds artifact types that `bootstrap` seeds and `lint` check 12 syncs, and `scripts/vendor-shared.py` copies it into skills. Each file starts with a `kms-generated: true` comment; `uninstall` lists them (category 3c) and offers removal. Nothing installs them: `INSTALLING.md` documents the copy steps, and the adopter keeps their own copy of the checker at `.vivantel/akasha/lint_check.py`. This amends 0027's file classes (adds one) and the uninstall inventory.

## Why

The only automation was two Claude Code `SessionStart` hooks; a team on Codex or Kilo, or one that never runs a skill, had no trigger. The checker is deterministic, so a hook and a CI job give every agent the same guarantee.

## Tradeoffs considered

- **Documentation only**: no new file class, but each team rewrites the same ten lines.
- **Under `templates/ci/`**: gets vendored into every skill and read as an artifact type by `bootstrap` and check 12.
- **A pre-commit that installs itself**: rejected; hooks are the adopter's to choose.
- **Chosen: shipped, opt-in, outside `templates/`.**
