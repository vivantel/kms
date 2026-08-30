---
id: 0010-decision-track-field
title: Add a track field (product | process) to decisions
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Every decision carries a required `track` field: `product` or `process`.

- **`product`** — decisions about what kms is for and who it serves:
  mission, scope, target agents, target domains.
- **`process`** — decisions about how kms is built, organized, formatted,
  or shipped: which skills exist, file formats, packaging, naming,
  contribution mechanics.

New decisions declare `track` from the start. The 9 existing decisions
are retrofitted (see
`docs/plans/product-process-track-and-domain-agnostic-scope.md`):

- `product`: `0006-agent-agnostic-scope`, `0008-native-codex-plugin-support`
- `process`: `0001`, `0002`, `0003`, `0004`, `0005`, `0007`, `0009`

## Why

kms's own decision history conflates two different questions: what kms
is for (who it serves, what domains it covers) and how the current skill
set happens to be built. Without a label, a reader can't tell "core
mission commitment" apart from "today's implementation choice" on sight
— e.g. `0009` (splitting bootstrap/steward into two skills) and `0008`
(supporting Codex) read as the same kind of decision, but only one of
them is about who kms serves.

The line drawn here: does the decision change what kms's target
users/domains are (`product`), or does it change how the current skill
set is organized/built to serve that same audience (`process`)? Skill
existence, addition, removal, improvement, and format decisions are
`process` even when significant — only decisions about mission, scope,
or target agents are `product`.

Required rather than optional, matching how `governed-by` is already
required (with `TBD` as declared debt elsewhere) rather than silently
missing — an unlabeled decision is itself a gap worth surfacing, not
something to let slide by default.

## Tradeoffs considered

- **Optional, inferred when obvious**: less friction, but the whole
  point is to stop conflating two kinds of decision at a glance — optional
  means it stays missing wherever it's least obvious, exactly where it
  matters most.
- **Field on facts too, not just decisions**: rejected — many facts
  (e.g. a schema fact) don't cleanly split, and facts already inherit
  relevance from their governing decision.
- **New artifact type, or parallel doc trees for the two tracks**:
  rejected — reuses the existing `docs/{facts,decisions,guardrails,skills}/`
  structure as-is rather than doubling it.
- **Chosen: a required `track` field on decisions only.**
