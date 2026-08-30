---
id: 0003-codex-plugin-manifest-schema
title: Codex's plugin manifest schema and location
status: current
date: 2026-07-29
tags: [kms, agent-agnostic, codex, packaging]
kind: environmental
governed-by: 0008-native-codex-plugin-support
---

Confirmed 2026-07-29 via OpenAI's own developer docs
(`developers.openai.com/codex/plugins/build`, fetched directly — not
search-engine summaries):

- The manifest file is `.codex-plugin/plugin.json`, living inside the
  plugin's own root directory — the same relationship
  `.claude-plugin/plugin.json` has to a Claude Code plugin root.
- Required fields: `name` (string), `version` (string), `description`
  (string).
- Optional fields include `author`, `homepage`, `repository`, `license`,
  `keywords`, `skills`, `mcpServers`, `apps`, `hooks`, `interface`.
- `skills` is a **single relative path string** (e.g. `"./skills/"`),
  relative to the plugin root — not an array of paths, unlike Claude
  Code's `plugin.json` `skills` array. Codex discovers `SKILL.md` files
  recursively under that one path.
- Manifest paths generally must be relative and start with `./`.
- Plugins can be installed via a local path, a git URL (optionally with a
  `ref`/`sha`), or an npm package — none of which require a
  marketplace/registry manifest to exist first.

**Not confirmed with high confidence**: the exact path of a
marketplace/registry manifest for Codex (analogous to Claude Code's
`.claude-plugin/marketplace.json`). One fetch of
`developers.openai.com/codex/plugins/build` returned
`$REPO_ROOT/.agents/plugins/marketplace.json` (or
`~/.agents/plugins/marketplace.json`) and mentioned a
`codex plugin marketplace add owner/repo` CLI command, but a follow-up
fetch of the adjacent `/codex/plugins` overview page could not
corroborate that path. Given local-path/git-URL installs don't need this
file, it wasn't pursued further — see
`docs/decisions/0008-native-codex-plugin-support.md`, which defers the
marketplace manifest rather than committing to an unconfirmed path.

**Why primary docs, not search results**: an earlier search-engine pass
for this same question returned a batch of low-trust sites all claiming
broad `SKILL.md` support, none of them corroborating each other or citable
back to Codex's own docs — those claims were discarded once the primary
docs above gave a precise, citable schema instead.

This is the descriptive basis for
`docs/decisions/0008-native-codex-plugin-support.md` and
`docs/plans/codex-plugin-support.md`. Because this is a fast-evolving,
externally-owned spec, re-verify against the primary docs before relying
on it again if much time has passed.

**Re-verified 2026-08-30, install-command claim retracted**: attempting
to resolve the marketplace-manifest gap above, `developers.openai.com/
codex/plugins` now 308-redirects to `learn.chatgpt.com/docs/plugins`, a
page covering both ChatGPT plugins and Codex CLI plugins as one shared
catalog. It documents no `codex plugin marketplace add owner/repo`
command at all — the only corroborated end-user install path is the
interactive `codex /plugins` browser (browse/install/uninstall from
configured marketplace sources; no documented flag or config syntax for
adding a git URL or local path directly as an end user — "workspace"
marketplace sources are described as admin-imported, not end-user-added).
This means the original `local path / git URL (ref/sha) / npm package`
install claim above is now also unconfirmed, not just the marketplace-
manifest path — it wasn't corroborated by this second source either, and
this fact should not be treated as settling how a `kms` user actually
installs the Codex plugin. `docs/decisions/0008-native-codex-plugin-
support.md`'s manifest-file claims (location, schema, required fields)
are unaffected — only the *installation command* was ever in question.
