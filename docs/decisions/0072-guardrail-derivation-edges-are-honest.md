---
id: 0072-guardrail-derivation-edges-are-honest
title: Guardrail derivation edges are lists of decisions plus optional fact grounding
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
---

## Decision

`governed-by` on guardrails becomes a list of one or more decision ids, each resolving to a non-superseded decision (re-pointed in the same edit that supersedes the old one; `capture` check 1 does this). `grounded-in` becomes optional and fact-only; absent means "a direct consequence of the governing decision(s)". `derivation-note` must name every id in the two edges; it may be `TBD` only while `governed-by` is `TBD` (seeded templates). Retired source rule: a deprecated `grounded-in` fact or superseded `governed-by` decision triggers re-derivation in the same pass: re-point and note "re-derived <date> from <id>" if the consequence stands, else deprecate the guardrail. `governed-by` is optional on procedures. A second governing decision is a second list entry. Templates ship `governed-by: TBD`, no `grounded-in`, `derivation-note: TBD`; `template-version` stays 1 (the migration rewrites seeded files' frontmatter; check 12 is unchanged).

## Why

The model says a guardrail derives from a commitment plus a descriptive fact and is valid only while its sources are current, but `grounded-in` may hold the same id as `governed-by` (0051). Of 17 live guardrails, 6 are "grounded" in `0001-knowledge-artifact-storage-convention` as filler, 3 in their own `governed-by`, 3 in facts now deprecated, 1 is `TBD`, and only 2 rest on live independent facts. The flagship `ARCHITECTURE.md` example has both sources retired and is still `active`. `governed-by` is scalar while `plugin-manifest-version-sync` has two governing decisions. Nothing says what a guardrail does when its decision is superseded. Procedures created by 0013 and 0042 have no `governed-by`.

## Tradeoffs considered

- **Keep 0051 and add a check for filler**: leaves two meanings in one field.
- **Chosen: list-valued `governed-by`, fact-only optional `grounded-in`.**

## Dispositions

0051 superseded by this decision. 0039 amended (`superseded-by` scope, see 2.3). 0027 and 0045 left active; the template frontmatter change is an amendment to 0027. The 17 guardrails' new edges are filled in 2.10. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.2.
