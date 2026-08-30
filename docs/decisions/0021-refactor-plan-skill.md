---
id: 0021-refactor-plan-skill
title: Add refactor-plan — a phased, guardrail-respecting refactor-planning skill
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Add `refactor-plan`, a new skill: given a refactoring goal, produce a
phased plan — (1) query the knowledge base for relevant decisions and
guardrails, (2) map dependencies affected by the change, (3) produce
step-by-step phases with verification checkpoints and rollback
strategies, (4) recommend which facts or decisions need updating once
the refactor lands — citing specific artifact paths throughout, and
flagging for confirmation any step that would violate a standing
guardrail rather than silently proceeding or silently dropping the
step. Writes nothing to disk.

Dependency mapping (phase 2) does its own direct, lightweight scan and
separately recommends running `lint` before/after for full validation,
rather than depending on invoking `lint` as a sub-step — this plugin's
skills don't assume runtime invocation of one another (per
`docs/decisions/0016-lint-skill.md`, which restates `steward`'s checks
in full rather than depending on it, because "only the invoked skill's
body is loaded at runtime"), and this plugin ships to more than one
agent, not all of which necessarily support one skill invoking another.

## Why

Refactoring is the one planning task in this plugin's scope where
getting it wrong is expensive after the fact (mid-refactor reversal,
or a plan that silently steps on a guardrail nobody re-checked) —
exactly the profile `roadmap`'s "hard to reverse, surprising without
context, or a genuine tradeoff" bar uses for what deserves a full
record, applied here to planning itself rather than to one decision.
Neither `brainstorm` (unconstrained, knowledge-base-blind ideation) nor
`onboard` (role-based ramp-up) nor `clarify`/`roadmap` (single-decision
interviews) cover "plan a bounded, multi-step change against what the
project has already committed to."

Requiring guardrail-violation flags rather than silent pass-through
matches `lint`'s "never silently fix anything" and `steward`'s
"contradiction found → block" disciplines — a refactor plan that
proceeds past a guardrail violation without surfacing it would defeat
the point of consulting guardrails at all.

## Tradeoffs considered

- **Have refactor-plan invoke lint as a literal sub-step**: matches the
  original phrasing most literally, but introduces a runtime
  cross-skill dependency this plugin has consistently avoided
  elsewhere, and assumes a level of agent skill-invocation support this
  plugin can't guarantee across every packaged target. Rejected.
- **Fold into roadmap**: `roadmap` captures one already-decided change
  as artifacts; `refactor-plan` plans a not-yet-started multi-step
  change against existing artifacts and produces no new artifacts of
  its own. Different inputs, different outputs. Rejected.
- **Chosen: a new, separate, read-only, citation-required skill.**
