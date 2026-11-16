---
id: 0081-skill-moves-and-deprecation-window
title: Five skills leave kms after a one-release deprecation window; roadmap becomes decide
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-15
tags: [kms, scope, packaging]
---

## Decision

kms narrows to skills that read or write durable knowledge. Five skills produce plans, options or release output and move or leave:

| Skill | kms after | go-getter after |
|---|---|---|
| `roadmap` | renamed `decide`: interview to admissible records only, no plan file, no unit tree; `roadmap` stays one release as a deprecated alias | keeps `roadmap` as decomposition into units |
| `refactor-plan` | deprecated, removed after one release | keeps, as a decompose variant |
| `brainstorm` | deprecated, removed after one release | keeps |
| `clarify` | deprecated, removed after one release | folded into `discover` as its interview mechanic |
| `changelog` | deprecated, removed after one release | folded into `release` |

Deprecation window: one minor release in which each deprecated skill's description starts with "Deprecated: moved to go-getter, removed in 0.19" and still works. The removal is planned in `docs/plans/kms-remove-deprecated-skills.md` (H3).

## Why

Plans, brainstorms and changelogs are not durable knowledge (0069); go-getter already carries them with its coordination artifacts. Removing a shipped skill breaks installed users, so each move has a deprecation path and a named replacement.

## Tradeoffs considered

- **Remove immediately**: breaks installed users without notice.
- **Keep all fourteen**: keeps kms's prompt surface and maintenance cost for work outside its scope.

## Twin

go-getter twin: written in D0. Accepted 2026-11-16 by the owner. Plan: `kms-core-and-go-getter-consolidation.md` E1.

## Amendment 2026-11-16

The deprecation window is one minor release, which makes the removal release 0.17 (deprecated in 0.16), not 0.19 as the paragraph above and the skill descriptions said. The "0.19" was a slip carried from the plan (E1), not a longer window. The descriptions now say "removed in 0.17" (shipped in 0.16.3). The removal ships in 0.17, the next minor release.
