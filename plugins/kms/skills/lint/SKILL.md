---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/procedure knowledge system — dangling references, stale prose cross-references, missing required fields, numbering collisions, expired decisions, redundant guardrails, audit-log-style facts, verbosity, and stale derived artifacts — independent of what changed this session. Use when the user wants the whole knowledge base checked for health, e.g. "lint the knowledge base", "check the whole docs/ tree for problems".
---

Scan every fact, decision, guardrail and procedure, not just recent changes, and report each violation. `capture` handles what a session just produced; this is everything else, checked here only.

Checks scan the live set; `archive/` is excluded unless a deep pass is requested, except checks 1 and 19, which always include it. For a large corpus, scope judgment checks to files changed since a ref the user names (`git diff --name-only <ref>`).

## Run the checker first

Run `python3 <checker> --root <project root>` before anything else (needs PyYAML; add `--docs <dir>` if the knowledge directory is not `docs/`). `<checker>` is `shared/lint_check.py` two directories above this skill's directory; else `find . ~ -name lint_check.py`. It does checks 1, 2, 3, 4, 7, 9, 12, 17, 18, 19, 20, 21, 24, 25 and the pinned part of 13 (`pinned` map; see `../../shared/artifact-model.md`), printing `check N: <file>: <problem>` per violation, exit 1 if any. Report its lines as findings; don't re-derive or second-guess them, and don't skip a check because its list is empty. If it can't run, say so and do those checks by hand. Every other check is yours to judge, including 13 for unpinned edges.

Check 9 skips placeholders (`NNNN`) and decision files but reports a conditionally-optional file or a reference a plan annotates as preserved history; dismiss those two when presenting.

## Checks

Edge and field rules are in `../../shared/artifact-model.md`.

1. **Dangling references** [structural] — `governed-by`, `grounded-in`, `superseded-by`, `governed-facts` or `operationalizes` naming an id that doesn't exist (targets typed per the model).
2. **Missing required fields** [structural] — base frontmatter (`id`, `title`, `status`, `date`, `tags`) absent; guardrail without `governed-by`/`grounded-in`/`derivation-note`; `status` outside `draft | active | superseded | deprecated`; decision `superseded` without `superseded-by`; `scope` not a non-empty `component | environment | version` string mapping, or on a non-fact; `grounded-in`/`governed-facts`/`operationalizes` not a YAML list.
3. **Numbering collisions** [structural] — duplicate numbers in `facts/` or `decisions/`; skipped numbers advisory only.
4. **Expired** [structural for `expires`, judgment for `expires-when`] — a governed artifact past `expires`, or whose `expires-when` has plausibly been met, still standing without re-evaluation.
5. **Redundant guardrails** [advisory] — true only "whenever skill X does Y", no claim broader than that skill's procedure.
6. **Audit-log facts** [advisory] — a timestamped event that grounds and is referenced by nothing.
7. **Orphans** [structural] — a fact or guardrail nothing references.
8. **Unenforced guardrails** [advisory] — describes behavior a shipped skill should perform that its body doesn't say.
9. **Stale prose references** [structural] — an inline `docs/{facts,decisions,guardrails,skills}/` path (optionally with `archive/`) that doesn't exist, in a live artifact, `README.md`, `AGENTS.md`, `CONTRIBUTING.md` or a live `docs/plans/*.md`. Not a violation: placeholders, conditionally-optional files, history a plan annotates as preserved.
10. **Verbose artifacts** [advisory] — a fact, guardrail or procedure (not decisions/plans) using several sentences for one idea, or restating itself.
11. **Unsplit statements** [advisory] — one fact, guardrail or derivation-note doing two jobs.
12. **Baseline out of sync** [structural] — compare each `../../templates/<type>/` with this project's `docs/<type>/` by `id`: a template missing here (unless in the AGENTS.md block's `kms-declined:` line); a `kms-seeded: true` file behind its `template-version`, or whose template is gone. Files without `kms-seeded: true` are project-owned; never flag. A fix refreshes only the content section (guardrail: `## Guardrail`), never `## Derivation`.
13. **Derived artifact stale** [judgment] — a guardrail grounded in a since-superseded decision, changed fact, or superseded/deprecated/changed sibling guardrail. A source already flagged by a `pinned` mismatch is the checker's finding. Re-apply the derivation recipe and propose new text.
14–15. *(retired; numbers unused)*
16. **Cross-artifact contradiction** [advisory] — two `active` decisions, or a decision and its derived guardrail, sharing a non-`(umbrella)` tag from `docs/skills/tags.md` and contradicting on overlapping matter.
17. **Stale unresolved debt** [structural] — `governed-by: TBD`, `grounded-in: TBD` or `status: draft` older than 180 days (the model's stale threshold), except a draft with `expires-when` (an open question).
18. **Stale fitness-functions** [structural] — an entry with no `last-verified`, or older than the threshold.
19. **Index out of sync** [structural] — an `INDEX.md` (live or `archive/`) missing a row for a file in its directory, holding a row for a missing file, or whose `id`/`title`/`tags`/`status` differ from frontmatter.
20. **Archive candidate** [structural] — a `superseded` or `deprecated` artifact still live. Propose moving it to `archive/` (name and `id` unchanged), moving its index row, and updating path references elsewhere except inside decision files (frozen history).
21. **Tag off the list** [structural] — a tag in use not in `docs/skills/tags.md`, when that file exists.
22. **Tag gone cold** [judgment] — a listed tag unused by any artifact for a long time.
23. **Unoperationalized guardrail** [judgment] — a guardrail describing a recurring or multi-step action (not a one-line prohibition) that no procedure's `operationalizes` points to and nothing else (CI, hook, skill logic) already carries out. "Never commit secrets" never triggers; "every release must be tagged" does, unless enforced.
24. **Completed plan not archived** [structural] — a live `docs/plans/*.md` whose step legend shows every step `done`. The only plan check; it reads just the legend. Propose moving to `docs/plans/archive/` (a plan without frontmatter first gets minimal frontmatter).
25. **Stale or unverified fact** [structural] — a fact whose `source` is a URL or command and `last-verified` is past the threshold, or whose `source` is a repo path that no longer exists; no `last-verified` is reported once as "never verified" (advisory).

## Output

Group by check, one line per violation: path and problem; label judgment checks "advisory". Never fix silently: propose and wait for confirmation.

## Out of scope

Fixing without confirmation; domain-specific correctness beyond structure (that's `decide`'s interview); `kms`'s own packaging layer (`plugins/*/skills/*/SKILL.md`); `docs/plans/` beyond check 24.
