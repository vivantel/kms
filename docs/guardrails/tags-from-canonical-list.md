---
id: tags-from-canonical-list
title: Any artifact's tags must come from the canonical tag list, when one exists
status: active
date: 2026-09-01
tags: [kms, knowledge-management, guardrail]
governed-by: 0042-tag-vocabulary-and-scoped-contradiction-check
grounded-in: TBD
derivation-note: >
  Given decision 0042 (a canonical tag vocabulary exists so tag-scoped
  checks and discovery work), any artifact's tags must be drawn from
  that list once one exists, whoever wrote the file.
---

## Guardrail

When `docs/skills/tags.md` exists, any fact, decision, guardrail, or
procedure file's `tags` MUST all be entries from that list — whether the
file was written by `bootstrap`/`capture`/`roadmap` or by hand. A tag
found that isn't on the list MUST be flagged as debt: either the list is
missing a genuinely new tag (propose adding it, with a one-line meaning)
or the file should use an existing tag instead of a near-duplicate.

## Derivation

- **Axiomatic basis**: `docs/decisions/0042-tag-vocabulary-and-scoped-contradiction-check.md`
  — the team committed to a controlled tag vocabulary so tag-based
  clustering (discovery, and the scoped contradiction check) stays
  meaningful as the knowledge base grows.
- **Descriptive basis**: `docs/decisions/0001-knowledge-artifact-storage-convention.md`
  establishes the base `id/title/status/date/tags` frontmatter this
  guardrail's field constrains.
- **Normative conclusion**: therefore any of the four governed types'
  `tags` are checked against `docs/skills/tags.md` when it exists,
  regardless of how the file was written, matching `lint`'s tag check.
