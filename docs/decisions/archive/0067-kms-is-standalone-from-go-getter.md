---
id: 0067-kms-is-standalone-from-go-getter
title: kms stays a standalone knowledge-system plugin; go-getter owns its fork
status: superseded
superseded-by: 0070-kms-is-the-knowledge-base-core-consumed-by-pin
accepted-by: Sergei Strebulaev
date: 2026-11-12
tags: [kms, scope, packaging]
---

## Decision

kms is a standalone knowledge-system plugin for any git project. go-getter is a separate project that forked kms's skills in 2026-10 and owns its copy. kms does not vendor, sync with, or try to become it; ideas may be borrowed, code is not shared.

## Why

go-getter's own decision 0066 states "There is no upstream to sync from", and the two have diverged. Keeping kms focused on the fact/decision/guardrail/procedure system keeps its skill bodies small (`docs/guardrails/token-economy.md`).

## Tradeoffs considered

- **Upstream library for go-getter**: rejected by go-getter's own 0066; would couple release cadences.
- **Retire kms**: would end the redesign in `docs/plans/kms-review-and-redesign.md` after phase 1. Rejected by the owner.
