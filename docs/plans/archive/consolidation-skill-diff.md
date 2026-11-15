---
title: Skill and checker diff, kms vs go-getter (plan step A2)
date: 2026-11-15
sources: kms plugins/kms/skills/*/SKILL.md vs go-getter skills/*/SKILL.md (master 1930ecf, read-only); normalised word-level diff, `<`/`>` lines counted
---

# Skill and checker diff

## Skills (14 shared)

| Skill | kms words | gg words | Diff lines | Divergence | Verdict |
|-------|-----------|----------|-----------|------------|---------|
| brainstorm | 329 | 329 | 0 | none | identical |
| changelog | 274 | 274 | 0 | none | identical |
| clarify | 262 | 262 | 0 | none | identical |
| onboard | 422 | 422 | 0 | none | identical |
| query | 312 | 297 | 15 | wording | identical (cosmetic) |
| quickstart | 309 | 314 | 43 | host/CLI wording | divergent (host-specific) |
| conform | 330 | 348 | 48 | wording plus gg CLI hooks | divergent (host-specific) |
| capture | 496 | 447 | 51 | gg shorter | divergent (semantic, small) |
| refactor-plan | 358 | 457 | 99 | gg adds unit-tree framing | go-getter-ahead |
| bootstrap | 1410 | 1372 | 126 | kms has marker/template steps; gg has pack hooks | divergent |
| uninstall | 431 | 519 | 120 | gg adds `.go-getter/manifest.json` and `apply --remove` | go-getter-ahead (host-specific) |
| lint | 1790 | 1473 | 333 | kms runs `lint_check.py` first and tags checks [structural]/[judgment]; gg is prose-only | kms-ahead |
| attribute | 297 | 575 | 356 | gg uses `go-getter refs --staged` must-have/should-have groups | go-getter-ahead (host-specific) |
| roadmap | 1284 | 1655 | 643 | gg decomposes into a unit tree (scope, Accept, owner kind, grants); kms writes records plus a roadmap file | divergent (semantic, the E1 split) |

Totals: identical 5 (incl. query), kms-ahead 1, go-getter-ahead 3, divergent 5. Seven of 14 differ only by go-getter CLI/host integration, so a shared core can be consumed without touching their prose; the semantic divergences are `roadmap`, `bootstrap`, `capture`.

## Checkers

Both lint skills list the same 24 checks in the same order. Their implementations differ:

| Check area | kms | go-getter | Verdict |
|------------|-----|-----------|---------|
| Structural lint (checks 1, 2, 3, 7, 9, 12, 15, 19, 20, 21) | `plugins/kms/shared/lint_check.py` (468 lines), CLI `--root`, `--pin`, 45 unit tests | none; the skill does it in prose | kms-ahead |
| Pinned-edge revisions (13) | `lint_check.py --pin`, `check_pins` | absent | kms-ahead |
| Fact `scope` validation | `check_scope` | absent | kms-ahead |
| `check indexes` | `check_index` (loose quoting) | `compiler/src/checks/indexes.mjs`, generated and sorted | go-getter-ahead |
| `check tags` | `check_tags` | `tags.mjs` | identical in intent |
| `check docs-consistency` | none | `docs-consistency.mjs` | go-getter-ahead (repo-specific) |
| `check plans` | none | `plans.mjs` | go-getter-ahead (plan legends) |
| `check meters`, `packs`, `neutral`, `self-adoption`, `generated`, `guardrails`, `deps`, `plugin-pin`, `versions`, `node-floor` | none | one module each (523 lines across `checks/`) | go-getter-only; coordination and harness, outside the core |

## Direction of later ports

- Checker: kms is the source (D1 vendors `lint_check.py` and the model). go-getter's `indexes`/`tags` checks stay as separate post-core checks, or their stricter index format is adopted by the core (resolves A1 item 18).
- Skills: nothing flows from go-getter into kms bodies except the `lint` cross-check and `attribute` refs idea, which stay go-getter-only (CLI-bound). `roadmap` is the only semantic fork; E1/E2 settle it.
