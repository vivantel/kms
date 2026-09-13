---
id: 0057-confirming-party-generalizes-human-checkpoint
title: Generalize lint's "wait for human confirmation" gate to "wait for a confirming party"
status: active
date: 2026-09-13
tags: [kms, knowledge-management, automation]
track: process
grounded-in: [0056-chunked-checkpointed-execution-for-bootstrap-and-lint]
---

## Decision

`lint`'s gate ("never silently fix anything — propose the fix and wait for confirmation") generalizes to
a **confirming party**: ordinarily the human user, but an explicitly authorized reviewing subagent may
stand in for one, acting within its own configured authority.

This decision's scope is `lint`'s gate specifically — the one the `0056-...` validation phase actually
runs into, since `bootstrap` writes directly with no gate of its own. Several other skills phrase an
analogous gate around a human specifically — `roadmap`'s "before writing anything" and "until the user
has confirmed," `clarify`'s "until I confirm," `capture`'s "owning domain's sign-off," `attribute`'s
"confirm the list with the user," `refactor-plan`'s "ask the user to confirm," `uninstall`'s "wait for an
explicit yes" — and are natural candidates for the same generalization, but are **not** changed by this
decision; extending it to them is deliberately left as a follow-on, tracked in `docs/plans/scale-
bootstrap-and-lint-chunked-checkpointing.md`, not silently assumed done here.

This is a wording-scope decision only. kms does not define, ship, or own any authority-configuration
mechanism for a reviewing subagent — how a subagent is authorized, what scope it's granted, and how it
decides delegate-vs-escalate on a given proposal is entirely the deploying environment's concern, external
to this plugin. kms's own obligation is narrower: never hardcode an assumption, in a gate's own wording,
that the party on the other side of a "wait for confirmation" is necessarily a human.

## Why

This surfaced directly out of `0056-...`'s validation design: proving chunking/checkpointing holds at
real scale means running `bootstrap` and `lint` against a large fork unattended, and `lint`'s own gate
("propose the fix and wait for confirmation") is exactly the kind of point that would otherwise force
either silently skipping the propose→confirm→apply loop, or quietly redefining "confirmation" for one
validation run without ever writing that redefinition down as a decision. Neither is acceptable — this
plugin's whole design treats a proposal that needs confirming as consequential enough that it must never
be silently waived, and quietly bypassing that for one exercise would be exactly the kind of undocumented
exception this knowledge system exists to prevent.

Generalizing the wording, rather than special-casing an "automated mode" only for the validation run,
keeps the underlying principle intact (something must confirm before a consequential or hard-to-reverse
action lands) while making it possible for that something to be a genuinely authorized non-human party —
without kms itself taking on the harder, separate problem of how such authorization is granted, scoped, or
verified. That stays a deliberate non-goal: an authority-configuration mechanism is real infrastructure
(who grants scope, how it's revoked, what happens on ambiguous cases) on the order of decisions this
plugin has already declined to take on lightly, and nothing about the current scaling problem requires
kms to solve it.

## Tradeoffs considered

- **Leave `lint`'s gate wording human-specific, treat the validation run as a one-off silent exception**:
  no change needed, but repeats the exact failure mode this plugin's own guardrails exist to catch
  elsewhere — an undocumented exception to a stated principle, discovered only by reading the validation
  run's actual transcript rather than any written record.
- **kms defines its own authority-configuration mechanism** (a config file naming which checks/categories
  a reviewing subagent may auto-approve): more complete, and was raised directly during this decision's
  interview, but explicitly declined — it's a distinct, real infrastructure decision (config format,
  default policy, where it lives, how it's verified) that the person raising it directed not be designed
  here, since it's the reviewing agent's own concern, not something this plugin needs to own to solve the
  scaling problem at hand.
- **A single blanket "--auto" flag that disables all confirmation gates outright**: simplest to implement,
  but throws away the actual distinction that matters — a mechanical, reversible fix (an index re-sync, an
  archive move) is a fundamentally different risk than a judgment call (a contradiction resolution, a
  derivation rewrite), and a blanket bypass can't express that difference at all.
- **Chosen**: generalize `lint`'s gate wording to "confirming party" (human or an externally-authorized
  subagent acting within its own configured authority), with the authority mechanism itself explicitly
  left out of kms's scope, and every other skill's analogous gate deliberately left for a follow-on.
