---
id: 0033-kms-architecture-doc
title: Add a single reference doc synthesizing kms's own layers and marker conventions
status: active
date: 2026-08-30
tags: [kms, knowledge-management, documentation]
track: process
---

## Decision

Add `docs/skills/kms-architecture.md`: one reference doc synthesizing
`kms`'s own internal layering — `docs/{facts,decisions,guardrails,
skills}/` (this repo's internal process knowledge, dogfooded, never
shipped) vs. `plugins/kms/skills/` (packaging) vs.
`plugins/kms/templates/` (shippable product seed content) vs.
`plugins/kms/hooks/` (automation) — and the marker conventions
(`kms-seeded`, `kms-template-version`, `kms-generated`,
`<!-- kms:start/end -->`) in one place. It points at `bootstrap`/
`capture` for the 4-artifact-type model (fact/decision/guardrail/skill
prescription) rather than re-explaining it — that's already duplicated
there by design (`docs/decisions/0016`), and doing it a third time would
just be a third copy to keep in sync. `AGENTS.md` gets one line pointing
to it, matching how it already points at
`docs/skills/adding-agent-support.md` and
`docs/skills/scoping-shipped-vs-repo-rules.md` instead of inlining them.

## Why

This knowledge already exists, but only in pieces: `AGENTS.md`'s
"Structure" section gives file paths and one-line comments, not a
connected explanation of why the layers are split the way they are;
the actual reasoning is scattered across roughly six decisions
(`0018`, `0026`-`0029`) and one narrow procedural doc
(`docs/skills/scoping-shipped-vs-repo-rules.md`, which covers only the
shipped-vs-repo-rule question, not the full picture). Reconstructing
"how does kms actually fit together" today means reading all of that
in sequence. That gap became concrete while explaining this exact
question mid-session — worth capturing once, durably, rather than
re-deriving it from decisions again next time someone asks.

## Tradeoffs considered

- **Expand `AGENTS.md` itself with a full architecture section** instead
  of a separate file: keeps everything in the one place agents are
  guaranteed to load, but `AGENTS.md` is meant to stay economical
  (`docs/guardrails/token-economy.md` applies to it via
  `AGENTS.md`'s own "Adding a new skill" section), and a full layer-by-
  layer walkthrough doesn't fit that bar. Rejected — matches the
  existing pattern of pointing at `docs/skills/*.md` for depth instead
  of inlining it.
- **Duplicate the 4-artifact-type model here too**, for a fully
  self-contained architecture doc: this is a `kms`-internal reference,
  not a shipped skill loaded independently at runtime — the
  self-sufficiency argument that justifies duplicating that model into
  every shipped skill (`docs/decisions/0016`) doesn't apply to a doc
  that's always read alongside the rest of this repo. Rejected; points
  at `bootstrap`/`capture` instead.
- **Chosen: one new `docs/skills/kms-architecture.md`, pointed to from
  `AGENTS.md`.**
