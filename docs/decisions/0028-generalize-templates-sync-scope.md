---
id: 0028-generalize-templates-sync-scope
title: Generalize the templates sync mechanism from guardrails-only to any artifact type
status: active
date: 2026-08-30
tags: [kms, knowledge-management, packaging]
track: process
---

## Decision

`bootstrap`/`steward`/`lint`'s baseline-artifact-sync mechanism
(`docs/decisions/0027-baseline-guardrail-seeding.md`) generalizes from
hardcoding `plugins/kms/templates/guardrails/` and `docs/guardrails/`
specifically, to scanning every subdirectory of `plugins/kms/templates/`
and mapping each `<type>/` to the matching `docs/<type>/` in the target
project. `guardrails/` is the only subdirectory that exists today; the
mechanism no longer assumes it's the only one that ever will.

Once a template is seeded into a project, it's a normal artifact in
that project's own `docs/<type>/` — a guardrail, or whatever type —
traceable back to `kms` only via its `kms-seeded`/`kms-template-version`
frontmatter, not by living in any "templates" location itself.

## Why

This was going to be needed the moment `kms` shipped a second template
type, and building the new `uninstall` skill
(`docs/decisions/0030-uninstall-skill.md`) as a true inverse of
`bootstrap` surfaced exactly that need immediately — `bootstrap` was
about to grow `kms-generated` (non-template, per-project) artifacts
alongside `kms-seeded` (template-copied) ones, and hardcoding
"guardrails" into three already-shipped skills would have meant
touching all three again for every future artifact type.

## Tradeoffs considered

- **Leave it guardrails-only, generalize later if a second type ships**:
  less work now, but this exact rework was already needed one
  design-conversation later. Rejected — chosen explicitly over this
  option when interviewed.
- **Chosen: generalize now, across `bootstrap`/`steward`/`lint`.**
