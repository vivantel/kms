---
id: require-changelog-entry
title: Every release must have a changelog entry
status: active
date: '2026-10-01'
tags: [release, documentation]
governed-by: 0002-changelog-per-release
grounded-in: [0001-release-cadence, 0002-changelog-per-release]
derivation-note: Weekly cadence plus the per-release entry rule imply one entry a week.
---
## Guardrail

A release without a CHANGELOG.md entry is not shipped.

## Derivation

Weekly releases (fact) and the per-release entry rule (decision) imply one entry per week.
