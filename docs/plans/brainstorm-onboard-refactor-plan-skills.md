# Plan: add brainstorm, onboard, refactor-plan skills; ship examples.md repo-wide

## Context (read this before touching anything)

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace with one plugin, `kms`, at
`plugins/kms/`. It ships skills as `plugins/kms/skills/<skill>/SKILL.md`
(plus an optional `agents/openai.yaml` sidecar), and dogfoods its own
knowledge-management system under `docs/{facts,decisions,guardrails,
skills}/` (`docs/decisions/NNNN-slug.md` etc., 4-digit sequential ids
per directory; guardrails/skill-prescriptions have no numeric prefix).
See `AGENTS.md` at the repo root for the full authoritative structure —
read it before making any structural change not covered by this plan.

This plan was produced by a `roadmap`-skill interview (see
`docs/decisions/0018-per-skill-examples-convention.md` through `0021`
for the decisions it recorded). All artifact-writing steps below are
already done as of this plan's creation. What remains, if anything, is
tracked per-step below — re-read this file rather than assuming
anything from a prior conversation.

## Status legend

`done` — file exists and was verified present. `pending` — not yet
created/edited. `blocked` — needs a decision or input before it can
proceed.

## Steps

### 1. Four new decision records — status: done

- `docs/decisions/0018-per-skill-examples-convention.md` (track: process)
  — the repo-wide decision that every skill ships a colocated
  `examples.md`, applied retroactively to all 8 pre-existing skills,
  not just the 3 new ones.
- `docs/decisions/0019-brainstorm-skill.md` (track: process)
- `docs/decisions/0020-onboard-skill.md` (track: process)
- `docs/decisions/0021-refactor-plan-skill.md` (track: process)

Done when: all four files exist with `id/title/status/date/tags/track`
frontmatter and `## Decision` / `## Why` / `## Tradeoffs considered`
sections, matching the shape of `docs/decisions/0016-lint-skill.md` and
`docs/decisions/0017-query-skill.md`.

### 2. New guardrail — status: done

- `docs/guardrails/every-skill-ships-examples.md` — `governed-by:
  0018-per-skill-examples-convention`, `grounded-in: TBD` (no existing
  fact enumerates the skill roster; a future `bootstrap`/`steward` pass
  could generate one). States the requirement is checked by review, not
  by `lint`/`steward`'s automated pass, since both skills' stated scope
  is `docs/{facts,decisions,guardrails,skills}/`, not
  `plugins/kms/skills/` itself — matching how
  `docs/guardrails/plugin-manifest-version-sync.md` is also
  review-checked, not automated.

Done when: the file exists with `governed-by`/`grounded-in`/
`derivation-note` fields, matching the shape of
`docs/guardrails/plugin-manifest-version-sync.md`.

### 3. Three new skills — status: done

- `plugins/kms/skills/brainstorm/SKILL.md` — generative ideation, caps
  at 5-7 approaches with pros/cons/risks/effort, then a `## Synthesis`
  section with 2-3 recommendations. Never reads
  `docs/{facts,decisions,guardrails,skills}/`. Writes nothing.
- `plugins/kms/skills/onboard/SKILL.md` — reads the knowledge base,
  asks for role if not given, warns if critical artifact types
  (especially facts) are missing, produces a 5-day plan (goal / read /
  run per day). Writes nothing.
- `plugins/kms/skills/refactor-plan/SKILL.md` — 4 phases (query
  knowledge base → map dependencies directly, no runtime dependency on
  invoking `lint` → phased steps with verification+rollback → recommend
  post-refactor artifact updates). Flags guardrail conflicts for
  confirmation rather than dropping/working around them silently.
  Writes nothing.

Each has an `agents/openai.yaml` sidecar
(`plugins/kms/skills/<name>/agents/openai.yaml`) with
`interface.display_name`, `interface.short_description`, and
`policy.allow_implicit_invocation: false`, matching every existing
skill's sidecar (see e.g. `plugins/kms/skills/lint/agents/openai.yaml`)
— required by `docs/decisions/0008-native-codex-plugin-support.md`.

Done when: all three `SKILL.md` files and all three
`agents/openai.yaml` sidecars exist.

### 4. Eleven examples.md files — status: done

Colocated `examples.md` (2-3 worked usage examples: trigger prompt +
sketch of what happens) for:
- The 3 new skills: `plugins/kms/skills/{brainstorm,onboard,refactor-plan}/examples.md`
- The 8 pre-existing skills (retrofit, per decision 0018):
  `plugins/kms/skills/{clarify,roadmap,bootstrap,steward,lint,query,attribute,changelog}/examples.md`

Done when: all 11 files exist and each example is grounded in real
behavior from that skill's own `SKILL.md` — not invented behavior.

### 5. Manifest version bump — status: done

Per `docs/guardrails/plugin-manifest-version-sync.md`, both manifests'
`version` moved together from `0.2.1` to `0.3.0`:
- `plugins/kms/.claude-plugin/plugin.json`
- `plugins/kms/.codex-plugin/plugin.json`

Both manifests' `description`, and `.claude-plugin/marketplace.json`'s
top-level and per-plugin `description`, were updated to mention
`brainstorm`/`onboard`/`refactor-plan` alongside the existing 8 skills.

Done when: `python3 -m json.tool` on all three files succeeds, all
three `version` fields read `0.3.0`, and none references only the old
8-skill set in its description.

### 6. README — status: done

`README.md`'s skill table gained 3 new rows (`brainstorm`, `onboard`,
`refactor-plan`) and a third "Examples" column linking every one of the
11 skills' `examples.md`.

Done when: the table has 11 data rows, 3 columns (`Skill` / `What it
does` / `Examples`), and every link resolves to a real file under
`plugins/kms/skills/`.

### 7. CHANGELOG — status: done

`CHANGELOG.md` gained a new `## [0.3.0] - 2026-08-30` section (prepended
above `## [0.2.1]`) with an `### Added` block covering: the 3 new
skills (one bullet each, stating their key constraints — brainstorm
never queries the KB; onboard warns on missing facts; refactor-plan
doesn't runtime-depend on `lint`) and the repo-wide `examples.md`
retrofit + new guardrail.

Done when: the section exists, uses Why-summary style bullets (not raw
commit subject lines), and the version header reads `[0.3.0] -
2026-08-30`.

### 8. AGENTS.md — status: done

- The "What this repo is" section's skill enumeration updated from
  "eight skills" to "eleven skills", inserting `brainstorm` (after the
  intro, before `clarify`, since it's the other write-nothing
  interview-adjacent skill) and `onboard`/`refactor-plan` (after
  `query`, since all three are knowledge-base-consuming skills in that
  cluster).
- The "Structure" code block gained a
  `plugins/<plugin-name>/skills/<skill>/examples.md` line.
- The "Adding a new skill" section gained a paragraph requiring a
  colocated `examples.md`, linked from the README, per the new
  guardrail.

Done when: grepping AGENTS.md for "eight skills" returns nothing, and
"eleven skills" appears with all 11 names present in the enumeration.

## Explicitly not done in this plan (separate, later work)

- **Committing any of this.** The user explicitly asked not to commit
  until asked; this plan's completion does not imply anything was
  committed. Check `git status`/`git log` before assuming otherwise.
- **Running `/code-review`** on this diff was requested separately by
  the user in the same session that approved this plan — track that as
  its own follow-up, not part of this plan's done-criteria.
- Adding `docs/facts/` entries enumerating the full skill roster (the
  guardrail in step 2 notes this as `grounded-in: TBD`) — left as debt
  for a future `bootstrap`/`steward` pass, not this plan's job.
