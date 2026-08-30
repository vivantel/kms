---
id: 0019-brainstorm-skill
title: Add brainstorm — a generative, write-nothing ideation skill
status: accepted
date: 2026-08-30
tags: [kms, ideation]
track: process
---

## Decision

Add `brainstorm`, a new skill: given a problem or feature description,
produce 5-7 distinct approaches (each with pros, cons, risks, and an
effort estimate), then synthesize 2-3 recommended directions. It writes
nothing to disk and never queries `docs/{facts,decisions,guardrails,skills}/`
— unlike every other skill in this plugin, `brainstorm`'s job is
unconstrained ideation, not knowledge-base-grounded work.

It stays generative (produce options) through the approach-listing
phase and only becomes evaluative (compare, recommend) in the synthesis
phase — the same discipline `clarify`/`roadmap` already apply to
splitting "explore the decision tree" from "classify the outcome",
kept explicit here because ideation collapses into premature judgment
easily without it.

## Why

Every other skill in this plugin either writes to the knowledge base
(`roadmap`, `bootstrap`, `steward`) or reads from it
(`query`, `attribute`, `lint`, and now `onboard`/`refactor-plan`). None
of them cover the step before any of that: generating candidate
approaches to a problem that doesn't have a decision yet to record or
query. `clarify` interviews about a plan the user already has in mind;
`brainstorm` is for when there isn't one yet.

Excluding the knowledge base by design (not just by omission) keeps
`brainstorm`'s output unanchored to this project's existing decisions —
useful specifically because sometimes the right approach is one prior
decisions would have ruled out, and that tension is exactly what should
surface for a human to weigh, not get silently filtered before it's
ever generated.

## Tradeoffs considered

- **Let brainstorm read the knowledge base for context**: could produce
  more project-fitted suggestions, but risks anchoring ideation on
  existing decisions before divergent options are even generated —
  the opposite of what a generative-ideation skill is for. Rejected.
- **Fold into clarify**: `clarify` interrogates an existing plan;
  `brainstorm` generates plans that don't exist yet. Different starting
  conditions and different failure modes (leading questions vs.
  premature convergence) argue for separate skills, the same
  by-temporal/behavioral-pattern split this plugin already uses
  elsewhere (`docs/decisions/0009-bootstrap-and-steward-skills.md`,
  `docs/decisions/0016-lint-skill.md`). Rejected.
- **Chosen: a new, separate, read-nothing/write-nothing skill.**
