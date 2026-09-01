---
id: taxonomy-and-plan-organization
title: Unify the lifecycle dimension, enforce track exclusivity, exclude plans from the governed model, rename skill prescription to procedure, add lint contradiction/staleness checks
status: pending
date: 2026-09-01
tags: [kms, taxonomy, lifecycle, knowledge-management, refactor]
---

# Unify the lifecycle dimension, enforce track exclusivity, exclude plans from the governed model, rename skill prescription to procedure, add lint contradiction/staleness checks

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace, one plugin (`kms`) at
`plugins/kms/`. See `AGENTS.md` at the repo root for full structure and
conventions before making any change not covered by this plan.

This plan **replaces** an earlier, narrower version of itself (a
taxonomy-only rename plus an unworkable `track: both` addition to plans)
that a `code-review` pass found structurally broken — its Done-when
criteria could never be satisfied given its own sub-steps. A `roadmap`
interview then reopened the underlying model questions properly and
produced four new decisions plus supporting guardrails, already written
to disk:

- `docs/decisions/0037-plans-not-a-governed-artifact-type.md` — a plan
  is not a 5th artifact type; it carries no `track`/`status`/`expires`
  and isn't structurally validated by `lint`.
- `docs/decisions/0038-track-field-mutual-exclusivity.md` — `track` is
  always exactly one of `product`/`process`; `both`/`mixed` is never
  stored, only computed as a rollup.
- `docs/decisions/0039-unify-lifecycle-and-drop-scope.md` — `status`
  becomes one shared enum (`draft | active | superseded | deprecated`)
  across all four governed types; `expires` extends from decision-only
  to all four types; `scope` is dropped; decisions gain
  `superseded-by: <decision-id>`.
- `docs/decisions/0040-lint-contradiction-and-staleness-checks.md` —
  four new `lint` checks (track-exclusivity violations, cross-artifact
  contradiction, stale debt, stale fitness-functions).

Supporting guardrails already written/updated:
`docs/guardrails/lifecycle-status-values.md` (new),
`docs/guardrails/superseded-decision-requires-pointer.md` (new),
`docs/guardrails/decision-track-field.md` (updated — mutual-exclusivity
clause), `docs/guardrails/decision-expires-must-be-reevaluated.md`
(updated — broadened from decision-only to all four types).

