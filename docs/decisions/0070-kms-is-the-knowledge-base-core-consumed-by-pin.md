---
id: 0070-kms-is-the-knowledge-base-core-consumed-by-pin
title: kms is the knowledge-base core; go-getter consumes it by pinned schema version instead of forking it
status: draft
date: 2026-11-15
tags: [kms, scope, packaging]
track: process
---

## Decision

The knowledge-base core (artifact model, structural checker, conformance fixtures) is defined once, in kms, and versioned by a schema version independent of the plugin version. go-getter ships no fork of it and pins a kms schema release. kms stays standalone and usable alone. Proposes superseding `0067-kms-is-standalone-from-go-getter` (the supersession and archive move are applied only after the owner accepts this draft; until then 0067 stays as it is) and go-getter 0066.

## Why

Plan step A1 measured the two models: 9 identical items, 4 kms-only, 3 go-getter-only, 2 conflicting, so the verdict is "alignment is a cleanup" (`docs/plans/archive/consolidation-model-diff.md`). A2 found the checker is kms-only (`lint_check.py`; go-getter's lint is prose) and 5 of 14 skills identical (`docs/plans/archive/consolidation-skill-diff.md`). The cost of keeping two forks (silent drift since 2026-10) now exceeds the cost of one pin.

## Tradeoffs considered

- **Clean-break third repo**: only warranted on a rewrite verdict; not the case.
- **Keep 0067 (no sharing)**: leaves the drift and two checkers.
- **Merge the products**: rejected in 0069.

## Dependency

Rests on verdict *cleanup* from A1. Go-getter twin: written in D0. Draft by an agent; accepting means `status: active` plus `accepted-by`, then archive 0067 and update both INDEX files. Plan step A4.
