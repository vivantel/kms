---
id: 0030-uninstall-skill
title: Add uninstall — a manual pre-uninstall step that reverses everything bootstrap adds
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management, packaging]
track: process
---

## Decision

Add `uninstall`, a new skill: run manually, before actually uninstalling
the `kms` plugin (Claude Code has no uninstall/disable lifecycle hook —
see `docs/facts/0007-claude-code-plugin-uninstall-lifecycle.md` — so
this can never be automatic). It finds every trace `bootstrap` (or
`steward`'s ongoing sync) could have left in the target project:

- `kms-seeded: true` files (seeded guardrails, or any future template
  type, per `docs/decisions/0028-generalize-templates-sync-scope.md`)
- `kms-generated: true` files (`docs/skills/{product,process}-track-roles.md`,
  `docs/facts/docs-manifest.md`, per `docs/decisions/0029-bootstrap-full-traceability.md`)
- the `<!-- kms:start -->`/`<!-- kms:end -->` block in the project's
  `AGENTS.md`/`CLAUDE.md`
- any decision/fact still at `status: draft`/`governed-by: TBD` —
  a `bootstrap` proposal nobody ever acted on

It reports every finding first (nothing hidden in per-file prompts),
then asks per file: detach (strip the marker, keep the content as the
team's own) or remove. Both need the same confirmation — the standard
propose-and-wait every skill in this plugin already uses, no extra step
for removal specifically.

**Never touched**: any decision/fact past `status: draft`, any guardrail
without a `kms-seeded`/`kms-generated` marker, any custom guardrail/fact/
decision the team authored themselves — regardless of topic or
resemblance to something `kms` seeded. `plugins/kms/hooks/hooks.json` is
explicitly out of scope: it lives in the plugin's own installed
directory, not the target project's repo, and Claude Code removes it
automatically when the plugin itself is uninstalled.

## Why

A team stopping use of `kms` is left with seeded guardrails, generated
role lists and doc-manifest, an AGENTS.md section, and possibly
still-draft stubs — none of which `kms` can reverse itself, since
plugins can't act after they're uninstalled and Claude Code has no
uninstall hook to act *during* removal. The only window where cleanup
is possible at all is before uninstalling, while `kms`'s skills are
still invocable — so this has to be a skill the team runs deliberately,
not something that happens for them.

Scoping strictly to marked/traceable content (never anything without a
`kms-seeded`/`kms-generated` marker, never a decision/fact the team
acted on) is the same discipline `roadmap`'s duplicate-check and
`steward`'s sync logic already apply: `kms` never touches content it
can't prove is its own.

## Tradeoffs considered

- **Fold into `steward`**: `steward` already has sync logic (check 14) to
  build on, but bundling a rare, deliberate, potentially-destructive
  pre-uninstall action into a skill that runs routinely after every
  session risks it firing unprompted or getting lost among steward's
  eleven other checks. Rejected — matches this plugin's established
  pattern of splitting skills by *when* they run
  (`docs/decisions/0009-bootstrap-and-steward-skills.md`,
  `docs/decisions/0016-lint-skill.md`).
- **Automatic, hook-triggered cleanup**: not possible — per
  `docs/facts/0007-claude-code-plugin-uninstall-lifecycle.md`, no
  uninstall/disable lifecycle event exists in Claude Code's plugin
  system, and a plugin can't act on a project after it's been
  uninstalled. Not a design choice, a hard platform constraint.
- **Same confirmation level for detach and remove**: a stronger,
  separate confirmation for remove specifically was considered, but
  both already require explicit per-file confirmation before writing or
  deleting anything — matching every other skill in this plugin.
  Rejected as unneeded extra friction.
- **Chosen: a new, separate, manual pre-uninstall skill, scoped strictly
  to marked/traceable content.**
