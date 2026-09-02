---
id: 0008-kilo-code-skills-spec
title: Kilo Code CLI's skill format and remote-skill-source schema
status: active
date: 2026-08-30
tags: [kms, agent-agnostic, kilo, packaging]
kind: environmental
governed-by: 0035-native-kilo-code-support
---

Confirmed 2026-08-30 via Kilo's own docs (`kilo.ai/docs/customize/skills`,
fetched directly) and the `Kilo-Org/kilo-marketplace` GitHub repo's
structure:

- Kilo Code CLI reads skills in the same open **Agent Skills** format
  Claude Code and Codex use: one folder per skill, containing a
  `SKILL.md` with YAML frontmatter (`name`, `description` required;
  `license`, `compatibility`, `metadata` optional). No Kilo-specific
  manifest wraps this — `plugins/kms/skills/<skill>/SKILL.md` is already
  in the shape Kilo expects, unchanged.
- Kilo also has an unrelated "Plugin" concept (an npm package exporting
  hook functions, `.kilo/plugin/`) — that's a code-extension mechanism,
  not how skill content ships, and doesn't apply here.
- Kilo discovers skills from, in priority order: project-level
  `.kilo/skills/`, user-level `~/.kilo/skills/`, compatibility dirs
  `.claude/skills/` and `.agents/skills/`, additional local paths via
  `skills.paths` in `kilo.jsonc`, and **remote URLs** via `skills.urls`
  in `kilo.jsonc` (lowest priority).
- A remote source must serve an `index.json` at the given URL:
  `{"skills": [{"name": "...", "version": "...", "files": ["SKILL.md", ...]}]}`.
  Kilo fetches each listed file from `{url}/{skill-name}/{file}`,
  atomically replaces its local cache when a skill's `version` string
  changes, and keeps the previous cached copy if a download fails.
  Kilo's own doc does not require a `.well-known/` path prefix for this
  — the `url` in `skills.urls` can point anywhere serving that shape.
- The `Kilo-Org/kilo-marketplace` repo (skills/mcps/agents dirs) is a
  separate, PR-reviewed, browse-and-install-via-UI catalog. It has no
  top-level registry manifest of its own — entries are just directories
  containing a `SKILL.md`.

**Not confirmed with high confidence**: whether Kilo's remote-source
fetcher tolerates `raw.githubusercontent.com`'s response headers
(content-type, caching) without issue — Kilo's docs don't call out
HTTP-level requirements beyond the path shape. Also unconfirmed: a
separate, evolving `/.well-known/agent-skills/index.json` discovery
convention exists as a Cloudflare-authored RFC with a *different* schema
(`$schema`, `type`, `url`, `sha256` digest, no `version` field) — it is
not the same thing as Kilo's own `skills.urls` + `index.json` mechanism
described above, and this repo is targeting Kilo's documented mechanism,
not the RFC.

**Why primary docs, not search results alone**: an initial search-engine
pass returned a claim about a `/plugin marketplace add` CLI command for
Kilo that could not be corroborated from Kilo's own docs and appears to
be search-result bleed from unrelated Claude Code plugin-marketplace
content — discarded in favor of the fetched primary-doc schema above.

This is the descriptive basis for
`docs/decisions/0035-native-kilo-code-support.md`. Because this is a
fast-evolving, externally-owned spec (same caution as
`docs/facts/0003-codex-plugin-manifest-schema.md`), re-verify against
Kilo's primary docs before relying on it again if much time has passed.
