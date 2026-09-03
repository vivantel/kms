---
id: 0040-lint-contradiction-and-staleness-checks
title: Add lint checks for cross-artifact contradiction, stale debt, and stale fitness-functions
status: active
date: 2026-09-01
tags: [kms, knowledge-management, taxonomy]
track: process
fitness-functions: ["Adopt a reproducible eval harness (e.g. promptfoo, https://github.com/promptfoo/promptfoo) with a Claude Code adapter provider, wired into CI, to compare lint/capture/roadmap output before and after a change to this repo's own skill bodies or artifact model — declared debt, no implementation yet; see Why for why it's deliberately out of this decision's scope."]
---

## Decision

`lint` gains four checks:

15. **Track exclusivity violation** — a `track` field found with a
    literal `both`/`mixed`/similar value
    (`docs/decisions/0038-track-field-mutual-exclusivity.md`), rather
    than exactly one of `product`/`process`.
16. **Cross-artifact contradiction** — two active (`status: active`)
    decisions, or a decision and a guardrail derived from it, making
    contradictory claims on overlapping subject matter — scanned across
    the whole project history, not just what one session just produced
    (`capture`'s check 4 already catches this within a session; nothing
    previously caught it standing between two already-existing
    artifacts).
17. **Stale unresolved debt** — a `governed-by: TBD`, `grounded-in:
    TBD`, or `status: draft` marker that has sat unresolved a long
    time, judged the same relative way check 14 already judges a role
    gone cold against the project's whole decision history.
18. **Stale fitness-functions** — a decision's declared
    `fitness-functions` entries that haven't been verified or
    re-checked in a long time, surfaced the same way rather than left
    standing as an unchecked promise.

Check 1 (dangling references) additionally validates `superseded-by`
targets (`docs/decisions/0039-unify-lifecycle-and-drop-scope.md`)
alongside `governed-by`/`grounded-in`. Check 2 (missing required fields)
additionally validates `status` against the unified 4-value enum, for
all four governed types.

## Why

`capture` only reasons about what one session just produced; it was
never meant to, and can't, catch a contradiction standing between two
artifacts that were each fine on their own when written but drifted
apart later, or a `TBD`/`draft` marker nobody has revisited since.
`lint` is the only skill with the full-history, whole-repo view needed
to catch either — matching its own stated job ("independent of what
changed this session... everything else") and its precedent for exactly
this shape of check (14, "role gone cold," already judges staleness
against full history rather than a session diff).

The `fitness-functions` field exists precisely to declare "here's how
we'd check this holds in reality" without requiring it be automated
immediately (`plugins/kms/shared/artifact-model.md`'s own field
description: "optionally... fitness-functions"). A declared
fitness-function nobody ever re-verifies is the same failure mode as a
`TBD` nobody resolves — check 18 closes that loop for every decision
that declares one, including this one's own entry above, which
deliberately logs the promptfoo/CI recommendation as debt rather than
building it now: this repo has zero CI, zero package manager, and zero
dependencies today, so adopting one is a decision (and infrastructure
buildout) in its own right, not a rider on a taxonomy/lifecycle-field
revision.

## Tradeoffs considered

- **Fold contradiction/staleness detection into `capture` instead**:
  rejected — both checks inherently need the whole project's history,
  not one session's diff, which is exactly the reasoning
  `docs/decisions/0016`/`0031` already used to keep full-repo checks in
  `lint` and session-scoped checks in `capture`.
- **Build the eval-harness recommendation into this decision instead of
  logging it as a fitness-function**: gets the "before/after" comparison
  in the same PR as the artifact-model changes, but bootstraps CI, a
  dependency, secrets, and a custom adapter all at once — a large,
  separable decision that deserves its own interview rather than riding
  along here. Git already preserves the "before" state as this commit
  regardless of when that lands.
- **Chosen: four new `lint` checks now; the eval-harness idea logged as
  declared debt via `fitness-functions`, deferred to its own future
  decision.**
