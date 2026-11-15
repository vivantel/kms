---
id: 0076-admission-reconciled-with-existing-rules
title: Reconcile the admission test with the rules it contradicts
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

1. An incident-grounded fact is admitted when a guardrail cites it in `grounded-in`, and retires with that guardrail, not before. For `version-bump-requires-changelog-entry` take the cheaper branch: `governed-by: [0050]`, no `grounded-in`, derivation-note naming 0050; fact 0013 stays archived.
2. `accepted-by` is the one field that may name a person, because it records accountability; it may hold a role or team instead.
3. "Carried" per 0071: a fact cited by a decision is not carried by its citer.
4. Legacy records predating the admission test are not split retroactively and `lint` does not flag them; the one-claim gate applies to new and re-derived records.

Sentences 2 and 4 are the adopter-facing text for `admission.md`; 1 and 3 tidy kms's own corpus.

## Why

0015 (active) says a one-time observation that grounds a guardrail is exactly what the system wants; 0065 (active) says reject a raw reading or timestamped event; 0066 then deprecated fact 0013, 0015's archetype and the sole `grounded-in` of `version-bump-requires-changelog-entry`. Admission says "name a role or system, not a person" while `accepted-by` holds a person's name. Gate 1's "carried in a sibling record" collides with the requirement that a fact be cited. 0066 concedes 27 legacy records bundle several claims and gives adopters no guidance.

## Tradeoffs considered

- **Re-admit fact 0013**: partly reverses 0066.
- **Chosen: point 1's cheaper branch.**

## Dispositions

0015 amended (point 1). 0065 amended (points 2 to 4). 0066 left active. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.6 (carries consolidation B2).
