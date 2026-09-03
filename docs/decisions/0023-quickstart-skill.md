---
id: 0023-quickstart-skill
title: Add quickstart — bootstrap plus one real decision captured live
status: active
date: 2026-08-30
tags: [kms, onboarding, knowledge-management]
track: process
---

## Decision

Add `quickstart`, a new skill: run `bootstrap`'s setup (or confirm it's
already done), then immediately walk the user through capturing one real,
current decision as a full artifact in the same sitting — instead of
leaving "now go use `roadmap` sometime" as a cold follow-up action a new
user has no particular reason to take next.

Kept separate from `bootstrap` rather than added as a closing step to
it, matching this plugin's existing pattern of splitting skills by *when*
they run: `bootstrap` is one-time/rare setup; `quickstart` is a single,
guided first-use experience layered on top of it. Bundling first-use
guidance into `bootstrap` would add ongoing-relevance weight to a skill
meant to run once, the same reasoning
`docs/decisions/0009-bootstrap-and-steward-skills.md` already used to
split `bootstrap` from `steward`.

## Why

A new user who runs `bootstrap` gets a working `docs/` structure, but no
felt reason yet to keep using it — the value of this system only becomes
obvious once a real decision has actually been captured and can be
queried back. Every other skill in this plugin assumes the user already
knows what to do next; `quickstart` is the one skill whose entire job is
closing that gap for a first-time user, in one sitting, rather than
across several separate skill invocations they'd have to already know to
chain together.

## Tradeoffs considered

- **Extend `bootstrap` itself** with a closing "capture your first
  decision" step: fewer files, but forces every future `bootstrap`
  invocation (including gap-fill passes on existing projects) to carry
  first-use guidance that only makes sense the very first time. Rejected
  — chosen explicitly over this option when interviewed.
- **Do nothing, rely on README/docs to point new users at `roadmap`**:
  cheapest, but leaves the exact gap this decision exists to close —
  reading about a workflow doesn't produce the felt value of having
  already used it once. Rejected.
- **Chosen: a new, separate `quickstart` skill wrapping `bootstrap` and
  ending with one real decision captured.**
