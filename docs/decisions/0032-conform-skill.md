---
id: 0032-conform-skill
title: Add conform — validates a pending changeset against existing decisions and guardrails
status: active
date: 2026-08-30
tags: [kms, knowledge-management]
track: process
---

## Decision

Add `conform`, a new skill: given a pending changeset — the staged diff
by default, or a commit range, or a flexible free-text target like "the
last 3 PRs" the agent resolves at invocation time — search
`docs/{decisions,guardrails}/` for anything relevant to what the diff
touches, and flag any part of it that appears to violate an existing
guardrail. Cites every guardrail (and, for context, the decision behind
it) by path, the same discipline `query`/`refactor-plan` already use.
Read-only: reports findings, never modifies the changeset itself.

Scope excludes changes to the knowledge base's own artifacts
(`docs/{facts,decisions,guardrails,skills}/`) entirely — that's `lint`/
`capture`'s job. `conform` checks whether the project's actual code or
content changes conform to what's already been committed to, not
whether the KB itself is well-formed.

## Why

Nothing in this plugin currently gates a *pending* change against
existing guardrails before it lands. `refactor-plan` queries the
knowledge base, but only as input to planning a refactor already decided
on; `attribute` reads a staged diff, but only to draft a commit message.
Neither checks whether a diff — any diff, not specifically a refactor —
actually conforms to what the team has already committed to. That gap
surfaced directly while restructuring `lint`/`capture`
(`docs/decisions/0031`): once "does this change conform to our own
rules" was named as a real, missing capability, it was clearly worth
building rather than folding into an existing skill that already has a
different job.

Excluding KB-artifact changes keeps this consistent with the same
line `docs/decisions/0031` just drew — a skill checks either the
project's actual changes against the KB, or the KB's own structural
health, never a mix of both in one pass.

## Tradeoffs considered

- **Fold into `refactor-plan`**: `refactor-plan` already queries
  decisions/guardrails as Phase 1 of planning a refactor — but it plans
  a not-yet-started, multi-step change the user already decided to make;
  `conform` checks a diff that already exists, for any reason, not just
  a refactor. Different trigger, different job. Rejected.
- **Fold into `attribute`**: `attribute` already inspects the staged
  diff, but purely to draft a commit message from it — adding guardrail-
  conformance checking would bloat a skill whose entire job today is
  "write good commit messages," the same "one job per skill" reasoning
  applied throughout this plugin. Rejected.
- **Also flag changes to the KB's own artifacts within the diff**:
  slightly more helpful in one pass, but reintroduces exactly the
  scope-blur `docs/decisions/0031` just resolved. Rejected.
- **Chosen: a new, separate, read-only skill, scoped to non-KB changes
  against existing guardrails.**
