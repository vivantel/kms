---
id: 0038-track-field-mutual-exclusivity
title: track values are mutually exclusive; "both"/"mixed" is never stored
status: active
date: 2026-09-01
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

`track` (`docs/decisions/0010-decision-track-field.md`, decisions only)
always stores exactly one of `product`/`process` — never a literal
`both` or `mixed`. A rollup describing a group of decisions spanning
both tracks (e.g. characterizing a plan by the decisions it implements)
is computed at read time from those decisions' own `track` values; it
is never written into any file's frontmatter as a stored third value.

## Why

`0010` never actually defined a `both` value — it required exactly one
of `product`/`process` — but nothing said so explicitly, and that gap
got a foothold the first time something (a plan) needed to describe a
mix. This decision closes it: `track`'s exclusivity was always the
intent, this makes it the enforced rule, and separates "what a single
decision commits to" (always one track) from "how to summarize several
decisions at once" (a computed rollup, not a new stored value).

## Tradeoffs considered

- **Allow `both`/`mixed` as a literal stored value**: simplest to write,
  but reintroduces the exact non-exclusive enum this decision exists to
  close — and a decision that genuinely spans both tracks is more
  honestly two decisions than one ambiguous one.
- **Leave it implicit, as `0010` did**: costs nothing until the next
  time a rollup is needed, which is exactly how this gap got found the
  first time.
- **Chosen: explicit, enforced exclusivity; rollups are always computed,
  never stored.**
