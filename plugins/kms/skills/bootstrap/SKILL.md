---
name: bootstrap
description: One-time setup of a fact/decision/guardrail/procedure knowledge system in a project that has none yet, or a gap-fill pass over one that's incomplete — extract decisions from git history, extract facts from existing docs, audit guardrails for missing derivation, and record fitness functions. Use when the user wants to set up knowledge management for a project, e.g. "bootstrap the knowledge system here", "set up facts/decisions/guardrails for this repo".
---

Set up the knowledge system this plugin's other skills assume: decisions (commitments), facts (what's true), guardrails (what must or must not happen, derived from the first two), procedures (how to act). Run once per project, or as a gap-fill on an incomplete one; `capture` maintains it afterward.

Read first: `shared/artifact-model.md` (schema: types, fields, lifecycle) and `shared/admission.md` (gates and economy rule for the stubs written here).

## How to run

Act; never ask which step to start with or whether to proceed. Read the model, inspect the repo, then do steps 1, 2, 4, 9 and 10 now, writing files directly (your first turn creates files under `docs/`; say in one line first which directories and files you are about to write, and that `uninstall` reverses it). Steps 3, 5, 6, 7 and 8 each ask before writing; batch those asks into one question at the end, after the other steps are done. Finish with step 11 and list what you wrote.

## Before starting

Look for existing `decisions/`, `facts/`, `guardrails/`, `skills/` directories and infer format from real examples (as `decide` does); else use the model's layout under `docs/`. Extend what exists; don't duplicate. Note the highest number in `facts/` and `decisions/` so stubs continue the sequence. Write files directly; extend a file that already covers the ground.

## Steps

### 1. Decision extraction from history

Print `git rev-list --count HEAD`; above 1,000 commits ask how far back to mine (recommend two years). Scan git log and existing docs (README, planning notes, guardrail/skill files) for decision language: markers (`DECISION:`/`RFC:`/`APPROVED:`) or natural language (`why`, `because`, `must`, `never`, `required by`).

- Apply `admission.md` first; skip a finding that fails a hard gate or whose shelf life times recurrence doesn't exceed its rediscovery cost, listing each skip in one line.
- Cluster admitted findings by domain; one stub per cluster: base frontmatter, a one-line motivation, `expires` if bounded or provisional, `status: draft`.
- Flag ambiguous entries inline (`<!-- looks like a decision, could be a behavioral rule — classify before finalizing -->`) rather than guessing.
- Stop at the stub; rationale and tradeoffs belong to the domain owner.

### 2. Fact extraction

Classify every table, value list or configuration default embedded in a procedure or guardrail file; a value restating a decision is not a fact. Apply `admission.md`, then one stub per admitted fact: base frontmatter plus `source` where one exists. Write location or aggregation facts (a path, a count) only when asked, and state the cap.

### 3. Doc manifest

For each human-facing doc (README, planning notes, roadmap, other `docs/` markdown) add a row to `facts/docs-manifest.md` (frontmatter: base fields, `kms-generated: true`, `kms-registry: docs-manifest`) mapping its sections to the content and decisions they describe, plus the watch paths that would make each drift. Leave `last-verified` blank for `capture`. Ask before writing.

### 4. Guardrail derivation audit

For each guardrail missing `governed-by`, `grounded-in` or `derivation-note`: flag it undeclared, propose the likeliest governing decision(s) and grounding fact(s), draft the `derivation-note`, and log it as debt.

### 5. Fitness functions

List rules already enforced (CI/build config, review checklists, approval gates) for confirmation before writing. Add rules in procedure/guardrail files that could be automated but aren't as `{check, enforced-by: none, last-verified}` on the governing decision's `fitness-functions`, or draft a `status: draft` decision stub when none governs. Ask before writing.

### 6. Procedure gap detection

Propose domains needing their own procedure:

| Signal in the repo | Domain to cover | Likely review role |
|---|---|---|
| Build manifests, compiled language | Build tooling, runtime constraints | Build Engineer |
| CI workflows, deployment config | Pipeline structure, release process | Release Engineer |
| Multi-repo boundary, subtree/submodule sync | Integration contracts, public APIs | Architect |
| Test suite, quality gates | Correctness verification, release criteria | QA/Test Owner |
| Roadmap, pricing tiers, access control | Product scope, positioning | Product Strategist |
| Recurring manual process, no written procedure | Process/procedure documentation | Process Owner |
| External compliance, regulatory, or ethical requirement | Compliance/review procedure | Compliance Reviewer |
| Repeated reviewer or stakeholder feedback pattern | Review/quality procedure | Quality Reviewer |
| Data provenance, method choice, literature claim | Sourcing and method rules | Domain Lead |
| Approval or publication gate | Sign-off procedure | Approver |

Per domain: one paragraph on what it owns, one hard constraint, one fitness-function candidate. Proposals only; ask before writing, the team decides adoption and naming. Formalize domains governing irreversible decisions (published APIs, schema changes, legal commitments) first.

### 7. Tag vocabulary

Ask before writing. Compile `docs/skills/tags.md` from every tag already in use (or, in a fresh project, domain vocabulary from existing docs), one per line as `tag — meaning` (the checker also reads `- tag — meaning`, `tag - meaning`, `tag: meaning`). Mark a tag carried by over half of active decisions `(umbrella)`, computed from the scan, since `lint` check 16 excludes umbrella tags. Frontmatter: base fields, `kms-generated: true`, `kms-registry: tags`.

### 8. Seed baseline artifacts

Ask before writing: list the ids with one line each (they are rules about keeping knowledge short, derived and unduplicated; recommend yes when the team will keep using kms, else no). `templates/` has one subdirectory per artifact type kms seeds (currently `guardrails/`). For each template whose `id` is absent from this project's `docs/<type>/` and not in the AGENTS.md block's `kms-declined:` line, write it on a yes: copy as-is, replace `date: TBD` with today, drop `template-version`, add `kms-seeded: true` and `kms-template-version: <its template-version>` right after `date`. On a no, list the ids in the block's `kms-declined:` line. Leave the type's debt-marking fields (per the model, e.g. `governed-by`/`grounded-in` for a guardrail) as `TBD` until the team drafts a decision.

### 9. Wire into the agent-instructions file

If `<!-- kms:start -->` is absent, insert this section into `AGENTS.md` (or the host's equivalent; create a minimal `AGENTS.md` if none). Skip on a repeat run:

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

### 10. Per-type index

For each of `docs/{facts,decisions,guardrails,skills}/`, write `INDEX.md`: one row per artifact (excluding `INDEX.md` and `archive/`), fields `id, title, tags, status` from frontmatter, in the CSV format in `shared/artifact-model.md`: no space after commas, a value with a comma double-quoted, no row for a registry such as `tags.md`. Start the file with the two comment lines `<!-- kms-registry: index -->` and `<!-- kms-generated: true -->` (the second lets `uninstall` recognize it), then the header and rows, e.g. `0001-use-postgres,Use Postgres,"data, storage",active`. Match the shape of any existing `INDEX.md`.

### 11. Check what you wrote

Run `python3 shared/lint_check.py --root .` (this skill's directory; needs `python3` and PyYAML, else say so and skip; add `--docs <dir>` for a non-`docs/` layout). Fix every finding about a file you just wrote; report any other as existing debt.

## Out of scope

Finalizing decision records, choosing which proposed domains become procedures, arbitrating domain conflicts — surface to the team.
