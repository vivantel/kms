---
id: 0029-bootstrap-full-traceability
title: Make every bootstrap output traceable back to kms, and wire a pointer into the project's own agent-instructions file
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management, packaging]
track: process
---

## Decision

Two additions to `bootstrap`:

1. **AGENTS.md wiring**: `bootstrap` inserts a marked section —
   `<!-- kms:start -->` ... `<!-- kms:end -->` — into the target
   project's `AGENTS.md` (or `CLAUDE.md` if that's what exists;
   creates a minimal `AGENTS.md` if neither does), pointing at
   `docs/{facts,decisions,guardrails,skills}/` and naming `steward`/
   `lint`/`query` as the maintenance/validation/retrieval skills. This
   mirrors how `kms`'s own `AGENTS.md` documents its own knowledge
   system (see this repo's own "This repo dogfoods its own skills"
   README section) — every adopting project gets the same self-
   documentation `kms` gives itself.
2. **`kms-generated: true`** — a new frontmatter marker, parallel to
   `kms-seeded`/`kms-template-version` but for content `bootstrap`
   *constructs from project-specific analysis* rather than copies from
   a static template: `docs/skills/{product,process}-track-roles.md`
   (step 7) and `docs/facts/docs-manifest.md` (step 3). These can't be
   "synced to a newer template version" the way a seeded guardrail
   can — there's no template, just per-project output — but they still
   need to be identifiable as `kms`'s doing.

Both changes exist for one reason: `docs/decisions/0030-uninstall-skill.md`
needs every one of `bootstrap`'s outputs to be findable and reversible,
and two of them — the AGENTS.md wiring and the two dynamically-generated
files — had no marker or trace at all before this decision.

## Why

`bootstrap` already marks decision/fact stubs as debt (`status: draft`,
`governed-by: TBD`) and, since `docs/decisions/0027`, marks seeded
guardrails as `kms-seeded`. Two of its outputs were invisible to any
future cleanup pass: `docs/skills/{product,process}-track-roles.md` and
`docs/facts/docs-manifest.md` carried no marker distinguishing "`kms`
put this here" from "the team wrote this," and nothing pointed a human
or agent working in the target project at the knowledge system's
existence at all — a second person joining the project has no reason to
discover `docs/{facts,decisions,guardrails,skills}/` exists unless they
already know to look. `onboard` addresses this for a specific role
asking for a ramp-up plan; the AGENTS.md pointer addresses it for anyone
just reading the project's own instructions file, the way a `kms`
contributor already gets from `kms`'s own `AGENTS.md`.

## Tradeoffs considered

- **A separate `docs/KMS.md` linked from one line in AGENTS.md**,
  instead of inline markers: cleaner removal (delete one file, one
  line), but adds a second file most projects wouldn't otherwise have.
  Rejected — chosen explicitly over this option when interviewed.
- **No marker for dynamically-generated files, treat them as always
  project-owned**: simpler, but leaves `uninstall` unable to offer
  cleanup for two real `bootstrap` outputs. Rejected.
- **Reuse `kms-seeded` for generated files too**: fewer field names, but
  conflates "copied from a static template, version-comparable" with
  "constructed per-project, no template to compare against" — a real
  semantic difference `uninstall`'s logic depends on. Rejected.
- **Chosen: `<!-- kms:start/end -->` markers for the AGENTS.md section;
  `kms-generated: true` for dynamically-constructed files.**
