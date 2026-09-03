---
id: 0007-claude-code-plugin-uninstall-lifecycle
title: Claude Code has no plugin uninstall/disable lifecycle hook
status: active
date: 2026-08-30
tags: [kms, packaging, claude-code, hooks]
kind: environmental
governed-by: 0030-uninstall-skill
---

Confirmed 2026-08-30 via Claude Code's own docs
(`code.claude.com/docs/en/hooks.md`, `plugins-reference.md`, `plugins.md`,
`discover-plugins.md`, fetched directly):

- Of the 33 documented hook events, none is an uninstall or disable
  event (no `PluginUninstall`, `PluginDisable`, or equivalent).
- Uninstalling removes the plugin's *own* installed directory: the
  previous version is marked orphaned and swept in the background
  roughly 14 days later; a plugin's persistent data directory
  (`${CLAUDE_PLUGIN_DATA}`) is deleted immediately unless `--keep-data`
  is passed. Neither applies to files a plugin wrote elsewhere.
- Skills-directory plugins (discovered in place under `~/.claude/skills/`,
  not copied) are never automatically deleted at all.
- Claude Code explicitly blocks a plugin from referencing files outside
  its own directory in manifest-declared paths ("It rejects a component
  path that resolves outside the plugin root"). This governs
  manifest-declared paths specifically — it does not prevent a skill's
  own instructions from directing an agent to read/write files in a
  target project via ordinary tool use, which is how
  `bootstrap`/`steward`/`lint`/`uninstall`'s templates-sync mechanism
  works.
- No documented mechanism exists for a plugin to run cleanup logic, or
  even be notified, when it's uninstalled or when a project it
  previously wrote into changes.

**Conclusion**: cleanup of what `bootstrap` writes into an adopting
project can only ever be a skill the team runs manually, before
uninstalling — never an automatic, hook-triggered action. This is a
platform constraint, not a design choice; see
`docs/decisions/0030-uninstall-skill.md`.
