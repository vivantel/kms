---
id: 0035-native-kilo-code-support
title: Ship a self-hosted Kilo remote-skills index; list on kilo-marketplace; no directory restructuring
status: accepted
date: 2026-08-30
tags: [kms, agent-agnostic, kilo, packaging]
track: product
---

## Decision

This repo will ship `plugins/kms/skills/index.json`, a remote-skills
manifest in the shape Kilo Code CLI's `skills.urls` config expects (see
`docs/facts/0008-kilo-code-skills-spec.md`), listing every skill under
`plugins/kms/skills/` with its `files` (`SKILL.md`, `examples.md`) and a
`version` string kept in lockstep with every other plugin manifest. Kilo
users add one entry to their `kilo.jsonc`:

```json
{ "skills": { "urls": ["https://raw.githubusercontent.com/vivantel/kms/master/plugins/kms/skills"] } }
```

and get automatic re-fetch whenever `index.json`'s per-skill `version`
bumps — no manual copying into a project, no drift between projects.

Also: prepare a PR to the community `Kilo-Org/kilo-marketplace` repo,
mirroring the skill folders under its `skills/` directory, so kms is
also discoverable via Kilo's built-in browse-and-install UI, not only
via manual config. **That external PR is not submitted as part of this
change** — it's an outward-facing action against a third-party repo and
gets its own go-ahead before it's opened.

Specifically:

- **No directory restructuring.** `plugins/kms/skills/` stays exactly
  where it is; `index.json` sits at its root, generated from the
  existing per-skill folders. Kilo's `files` array is per-skill (not a
  single global path constraint the way Codex's manifest is), so the
  "exclude private skills" failure mode from
  `docs/skills/adding-agent-support.md` doesn't force a restructure here
  either — same as it didn't for Codex.
- **No symlinks** — `index.json` points at the real files Kilo fetches
  over HTTP; nothing here depends on symlink behavior at all, so Kilo's
  (undocumented, for this specific concern) install behavior isn't a
  risk.
- **No `agents/kilocode.yaml` sidecars added.** Per
  `docs/skills/adding-agent-support.md` step 5, sidecars are for *real*
  per-agent differences. There is no known behavioral difference for
  Kilo yet — the content that would go in a `kilocode.yaml` would be
  identical to `agents/openai.yaml`'s, which is exactly the
  boilerplate-duplication case that guidance says not to add.
- **`index.json`'s per-skill `version` fields join
  `docs/guardrails/plugin-manifest-version-sync.md`** — bumped alongside
  `plugins/kms/.claude-plugin/plugin.json` and
  `plugins/kms/.codex-plugin/plugin.json` on every release from now on.
- **Testing is scoped to static schema validation** (valid JSON, shape
  matches `docs/facts/0008-kilo-code-skills-spec.md`) plus verifying the
  raw GitHub URLs actually resolve. No live `kilo` CLI is available in
  this dev environment, so a real `skills.urls` fetch-and-load test is
  left as a named follow-up, not claimed as done here.

## Why

Unlike Codex, Kilo has no manifest to write at all — it already reads
plain `SKILL.md` folders, and this repo's `plugins/kms/skills/` already
matches that shape. The only real gap was *distribution without manual
per-project copying*, which Kilo's `skills.urls` + `index.json` remote-
source mechanism solves directly, using nothing but static files this
repo already serves via GitHub — no build step, no new runtime, no
server, consistent with this repo's existing packaging model.

## Tradeoffs considered

- **Doc-only support (point users at a raw path manually, no
  `index.json`)**: rejected — the user explicitly rejected manual
  per-project copying with no update path; the remote-source mechanism
  costs one generated file and gets auto-updates for free.
- **kilo-marketplace PR only, skip self-hosted `index.json`**: rejected
  — marketplace listing there is browse-and-install via UI, not
  config-driven auto-update, and review/merge latency on a third-party
  repo shouldn't gate having a working distribution path at all.
- **Add `agents/kilocode.yaml` sidecars now "to establish the pattern"**
  (as was done for Codex in `docs/decisions/0008-native-codex-plugin-
  support.md`): rejected this time — that was a one-time, explicit user
  choice for Codex specifically, not a standing default, and
  `docs/skills/adding-agent-support.md` step 5's actual default is to
  skip boilerplate sidecars absent a real difference.
