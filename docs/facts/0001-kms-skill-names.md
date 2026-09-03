---
id: 0001-kms-skill-names
title: Names of the commit/PR attribution and changelog skills
status: active
date: 2026-07-29
tags: [kms, naming]
kind: decision
governed-by: 0002-commit-pr-attribution-skill-design
---

The two skills designed in `docs/decisions/0002-commit-pr-attribution-skill-design.md`
are named:

- `attribute` — directory `plugins/kms/skills/attribute/`, frontmatter `name: attribute`
- `changelog` — directory `plugins/kms/skills/changelog/`, frontmatter `name: changelog`

`commit` / `changelog` was considered for the first skill and rejected as
too literal — it undersells that the skill also writes PR descriptions and
embeds artifact-traceability links, not just commit messages.
