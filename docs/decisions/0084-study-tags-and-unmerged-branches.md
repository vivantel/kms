---
id: 0084-study-tags-and-unmerged-branches
title: Study tags are measurement snapshots exempt from the release-tag rule; three study branches were not merged
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-16
tags: [kms, packaging]
---

## Decision

1. `study-v1` and `study-v2` are measurement snapshots. They are exempt from `0048-tag-git-releases-matching-plugin-version`'s "tags match plugin.json" rule and are never reused or moved.
2. Three branches were not merged and were deleted from `origin` on 2026-11-16. Tips, for restoring with `git push origin <sha>:refs/heads/<name>` while GitHub still holds the objects:
   - `harness/impl/step_01` (206f4aefc50e): an autonomous self-improvement loop on OpenCode. Its checker was rejected in 0058; its 13 draft decisions collide with master's numbering; auto-commit contradicts `lint`'s never-fix rule.
   - `fix-eval-doc-drift` (5593e6a4f11b): a model-first README superseded by 0052 and PR #51. Two tables (per-skill Reads/Writes/Blocks, "what this system does not do") were meant to be salvaged; the objects were no longer fetchable on 2026-11-16, so they are rewritten from the current model instead.
   - `scale-bootstrap-lint-chunking` (0767100ab21f): checkpointed `bootstrap`/`lint`, abandoned when its resume evals failed with `spawn E2BIG`. Deferred, trigger: a reported `bootstrap` failure on a large repository after the history-size prompt is in use.

## Why

0065 and 0066 cite the two tags and a future reader would otherwise read them as release tags that broke 0048. The branches held work that was reviewed and declined; recording why and where the tips were stops the same work being redone.

## Tradeoffs considered

- **Delete the tags:** 0065/0066 cite them as the measured state.
- **Keep the branches:** three stale remote branches that collide with live numbering and rules.

Owner to accept.
