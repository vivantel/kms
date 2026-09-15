---
id: 0050-version-bump-changelog-linkage
title: Require a CHANGELOG entry for every plugin manifest version bump
status: active
date: 2026-09-12
tags: [kms, git, changelog, release, packaging]
track: process
governed-facts: [0013-changelog-lagged-four-version-bumps]
fitness-functions: ["A lint check comparing the latest manifest version against CHANGELOG.md's headings, flagging a mismatch, once worth the setup cost — currently manual discipline only, same debt shape as docs/guardrails/plugin-manifest-version-sync.md's own unenforced status logged on docs/decisions/0008-native-codex-plugin-support.md."]
---

## Decision

A plugin manifest version bump (`docs/guardrails/plugin-manifest-version-sync.md`)
and a `CHANGELOG.md` entry for that version are one unit of work, not two
independently-timed ones. `docs/guardrails/version-bump-requires-changelog-entry.md`
makes this a standing rule: whenever the manifests bump, run `changelog`
for that version in the same change, or before the change is considered
done — never leave it for "later."

This does not reopen `docs/decisions/0005-changelog-generation-design.md`'s
design: `changelog` stays on-demand, asks for the version/date at
invocation, and still writes nothing automatically. It only says *when*
that on-demand invocation is required, not how the skill itself behaves —
narrower than the "enforced release cadence" `0005` explicitly rejected,
since drafting/exploratory work between named versions still needs no
entry at all; only a version that actually ships does.

## Why

`docs/facts/0013-changelog-lagged-four-version-bumps.md` records what
happened without this rule: four manifest version bumps landed with zero
corresponding entries, because nothing anywhere connected the two. The
plugin's `version` field is what a consumer sees when installing or
updating (`0005`'s own stated rationale for shipping `changelog` at all)
— a version with no changelog entry defeats that purpose just as
thoroughly as never having built the skill.

The gap wasn't a one-off oversight: this same session's own
`docs/plans/archive/operationalizes-field-and-check.md` flagged its own
missing `0.11.0` entry as a pending step and it still sat unresolved
through two more bumps, because nothing forced revisiting it. A rule that
depends on remembering, with no check or requirement backing it, degrades
the same way every other unenforced guardrail in this project has —
matching the exact pattern `docs/guardrails/plugin-manifest-version-sync.md`
itself already hit (logged as fitness-function debt on `0008`).

## Tradeoffs considered

- **Leave it fully on-demand, no linkage (status quo)**: matches `0005`'s
  original minimalism most closely, but is the exact gap this decision
  exists to close — already produced a 4-version, months-spanning
  documentation hole once.
- **Auto-generate a CHANGELOG entry as part of the version-bump action
  itself**: would close the gap mechanically, but reopens `0005`'s
  explicitly-rejected auto-versioning/automation scope, and a
  machine-drafted entry loses the human-chosen Why-summary framing `0005`
  deliberately wanted over raw commit subjects.
- **Chosen: keep `changelog` on-demand and manual, but make invoking it
  part of the same unit of work as the version bump** — closes the
  linkage gap without touching `0005`'s actual design, and matches this
  project's existing preference (see `0047`) for a checkable guarantee
  over a purely aspirational rule.
