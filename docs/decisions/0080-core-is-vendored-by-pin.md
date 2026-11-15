---
id: 0080-core-is-vendored-by-pin
title: go-getter consumes the knowledge-base core by vendoring it at a pinned release tag
status: draft
date: 2026-11-15
tags: [kms, packaging]
---

## Decision

go-getter consumes the core by **vendor by pin**: `artifact-model.md`, `lint_check.py`, `migrate.py` and `evals/lint/conformance/` are copied from a named kms release tag (`kms-schema-<version>`). go-getter adds `check core-pin` (CI fails if the copy differs from the tag, or if the schema version it records does not match the vendored model's first line) and a `go-getter core update <tag>` verb that does the copy. It is not a runtime dependency and not a shared package. `docs/skills/core-contract.md` names the mechanism.

## Why

go-getter already has `check plugin-pin`, `check deps` and `check generated`, so one more pin check fits its habits. Four small files do not justify a package or a second plugin to keep in sync.

## Tradeoffs considered

- **Install kms as a prerequisite**: rejected. It breaks go-getter's one-install story and adds a second plugin manifest to keep in sync.
- **Git submodule or subtree**: rejected. Heavy for four files.
- **npm or pip package**: deferred until a third consumer exists.

## Twin

go-getter twin: written in D0. Draft by an agent; owner acceptance in plan phase I. Plan: `kms-core-and-go-getter-consolidation.md` C3.
