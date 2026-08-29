---
id: plugin-manifest-version-sync
title: Every plugin manifest's version field must be bumped together
status: active
date: 2026-07-29
tags: [kms, agent-agnostic, codex, packaging, guardrail]
---

## Guardrail

Whenever `plugins/kms`'s skill set changes in a way that warrants a
version bump, every plugin manifest for that plugin — currently
`plugins/kms/.claude-plugin/plugin.json` and
`plugins/kms/.codex-plugin/plugin.json` — MUST have its `version` field
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
- **Normative conclusion**: therefore every manifest's `version` is
  treated as one logical value with multiple physical copies, not
  independent version histories.
