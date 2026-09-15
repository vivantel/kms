---
id: 0055-automate-lint-nudge-hook
title: Ship a Claude Code SessionStart hook that nudges toward lint on KB churn
status: active
date: 2026-09-12
tags: [kms, automation, claude-code, hooks]
track: process
---

## Decision

A second `SessionStart` hook entry (`plugins/kms/hooks/lint-nudge.sh`,
sibling to `capture-nudge.sh`, not a mode of it) counts commits touching
`docs/{facts,decisions,guardrails,skills}/` in the last 14 days and
suggests `lint` at 5 or more. `docs/skills/automating-lint-nudge.md`
documents the mechanism, adjustment, and disabling — same shape as
`docs/skills/automating-capture.md`.

## Why

`lint`'s own checks (dangling references, contradictions, stale debt,
stale fitness-functions) are `kms`'s proactive-review mechanism in
spirit, but nothing has ever forced them to actually run on a cadence —
`lint` is entirely on-demand, and someone has to remember to invoke it.
This is the same failure shape that already cost real time twice this
session: `docs/decisions/0050-version-bump-changelog-linkage.md` (a
version bump with no changelog entry, because nothing tied the two
together) and the token-economy check being skipped on newly-drafted
artifacts until asked. A principle stated with no forcing function
degrades to "whenever someone happens to remember."

`docs/decisions/0024-automate-steward-nudge-hook.md` already solved
this exact shape of problem for `capture` — reused directly rather than
reinvented. The two nudges use different heuristics because they answer
different questions: `capture-nudge.sh` asks "did a commit just happen"
(a point-in-time signal, single recent commit is enough); `lint` needs
"has the KB accumulated enough recent change that drift is plausible" —
a single commit says nothing about that, so it needed a count over a
window instead of a recency check. Kept as a separate script rather than
a second mode of `capture-nudge.sh`, per
`docs/guardrails/one-statement-one-job.md`.

## Tradeoffs considered

- **Track when `lint` last actually ran, nudge based on elapsed time
  since**: more precise than a proxy, but requires `lint` to write new
  persistent state somewhere and the hook to read it — the same
  undocumented cross-hook state convention `0024` already rejected once,
  for a harder version of this same problem (correlating hook and skill
  invocations with no documented mechanism to do so).
- **Nudge on every `SessionStart` unconditionally**: simplest, but
  `0024` already rejected this shape for `capture` as noise-prone on
  sessions with nothing to report; the same reasoning applies here.
- **Fold into `capture-nudge.sh` as a second check in the same
  script**: fewer files, but conflates two genuinely different
  heuristics (point-in-time vs. windowed count) and two different
  target skills in one script, against `one-statement-one-job`.
- **Chosen: a separate `SessionStart` hook entry, windowed commit-count
  heuristic, own script and doc, explicitly acknowledged as an imperfect
  proxy rather than a real staleness measurement.**
