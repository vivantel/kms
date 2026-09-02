---
id: 0024-automate-steward-nudge-hook
title: Ship a Claude Code SessionStart hook that nudges toward steward after a recent commit
status: active
date: 2026-08-30
tags: [kms, automation, claude-code, hooks]
track: process
---

## Decision

`plugins/kms/hooks/hooks.json` ships a `SessionStart` hook (Claude Code
only — see `docs/facts/0006-claude-code-plugin-hooks-mechanism.md`) that
runs `plugins/kms/hooks/steward-nudge.sh`, which prints a plain-text note
when `HEAD`'s commit is recent (default: under 4 hours old), as an
approximation of "a commit happened recently enough that steward may be
worth running." The note is phrased as context for the agent to
optionally raise with the user ("if relevant, mention to the user
that..."), not as a guaranteed user-visible banner — `SessionStart`'s
plain stdout is added as context the model can see and act on, not
rendered as a distinct system message (per
`docs/facts/0006-claude-code-plugin-hooks-mechanism.md`).

This is a revision of this decision's original design, which used
`SessionEnd` and assumed its output would be shown to the user. Two
corrections were needed after the original design shipped, both from
targeted fact-checks against primary docs:

1. `SessionEnd` output is discarded entirely — it cannot reach the user
   or the model at all, by design, since the session is already
   terminating. The originally shipped hook was consequently a complete
   no-op, caught by a `/code-review` pass, not by testing (the hook's
   logic was verified correct in isolation, but never checked against
   what `SessionEnd` actually does with its output).
2. `SessionStart` (the corrected event) doesn't display a message
   either — it adds plain stdout as *context for the model*, which is
   why the script's wording addresses the agent ("mention to the user
   that...") rather than the user directly.

The shell logic itself was extracted from an inline `hooks.json` command
string into `plugins/kms/hooks/steward-nudge.sh`, referenced via the
`${CLAUDE_PLUGIN_ROOT}` path placeholder — both for readability (a
one-line JSON string has no room for the comments and structure a
`/code-review` pass flagged as needed) and because a real script file
could be tested standalone, which is how the two shell bugs below were
caught and verified fixed.

Two bugs in the original shell logic were also fixed in the same pass:
- `git rev-parse --is-inside-work-tree` exits 0 even when it prints
  `false` (e.g. a bare repo, or cwd inside `.git`) — the original `if`
  only checked exit status; the fix checks the printed value.
- A future-dated commit or clock skew could produce a negative `age`,
  which unconditionally satisfied `age -lt window`; the fix adds an
  `age -ge 0` guard.

`docs/skills/automating-steward.md` documents the corrected mechanism,
the time window, how to disable it, and a manual recipe for
non–Claude-Code agents.

> **Note (2026-08-30)**: `steward` was later renamed `capture`
> (`docs/decisions/0031`); the file above was renamed
> `docs/skills/automating-capture.md` and the hook script
> `capture-nudge.sh` to match. Left unedited above as the historical
> record of what this decision actually built at the time.

## Why

The single biggest reason a knowledge-management workflow goes unused is
that invoking it depends entirely on the user remembering to — every
skill in this plugin so far is opt-in with no ambient reminder at all.
Claude Code's plugin-level `hooks/hooks.json` auto-activates for anyone
who installs the plugin, with zero manual setup, making it the most
"ambient" mechanism available without asking every user to hand-edit
their own `settings.json` — even constrained to `SessionStart`'s
context-injection (agent-mediated) rather than a guaranteed visible
banner.

Gating on commit recency (rather than firing on every session start
unconditionally) directly answers a concern raised during this
decision's original interview: an unconditional nudge on every session
start — including ones with nothing recent to report — would read as
noise. Commit recency is an imperfect proxy for "committed during the
prior session" (a long-idle gap between sessions, or a commit made by
someone else, can mis-fire either way), but it needs no cross-hook state
and uses only confirmed, documented hook behavior.

## Tradeoffs considered

- **`SessionStart` records a starting ref/timestamp, a later hook
  compares against it** for exact commit-during-session detection: more
  precise, but requires inventing an undocumented cross-hook scratch-state
  convention — rejected in the original design and still rejected here;
  see the git history of this file for that reasoning, preserved because
  it's still correct.
- **Unconditional nudge, no gating at all**: simplest, but risks becoming
  noise on sessions where nothing relevant happened. Rejected.
- **Docs-only recipe, no shipped hook**: fully agent-neutral, zero risk of
  another broken mechanism, but gives up the one genuinely zero-setup
  automation win available on Claude Code. Rejected a second time after
  the `SessionEnd` failure was found — the fix was to correct the
  mechanism, not abandon it, since a working `SessionStart` version was
  confirmed achievable.
- **Chosen: a self-contained `SessionStart` hook, gated on commit
  recency, phrased as agent-facing context; plus a manual recipe for
  other agents.**
