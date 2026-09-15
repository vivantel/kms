---
id: 0037-plans-not-a-governed-artifact-type
title: Plans are not a 5th governed artifact type
status: active
date: 2026-09-01
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

A plan (`docs/plans/<slug>.md`, produced by `roadmap`) is not a 5th
artifact type alongside facts, decisions, guardrails, and procedures
(`docs/decisions/0001-knowledge-artifact-storage-convention.md`). It
carries none of the governed lifecycle machinery those four types
share:

- No `track` (`docs/decisions/0010-decision-track-field.md`,
  `0038-track-field-mutual-exclusivity.md`).
- No `status` drawn from the unified enum
  (`docs/decisions/0039-unify-lifecycle-and-drop-scope.md`) and no
  `expires` — a plan keeps only its own existing, separate per-step
  legend (`done`/`pending`/`blocked`) for tracking execution, unrelated
  to the 4 types' lifecycle.
- Not scanned or structurally validated by `lint` the way the 4 governed
  types are.

## Why

The 4 governed types are all parametric statements: a decision states a
general commitment, a guardrail a general MUST derived from a decision
and a fact, a fact a general truth about the world, a procedure a
general how-to — none of them names the specific objects it will act
on; those are supplied when the statement is applied. A plan is the
opposite: it is fully applied. It names concrete files, concrete
decision ids, concrete steps, for one occasion — it is what results
from binding the general knowledge above to specific arguments and
running it once. That is why a plan is disposable where the 4 types are
durable: its concrete bindings go stale the moment it executes (the
files it named have since been edited), while a decision's generality
outlives any one occasion it was applied to.

This also gives the model a real, testable discriminator it lacked
before, not just a rule for `docs/plans/` itself: a candidate procedure
that hardcodes the specific files/decisions it will always act on is
actually a plan wearing a procedure's clothes, and genuinely reusable
guidance written into a plan is a procedure that landed in the wrong
place. `roadmap` (which decides where new content goes) and
`docs/skills/kms-architecture.md` (this repo's contributor reference)
both state the test, since it's operationally relevant to whichever
skill is placing new content.

This session's own predecessor plan,
`docs/plans/taxonomy-and-plan-organization.md`, is the concrete evidence
this needed stating: its step 2 added `track: product | process | both`
directly to plan frontmatter, treating plans as if they were a governed
type extending `0010`'s field — caught in review as introducing an
unminted, non-exclusive enum value with no decision behind it. Rather
than authorize that one case, this decision closes the general
question: plans were never one of the 4 types `0001` established, and
nothing about them (one-time, concretely-bound, disposable) fits that
model's shape.

## Tradeoffs considered

- **Make plans a 5th governed type**, with the same `track`/`status`/
  `expires` machinery as the other 4: the most uniform option, but plans
  fail the parametric test above — they're bound to concrete, one-time
  content by design, and adding lifecycle fields meant for durable,
  reusable claims would just be tracked noise (a plan is either being
  executed or it's finished; that's already its per-step legend's job).
- **A lighter partial governance** (e.g. just a `status: complete`
  marker, no `track`/`expires`): still conflates two different kinds of
  "done" — a plan finishing execution isn't the same claim as a decision
  reaching `active`, and half-governing plans invites the same confusion
  this decision exists to close.
- **Chosen: plans stay wholly outside the governed model.** Only their
  own per-step legend tracks state; `roadmap` (which produces them) and
  `lint` (which must not validate them like the 4 types) say so
  explicitly in their own bodies.
