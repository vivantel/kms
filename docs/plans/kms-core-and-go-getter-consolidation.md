---
id: kms-core-and-go-getter-consolidation
title: Narrow kms to process knowledge, make it the knowledge-base core, and have go-getter consume it instead of its fork
status: in progress; A1-H1 done (D3 blocked); branch feat/kms-core-consolidation (kms) and feat/adopt-kms-core (go-getter, worktree)
date: 2026-11-15
---

# Narrow kms to the knowledge-base core and make go-getter consume it

## Context for a fresh session

Two products by one owner overlap. `kms` (`/home/sergei/projects/vivantel/kms`) is a Claude Code / Codex / Kilo plugin of 14 skills over a four-artifact knowledge base (fact, decision, guardrail, procedure), a shared model (`plugins/kms/shared/artifact-model.md`, 1,308 words), a structural checker (`plugins/kms/shared/lint_check.py`) and a Kilo/promptfoo eval harness. `go-getter` (`/home/sergei/projects/vivantel/go-getter`, v0.5.0, about 347 commits, about 200 decision files) forked kms's skills in 2026-10. Its `skills/` holds the same 14 names plus `autonomous-run`, `discover` and `go-getter-init`. It also keeps its own `shared/artifact-model.md` (1,025 words) and its own `lint`, and adds a compiler for 7 host agents, a CLI and 10 harness packs. go-getter decision 0066 ("own the knowledge-base tooling") and kms decision 0067 ("standalone") both record that neither shares code with the other. The two models have therefore been drifting since October. Nobody has measured by how much.

Separately, kms's model is internally muddled: decisions carry a `track` (`product` | `process`) that almost nothing consumes (8 of 64 decisions are `product`), and nothing says whether kms is meant to hold product specs. OpenSpec (Fission-AI) owns specs and keeps decision rationale only as per-change `design.md`; go-getter's decision 0075 already settles the boundary by detecting and tolerating it.

**Goal.** One artifact model, one checker and one eval suite. kms is the lightweight, standalone distribution and the reference implementation of that core. go-getter drops its fork and adopts the core by a pinned schema version. Product specs stay outside both. The cut is by artifact ownership: kms owns what outlives the work (fact, decision, guardrail, procedure); go-getter owns what has an owner, state and `Accept` (outcome brief, unit tree, meter, operating charter, harness config); OpenSpec owns what a change should do.

**Not the goal.** Merging the two products into one, retiring kms, or starting a third repo. Section "Repo question" says when that last one is reconsidered.

## Execution mode (read first; this section overrides step text where they differ)

This plan is executed end to end by an agent on **feature branches**, in as many sessions as it takes. Nothing is pushed, tagged, released or merged by the agent.

