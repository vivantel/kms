---
id: 0031-consolidate-kb-checks-rename-capture
title: Permanently move duplicated KB checks into lint; narrow and rename steward to capture
status: active
date: 2026-08-30
tags: [kms, knowledge-management, packaging]
track: process
---

## Decision

`lint` permanently owns every check that was duplicated between it and
`steward`: redundant/unenforced guardrails, expired decisions, audit-log
facts, verbosity, statement-split, and baseline-artifact sync. `steward`
is renamed `capture` and narrows to only what's genuinely session-driven:
new decision, fact changed, new automatable rule, contradiction found,
human-doc drift, and the session-scoped half of the old role-list check
(a decision drafted *this session* suggesting an unlisted role — a role
that's simply gone cold over the project's whole history moves to
`lint`, which is the only skill with the full-history view to judge
"a while"). The old "derived artifact stale" check also moves to `lint`
outright — re-checking a guardrail against its grounding decision/fact
inherently needs a full sweep, not a session diff, to catch drift from a
change in some past session nobody re-derived at the time.

`steward`'s directory, `SKILL.md`, `examples.md`, and agent sidecar are
renamed to `capture` throughout `plugins/kms/skills/`. Its "Global
principles" section (which fully overlapped with what's now `lint`-only
content) is removed; a one-line economy reminder for what `capture`
itself drafts replaces it, matching `roadmap`/`bootstrap`'s existing
pattern. The `capture-nudge.sh` hook and `docs/skills/automating-capture.md`
are renamed and updated to match. Every *live* cross-reference to
`steward` across other skill bodies, guardrails, `AGENTS.md`, and
`README.md` is updated; every *historical* reference (existing decisions,
completed plans, past `CHANGELOG.md` entries, facts recording what a
past audit found) is left untouched — those are accurate records of what
was true when written, not living documentation.

## Why

Both skills were invoked together in practice, every time, across this
whole session — never one without the other. That's real evidence
against the reasoning that originally justified keeping them fully
separate (`docs/decisions/0009`, `docs/decisions/0016`): the "don't make
the common case pay for the rare case's cost" argument assumed a
performance difference between a session-scoped check and a full sweep
that, at this repo's actual size (a few dozen files), barely exists.
What's left as a genuine difference — `capture`'s checks need "what
changed this session" context that `lint`'s full-repo, no-session-context
checks don't — is a reason for some checks to require session context,
not a reason to duplicate every check's text across two files and
maintain both copies identically forever. This session already paid
that cost concretely: a single wording fix (which section a sync-refresh
is allowed to touch) had to land in both `lint` check 12 and `steward`
check 14 identically, caught only because both were re-read together.

Renaming `steward` to `capture` follows the same "name says what it
does" bar applied to `uninstall`, `quickstart`, `onboard`, and every
other skill in this plugin — "steward" required already knowing the
domain to guess its function; "capture" doesn't.

## Tradeoffs considered

- **Merge `capture`'s remaining checks into `lint` too, one skill total**:
  considered directly as the opening proposal for this whole
  restructuring. Rejected — the session-context checks (draft a decision
  stub, update a fact, block on a contradiction) need conversational
  awareness of what just happened that a "scan everything, independent
  of any session" skill's design doesn't have room for; keeping them
  separate from `lint`'s job is not the same failure mode as duplicating
  the *same* check in both.
- **Keep `steward`'s name, just narrow its checks**: avoids a rename
  entirely, but leaves a name that told nothing about the (now much
  narrower) job it does, the opposite direction of every other naming
  decision this plugin has made.
- **Rewrite historical decisions/plans/facts to say "capture" instead of
  "steward"**: keeps every file internally consistent, but falsifies
  what was actually decided/built at the time — decision `0009` is
  literally titled "bootstrap-and-steward-skills," explaining why those
  names were chosen; rewriting it would misrepresent history the same
  way `docs/plans/commit-pr-attribution-skills.md` already establishes
  the opposite precedent for (annotate, don't rewrite).
- **Chosen: consolidate the duplicated checks into `lint` permanently,
  narrow and rename `steward` to `capture`, update only live
  documentation.**
