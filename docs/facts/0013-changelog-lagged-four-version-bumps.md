---
id: 0013-changelog-lagged-four-version-bumps
title: CHANGELOG.md lagged four manifest version bumps before being backfilled
status: active
date: 2026-09-12
tags: [kms, git, changelog, release]
kind: environmental
governed-by: 0050-version-bump-changelog-linkage
---

## Fact

As of 2026-09-12, `plugins/kms/.claude-plugin/plugin.json`'s `version`
field had been bumped four times (`0.9.0` → `0.12.0`) with zero
corresponding `CHANGELOG.md` entries — the last real entry was `[0.8.0]`.
Backfilled retroactively in the same session this fact was written; see
`docs/decisions/0050-version-bump-changelog-linkage.md` for why.
