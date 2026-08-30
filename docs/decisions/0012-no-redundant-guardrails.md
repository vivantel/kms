---
id: 0012-no-redundant-guardrails
title: A guardrail must not be a pure restatement of one skill's own procedure
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

A guardrail is invalid if it only ever applies "whenever skill X does
Y," with no claim broader than that skill's own procedure — the content
belongs in skill X's `SKILL.md` body, which already states it, and a
second file restating it is dead weight that can drift out of sync.

Applying this test to the 8 guardrails that existed before this
decision:

- **Deleted** — `clarify-option-formatting.md`,
  `commit-attribution-format.md`. Both were scoped explicitly to "whenever
  the `<skill>` skill does X"; their own governing decisions establish
  this as skill-invocation-scoped policy with no broader, system-wide
  form to reword into.
- **Reworded** — `guardrail-derivation-fields.md`,
  `fact-governance-fields.md`. Both were scoped to "the file `bootstrap`
  or `steward` writes or updates," even though `0009`'s own rationale
  treats these fields as extending the repo's general artifact format —
  a genuine system-wide invariant, not `bootstrap`/`steward`-only
  behavior. Reworded to drop the skill-name scoping instead of deleting.
- **Unchanged** — `guardrail-re-derivation-on-source-change.md` and
  `decision-track-field.md` were already worded as system-wide
  invariants; `agent-agnostic-skill-content.md` and
  `plugin-manifest-version-sync.md` don't restate any skill's own
  procedure at all.

`steward` now checks for this on every pass, and checks it before
writing a new guardrail too — see its `SKILL.md`.

## Why

This is the same anti-pattern already fixed once this session for
`docs/skills/{attribute,changelog}-skill-behavior.md` — a shipped
`SKILL.md` is the spec; a second file restating it provides no
enforcement value beyond what's already there. It applies to guardrails
too, and it's `kms` itself (via earlier `roadmap`/`bootstrap` work) that
created these — exactly the clutter `bootstrap`/`steward` must not leave
behind in a target repo either, since that's the entire premise these
two skills ship on.

The reworded pair, `guardrail-derivation-fields.md` and
`fact-governance-fields.md`, aren't the same failure: the *policy* they
state was always meant to be a repo-wide invariant (any guardrail/fact
file, hand-written or not), only the *wording* accidentally scoped it to
two specific skills. Rewording preserves the real, non-redundant claim;
deleting them would have thrown out a legitimate guardrail along with
the redundant ones.

## Tradeoffs considered

- **Delete all four**: simpler, one rule ("guardrail restates a skill →
  delete"), but throws away two guardrails whose underlying policy is
  genuinely system-wide — just worded badly.
- **Reword all four**: the other two (`clarify-option-formatting`,
  `commit-attribution-format`) have no legitimate system-wide form to
  reword into — their governing decisions establish the policy as
  skill-invocation-only, so a "generalized" version of them would
  misstate the actual policy.
- **Chosen: delete the two with no legitimate general form, reword the
  two that do.**
