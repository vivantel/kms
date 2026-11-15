---
id: 0074-registries-by-marker
title: Registries are identified by marker; the fitness-function inventory lives on decisions
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

1. A declared non-governed file class, **registry**, is identified by `kms-registry: <name>` in frontmatter (or `<!-- kms-registry: <name> -->` as the first line of a pure CSV). Registries are excluded from the four types' checks and from Admission, included in the sync checks (19 indexes, 21 tags), and listed by `uninstall` under one category. Existing files stay where they are: `INDEX.md`, `docs/skills/tags.md`, the role lists, `docs/facts/docs-manifest.md`.
2. The fitness-function inventory is the union of decisions' `fitness-functions` lists. Each entry is a map `{check: <text>, enforced-by: <code path | ci job | hook | procedure id | none>, last-verified: <date>}`. `capture` check 3 and `bootstrap` step 5 append to the governing decision's list, or draft a `status: draft` decision stub when no decision governs the rule.
3. `last-verified` is defined once (0071) and the docs manifest uses the same word.
4. Marker forms: a frontmatter field where frontmatter exists, a first-line comment otherwise; `kms-seeded`, `kms-generated`, `kms-registry`.

## Why

Files that are not instances of any type sit in the type directories: every `INDEX.md`, `docs/skills/tags.md` (a vocabulary filed as a procedure), the role lists, and `docs/facts/docs-manifest.md` (an un-numbered fact that passes the checker only because fields were added by hand). The "fitness-function inventory" is written by `bootstrap` step 5 and `capture` check 3 and exists nowhere; lint check 18 reads only the field on decisions. The `kms-seeded`/`kms-generated` markers take two forms and the model mentions neither.

## Tradeoffs considered

- **New directory or files for registries**: churn for adopters with no gain.
- **Chosen: marker-identified registries in place.**

## Dispositions

0049 left active (indexes are registries; format unchanged). 0013 amended (role lists are registries, proposal-only per 3.6). 0029 amended (docs manifest is a registry). 2.9 updates `bootstrap` 3/5/7/10, `capture` 3/5/7, `lint` 18/19/21, `uninstall`, `query` and `onboard` index reads. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.4.
