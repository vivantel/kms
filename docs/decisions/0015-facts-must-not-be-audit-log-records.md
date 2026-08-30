---
id: 0015-facts-must-not-be-audit-log-records
title: Facts must not be audit-log records
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

A fact is legitimate if it's descriptive knowledge that grounds, or
could plausibly ground, a decision or guardrail. It's log noise — and
must not be written as a fact — if it's a timestamped event record with
no forward-looking derivational purpose and nothing references it.

`steward` checks for this: a fact reading like "X happened at time T"
with no fact/guardrail/decision grounded in it is flagged for removal or
rewrite, not left standing. A guardrail
(`docs/guardrails/fact-not-audit-log.md`) states the test as a
system-wide invariant.

kms is a knowledge base, not a dashboard, log, or monitoring tool —
`bootstrap`'s fact-extraction step and `steward`'s ongoing checks must
not let it accumulate into one.

## Why

`fact-governance-fields.md` already requires every fact to declare
`governed-by` — but that alone doesn't stop an LLM-driven `bootstrap`/
`steward` from writing routine event-log entries as if they were durable
knowledge (a real, observed failure mode in at least one related
knowledge system this session reviewed, where raw incident logs were
briefly embedded where they didn't belong). A one-time observation that
actually grounds a guardrail (e.g. "dependency X panicked once, here's
why we avoid it") is exactly the kind of fact this system wants; a
routine "run #4521 completed at 3:42am" with nothing built on it is not
the same thing, and a blanket "no logs" rule without a sharp test would
be as unenforceable as the guardrails already removed in
`docs/decisions/0012-no-redundant-guardrails.md`.

## Tradeoffs considered

- **Blanket ban on anything resembling a timestamped record**: simpler
  to state, but would also exclude legitimate one-time observations that
  ground a guardrail — too blunt.
- **No guardrail, `steward`-check only**: rejected — this is a
  system-wide invariant (a human hand-authoring a fact should also avoid
  this), not something true only "whenever `steward` runs."
- **Chosen: grounds-a-decision-or-guardrail vs. no-forward-looking-purpose
  as the test, enforced by both a steward check and a guardrail.**
