---
id: 0066-corpus-cleanup-under-admission-test
title: Six facts that fail the admission test are deprecated; the other contested records stay
status: draft
date: 2026-11-08
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

Decision 0065 applies the admission test to new records. This decision applies it once to the 98 active artifacts and changes the state at tag `study-v1` (b517c52) as follows. Six facts that two independent raters both failed are set to `status: deprecated` and moved to `docs/facts/archive/`: `0001-kms-skill-names`, `0002-skill-bodies-already-agent-neutral`, `0004-kms-skill-names-steward-bootstrap`, `0005-vivantel-kms-display-name`, `0013-changelog-lagged-four-version-bumps`, `0014-guardrails-carry-derivation-prose`. They are archived, not deleted, because live guardrails and decisions cite them and lint check 1 would otherwise flag dangling references. `fact-governance-fields` drops the `derived` and `mixed` kinds that decision 0064 removed. `no-unenforced-guardrail` cites fact 0008 instead of the decision that seeded it. Nothing else is changed.

## Why

Two fresh model raters (agreement 81 of 98, kappa 0.69) failed 6 records in both readings, all facts: names visible in directories, or dated readings that sit in history. Under the earlier wording of the guardrail criterion, 20 failed in both; the reworded criterion (enforcement alone is not a failure) removed all guardrail and decision failures. Rater verdicts are in the author's repo, `docs/plans/knowledge-boundary/step6b/`.

## Tradeoffs considered

- **Delete instead of archive:** cleaner, but three guardrails and decision 0050 cite these facts, so deletion breaks derivations.
- **Keep every contested record:** 27 records were contested by both raters, mostly decisions that bundle several claims (0039, 0040, 0042 hold four each). Splitting them rewrites history-bearing records and renumbers references; the admission test governs new records. They stay and are counted as a limitation.
- **Lint-check mirrors** (`lifecycle-status-values`, `tags-from-canonical-list`): lint check 5 defines a redundant guardrail as true only while one skill runs, which these are not, and `lifecycle-status-values` adds the plans exemption lint does not state. Kept.
- **Seeded templates** (`kms-seeded`): the circular derivation was in kms's own copy, not the template (whose derivation is a `TBD` placeholder), and lint check 12 syncs only the Guardrail section, so the template is unchanged. Removing them would contradict decision 0027.

## Limits

Model raters, one family. The effect of the cleanup on evals that read the knowledge base (lint, query) is not separated here; run those on `study-v1` and on this state before attributing a change to the rule.
