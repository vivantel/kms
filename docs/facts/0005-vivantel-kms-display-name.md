---
id: 0005-vivantel-kms-display-name
title: Fields carrying the "Vivantel KMS" display name
status: active
date: 2026-08-30
tags: [kms, naming, branding]
kind: decision
governed-by: 0022-vivantel-kms-display-name
---

The display-name change decided in
`docs/decisions/0022-vivantel-kms-display-name.md` touches these fields:

- `plugins/kms/.claude-plugin/plugin.json` — `displayName: "Vivantel KMS"`
- `plugins/kms/.codex-plugin/plugin.json` — `description` prefixed with
  "Vivantel KMS (Knowledge Management System): ..."
- `.claude-plugin/marketplace.json` — top-level and per-plugin
  `description`, same prefix
- `README.md` — title `# Vivantel KMS`, opening line expands the acronym
- `CONTRIBUTING.md` — opening line expands the acronym

`name: "kms"` (both manifests), the `/plugin install kms` slug, and the
`plugins/kms/` directory path are unchanged.
