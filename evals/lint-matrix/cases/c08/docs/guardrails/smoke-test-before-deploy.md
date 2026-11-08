---
id: smoke-test-before-deploy
title: Every deploy runs the smoke test first
status: active
date: '2026-10-01'
tags: [release]
governed-by: 0002-changelog-per-release
grounded-in: [0001-release-cadence]
derivation-note: Follows from the release cadence fact.
---
## Guardrail

Before any deploy, the deploy checklist runs the smoke test suite and aborts on failure.

## Derivation

A failed deploy costs a weekly release.
