---
name: bootstrap
description: One-time setup of a fact/decision/guardrail/skill knowledge system in a project that has none yet, or a gap-fill pass over one that's incomplete — extract intents from git history, extract facts from existing docs, audit guardrails for missing derivation, and inventory fitness functions. Use when the user wants to set up knowledge management for a project, e.g. "bootstrap the knowledge system here", "set up facts/decisions/guardrails for this repo".
---

Set up the knowledge system this plugin's other skills assume: intents (what the team commits to), facts (what's currently true), guardrails (what must or must not happen, derived from the first two), and procedures (how to act). Run once per project, or as a gap-fill pass on an incomplete one. Once artifacts exist, `capture` maintains them across sessions.

## Artifact model

This skill's sibling `../../shared/artifact-model.md` defines the four artifact types, their fields, and the derivation recipe — read it before drafting anything. Fact and guardrail stubs written here use the shortest phrasing that preserves meaning — decisions and plans are exempt.

## Before starting

Detect what the project already has, the same way `roadmap` does: look for an existing `decisions/`, `facts/`, `guardrails/`, or `skills/` directory and infer format from real examples there. If none exists, default to the structure above under `docs/`. Never invent a mismatched directory convention — extend what exists, don't duplicate.

Note the highest existing number in `facts/` and `decisions/` so new stubs continue the sequence rather than collide.

Write files directly — this is a setup pass, not a chat recommendation. If a file already covers the same ground, extend it rather than creating a duplicate.

## Steps

### 1. Intent extraction from history

Scan git log and existing docs (README, planning notes, guardrail/skill files) for decision language: project-specific markers (`DECISION:`/`RFC:`/`APPROVED:`) or natural language (`why`, `because`, `must`, `never`, `required by`).

- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `track: product | process` (exactly one), `expires` if bounded or provisional, `status: draft`.
- Flag ambiguous entries inline (`<!-- looks like a decision, could be a behavioral rule — classify before finalizing -->`) rather than guessing.
- Stop at the stub. Full authorship (rationale, tradeoffs) belongs to the domain that owns the decision.

### 2. Fact extraction

For every table, value list, or configuration default embedded in a skill or guardrail file, classify it: environmental, decision, or derived (see `../../shared/artifact-model.md`'s Artifact types). Write one fact stub per finding, `governed-by: TBD` when none exists yet.

### 3. Doc manifest bootstrap

For every human-facing doc (README, planning notes, roadmap, other `docs/` markdown), add an entry to `facts/docs-manifest.md` mapping the doc's sections to the content and decisions they describe, plus the watch paths that would make each section drift. Leave `last-verified` blank; `capture` fills it in later. Mark the file `kms-generated: true` — it's constructed from this project's own docs, not copied from a template, but `uninstall` still needs to recognize it as this skill's output.

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

### 7. Compile the track role lists and tag vocabulary

From the "Likely review role" column above, write
`docs/skills/product-track-roles.md` and
`docs/skills/process-track-roles.md` — base frontmatter (`id`, `title`,
`status`, `date`, `tags`) plus `kms-generated: true` (constructed from
this project's own signals, not a template, but still `uninstall`'s to
recognize), like any other procedure, then one
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
assignment. Using the same repo-scan signals, compile
`docs/skills/tags.md`: every tag already used across this project's
artifacts (or, in a fresh project, domain vocabulary drawn from existing
docs), one tag per line with a one-line meaning. Mark any tag carried by
over half of active decisions as `(umbrella)` — computed from the
scan, not asserted — since `lint` check 16 excludes umbrella tags from
its contradiction-scoping test. Same frontmatter and `kms-generated:
true` marking as the role lists above.

### 8. Seed baseline artifacts

This skill's sibling `../../templates/` holds one subdirectory per artifact type kms ships seed content for (currently just `guardrails/`). For each `<type>/` subdirectory and each template not yet present (by `id`) in this project's `docs/<type>/`, write it directly, like any other stub this skill produces: copy the template as-is, replace `date: TBD` with today's date, drop its `template-version` field, and add `kms-seeded: true` and `kms-template-version: <the template's own template-version>`. Leave whichever debt-marking fields apply to that artifact type (see `../../shared/artifact-model.md` — e.g. `governed-by`/`grounded-in` for a guardrail, `governed-by` alone for a fact) as `TBD` unless the team later drafts a decision for it.

### 9. Wire into the project's own agent-instructions file

If the `<!-- kms:start -->` marker isn't already present, insert a marked section into the project's `AGENTS.md` (or whatever host-specific equivalent filename it uses instead of that cross-agent convention; create a minimal `AGENTS.md` if neither exists) — this is a gap-fill step like the rest of this skill, not something to duplicate on a repeat run:

```
<!-- kms:start -->
## Knowledge base

This project uses kms's fact/decision/guardrail/skill knowledge system.
See `docs/{facts,decisions,guardrails,skills}/` — facts (what's true),
decisions (what's committed to and why), guardrails (what must/must not
happen), procedures (how to act). Maintained via `capture`
after work sessions; validated via `lint` on demand; queried via
`query`.
<!-- kms:end -->
```

The markers let `uninstall` remove exactly this block later without
touching anything else in the file.

### 10. Seed the per-type index

For each of
`docs/{facts,decisions,guardrails,skills}/`, write `INDEX.md` in TOON
format: one row per artifact in that directory (excluding `INDEX.md`
itself and anything under an `archive/` subdirectory) with
fields `id, title, tags, status`, extracted from each file's
frontmatter. Mark it `kms-generated: true` in a leading comment line,
since `uninstall` needs to recognize it as this skill's output. Verify
the current TOON spec before finalizing exact syntax — this step only
fixes the field set and source (frontmatter), not the literal encoding.

## Out of scope

Finalizing decision records, choosing which proposed domains become skills, arbitrating domain conflicts — surface to the team.
