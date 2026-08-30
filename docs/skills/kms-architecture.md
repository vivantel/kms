---
id: kms-architecture
title: How kms's own layers, marker conventions, and skills fit together
status: active
date: 2026-08-30
tags: [kms, knowledge-management, procedural]
---

## The four layers

- **`docs/{facts,decisions,guardrails,skills}/`** — this repo's own internal knowledge base. Dogfooded via `bootstrap`/`capture`/`lint`, never shipped to an adopting project.
- **`plugins/kms/skills/`** — the packaging layer: one `SKILL.md` (+ `examples.md`, optional `agents/*.yaml`) per shipped skill. Governed by `AGENTS.md`/`CONTRIBUTING.md` for `kms` contributors, out of `lint`/`capture`'s scope (`docs/skills/scoping-shipped-vs-repo-rules.md`).
- **`plugins/kms/templates/<artifact-type>/`** — shippable product assets, distinct from this repo's own `docs/`. `bootstrap` seeds them into an adopting project's `docs/<artifact-type>/`; `lint`/`capture` keep them synced afterward (`docs/decisions/0027`, `0028`).
- **`plugins/kms/hooks/`** — automation shipped with the plugin itself (e.g. the `capture` nudge), auto-activated on install, never written into an adopting project's own repo.

For the 4-artifact-type model itself (fact/decision/guardrail/skill prescription, their fields, the derivation recipe) — see `bootstrap` or `capture`'s own `SKILL.md`, not repeated here; both already carry it in full since each must be self-sufficient at runtime (`docs/decisions/0016`).

## Marker conventions (in an adopting project's own docs/)

- **`kms-seeded: true` + `kms-template-version: N`** — this file was copied from `plugins/kms/templates/<type>/`; `N` tracks that specific template's own version, not the plugin's overall release. `lint`/`capture` sync it (add/update/remove); deleting both fields permanently detaches it as project-owned.
- **`kms-generated: true`** — `bootstrap` constructed this file from project-specific analysis (no template exists to compare against): `docs/skills/{product,process}-track-roles.md`, `docs/facts/docs-manifest.md`.
- **`<!-- kms:start -->`/`<!-- kms:end -->`** — marks the section `bootstrap` inserted into the project's own `AGENTS.md`/equivalent, pointing at its knowledge base.

`uninstall` is what finds and removes/detaches all three, plus any still-`status: draft` decision or `governed-by: TBD` fact nobody acted on.

## Which skill does what

`bootstrap` sets a project up once. `capture` turns a session's work into decisions/facts. `lint` validates the whole knowledge base, on demand, and owns everything not genuinely session-scoped. `conform` checks a pending changeset against existing guardrails — the only skill that reads code/content outside `docs/` and compares it to the KB, rather than validating the KB itself. `query`/`onboard` read and answer; `roadmap`/`refactor-plan`/`brainstorm` plan; `attribute`/`changelog` write commit history; `uninstall` reverses `bootstrap`.
