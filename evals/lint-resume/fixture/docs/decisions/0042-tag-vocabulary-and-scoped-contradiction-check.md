---
id: 0042-tag-vocabulary-and-scoped-contradiction-check
title: Add a canonical tag vocabulary; scope the contradiction check to tag overlap
status: active
date: 2026-09-01
tags: [kms, knowledge-management, scale]
track: process
---

## Decision

- **Canonical tag vocabulary** — `docs/skills/tags.md`: a `kms-generated:
  true` procedure artifact (same bucket and precedent as
  `docs/decisions/0013-ai-agent-role-lists-per-track.md`'s role lists),
  listing every recognized tag with a one-line meaning. `bootstrap`
  generates the initial list by extending its existing step 7 (which
  already compiles the track role lists from repo signals) to also
  compile the starting tag vocabulary from whatever tags already exist
  in the project, or from domain vocabulary in existing docs for a fresh
  one. Detection of a genuinely new tag is an explicit, required step —
  not left implicit — in every skill that assigns tags to a new or
  edited artifact (`bootstrap`, `capture`, `roadmap`): check each
  intended tag against the list's stated meanings; if none fit, propose
  a new tag (name, one-line meaning, why nothing existing covers it) and
  get confirmation before using it, the same shape as `capture`'s
  existing decision-stub proposal. `lint` flags any tag in use that
  isn't on the list, plus — symmetric to check 14's "role gone cold" — a
  listed tag unused for a long time.
- **Scoped contradiction check** — `docs/decisions/0040-lint-contradiction-and-staleness-checks.md`'s
  check 16 ("two `status: active` decisions... making contradictory
  claims... anywhere in the project's history") is narrowed: only
  compare two active decisions (or a decision and a guardrail derived
  from it) that share at least one **non-umbrella** tag from the
  canonical list above. A tag carried by more than half of active
  decisions is marked `umbrella` in `docs/skills/tags.md` — computed at
  generation/update time, not hand-maintained — and doesn't count
  toward this scoping test. Without that exclusion the test is a no-op
  on a project where a domain-wide tag sits on nearly everything (this
  repo's own `kms` tag is on all 42 decisions today); with it, bounded
  by non-umbrella tag-cluster size instead of total corpus size.
- No physical directory reorganization (e.g. topic subdirectories under
  `docs/decisions/`) — considered and declined; see "Why".

To avoid three near-identical copies of "how to check/propose tags"
across `bootstrap`/`capture`/`roadmap`: the schema-level fact (a
`tags.md` file may exist; check it before assigning a tag) is added as
one clause to `plugins/kms/shared/artifact-model.md`, already read via
sibling-reference by `bootstrap` and `capture`
(`docs/decisions/0034-shared-artifact-model.md`) — both inherit the
behavior with zero new duplication. `roadmap` doesn't read that shared
file (`0034` deliberately scoped it out, since `roadmap` already
restates only the narrow slice it needs, e.g. `track`, rather than the
full schema) — it gets one matching sentence directly in its own body
instead, the same terse, self-contained style it already uses for
role-list checking.

## Why

A controlled vocabulary is what makes the scoped contradiction check
(and tag-based discovery generally) actually work — uncontrolled free
text drifts into synonyms (`auth`/`authn`/`authentication`) that
silently fragment tag-based clustering right when a growing project
needs it most. Detection has to be an explicit required step, not an
assumption that whichever skill is writing an artifact will happen to
notice a new topic needs a new tag on its own; that mirrors check 14's
explicit "role gone cold" algorithm rather than the vaguer "propose
tags when needed" this decision's own earlier draft left underspecified.

The full-repo O(n²) contradiction scan `0040` shipped was designed
without this scale question in view: at 40 decisions the ~780 pairs
(C(40,2)) are nothing, at 400 the ~80,000 pairs (C(400,2)) aren't
something an LLM-driven semantic comparison can run per `lint`
invocation. Tag-scoping — now that tags are controlled, not free text —
bounds the check by tag-cluster size instead, provided the shared tag
actually discriminates. Checked against this repo's own 42 decisions
during the interview: every one of them carries `kms`, so "share a tag"
alone would still compare the full corpus — the umbrella exclusion
above isn't a refinement, it's load-bearing; without it, tag-scoping
degenerates back to exactly the O(n²) cost it exists to avoid, on
exactly the kind of project (many decisions, a common domain tag) this
decision targets.

No directory reorganization, because the index (`docs/decisions/0041-...`),
tag vocabulary, and archive together already solve what subdirectories
would: the index gives a scannable table of contents, controlled tags
give filterable topic clusters, archiving shrinks the live set.
Physical subdirectories would additionally move numbering from a simple
per-directory file count to a global or cross-directory scheme — a
wider blast radius across every skill that assigns an id, in every
project that adopts `kms`, not just this repo — for browsability the
other three mechanisms already deliver. This is the same cost/benefit
call `docs/decisions/0037-plans-not-a-governed-artifact-type.md` already
made for `docs/plans/`, applied consistently here.

## Tradeoffs considered

- **Free tagging + periodic `lint` consolidation** instead of a
  controlled list: less ceremony per write, but drift still accumulates
  between `lint` runs rather than being prevented at the source.
- **Namespaced/hierarchical tags** (`area:auth`, `kind:security`): more
  expressive and machine-filterable, but a bigger schema change and a
  steeper convention for every artifact author to learn, for a benefit
  this project's actual tag usage doesn't yet demonstrate a need for.
- **Tag-scoped plus a periodic full O(n²) sweep**: catches a
  cross-topic contradiction that never shared a tag, at the cost of
  running the expensive check anyway on some cadence — deferred; add
  later if tag-scoping is found to be missing real contradictions in
  practice.
- **No umbrella-tag exclusion**: a simpler rule ("share any tag"), but
  verified empirically to be a no-op on this repo's own decisions (all
  42 share `kms`) — the scoping would add bookkeeping for zero benefit
  on exactly the corpus it's meant to help.
- **Extend the sibling-reference relationship to `roadmap` too**,
  rather than one restated sentence: zero duplication at all, but
  reopens `0034`'s deliberate boundary for one clause's worth of
  savings — not worth revisiting that boundary at this scale.
- **Subdirectories by tag/topic**: better for browsing a file tree by
  hand, but the numbering-scheme change costs more than the index/tags/
  archive combination already delivers for the same problem.
- **Chosen: a generated, `lint`-enforced canonical tag list with
  explicit write-time detection; tag-scoped contradiction checking; no
  directory reorganization.**
