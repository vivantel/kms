---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/skill knowledge system — dangling references, stale prose cross-references, missing required fields, numbering collisions, expired decisions, redundant guardrails, audit-log-style facts, verbosity, and stale derived artifacts — independent of what changed this session. Use when the user wants the whole knowledge base checked for health, e.g. "lint the knowledge base", "check the whole docs/ tree for problems".
---

Scan every fact, decision, guardrail, and procedure in the project — not just what changed recently — and report every structural violation found. `capture` handles what a session just produced (new decisions, changed facts, contradictions, doc drift); this is everything else — the whole knowledge base's structural health, checked here and only here.

The default invocation's *health* checks (verbosity, staleness, contradiction-scanning) scan only the live set — artifacts under `docs/<type>/archive/` are excluded unless a deep pass is explicitly requested. This exclusion does NOT apply to check 1 (dangling references): resolving whether a `governed-by`/`grounded-in`/`superseded-by` id exists always searches both the live directory and its `archive/` subdirectory, otherwise archiving an artifact would immediately turn every reference to it into a false-positive dangling reference.

## What to check

1. **Dangling references** — any `governed-by`, `grounded-in`, or `superseded-by` value pointing at a decision/fact id that doesn't exist.
2. **Missing required fields** — facts without `kind`/`governed-by`; guardrails without `governed-by`/`grounded-in`/`derivation-note`; decisions without `track`; any of the four types with a `status` value outside `draft | active | superseded | deprecated`; a decision `status: superseded` without `superseded-by`.
3. **Numbering collisions or gaps** — duplicate or skipped numbers in `facts/`/`decisions/`.
4. **Expired decisions** — any of the four governed types carrying an `expires` field whose date has passed or condition has plausibly been met, still standing without re-evaluation.
5. **Redundant guardrails** — a guardrail only ever true "whenever skill X does Y," with no claim broader than that skill's own procedure.
6. **Audit-log facts** — a fact that only records a timestamped event, grounds nothing, and is referenced by nothing.
7. **Orphaned artifacts** — a fact or guardrail nothing references at all.
8. **Unenforced guardrails** — a guardrail describing behavior a shipped skill should perform, where that skill's own body doesn't actually say it.
9. **Stale prose references** — any inline mention (not just `governed-by`/`grounded-in` fields, covered by check 1) of a `docs/{facts,decisions,guardrails,skills}/` path that doesn't exist, typically left behind after a rename or deletion. Not a violation: a placeholder pattern (`NNNN-slug.md`), a conditionally-optional file ("if X exists..."), or a reference a plan already annotates as deliberately-preserved history.
10. **Verbose artifacts** — a fact, guardrail, or procedure (decisions/plans exempt) saying in several sentences what one would do, or restating something already said elsewhere in the same file — every one of these gets read into an agent's context, so unnecessary length is a real, recurring cost.
11. **Unsplit statements** — a fact, guardrail, or derivation-note doing two distinct things that should be two files.
12. **Baseline artifacts out of sync** — this skill's sibling `../../templates/` has one subdirectory per artifact type (currently just `guardrails/`); for each `<type>/`, compare it against this project's `docs/<type>/`, matching by `id`: a template missing here, a `kms-seeded: true` file behind its template's `template-version`, or a `kms-seeded: true` file whose template no longer exists. A file without `kms-seeded: true` is project-owned (possibly a deliberately-detached former template) — never flag it. If proposing a fix, only the section stating the artifact's actual content (for a guardrail, `## Guardrail`) is ever refreshed from the template — never `## Derivation` or any other section a team has since filled in beyond the template's own `TBD`.
13. **Derived artifact stale** — a guardrail grounded in a decision that's since been superseded, or a fact that's since changed, anywhere in the project's history — not just from this session. Re-apply the derivation recipe and propose updated text; never leave a stale norm standing silently.
14. **Role list gone cold** — a role on `docs/skills/{product,process}-track-roles.md` that hasn't matched any decision in a long while, judged against the project's whole decision history, not just recent ones.
15. **Track exclusivity violation** — a `track` field storing a literal `both`/`mixed`/similar value instead of exactly one of `product`/`process`.
16. **Cross-artifact contradiction** — two `status: active` decisions, or a decision and a guardrail derived from it, sharing at least one non-`(umbrella)` tag from `docs/skills/tags.md`, making contradictory claims on overlapping subject matter — anywhere in the project's history, not just this session. A tag marked `(umbrella)` (over half of active decisions) never counts as the shared tag, bounding the comparison by cluster size rather than the full corpus.
17. **Stale unresolved debt** — a `governed-by: TBD`, `grounded-in: TBD`, or `status: draft` marker that has sat unresolved a long time, judged the same relative way check 14 judges a role gone cold.
18. **Stale fitness-functions** — a decision's declared `fitness-functions` entries that haven't been verified or re-checked in a long time.
19. **Index out of sync** — any type's `INDEX.md` missing a row for a file that exists in its directory, containing a row for a file that doesn't, or a row whose `id`/`title`/`tags`/`status` no longer matches that file's frontmatter.
20. **Archive candidate** — a `status: superseded` or `status: deprecated` artifact still in its live directory (not yet under `docs/<type>/archive/`) — propose moving it, filename and `id` unchanged, and updating any literal (non-id) path references elsewhere in the repo to the new path.
21. **Tag off the list** — a tag in use on any of the four types that isn't in `docs/skills/tags.md`, when that file exists (`docs/guardrails/tags-from-canonical-list.md`).
22. **Tag gone cold** — a tag on `docs/skills/tags.md` unused by any artifact in a long time, judged the same relative way check 14 judges a role gone cold.

## Output

Group findings by check, one line per violation with the file path and what's wrong. Never silently fix anything — propose the fix and wait for confirmation, the same way every other skill in this plugin defers to the user before writing.

## Out of scope

Fixing anything without confirmation, and judgment calls about domain-specific correctness beyond structural validity (e.g. whether a decision's rationale is actually convincing) — that's what `clarify`/`roadmap`'s interview is for, not a mechanical scan. Also out of scope: `kms`'s own plugin-packaging layer (`plugins/<plugin-name>/skills/*/SKILL.md`, its `examples.md` convention) — that governs how `kms` itself is built, not the target project's knowledge base; see `AGENTS.md`/`CONTRIBUTING.md` for that instead. Also out of scope: `docs/plans/` — a plan is not a governed artifact type and isn't structurally validated here; it keeps only its own per-step done/pending/blocked legend.
