---
id: 0026-token-economy-guardrail
title: Promote token economy from unenforced steward prose to a governed, checked guardrail
status: active
date: 2026-08-30
tags: [kms, knowledge-management, guardrail]
track: process
---

## Decision

"Token economy" — every fact, guardrail, and skill prescription
(decisions and plans exempt) uses the shortest phrasing that preserves
meaning and avoids ambiguity — moves from a single unnumbered prose
bullet in `steward`'s "Global principles" section to a real guardrail,
`docs/guardrails/token-economy.md`, with actual enforcement:

- `lint` gains a full-repo check for it (was entirely absent).
- `steward` gains it as a numbered check (was prose only, never one of
  its checks — so running `steward` never actually verified it).

Both checks restate the rule inline, self-contained, matching how every
other check in `lint`/`steward` already works — neither references
`docs/guardrails/token-economy.md` by path. That file only exists in the
`kms` marketplace repo itself; a shipped check referencing it directly
would silently fail the moment it ran against an adopting project's own
repo, which doesn't have it. This was the first design tried here and
corrected after review, in the same session — see the git history of
this file and of `docs/guardrails/token-economy.md` for that version.

Scope is `docs/{facts,guardrails,skills}/` — a project's own knowledge
base — not `kms`'s Claude Code packaging layer
(`plugins/<plugin-name>/skills/*/SKILL.md`). That layer is `kms`-repo-
specific (only relevant to whoever authors a Claude Code plugin, not to
an arbitrary team using `kms`'s fact/decision/guardrail method for their
own docs) and is governed by `AGENTS.md`/`CONTRIBUTING.md` for `kms`
contributors instead, the same split `docs/decisions/0018-per-skill-examples-convention.md`
already drew for the `examples.md` convention.

## Why

Before this decision, "token economy" had none of the properties this
repo requires of every other cross-cutting rule: no governing decision,
no guardrail file, no numbered check anywhere. It was pure aspiration —
structurally identical to the "unenforced guardrail" failure mode this
repo has already caught and fixed twice (`every-skill-ships-examples`
needed a `lint` check added; the 0.2.1 changelog records the same gap
for "no unenforced guardrail" itself).

This was caught only because a user asked directly whether a token
economy pass had run — not because any of this plugin's own skills
would have surfaced it unprompted. A second correction (the
kms-repo-specific file reference, and the packaging-layer scope
question) was caught the same way, by the same user, immediately after
the first fix — both are recorded here rather than smoothed over,
consistent with how `docs/decisions/0024-automate-steward-nudge-hook.md`
documents its own two corrections.

## Tradeoffs considered

- **Leave it as steward prose, just add the missing check number**:
  fixes the "steward never actually checks it" gap, but leaves it
  ungrounded and absent from `lint`. Rejected.
- **Reference `docs/guardrails/token-economy.md` directly from `lint`/
  `steward`'s shipped checks**: simpler to write, but breaks the moment
  either skill runs against an adopting project's own repo, where that
  file doesn't exist. Tried first, rejected after review.
- **Scope the guardrail to include `plugins/<plugin-name>/skills/*/SKILL.md`**:
  tried first, rejected — that's `kms`'s own packaging layer, not a
  target project's knowledge base; conflating the two is the same
  category error `every-skill-ships-examples` already had to draw a line
  around.
- **Also fix steward's other three "Global principles"** (one-statement-
  one-job, no-redundant-guardrails, no-unenforced-guardrail), which have
  the identical gap: no decision, no guardrail file, present only as
  steward prose: deferred, out of scope for this decision — flagged to
  the user as the same latent issue, not silently expanded into here.
- **Chosen: a real guardrail scoped to `docs/{facts,guardrails,skills}/`,
  checked by `lint` and `steward` via self-contained inline rules.**