**A second `code-review` pass, run after this plan's first draft, found
this replacement reproducing the same defect class it was written to
fix** (an unsatisfiable Done-when, incomplete rename coverage in
`roadmap/SKILL.md`, a `lint` check left un-broadened, a literal-string
match that doesn't survive a line wrap). Every step below already has
those fixes folded in — this is the corrected version; there is no
separate errata list to cross-reference.

**This plan turns the four decisions above into actual file edits.
Nothing below has been executed yet.** Writing the decisions/guardrails
and this plan was `roadmap`'s deliverable; running this plan is a
separate, later action, per that skill's own hard limit ("never execute
the changeset plan yourself").

A cold session can execute every step below by reading only this file
plus the four decisions and four guardrails named above — no other
prior context required.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Retrofit lifecycle fields on existing artifacts — status: pending

Per `docs/decisions/0039-unify-lifecycle-and-drop-scope.md`, migrate
every existing decision and fact off the old ad hoc `status` vocabulary.
Guardrails (13 files) and `docs/skills/` procedures (4 files) already
use `status: active` — do not touch them in this step.

**1a.** In each of these 35 files under `docs/decisions/`, change the
frontmatter line `status: accepted` to `status: active` — edit only the
frontmatter block at the top of the file (between the two `---`
delimiters), and change nothing else in it. In particular,
`0014-decision-scope-and-expires-fields.md`'s body also contains the
illustrative phrase `status: accepted` in prose (discussing what
happens without this mechanism, not in its frontmatter) — leave that
sentence untouched:

`0001-knowledge-artifact-storage-convention.md`,
`0002-commit-pr-attribution-skill-design.md`,
`0003-commit-trailer-traceability.md`,
`0004-conventional-commits-adoption.md`,
`0005-changelog-generation-design.md`,
`0007-claude-md-agents-md-symlink.md`,
`0008-native-codex-plugin-support.md`,
`0009-bootstrap-and-steward-skills.md`,
`0010-decision-track-field.md`,
`0011-kms-domain-agnostic-beyond-software.md`,
`0012-no-redundant-guardrails.md`,
`0013-ai-agent-role-lists-per-track.md`,
`0014-decision-scope-and-expires-fields.md`,
`0015-facts-must-not-be-audit-log-records.md`,
`0016-lint-skill.md`,
`0017-query-skill.md`,
`0018-per-skill-examples-convention.md`,
`0019-brainstorm-skill.md`,
`0020-onboard-skill.md`,
`0021-refactor-plan-skill.md`,
`0022-vivantel-kms-display-name.md`,
`0023-quickstart-skill.md`,
`0024-automate-steward-nudge-hook.md`,
`0025-discoverability-improvements.md`,
`0026-token-economy-guardrail.md`,
`0027-baseline-guardrail-seeding.md`,
`0028-generalize-templates-sync-scope.md`,
`0029-bootstrap-full-traceability.md`,
`0030-uninstall-skill.md`,
`0031-consolidate-kb-checks-rename-capture.md`,
`0032-conform-skill.md`,
`0033-kms-architecture-doc.md`,
`0034-shared-artifact-model.md`,
`0035-native-kilo-code-support.md`,
`0036-standalone-installing-doc.md`.

**1b.** In `docs/decisions/0006-agent-agnostic-scope.md`, change the
frontmatter line `status: superseded by 0008-native-codex-plugin-support`
to two lines:
```
status: superseded
superseded-by: 0008-native-codex-plugin-support
```
Change nothing else in the file.

**1c.** In each of these 8 files under `docs/facts/`, change the
frontmatter line `status: current` to `status: active`. Change nothing
else in any of these files: `0001-kms-skill-names.md`,
`0002-skill-bodies-already-agent-neutral.md`,
`0003-codex-plugin-manifest-schema.md`,
`0004-kms-skill-names-steward-bootstrap.md`,
`0005-vivantel-kms-display-name.md`,
`0006-claude-code-plugin-hooks-mechanism.md`,
`0007-claude-code-plugin-uninstall-lifecycle.md`,
`0008-kilo-code-skills-spec.md`.

Done when: `grep -rn "^status:" docs/decisions/*.md docs/facts/*.md`
shows only `active`, `draft`, `superseded`, or `deprecated` values, and
`docs/decisions/0006-agent-agnostic-scope.md` has both `status:
superseded` and `superseded-by: 0008-native-codex-plugin-support`.

### 2. Rewrite `plugins/kms/shared/artifact-model.md` — status: pending

This is the runtime-operational copy of the artifact-type model, shipped
inside `plugins/kms/` to every adopting project and read by `bootstrap`/
`capture` at runtime (`docs/decisions/0034-shared-artifact-model.md`).
Replace the entire file's content with:

```markdown
## Artifact types

| Type | Mode | Origin | Where | Verified by |
|------|------|--------|-------|-------------|
| Environmental fact | descriptive | original | `facts/` | Observe from the world (tool output, docs, benchmarks) |
| Decision fact | descriptive | original | `facts/` | Check the governing decision is still current |
| Decision | axiomatic | original | `decisions/` | Expert review; immutable once accepted |
| Procedure | procedural | original | `skills/` | Expert review; can be refined |
| Guardrail | normative | derived | `guardrails/` | Re-derive from its sources; compare |

**Mode** is the kind of claim: descriptive — true right now; axiomatic — what the team commits to, with context and rationale; normative — must or must not happen, derived from an axiomatic commitment plus a descriptive fact; procedural — how to decide or act. A procedure covers both a shipped skill's own prescription and a project-specific workflow — both live in `skills/`.

A guardrail is only valid while its sources are current — a source change invalidates it.

## File formats

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md` (4-digit, 1-based, per directory); guardrails and procedures as `docs/{guardrails,skills}/slug.md`, no numeric prefix.

All four carry the base frontmatter `id, title, status, date, tags` — `status` is one of `draft | active | superseded | deprecated` — plus an optional `expires: <date or condition>` (when this stops being current), and these type-specific fields:

For `tags`: if `docs/skills/tags.md` exists, every tag assigned to any of the four types MUST come from it — check each intended tag against the list's stated meanings before writing it. If none fit, propose a new tag (name, one-line meaning, why nothing existing covers it) and get confirmation before using it and adding it to the list.

Fact — add `kind: environmental | decision | derived | mixed` (mixed = file has both; label each section inline) and `governed-by: <decision-id>` (`TBD` = debt).

Guardrail — add `governed-by: <decision-id>`, `grounded-in: <fact-id[, ...]>`, and `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. Missing any of the three = undeclared, flag as debt.

Decision — add `track: product | process` (required, exactly one — never `both`/`mixed`: product = what the project is for and who it serves; process = how it's built, organized, or shipped); `superseded-by: <decision-id>`, required when `status: superseded`; optionally `governed-facts: [<fact-id>, ...]` and `fitness-functions: [<check description>, ...]`.

**Derivation recipe**: `Decision (why) + Fact (what is) → Guardrail (ought)`. The `derivation-note` states that step in one sentence; if either source changes, re-apply and propose updated guardrail text.
```

(Note: the `tags`/`docs/skills/tags.md` paragraph above is what
`docs/decisions/0042-tag-vocabulary-and-scoped-contradiction-check.md`
and `docs/plans/knowledge-base-scale.md` reference — it's included here
because this step already rewrites the whole file; no separate edit to
this file is needed when that plan runs later.)

Done when: the file matches the text above exactly, and
`python3 -c "import re,sys; t=open('plugins/kms/shared/artifact-model.md').read(); sys.exit('scope' in t or 'skill prescription' in t.lower())"`
exits 0 (no leftover `scope` field or old terminology).

### 3. Update `plugins/kms/skills/roadmap/SKILL.md` — status: pending

This file has 5 literal occurrences of "skill prescription" today (in
its frontmatter `description`, its numbering section, its mode list,
and twice in "What must be captured") plus 2 field mentions (`track`
paragraph, "What must be captured") that need generalizing. All 6
sub-edits below must be applied — a prior draft of this step covered
only 4 of them and left the `description` and mode-list occurrences
behind.

**3a.** In the frontmatter `description:` field, replace "guardrails,
skill prescriptions)" with "guardrails, procedures)".

