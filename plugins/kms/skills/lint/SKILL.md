---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/procedure knowledge system — dangling references, stale prose cross-references, missing required fields, numbering collisions, expired decisions, redundant guardrails, audit-log-style facts, verbosity, and stale derived artifacts — independent of what changed this session. Use when the user wants the whole knowledge base checked for health, e.g. "lint the knowledge base", "check the whole docs/ tree for problems".
---

Scan every fact, decision, guardrail, and procedure in the project — not just what changed recently — and report every structural violation found. `capture` handles what a session just produced (new decisions, changed facts, contradictions, doc drift); this is everything else — the whole knowledge base's structural health, checked here and only here.

Health checks scan only the live set; `archive/` is excluded unless a deep pass is requested. Checks 1 and 19 always include `archive/`, so archiving never creates dangling references and archive indexes get synced. For a large corpus, scope the judgment checks to files changed since a ref the user names (`git diff --name-only <ref>`).

## Run the checker first

Run `python3 <checker> --root <project root>` (add `--docs <dir>` if the knowledge directory is not `docs/`; needs PyYAML) before anything else, where `<checker>` is `shared/lint_check.py` two directories above this skill's own directory, resolved to a path from the project root; if it is not there, `find . ~ -name lint_check.py` locates it. It performs checks 1, 2, 3, 4, 7, 9, 12, 17, 18, 19, 20, 21, 24 and 25 deterministically, plus the part of check 13 that covers pinned edges (a `pinned` map in a file's frontmatter; see `../../shared/artifact-model.md`) and prints one `check N: <file>: <problem>` line per violation, exit status 1 if any. Report those lines as that check's findings; do not re-derive or second-guess them by reading the files, and do not skip a check because its list is empty. If it cannot run, say so and do those checks by hand per the definitions below. Every other check is yours to judge, including check 13 for edges that carry no pin.

Check 9 skips placeholders (`NNNN`) and decision files, but reports a conditionally-optional file or a reference a plan annotates as preserved history — dismiss those two when presenting.

## What to check

