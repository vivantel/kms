---
id: 0017-query-skill
title: Add query — an on-demand skill that answers questions from the knowledge base with citations
status: active
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Add `query`, a new skill: given a question, search
`docs/{facts,decisions,guardrails,skills}/` and answer using only what
those artifacts say, citing every artifact the answer drew from as a
`Refs:` trailer — the same citation format `attribute` already uses, so
this plugin has one citation convention, not two.

`query` only reads and cites; it never writes or edits an artifact —
that's `roadmap`'s (capture), `steward`'s (maintain), or `bootstrap`'s
(setup) job.

## Why

Every other skill in this plugin writes *to* the knowledge base; none of
them answer a question *from* it. Once a project accumulates a dozen
decisions and guardrails (this repo already has more than that), "what
did we decide about X, and why" becomes a real grep-and-read chore for a
human or agent — exactly the kind of task this plugin already exists to
make cheap for writing, but has never covered for reading.

Never answering from memory when the knowledge base already settles a
question mirrors the same discipline `clarify`/`roadmap` already apply
to facts ("if a fact can be found by exploring the environment, look it
up rather than asking") — `query` is that same discipline applied
retroactively, on demand, instead of during an interview.

## Tradeoffs considered

- **Fold into steward or lint**: rejected — both are write/validate
  skills; retrieval is a different job (read-only, user-facing answer)
  from either maintenance or validation.
- **Chosen: a new, separate, read-only skill.**
