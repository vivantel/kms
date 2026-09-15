---
id: 0016-lint-skill
title: Add lint — an on-demand, full-repo validation skill, separate from steward
status: active
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Add `lint`, a new skill: an on-demand, full-repo validation pass over a
project's `docs/{facts,decisions,guardrails,skills}/` tree, independent
of what changed in any particular session. It is a separate skill from
`steward`, not a mode of it — a third temporal pattern (on-demand,
full-scan) distinct from `steward`'s "after a work session" framing and
`bootstrap`'s one-time setup, matching this plugin's established pattern
of splitting skills by *when* they run rather than bundling multiple
temporal modes into one file.

Named `lint` rather than `audit`, to avoid reading as related to the
now-banned "audit-log" fact type
(`docs/decisions/0015-facts-must-not-be-audit-log-records.md`) — a
different word for a similar-sounding but unrelated concept would have
been a source of confusion.

`lint` checks: dangling `governed-by`/`grounded-in` references, missing
required fields per artifact type, numbering collisions, expired
decisions, redundant guardrails, audit-log-style facts, and orphaned
artifacts nothing references. It restates these checks in full rather
than pointing at `steward`'s file, the same way `clarify`/`roadmap`
already share their entire interview-mechanics text verbatim — each
skill must be self-sufficient since only the invoked skill's body is
loaded at runtime.

## Why

`steward`'s checks are explicitly session-diff-scoped and can't catch
rot that predates "this session" — pre-existing dangling references,
fields missing from artifacts nobody has touched recently, or a decision
whose `expires` date passed while nobody happened to run `steward`
around that time. A skill that scans the whole tree on demand, the same
way `changelog` reads full commit history rather than just recent
commits, closes that gap.

Kept as a separate skill rather than a `steward` mode because bundling
"check recent changes" and "check everything" into one file forces the
common case (a post-session check) to carry the rare case's scanning
logic on every load, the same reasoning that already split
`bootstrap`/`steward` apart in
`docs/decisions/0009-bootstrap-and-steward-skills.md`.

## Tradeoffs considered

- **A mode of steward** (e.g. "steward --full"): fewer files, reuses
  steward's existing checks directly, but forces one file to describe
  two distinct invocation patterns and their different completeness
  guarantees. Rejected, matching the reasoning that already split
  bootstrap from steward.
- **Name it `audit`**: more immediately descriptive, but risks reading
  as related to the just-banned "audit-log" fact type. Rejected.
- **Chosen: a new, separate skill named `lint`.**
