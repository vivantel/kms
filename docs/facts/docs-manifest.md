---
id: docs-manifest
title: Human-facing doc sections mapped to the decisions/facts they describe
status: active
date: 2026-09-12
tags: [kms, knowledge-management, documentation]
kind: environmental
governed-by: 0029-bootstrap-full-traceability
kms-generated: true
kms-registry: docs-manifest
---

Maps each human-facing doc's sections to what they describe and what
would make them drift, per `bootstrap` step 3. `capture` check 5 reads
this to decide whether a session's changes touched a watched path;
`last-verified` is the date a row's doc section was last checked against its watch paths; `capture` bumps it.

## README.md

| Section | Describes | Watch paths | Last verified |
|---|---|---|---|
| Tagline + hook paragraph | The core thesis (vocabulary, not memory), linking the author's article | `docs/decisions/0052-state-the-core-thesis-in-positioning-copy.md`; the three manifest `description` fields and the GitHub repo description (kept in wording sync manually, no single source of truth) | 2026-11-17 |
| Title/intro | What `kms` is, agent-neutral design, 3-agent packaging | `plugins/kms/.claude-plugin/plugin.json` (description), `docs/decisions/0011-...`, `docs/guardrails/agent-agnostic-skill-content.md` | 2026-11-17 |
| Skill table | One-line description + examples link per skill | `plugins/kms/skills/*/SKILL.md` (`description`), `plugins/kms/skills/*/examples.md` existence, `docs/guardrails/every-skill-ships-examples.md` | 2026-11-17 |
| Installing | Quick-start command, link to `INSTALLING.md` | `INSTALLING.md`, `.claude-plugin/marketplace.json` | 2026-11-17 |
| Repo structure | Top-level layout (subset of AGENTS.md's) | `AGENTS.md`'s own Structure section | 2026-11-17 |
| Dogfooding | Points to `AGENTS.md` for the knowledge-base convention | `AGENTS.md` | 2026-11-17 |
| Contributing | Points to `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md` | 2026-11-17 |

## AGENTS.md

| Section | Describes | Watch paths | Last verified |
|---|---|---|---|
| What this repo is | Repo type, no build/test tooling claim | `docs/skills/kms-architecture.md`; note `package.json`/`evals/` are dev-only eval tooling, not a build step for plugin content — re-check this claim if that scope ever grows | 2026-11-17 |
| Structure | Full repo layout diagram | `docs/decisions/0027-...`, `0029-...`, `0034-...`, `0035-...`, `0043-...`; actual directory layout | 2026-11-17 |
| Skill roster paragraph | Names and one-line role of all 15 skills | `plugins/kms/skills/*/SKILL.md` (`description`), actual skill count | 2026-11-17 |
| Manifest/packaging bullets | Marketplace/plugin-manifest mechanics per agent | `docs/facts/0003-...`, `0008-...`, `docs/guardrails/plugin-manifest-version-sync.md`, `docs/decisions/0035-...` | 2026-11-17 |
| Adding a new skill | Skill-authoring steps, economy/eval requirements | `docs/guardrails/every-skill-ships-examples.md`, `docs/guardrails/token-economy.md`, `docs/skills/scoping-shipped-vs-repo-rules.md`, `docs/decisions/0043-...`, `0044-...` | 2026-11-17 |
| Adding a new plugin | Steps for a second plugin | `.claude-plugin/marketplace.json` schema | 2026-11-17 |
| Validation | "No automated checks" claim for manifests | `evals/` (a narrower, skill/shared-content-only automated check now exists — this claim is scoped to manifest JSON well-formedness specifically; re-check if that scope blurs) | 2026-11-17 |

## INSTALLING.md

| Section | Describes | Watch paths | Last verified |
|---|---|---|---|
| Claude Code | Install steps for Claude Code | `.claude-plugin/marketplace.json`, `plugins/kms/.claude-plugin/plugin.json` | 2026-11-17 |
| Codex | Install steps for Codex | `plugins/kms/.codex-plugin/plugin.json`, `docs/facts/0003-...` | 2026-11-17 |
| Kilo Code CLI | Install steps for Kilo | `plugins/kms/skills/index.json`, `kilo.jsonc`, `docs/decisions/0035-...` | 2026-11-17 |

## CONTRIBUTING.md

| Section | Describes | Watch paths | Last verified |
|---|---|---|---|
| Before you start | Repo orientation for a contributor | `AGENTS.md` | 2026-11-17 |
| Adding or changing a skill | Same steps as AGENTS.md's own section | `AGENTS.md`'s "Adding a new skill" section (kept in sync manually — no single source of truth between the two today) | 2026-11-17 |
| This repo dogfoods its own skills | Same as README's section | `AGENTS.md` | 2026-11-17 |
| Governance | Who accepts a decision, `accepted-by` | `docs/decisions/0053-decision-accepted-by-field.md`, `plugins/kms/shared/artifact-model.md`'s immutability note | 2026-11-17 |
| Validation | Manifest JSON validity + eval suite | `docs/decisions/0043-...`, `0044-...`, `evals/` | 2026-11-17 |
| Pull requests | PR conventions | `docs/decisions/0002-...`, `0003-...`, `0004-...` (attribute/commit conventions) | 2026-11-17 |
| Code of Conduct | Points to `CODE_OF_CONDUCT.md` | `CODE_OF_CONDUCT.md` | 2026-11-17 |

## ARCHITECTURE.md

| Section | Describes | Watch paths | Last verified |
|---|---|---|---|
| Overview | The core thesis | `docs/decisions/0052-...` | 2026-11-17 |
| The artifact model | Type table, `track`, lifecycle (incl. `expires`/archive), derivation recipe worked example | `plugins/kms/shared/artifact-model.md`, `docs/decisions/0038-...`, `docs/guardrails/artifact-expires-must-be-reevaluated.md`, `docs/guardrails/agent-agnostic-skill-content.md` (the worked example's own sources, `0006`/`0002`, if either is ever superseded/changed) | 2026-11-17 |
| Governance | Traceability/change-control/enforcement/accountability synthesis; explicit non-additions (`scope`, quality score, `domain`) | `docs/decisions/0053-...`, `0054-...`, `0039-...` | 2026-11-17 |
| The four layers | `docs/` vs. `plugins/kms/skills/` vs. `templates/` vs. `hooks/` | `docs/skills/kms-architecture.md` (the agent-facing version of the same content — keep in sync) | 2026-11-17 |
| How the skills fit together | All 15 skills grouped by role | `plugins/kms/skills/*/SKILL.md` (any added/removed/reclassified), actual skill count | 2026-11-17 |
| How the design got here | 10 pivotal decisions, one line each | Each decision listed — if any is superseded/reworded, update its line or move it out | 2026-11-17 |

## Not tracked here

- `CHANGELOG.md` — an append-only generated log, not a doc whose current
  content should track a decision's current state; `changelog`/`0050`
  own its correctness, not doc-drift checking.
- `CODE_OF_CONDUCT.md`, `LICENSE` — standard boilerplate, not
  `kms`-decision-governed content.
- `CLAUDE.md` — a symlink to `AGENTS.md` (`docs/decisions/0007-...`),
  same content, no separate entry needed.
