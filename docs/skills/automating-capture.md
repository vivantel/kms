---
id: automating-capture
title: How the capture nudge automation works, and how to adapt it
status: active
date: 2026-08-30
tags: [kms, automation, claude-code, hooks, procedural]
---

## What ships today

`plugins/kms/hooks/hooks.json` is a Claude Code plugin hook (see
`docs/facts/0006-claude-code-plugin-hooks-mechanism.md`), auto-activated
for anyone who installs this plugin — no manual `settings.json` edit
needed. It fires on `SessionStart` and runs
`plugins/kms/hooks/capture-nudge.sh`, which checks whether `HEAD`'s
commit is recent and, if so, prints a note.

That note is **context for the agent, not a guaranteed message to the
user** — `SessionStart`'s plain stdout is added as context the model can
see and act on, not rendered as a distinct system message. This is why
the script's wording addresses the agent ("if relevant, mention to the
user that...") rather than the user directly.

This is an approximation of "the prior session made a commit," not an
exact check — a long-idle gap between sessions, or a commit made by
someone else, can mis-fire either way. See
`docs/decisions/0024-automate-steward-nudge-hook.md` for why a more
precise design (correlating an exact session's start and end) was
rejected, and for the history of two corrections this mechanism needed
before it worked as intended (that decision predates the `steward`→
`capture` rename in `docs/decisions/0031`; its reasoning still applies
unchanged, only the target skill's name did not).

## Adjusting the time window

Edit the `window=14400` value (seconds; 14400 = 4 hours) at the top of
`plugins/kms/hooks/capture-nudge.sh` — that's the only place it's
defined.

## Disabling it

Delete `plugins/kms/hooks/hooks.json`, or remove the `SessionStart` entry
from it. There's no separate opt-out flag — the file's presence is the
whole mechanism.

## Testing it standalone

`plugins/kms/hooks/capture-nudge.sh` is a plain POSIX shell script and
can be run directly to check its logic without needing a live Claude
Code session:

```sh
sh plugins/kms/hooks/capture-nudge.sh   # prints the note iff HEAD is recent
```

## Non–Claude-Code agents

No confirmed auto-activating equivalent exists yet (Codex's plugin
manifest has its own `hooks` field per
`docs/facts/0003-codex-plugin-manifest-schema.md`, but its schema wasn't
investigated for this). Until one is confirmed, the manual recipe is: run
`plugins/kms/hooks/capture-nudge.sh` yourself after a work session, or
run `capture` directly if you already know a commit just happened. See
`docs/skills/adding-agent-support.md` if a future agent target should get
its own confirmed automation added here.
