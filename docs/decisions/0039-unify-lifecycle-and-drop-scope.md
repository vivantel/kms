---
id: 0039-unify-lifecycle-and-drop-scope
title: Unify status and expires across all four artifact types; add superseded-by; drop scope
status: active
date: 2026-09-01
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

The lifecycle dimension is unified across all four governed types
(facts, decisions, guardrails, procedures):

- **`status`** becomes one shared enum: `draft | active | superseded |
  deprecated`. This narrows
  `docs/decisions/0014-decision-scope-and-expires-fields.md`'s treatment
  of decision status and extends the same enum to facts/guardrails/
  procedures, replacing the ad hoc values in use today (`accepted`,
  `current`).
- **`expires`** (a date, or a condition) extends from decision-only
  (`0014`) to all four types, semantics unchanged: when it stops being
  current.
- **`scope`** (free text, "what this applies to," `0014`) is dropped
  entirely — decision-only, optional, and unused by every one of the 36
  decisions that existed when this decision was made. What a decision
  applies to belongs in its own prose.
- Decisions additionally carry **`superseded-by: <decision-id>`**,
  required exactly when `status: superseded`. This is decision-only: per
  `plugins/kms/shared/artifact-model.md`'s own table, decisions are the
  only type immutable once accepted, and therefore the only type
  actually superseded by a sibling file rather than refined in place.

Retrofit of the 44 existing artifacts affected: 35 decisions
(`status: accepted` → `active`), 1 decision
(`docs/decisions/0006-agent-agnostic-scope.md`:
`status: superseded by 0008-native-codex-plugin-support` →
`status: superseded` + `superseded-by: 0008-native-codex-plugin-support`),
8 facts (`status: current` → `active`). The 13 guardrails and 4
`docs/skills/` procedures already use `active` and need no change. Plans
are unaffected — `docs/decisions/0037-plans-not-a-governed-artifact-type.md`
excludes them from this lifecycle model entirely; their own per-step
legend is untouched.

## Why

`status` had drifted into three different vocabularies doing the same
job — decisions said `accepted`, facts said `current`, guardrails/
procedures already said `active` — with no way to tell, short of
reading each type's own convention, whether two files in different
states or the same state. A shared vocabulary makes that legible at a
glance across the whole knowledge base, and reuses `active` (already the
majority usage, 17 of 61 status-bearing files) rather than inventing a
fourth term.

`expires` generalizing follows the same logic that motivated it for
decisions in `0014`: a fact, guardrail, or procedure can just as easily
be bounded or provisional (a fact about a third-party API's current
rate limit, a guardrail derived from a time-boxed decision, a procedure
for a migration window) — restricting it to decisions was an artifact of
`0014` only having decisions in view at the time, not a reason specific
to decisions.

`scope` is dropped on evidence, not principle: it was designed for the
bounded/provisional decision case, and zero artifacts ever used it
across this repo's full history. Carrying an unused optional field is
dead weight in the model with nothing to show for it; if a genuine need
resurfaces, prose in the decision's own body already covers it, and a
field can be reintroduced with a real example driving its shape.

`superseded-by` fixes a concrete inconsistency the new `status` enum
would otherwise be broken by on day one: `docs/decisions/0006` already
encodes its supersession as free text glued onto `status`
(`superseded by 0008-...`), which is illegal under a strict 4-value
enum. Making it a real field — decisions-only, matching decisions'
unique immutability — fixes that file and gives `lint`/`query` a
structural pointer instead of prose to parse. `query`'s own check 3 ("if
a decision has been superseded, cite the superseding one too") gets more
reliable as a direct consequence.

## Tradeoffs considered

- **Per-type status enums** instead of one shared vocabulary: more
  precise per type, but five vocabularies to remember and lint instead
  of one, for a distinction (draft/active/superseded/deprecated reads
  fine for a fact or a procedure too) that doesn't actually need
  type-specific values.
- **Leave `status` as free text, just add an allow-list lint check**:
  cheapest to ship, but leaves today's inconsistency (`accepted` vs.
  `current` vs. `active`) uncorrected rather than actually unified.
- **Keep `expires`/`scope` decision-only**: no retrofit needed, but
  leaves facts/guardrails/procedures with no way to say "this stops
  applying at X" short of going stale silently — the same gap `0014`
  closed for decisions, just left open for the other three types.
- **`superseded-by` on all four types, matching `status`/`expires`'s
  generalization**: rejected specifically — facts/guardrails/procedures
  are refined in place (per `artifact-model.md`'s own "can be refined"
  vs. decisions' "immutable once accepted"), so they structurally never
  get superseded by a new sibling file; only decisions do.
- **Chosen: one shared `status` enum and generalized `expires` across
  all 4 types; `scope` dropped; `superseded-by` added to decisions
  only.**
