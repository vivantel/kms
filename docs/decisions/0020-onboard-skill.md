---
id: 0020-onboard-skill
title: Add onboard — a role-tailored, read-only onboarding-plan skill
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Add `onboard`, a new skill: given a role (e.g. "backend dev", "QA",
"writer"), read `docs/{facts,decisions,guardrails,skills}/` and produce
a 5-day action plan — daily goals, which of this plugin's skills to run
and when, and links to the specific artifacts relevant to that role —
without writing anything to disk. If critical artifact types are
missing entirely (most importantly, no facts at all), the plan says so
explicitly rather than producing a plan that quietly assumes context
that was never captured.

It is read-only and citation-based like `query`, but answers a
different question: `query` answers one specific question from the
knowledge base; `onboard` produces a structured, multi-day plan tailored
to a role, treating the whole knowledge base as its input rather than
searching for an answer to one query.

## Why

`bootstrap` sets a knowledge base up and `steward` maintains it, but
neither helps a new team member actually *use* what's there — that's
still a manual "go read docs/" task today, with no guidance on what to
read first or in what order for a given role. `onboard` turns the
knowledge base into a practical ramp-up plan instead of leaving a new
contributor to reconstruct that structure from scratch.

Warning on missing critical artifacts (rather than producing a
plausible-looking plan anyway) matches this plugin's existing
discipline in `query` ("if nothing relevant is found, say so plainly")
and `lint` (report structural gaps, don't paper over them) — an
onboarding plan built on a knowledge base with no facts in it would
misrepresent how much is actually documented.

## Tradeoffs considered

- **Fold into query** (treat "onboard me as X" as one big question):
  `query` answers from citations directly; `onboard` synthesizes a
  structured, sequenced, multi-day plan spanning the whole knowledge
  base. Different output shape and different completeness requirements
  (a query can legitimately say "nothing found"; an onboarding plan
  still owes the reader *something* to do on day one). Rejected.
- **Fold into bootstrap**: `bootstrap` sets the knowledge system up for
  the project as a whole; `onboard` is per-person, per-role, and runs
  any time a new person joins, not once. Different temporal pattern,
  matching this plugin's existing split-by-when-it-runs precedent.
  Rejected.
- **Chosen: a new, separate, read-only skill.**
