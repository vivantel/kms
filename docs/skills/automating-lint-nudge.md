---
id: automating-lint-nudge
title: How the lint nudge automation works, and how to adapt it
status: active
date: 2026-09-12
tags: [kms, automation, claude-code, hooks, procedural]
---

## What ships today

The same `plugins/kms/hooks/hooks.json` `SessionStart` hook that runs
`capture-nudge.sh` also runs `plugins/kms/hooks/lint-nudge.sh` — a
separate script, not a mode of the first one, matching
`docs/guardrails/one-statement-one-job.md`. It counts commits touching
`docs/{facts,decisions,guardrails,skills}/` in the last 14 days and, at
5 or more, prints a note suggesting `lint`. Same context-not-message
caveat as `capture-nudge.sh`
(`docs/decisions/0024-automate-steward-nudge-hook.md`): `SessionStart`
stdout is agent-visible context, not a guaranteed user-facing banner.

This is a proxy for "the knowledge base has churned enough that
structural drift may have accumulated," not a real measure of staleness
— a burst of unrelated small commits could trip the threshold with
nothing actually wrong, and a knowledge base that changes rarely but
badly could go a long time under it. `docs/decisions/0040-lint-contradiction-and-staleness-checks.md`'s
own `lint` already does the real check; this only decides when to
suggest running it. `git log --since`/path-filtered counting was chosen
over tracking "when `lint` last actually ran" because the latter needs
new persistent state `lint` itself would have to write — the same kind
of undocumented cross-hook state `0024` already rejected once for a
harder version of this same problem.

## Adjusting the window or threshold

Edit `window_days=14` and `threshold=5` at the top of
`plugins/kms/hooks/lint-nudge.sh` — the only place either is defined.

## Disabling it

Remove its entry from `plugins/kms/hooks/hooks.json`'s `SessionStart`
array, or delete `hooks.json` entirely to disable both nudges at once.

## Testing it standalone

```sh
sh plugins/kms/hooks/lint-nudge.sh   # prints the note iff the count clears the threshold
```

## Non–Claude-Code agents

Same gap as `capture-nudge.sh`: no confirmed auto-activating equivalent
exists yet for other agents. Manual recipe: run
`plugins/kms/hooks/lint-nudge.sh` yourself, or just run `lint` on
whatever cadence makes sense for the project.
