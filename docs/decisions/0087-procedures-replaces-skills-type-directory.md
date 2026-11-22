---
id: 0087-procedures-replaces-skills-type-directory
title: The procedure type directory is named procedures/; skills/ is read for one release and migrated on request
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-22
tags: [kms, packaging]
---

## Decision

The directory holding procedures is `procedures/`, not `skills/`. For one release `lint_check.py` reads both names (tags list from either, prose references to either), so no existing project breaks. `migrate.py --rename` is opt-in: it moves `skills/` to `procedures/` and rewrites `<dir>/skills/` path mentions inside the knowledge directory; it refuses when both exist. `bootstrap` creates `procedures/` for new projects. This repo's own `docs/skills/` stays where it is (it is read through the compatibility path and is not a new adopter), so there is one documented exception.

## Why

"Skill" means an agent skill; a first-time reader of `docs/skills/` met the word with two meanings in the 2026-11-22 cold starts (two reports). Renaming costs more with every adopter, so it ships with decision 0086's path change, in one release.

## Tradeoffs considered

- **Keep `skills/`**: no work, but the vocabulary clash stays and the cost of fixing it later grows.
- **Rename silently on migrate**: rejected; a rename rewrites cross-references and belongs to an explicit flag.
- **Move this repo's `docs/skills/` too**: touches many cross-references for no adopter benefit.
- **Chosen: both names read for one release, rename opt-in.** Support for `skills/` ends in the release after.