**3b.** Replace this paragraph (under "## Classify at the end, not
during"):
```
Decisions additionally carry a `track`: **product** — what the project
is for and who it serves; or **process** — how it's built, organized,
or shipped. If the decision is bounded or provisional, also note
`scope` (what it applies to) and `expires` (a date or condition — when
it stops being current).
```
with:
```
Decisions additionally carry a `track`: **product** — what the project
is for and who it serves; or **process** — how it's built, organized,
or shipped. Exactly one value, never both. Any of the four types may be
bounded or provisional — note `expires` (a date or condition — when it
stops being current). `status` is one of `draft | active | superseded |
deprecated`; a decision moving to `superseded` also gets
`superseded-by: <decision-id>`. If `docs/skills/tags.md` exists, check
any tag against it before assigning; propose additions there when none
fit.
```

**3c.** In "## Numbering facts and decisions", replace "Guardrails and
skill prescriptions" with "Guardrails and procedures".

**3d.** In the mode list under "## Classify at the end, not during",
replace:
```
- **Procedural** — this is how to decide or act (a skill prescription)
```
with:
```
- **Procedural** — this is how to decide or act (a procedure)
```

**3e.** In "## What must be captured", replace:
```
- Descriptive, Normative, and Procedural decisions are written as real artifacts too (facts, guardrails, skill prescriptions respectively), in the detected format — not just labeled in a summary.
- Facts, guardrails, and skill prescriptions written this way use the shortest phrasing that preserves meaning — decisions and the plan file are exempt.
```
with:
```
- Descriptive, Normative, and Procedural decisions are written as real artifacts too (facts, guardrails, procedures respectively), in the detected format — not just labeled in a summary.
- Facts, guardrails, and procedures written this way use the shortest phrasing that preserves meaning — decisions and the plan file are exempt.
```

**3f.** In "## The changeset implementation plan", after the existing
paragraph ending "...exactly what remains.", insert two new paragraphs:
```
A plan is not a 5th artifact type (`docs/decisions/0037-plans-not-a-governed-artifact-type.md`): it carries no `track`, no `status` from the enum above, and no `expires` — only its own per-step done/pending/blocked legend. The test for which bucket new content belongs in: a procedure doesn't name the specific objects it acts on — those are supplied at invocation. A plan does — it names concrete files, decisions, and steps for one occasion. If a candidate procedure hardcodes the files/decisions it will always act on, it's actually a plan.

Before finalizing this file, verify each step's Done-when against the actual current content of the files it names — not from memory or assumption. A Done-when that can't be satisfied by its own preceding steps is a defect in the plan itself, the same as any other error.
```

Done when: all six edits (3a–3f) are applied verbatim and
`grep -c "skill prescription" plugins/kms/skills/roadmap/SKILL.md`
prints `0`.

### 4. Update `plugins/kms/skills/bootstrap/SKILL.md` — status: pending

**4a.** Replace the opening paragraph's "...and skill prescriptions
(how to act)." with "...and procedures (how to act)."

**4b.** In step 1 ("Intent extraction from history"), replace:
```
- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `track: product | process` (add `scope`/`expires` if the decision is bounded or provisional), `status: draft`.
```
with:
```
- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `track: product | process` (exactly one), `expires` if bounded or provisional, `status: draft`.
```

**4c.** In step 7's role-list compilation step, replace "like any other
skill prescription, then one" with "like any other procedure, then
one".

**4d.** In step 9's `AGENTS.md` wiring block, replace "skill
prescriptions (how to act)" with "procedures (how to act)".

Done when: all four edits are applied verbatim and
`grep -c "skill prescription" plugins/kms/skills/bootstrap/SKILL.md`
prints `0`.

### 5. Update `plugins/kms/skills/capture/SKILL.md` — status: pending

`docs/guardrails/superseded-decision-requires-pointer.md` requires any
decision with `status: superseded` to also carry `superseded-by`. Today
nothing in `capture`'s own workflow ever sets it — check 1 drafts a new
decision but never touches the decision it replaces, which is exactly
the moment supersession is known.

Replace check 1 in "## Checks, one pass per invocation":
```
1. **New decision?** Draft a stub: next id, title, one-line motivation, `track: product | process`, `status: draft`. Don't finalize without the owning domain's sign-off.
```
with:
```
1. **New decision?** Draft a stub: next id, title, one-line motivation, `track: product | process`, `status: draft`. Don't finalize without the owning domain's sign-off. If this decision explicitly replaces an existing one, also update that decision's `status` to `superseded` and add `superseded-by: <new-decision-id>` — don't leave two `active` decisions on the same topic for a later `lint` pass to catch.
```

Done when: the edit is applied verbatim and no other check's number
changed.

### 6. Update `plugins/kms/skills/lint/SKILL.md` — status: pending

**6a.** Replace the opening line "Scan every fact, decision, guardrail,
and skill prescription in the project" with "Scan every fact, decision,
guardrail, and procedure in the project".

**6b.** In check 2 ("Missing required fields"), replace:
```
2. **Missing required fields** — facts without `kind`/`governed-by`; guardrails without `governed-by`/`grounded-in`/`derivation-note`; decisions without `track`.
```
with:
```
2. **Missing required fields** — facts without `kind`/`governed-by`; guardrails without `governed-by`/`grounded-in`/`derivation-note`; decisions without `track`; any of the four types with a `status` value outside `draft | active | superseded | deprecated`; a decision `status: superseded` without `superseded-by`.
```

**6c.** In check 1 ("Dangling references"), replace:
```
1. **Dangling references** — any `governed-by` or `grounded-in` value pointing at a decision/fact id that doesn't exist.
```
with:
```
1. **Dangling references** — any `governed-by`, `grounded-in`, or `superseded-by` value pointing at a decision/fact id that doesn't exist.
```

**6d.** Replace check 4 ("Expired decisions"):
```
4. **Expired decisions** — a decision with an `expires` field whose date has passed or condition has plausibly been met, still standing without re-evaluation.
```
with:
```
4. **Expired decisions** — any of the four governed types carrying an `expires` field whose date has passed or condition has plausibly been met, still standing without re-evaluation (`docs/decisions/0039-unify-lifecycle-and-drop-scope.md` extends `expires` beyond decisions).
```

**6e.** In check 10 ("Verbose artifacts"), replace "a fact, guardrail,
or skill prescription (decisions/plans exempt)" with "a fact, guardrail,
or procedure (decisions/plans exempt)".

**6f.** Immediately after check 14, insert four new checks:
```
15. **Track exclusivity violation** — a `track` field storing a literal `both`/`mixed`/similar value instead of exactly one of `product`/`process` (`docs/decisions/0038-track-field-mutual-exclusivity.md`).
16. **Cross-artifact contradiction** — two `status: active` decisions, or a decision and a guardrail derived from it, making contradictory claims on overlapping subject matter, anywhere in the project's history — not just what one session just produced. (`docs/plans/knowledge-base-scale.md`, if executed, narrows this check to tag-scoped pairs — see that plan before applying this check as written if it has already run.)
17. **Stale unresolved debt** — a `governed-by: TBD`, `grounded-in: TBD`, or `status: draft` marker that has sat unresolved a long time, judged the same relative way check 14 judges a role gone cold.
18. **Stale fitness-functions** — a decision's declared `fitness-functions` entries that haven't been verified or re-checked in a long time.
```

**6g.** In "## Out of scope", after the existing paragraph, add a new
sentence: "Also out of scope: `docs/plans/` — a plan is not a governed
artifact type (`docs/decisions/0037-plans-not-a-governed-artifact-type.md`)
and isn't structurally validated here; it keeps only its own per-step
done/pending/blocked legend."

Done when: all seven edits (6a–6g) are applied verbatim; the checklist
runs 1 through 18 with no gaps; `grep -c "skill prescription"
plugins/kms/skills/lint/SKILL.md` prints `0`.

### 7. Update `plugins/kms/skills/lint/examples.md` — status: pending

Replace "Every fact, decision, guardrail, and skill prescription is
scanned" with "Every fact, decision, guardrail, and procedure is
scanned".

Done when: the edit is applied verbatim.

### 8. Update `docs/skills/kms-architecture.md` — status: pending

**8a.** Replace "For the 4-artifact-type model itself (fact/decision/
guardrail/skill prescription, their fields, the derivation recipe)"
with "For the 4-artifact-type model itself (fact/decision/guardrail/
procedure, their fields, the derivation recipe)".

