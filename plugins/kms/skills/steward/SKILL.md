---
name: steward
description: Maintain a project's fact/decision/guardrail/skill knowledge system across sessions — capture new decisions, keep facts current, flag contradictions, catch human-doc drift, re-derive guardrails when sources change. Use after a work session that touched decisions, facts, or documented behavior, e.g. "run the knowledge check", "did anything here need capturing as a decision or fact".
---

If the project has no knowledge system yet, run `bootstrap` first — this skill maintains what that one sets up.

## Global principles

**Token economy:** in every artifact except decisions and plans, use the shortest phrasing that preserves meaning and avoids ambiguity. If a statement needs explanation, it's not a fact or guardrail — it's context for a decision record.

**One statement, one job:** if a fact, guardrail, or derivation-note does two things, split it.

**No redundant guardrails:** before writing a guardrail, check it doesn't only apply "whenever skill X does Y" — if it does, that content belongs in skill X's own body, not a second file.

**No unenforced guardrail:** a guardrail describing behavior a shipped skill should enforce is worthless to that skill's users until the skill's own body says it too — update the skill in the same pass, never defer it. A project's `docs/guardrails/` never ships to anyone who installs the skill; only the skill's own body does.

## Artifact formats

Facts and decisions: `docs/{facts,decisions}/NNNN-slug.md`. Guardrails and skill prescriptions: `docs/{guardrails,skills}/slug.md`. Base frontmatter on all four: `id, title, status, date, tags`.

- **Fact** — add `kind: environmental | decision | derived | mixed` and `governed-by: <decision-id>` (`TBD` = debt).
- **Guardrail** — add `governed-by: <decision-id>`, `grounded-in: <fact-id[, ...]>`, `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. Missing any of the three = undeclared, flag as debt.
- **Decision** — add `track: product | process` (required: product =
  what the project is for and who it serves; process = how it's built,
  organized, or shipped); optionally `scope: <what it applies to>`,
  `expires: <date or condition>`, `governed-facts: [...]`,
  `fitness-functions: [...]`.

Derivation recipe: `Decision (why) + Fact (what is) → Guardrail (ought)`. If either source changes, re-apply and propose updated guardrail text — never leave wording unchanged when its basis moved.

## Checks, one pass per invocation

1. **New decision?** Draft a stub: next id, title, one-line motivation, `track: product | process`, `status: draft`. Don't finalize without the owning domain's sign-off.
2. **Fact changed?** Update the fact file and its `last-verified`. If the governing decision is no longer current, surface the contradiction now.
3. **New automatable rule?** Log as debt in the fitness-function inventory: rule text, governing decision, why not automated yet.
4. **Contradiction found?** Block. Don't close the session until resolved or explicitly deferred with a written note (decision, fact, or stub).
5. **Human-doc drift?** If watched paths overlap what changed this session, propose the specific update; if the doc's still accurate, bump its verified date.
6. **Derived artifact stale?** For every guardrail grounded in a superseded decision or changed fact: re-apply the recipe, propose updated text inline. Never leave a stale norm standing silently.
7. **Guardrail redundant?** If a guardrail only ever applies "whenever skill X does Y" with no broader claim, flag it for removal — or reword it as a system-wide invariant, if the underlying policy was never meant to be skill-specific.
8. **Decision expired?** For every decision with `expires`: if the date has passed, or the condition has plausibly been met, surface it for re-evaluation — don't leave it standing as current.
9. **Fact reads like a log?** If a fact only records a timestamped event, grounds nothing, and nothing references it, flag it for removal or rewrite.
10. **Role list stale?** If recent decisions of a track suggest a role not on that track's role list (`docs/skills/{product,process}-track-roles.md`, if present), or a listed role hasn't matched anything in a while, propose an addition or removal.
11. **Guardrail unenforced?** For every guardrail describing behavior a shipped skill should perform, check that skill's own body actually says it. If it doesn't, update the skill now — a guardrail alone never reaches that skill's users.

## Recommending a new skill

When proposing a domain for its own skill, state: domain name, trigger condition, one hard constraint, one fitness-function candidate. Proposals — the team decides adoption and naming.

## Out of scope

Authoring final decision records (owning domain), choosing which domains become skills, writing behavioral rules in skill files, arbitrating domain conflicts — surface to the team.
