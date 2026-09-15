---
id: 0034-shared-artifact-model
title: Extract the shared artifact-type model into one file, read by sibling reference
status: active
date: 2026-08-30
tags: [kms, knowledge-management, packaging]
track: process
---

## Decision

`bootstrap` and `capture` both fully restated the same fact/decision/
guardrail/skill-prescription field model — base frontmatter, type-specific
fields, the derivation recipe — worded slightly differently, and already
caught drifting once. That model moves to
`plugins/kms/shared/artifact-model.md`; both skills now read it via a
sibling-relative reference ("this skill's sibling
`../../shared/artifact-model.md`"), the same mechanism `bootstrap`/
`capture`/`lint` already depend on for `../../templates/`.

## Why

`docs/decisions/0016-lint-skill.md` chose full duplication over
cross-referencing specifically because sharing content meant an agent
taking an extra, unproven read step at runtime. That's no longer true —
this plugin's own templates-sync mechanism
(`docs/decisions/0027-baseline-guardrail-seeding.md`,
`docs/decisions/0028-generalize-templates-sync-scope.md`) already
depends on exactly that kind of sibling-directory read, reliably, across
`bootstrap`, `capture`, and `lint`. Once a real precedent exists for
"read a sibling file at runtime" working, continuing to fully duplicate
this specific model — rather than a check's own logic, which still has
good reason to stay inline (`docs/decisions/0031`) — was paying the
duplication cost for no remaining benefit. `roadmap` doesn't restate
this same model (it only needs numbering/classification, not the field
schema), so this was specifically a two-file, not a plugin-wide, problem.

## Tradeoffs considered

- **Keep full duplication, matching `0016`'s original reasoning**: the
  safest option when that decision was made, but the platform
  assumption behind it no longer holds, and this session already paid
  the cost once (a wording drift between the two copies).
- **Extract it into `docs/skills/kms-architecture.md`** (the new
  contributor-facing reference doc) instead of a new file: keeps one
  fewer file, but conflates a *contributor* reference (how kms's own
  layers fit together) with *runtime-operational* content
  `bootstrap`/`capture` need mid-invocation in an arbitrary adopting
  project — different audiences, different lifecycle. Rejected.
- **Chosen: a new `plugins/kms/shared/artifact-model.md`, read via the
  same sibling-reference pattern already proven for `templates/`.**