**8b.** Immediately after the paragraph just edited in 8a (the "For the
4-artifact-type model itself..." paragraph) and before the next section
heading ("## Marker conventions"), add a new paragraph:
```
A plan (`docs/plans/<slug>.md`, produced by `roadmap`) is not a 5th layer or artifact type (`docs/decisions/0037-plans-not-a-governed-artifact-type.md`). The four governed types are all parametric — a decision, guardrail, fact, or procedure states a general claim without naming the specific objects it acts on. A plan is fully applied — it names concrete files, decisions, and steps for one occasion, which is why it's disposable where the four types are durable, and why `lint` doesn't structurally validate it the way it validates them.
```

(This is anchored to the paragraph from 8a, not to the preceding
`plugins/kms/hooks/` bullet, because that paragraph — not the bullet —
is the section's actual last content before the next heading.)

Done when: both edits are applied verbatim, in that order.

### 9. Update `README.md` — status: pending

In the `roadmap` row of the skills table, replace "(facts, decisions,
guardrails, skill prescriptions)" with "(facts, decisions, guardrails,
procedures)".

Done when: the edit is applied verbatim. (Do not touch
`CHANGELOG.md:111` — historical record, left as-is per
`docs/decisions/0031-consolidate-kb-checks-rename-capture.md`'s own
precedent for not rewriting history.)

### 10. Update the token-economy guardrail pair — status: pending

Two files carry the same "skill prescription" wording and must stay in
sync (`docs/guardrails/token-economy.md` is `kms-seeded: true` from
`plugins/kms/templates/guardrails/token-economy.md`, per `lint` check
12). Apply the same rename to both.

**10a.** `docs/guardrails/token-economy.md`:
- In the frontmatter `title`, replace "skill prescription" with
  "procedure".
- In the `derivation-note`, replace "any fact, guardrail, or skill
  prescription" with "any fact, guardrail, or procedure" (this
  occurrence is on one line in the current file).
