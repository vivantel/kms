---
id: 0054-defer-business-domain-dimension
title: Defer a business-domain dimension until kms operates on a real multi-domain monorepo
status: active
date: 2026-09-12
tags: [kms, knowledge-management, scale]
track: process
fitness-functions: ["Once kms is actually installed on a monorepo with multiple weakly-coupled product domains, check whether tags.md's flat clustering is still adequate for query/onboard scoping and check 16's contradiction-scoping, or whether a real domain-boundary field is by then justified by an observed problem, not a hypothetical one."]
---

## Decision

`kms`'s artifact model does not gain a `domain` field now. `tags`
(`docs/skills/tags.md`) remains the only clustering mechanism — flexible,
discovery-oriented, with no hierarchy, no ownership implication, and no
enforced boundary. This is a deliberate scope limit, not an oversight:
logged so a future reader doesn't wonder whether it was missed.

## Why

A `domain` dimension would matter concretely in one scenario: a large
monorepo hosting several weakly-coupled product domains sharing one
knowledge base, where `query`/`onboard`'s index reads
(`docs/decisions/archive/0041-index-and-archive-for-scale.md`, later
`docs/decisions/0049-plain-csv-index-not-toon.md`) stay unscoped by
domain regardless of which product a question concerns, and `lint`
check 16's contradiction-scoping compares across domains that may share
a generic tag without being remotely related. That's the same shape of
problem `0041`/`0042` already solved for *count*-based scale ("hundreds
of artifacts of one type") — a `domain` field would be the sequel for
*breadth*-based scale ("many weakly-related sub-projects in one repo").

`kms` doesn't operate at that scale today (~50 decisions, one product),
so there's no observed problem to design against yet — only a
hypothetical one. Building a domain-boundary mechanism now would repeat
exactly the mistake `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`
already made once with `scope`: a field introduced ahead of a concrete,
demonstrated need, later dropped because nothing ever actually used it.

## Tradeoffs considered

- **Add a `domain` field now, get ahead of the need**: matches how
  `0041`/`0042` were justified (real scale, not hypothetical) only in
  form, not substance — those were built once a concrete cost was
  already being paid; this would be speculative.
- **Rely on tags indefinitely, never revisit**: cheapest, but risks
  silently degrading if `kms` ever is used on a genuinely large,
  multi-domain monorepo, with nobody having flagged that the model's
  assumptions no longer hold.
- **Chosen: stay with tags now; log the trigger condition
  (`fitness-functions`) that would justify revisiting this, so the
  question gets a real answer against real data if it ever comes up,
  not resolved by default through inertia.**
