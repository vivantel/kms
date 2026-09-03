---
id: 0022-vivantel-kms-display-name
title: Display name becomes "Vivantel KMS", technical identifiers stay "kms"
status: active
date: 2026-08-30
tags: [kms, naming, branding]
track: product
---

## Decision

The plugin's human-facing display name changes from "KMS Dev Skills" to
"Vivantel KMS", expanded on first mention as "Vivantel KMS (Knowledge
Management System)" so a reader can decipher the acronym. This applies
everywhere the plugin is *introduced* to a user or contributor:

- `plugins/kms/.claude-plugin/plugin.json`'s `displayName` field
- `plugins/kms/.codex-plugin/plugin.json`'s `description` (Codex has no
  `displayName` field, per `docs/facts/0003-codex-plugin-manifest-schema.md`,
  so the expansion is woven into the description prose instead)
- `.claude-plugin/marketplace.json`'s top-level and per-plugin
  `description`
- `README.md`'s title and opening line
- `CONTRIBUTING.md`'s opening line

Every technical identifier is unchanged: `plugin.json`/`marketplace.json`
`name: "kms"`, the `/plugin install kms` slug, and the `plugins/kms/`
directory path.
`docs/facts/0005-vivantel-kms-display-name.md` names the exact fields
that carry the new display name, the same way
`docs/facts/0001-kms-skill-names.md` names fields for a governed
decision rather than re-arguing it.

## Why

"KMS" alone reads as an unexplained acronym to a first-time reader with
no vivantel/kms context — prefixing the publisher name and expanding
the acronym on first mention removes that ambiguity at the point a user
or contributor is actually deciding whether this is the right plugin,
without requiring them to already know what it stands for.

## Tradeoffs considered

- **Also rename the technical identifier** (`name: "kms"` →
  `"vivantel-kms"`, `plugins/kms/` → `plugins/vivantel-kms/`, install
  slug changes): fully consistent display/technical naming, but breaks
  the `/plugin install kms` slug for anyone with an existing install and
  touches dozens of cross-references (source path, docs, skill `Refs:`
  trailers) for a purely cosmetic gain. Rejected — chosen explicitly
  over this option when the decision was interviewed; low blast radius
  was preferred over full consistency.
- **Change nothing, keep "KMS Dev Skills"**: no ambiguity resolved, and
  doesn't read as tied to the `vivantel` publisher at all. Rejected.
- **Chosen: display name only becomes "Vivantel KMS", expanded on first
  mention; technical identifiers unchanged.**
