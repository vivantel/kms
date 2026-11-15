---
title: Consolidation handover (plan step I1, partial)
date: 2026-11-16
---

# Handover

Stopped early: the machine's root filesystem hit 100% (550 MB free of 291 GB), so go-getter's `npm test` could not be re-verified after D2 (30 failures in worktree/work-* tests are ENOSPC symptoms, not confirmed regressions; the full run passed 1438/1438 after D1). Free disk, then re-run `npm test` in the go-getter worktree.

## Branches
- kms: `feat/kms-core-consolidation` @ e1208e4 (all steps merged into it; `wt/consolidation` is the same commit). Nothing pushed, tagged or merged into master.
- go-getter: `feat/adopt-kms-core` @ e2d617c (worktree `/home/sergei/projects/vivantel/go-getter-wt/adopt-kms-core`, may be removed; the branch stays).

## Done
A1-A4, redesign 2.1-2.10 (matrix regrade and eval runs blocked: no provider key or kilo), B1-B3, C1-C3, E1, E2, F1, D0, D1. D2 partly: corpus migrated, strict checker clean except 21 facts without a `source` or citer (see below).

## Not done
D2 (21 facts: add `source` or retire; tests not re-run), D3, E3, F2 (go-getter CI conformance), G1, G2, H1-H3, I1 full.

## Owner decisions pending (all `status: draft`)
kms: 0069, 0070, 0071-0078, 0079, 0080, 0081, 0082 (dependents and revert hints are in the table in the plan). go-getter: 0210-0214 (revert: the D0 commit). Accepting means `status: active` plus `accepted-by`; accepting 0070/0211 means archive 0067 and 0066.

## Blocked
Lint-matrix relabel run, `npm run eval`, decide eval (need kilo CLI and a provider key); release steps (push, tag `kms-schema-1.0.0`, then `go-getter core update <tag> --from <kms>`, which currently pins a commit).

## Core changes found during D2
Guardrail `enforced-by` field; skipped numbers advisory (both in kms, vendored).
