---
id: 0063-typed-scope-on-facts
title: Facts carry an optional typed scope of component, environment and version
status: active
date: 2026-11-08
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

A fact may carry `scope: {component, environment, version}`: a non-empty mapping over those three keys only, values non-empty strings. A fact without `scope` claims to hold everywhere. The field exists on facts only. `shared/lint_check.py` validates its shape (check 2). This amends `0039-unify-lifecycle-and-drop-scope`: the free-text, decision-only `scope` it dropped stays dropped; this is a different field with a fixed shape.

## Why

0039 dropped `scope` because it was free text, decision-only and used by none of 36 decisions. Facts differ: an environmental fact is true of a component, in an environment, on a version (a rate limit on one API tier, a CI behavior on one runner image), and a fact stated without those bounds reads as universal. A reader or `query` cannot tell "holds everywhere" from "holds where it was observed", and a stale-scope fact is judged against the wrong world. A fixed shape lets a tool compare scopes where prose could not.

## Tradeoffs considered

- **Reinstate 0014's free-text `scope`**: unchecked and unqueryable; the reason it was dropped.
- **Scope in the prose body only**: what 0039 left in place; leaves "unqualified" and "forgot to say" indistinguishable.
- **Open key set**: invites per-project keys that no consumer understands. Three keys cover the cases seen in this repo's facts; a fourth needs its own decision.
- **Required on every fact**: forces a value onto facts that are universal (a naming fact), producing filler. Absence meaning "everywhere" is the cheaper convention, at the cost that a forgotten scope looks like a universal claim.
- **Chosen: optional, typed, facts only.** Not yet used by `query` or `conform` to filter; this change makes the field exist and be valid. Existing facts are left unscoped. The scope is part of a fact's content, so a change to it changes the revision that pinned edges compare (decision 0062).
