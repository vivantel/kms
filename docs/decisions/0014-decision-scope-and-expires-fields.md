---
id: 0014-decision-scope-and-expires-fields
title: Add optional scope and expires fields to decisions
status: active
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Decisions may optionally carry two fields:

- **`scope`** — what the decision applies to (free text, e.g. "this
  module only," "this release only").
- **`expires`** — when the decision stops being current: a date
  (`2026-12-01`) or a condition (`when the hypothesis test completes —
  see fact 0013`).

Both are optional — most decisions are permanent until superseded, and
forcing a value on every decision would just add "N/A" noise. `lifetime`
and `condition` (as originally proposed) are collapsed into the single
`expires` field: both answer the same question, "when does this stop
being current," just with a date vs. a condition.

`steward` gains a check: for every decision with `expires`, if a date
has passed or a condition has plausibly been met, surface it for
re-evaluation rather than leaving it standing as current. A guardrail
(`docs/guardrails/decision-expires-must-be-reevaluated.md`) states this
as a system-wide invariant, since a human reviewing decisions by hand
should catch an expired one too, not only `steward`.

## Why

Decisions today are treated as effectively permanent until a human
manually supersedes them — there's no mechanism for a decision that's
only meant to hold until a specific point (a hypothesis test, an
experiment, a temporary workaround). Without `expires`, these decisions
sit as `status: accepted` indefinitely unless someone remembers to
revisit them; `steward`'s existing check 2 only catches drift when a
*fact* changes, not when a decision's own self-declared expiration
arrives.

## Tradeoffs considered

- **Three separate fields (scope, lifetime, condition)**: more
  structure, lets a decision have both a hard date and an independent
  trigger simultaneously — but `lifetime` and `condition` answer the
  same underlying question, violating one-statement-one-job to keep them
  apart.
- **Required on every decision, `TBD` if not applicable**: forces a
  deliberate call every time, consistent with `governed-by`, but adds
  ceremony to the majority of decisions that are simply permanent.
- **Chosen: two optional fields, `scope` and `expires`.**
