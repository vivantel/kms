---
name: bootstrap
description: One-time setup of a fact/decision/guardrail/skill knowledge system in a project that has none yet, or a gap-fill pass over one that's incomplete — extract intents from git history, extract facts from existing docs, audit guardrails for missing derivation, and inventory fitness functions. Use when the user wants to set up knowledge management for a project, e.g. "bootstrap the knowledge system here", "set up facts/decisions/guardrails for this repo".
---

Set up the knowledge system this plugin's other skills assume: intents (what the team commits to), facts (what's currently true), guardrails (what must or must not happen, derived from the first two), and skill prescriptions (how to act). Run once per project, or as a gap-fill pass on an incomplete one. Once artifacts exist, `steward` maintains them across sessions.

## Artifact types

| Type | Mode | Origin | Where | Verified by |
|------|------|--------|-------|-------------|
| Environmental fact | descriptive | original | `facts/` | Observe from the world (tool output, docs, benchmarks) |
| Decision fact | descriptive | original | `facts/` | Check the governing decision is still current |
| Decision | axiomatic | original | `decisions/` | Expert review; immutable once accepted |
| Skill prescription | procedural | original | `skills/` | Expert review; can be refined |
| Guardrail | normative | derived | `guardrails/` | Re-derive from its sources; compare |

**Mode** is the kind of claim: descriptive — true right now; axiomatic — what the team commits to, with context and rationale; normative — must or must not happen, derived from an axiomatic commitment plus a descriptive fact; procedural — how to decide or act.

A guardrail is only valid while its sources are current — a source change invalidates it.

## File formats

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md` (4-digit, 1-based, per directory); guardrails and skill prescriptions as `docs/{guardrails,skills}/slug.md`, no numeric prefix.

All four carry the base frontmatter `id, title, status, date, tags`, plus these type-specific fields:

Fact — add `kind: environmental | decision | derived | mixed` (mixed = file has both; label each section inline) and `governed-by: <decision-id>` (`TBD` = debt).

Guardrail — add `governed-by: <decision-id>`, `grounded-in: <fact-id[, ...]>`, and `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. Missing any of the three = undeclared, flag as debt.

Decision — add `track: product | process` (required: product = what the
project is for and who it serves; process = how it's built, organized,
or shipped); optionally `scope: <what it applies to>`,
`expires: <date or condition>`, `governed-facts: [<fact-id>, ...]`, and
`fitness-functions: [<check description>, ...]`.

**Derivation recipe**: `Decision (why) + Fact (what is) → Guardrail (ought)`. The `derivation-note` states that step in one sentence; if either source changes, re-apply and propose updated guardrail text.

Fact and guardrail stubs written here use the shortest phrasing that preserves meaning — decisions and plans are exempt.

## Before starting

Detect what the project already has, the same way `roadmap` does: look for an existing `decisions/`, `facts/`, `guardrails/`, or `skills/` directory and infer format from real examples there. If none exists, default to the structure above under `docs/`. Never invent a mismatched directory convention — extend what exists, don't duplicate.

Note the highest existing number in `facts/` and `decisions/` so new stubs continue the sequence rather than collide.

Write files directly — this is a setup pass, not a chat recommendation. If a file already covers the same ground, extend it rather than creating a duplicate.

## Steps

### 1. Intent extraction from history

Scan git log and existing docs (README, planning notes, guardrail/skill files) for decision language: project-specific markers (`DECISION:`/`RFC:`/`APPROVED:`) or natural language (`why`, `because`, `must`, `never`, `required by`).

- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `track: product | process` (add `scope`/`expires` if the decision is bounded or provisional), `status: draft`.
- Flag ambiguous entries inline (`<!-- looks like a decision, could be a behavioral rule — classify before finalizing -->`) rather than guessing.
- Stop at the stub. Full authorship (rationale, tradeoffs) belongs to the domain that owns the decision.

### 2. Fact extraction

For every table, value list, or configuration default embedded in a skill or guardrail file, classify it: environmental, decision, or derived (see Artifact types above). Write one fact stub per finding, `governed-by: TBD` when none exists yet.

### 3. Doc manifest bootstrap

For every human-facing doc (README, planning notes, roadmap, other `docs/` markdown), add an entry to `facts/docs-manifest.md` mapping the doc's sections to the content and decisions they describe, plus the watch paths that would make each section drift. Leave `last-verified` blank; `steward` fills it in later.

### 4. Guardrail derivation audit

For every existing guardrail file, check whether `governed-by`, `grounded-in`, and `derivation-note` are present. If any are missing, flag it as undeclared, propose the most likely governing decision(s) and grounding fact(s), and draft the `derivation-note`. Log undeclared guardrails as debt.

### 5. Fitness function inventory

Scan existing checks (CI/build config, review checklists, approval gates) for rules already enforced, and record them. Scan skill/guardrail files for rules that *could* be automated but aren't, and log each as debt: rule text, why not automated yet, governing decision (or `TBD`).

### 6. Skill gap detection

Propose domains that need their own skill, based on what's in the repo:

| Signal in the repo | Domain to cover | Likely review role |
|---|---|---|
| Build manifests, compiled language | Build tooling, runtime constraints | Build Engineer |
| CI workflows, deployment config | Pipeline structure, release process | Release Engineer |
| Multi-repo boundary, subtree/submodule sync | Integration contracts, public APIs | Architect |
| Test suite, quality gates | Correctness verification, release criteria | QA/Test Owner |
| Roadmap, pricing tiers, access control | Product scope, positioning | Product Strategist |
| Recurring manual process, no written procedure | Process/procedure documentation | Process Owner |
| External compliance, regulatory, or ethical requirement | Compliance/review skill | Compliance Reviewer |
| Repeated reviewer or stakeholder feedback pattern | Review/quality skill | Quality Reviewer |

For each: one paragraph on what it would own, one hard constraint, one fitness-function candidate. Proposals — the team decides adoption and naming. Domains governing irreversible decisions (published APIs, binary ABI, irreversible schema changes, legal/compliance commitments, public claims) are the highest priority to formalize first.

### 7. Compile the track role lists

From the "Likely review role" column above, write
`docs/skills/product-track-roles.md` and
`docs/skills/process-track-roles.md` — base frontmatter (`id`, `title`,
`status`, `date`, `tags`) like any other skill prescription, then one
role per line: name plus a one-line scope (what kind of decision it
should weigh in on). Sort each role by whether it bears on what the
project is for (product) or how it's built (process) — a role can
appear on both lists if it's relevant to both. When a role's track is
genuinely ambiguous (e.g. a compliance, quality, or process-documentation
role), default to process: these typically govern how something is
built or reviewed, not what the project is for; only place a role on
product if its scope is explicitly about mission, audience, or
positioning. These are review perspectives an agent considers while
drafting or reviewing a decision of that track, not a staffing
assignment.

### 8. Seed baseline guardrails

This skill's sibling `../../templates/guardrails/` holds kms's standard starter guardrails. For each template not yet present (by `id`) in this project's `docs/guardrails/`, write it directly, like any other stub this skill produces: copy the template as-is, replace `date: TBD` with today's date, drop its `template-version` field, and add `kms-seeded: true` and `kms-template-version: <the template's own template-version>`. `governed-by`/`grounded-in` stay `TBD` (debt) unless the team later drafts a decision for it.

## Out of scope

Finalizing decision records, choosing which proposed domains become skills, arbitrating domain conflicts — surface to the team.