1. **Dangling references** [structural] — any `governed-by`, `grounded-in`, `superseded-by`, or `governed-facts` value pointing at an id that doesn't exist (`governed-by` and `superseded-by` resolve to decisions, `grounded-in` to facts, `operationalizes` to guardrails; per `../../shared/artifact-model.md`).
2. **Missing required fields** [structural] — any of the four types missing base frontmatter (`id`, `title`, `status`, `date`, `tags`); guardrails without `governed-by`/`grounded-in`/`derivation-note`; any of the four types with a `status` value outside `draft | active | superseded | deprecated`; a decision `status: superseded` without `superseded-by`; a `scope` that is not a non-empty mapping over `component | environment | version` with string values, or that sits on anything but a fact; a `grounded-in`/`governed-facts`/`operationalizes` value that isn't a YAML list (even a single-entry one), per `../../shared/artifact-model.md`.
3. **Numbering collisions** [structural] — duplicate numbers in `facts/`/`decisions/`; skipped numbers are advisory only.
4. **Expired decisions** [structural for `expires`, judgment for `expires-when`] — any of the four governed types whose `expires` date has passed, or whose `expires-when` condition has plausibly been met, still standing without re-evaluation.
5. **Redundant guardrails** [advisory] — a guardrail only ever true "whenever skill X does Y," with no claim broader than that skill's own procedure.
6. **Audit-log facts** [advisory] — a fact that only records a timestamped event, grounds nothing, and is referenced by nothing.
7. **Orphaned artifacts** [structural] — a fact or guardrail nothing references at all.
8. **Unenforced guardrails** [advisory] — a guardrail describing behavior a shipped skill should perform, where that skill's own body doesn't actually say it.
9. **Stale prose references** [structural] — any inline mention (not just `governed-by`/`grounded-in` fields, covered by check 1) of a `docs/{facts,decisions,guardrails,skills}/` path (optionally with `archive/`) that doesn't exist, in any live artifact, `README.md`, `AGENTS.md`, `CONTRIBUTING.md` or a live `docs/plans/*.md`, typically left behind after a rename or deletion. Not a violation: a placeholder pattern (`NNNN-slug.md`), a conditionally-optional file ("if X exists..."), or a reference a plan already annotates as deliberately-preserved history.
10. **Verbose artifacts** [advisory] — a fact, guardrail, or procedure (decisions/plans exempt) saying in several sentences what one would do, or restating something already said elsewhere in the same file.
11. **Unsplit statements** [advisory] — a fact, guardrail, or derivation-note doing two distinct things that should be two files.
12. **Baseline artifacts out of sync** [structural] — this skill's sibling `../../templates/` has one subdirectory per artifact type (currently just `guardrails/`); for each `<type>/`, compare it against this project's `docs/<type>/`, matching by `id`: a template missing here (unless its id is in the AGENTS.md block's `kms-declined:` line), a `kms-seeded: true` file behind its template's `template-version`, or a `kms-seeded: true` file whose template no longer exists. A file without `kms-seeded: true` is project-owned (possibly a deliberately-detached former template) — never flag it. A fix refreshes only the section stating the artifact's content (for a guardrail, `## Guardrail`), never `## Derivation` or other filled-in sections.
13. **Derived artifact stale** [judgment] — a guardrail grounded in a decision that's since been superseded, a fact that's since changed, or a sibling guardrail that's since been superseded/deprecated or itself changed, A source the checker already flagged through a `pinned` mismatch is reported as the checker's finding, not re-judged. Re-apply the derivation recipe and propose updated text.
14. *(retired; the number stays unused)*
15. *(retired; the number stays unused)*
16. **Cross-artifact contradiction** [advisory] — two `status: active` decisions, or a decision and a guardrail derived from it, sharing at least one non-`(umbrella)` tag from `docs/skills/tags.md`, making contradictory claims on overlapping subject matter. A tag marked `(umbrella)` never counts as the shared tag.
17. **Stale unresolved debt** [structural] — a `governed-by: TBD`, `grounded-in: TBD`, or `status: draft` marker older than the stale threshold (180 days, per the artifact model), except a draft carrying `expires-when` (an open question).
18. **Stale fitness-functions** [structural] — a decision's `fitness-functions` entry with no `last-verified` date, or one older than the stale threshold.
19. **Index out of sync** [structural] — any type's `INDEX.md`, live or under `archive/`, missing a row for a file that exists in that same directory, containing a row for a file that doesn't, or a row whose `id`/`title`/`tags`/`status` no longer matches that file's frontmatter.
20. **Archive candidate** [structural] — a `status: superseded` or `status: deprecated` artifact still in its live directory (not yet under `docs/<type>/archive/`) — propose moving it (filename and `id` unchanged), moving its index row to that type's `archive/INDEX.md`, and updating literal path references to it elsewhere, except inside other decision files (their frozen text stays as history).
21. **Tag off the list** [structural] — a tag in use on any of the four types that isn't in `docs/skills/tags.md`, when that file exists.
22. **Tag gone cold** [judgment] — a tag on `docs/skills/tags.md` unused by any artifact in a long time.
23. **Unoperationalized guardrail** [judgment] — a guardrail whose own text describes a recurring or multi-step action (not a simple one-line prohibition), where no procedure's `operationalizes` field points back at it *and* nothing else already carries it out. "Never commit secrets" never triggers this; "every release must be tagged" does — unless code (CI, a hook, a skill's own logic) already enforces it.
24. **Completed plan not archived** [structural] — a `docs/plans/*.md` file whose own per-step legend shows every step `done` (no `pending`/`blocked` remaining), still sitting in the live `docs/plans/` directory rather than `docs/plans/archive/`. The only plan check `lint` performs: it reads just the plan's step legend. Propose the move (filename and `id`, if any, unchanged); a plan with no frontmatter is proposed for a minimal frontmatter addition first.
25. **Stale or unverified fact** [structural] — a fact whose `source` is a URL or command and whose `last-verified` is older than the stale threshold, or whose `source` is a repo path that no longer exists; a fact with no `last-verified` is reported once as "never verified" (advisory).

## Output

Group findings by check, one line per violation with the file path and what's wrong; label judgment checks "advisory". Never silently fix anything — propose the fix and wait for confirmation, the same way every other skill in this plugin defers to the user before writing.

## Out of scope

Fixing anything without confirmation, and judgment calls about domain-specific correctness beyond structural validity (e.g. whether a decision's rationale is actually convincing) — that's what `decide`'s interview is for. Also out of scope: `kms`'s own plugin-packaging layer (`plugins/<plugin-name>/skills/*/SKILL.md`) and `docs/plans/` (not a governed type; only check 24 reads its step legend).
