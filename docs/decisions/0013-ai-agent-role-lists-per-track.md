---
id: 0013-ai-agent-role-lists-per-track
title: bootstrap creates, steward maintains, product/process role lists for reviewing decisions
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Two skill-prescription artifacts, `docs/skills/product-track-roles.md` and
`docs/skills/process-track-roles.md`, each list the AI-agent review
perspectives relevant to that track — a role name plus a one-line scope
(what kind of decision it should weigh in on), not a human staffing
assignment.

`bootstrap` creates both lists as an extension of its existing
skill-gap-detection step: the same repo-scan that already maps a signal
to a candidate skill domain also gets a role column, and the two lists
are compiled from it. `steward` keeps them current: if recent decisions
of a track suggest a role not on that track's list, or a listed role
hasn't matched anything in a while, propose an addition/removal.

A "role" is a lightweight perspective checklist — the same agent
considers it while drafting or reviewing a decision, not a separate
agent/persona actually invoked per role.

`roadmap` checks for the matching track's role-list file and surfaces it
as context while drafting a decision of that track, if the file exists;
if it doesn't (e.g. `bootstrap` hasn't run yet, or a project has no role
lists), `roadmap` proceeds exactly as it does today.

## Why

This generalizes a pattern that already works in practice elsewhere: a
decision-class-to-reviewer mapping that tells an agent which perspective
a decision needs before it's finalized. Simplified here to two tracks
instead of many fine-grained decision classes, to stay cheap — a full
decision-class taxonomy would be a much larger, project-specific design
effort every time `bootstrap` runs.

Extending the existing skill-gap-detection table (rather than a new
scanning step) reuses signal-detection work `bootstrap` already does —
the same repo signals that suggest a missing skill also suggest which
perspective should own reviewing decisions in that area.

Keeping roles as a lightweight checklist rather than literal per-role
agent invocation avoids a large orchestration cost for a feature whose
value is mostly "don't forget to think about X" — real multi-agent
review is a different, larger feature this decision explicitly doesn't
build.

No guardrail governs this: "the role lists must stay current" is only
ever true "whenever `bootstrap`/`steward` runs" — a separate guardrail
would just restate their own procedure, which
`docs/decisions/0012-no-redundant-guardrails.md` already rules out.

## Tradeoffs considered

- **A full decision-class taxonomy** (like a fine-grained council table):
  more precise, but expensive to derive and maintain per project.
  Rejected in favor of the existing two-track split.
- **Literal per-role agent invocation**: real multi-perspective review,
  but a much bigger cost/complexity jump — orchestration, not just an
  artifact. Deferred; nothing today needs it.
- **roadmap always surfaces the role list unconditionally**: rejected —
  couples `roadmap` to an artifact that may not exist, and `roadmap`
  ships to projects that may never run `bootstrap`.
- **Chosen: a lightweight, two-file checklist; bootstrap creates it as
  part of existing signal-scanning; steward maintains it; roadmap
  consults it only when present.**
