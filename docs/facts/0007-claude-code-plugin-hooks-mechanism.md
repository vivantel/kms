---
id: 0007-claude-code-plugin-hooks-mechanism
title: Claude Code plugin hooks — file location, schema, and event options
status: current
date: 2026-08-30
tags: [kms, packaging, claude-code, hooks]
kind: environmental
governed-by: 0024-automate-steward-nudge-hook
---

Confirmed 2026-08-30 via Claude Code's own docs
(`code.claude.com/docs/en/plugins.md`, `code.claude.com/docs/en/hooks.md`
and `hooks-guide.md`, fetched directly):

- A plugin can ship a `hooks/hooks.json` file at its own root
  (`plugins/<plugin-name>/hooks/hooks.json`). When a user installs/enables
  the plugin, these hooks are activated automatically — no manual
  `settings.json` editing required. Schema matches user-level
  `settings.json` hooks: an event name (e.g. `SessionEnd`) mapping to an
  array of `{ hooks: [{ type: "command", command: "..." }] }` entries.
- Relevant lifecycle events: `SessionStart` (once per session, source
  values `startup`/`resume`/`clear`/`compact`/`fork`), `SessionEnd` (once
  per session, not blockable), `Stop` (once per turn — too frequent for a
  once-a-session nudge), `PostToolUse` (every tool call, matchable to
  e.g. `Bash(git commit *)`).
- All hook types receive common stdin JSON fields: `session_id`, `cwd`,
  `transcript_path`, `prompt_id`, `hook_event_name`, `permission_mode`.
- `${CLAUDE_PLUGIN_ROOT}` is a documented path placeholder resolving to
  the plugin's own root directory at runtime, usable in a hook's
  `command` field to call a script shipped inside the plugin (e.g.
  `"${CLAUDE_PLUGIN_ROOT}/hooks/some-script.sh"`) instead of inlining
  shell logic as a single dense JSON string value.
- **`SessionEnd` output is discarded entirely and cannot reach the user
  or the model** — the session is already terminating, so there is no
  active interface for it to reach. A hook on this event is suitable
  only for cleanup/logging/side-effects, never for anything meant to be
  seen. (This was learned the hard way: an earlier version of
  `plugins/kms/hooks/hooks.json` shipped a `SessionEnd` hook assuming its
  `echo` output would be shown to the user; a `/code-review` pass caught
  that it was a complete no-op.)
- **`SessionStart`'s plain stdout is added as context the model can see
  and act on — it is not rendered as a distinct, guaranteed user-visible
  message.** A hook nudge on this event reaches the agent, which may or
  may not choose to surface it to the user, rather than reaching the user
  directly. `UserPromptSubmit`, `UserPromptExpansion`, and
  `PostModelSwitch` share this same "stdout becomes context" behavior;
  most other events' stdout goes only to a debug log.
- **Not confirmed with high confidence**: any documented, idiomatic way
  to persist state from one hook invocation to another within the same
  session (e.g. "record something at `SessionStart`, read it back at
  `SessionEnd`") — the official docs don't recommend a scratch-storage
  convention for this. A design that needs cross-hook correlation would
  have to invent its own convention with no doc backing.
- **No documented pattern exists for a hook to directly invoke a skill or
  slash command.** A `command`-type hook can only run a shell command and
  surface output; getting a user to actually run a skill still requires
  them to act on that output themselves.
- Codex's plugin manifest has its own optional `hooks` field (per
  `docs/facts/0003-codex-plugin-manifest-schema.md`) but its schema was
  not investigated here — no confirmed Codex equivalent to Claude Code's
  `hooks/hooks.json` auto-activation exists yet.

This is the descriptive basis for
`docs/decisions/0024-automate-steward-nudge-hook.md`. A primary-source
re-check consulted via a subagent for this fact returned output the
harness flagged as containing instruction-shaped content (a
"bypass-permissions" pattern) and neutralized before it reached this
session — its cross-hook-state suggestion was discarded rather than
acted on, which is why that mechanism is recorded here as unconfirmed
rather than designed around. Re-verify against primary docs before
relying on this fact again if much time has passed, per this repo's own
convention for fast-evolving, externally-owned specs
(`docs/facts/0003-codex-plugin-manifest-schema.md`).
