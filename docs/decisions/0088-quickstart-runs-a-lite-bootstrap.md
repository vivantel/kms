---
id: 0088-quickstart-runs-a-lite-bootstrap
title: quickstart runs a lite bootstrap that seeds nothing and asks nothing; bootstrap by name keeps the full path
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-22
tags: [kms, onboarding, packaging]
---

## Decision

`quickstart` runs `bootstrap` in lite mode: steps 1, 2, 9, 10 and 11 only (history stubs, fact stubs, the AGENTS.md block, per-type indexes, the checker). It skips the doc manifest, derivation audit, fitness functions, domain proposals, tag vocabulary and seeding, asks no setup question, and writes `kms-declined:` for every template id so `lint` check 12 stays quiet. `bootstrap` run by name keeps the full path and its ask; a later full run offers what lite skipped, because `kms-declined:` is honoured and removable. A history stub whose only support is a commit message fails admission. This amends decisions 0027 (seeding stays opt-in, now also declined by default on a first run) and 0072 (no guardrail is written, so no `governed-by: TBD` appears on a first run).

## Why

Cold starts on 2026-11-22 took 10 to 25 tool calls and 5 to 10 self-answered questions, and left mostly stubs: draft decisions restating commit messages, a manifest for a one-README repo, five meta-guardrails with `governed-by: TBD`. A first run should end with one real decision and a silent checker, and nothing the user did not ask for.

## Tradeoffs considered

- **One path, rely on the ask**: still costs a batched question a first-time user cannot judge.
- **A flag on `bootstrap`**: a mode named in `quickstart`'s text is enough; no new user-facing surface.
- **Chosen: lite inside `quickstart`, full by name.**
