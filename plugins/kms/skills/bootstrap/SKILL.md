---
name: bootstrap
description: One-time setup of a fact/decision/guardrail/procedure knowledge system in a project that has none yet, or a gap-fill pass over one that's incomplete — extract decisions from git history, extract facts from existing docs, audit guardrails for missing derivation, and record fitness functions. Use when the user wants to set up knowledge management for a project, e.g. "bootstrap the knowledge system here", "set up facts/decisions/guardrails for this repo".
---

Set up the knowledge system this plugin's other skills assume: decisions (what the team commits to), facts (what's currently true), guardrails (what must or must not happen, derived from the first two), and procedures (how to act). Run once per project, or as a gap-fill pass on an incomplete one. Once artifacts exist, `capture` maintains them across sessions.

## Artifact model

This skill's siblings `../../shared/artifact-model.md` (the schema: types, fields, lifecycle) and `../../shared/admission.md` (the gates and economy rule for stubs written here) — read both before drafting anything.

## Before starting

Detect what the project already has, the same way `decide` does: look for an existing `decisions/`, `facts/`, `guardrails/`, or `skills/` directory and infer format from real examples there. If none exists, use the layout in the artifact model under `docs/`. Extend what exists; don't duplicate.

Note the highest existing number in `facts/` and `decisions/` so new stubs continue the sequence rather than collide.

Write files directly; extend a file that already covers the same ground.

## Steps

### 1. Decision extraction from history

Print `git rev-list --count HEAD`; above 1,000 commits ask how far back to mine (recommend two years). Scan git log and existing docs (README, planning notes, guardrail/skill files) for decision language: project-specific markers (`DECISION:`/`RFC:`/`APPROVED:`) or natural language (`why`, `because`, `must`, `never`, `required by`).

- Apply `admission.md` to each finding first; skip a finding that fails a hard gate or whose estimated shelf life times recurrence does not exceed its rediscovery cost, and list skipped findings in one line each.
- Cluster the admitted findings by domain; write one decision stub per cluster (base frontmatter per the model, plus a one-line motivation, `expires` if bounded or provisional, `status: draft`).
- Flag ambiguous entries inline (`<!-- looks like a decision, could be a behavioral rule — classify before finalizing -->`) rather than guessing.
- Stop at the stub. Full authorship (rationale, tradeoffs) belongs to the domain that owns the decision.

### 2. Fact extraction

For every table, value list, or configuration default embedded in a skill or guardrail file, classify it; a value that restates a decision is not a fact. Apply `admission.md` here too, then write one fact stub per admitted finding (base frontmatter per the model, plus `source` where one exists). Write location or aggregation facts (a path, a count) only when the user asks, and state the cap.

### 3. Doc manifest bootstrap

For every human-facing doc (README, planning notes, roadmap, other `docs/` markdown), add a row to `facts/docs-manifest.md` (frontmatter: base fields, `kms-generated: true`, `kms-registry: docs-manifest`) mapping the doc's sections to the content and decisions they describe, plus the watch paths that would make each section drift. Leave `last-verified` blank; `capture` fills it in later. Ask before writing.

### 4. Guardrail derivation audit

For every existing guardrail file, check whether `governed-by`, `grounded-in`, and `derivation-note` are present. If any are missing, flag it as undeclared, propose the most likely governing decision(s) and grounding fact(s), and draft the `derivation-note`. Log undeclared guardrails as debt.

### 5. Fitness functions

Scan existing checks (CI/build config, review checklists, approval gates) for rules already enforced, and list them for confirmation before writing. Scan skill/guardrail files for rules that *could* be automated but aren't, and add each as `{check, enforced-by: none, last-verified}` to the governing decision's `fitness-functions` (or draft a `status: draft` decision stub when none governs it).

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
| Data provenance, method choice, literature claim | Sourcing and method rules | Domain Lead |
| Approval or publication gate | Sign-off procedure | Approver |

For each: one paragraph on what it would own, one hard constraint, one fitness-function candidate. Proposals — ask before writing; the team decides adoption and naming. Formalize domains governing irreversible decisions (published APIs, schema changes, legal commitments) first.

### 7. Compile the tag vocabulary

Ask before writing. From the same repo-scan signals, compile
`docs/skills/tags.md`: every tag already used across this project's
artifacts (or, in a fresh project, domain vocabulary drawn from existing
docs), one tag per line as `tag — meaning` (the checker also reads `- tag — meaning`, `tag - meaning` and `tag: meaning`). Mark any tag carried by
over half of active decisions as `(umbrella)` — computed from the
scan, not asserted — since `lint` check 16 excludes umbrella tags from
its contradiction-scoping test. Frontmatter: the base fields plus `kms-generated: true` and `kms-registry: tags`.

### 8. Seed baseline artifacts

This skill's sibling `../../templates/` holds one subdirectory per artifact type kms ships seed content for (currently just `guardrails/`). For each `<type>/` subdirectory and each template not yet present (by `id`) and not listed in the AGENTS.md block's `kms-declined:` line in this project's `docs/<type>/`, write it directly, like any other stub this skill produces: copy the template as-is, replace `date: TBD` with today's date, drop its `template-version` field, and add `kms-seeded: true` and `kms-template-version: <the template's own template-version>`. Leave whichever debt-marking fields apply to that artifact type (see `../../shared/artifact-model.md` — e.g. `governed-by`/`grounded-in` for a guardrail; a fact has none) as `TBD` unless the team later drafts a decision for it.

### 9. Wire into the project's own agent-instructions file

If the `<!-- kms:start -->` marker isn't already present, insert a marked section into the project's `AGENTS.md` (or whatever host-specific equivalent filename it uses instead of that cross-agent convention; create a minimal `AGENTS.md` if neither exists) — this is a gap-fill step like the rest of this skill, not something to duplicate on a repeat run:

```
<!-- kms:start -->
## Knowledge base

This project uses kms's fact/decision/guardrail/procedure knowledge system.
See `docs/{facts,decisions,guardrails,skills}/` — facts (what's true),
decisions (what's committed to and why), guardrails (what must/must not
happen), procedures (how to act). Maintained via `capture`
after work sessions; validated via `lint` on demand; queried via
`query`. Run `conform` before committing. Run `query` before designing
anything that touches a recorded decision.
<!-- kms:end -->
```

The markers let `uninstall` remove exactly this block.

### 10. Seed the per-type index

For each of `docs/{facts,decisions,guardrails,skills}/`, write
`INDEX.md` with one row per artifact in that directory (excluding
`INDEX.md` itself and anything under an `archive/` subdirectory),
fields `id, title, tags, status` extracted from each file's
frontmatter, in the CSV format defined in
`../../shared/artifact-model.md`. Mark it `kms-generated: true` in a
leading comment line, since `uninstall` needs to recognize it as this
skill's output. Match the exact shape of any `INDEX.md` already in
this project if one exists.

## Out of scope

Finalizing decision records, choosing which proposed domains become skills, arbitrating domain conflicts — surface to the team.
