---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/skill knowledge system — dangling references, stale prose cross-references, missing required fields, numbering collisions, expired decisions, redundant guardrails, audit-log-style facts, and verbosity — independent of what changed this session. Use when the user wants the whole knowledge base checked for health, e.g. "lint the knowledge base", "check the whole docs/ tree for problems".
---

Scan every fact, decision, guardrail, and skill prescription in the project — not just what changed recently — and report every structural violation found. Complements `steward`'s per-session checks with a full, on-demand sweep; `steward` can't catch rot that predates the session it happens to run in.

## What to check

1. **Dangling references** — any `governed-by` or `grounded-in` value pointing at a decision/fact id that doesn't exist.
2. **Missing required fields** — facts without `kind`/`governed-by`; guardrails without `governed-by`/`grounded-in`/`derivation-note`; decisions without `track`.
3. **Numbering collisions or gaps** — duplicate or skipped numbers in `facts/`/`decisions/`.
4. **Expired decisions** — a decision with an `expires` field whose date has passed or condition has plausibly been met, still standing without re-evaluation.
5. **Redundant guardrails** — a guardrail only ever true "whenever skill X does Y," with no claim broader than that skill's own procedure.
6. **Audit-log facts** — a fact that only records a timestamped event, grounds nothing, and is referenced by nothing.
7. **Orphaned artifacts** — a fact or guardrail nothing references at all.
8. **Unenforced guardrails** — a guardrail describing behavior a shipped skill should perform, where that skill's own body doesn't actually say it.
9. **Stale prose references** — any inline mention (not just `governed-by`/`grounded-in` fields, covered by check 1) of a `docs/{facts,decisions,guardrails,skills}/` path that doesn't exist, typically left behind after a rename or deletion. Not a violation: a placeholder pattern (`NNNN-slug.md`), a conditionally-optional file ("if X exists..."), or a reference a plan already annotates as deliberately-preserved history.
10. **Verbose artifacts** — a fact, guardrail, or skill prescription (decisions/plans exempt) saying in several sentences what one would do, or restating something already said elsewhere in the same file — every one of these gets read into an agent's context, so unnecessary length is a real, recurring cost.
11. **Unsplit statements** — a fact, guardrail, or derivation-note doing two distinct things that should be two files.
12. **Baseline guardrails out of sync** — compare this skill's sibling `../../templates/guardrails/` against this project's `docs/guardrails/`, matching by `id`: a template missing here, a `kms-seeded: true` file behind its template's `template-version`, or a `kms-seeded: true` file whose template no longer exists. A file without `kms-seeded: true` is project-owned (possibly a deliberately-detached former template) — never flag it. If proposing a fix, only its `## Guardrail` rule text is ever refreshed from the template — never `## Derivation`/other sections a team has since filled in.

## Output

Group findings by check, one line per violation with the file path and what's wrong. Never silently fix anything — propose the fix and wait for confirmation, the same way every other skill in this plugin defers to the user before writing.

## Out of scope

Fixing anything without confirmation, and judgment calls about domain-specific correctness beyond structural validity (e.g. whether a decision's rationale is actually convincing) — that's what `clarify`/`roadmap`'s interview is for, not a mechanical scan. Also out of scope: `kms`'s own plugin-packaging layer (`plugins/<plugin-name>/skills/*/SKILL.md`, its `examples.md` convention) — that governs how `kms` itself is built, not the target project's knowledge base; see `AGENTS.md`/`CONTRIBUTING.md` for that instead.
