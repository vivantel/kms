---
id: 0045-seed-tags-from-canonical-list-as-template
title: Extend the seeded guardrail templates to include tags-from-canonical-list
status: active
date: 2026-09-05
tags: [kms, knowledge-management, guardrail]
track: process
---

## Decision

`plugins/kms/templates/guardrails/` gains a 5th seeded template,
`tags-from-canonical-list.md`, alongside the four established by
`docs/decisions/0027-baseline-guardrail-seeding.md`. Its content matches
`docs/guardrails/tags-from-canonical-list.md`'s `## Guardrail` section,
generalized the same way the other four templates are (`governed-by`/
`grounded-in` left `TBD`, a generic starting point rather than a
project-specific derivation) — so a project adopting `kms`'s tag
vocabulary mechanism (`docs/decisions/0042-tag-vocabulary-and-scoped-contradiction-check.md`)
gets this guardrail seeded automatically via `bootstrap`, rather than it
only ever existing in this repo's own dogfooded copy.

This repo's own `docs/guardrails/tags-from-canonical-list.md` is
deliberately **not** retroactively marked `kms-seeded: true` — it
predates the template (this repo's copy was authored directly from
`0042`, then the template extracted from it, not the reverse), so
marking it seeded would misrepresent its actual provenance. `lint`
check 12 already treats a non-seeded file matching a template as
project-owned, "possibly a deliberately-detached former template" —
exactly this case.

## Why

`0027` explicitly scoped `plugins/kms/templates/guardrails/` to exactly
four named guardrails when it established the templating mechanism.
Adding a fifth without a decision recording why breaks that decision's
own declared scope — discovered by a code-review pass after the
template had already been added directly, with no such decision. The
template itself is worth keeping despite the process gap: without it,
`docs/guardrails/tags-from-canonical-list.md`'s normative claim (any
artifact's tags must come from the canonical list) would only ever
exist in this one repo, never propagating to a project that adopts the
tag-vocabulary mechanism `0042` introduces — the same category of gap
`0027` itself exists to close for the original four.

## Tradeoffs considered

- **Revert the template instead of authorizing it**: keeps `0027`'s
  scope technically untouched, but reopens the propagation gap the
  template exists to close, for a mechanism (`0042`) this repo already
  relies on itself.
- **Fold this into `0042` retroactively**: not possible — decisions are
  immutable once accepted.
- **Chosen**: a new, minimal decision authorizing the addition, rather
  than reverting a useful template or leaving its addition undeclared.
