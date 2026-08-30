---
id: plugin-manifest-version-sync
title: Every plugin manifest's version field must be bumped together
status: active
date: 2026-07-29
tags: [kms, agent-agnostic, codex, kilo, packaging, guardrail]
governed-by: 0008-native-codex-plugin-support
grounded-in: 0003-codex-plugin-manifest-schema, 0008-kilo-code-skills-spec
derivation-note: >
  Given decision 0008 (one skill set, many manifests, later extended to
  Kilo by decision 0035) and facts 0003 and 0008 (Codex's manifest and
  Kilo's index.json each carry their own independent version
  field/values), every manifest's version must move together.
---

## Guardrail

Whenever `plugins/kms`'s skill set changes in a way that warrants a
version bump, every plugin manifest for that plugin — currently
`plugins/kms/.claude-plugin/plugin.json`,
`plugins/kms/.codex-plugin/plugin.json`, and every per-skill `version`
field in `plugins/kms/skills/index.json` — MUST have its `version` field
bumped to the same value in the same change. Never bump one manifest's
version and leave another stale; a stale manifest gives users on that
agent a wrong signal about whether an update is available.

If a future agent target (see `docs/skills/adding-agent-support.md`)
gains its own manifest with its own `version` field, it joins this same
rule.

## Derivation

- **Descriptive basis**: `docs/facts/0003-codex-plugin-manifest-schema.md`
  — Codex's `plugin.json` has its own independent `version` field, just
  like Claude Code's.
- **Axiomatic basis**: `docs/decisions/0008-native-codex-plugin-support.md`
  — the team committed to shipping the same skill set to multiple agents
  from one repo, which only works as "one release, many manifests" if the
  manifests don't drift.
- **Descriptive basis**: `docs/facts/0008-kilo-code-skills-spec.md` —
  Kilo's remote-skills `index.json` carries a `version` string per
  skill entry, used to trigger cache refresh on the consuming side.
- **Extension**: `docs/decisions/0035-native-kilo-code-support.md` — a
  later decision that joins Kilo's `index.json` to this same rule, per
  the "a future agent target... joins this same rule" clause above,
  rather than replacing 0008 as the guardrail's governing decision.
- **Normative conclusion**: therefore every manifest's `version` is
  treated as one logical value with multiple physical copies, not
  independent version histories.
