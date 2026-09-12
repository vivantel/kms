---
id: 0053-decision-accepted-by-field
title: Add an optional accepted-by field recording who is accountable for a decision
status: active
date: 2026-09-12
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

Decisions gain an optional `accepted-by: <name>` field, set when
`status` first becomes `active` (`plugins/kms/shared/artifact-model.md`).
It records who is accountable for the decision's content — not
necessarily whoever ran the commit. `capture` and `roadmap` both set it
in the same edit that flips a decision to `active`, so it doesn't become
a field nobody actually populates. Not backfilled onto the ~50 decisions
that predate it — same precedent as `operationalizes` (`0047`): new
fields apply going forward, retroactive backfill is separate, later work
if ever warranted.

## Why

Every artifact's attribution today rides entirely on git's own
`Author:` metadata — there is no field on the artifact itself recording
who is accountable for it. That's worked out fine in this repo so far
only because every commit happens to be made under one person's git
identity even when an AI agent drafted the actual content — which is
incidental to how this repo is configured, not something the model
itself guarantees. An agent committing under its own identity (a common,
realistic setup) would make git blame conflate "who typed it" with
"who's accountable for it," with nothing on the decision itself to
recover the distinction.

This also gives `docs/decisions/0025-...`'s successor — the still-open
question of stating `kms`'s own governance in `CONTRIBUTING.md` — a
concrete, per-artifact mechanism to point at: the process can say "the
maintainer accepts decisions," and each decision file can then actually
record that it was.

## Tradeoffs considered

- **Rely on git blame alone**: no new field, but conflates authorship
  with accountability whenever they diverge, and provides no answer at
  all for a squashed/rebased history where the original commit is gone.
- **Require `accepted-by` on every decision, backfill retroactively**:
  more complete, but forcing ~50 files through a field they were never
  drafted with is exactly the kind of manufactured, low-value work
  `docs/decisions/0038-...`'s reasoning about not inventing ungrounded
  values already argues against by analogy — nobody can accurately state
  who accepted a 45-day-old decision after the fact with any more
  confidence than "presumably the same person as now."
- **Chosen: optional field, set going forward by the skills that flip a
  decision to `active`, no retroactive backfill.**
