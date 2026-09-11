---
id: 0047-operationalizes-field-and-unoperationalized-guardrail-check
title: Add an optional operationalizes field to Procedure, plus a lint check for guardrails missing one
status: draft
date: 2026-09-10
tags: [kms, knowledge-management, taxonomy, guardrail]
track: process
fitness-functions: ["lint check 23 (unoperationalized guardrail) is itself the automation for this decision's normative half — no separate manual check needed once it ships."]
---

## Decision

- `Procedure` (the fourth governed artifact type, `docs/skills/`) gains one
  new **optional** frontmatter field: `operationalizes: <guardrail-id[, ...]>`
  — which guardrail(s) this procedure's steps satisfy, when the procedure
  is a runbook/playbook for a guardrail's required behavior rather than
  general reference material. Most existing procedures won't carry it;
  this repo's own four (`adding-agent-support`, `automating-capture`,
  `kms-architecture`, `scoping-shipped-vs-repo-rules`) are all meta
  reference docs, not runbooks, and none gets it retrofitted by this
  decision.
- Multiplicity is many-to-many, unconstrained: a procedure may list
  several guardrail ids, and more than one procedure may list the same
  guardrail id (e.g. a general runbook plus a team-specific variant).
  Nothing enforces "exactly one canonical procedure per guardrail."
- A new `lint` check (23): a guardrail whose own text describes a
  recurring or multi-step action, with no `Procedure`'s `operationalizes`
  pointing back at it, is flagged — a judgment call, the same style as
  several existing `lint` checks (5, 6, 8), not a mechanical field-presence
  test. A guardrail that's a simple prohibition ("never commit secrets")
  never triggers this; one that implies an ongoing process ("every release
  must be tagged") does if nothing operationalizes it.
- Shipped immediately together, not phased — the field without the check
  would let `operationalizes` silently go unused; the check without the
  field would have nothing to check for a pass condition. Every existing
  adopting project's guardrails will surface as new debt the first time
  this check runs — accepted, not treated as a defect, the same way
  `docs/decisions/0040-lint-contradiction-and-staleness-checks.md`'s four
  new checks surfaced whatever violations already existed when they
  shipped.

This resolves the analysis question of whether `kms` needs a "runbook"/
"playbook" as a 5th artifact type — it doesn't; a runbook already fits
`Procedure`'s existing definition (general, parametric, invoked
repeatedly — see `docs/decisions/0037-plans-not-a-governed-artifact-type.md`'s
own parametric/applied test) and `bootstrap`'s existing skill-gap table
already detects "recurring manual process, no written procedure" as a
domain signal. What was actually missing was traceability: `Procedure`
was the only one of the four governed types with zero type-specific
frontmatter (`Fact` has `kind`/`governed-by`; `Guardrail` has
`governed-by`/`grounded-in`/`derivation-note`; `Decision` has `track`/
`superseded-by`/etc.), so nothing let a guardrail's required behavior be
checked against whether a written procedure actually exists for it.

## Why

`operationalizes` lives on `Procedure`, not on `Guardrail` (as a reverse
pointer), because a guardrail is meant to stay simple — a single MUST/
MUST NOT statement plus its own derivation chain back to the decision and
fact that produced it (`docs/decisions/archive`'s original derivation
recipe). Adding a forward-pointing list of implementing procedures to
every guardrail would mean updating the guardrail file every time a new
runbook is written for it; putting the pointer on the procedure instead
means writing a new runbook never requires touching the guardrail it
serves.

Many-to-many multiplicity (not "exactly one procedure per guardrail") was
chosen because real operational practice already produces this shape —
a team might have both a general runbook and an environment-specific
variant for the same required behavior, and constraining that would
fight how runbooks actually get written and revised over time, not help
`lint` do its job.

Shipping the check alongside the field (rather than deferring it) matches
what the user actually decided when asked directly — the alternative
(field now, check later) was offered and recommended, but rejected in
favor of getting the checkable guarantee immediately rather than waiting
for organic `operationalizes` adoption to build up first.

## Tradeoffs considered

- **A 5th governed artifact type ("runbook"/"playbook")**: rejected —
  fails `docs/decisions/0037-...`'s parametric/applied test the same way
  every other candidate for a new type would need to pass it; a runbook
  is parametric and reusable, exactly what `Procedure` already is.
- **`operationalizes` as a reverse pointer on `Guardrail` instead**:
  keeps the guardrail file self-describing, but couples every new runbook
  to an edit of the guardrail it serves — rejected for the reason in
  "Why" above.
- **Ship the field alone, defer the check** (this decision's original
  recommendation): avoids an immediate mass-debt surfacing across every
  adopting project's existing guardrails, letting real usage patterns
  inform the check's exact heuristic first. Rejected — explicitly, by
  direct choice, in favor of shipping the checkable guarantee now.
- **Constrain to exactly one procedure per guardrail**: simpler to
  reason about, but doesn't match how runbooks are actually maintained
  in practice (variants, revisions co-existing). Rejected.
- **Chosen**: optional `operationalizes` on `Procedure`, many-to-many,
  plus `lint` check 23, shipped together.

## Amendment (pre-merge review, 2026-09-11)

Checked check 23 against this repo's own 14 guardrails before merging, per the standard
"does this actually propagate correctly" pass: almost none of them could ever be satisfied by
`operationalizes`, because the thing that actually carries most of them out is a *shipped
skill* (`lint`, `bootstrap`, `capture` — code in `plugins/kms/skills/`), not a `docs/skills/*.md`
procedure — and `lint` explicitly treats that packaging layer as out of its own scope. Check 23
as originally worded had no way to recognize "enforced by code/CI instead of a written
procedure" as satisfying a guardrail, so it would have flagged most of kms's own guardrails as
unoperationalized, permanently and unactionably — not a one-time debt-surfacing like
`docs/decisions/0040-...`'s checks, which real usage could eventually resolve.

This isn't kms-specific: any project enforcing a rule via a script or CI job rather than a
written runbook would hit the same false positive. Fixed by widening check 23's satisfying
condition to "a procedure operationalizes it, *or* it's already actively enforced by code (a
CI check, a hook, a shipped skill/tool's own logic)" — `plugins/kms/skills/lint/SKILL.md`'s
check 23 wording updated accordingly. The field itself (`operationalizes`) is unchanged; only
the check's definition of "satisfied" widened.
