---
id: 0027-baseline-guardrail-seeding
title: Ship kms's four Global Principles as templated, synced baseline guardrails
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management, guardrail, packaging]
track: process
---

## Decision

`steward`'s remaining three "Global principles" (one-statement-one-job,
no-redundant-guardrails, no-unenforced-guardrail — token economy was
already covered by `docs/decisions/0026-token-economy-guardrail.md`)
become real guardrails in `kms`'s own `docs/guardrails/`, governed by
this decision, the same way `docs/guardrails/token-economy.md` is.
`no-redundant-guardrails` and `no-unenforced-guardrail` already had
matching numbered checks (`steward` 7 and 11); `one-statement-one-job`
gets a new one (`steward` 13, mirroring `lint` 11).

Separately — and this is the larger part of this decision — `kms` ships
these four as **product assets**, not just internal process docs:
`plugins/kms/templates/guardrails/{token-economy,one-statement-one-job,
no-redundant-guardrails,no-unenforced-guardrail}.md`. `bootstrap` seeds
any missing one into a project's own `docs/guardrails/` at setup;
`steward`/`lint` keep them synced afterward — add what's missing, update
what's stale, remove what's been retired upstream, and never touch what
a team has deliberately detached.

**Sync mechanism**: each seeded file is stamped `kms-seeded: true` and
`kms-template-version: <N>`, where `N` comes from the *template file's
own* `template-version` field — not the plugin's overall version. A
team detaches a copy permanently (opting out of future update/removal)
by deleting those two stamped fields.

This template directory is distinct from `docs/{facts,decisions,
guardrails,skills}/`, which stays `kms`'s own internal/process knowledge
base — `docs/skills/scoping-shipped-vs-repo-rules.md` already drew this
line for behavior; this decision draws the matching line for seeded
*content*.

## Why

Two gaps, found in sequence during this same design conversation:

1. Token economy alone, as a hardcoded rule inline in `lint`/`steward`,
   is invisible and unowned by an adopting team — they can't see it,
   customize it, or know it exists until a check fires. The same is true
   for the other three principles, worse: they had no numbered check at
   all until this decision (`one-statement-one-job`) or were checked
   without ever being named as a guardrail a team could inspect.
2. `bootstrap`-only seeding isn't enough once `kms` itself keeps
   evolving — a project bootstrapped before a given baseline guardrail
   existed has no way to pick it up later except by re-running the
   *setup* skill. `steward`, which already runs every session, is the
   natural place for ongoing sync.

Two design mistakes were caught and corrected before landing here,
both by direct pushback in this session, not by the design surviving
review unchallenged:

- **Reusing the plugin's whole semver as the sync version** would make
  every seeded guardrail in every adopting project look stale the
  moment *any* unrelated part of `kms` shipped a new version — pure
  noise, since the guardrail's actual wording never changed. Fixed by
  giving each template its own independent `template-version`.
- **Detecting the installed version by parsing the observed
  `Base directory for this skill: .../kms/<version>/skills/<name>`
  path** would have baked a Claude-Code-specific, undocumented
  cache-layout detail into supposedly agent-neutral skill instructions
  — exactly what `docs/guardrails/agent-agnostic-skill-content.md`
  exists to prevent, and fragile besides (an implementation detail, not
  a documented API). Fixed by reading `template-version` directly off
  the template file on disk instead.

## Tradeoffs considered

- **Keep these as inline-only checks, no seeded files** (the design
  before this decision): cheapest, but leaves every adopting team
  blind to rules being applied to their own repo, with no way to
  inspect, override, or opt out short of ignoring lint/steward output.
  Rejected.
- **One combined `docs/guardrails/` file for all four principles**:
  fewer files, but conflates four independently-derivable rules into
  one — the same "one statement, one job" split this very principle
  argues for. Rejected.
- **Version by content hash instead of a hand-bumped counter**: fully
  automatic, no risk of a contributor forgetting to bump it, but a hash
  can't distinguish "this template changed" from "this template's
  formatting changed" the way a human decision to bump a counter can,
  and adds tooling this repo (no CI, no scripts) doesn't have anywhere
  else. Rejected.
- **Chosen: four real guardrails, seeded as versioned, syncable product
  templates, with an explicit detach escape hatch.**

## Known open risk

Whether Codex's plugin install mechanism copies sibling directories
like `templates/` (or `hooks/`, shipped earlier) at all, versus only the
`skills` path its manifest declares, is unconfirmed — see
`docs/facts/0003-codex-plugin-manifest-schema.md`'s own unconfirmed
gaps. Not resolved here; flagged rather than assumed away.