- In "## Guardrail", replace "Every fact, guardrail, and skill
  prescription" with "Every fact, guardrail, and procedure".
- In "## Derivation"'s normative-conclusion bullet, this occurrence
  currently wraps across two lines — "...any fact, guardrail, or
  skill\n  prescription in a project's own..." (the word "skill" ends
  one line, "prescription" starts the next). Match on content, not
  exact line breaks: replace that two-line span with "procedure",
  producing "...any fact, guardrail, or procedure in a project's
  own...".

**10b.** `plugins/kms/templates/guardrails/token-economy.md`: in the
frontmatter `title`, replace "skill prescription" with "procedure". In
"## Guardrail", replace "Every fact, guardrail, and skill prescription"
with "Every fact, guardrail, and procedure".

Done when: both edits are applied verbatim and the two files' `##
Guardrail` sections differ only in the wording `lint` check 12 already
permits to differ between a seeded file and its template (i.e., no new
divergence introduced).

### 11. Verify — status: pending

**11a.** Run `lint` against this repo's own knowledge base. Confirm zero
new violations beyond any pre-existing, already-known debt (`TBD`
markers, etc.) — every check from 1 through 18 should pass on the
retrofitted artifacts.

**11b.** Run `grep -rl "skill prescription" --include="*.md" . | grep -v
"^\./docs/plans/"` from the repo root. `docs/plans/` is excluded
entirely from this check: plans aren't governed artifacts
(`docs/decisions/0037-plans-not-a-governed-artifact-type.md`), so their
own prose is out of scope here — this covers both this plan and
`docs/plans/knowledge-base-scale.md` (which necessarily quote the
phrase while documenting the rename itself) and the pre-existing
historical plan `docs/plans/product-process-track-and-domain-agnostic-scope.md`
(already meant to be left untouched per `docs/decisions/0031`'s
precedent, regardless of this exclusion). Confirm the result is exactly
these two files, both historical records left deliberately unrewritten:
- `CHANGELOG.md`
- `docs/decisions/0026-token-economy-guardrail.md`

Done when: 11a and 11b both hold.

## Explicitly out of scope for this plan

- **Adopting a reproducible eval harness** (e.g. `promptfoo`) to compare
  `lint`/`capture`/`roadmap` behavior before and after a change to this
  repo's own skill bodies or artifact model. Logged as a
  `fitness-functions` entry on `docs/decisions/0040-...` — this repo has
  zero CI, zero package manager, and zero dependencies today, so
  adopting one is an infrastructure decision in its own right, deserving
  its own interview and plan, not a rider on this one. Git already
  preserves this plan's pre-execution commit as a valid "before"
  snapshot regardless of when that lands.
- **Splitting `status: draft` into finer sub-states** (e.g. "drafted,
  not yet reviewed" vs. "under review, awaiting sign-off"). Considered
  and declined during the interview — this is workflow/kanban tracking,
  not knowledge management, the same category of scope this plan's
  decisions already keep out (see `docs/decisions/0037-...`'s discussion
  of the idea→goal→plan pipeline).
- **A `reviewed-by`/`owner` field** linking a decision to which
  `docs/skills/{product,process}-track-roles.md` role(s) actually
  weighed in on it. Noted during the interview as a real but optional
  completeness gap — `docs/decisions/0013-ai-agent-role-lists-per-track.md`'s
  role lists remain informal context `roadmap` surfaces, not a
  structured link. Not actioned here; revisit only if it becomes a
  practical problem.
- **The per-type `INDEX.md`, archive mechanism, and canonical tag
  vocabulary** — a separate `roadmap` interview and plan
  (`docs/plans/knowledge-base-scale.md`, `docs/decisions/0041-...`,
  `0042-...`), which has a hard dependency on this plan executing first
  (it edits check 16 and skill-body wording this plan produces).
- Physically reorganizing `docs/plans/` into subdirectories — no longer
  relevant now that plans are explicitly out of the governed model
  (`docs/decisions/0037-...`); nothing about their storage location
  needed to change.
- Committing or pushing — not requested; check `git status`/`git log`
  before assuming otherwise.
