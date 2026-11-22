---
id: 0086-default-knowledge-directory-vivantel-akasha
title: New projects get their knowledge base at .vivantel/akasha/docs/; the path is resolved, not hardcoded
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-22
tags: [kms, packaging]
---

## Decision

`bootstrap` creates a new project's knowledge base under `.vivantel/akasha/docs/` (holding `facts/`, `decisions/`, `guardrails/` and `skills/`). A project that already has `docs/{facts,decisions,guardrails,skills}/` keeps it; nothing is moved. Skills and the checker do not name a literal path: they resolve the knowledge directory once and say "the knowledge directory". Resolution order: the path in the AGENTS.md kms block's `kms-dir:` line, else an existing `.vivantel/akasha/docs/`, else `docs/` if it holds `decisions/`, else the first root-level directory holding `decisions/`. `bootstrap` writes `kms-dir:` into the block so every later run, and the hooks, read it instead of guessing. A user may choose another path at bootstrap; the same line records it.

## Why

A knowledge base in `docs/` collides with a project's own documentation tree (a Sphinx `docs/` was written beside its `.rst` files in a cold start on 2026-11-22) and reads as published docs. A hidden, vendor-namespaced directory keeps the base independent of any docs tool and the same across projects. The checker already takes `--docs DIR` and the artifact model already defines the knowledge directory as the one holding `decisions/`, so the cost is making resolution explicit, not adding a concept.

## Tradeoffs considered

- **Hardcode the new path everywhere**: simplest text, but breaks every existing adopter and any user who wants another location.
- **A `KMS_DIR` environment variable**: invisible to a teammate and to CI; a line in the committed AGENTS.md block is shared.
- **Migrate existing projects too**: rejected for now; moving a populated `docs/` rewrites every cross-reference. `migrate.py` support, if wanted, is a later decision.
- **Chosen: resolve, with `kms-dir:` as the source of truth.**

Ships in the same release as the `docs/skills/` to `docs/procedures/` rename, so adopters change once.
