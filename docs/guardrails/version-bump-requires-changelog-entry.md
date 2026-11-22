---
id: version-bump-requires-changelog-entry
title: Every plugin manifest version bump must have a matching CHANGELOG.md entry
status: active
date: 2026-09-12
tags: [kms, git, changelog, release, packaging, guardrail]
governed-by: [0050-version-bump-changelog-linkage]
derivation-note: >
  Given decision 0050 (a version bump and its changelog entry are one unit
  of work), every future bump must have its entry before it's considered
  shipped.
pinned:
  0050-version-bump-changelog-linkage: "8622759d8dce"
---

## Guardrail

Whenever `docs/guardrails/plugin-manifest-version-sync.md` fires,
`CHANGELOG.md` MUST gain a `## [x.y.z] - date` heading for that version
before the bump is considered done — never deferred to "later." Scope is
narrow: how the entry is produced is free (by hand, or any
tool), and unnamed/exploratory work between versions still needs no
entry.

## Derivation

- **Axiomatic basis**: `docs/decisions/0050-version-bump-changelog-linkage.md`
  — the team committed to treating a version bump and its changelog entry
  as one unit of work, without reopening how the entry is generated.
- **Background (retired fact)**: `docs/facts/archive/0013-changelog-lagged-four-version-bumps.md`
  — four manifest version bumps landed with zero corresponding entries
  before this rule existed.
- **Normative conclusion**: therefore a version bump and its `CHANGELOG.md`
  entry are treated as one unit of work, not two independently-timed ones.
