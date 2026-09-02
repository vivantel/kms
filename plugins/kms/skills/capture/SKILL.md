---
name: capture
description: Turn what a work session produced into durable knowledge — draft new decisions, update changed facts, flag contradictions, catch human-doc drift. Use after a work session that touched decisions, facts, or documented behavior, e.g. "run the knowledge check", "did anything here need capturing as a decision or fact".
---

If the project has no knowledge system yet, run `bootstrap` first — this skill maintains what that one sets up. For whole-knowledge-base health, independent of any one session, run `lint` instead — this skill only reasons about what just happened.

## Artifact model

This skill's sibling `../../shared/artifact-model.md` defines the four artifact types, their fields, and the derivation recipe — read it before drafting anything. Anything drafted here uses the shortest phrasing that preserves meaning — decisions exempt.

## Checks, one pass per invocation

1. **New decision?** Draft a stub: next id, title, one-line motivation, `track: product | process`, `status: draft`. Don't finalize without the owning domain's sign-off. If this decision explicitly replaces an existing one, also update that decision's `status` to `superseded` and add `superseded-by: <new-decision-id>` — don't leave two `active` decisions on the same topic for a later `lint` pass to catch.
2. **Fact changed?** Update the fact file and its `last-verified`. If the governing decision is no longer current, surface the contradiction now.
3. **New automatable rule?** Log as debt in the fitness-function inventory: rule text, governing decision, why not automated yet.
4. **Contradiction found?** Block. Don't close the session until resolved or explicitly deferred with a written note (decision, fact, or stub).
5. **Human-doc drift?** If watched paths overlap what changed this session, propose the specific update; if the doc's still accurate, bump its verified date.
6. **Role list gap?** If a decision drafted this session suggests a role not on that track's role list (`docs/skills/{product,process}-track-roles.md`, if present), propose adding it. (A role that's gone cold over the project's whole history is `lint`'s job, not this session-scoped check's.)

## Recommending a new skill

When proposing a domain for its own skill, state: domain name, trigger condition, one hard constraint, one fitness-function candidate. Proposals — the team decides adoption and naming.

## Out of scope

Authoring final decision records (owning domain), choosing which domains become skills, writing behavioral rules in skill files, arbitrating domain conflicts — surface to the team. Structural validity independent of this session (dangling references, missing fields, expired decisions, redundant/unenforced guardrails, verbosity, sync drift) — that's all `lint`'s job now, checked there once, not duplicated here.
