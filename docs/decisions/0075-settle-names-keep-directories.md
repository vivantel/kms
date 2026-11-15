---
id: 0075-settle-names-keep-directories
title: Settle the artifact names without renaming directories
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

Keep `docs/skills/` as the procedure directory. Fix the index title to "Procedures index". Purge "intent", "skill prescription", "steward" and "fact/decision/guardrail/skill" from shipped bodies, from the `description` frontmatter of `lint`, `bootstrap` and `query` (keeping their trigger phrases otherwise), and from the bootstrap AGENTS.md block, in favour of fact, decision, guardrail, procedure. Rename the guardrail `decision-expires-must-be-reevaluated` to `artifact-expires-must-be-reevaluated` (guardrails are refined in place; referrers are updated; decisions keep the old id as history). The directory rename is deferred, trigger: a second adopting project asks.

## Why

The type is "Procedure" in the model, `docs/skills/` on disk, "Skills index" in the index, `procedural` as tag, "skill" in bootstrap and README, "skill-prescription artifacts" in 0013, "intents" in bootstrap, "knowledge-steward-style" in `roadmap` (0031 renamed steward to capture). A directory rename would leave every adopter's immutable decisions citing stale paths forever and add permanent two-layout detection; kms's own tree has 43 such references outside `docs/plans/`.

## Tradeoffs considered

- **Rename `docs/skills/` to `docs/procedures/`**: rejected, see Why.
- **Chosen: keep the directory, fix the words.**

## Dispositions

0001 and 0031 left active. Check after 2.9: `grep -nE "knowledge-steward|skill prescription|fact / intent|fact/decision/guardrail/skill" plugins/kms/skills/*/SKILL.md plugins/kms/shared/*.md` returns nothing. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.5.
