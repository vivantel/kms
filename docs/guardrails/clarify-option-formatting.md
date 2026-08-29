---
id: clarify-option-formatting
title: clarify's discrete-option questions must avoid numbering collisions and duplicate free-text slots
status: active
date: 2026-07-29
tags: [kms, clarify, interview, guardrail]
---

## Guardrail

Whenever the `clarify` skill (or `roadmap`, which shares its interview
style) presents a decision as a list of discrete options, it MUST:

1. Cap the list at 4 entries total, including any free-text catch-all.
   If more genuine options exist than fit, merge the most similar/adjacent
   ones rather than exceeding the cap or dropping the free-text slot.
2. Skip the list entirely when the decision's natural answer is itself a
   number (a count, a date, a size) — ask it as an open question instead,
   optionally suggesting a default. Plain-number answers collide with
   plain-number option labels otherwise.
3. When a selectable-question tool is available, use it and rely on its
   own built-in free-text/"Other" option — never add a second
   "something else" entry, and never number the options manually (the
   tool renders its own).
4. When no such tool is available, number each real option with plain
   digits, then append exactly one final numbered option inviting a
   free-text answer — never both an in-list "something else" option and
   a separate "type your own" option.

## Derivation

- **Descriptive basis**: observed failures where a numeric decision (time
  per week) was rendered as 5 numbered options — one over the cap — and
  where a tool-rendered question duplicated its free-text option (a
  manual "something else" plus the tool's own "Other").
- **Normative conclusion**: therefore `clarify`'s (and `roadmap`'s)
  option-list rendering must apply the cap-with-merge rule, the
  numeric-answer carve-out, and the single-free-text-slot rule
  consistently, whichever rendering path (tool or plain text) is active.