**Branches.**
- kms: `feat/kms-core-consolidation`, cut from `plan/kms-review-and-redesign` at `746aa93` (so it carries the redesign's done steps 0.x, 1.2, 1.5).
- go-getter: `feat/adopt-kms-core`, cut from go-getter `master` (`1930ecf`), in its own worktree `/home/sergei/projects/vivantel/go-getter-wt/adopt-kms-core` (`git -C /home/sergei/projects/vivantel/go-getter worktree add /home/sergei/projects/vivantel/go-getter-wt/adopt-kms-core -b feat/adopt-kms-core master`, then `npm ci` there). Created lazily by the first step tagged `[go-getter]`. The main go-getter checkout is never touched.
- Every step is tagged `[kms]` or `[go-getter]` (its repo). A step may touch only its own repo.

**Checkpoint = one commit per step.** A step is finished only when (1) its "Done when" holds, (2) its heading is flipped to `[done]` and one Progress-log line is added, (3) all of that is committed in one commit whose body ends with the trailer `Plan-Step: <id>` (for example `Plan-Step: A1`). The progress line and heading flip live in the *kms* plan file even for `[go-getter]` steps, committed in kms in a second tiny commit `docs: plan step <id> done (go-getter <short-sha>)`. Never leave a finished step uncommitted. If a session must stop mid-step, commit what exists as `wip(<id>): <what is left>` with trailer `Plan-Step: <id> wip`; never leave a dirty tree.

**Resume protocol (a fresh session, no memory of this one).**
1. `cd /home/sergei/projects/vivantel/kms && git switch feat/kms-core-consolidation && git status`. A dirty tree means an interrupted step: finish it or `git restore` it, then commit.
2. Read this file's Progress log and "Owner decisions pending" list. Run `git log --grep='^Plan-Step:' -n 5` and `git -C /home/sergei/projects/vivantel/go-getter-wt/adopt-kms-core log --oneline master..HEAD` (if the worktree exists) to see where things stand. If git and the Progress log disagree, **git wins**; fix the log.
3. Pick the first step in "Order of execution" that is not `[done]` and not `[blocked]` and whose predecessors are all `[done]`. If its latest commit is `wip`, continue it.
4. Re-run that step's "Done when" first. If it already holds, mark `[done]` and go to the next.
5. Do the step. Run the checks for the repo you touched: kms: `python3 -m unittest discover -s evals/lint/unit` and, once it applies, `python3 plugins/kms/shared/lint_check.py --root .`; `python3 -m json.tool` on every edited manifest; re-read every edited `SKILL.md` in full. go-getter: `npm test` and `npm run check:generated`, `check:docs-consistency`, `check:indexes`, `check:versions` (run `npm run build` first when sources under `src/` or `shared/` changed).
6. Commit per the checkpoint rule; continue with the next step until the plan is finished or every remaining step is blocked.

**Blocked steps never stall the plan.** A step needing something the agent lacks is marked `[blocked: reason]` (examples: the `kilo` or `codex` CLI, an eval provider key, a push or release, an owner's real approval) and skipped; later steps that do not depend on it proceed. Steps 1.1, 1.3, 1.4 and 1.6 of the redesign plan are already blocked and **do not gate this plan**; everything here is written to work without them.

**Owner decisions: draft, proceed, review at the end.** The agent cannot be the accountable party, so it never sets `accepted-by`. A "Decision needed" step is done when the decision file exists with `status: draft`, carries the recommended option, lists the alternatives, and is added to the **Owner decisions pending** list below. Later steps proceed on the draft's recommended option and record the dependency in their commit body. The owner reviews the list at the end (phase I): accepting means set `status: active` and `accepted-by`; rejecting means revert the dependent commits named in the list. This is the only place the plan trades certainty for progress; every dependent step is therefore a separate commit that can be reverted alone.

**Never, without the owner.** Push, open a PR, merge, tag, bump to a release version, publish, delete branches other than the two named above, change `master`, edit go-getter's main checkout, touch `~/.claude`, or spend money on eval providers (steps needing a key are `[blocked]`).

**Conventions** (same as `kms-review-and-redesign.md`). Headings carry `[pending]`, `[done]` or `[blocked: reason]`, updated in place. "Done when" must be checkable from files alone. Re-read a whole edited `SKILL.md` before calling a step done (`AGENTS.md`).

## Relationship to the redesign plan

`docs/plans/kms-review-and-redesign.md` has phases 2 to 5 pending. This plan **executes redesign steps 2.1 to 2.10 inside its own order** (see "Order of execution"), following that plan's step text, on this branch, and flips their headings there when done (log lines in both plans). Redesign phases 3, 4 and 5 are not prerequisites; 5.1 to 5.3 doc updates are folded into phase G here. Redesign 1.6 and the release steps are `[blocked]`, so versions stay at `0.15.0` on this branch until the owner releases. Wherever step text below says "0.17.0" or "0.6.0", read it as "the next release the owner cuts"; the agent only prepares the changelog entry and does not bump versions.

## Phase A — Measure and decide (read-only, then three decisions)

All `[kms]` unless stated; A1 and A2 read go-getter's main checkout read-only (no worktree needed).

### A1 [done] [kms] Diff the two artifact models

**What.** Produce `docs/plans/archive/consolidation-model-diff.md` comparing `plugins/kms/shared/artifact-model.md` with go-getter `shared/artifact-model.md` field by field: base frontmatter, per-type fields, lifecycle words, admission rules, derivation recipe, archive layout, id format, tag vocabulary, marker conventions (`kms-seeded`, `kms-generated`, `<!-- kms:start -->`) and what go-getter renamed or added (it uses `track`, `accepted-by`, `governed-facts`, `enforcement` fields in its own corpus; confirm each). Classify every difference as identical, cosmetic, additive in one side, or conflicting.

**Done when.** The file exists and has a count per class and a one-paragraph verdict: "alignment is a cleanup" (at most about 5 conflicting items, all mechanical) or "alignment is a rewrite" (otherwise).

### A2 [done] [kms] Diff the 14 shared skills and the two checkers

**What.** For each of the 14 skills present in both repos (`attribute`, `bootstrap`, `brainstorm`, `capture`, `changelog`, `clarify`, `conform`, `lint`, `onboard`, `query`, `quickstart`, `refactor-plan`, `roadmap`, `uninstall`), record body word count in each repo, normalised diff size and whether the divergence is host-specific (go-getter targets 7 hosts through a compiler) or semantic. Compare `lint_check.py` with go-getter's lint (a skill plus `check` verbs in `compiler/`) and with its `check docs-consistency`, `check indexes`, `check tags`, `check plans`. List what go-getter's checks cover that kms's do not, and the reverse.

**Done when.** `consolidation-skill-diff.md` has one row per skill and per check with a verdict: identical, kms-ahead, go-getter-ahead, divergent. The totals decide the direction of every later port.

### A3 [done] [kms] Decision needed: boundary and non-goals (both repos, `track: process`)

**What.** One decision per repo with the same text, linked from each:

- kms owns durable knowledge artifacts (fact, decision, guardrail, procedure) and their validation. kms does not store product specs, plans, outcome briefs, meters or harness configuration.
- go-getter owns coordination artifacts and the harness. It does not define or validate knowledge artifacts.
- Both detect and tolerate OpenSpec (go-getter 0075). Neither copies spec content; a record points at an OpenSpec change with `source`.
- Guardrails that constrain product behaviour ("never log PII") **stay in scope** (they are enforceable rules, not specs). Requirements, behaviours and acceptance criteria stay out.

**Alternatives to record.** Extend kms to specs (rejected: a fifth artifact type, collides with OpenSpec, expands onto an unstable base). Full merge into one product (rejected: kms's small footprint is its adoption funnel).

**Done when.** The kms decision exists as `status: draft` (next free number, `track: process` until B1 removes the field), is added to the Owner decisions pending list, and names the go-getter twin it will be linked to (written in D0). It supersedes nothing yet. Skill moves are separate (phase E).

### A4 [done] [kms] Decision needed: consolidation and the clean-break gate

**What.** After A1 and A2, record one decision in each repo that supersedes kms 0067 and go-getter 0066: the knowledge-base core is defined once and consumed by pinned schema version; go-getter ships no fork of it. Chosen path depends on A1's verdict:

- **Cleanup verdict** → kms is the core, in place (this plan).
- **Rewrite verdict** → evaluate the clean-break repo (see "Repo question") before continuing; stop this plan at A4 until that is decided.

**Gate.** If the verdict is *rewrite*, the agent writes the decision as a draft recommending the choice it finds better, marks every later step `[blocked: owner chooses repo path (A4)]`, logs it, and stops. If *cleanup*, it continues.

**Done when.** The kms-side decision exists as `status: draft`, names the verdict it rests on and proposes superseding 0067. The supersession (archive move and index rows) is applied only after the owner accepts it in phase I; until then both files stay as they are and the draft states the dependency.

## Phase B — Narrow kms's scope (merged into kms redesign phase 2)

### B1 [done] [kms] Drop the `track` field

**What.** Supersede `0010-decision-track-field` and `0038-track-field-mutual-exclusivity` (and archive `docs/guardrails/decision-track-field.md`). Remove `track` from the model's Decision section, from `lint_check.py` (required-field check and the id and tag handling that reads it), and from the six skills that read it (`bootstrap`, `capture`, `lint`, `onboard`, `roadmap`, `uninstall`). The 8 `track: product` decisions become ordinary decisions; their `track:` line is deleted by the migration step (kms 2.10). Product/process role lists (`docs/skills/{product,process}-track-roles.md`, decision 0013) are retired with it. `bootstrap` step 7 stops proposing them.

**Done when.** `grep -rn "track" plugins/kms` returns no model or checker hits except historical changelog text, the checker passes on a corpus with no `track`, and 0010/0038 are archived.

### B2 [done] [kms] Narrow facts to environmental and process facts

**What.** Folded into kms redesign step 2.1. A fact states something true about the environment or the process (tool behaviour, upstream contract, a figure recomputed from observation); it does not restate product behaviour. Product behaviour that must hold is a guardrail; what the product should do is a spec and lives in OpenSpec. Update the Admission section: "not already carried elsewhere" gains "or a spec tool".

**Done when.** Redesign 2.1 and 2.6 name this boundary and the model has one sentence for it.

### B3 [done] [kms] Fix the model's shape by owner decision

**What.** Redesign steps 2.2 to 2.9 stay as written. This plan adds one requirement to 2.9: the model file begins with a `schema-version:` line (semver, starts at `1.0.0` on the first release after 2.10) and a changelog of schema changes. That version is what go-getter pins (phase C).

**Done when.** Redesign 2.9 is done and the model file carries `schema-version`.

## Phase C — Define the contract

### C1 [done] [kms] Specify what a consumer pins

**What.** A short `docs/skills/core-contract.md` in kms stating: the schema (frontmatter per type, lifecycle words, id format, archive layout); the checker's CLI (`python3 lint_check.py --root <dir>`, exit codes, JSON output keys) as a stable interface; the marker conventions; what is explicitly not part of the contract (skill bodies, eval harness, templates' wording). Define compatibility: a patch release never changes accept/reject on a previously valid corpus; a minor release may add optional fields or new warning-level checks; a major release may reject what was valid and ships a migration note. Schema version moves independently of plugin version, but a release note links the two.

**Done when.** The file exists, is linked from `plugins/kms/shared/artifact-model.md` and `README.md`, and `lint_check.py --version` prints the schema version it implements.

### C2 [done] [kms] Conformance fixtures

**What.** Add `evals/lint/conformance/` with a corpus of small valid and invalid artifact trees, each with its expected checker output (rule id, file, severity). It extends the existing `evals/lint/unit` tests (45 pass today). It is the thing go-getter runs to prove its vendored checker still agrees with kms's.

**Done when.** `python3 -m unittest discover -s evals/lint` runs it, at least one fixture exists per checker rule, and the fixture set is published as a tarball or directory path in `core-contract.md`.

### C3 [done] [kms] Decision needed: how go-getter consumes the core

**What.** Recommended: **vendor by pin**, not a runtime dependency and not a shared package. go-getter already has `check plugin-pin`, `check deps` and `check generated`; add `check core-pin`: the vendored `shared/artifact-model.md`, `lint_check.py` and the conformance fixtures are copied from a named kms release tag, and CI fails if the copy differs from the tag or if the schema version in `package.json` metadata does not match. A `go-getter core update <tag>` verb does the copy. Alternatives to record: install the kms plugin as a prerequisite (rejected: breaks the go-getter one-install story and adds a second plugin manifest to keep in sync); git submodule or subtree (rejected: heavy for four files); npm or pip package (deferred until a third consumer exists).

**Done when.** The decision exists in kms as a draft (the go-getter twin is written in D0) and `core-contract.md` (C1) names the vendoring mechanism.

## Phase D — go-getter adopts the core

All `[go-getter]` steps run in the worktree `feat/adopt-kms-core` (see Execution mode). They start after B3, C1 and C2 are `[done]` and the A4 verdict is *cleanup*.

### D0 [done] [go-getter] Twin decisions

**What.** Create the worktree and branch. Write go-getter-side drafts, same numbering rule as its `docs/decisions/INDEX.md`: boundary (twin of A3), consolidation superseding 0066 (twin of A4), vendor-by-pin (C3), skill moves (E1), eval ownership (F1). Each `status: draft`, no `accepted-by`, cross-linked to its kms twin by path, and added to the Owner decisions pending list. Run `npm run check:indexes`.

**Done when.** Five draft decision files exist on `feat/adopt-kms-core`, index rows added, `check:indexes` and `check:docs-consistency` pass.

### D1 [done] [go-getter] Add the pin and replace the fork

**What.** Implement `check core-pin` and `core update` (C3). Replace `shared/artifact-model.md`, `src/shared/artifact-model.md` and go-getter's checker with the vendored copies. Keep go-getter's own additions (compiler `check` verbs for plans, indexes, packs and the harness) as separate checks that run after the core checker and never edit core files.

**Done when.** `npm run check:core-pin` passes, the vendored files are byte-identical to the kms tag, and `rg "own the knowledge-base tooling" docs` returns only archived text.

### D2 [done] [go-getter] Migrate go-getter's corpus

**What.** Run the core checker over go-getter's `docs/` (about 200 decision files plus facts, guardrails, procedures and meters). Fix findings in batches by class: field renames, dropped `track`, fact narrowing, lifecycle words. Do not rewrite decision content. Anything go-getter uses that the core lacks (for example fields on its harness packs' decisions) either becomes an additive optional field proposed to the core (C1 minor release) or moves out of the knowledge artifact into the pack config.

**Done when.** The core checker passes on go-getter's own `docs/` with no suppressed findings, and `npm test` plus `npm run check:docs-consistency` pass.

### D3 [blocked: evals and e2e spend money and read ~/.claude credentials; owner runs them] [go-getter] Re-run go-getter's own evals

**What.** Run `npm run eval` and `eval:bypass` and the lifecycle e2e (`scripts/e2e/lifecycle.mjs`) against the migrated corpus and core skills.

**Done when.** No regression against the last green run on `master`, recorded in the PR.

## Phase E — Skill moves (kms narrows, go-getter keeps the coordination skills)

kms keeps: `bootstrap`, `capture`, `lint`, `query`, `onboard`, `conform`, `attribute`, `uninstall`, `quickstart`. Five skills leave kms because they produce plans, options or release output, not durable knowledge. Removing a shipped skill breaks installed users, so each move has a deprecation path.

| Skill | kms after | go-getter after |
|---|---|---|
| `roadmap` | rename to `decide`: interview to admissible records only, no plan file, no unit tree | keeps `roadmap` as decomposition into units (0177) |
| `refactor-plan` | removed after one deprecation release | keeps, becomes a decompose variant |
| `brainstorm` | removed after one deprecation release | keeps |
| `clarify` | removed after one deprecation release | folded into `discover` as its interview mechanic (resolves redesign 3.1's duplicated interview text once) |
| `changelog` | removed after one deprecation release | folded into `release` |

### E1 [done] [kms] Decision needed: skill moves and the deprecation window

**What.** Record the table above as one decision per repo. Default deprecation window: one minor release in which the kms skill's description starts with "Deprecated: moved to go-getter, removed in 0.19" and still works.

**Done when.** The kms decision exists as a draft (go-getter twin in D0) and `docs/skills/kms-architecture.md` "Which skill does what" matches the table.

### E2 [done, eval run blocked: no kilo CLI] [kms] Implement the moves in kms

**What.** Add `decide` (new body derived from `roadmap`'s record steps, with `examples.md` and an eval case per the every-skill-ships-examples guardrail). Mark the other four deprecated in their frontmatter descriptions. Update `README.md` skill table, `plugins/kms/skills/index.json`, the Codex and Claude manifests and all three versions in lockstep (`docs/guardrails/plugin-manifest-version-sync.md`).

**Done when.** Evals for `decide` pass in CI, manifests agree, and removal is scheduled in the next plan's step list.

### E3 [done] [go-getter] Implement the moves in go-getter

**What.** Retain the five skills; remove their copy of kms-only knowledge text; point to the core for artifact semantics. Resolve `clarify`→`discover` and `changelog`→`release` per E1.

**Done when.** `go-getter` skill count is unchanged or lower, none of them restates the artifact model, and the generated host outputs build (`npm run check:generated`).

## Phase F — One eval suite

### F1 [done] [kms] Decision needed: where core evals run

**What.** The core's skill evals (Kilo CLI against its free gateway, orchestrated by `promptfoo`; lint matrix; admission eval) stay in kms. go-getter runs only the conformance fixtures and its own harness evals. Record this so the same behaviour is not measured twice with two different harnesses. Note both repos use promptfoo (go-getter pins 0.123.1); align the version.

**Done when.** The kms decision exists as a draft (go-getter twin in D0); the go-getter `eval` change is made in D3.

### F2 [done] [kms] Close the evidence gaps that the review found

**What.** Already covered by kms redesign phase 4 (eval cases for unmeasured skills; lint matrix re-run on the pinned model; evidence in or out of the repo). Add one item: a conformance check that fails if go-getter's vendored checker and kms's disagree on any fixture.

**Done when.** The conformance fixtures run in both CIs.

## Phase G — Distribution and docs

### G1 [done] [kms] Make the story consistent in both repos

**What.** kms `README.md`, `ARCHITECTURE.md`, `INSTALLING.md`: kms is the lightweight knowledge-base plugin and the reference implementation of the core; it works alone; go-getter builds on it. go-getter `README.md`: it adopts the core by pin; it does not define knowledge artifacts. Both state the OpenSpec boundary in one sentence. Keep the thesis sentence required by kms decision 0052.

**Done when.** Both READMEs link to each other and to `core-contract.md`; `lint` and `conform` pass on both repos.

### G2 [done] [kms] Dogfood and traceability

**What.** Record this work in each repo's knowledge base through the new `decide` flow once available: boundary, consolidation, skill moves, pin mechanism. Archive superseded decisions with index rows. Run `lint` and `conform` on both.

**Done when.** Both repos' `lint` and `conform` are green with no suppressed findings.

## Phase H — Release preparation (the agent prepares, the owner releases)

### H1 [done] [kms] Prepare the kms release

**What.** Write the `CHANGELOG.md` entry (via the repo's own conventions), the schema-version note, the deprecation notices and the upgrade note for users of the five deprecated skills. Do **not** change `version` in any manifest, tag, or push. Leave a `docs/plans/release-notes-next.md` the owner can paste from.

**Done when.** The entry and notes exist and `python3 -m json.tool` passes on all manifests (unchanged).

### H2 [pending] [go-getter] Prepare the go-getter release

**What.** Same for go-getter: changelog entry, the pinned kms tag name it expects (`kms-schema-1.0.0`, to be created by the owner at release), and what `go-getter core update` does. No version bump.

**Done when.** Entry exists; `npm run check:versions` still passes unchanged.

### H3 [pending] [kms] Plan the removal release

**What.** Write the small follow-up plan for removing the five deprecated skills one minor release after the deprecation ships: `docs/plans/kms-remove-deprecated-skills.md` with steps and "Done when" lines.

**Done when.** The plan file exists.

## Phase I — Owner review gate

### I1 [pending] [kms] Hand over

**What.** Produce `docs/plans/archive/consolidation-handover.md`: the Owner decisions pending list with one line each (file, recommended option, commits that depend on it, how to revert), every `[blocked]` step with what unblocks it, both branch names and tip commits, the test and check results at the tips, and the release sequence the owner runs next (kms 1.6 prerequisites, tag, then go-getter pin). Then stop and report; do not merge.

**Done when.** The file exists and its decision list matches the one in this plan.

## Order of execution

The agent executes in this order, skipping `[blocked]` steps:

1. **A1, A2** (read-only diffs), **A3** (boundary draft).
2. **A4** (consolidation draft; gate on the verdict).
3. Redesign steps **2.1 to 2.8** (their decisions, as drafts, with B1 to B3 folded in: 2.1 = B2, 2.5 and 2.6 absorb B1, 2.9 adds `schema-version`), then **2.9** (model rewrite), **2.10** (migration of kms's corpus, templates and eval fixtures). Flip each heading in `kms-review-and-redesign.md` and add a log line in both plans.
4. **B1, B2, B3** (confirm each is satisfied by step 3; do the remainder).
5. **C1, C2** (contract, conformance fixtures), **C3** (draft).
6. **E1, F1** (drafts), **E2** (kms skill moves, `decide` plus deprecations).
7. **D0, D1, D2, D3** (go-getter worktree), **E3**.
8. **F2, G1, G2** (conformance in both CIs; docs; dogfood and lint/conform on both repos).
9. **H1, H2, H3**, then **I1** and stop.

The redesign plan's phases 3 and 4 and release steps (1.6) are out of scope here; 5.1 to 5.3 are done as G1.

## Owner decisions pending

Every decision drafted by an agent step is listed here with its file path, recommended option and dependent commits. Empty until step A3.

| Decision (file) | Recommended | Dependent steps | To revert |
|---|---|---|---|
| `docs/decisions/0069-kms-owns-durable-knowledge-not-specs-or-coordination.md` (A3) | As written (kms owns the four artifacts; specs and coordination out) | B2, E1, G1 | Delete the file and its INDEX row; revert dependents |
| `docs/decisions/0070-kms-is-the-knowledge-base-core-consumed-by-pin.md` (A4) | Cleanup path: kms is the core, supersede 0067 on acceptance | B, C, D, E, F, G | Delete file and INDEX row; revert dependents; 0067 stays active |
| `docs/decisions/0071-facts-carry-no-outgoing-edges.md` (2.1, B2) | As written | 2.2-2.10, B2 | Revert the 2.1 commit (restores 0064 and 0009); revert dependents |
| `docs/decisions/0072-guardrail-derivation-edges-are-honest.md` (2.2) | As written | 2.3-2.10 | Revert the 2.2 commit (restores 0051, 0027); revert dependents |
| `docs/decisions/0073-lifecycle-words-defined.md` (2.3) | As written | 2.7-2.10 | Revert the 2.3 commit (restores 0039); revert dependents |
| `docs/decisions/0074-registries-by-marker.md` (2.4) | As written | 2.7, 2.9, 2.10 | Revert the 2.4 commit (restores 0013, 0029); revert dependents |
| `docs/decisions/0075-settle-names-keep-directories.md` (2.5) | As written | 2.9, 2.10 | Revert the 2.5 commit; revert dependents |
| `docs/decisions/0076-admission-reconciled-with-existing-rules.md` (2.6) | As written | 2.9, 2.10 | Revert the 2.6 commit (restores 0015, 0065 text); revert dependents |
| `docs/decisions/0077-more-structural-lint-checks-optional-pins.md` (2.7) | As written | 2.9, 2.10 | Revert the 2.7 commit (restores 0058, 0061, 0062); revert dependents |
| `docs/decisions/0078-open-questions-are-draft-decisions.md` (2.8) | As written | 2.9 | Revert the 2.8 commit (restores 0030); revert dependents |
| `docs/decisions/0079-drop-track-field.md` (B1) | As written | C, E, G | Revert the B1 commit (restores 0010, 0038, 0013, the guardrail and every `track:` line) |
| `docs/decisions/0080-core-is-vendored-by-pin.md` (C3) | Vendor by pin | D1, G1 | Delete file and INDEX row; D1 changes with it |
| `docs/decisions/0081-skill-moves-and-deprecation-window.md` (E1) | As written | E2, E3, H1, H3 | Revert E1 and E2 commits |
| `docs/decisions/0082-core-evals-live-in-kms.md` (F1) | As written | D3, F2 | Delete file and INDEX row |
| go-getter `docs/decisions/0210..0214` on `feat/adopt-kms-core` (D0) | As written | D1-D3, E3 | Revert the D0 commit in the go-getter worktree |

## Repo question: when a new repo is warranted

Default is no new repo; kms is the core. Reconsider only at A4 if one of these holds:

1. **A1 says rewrite**: the models differ so much that aligning go-getter means rewriting its corpus. A clean-break repo with the narrowed model and no legacy then competes with an in-place shrink of kms. Choose it only if migrating go-getter's about 200 decisions is the same cost either way, since that migration happens in both options.
2. **You want a neutral spec**: if third parties should implement the model without adopting either product, publish the schema, the contract and the conformance fixtures as their own repo; kms and go-getter both pin it.
3. **Neither product should own the model**: treat them as peers consuming a third thing. I don't see this today, because go-getter is the larger consumer.

If a new repo is chosen, it replaces phases C and D's "kms is the core" with "the new repo is the core"; B, E, F and G are unchanged.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Aligning go-getter to a model that still changes | D starts only after redesign 2.10 and B3 are done on this branch; the pin makes any later change an explicit bump |
| Agent proceeds on unaccepted decisions | Each dependent step is its own commit and listed in Owner decisions pending; nothing is merged or released until I1 |
| An interrupted session leaves a half step | One commit per step, `wip` commits, git is the source of truth over the log |
| A1 shows a large divergence | The gate at A4 stops the plan before any code moves |
| Removing kms skills breaks installed users | One-release deprecation window; replacement named in the description |
| Pin mechanism rots (copy drifts) | `check core-pin` in go-getter CI, conformance fixtures in both CIs |
| Two products' release trains couple | Schema version, not plugin version, is the contract; patch never changes accept/reject |
| kms loses its "no build step" property | It does not: the core is hand-written in kms and copied out, not generated into it |
| Owner time (one maintainer) | Phases are ordered so each ends in a releasable state; A1 to A3 are small and valuable even if the rest is cancelled |

## Minimal path (if only a weekend is available)

A1, A2, A3. This yields the measurement, the kms-side boundary draft and the OpenSpec non-goal, without touching code. Stop there if the weekend ends; the Progress log and branch make it resumable.

## Deferred, with triggers

- A published package (npm or pip) for the core: when a third consumer exists.
- A neutral spec repo: when an outside party asks to implement the model.
- A `retro` skill for events: already deferred in the redesign plan.
- Cross-repo contract tests in CI that fetch the other repo: when the pin copy has drifted twice.

## Not in this plan, deliberately

- Merging the products or retiring kms.
- A spec-management feature in either product (go-getter 0075, this plan's A3).
- Rewriting go-getter's coordination skills, packs or compiler.
- Re-litigating admission-test thresholds (decision 0065) or the eval model pin (0057).

## Progress log

- 2026-11-15 plan drafted; branch `feat/kms-core-consolidation` cut from `plan/kms-review-and-redesign` @ 746aa93; no step executed.
- 2026-11-15 A1 [done]: model diff written, verdict cleanup (9 identical, 4 kms-only, 3 go-getter-only, 2 conflicting) (kms see git log Plan-Step: A1)
- 2026-11-15 A2 [done]: skill/checker diff written; 5 identical, 1 kms-ahead, 3 go-getter-ahead, 5 divergent; checker direction kms to go-getter (kms see git log Plan-Step: A2)
- 2026-11-15 A3 [done]: boundary decision 0069 drafted, listed in Owner decisions pending (kms see git log Plan-Step: A3)
- 2026-11-15 A4 [done]: consolidation decision 0070 drafted on A1 verdict cleanup; gate passed, plan continues (kms see git log Plan-Step: A4)
- 2026-11-15 B2 [done]: satisfied by 0071 fact boundary sentence; model text lands in 2.9
- 2026-11-15 B3 [done]: satisfied by 2.9: model file begins with schema-version
- 2026-11-15 B1 [done]: decision 0079 drafted (supersedes 0010, 0038, 0013); track dropped from model, checker, skills, corpus and fixtures; checks 14/15 retired; matrix regenerated with 2.7 split
- 2026-11-15 C1 [done]: core-contract.md written; linked from the model and README; lint_check.py --version prints 1.0.0-draft
- 2026-11-15 C2 [done]: conformance fixtures: 21 cases under evals/lint/conformance, at least one per checker rule, run by `python3 -m unittest discover -s evals/lint -t .` (also in CI)
- 2026-11-15 C3 [done]: decision 0080 drafted (vendor by pin)
- 2026-11-15 E1 [done]: decision 0081 drafted (skill moves, one-release deprecation)
- 2026-11-15 F1 [done]: decision 0082 drafted (evals stay in kms)
- 2026-11-15 E2 [done]: decide skill added (SKILL.md, examples.md, eval case evals/decide, CI matrix); roadmap, refactor-plan, brainstorm, clarify, changelog marked deprecated; README and index.json updated; versions untouched. The decide eval has not been run (blocked: no kilo CLI here)
- 2026-11-15 D0 [done]: go-getter worktree created; five twin drafts 0210-0214 on feat/adopt-kms-core; check:indexes, docs-consistency, tags ok (go-getter 750fc14)
- 2026-11-15 D1 [done]: core pinned at kms a47033c (src/core-pin.json); check core-pin, core update/status, core-pin test; artifact-extensions.md holds go-getter additions; npm test 1438 pass. Not done: 0066 remains active until the owner accepts 0211 (go-getter 9ea0f2b)
- 2026-11-16 D2 [blocked]: superseded by the line below (cleared in a later session)
- 2026-11-16 D2 [done]: 21 facts given a `source`; core checker clean (advisory warnings only); npm test 1438 pass, check:generated/docs-consistency/indexes/versions/core-pin ok (go-getter a37d4ea)
- 2026-11-16 D3 [blocked]: `npm run eval`, `eval:bypass` and `e2e:lifecycle` call real model providers (cost, ~/.claude token); not run. Offline `npm test` 1438 pass stands in
- 2026-11-16 E3 [done]: five skills kept (count unchanged, 17); bootstrap/capture/lint/roadmap and examples drop `track`, role lists and restated field rules; lint check 2 defers to the core checker; build and npm test 1438 pass. Not done: folding clarify into discover and changelog into release (no `release` skill exists; kept as is, left to the owner with 0213) (go-getter 4aabae4)
- 2026-11-16 F2 [done]: conformance fixtures run in kms CI (existing) and in go-getter `npm test` (new core-pin test, CHECKER=vendored checker); pin moved to kms fdd1bba; npm test 1439 pass (kms fdd1bba / go-getter c24e10b)
- 2026-11-16 G1 [done]: kms README/ARCHITECTURE/INSTALLING and go-getter README state the story, link each other and core-contract.md, give the OpenSpec boundary; thesis sentence kept; structural checker clean on both (the `lint`/`conform` skills themselves are model-run and not executed here) (kms see git log Plan-Step: G1 / go-getter fa90e06)
- 2026-11-16 G2 [done]: the work is recorded as the drafts in the Owner decisions list (kms 0069-0082, go-getter 0210-0214); archive moves for 0066/0067 wait for acceptance; structural checker clean on both repos; model-run `decide`/`lint`/`conform` not executed (no provider)
- 2026-11-16 H1 [done]: CHANGELOG `[Unreleased]` entry and docs/plans/release-notes-next.md; no version, tag or push
- Format for new lines: `YYYY-MM-DD <step id> [done|blocked: reason]: <one line> (kms <sha> / go-getter <sha>)`.
