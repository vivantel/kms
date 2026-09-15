---
id: 0051-grounded-in-may-hold-a-decision
title: A guardrail's grounded-in may point at a decision or guardrail, not only a fact
status: active
date: 2026-09-12
tags: [kms, knowledge-management, taxonomy, guardrail]
track: process
---

## Decision

`grounded-in` may hold a decision or guardrail id, not only a fact id,
when a guardrail's real descriptive basis is one of those rather than an
independent "what's currently true" fact — including the *same*
decision already named in `governed-by`, when the guardrail is a direct,
unmediated consequence of that decision with nothing in between.
`plugins/kms/shared/artifact-model.md` and `lint` checks 1/2/13 are
updated to resolve and accept any of the three id shapes.

Applied to the 14 guardrails that had sat at `grounded-in: TBD` since
the project's earliest days — archaeology (each file's own `##
Derivation` prose already stated a real basis, just never copied into
the structured field) resolved 13:

- **7 cite a different decision** than their own `governed-by`:
  `lifecycle-status-values.md`, `superseded-decision-requires-pointer.md`,
  `tags-from-canonical-list.md`, `decision-expires-must-be-reevaluated.md`,
  `decision-track-field.md`, `fact-governance-fields.md` (all →
  `0001-knowledge-artifact-storage-convention.md`), and
  `no-redundant-guardrails.md` (→ `0012-no-redundant-guardrails.md`).
- **2 ground in a sibling guardrail**: `fact-not-audit-log.md` (→
  `fact-governance-fields.md`) and `guardrail-re-derivation-on-source-change.md`
  (→ `guardrail-derivation-fields.md`).
- **1 got a genuine new fact**, not a decision/guardrail substitute:
  `guardrail-derivation-fields.md`'s own basis ("this repo's guardrails
  already carry `## Derivation` prose") was a real, currently-true,
  never-written-down observation — written as
  `docs/facts/0014-guardrails-carry-derivation-prose.md`.
- **3 are self-referential** — no second source named anywhere, so their
  own `governed-by` decision is what grounds them: `no-unenforced-guardrail.md`,
  `one-statement-one-job.md` (both `0027`), `token-economy.md` (`0026`).

**1 stays `TBD`**: `every-skill-ships-examples.md` explicitly wants a
future roster *fact*, not a decision or guardrail — forcing a substitute
in would be less accurate than the honest gap.

## Why

`lint` check 13 already anticipated this, worded as "a guardrail
grounded in **a decision** that's since been superseded, or a fact
that's since changed" — the schema never caught up to what the check
already assumed was possible. The derivation recipe (`Decision (why) +
Fact (what is) → Guardrail (ought)`) models the common case, where an
independent, separately-falsifiable fact exists
(`agent-agnostic-skill-content.md`'s pairing with fact `0002` is the
clean example — the fact could become false without the decision
changing). But several of `kms`'s own meta-guardrails rest on another
established norm instead — a decision alone, or a sibling guardrail that
already states the same requirement — with no independent factual claim
in between. Treating whichever of those is actually doing the work as
the ground is more honest than inventing a fact that doesn't exist, or
leaving debt standing indefinitely for something that was never actually
missing.

## Tradeoffs considered

- **Leave all 14 at `TBD` permanently, documented as a known category**:
  cheapest, but leaves `lint` check 17 (stale unresolved debt) flagging
  something that was never really unresolved — it just had nowhere to
  go structurally.
- **Force a fact for each of the 14**: matches the recipe's common case
  exactly, but for at least 9 of them there is no independent
  descriptive claim to write — inventing one would mean storing an
  ungrounded value, the same failure mode
  `docs/decisions/0038-track-field-mutual-exclusivity.md` already argues
  against by analogy, just on the fact side instead of `track`.
- **Chosen: let `grounded-in` hold a decision or guardrail id — including
  self-reference to `governed-by` — reserving `TBD` for the one guardrail
  that genuinely still needs a fact that doesn't exist yet.**
