---
id: kms-review-and-redesign
title: Fix, clarify and redesign the kms knowledge system after the 2026-11 whole-repo review
status: reconciled 2026-11-16 with the consolidation (0.16.0-0.16.3 shipped phases 0-2); open: 1.1, 1.3, 1.4 (blocked), phases 3-5 re-scoped below; next release 0.18.0, because 0.17 removes the deprecated skills (decision 0081)
date: 2026-11-12
---

# Fix, clarify and redesign the kms knowledge system

## State 2026-11-17 (branch `plan/kms-review-open-steps`)

**Proven by deterministic checks** (unit suites 123+8+6 pass; `lint_check.py --strict` exits 0; skill greps and word budget 6239 vs 6280 at 0.16.3): 3.2 skill text, 3.3, 3.4 (check 25 + text; `c25` matrix case), 3.5 (in `decide`), 3.6 applicable bullets, 4.3, 5.2, 5.3 (tables written fresh), 5.4 and 5.1 manifest part.

**Eval run 2026-11-17 with kilo 7.8.27 (free model `cohere/north-mini-code:free`):** `conform` 1/1, `query` 2/2, `uninstall` 1/1, `lint-clean` 1/1 pass after fixing sentinel regexes (bold markdown), the runner-created `.kilo/` in the file list and the `query` unanswerable case (now keys on `QUERY_CITED: NONE` only; the model answered `QUERY_ANSWERED: YES` there). Single runs, not repeated. `attribute` on master's config passes 1/3; with the new body-trailer assertion 0/3: the model often asks a question instead of committing (the known flake). Cause found: `attribute` step 2 says to confirm the artifact list with the user, and `kilo run --auto` has nobody to answer. Prompt variants, 4 runs each: pre-approval + no questions 2/4; 'nobody available' 1/4; naming the skill + pre-approval + 'with Refs trailers' 3/4 (adopted in the case). Small samples; the remaining failures are commits without a trailer. Then `attribute/SKILL.md` was rephrased (run `git diff --staged` itself; use clearly matching artifacts and ask once only when candidates conflict or none match; an explicit `git commit` step) and the case prompt restored to the bare 'Commit this with attribution.': 1/6, then 5/6 and 5/6, then 8/8 after compressing the body to 191 words (kilo 7.8.27, free model). This changes the skill from always-confirm to confirm-on-ambiguity: owner to review. Harness (step 1.4, partial): `kilo-judge.sh` retried nothing, so 429s and empty judge replies were scored as assertion failures in the `bootstrap`/`decide` variant runs of 2026-11-17/18; it now retries 5 times and otherwise prints `=== HARNESS ERROR ... ===` and exits 1, and `kilo-runner.sh` does the same after its 6 tries. `post-eval-summary.py` does not yet label such errors 'infra'; the gateway was returning `Too Many Requests` at the time, so the `decide` v2/v3 and `bootstrap` v1 numbers are unreliable. `lint` compressed 1431 to 995 words, eval 4/4 before and after, kept. `bootstrap` (1288 to 1057: 3/4 before, 3/4 after a harness-failed first run) and `decide` (744 to 640: 2/4 and 4/4 before, 1/4 and 2/4 after) were not adopted at the owner's call; drafts not committed. Whether `attribute` gates a merge is still step 1.4's decision. Earlier note, superseded for the four passing cases:** new eval cases `conform`, `query`, `uninstall`, `lint-clean` and the `attribute` assertion are written and wired into `run-all.sh` and the workflow, but never run (no `kilo` here). No skill-body change has passed the eval suite; CI must run on this PR.

**Open, owner decides:** decisions 0083 (step 3.2) and 0084 (step 5.4) were accepted 2026-11-17 at the owner's request (0032 amended); 5.8 release 0.18.0 (after the 0.17 removal release; outward-facing).
**Open, blocked:** 1.1, 1.3, 1.4 (kilo/Codex CLI); 4.2 (provider key; only `cases.tsv` wording stripped); 4.1 `attribute` `Refs:` assertion is wired (runner now prints the last commit body) but not run; 4.2 held-out set recorded as 'not in repo, never run' in a 0065 amendment, numbers pending a key; 5.1 done 2026-11-17 at the owner's choice (kms block added to AGENTS.md); 3.4 docs-manifest `last-verified` set without re-observing sources; 5.3 `fix-eval-doc-drift` unfetchable (SHA gone); 5.5 and 5.6 (query/lint/conform pass pasted into steps) not run; `lint --changed-since` is text only; `capture`/`lint`/`uninstall` examples not updated.

## Reconciliation 2026-11-16

`kms-core-and-go-getter-consolidation.md` ran after this plan was written and changed what is left. It shipped as 0.16.0, 0.16.1, 0.16.2 and 0.16.3 (schema 1.0.0, tag `kms-schema-1.0.0`). Read the phases below with these corrections; step text is otherwise unchanged.

- **Phases 0-2 and 1.6 are done.** The format change this plan reserved for 0.17.0 (schema split, facts without outgoing edges, `source`/`last-verified`, `migrate.py`, `enforced-by`, the `track` field dropped) shipped in 0.16.0.
- **Release numbering.** 0.17 is the release that removes `roadmap`, `brainstorm`, `clarify`, `refactor-plan` and `changelog` (decision 0081, amended 2026-11-16; `kms-remove-deprecated-skills.md`). This plan's release is therefore **0.18.0** (every `0.17.0` below was renamed).
- **Skills.** kms has fifteen skills until 0.17: the fourteen plus `decide` (0081), which replaces `roadmap` for records. Five skills are deprecated and move to go-getter. A step that edits one of them is dropped or retargeted to `decide`: 3.1 is superseded, 3.5 and the `roadmap`, `changelog` and `quickstart` bullets of 3.6 are retargeted, 4.1 drops four of its nine cases.
- **Role lists** are gone (0079), so the `bootstrap` role-list bullets of 3.6 and the role-list question in 5.1 are moot.
- **Still blocked:** 1.1 and 1.4 need the `kilo` CLI (a CI-only gap, since CI has it); 1.3 needs the Codex CLI; 4.2 needs a provider key.
- **Eval flakes seen 2026-11-16** (free model `cohere/north-mini-code:free`): `capture` and `attribute` fail on a share of runs even when the right skill loads, on master as well as on PRs; `bootstrap` once errored with `spawn E2BIG` until the runner capped its transcript (0.16.2). Step 1.4 is the place to make such failures distinguishable and to decide which cases gate a merge.

## Context for a fresh session

This repo (`/home/sergei/projects/vivantel/kms`) is a Claude Code plugin marketplace shipping one plugin, `kms`: fourteen agent skills under `plugins/kms/skills/`, a shared artifact model (`plugins/kms/shared/artifact-model.md`, 1,308 words), a deterministic structural checker (`plugins/kms/shared/lint_check.py`, 416 lines, needs PyYAML), five guardrail templates (`plugins/kms/templates/guardrails/`), two Claude Code `SessionStart` hooks (`plugins/kms/hooks/`), and packaging for Claude Code, Codex and Kilo Code CLI. The repo dogfoods the system on itself under `docs/{facts,decisions,guardrails,skills}/`: 63 live and 3 archived decisions, 6 numbered live facts plus the un-numbered `docs/facts/docs-manifest.md`, 8 archived facts, 17 guardrails, 6 procedures. A promptfoo plus Kilo eval harness lives under `evals/`.

On 2026-11-12 a whole-repo review was run: one pass by the planning session over every skill body, the model, the guardrails, facts, procedures, hooks, checker, evals, git history and the unmerged branches; then five independent review agents with separate lenses (taxonomy, process coverage, skill bodies and packaging, evidence and evals, dogfooding and history); then two independent critics of the draft plan and a fact-check of its claims (188 claims checked, 166 verified, 17 corrected before this version was written). The condensed evidence is in `docs/plans/archive/2026-11-review-record.md`; every "Why" below cites files directly, and line numbers were checked at commit `87bb51d` (branch `study/s6b-cleanup`, tree-identical to `origin/master` at `a9bc105`). Re-check a line number before editing; the quoted phrase is the anchor.

**Branch and release state.** The 2026-11 "study" (decisions 0056-0066: deterministic checker, lint matrix, structural/judgment labels, pinned edges, typed fact scope, two fact kinds, admission test, corpus cleanup) is merged into `origin/master` (PRs #76, #79, #80). Local `master` is 46 commits behind `origin/master`, fast-forward only. Every manifest still says `0.15.0` (tag `0.15.0` = `4cdd5bb`, 2026-09-13) although 11 commits since then changed shipped files under `plugins/` (9 files, +473/-33, including the new checker). `CHANGELOG.md`'s top entry is `[0.15.0] - 2026-09-12`. Important for migration: the model as tagged at 0.15.0 defined `kind: environmental | decision | derived | mixed` and shipped no checker, no `scope`, no `pinned`; a real 0.15.0 adopter has never run the checker and may hold `derived`/`mixed` facts. The current checker tolerates unknown frontmatter fields (there is no "unknown field" check), which is the backward-compatibility lever this plan uses.

**Sibling project.** `/home/sergei/projects/vivantel/go-getter` forked kms's skills in 2026-10 (its archived decision 0006 vendored kms; its decision 0066 then took ownership: "There is no upstream to sync from"). It has diverged. This plan assumes **kms stays a standalone, focused knowledge-system plugin** and borrows ideas from go-getter (a tooling-readable marker), not code. Step 0.1 records that positioning; nothing else is gated on it.

**How the plan is organised.** Six phases and two releases. Phase 0 is housekeeping. Phase 1 makes what already ships reach users, fixes the checker's bugs, and cuts **0.16.0** with a checker that tolerates the fact fields the next release will remove. Phase 2 is the model redesign: eight owner decisions (each a `roadmap` interview, because decisions are the owner's), then one rewrite of the model and one migration. Phase 3 adjusts skills for the processes the review found uncovered. Phase 4 makes the evidence real. Phase 5 updates kms's own dogfood and human docs and cuts **0.18.0**. A "Minimal path" section at the end says what to do if there are two weekends, not two months, and a "Deferred" section lists what was cut, each with the trigger that would bring it back.

**Conventions.** Each step heading carries `[pending]`, `[done]` or `[blocked: reason]`, updated in place. "Done when" is checkable from the files alone, by the step itself. "Decision needed" marks a step whose content the owner chooses; the recommendation is stated; the step is done when the decision record is `status: active` with `accepted-by` set, and every earlier decision it conflicts with has been disposed of **in the same commit** (left active, amended with a dated additive section following the precedent in 0043/0044/0047/0059 until step 2.3 ratifies that rule, or superseded: `status: superseded`, `superseded-by`, moved to `docs/decisions/archive/`, both index rows updated). `capture` check 1 already requires the same-commit rule. Nothing edits an accepted decision's `## Decision`/`## Why`/`## Tradeoffs considered` text. Every `SKILL.md` edit ends with one re-read of the whole file; every change under `plugins/kms/skills/**` or `plugins/kms/shared/**` goes through the eval suite on a same-repo PR into `master`. Shipped text never cites one of this repo's own `docs/decisions/NNNN` files (`docs/skills/scoping-shipped-vs-repo-rules.md`). This plan and its review record are committed on branch `plan/kms-review-and-redesign`, created from `origin/master`; execute the plan there (or on branches cut from it), not on `study/s6b-cleanup`, which step 0.2 deletes. Where a Done-when needs a live service (a Kilo or Codex install, a model run, CI), the thing checked is the *recorded result*: a named file or paragraph stating command, date and outcome; if the service is unavailable, mark the step `[blocked: no Kilo/Codex here]` rather than claiming the result.

**What the review found, in one paragraph.** The idea is sound and the decision record explains its reversals well. Four kinds of problem: (1) *Delivery*: the Kilo channel never ships `shared/` or `templates/`, so five skills point at files a Kilo user does not have; the checker crashes on a quoted template version and silently scans nothing on a non-`docs/` layout; the study's behaviour changes are unreleased. (2) *Model*: a plain fact cannot exist (it must carry `governed-by`, must ground something, must be referenced, and must not be "already carried" by config, so "the service listens on port 8080" fails admission and lint at once); `grounded-in` may equal `governed-by`, so the derivation recipe holds for 2 of 17 guardrails, one of which is also grounded in its own decision; three guardrails rest on facts the corpus cleanup deprecated and the flagship example in `ARCHITECTURE.md` has both sources retired; "immutable once accepted" is contradicted by eight `## Amendment` sections; `last-verified` and the "fitness-function inventory" are used by skills and defined nowhere; registries (indexes, tag list, docs manifest) are filed as facts and procedures. (3) *Process coverage*: the "decide" moment is covered, the "something happened" moment is not (incidents, retrospectives, experiments, external-fact re-verification); triggering is "remember to run it". (4) *Evidence*: 9 of 14 skills have no eval; on the free model the judgment lint checks have recall at or below 0.40 on 11 of 14 with a 0.20 false-alarm rate on a clean corpus; the admission numbers are development-set results from a different pipeline; `npm run eval` aborts on its first case without an Nvidia key; the unit tests never run in CI.

**Resume protocol (reentrant, self-checkpointing).** A fresh session starts here: (1) `git switch plan/kms-review-and-redesign` (or the branch named in the Progress log) and `git status` — a dirty tree means a step was interrupted; finish or `git restore` it; (2) read the Progress log below, then take the first heading marked `[pending]` whose predecessors in "Order of execution" are done; (3) re-run that step's "Done when" first — if it already holds, just mark it `[done]`; (4) do the step, run its checks (`python3 -m unittest discover -s evals/lint/unit`, `python3 plugins/kms/shared/lint_check.py --root .` once it applies), flip the heading to `[done]` (or `[blocked: reason]`), add one Progress-log line, and commit code and plan update **together** — one step, one commit, so git history is the checkpoint; (5) stop and tell the owner when the next step is "decision needed", needs outward-facing actions (remote branch deletion, push, tag, release), or needs a live service. Never batch several steps into one commit.

**Progress log** (append one line per step: date, step, commit subject).

- 2026-11-12 plan made reentrant; no step executed yet.
- 2026-11-12 0.3 [done]: bytecode untracked, .gitignore updated
- 2026-11-12 0.4 [done]: removed 'or derived'; fixed model sentence
- 2026-11-12 0.5 [done]: uninstall/roadmap/lint examples corrected
- 2026-11-12 0.6 [done]: eval script limited to 5 CI cases; unit job added; docs updated
- 2026-11-12 0.8 [done]: codex plan archived
- 2026-11-12 1.2 [done]: all bullets fixed with unit tests (45 pass); check 9 skips archived plans by design; skill-body edits (lint, bootstrap) still need the CI eval on a PR
- 2026-11-12 1.5 [done]: 0064 amended; checker drops fact kind/governed-by; conform/query draft sentences; matrix fixtures regenerated (pin quoting from 1.2)
- 2026-11-12 0.1 [done]: decision 0067 accepted (standalone)
- 2026-11-12 0.7 [done]: decision 0068 supersedes 0056; workflow master-only
- 2026-11-12 0.2 [done]: master fast-forwarded; 16 local and 18 remote study branches deleted
- 2026-11-12 1.1, 1.3, 1.4 [blocked]: need kilo/Codex CLI (absent here). Unblock by running on a machine with `kilo` installed (1.1 also needs the branch pushed); then 1.6 (release, tag) and phase 2 (owner-run roadmap interviews) follow.
- 2026-11-15 2.1 [done]: decision 0071 drafted (supersedes 0064, amends 0009); owner acceptance pending (kms Plan-Step: 2.1)
- 2026-11-15 2.2 [done]: decision 0072 drafted (supersedes 0051, amends 0027) (kms Plan-Step: 2.2)
- 2026-11-15 2.3 [done]: decision 0073 drafted (amends 0039) (kms Plan-Step: 2.3)
- 2026-11-15 2.4 [done]: decision 0074 drafted (amends 0013, 0029) (kms Plan-Step: 2.4)
- 2026-11-15 2.5 [done]: decision 0075 drafted (kms Plan-Step: 2.5)
- 2026-11-15 2.6 [done]: decision 0076 drafted (amends 0015, 0065) (kms Plan-Step: 2.6)
- 2026-11-15 2.7 [done]: decision 0077 drafted (amends 0062, 0061, 0058) (kms Plan-Step: 2.7)
- 2026-11-15 2.8 [done]: decision 0078 drafted (amends 0030) (kms Plan-Step: 2.8)
- 2026-11-15 2.9 [done]: model split into artifact-model.md (617 words) and admission.md (492); checker and tests updated (55 pass); skills re-pointed; schema-version 1.0.0-draft (kms Plan-Step: 2.9)
- 2026-11-15 2.10 [done]: migrate.py written; docs/ and four eval fixtures migrated; 17 guardrails re-derived and pinned; facts carry source/last-verified; strict checker clean on docs/ except one forward reference fixed in C1. Not done (blocked: needs eval provider key): lint-matrix labels/build.py regrade of the 2.7 split and `npm run eval` (kms Plan-Step: 2.10)
- 2026-11-16 5.7 [done early]: the three parked branches deleted from origin at the owner's request; tip SHAs in 5.7; 3.6, 5.3 and 5.4 still pending and now cite SHAs
- 2026-11-16 reconciled with the consolidation: phases 0-2 and 1.6 shipped as 0.16.0-0.16.3 (`kms-schema-1.0.0`); 3.1 superseded; 3.5, 3.6, 4.1, 5.1, 5.5, 5.2 re-scoped; this plan's release is 0.18.0 because 0.17 removes the deprecated skills (0081). Open: 1.1, 1.3, 1.4 (blocked), 3.2-3.4, 4.2-4.3, 5.1-5.7, 5.8

## Phase 0 — Housekeeping

### 0.1 [done] Record kms's positioning relative to go-getter (decision needed, not gating)

**What.** A short `track: product` decision (`docs/decisions/NNNN-<slug>.md`, the next free number at the time it is written; 0067 is free today): kms is a standalone knowledge-system plugin for any git project; go-getter is a separate project that forked kms's skills in 2026-10 and owns its copy; kms does not vendor, sync with, or try to become it. Alternatives to record: upstream library (rejected by go-getter's own 0066), retirement (if chosen, finish phase 1, write a deprecation notice, stop). Do this whenever convenient; no other step depends on it.

**Done when.** The decision exists, `status: active`, `accepted-by` set, row in `docs/decisions/INDEX.md`.

### 0.2 [done] Fast-forward local `master`; delete merged and throwaway branches

**What.** After committing this plan on a feature branch: `git checkout master && git merge --ff-only origin/master`. Delete locally and on `origin`: every local `study/s*` branch (all merged, PRs #61-#80), `study/base`, `study/v2-base`, and the unmerged throwaways `origin/study/s1-baseline`, `origin/study/s1-throwaway`, `origin/study/s8-rerun-base`, `origin/study/s8-rerun-head`. Keep `origin/harness/impl/step_01`, `origin/scale-bootstrap-lint-chunking`, `origin/fix-eval-doc-drift` until step 5.7. Keep tags `study-v1`/`study-v2` (0065/0066 cite them); step 5.4 records them.

**Done when.** `git branch` lists `master` and `plan/kms-review-and-redesign` (plus any branch cut from it); `git branch -r` lists `origin/master` and the three parked branches only.

### 0.3 [done] Untrack bytecode

**What.** `git rm -r --cached plugins/kms/shared/__pycache__ evals/lint/unit/__pycache__ evals/lint-matrix/__pycache__` (five `.pyc` files are tracked, one inside the shipped plugin); add `__pycache__/` and `*.pyc` to `.gitignore`.

**Done when.** `git ls-files | grep -c pycache` prints `0`.

### 0.4 [done] Fix the two text defects left by the study merge

**What.** `plugins/kms/skills/bootstrap/SKILL.md:33` "classify it: environmental, decision, or derived" → delete "or derived" (0064 removed it; the checker rejects it). `plugins/kms/shared/artifact-model.md:40` "A claim that needs both is written as two facts and `governed-by: <decision-id>` (`TBD` = debt)." lost its verb in the merge → "A claim that needs both is written as two facts. Add `governed-by: <decision-id>` (`TBD` = debt)." (Phase 2 rewrites this paragraph; fix it now so the shipped text is not wrong meanwhile.)

**Done when.** `grep -c "or derived" plugins/kms/skills/bootstrap/SKILL.md` prints `0`; the model sentence reads as two sentences.

### 0.5 [done] Fix the stale examples

**What.** `plugins/kms/skills/uninstall/examples.md:7` "4 seeded guardrails (`docs/guardrails/token-economy.md` and 3 siblings)" and `:13` "The other three are removed" → five templates exist: "5 seeded guardrails … and 4 siblings", "The other four are removed"; line 7's "3 generated files" list omits `docs/skills/tags.md` and every `INDEX.md` (stamped by bootstrap steps 7 and 10) → "the generated files (role lists if present, `docs/skills/tags.md`, `docs/facts/docs-manifest.md`, each `INDEX.md`)". `plugins/kms/skills/roadmap/examples.md:19` "fails the Admission section: it is easily reversible, unsurprising, visible in the diff and affects no one else" names gates the model does not have → "fails the **Not already carried** gate: a rename is visible in the diff". `plugins/kms/skills/lint/examples.md`: example 1 gains one sentence saying the checker runs first and its lines are reported as findings; example 3 moves "redundant guardrails" from the structural to the judgment list (check 5 is `[judgment]`). `plugins/kms/skills/capture/examples.md:7` keeps `last-verified` (phase 2 defines it).

**Done when.** None of the four quoted phrases remains; the replacements are present.

### 0.6 [done] Make `npm run eval` runnable and run the unit tests in CI

**Why.** `package.json`'s `eval` script loops every `evals/*/promptfooconfig.yaml` alphabetically; `evals/admission/` and `evals/lint-matrix/` pin `nvidia/nvidia/nemotron-3.5-lightning-30b-a3b`, which `kilo-runner.sh` routes to a Kilo `nvidia` provider needing a key, so `admission` (first alphabetically) fails and `|| exit 1` aborts before the five CI cases. `AGENTS.md:54` and `CONTRIBUTING.md:46` still say no key is needed. `.github/workflows/eval-skills.yml` has no `unittest`/`pytest` step and no PyYAML install; three suites exist (`evals/lint/unit`: 32 tests; `evals/lint-matrix`: 8; `evals/admission`: 6).

**What.** `package.json`: `eval` iterates only `attribute bootstrap capture lint roadmap`; add `eval:matrix` and `eval:admission` whose description says they need a provider key. Workflow: add a `unit` job on every `push` and `pull_request` (no path filter) running `pip install pyyaml`, `python3 -m unittest discover -s evals/lint/unit`, `-s evals/lint-matrix`, `-s evals/admission`, `python3 evals/lint-matrix/build.py --check`, `python3 evals/admission/build.py --check`; add `pip install pyyaml` to the `eval` and `eval-recheck` jobs; lower `evals/lint/promptfooconfig.yaml` `timeout_seconds` 1440 → 600 (the work is a script run plus transcription). `AGENTS.md`/`CONTRIBUTING.md`: the "no account or API key" sentences become "for the five CI cases; the matrix and admission evals need a provider key".

**Done when.** `node -e "console.log(require('./package.json').scripts.eval)"` names exactly the five cases; the workflow has a `unit` job with the six commands; the three `unittest discover` commands pass locally; the two doc sentences are changed.

### 0.7 [done] Drop the `study/base` CI trigger (decision needed, small)

**What.** The workflow still has `branches: [master, study/base]` (decision 0056). Write `docs/decisions/NNNN-eval-gate-master-only.md` (next free number at the time; `track: process`) superseding 0056; archive 0056 with pointer and index rows; change the workflow to `branches: [master]` in the same commit.

**Done when.** Workflow lists only `master`; 0056 archived with `superseded-by`; `python3 plugins/kms/shared/lint_check.py --root .` exits 0.

### 0.8 [done] Close the dead live plan

**What.** `docs/plans/codex-plugin-support.md` ("steps 1-4 done; step 5 blocked (needs Codex CLI)" since 2026-07-29; names `/home/ubuntu/projects/sergemso/dev_skills`, version `2.1.0`, four skills) → `git mv` to `docs/plans/archive/` with a top note: "Archived 2026-11: steps 1-4 done; step 5 (live Codex install test) is carried by step 1.3 of `docs/plans/kms-review-and-redesign.md`."

**Done when.** `ls docs/plans/*.md` shows only this plan; the archived file carries the note.

## Phase 1 — Delivery, checker bugs, release 0.16.0

### 1.1 [blocked: Done-when needs Kilo CLI + pushed branch for the live remote-skills test; no kilo here] Ship `shared/` and `templates/` through the Kilo remote channel

**Why.** `plugins/kms/skills/index.json` lists, for all 14 skills, exactly `"files": ["SKILL.md", "examples.md"]`; Kilo fetches only listed files as `{url}/{skill-name}/{file}` (`docs/facts/0008-kilo-code-skills-spec.md:31`). Yet bootstrap, capture, roadmap, lint and uninstall reference `../../shared/artifact-model.md`, `../../templates/`, and lint plus the model require `shared/lint_check.py`. The eval harness masks it: `evals/providers/kilo-runner.sh:82-87` copies `shared/` and `templates/` into `.kilo/` by hand. A real `skills.urls` user gets five broken skills. `plugins/kms/skills/lint/SKILL.md:12` names a `.kilo/shared/lint_check.py` layout only the harness produces. Codex: `.codex-plugin/plugin.json` points `skills` at `./skills`; whether `shared/` and `templates/` are installed is unknown (fact 0003 says the install path itself is unconfirmed).

**What.** First re-verify fact 0008 against Kilo's current docs and record the re-verification in the fact: does a `files` entry accept a subpath, and does the cache keep the directory name? Then choose, preferring (b) unless (a) is confirmed to work: (a) two non-skill entries in `index.json`, `shared` (files: `artifact-model.md`, `lint_check.py`, later `migrate.py`) and `templates` (files: each template path), with every sibling reference rewritten to a two-step rule ("`../../shared/` when installed as a plugin; otherwise `../shared/` beside this skill's directory, which is how a remote-skills cache lays it out"); verify Kilo does not choke on an entry without a `SKILL.md`; (b) vendor copies of `artifact-model.md` and `lint_check.py` into `skills/lint/` and `skills/bootstrap/` (and templates into `skills/bootstrap/templates/`), have the other skills reference those, and add a unit test asserting each vendored copy equals its `shared/` original. Option (b) partly supersedes decision 0034 (one shared file, read by sibling reference); if taken, say so in a one-paragraph amendment to 0034. Either way: `INSTALLING.md` states per agent what arrives, that `lint` needs `python3` plus PyYAML, and that the `SessionStart` nudge hooks are Claude Code only (Codex and Kilo users use the manual recipe in `docs/skills/automating-capture.md`); the Codex section says the plugin root must be installed whole until 1.3 confirms it; the lint skill drops the `.kilo/shared/` example for the two-step rule; `kilo-runner.sh` stops copying by hand so the eval exercises the real channel.

**Done when.** `index.json` or the vendored copies deliver the model, the checker and the five templates; fact 0008 carries a dated re-verification paragraph recording a `kilo.jsonc` pointing at this branch's raw-GitHub URL resolving every sibling reference in the five skills (the live test is done once and its result recorded; the record is what is checked); `INSTALLING.md` has the three per-agent statements; `kilo-runner.sh` no longer copies `shared/`.

### 1.2 [done] Fix the checker's crash, cascade and silent misses (bug fixes only)

**Why.** Reproduced by two reviewers on scratch fixtures (record in `docs/plans/archive/2026-11-review-record.md`):

- `plugins/kms/shared/lint_check.py:315` `if cur < ver:` raises `TypeError` on `kms-template-version: "1"` (quoted); the run aborts with a traceback, zero findings, and the skill falls back to ten checks by hand.
- A file whose frontmatter fails to parse (an unquoted colon in a title suffices) registers no id, so every referrer gets a false check 1 and its index row a false check 19.
- `load()` hardcodes `docs/<type>[/archive]`; on a project whose bootstrap extended an existing `decisions/` convention (as the skill's "Before starting" instructs) the checker scans nothing and prints five misleading `check 12: … has no file here` lines the skill forbids the model to second-guess.
- Check 9: `seen.add(name)` at line 288 dedups on bare filename across types; `PROSE_REF` cannot match `docs/<type>/archive/<file>.md`; the scan covers only the four artifact directories, so stale paths in `README.md`, `AGENTS.md`, `docs/plans/` are checked by nobody now that the model is told not to re-derive.
- No id-uniqueness check: a guardrail whose `id` equals a decision's shadows it in `by_id`, and `--pin` pins the wrong file's revision.
- `tags.md` parsing accepts only `^tag — meaning`; a list written with `- ` bullets or a plain hyphen flags every tag under check 21, including on `tags.md` itself; `bootstrap` never states the line format.
- `pin()` writes revisions unquoted (an all-digit value is re-read as an int and reported as a spurious check 13); raises `StopIteration` on unterminated frontmatter; rewrites CRLF to LF.
- `tags:` as a plain string is reported only as a check 19 title mismatch; no check says tags must be a list.
- Seeded guardrails (`kms-seeded: true`) are orphans by construction in every adopting project under check 7 (nothing references them); here they pass only because the corpus includes `plugins/**/*.md` and each template mentions its own id.

**What.** Fix each: `int()` both template versions (check 2 finding if not numeric); register the id from the filename when frontmatter fails and suppress checks 1/19 for it; add `--docs DIR` plus auto-detection of a directory containing `decisions/` at the root, and print one warning line when nothing is found; key check 9 on `(type, name)`, allow an optional `archive/` segment, and scan `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/plans/**` and every artifact (the skill's check 9 text then names that corpus); report duplicate ids under check 3 and refuse `--pin` on ambiguity; accept `- `/`* ` prefixes and `—`/`-`/`:` separators in `tags.md`, and have `bootstrap` step 7 state the format; quote pin values; message instead of traceback on unterminated frontmatter; preserve newline style (`newline=""`); a list-type test for `tags` under check 2; exempt `kms-seeded: true` files from check 7. One unit case per bullet in `evals/lint/unit/test_lint_check.py`. Do **not** change here: `PIN_IGNORED` (fixed by decision 0062; changed under 2.7), reference-target typing, check 7's corpus definition, the `superseded`-without-`superseded-by` rule (all under phase 2 decisions).

**Done when.** Each bullet has a unit test that fails on the old code and passes on the new; `python3 -m unittest discover -s evals/lint/unit` passes; the checker exits 0 on this repo and on a copy with `docs/` renamed to `knowledge/` run with `--docs knowledge`.

### 1.3 [blocked: no Codex CLI here] Test the Codex channel for real

**What.** In an environment with the Codex CLI, install the plugin from this repo's path; confirm all fourteen skills are discovered and whether `shared/` and `templates/` are present. Record command and result as a dated re-verification in `docs/facts/0003-codex-plugin-manifest-schema.md`; update `INSTALLING.md`'s Codex section. If the sibling directories are absent, apply 1.1's option (b) for Codex.

**Done when.** Fact 0003 has a 2026-11-or-later re-verification paragraph naming command and result; `INSTALLING.md` no longer says the command is unconfirmed (or says exactly what was tested).

### 1.4 [blocked: Done-when needs kilo to run the wrong-model case and re-verify the judge model; no kilo here] Make harness failures distinguishable from skill failures

**Why.** On 2026-11-08 all five CI cases failed with `Model not found: kilo/poolside/laguna-s-2.1:free` and read as five skill regressions (0057). `evals/providers/kilo-runner.sh` exits 0 at line 131 whatever Kilo returned and retries only on the literal "Too Many Requests"; `post-eval-summary.py` has no "infra" row; the judge model (`kilo-judge.sh`: `nvidia/nemotron-3-ultra-550b-a55b:free`) was never re-verified in 0057; `npm install -g @kilocode/cli` (workflow line 42) and `promptfoo/promptfoo-action@v1` are unpinned. Fact `docs/facts/0012-kilo-gateway-free-tier-access.md` (active, "no account or API key") is contradicted by 0059's amendment ("sign-up wall, then usage limits") and was never updated: a `capture` check 2 miss in kms's own dogfood.

**What.** Runner and judge: on `Model not found`, auth errors or non-zero Kilo exit, print one `=== HARNESS ERROR: <reason> ===` line as the whole output and exit non-zero; `post-eval-summary.py` labels such cases "infra". Pin `@kilocode/cli` to the current latest and record the version in the workflow comment; pin the action to a tag. Re-verify the judge model exists; record it in fact 0012's new dated paragraph, which also scopes the free-tier claim (held in CI 2026-09-10; failed from the author's machine 2026-11-08).

**Done when.** A local run with a wrong model id yields the one error line and the summary script labels it infra (add a unit test for the summary script's parsing); versions pinned; fact 0012 has the paragraph.

### 1.5 [done] Make the checker tolerate the fact fields phase 2 removes (amendment, small)

**Why.** 0.16.0 must not tell adopters to add `kind`/`governed-by` to every fact (check 2 today) when 0.18.0 removes both (2.1). 0.15.0 adopters have four-valued `kind` and no checker; their first run must not be a wall of findings about fields that are about to go.

**What.** A dated, additive `## Amendment` section on 0064 (following the precedent in 0043/0044/0047/0059; ratified by 2.3a): until the fact model is settled, `kind` is accepted with any value or absent, and `governed-by` on facts is optional; the checker's check 2 stops requiring them (`TYPE_FIELDS["facts"]` becomes empty; the `KINDS` test is removed). Also, from 2.3d but cheap and valuable now: `conform` and `query` each gain one sentence — a `status: draft` guardrail or decision is reported as "proposed", never as a violation or an answer. Record both in the same amendment.

**Done when.** 0064 carries the dated amendment; checker has no fact-kind finding (unit test: a fact with `kind: mixed` and no `governed-by` yields no check 2 line); the two sentences are in the two skills.

### 1.6 [done: 0.16.0 tagged 2026-11-16, then 0.16.1-0.16.3] Cut release 0.16.0

**What.** Bump `version` in `plugins/kms/.claude-plugin/plugin.json`, `plugins/kms/.codex-plugin/plugin.json` and all 14 entries of `plugins/kms/skills/index.json` to `0.16.0` (`docs/guardrails/plugin-manifest-version-sync.md`); add `## [0.16.0] - <date>` to `CHANGELOG.md` via the `changelog` skill from history since tag `0.15.0`, covering 0056-0066 plus the phase-0 decisions and phases 0-1, and stating what a 0.15.0 adopter's first checker run will report (check 12 if templates moved; nothing about fact `kind`); tag `0.16.0` (0048).

**Done when.** Three manifests and 14 entries say `0.16.0`; CHANGELOG has the entry with the first-run paragraph; `git tag` lists `0.16.0` on the release commit.

## Phase 2 — Model redesign: eight decisions, one model rewrite, one migration

Interviews 2.1-2.8 first, in order (each builds on the previous), each a `roadmap` run producing one decision plus the disposition of the decisions it touches. Then 2.9 rewrites the model once and 2.10 migrates once. Nothing in phase 2 ships to users before 2.10 is complete; adopters see one format change in one CHANGELOG entry.

### 2.1 [done] Facts carry no outgoing edges; plain facts become admissible (decision needed)

**Why.** Today a fact must carry `governed-by` (else `TBD` = debt aged by check 17), must "ground, or could plausibly ground, a decision or guardrail" (`docs/guardrails/fact-not-audit-log.md`), must be referenced (check 7), and must not be "stated in code, tests, config" (Admission gate 1). `ARCHITECTURE.md:29`'s own example "The service runs on port 8080" fails all four; the admission gold labels agree (`evals/admission/cases.tsv` c85 → `none`). `governed-by` means two things the model never separates: on a `kind: decision` fact, the decision that fixes the value; on every live environmental fact the arrow is inverted (fact 0003 "is the descriptive basis for 0008" yet carries `governed-by: 0008`; same in 0006, 0008, 0009, 0012). `kind: decision` facts are inadmissible by construction under gate 1 (a restatement of a sibling record); 0066 deprecated every one that existed; all seven live facts are environmental; the capture eval fixture still teaches the rejected shape (`evals/capture/fixture/docs/facts/0001-datastore-choice.md`). `last-verified` is used by `capture` check 2 (`SKILL.md:15`), `bootstrap` step 3 (`:37`) and `capture/examples.md:7` but is not a field in the model.

**Recommendation.** (a) Facts carry **no outgoing edges**: delete `kind` and `governed-by` from facts. The edges live on the consumers that already have them (`grounded-in` on guardrails, `governed-facts` on decisions); backlinks are computable (`lint_check.py --refs <id>` prints who cites a file; `query` prints "cited by"). Record that 0064's definitions are not disputed; 0065's gate 1 made the `decision` value empty by construction, so the field carries no information. (b) Add optional `source: <url | path | command>` (where to re-observe) and `last-verified: <date>` (last confirmed against `source`; moves only when re-observed, not on any edit) on facts; define both once. (c) Admission gate 1: "carried" means recoverable by one grep of the fact's own `source` path or of one file the reader would find first; a fact that *aggregates two or more sources* or *locates something not greppable* (an external system, a vault path, a dashboard, a vendor limit) is admissible uncited; a mechanical repeat of one value in one file is not. (d) Check 7 for facts becomes bounded: a fact with neither `source` nor any citer is noise; one with a `source` is not. `fact-not-audit-log` is rewritten: a fact is noise when it records an event, not when it is unreferenced. (e) Guards against sprawl: `bootstrap` step 2 writes location/aggregation facts only on request and with a stated cap; the stale-fact check (3.4) applies only to facts whose `source` is external (URL or command), since repo-path facts are checked by `conform`'s path overlap.

**Dispositions.** 0064: superseded (kind removed). 0009: amended (fact fields changed). 0015: left active; its "one-time observation" sentence is reconciled in 2.6. `fact-governance-fields` (guardrail): re-derived in 2.10 to require `source` or a citer, not `kind`/`governed-by`. `uninstall` category 4 ("facts still `governed-by: TBD`") and `bootstrap` steps 2 and 8 (`governed-by: TBD`): rewritten in 2.9/2.10. Alternative considered: keep `governed-by` optional; cheaper but keeps the inverted arrow.

**Done when.** Decision active with `accepted-by`; 0064 archived with pointer and index rows; 0009 amended; the decision names the five texts 2.9/2.10 will change.

### 2.2 [done] Make the derivation edges honest (decision needed)

**Why.** The model says a guardrail is "derived from an axiomatic commitment plus a descriptive fact" and "only valid while its sources are current", but `grounded-in` may hold "the same id already in `governed-by`" (0051). Tally over the 17 live guardrails: 6 "grounded" in `0001-knowledge-artifact-storage-convention` as filler ("establishes the base frontmatter"); 3 in their own `governed-by` (`one-statement-one-job` [0027], `token-economy` [0026], `no-unenforced-guardrail` [0027 plus fact 0008]); 1 in another decision; 2 in a sibling guardrail; 3 in facts now `deprecated` in `docs/facts/archive/` (`agent-agnostic-skill-content` → 0002, `guardrail-derivation-fields` → 0014, `version-bump-requires-changelog-entry` → 0013); 1 `TBD`; 2 in live independent facts (`plugin-manifest-version-sync` → 0003, 0008; and `no-unenforced-guardrail`'s second entry, 0008, already counted above among the self-grounded). The seven buckets sum to 18 because that one file is counted twice. `ARCHITECTURE.md:67-69`'s flagship example (0006 + 0002 → `agent-agnostic-skill-content`) has both sources retired and the guardrail is `active`, still `governed-by: 0006` (superseded); 0066 said "Nothing else is changed", contradicting the model. Nothing says what a guardrail does when its decision is superseded. `governed-by` is scalar while `plugin-manifest-version-sync` has two governing decisions (0008, 0035 as an "Extension" bullet). `derivation-note` has a stated shape ("given decision X and fact Y, Z must follow") but nothing checks it and three seeded copies carry a provenance line ("Seeded from kms's shipped guardrail templates, per 0027") instead. Procedures have `operationalizes` but no `governed-by`, although 0013 and 0042 created procedures.

**Recommendation.** `governed-by` on guardrails becomes a list of one or more decision ids, each resolving to a non-superseded decision (re-pointed in the same edit that supersedes the old one; `capture` check 1 does this). `grounded-in` becomes optional and fact-only; absent means "a direct consequence of the governing decision(s)". `derivation-note` must name every id in the two edges; may be `TBD` only while `governed-by` is `TBD` (seeded templates). Retired source rule: a deprecated `grounded-in` fact or superseded `governed-by` decision triggers re-derivation in the same pass (`guardrail-re-derivation-on-source-change` already says so): re-point and note "re-derived <date> from <id>" if the consequence stands, else deprecate the guardrail. Optional `governed-by` on procedures. The "extension" case is a second list entry. Templates ship `governed-by: TBD`, no `grounded-in`, `derivation-note: TBD`; `template-version` stays 1 (the migration script rewrites seeded files' frontmatter; check 12 is unchanged).

**Dispositions.** 0051: superseded. 0039: amended (`superseded-by` scope, see 2.3). 0027/0045: left active; the template frontmatter change is recorded as an amendment to 0027.

**Done when.** Decision active; 0051 archived with pointer; the decision lists the 17 guardrails' new edges (filled in 2.10).

### 2.3 [done] Define the lifecycle words the model already uses (decision needed)

**Why.** Eight `## Amendment` sections in four accepted decisions (0043 ×3, 0044 ×3, 0047, 0059); `fitness-functions` rewritten after acceptance (0040 at `4b356a4`, 0043 at `f025262`); 0008 gained `fitness-functions` 44 days after acceptance (`4db79fd`); `capture` check 1 itself edits an accepted decision's `status`/`superseded-by`; yet the model says "immutable once accepted" and `CONTRIBUTING.md:76-78` says "never an edit to the original". `date` is undefined. `deprecated` is undefined and 0066 used it for facts that are still true. `draft` has no stated force (1.5 fixes the `conform`/`query` half). `superseded-by` is decision-only in the model (0039), `status: superseded` is allowed on all four types, the checker demands `superseded-by` on all four, and a replaced fact (0012 replacing archived 0010, "now superseded") has no pointer. `expires` is "a date or condition" in one field, which is why check 4 is judgment. `docs/<type>/archive/` is described in an archived decision (0041), the lint preamble and bootstrap step 10, not in the model.

**Recommendation.** (a) Immutability scope: `## Decision`, `## Why`, `## Tradeoffs considered` frozen once `active`; `status`, `superseded-by`, `accepted-by`, `tags`, `expires`/`expires-when`, `fitness-functions` and dated, additive `## Amendment <date>` sections are editable. (b) `date` = creation date, never moves. (c) `deprecated` = retired without replacement; the body's first line after the frontmatter states why (no new field); `superseded` = replaced by a named successor; `superseded-by` allowed on all four types (reverses that clause of 0039 on the evidence of 0012/0010). (d) `draft` = proposed, not binding (ratifies 1.5). (e) `expires: <date>` (structural) and `expires-when: <condition>` (judgment), either or both. (f) One sentence on `archive/` in the model's File formats.

**Dispositions.** 0039: amended (c, e). 0053: left active. `lifecycle-status-values`, `superseded-decision-requires-pointer`, `decision-expires-must-be-reevaluated`: re-derived in 2.10. `CONTRIBUTING.md` Governance paragraph: rewritten in 5.3.

**Done when.** Decision active; 0039 amended in the same commit; the six rules are listed in the decision verbatim as they will appear in the model.

### 2.4 [done] Registries by marker; define the fitness-function inventory and `last-verified` (decision needed)

**Why.** Files that are not instances of any type live in the type directories: every `INDEX.md`; `docs/skills/tags.md` (a vocabulary filed as a procedure, tagged `scale`); the role lists bootstrap step 7 prescribes; `docs/facts/docs-manifest.md` (a watch-path registry filed as an un-numbered environmental fact, violating the model's `NNNN-slug` rule, passing the checker only because `kind`/`governed-by` were added by hand). The "fitness-function inventory" is written by `bootstrap` step 5 and `capture` check 3 and exists nowhere; lint check 18 reads only the `fitness-functions` field on decisions (seven carry it). The `kms-seeded`/`kms-generated` markers are frontmatter on some files and an HTML comment on `INDEX.md`; the model mentions neither form (it contains no `kms-` string; the forms are described in bootstrap, uninstall and lint).

**Recommendation.** No new directory, no new files. (a) A declared non-governed file class, **registry**, identified by `kms-registry: <name>` in frontmatter (or `<!-- kms-registry: <name> -->` as first line for a pure CSV); registries are excluded from the four types' checks and from Admission, included in the sync checks (19 for indexes, 21 for tags), and listed by `uninstall` under one category. Existing files stay where they are: `INDEX.md`, `docs/skills/tags.md`, the role lists, `docs/facts/docs-manifest.md`. (b) The fitness-function inventory **is** the union of decisions' `fitness-functions` lists; each entry becomes a small map `{check: <text>, enforced-by: <code path | ci job | hook | procedure id | none>, last-verified: <date>}` (editable per 2.3a); `capture` check 3 and `bootstrap` step 5 append to the governing decision's list, or draft a `status: draft` decision stub when no decision governs the rule (a rule worth automating is a commitment). (c) `last-verified` is defined once (2.1b) and the docs manifest uses the same word. (d) Marker forms stated in the model: frontmatter field where frontmatter exists, first-line comment otherwise; `kms-seeded`, `kms-generated`, `kms-registry`.

**Dispositions.** 0049: left active (indexes are registries; format unchanged); 0041 is already superseded and untouched. 0013: amended (role lists are registries, proposal-only per 3.6). 0029: amended (docs manifest is a registry).

**Done when.** Decision active; the two amendments are in the same commit; the decision names the skills 2.9 will update (`bootstrap` 3/5/7/10, `capture` 3/5/7, `lint` 18/19/21, `uninstall`, `query`/`onboard` index reads).

### 2.5 [done] Settle the names without renaming directories (decision needed, small)

**Why.** The type is "Procedure" (model); the directory is `docs/skills/`; the index says "Skills index"; the tag is `procedural`; bootstrap and README say "fact/decision/guardrail/skill"; decision 0013 says "skill-prescription artifacts"; bootstrap calls decisions "intents" ("Intent extraction"); `roadmap/SKILL.md:84` lists "fact / intent / guardrail / skill / plan" and `:26` says "knowledge-steward-style" (0031 renamed steward to capture). The guardrail id `decision-expires-must-be-reevaluated` applies to all four types.

**Recommendation.** Keep `docs/skills/` (a rename would leave every adopter's immutable decisions citing stale paths forever and add permanent two-layout detection; kms's own tree has 43 such references under `docs/` outside `docs/plans/`). Fix the index title to "Procedures index"; purge "intent", "skill prescription", "steward" and "fact/decision/guardrail/skill" from shipped bodies, from the `description` frontmatter of `lint`, `bootstrap` and `query` (keeping their trigger phrases otherwise), and from the bootstrap AGENTS.md block in favour of fact, decision, guardrail, procedure; rename the guardrail to `artifact-expires-must-be-reevaluated` (guardrails are refined in place; referrers updated; decisions keep the old id as history). Record the directory rename as deferred with trigger "a second adopting project asks".

**Dispositions.** 0001: left active (the directory stands). 0031: left active.

**Done when.** Decision active; `grep -nE "knowledge-steward|skill prescription|fact / intent|fact/decision/guardrail/skill" plugins/kms/skills/*/SKILL.md plugins/kms/shared/*.md` returns nothing (checked after 2.9).

### 2.6 [done] Reconcile the admission test with the rules it contradicts (decision needed)

**Why.** 0015:36 (active): "A one-time observation that actually grounds a guardrail … is exactly the kind of fact this system wants"; the Admission section (0065, active): "Reject a raw reading, run result, status or timestamped event"; 0066 then deprecated fact 0013 ("CHANGELOG.md lagged four manifest version bumps"), 0015's archetype and the sole `grounded-in` of `version-bump-requires-changelog-entry`. Admission says "Name a role or system, not a person" while `accepted-by` holds a person's name in 0065/0066. Gate 1's "not already carried … in a sibling record" collides with the requirement that a fact be cited: once a decision cites and restates it, the fact is "carried". 0066 concedes 27 legacy records bundle several claims and gives adopters no guidance. 0065's known misses (c10, c14, c26) are all real kms decisions.

**Recommendation.** One decision: (a) an incident-grounded fact is admitted when a guardrail cites it in `grounded-in`, and retires with that guardrail, not before; for `version-bump-requires-changelog-entry` take the cheaper branch: `governed-by: [0050]`, no `grounded-in` (2.2 makes it fact-only), derivation-note naming 0050, and leave 0013 archived (re-admitting 0013 would partly reverse 0066); (b) `accepted-by` is the one field that may name a person, because it records accountability; it may hold a role or team instead; (c) "carried" per 2.1c, and a fact cited by a decision is not carried by its citer; (d) legacy records predating the admission test are not split retroactively and `lint` does not flag them; the one-claim gate applies to new and re-derived records. Parts (b) and (d) are the adopter-facing sentences; (a) and (c) tidy kms's own corpus.

**Dispositions.** 0015: amended (a). 0065: amended (b, c, d). 0066: left active.

**Done when.** Decision active; the two amendments are in the same commit; the four sentences are listed verbatim for 2.9.

### 2.7 [done] Make four more lint checks deterministic; keep pins optional (decision needed)

**Why.** `evals/lint-matrix/results-2026-11-08.md`: judgment recall 0.00 on checks 5, 6, 8, 10, 11, 14, 24; 0.20 on 13, 16, 18; 0.40 on 17, 22, 23; 0.80 on 4; precision 0.20 on 23; 0.20 false-alarm rate on a clean corpus. Pinned edges moved check 13 from 0.20 recall to 1.00 with no false alarms. Checks 17 and 22 are "judged the same relative way check 14 judges a role gone cold" (`lint/SKILL.md:34,39`) while 14 defines no method and 18 says only "in a long time"; none is reproducible. But mandatory pins would make `python3` plus PyYAML a precondition for authoring a guardrail (a human in an editor, or a Codex/Kilo agent without Python, writes a file that fails check 2), against decision 0011's git-plus-Markdown substrate.

**Recommendation.** With 2.3's fields: check 4 on `expires:` dates is structural (`expires-when` stays judgment); check 17 on `TBD`/`draft` with file `date` is structural; check 24 is structural once the step-legend format is fixed (`### N. [done|pending|blocked...]`, as this plan uses); check 18 is structural on `fitness-functions[].last-verified` (2.4b). One threshold, one number, stated once in the model: 180 days, overridable by one line in the AGENTS.md block. Pins stay optional (0062 stands): an unpinned edge yields one advisory line ("unpinned: run `--pin`"); `bootstrap` and `capture` pin when the checker is available. `PIN_IGNORED` widens to `accepted-by`, `last-verified`, `status`, `superseded-by`, `expires`, `expires-when` (pins track content, not lifecycle; amends 0062). Checks 14 and 22 (role and tag gone cold) and 23 (`enforced-by`-based) are deferred until their registries carry dates (Deferred section). Checks 5, 6, 8, 10, 11, 16 stay judgment and the lint output labels them "advisory" (that word only; no recall numbers in a user's output). Relabel per 0061's rule and record a second-rater pass on the relabelled texts.

**Dispositions.** 0062: amended (`PIN_IGNORED`). 0061: amended (new labels). 0058: amended (checks 4, 17, 18, 24 join the script). 0040/0047: left active.

**Done when.** Decision active with the three amendments; the decision lists the final structural/judgment split by number (expected: structural 1, 2, 3, 4, 7, 9, 12, 13-pinned, 15, 17, 18, 19, 20, 21, 24; judgment 5, 6, 8, 10, 11, 13-unpinned, 14, 16, 22, 23; 3.4 later adds structural check 25).

### 2.8 [done] Give open questions and hypotheses a stated home (decision needed, small)

**Why.** Kinds of knowledge with no home: open questions (0053:35 refers to "the still-open question of stating kms's own governance" living only in prose), assumptions, risks, hypotheses (0014 gives "when the hypothesis test completes" as its example `expires` condition, with no record for the hypothesis itself), goals (every plan is disposable per 0037), experiment results (0065's tables live in a decision body), ownership beyond `accepted-by`.

**Recommendation.** No fifth governed type, no registry. (a) An open question or hypothesis is a decision in `status: draft` carrying `expires-when: <the test or event that closes it>` and the tag `question`; `uninstall` category 4 and lint check 17 exempt a draft that carries `expires-when` (it is a question, not an abandoned stub); Admission's "Typical rejections" says so, so agents do not invent a shape. (b) Goals and open plans: each plan's own `status:` line is the record; check 24 reads it; no cross-plan file. (c) Experiment results stay in the decision that cites them, with raw data committed under `evals/` or named as not committed (4.3). (d) Risks and assumptions are rejections, with the pointer "a risk that changes behaviour becomes a guardrail; an assumption a decision rests on becomes a fact with `source`".

**Dispositions.** 0037: left active (reaffirmed). 0030: amended (uninstall category 4 exemption).

**Done when.** Decision active; 0030 amended in the same commit; the rejection sentences are listed verbatim for 2.9.

### 2.9 [done] Rewrite the shared model as two files

**What.** Split `plugins/kms/shared/artifact-model.md` into (1) `artifact-model.md`, the normative **schema** read by every skill: types (four governed, registries by marker), one definition per field (`id`, `title`, `status`, `date`, `tags`, `expires`, `expires-when`, `source`, `last-verified`, `scope`, `governed-by`, `grounded-in`, `derivation-note`, `pinned`, `track`, `superseded-by`, `governed-facts`, `fitness-functions` map form, `accepted-by`, `operationalizes`, markers), lifecycle (status meanings, immutability scope, supersession and deprecation rules, `archive/`), edges (direction, list-ness, allowed targets, re-derivation on retirement), knowledge-directory detection ("the directory containing `decisions/`; procedures live in `skills/`"), file formats, index CSV, the 180-day threshold; target 600 words, exactly what the checker enforces; and (2) `admission.md`, the **writing guide** read only by `bootstrap`, `capture`, `roadmap` (and `quickstart` through them): the gates and signals as amended by 2.6, the rejection list from 2.8, the economy rule. `lint`, `conform`, `uninstall`, `query`, `onboard` load only the schema. Remove the parentheticals citing this repo's decisions (`0063-...`, `0051-...`). Update every skill that restates part of the model to say "per the artifact model" (the `roadmap` paragraphs restating modes, `track`, `status`, `expires`, `accepted-by`; the index rule stated in four skills; the umbrella-tag exclusion stated in four; the "apply Admission, say which gate failed" sentence stated in four). Update `lint_check.py` to the schema (list `governed-by` on guardrails, fact-only `grounded-in`, typed targets per field, `superseded-by` on all types, `expires` date check, `fitness-functions` map, `--refs <id>`, registry marker exclusion, detection sentence, threshold flag, advisory unpinned line, the bounded check 7 for facts from 2.1d, the check 17 exemption for a draft carrying `expires-when` from 2.8a, and a tolerant mode: a 0.16.0-shaped file (fact `kind`/`governed-by`, scalar guardrail `governed-by`, string `fitness-functions` entries) yields one advisory line per file and no finding unless `--strict` is passed) with unit tests, and the lint skill's check list and labels per 2.7. Ship both files through 1.1's channel.

**Done when.** `wc -w` of `artifact-model.md` ≤ 700 and of `admission.md` ≤ 600; a hand-made list of every frontmatter field name mentioned in any `SKILL.md` or the checker (take it from `grep -ohE "\`[a-z][a-z-]+\`" plugins/kms/skills/*/SKILL.md | sort -u`, filtered to field names by eye) is a subset of the schema's field table, recorded as a comment at the end of the schema; `grep -rn "docs/decisions/00[0-9]" plugins/kms/shared/*.md plugins/kms/skills/*/SKILL.md` returns nothing (placeholders such as `000X-...` and `attribute`'s `Refs:` example in `examples.md` are outside that pattern or path); the checker's constants match the schema; unit tests pass.

### 2.10 [done, except matrix regrade and eval run: blocked, needs provider key] Migrate kms's corpus, the templates and every eval fixture in one pass

**What.** Write `plugins/kms/shared/migrate.py` (ships through 1.1's channel; `--docs DIR`; idempotent; rename/move only): delete `kind` and `governed-by` from facts; scalar guardrail `governed-by` → one-element list; `grounded-in` entries that are decision or guardrail ids → removed (printed for re-derivation); `expires` values that parse as a date stay, others move to `expires-when`; `fitness-functions` strings → maps with `check:` only; seeded files' frontmatter (`derivation-note: TBD` where it is the provenance line); registry markers added to `INDEX.md`, `tags.md`, `docs-manifest.md`; index regenerated. Run it on `docs/`, on every `evals/*/fixture/docs`, and on `evals/lint-matrix/cases/*/docs` (regenerate via `build.py` where generated); then do by hand what the script cannot: re-derive every guardrail under 2.2 (the three on deprecated facts; the six on 0001 filler get an absent `grounded-in`; the three self-grounded ones; `every-skill-ships-examples` gets `governed-by: [0018]` and no `grounded-in` (0066 deprecated the roster facts its `TBD` waited for; 2.2 allows an absent `grounded-in`); `version-bump-requires-changelog-entry` per 2.6a; `agent-agnostic-skill-content` re-pointed from superseded 0006 to 0008 or deprecated); add `source` and `last-verified` to the seven live facts; pin every guardrail with `--pin`; `scope` on facts that are environment-bound (0012 at least); re-derive `fact-governance-fields`, `lifecycle-status-values`, `superseded-decision-requires-pointer`, `artifact-expires-must-be-reevaluated` to the new rules; fix `evals/capture/fixture`'s `kind: decision` fact. Update `evals/lint-matrix/build.py`, `labels.json` and `evals/lint/fixture` so the matrix grades the 2.7 split, and replace `build.py:82`'s `.keep` hack with the five templates seeded in the base fixture.

**Done when.** `python3 plugins/kms/shared/lint_check.py --root . --strict` exits 0; the migration script exits 0 and changes nothing on a second run over `docs/` and every fixture; `python3 -m unittest discover` passes for all three suites; `npm run eval` is green on one run; no live fact or guardrail points at a superseded decision or a deprecated fact (decisions are left as history, as check 20 says); every live guardrail has a `pinned` map.

## Phase 3 — Cover the processes the system misses

Budget rule for this phase: the sum of `wc -w` over all fourteen `SKILL.md` files at 0.18.0 is at or below the sum at 0.16.0; per-file growth is allowed only in `conform` (+120 words, 3.2), `capture` (+60, 3.4), `query`/`onboard`/`refactor-plan` (+25 each, 3.4), `changelog`/`quickstart`/`uninstall` (+40 each, 3.6); 2.9's de-duplication and 3.6's `lint`/`bootstrap`/`roadmap` cuts pay for them.

### 3.1 [superseded: `roadmap` and `clarify` are deprecated and leave in 0.17; `decide` carries the interview] Stop duplicating the interview mechanics

**Why.** `plugins/kms/skills/clarify/SKILL.md:7-18` is reproduced near-verbatim in `roadmap/SKILL.md` ("Interview mechanics"; three small wording differences, one bullet missing). `clarify` is self-contained and works on every channel today.

**What.** Leave `clarify` whole. In `roadmap`, replace the block with "Interview exactly as the sibling `clarify` skill does (`../clarify/SKILL.md`): one question at a time, look facts up, put decisions to the user with a recommendation, cap options at four." Skills are siblings in every layout, including the Kilo cache, so no new shared file is needed. `quickstart` already defers to `roadmap`.

**Done when.** The block appears once in the plugin; the roadmap eval still passes.

### 3.2 [pending] Give `conform` the whole changeset (decision needed, small)

**Why.** `conform` checks only guardrails and decisions, defers any diff touching `docs/` to `lint`/`capture` (decision 0032: "scope excludes changes to the knowledge base's own artifacts entirely"), so a PR touching code and a guardrail gets a split review, and never asks whether a fact the diff falsifies is now wrong.

**What.** A decision amending 0032 in part. `conform` gains: (1) a docs pass: when the diff touches the knowledge directory, run `lint_check.py` on the post-diff tree (for a staged diff: the working tree; for a range: a temporary checkout of its head) and report its lines in the same output; (2) a structural fact pass: list facts whose `source` or `scope.component` path-overlaps the diff as "re-verify"; (3) advisory only: a fact whose body names a value the diff changes, flagged "may be falsified" without claiming it is. Draft handling is already in (1.5). Keep it read-only.

**Done when.** Decision active and 0032 amended; `conform/SKILL.md` has the three passes within +120 words; `conform/examples.md` gains one example; new eval `evals/conform/` (fixture: a diff changing a port a fact `source`s and violating one guardrail; sentinel lines `CONFORM_VIOLATIONS: <ids>` and `CONFORM_REVERIFY: <ids>`) is in the workflow matrix and `package.json`'s `eval` list.

### 3.3 [pending] Put the triggers in the AGENTS.md block; fix the lint nudge's layout bug

**Why.** The only automation is two `SessionStart` nudges, Claude Code only. The block `bootstrap` step 9 writes names `capture`, `lint`, `query` but not `conform`, and that block is the only cross-agent trigger. `plugins/kms/hooks/lint-nudge.sh:18-19` hardcodes `docs/facts docs/decisions docs/guardrails docs/skills`, a silent no-op on any other layout. A post-commit `conform` nudge would be mis-timed (conform is pre-commit) and wallpaper on an active team, so no new hook now.

**What.** (a) The block gains: "Run `conform` before committing. Run `query` before designing anything that touches a recorded decision." (b) `lint-nudge.sh` detects the knowledge directory per the schema's sentence (walk `docs/`, else any directory containing `decisions/`). (c) `docs/skills/automating-lint-nudge.md` notes the detection. The lint-nudge signal change (compare against the last lint run) is deferred (Deferred section).

**Done when.** The block text in `bootstrap` has both sentences; `sh plugins/kms/hooks/lint-nudge.sh` prints the note on a scratch repo whose knowledge directory is `knowledge/` with six KB commits in 14 days.

### 3.4 [pending] Verify facts, not only derive from them

**Why.** Environmental facts say "re-verify before relying on it again if much time has passed" and nothing does; `capture` check 2 depends on the session remembering; facts have no source path until 2.1.

**What.** (a) `capture` check 2: "for every fact whose `source` is a path the session changed, or whose `scope.component` overlaps the diff, re-observe it; bump `last-verified` only if re-observed, correct it if changed" (+60 words). (b) New structural lint check 25 (recorded as an amendment to 2.7's decision, since that decision fixes the structural/judgment split): a fact whose `source` is a URL or command and whose `last-verified` is older than the threshold, or whose `source` is a repo path that no longer exists; a fact with no `last-verified` is reported once as "never verified" (advisory). (c) `query` and `onboard` print `last-verified` beside a citation older than the threshold. (d) `refactor-plan` phase 4 lists facts by `source` overlap.

**Done when.** The four skill texts carry the rule; check 25 has a unit test and a lint-matrix fixture; kms's seven live facts carry `last-verified`.

### 3.5 [pending, retarget: put the paragraph in `decide`, not `roadmap`] Give events an entry point inside `roadmap`

**Why.** Incidents, postmortems, retrospectives and failed experiments produce exactly the residue kms stores, but no skill starts from an event: `roadmap` interviews toward a change plan, `capture` needs a session that touched records, and Admission rejects the event itself (correctly) without saying where it goes. A fifteenth skill was considered and rejected for this release: it doubles the surface a one-maintainer project keeps green, on no more evidence of need than the `question` type 2.8 declined.

**What.** One paragraph in `roadmap`: "When the input is an event (an incident, a failed experiment, a retrospective, a dependency breakage), interview from the event to its admissible residue: a root-cause fact with `source` pointing at the incident record, a generalised guardrail (the recurrence gate applies: a one-incident prohibition needs a cause that generalises), a procedure, a process decision. The event record itself is rejected by Admission and lives in the tracker the fact's `source` names. The plan file is optional for an event." Add `roadmap/examples.md` example 4 (an incident) and an eval case in `evals/roadmap/` with an incident prompt grading that a guardrail, not an event log, is proposed. Record in the Deferred section: a standalone `retro` skill, trigger "the roadmap paragraph is used in three real incidents and proves too thin".

**Done when.** The paragraph is in `roadmap` (its `description` gains "turn an incident or retro into knowledge"); example 4 exists; the eval case passes once.

### 3.6 [pending, re-scoped: skip the role-list bullet and the `roadmap`/`changelog` bullets, apply the `roadmap` numbering and synonym fixes to `decide` if it has them] Smaller skill fixes found by the review (one commit each)

- `bootstrap` step 7: role lists become a proposal written only on confirmation (every consumer says "if present"; kms's own repo never had them; `CONTRIBUTING.md:69-70` says there is no role list); the inline rationale shrinks to "default to process when ambiguous". Steps 5-7 each start with "ask before writing".
- `bootstrap` step 1: print `git rev-list --count HEAD`; above 1,000 commits ask how far back to mine (recommend two years). Salvaged from `scale-bootstrap-lint-chunking` (`a6a583b`; branch deleted 2026-11-16, tip 0767100ab21f, see 5.7).
- `bootstrap` step 3: state the docs manifest's frontmatter (registry marker) and row shape.
- `bootstrap` step 6: add non-software rows (data provenance, method choice, literature claim, approval or publication gate) so 0011 has teeth; `onboard` takes a duration (default five days).
- `bootstrap`/`capture` stub recipes: "base frontmatter per the model, plus …" (today they omit `date`, `tags`).
- `bootstrap` "Before starting": "default to the structure above" → "the layout in the artifact model".
- `roadmap`: next number = highest across the directory *and its `archive/`* plus one (`:34` "count existing files" collides after an archive move); drop `:26` "knowledge-steward-style" and `:84`'s "fact / intent / guardrail / skill / plan".
- `quickstart`: say the plan file will be written (or skip it for the one decision); detect the knowledge directory as `bootstrap` does instead of testing `docs/` literally.
- `uninstall`: drop the stale parenthetical list of `kms-generated` files; add the registry category; define "remove" for a seeded guardrail as uninstall-path only; add a `kms-declined: [<id>, ...]` line to the AGENTS.md block that lint check 12 and bootstrap step 8 honour, so a team that deletes a seeded guardrail is not re-seeded and re-flagged forever (an amendment to 0027, which today offers detach as the only opt-out).
- `changelog`: when commits carry `Refs:` trailers, list the referenced decisions under the entry.
- `lint`: cut the duplicated justification of the archive exclusion and of check 24's non-governance (about 250 words); label judgment checks "advisory"; add `--changed-since <ref>` as an optional scope for judgment checks on large corpora.
- `capture`: the re-pin sentence stays; check 7 (index) names registries.
- All skills: the synonym purge from 2.5.
- Not done: a `brainstorm` cross-check against decisions (would reverse 0019, which says brainstorm "never queries `docs/{facts,decisions,guardrails,skills}/`"; `conform`/`query` already answer "was this rejected").

**Done when.** Each bullet is one commit naming it; every touched `SKILL.md` re-read whole; `grep -n "5-day\|count existing files\|knowledge-steward\|or derived" plugins/kms/skills/*/SKILL.md` returns nothing; the phase-3 word budget holds (`wc -w plugins/kms/skills/*/SKILL.md` compared with the 0.16.0 tag).

## Phase 4 — Make the evidence real

### 4.1 [pending, re-scoped: no cases for `clarify`, `brainstorm`, `refactor-plan` or `changelog`] Eval cases for the unmeasured skills

**Why.** Nine of fourteen skills have no eval (`quickstart`, `brainstorm`, `clarify`, `query`, `onboard`, `refactor-plan`, `conform`, `changelog`, `uninstall`); `attribute`'s eval is two regexes on the transcript and passes whether or not a commit was made; the CI `lint` case grades three violations that are all structural now, with no clean control.

**What.** Regex-gradeable cases with a sentinel line, as `evals/lint` does: `query` (answer ends with `Refs:` lines naming the two planted artifacts; says "nothing relevant" on an unanswerable question); `conform` (3.2); `changelog` (section headings, one bullet per planted commit, no `[Unreleased]`); `uninstall` (reports the planted seeded guardrail, registry and draft stub, writes nothing); `attribute` (assert on `git log -1 --format=%B` in the fixture, not the transcript). Add a clean-control test to `evals/lint` (all sentinels `NO` on the unmodified fixture). `brainstorm`, `clarify`, `onboard`, `refactor-plan`, `quickstart` stay unmeasured; `AGENTS.md` says so.

**Done when.** The five cases exist; the workflow matrix and `package.json` list them; one green run is recorded in the 0.18.0 CHANGELOG entry.

### 4.2 [pending] Re-run the lint matrix and the admission eval on the pinned model, once, after 2.10 and 3.4

**Why.** The matrix numbers come from an Nvidia model, mix first-pass and re-run results per case, and "Raw promptfoo output is not committed"; the admission numbers (0065) are development-set results from Sonnet-class subagents on the 66 cases the wording was tuned on; the shipped text was never run through Kilo; the held-out set "is not here" (`evals/admission/build.py:3`) and was never run; `cases.tsv` leaks labels (c02 "real kms 1fe279c, decision 0046"; c11/c17 name a "log row"/"plan Log"); the admission fixture is empty (`fixture/.keep`), so the "already carried" gate is untestable.

**What.** Strip decision numbers and type words from `cases.tsv`; give the admission fixture a small real tree; run both on the CI-pinned model (`cohere/north-mini-code:free` or its successor per 0057) with `--repeat 5`, one clean pass each, after 2.10 and 3.4 have landed (so the run measures the shipped split, check 25 included, not a state about to change); commit `evals/lint-matrix/out-<date>.json` and `evals/admission/out-<date>.json`; rewrite the results files from them. Held-out set: commit it under `evals/admission/held-out/` and run it once, or record "held-out set not in the repo, never run" in an amendment to 0065 (2.3a rule); either is acceptable, say which.

**Done when.** Both results files cite a committed raw output; 0065 carries an amendment with the pinned-model numbers and the held-out disposition; `.keep` is gone from the admission fixture.

### 4.3 [pending] Bring the study's evidence into the repo or declare it not committed

**What.** 0066 cites "the author's repo, `docs/plans/knowledge-boundary/step6b/`" for rater verdicts; `evals/lint-matrix/label-agreement.md` is author-versus-model, `kind-agreement.md` is model-versus-model and self-described as "a fit to these facts, not a held-out result". Copy the verdict files under `evals/admission/raters/` if they exist; otherwise add one amendment line to 0066 saying they are not in the repo. Reword the two agreement notes to claim "classifiable by a model reader", not inter-rater reliability.

**Done when.** Every evidence citation in 0059-0066 resolves to a committed file or an explicit "not committed" line.

## Phase 5 — Dogfood, human docs, release 0.18.0

### 5.1 [pending, role lists moot; check which `fitness-functions` and `last-verified` items the consolidation already did] Run `bootstrap` gap-fill and `capture` on kms itself

**What.** Fill every blank `last-verified` in `docs/facts/docs-manifest.md` (blank since creation 2026-09-12 while README/AGENTS/ARCHITECTURE changed); convert the seven decisions' `fitness-functions` to the map form with `enforced-by` and `last-verified`; role lists only if the owner confirms (otherwise one sentence in the AGENTS.md block says kms uses none); add kms's own `<!-- kms:start -->` block to `AGENTS.md` or one sentence in 0029's amendment exempting the plugin repo (today the marker exists only inside a comment).

**Done when.** No blank `last-verified` in the manifest; all seven `fitness-functions` fields are maps; the AGENTS.md question is settled either way.

### 5.2 [pending, also: fifteen skills incl. `decide`, five deprecated, `CLAUDE.md` mirrors it] Rewrite `AGENTS.md`

**What.** Last substantive edit `fa9e08d` (2026-09-10). Wrong today: line 7 "plus one small POSIX shell script" (two hooks and a 416-line checker needing PyYAML); line 63 "There are no automated checks" (three unit suites, two eval matrices, a checker); the Structure block lists `hooks/hooks.json`, `shared/<topic>.md`, `evals/<case>/promptfooconfig.yaml` and `evals/providers/kilo-runner.sh` and omits `hooks/lint-nudge.sh`, `shared/lint_check.py`, `shared/admission.md`, `shared/migrate.py`, `evals/{lint-matrix,admission,lint/unit,conform}`, `evals/providers/kilo-judge.sh`; the Validation section must name the unit tests and `npm run eval`'s scope (0.6). Keep it terse.

**Done when.** Every path in the Structure block exists; the two false claims are gone; the docs manifest's AGENTS.md rows get a fresh `last-verified`.

### 5.3 [pending] Update `ARCHITECTURE.md`, `docs/skills/kms-architecture.md`, `README.md`, `CONTRIBUTING.md`

**What.** `ARCHITECTURE.md`: the artifact-model section gains Admission, registries, `source`/`last-verified`, `expires`/`expires-when`, pins; replace the derivation example (lines 67-69) with a guardrail whose sources are live after 2.10; correct the "deliberately left out" `scope` bullet (0063 reinstated a typed one); extend the decision history with 0058, 0062, 0065 and the phase-2 decisions; in "How the skills fit together" add the per-skill Reads/Writes/Blocks table and the "What this system does not do" table salvaged from `origin/fix-eval-doc-drift` (`5593e6a`), rewritten to the current model. `docs/skills/kms-architecture.md:16` still says "see `bootstrap` or `capture`'s own `SKILL.md`" for the model (moved to `shared/` by 0034) → point at the two shared files; add the registry class. `README.md`: skill table wording for `roadmap` (events) and `conform` (facts); Installing points at the per-agent caveats. `CONTRIBUTING.md`: Governance paragraph restates 2.3's immutability scope; the grep patterns gain `kilo|codex|openai` and a `docs/decisions/[0-9]{4}` form without requiring `.md`, so the scoping doc's tell-tale pattern is caught.

**Done when.** Every decision id named in `ARCHITECTURE.md` resolves; the manifest rows for these files have fresh `last-verified`; `grep -n "own .SKILL.md" docs/skills/kms-architecture.md` returns nothing.

### 5.4 [pending] Record the study tags and why three branches were not merged (decision needed, small)

**What.** One process decision: `study-v1` and `study-v2` are measurement snapshots exempt from 0048's "tags match plugin.json" rule, never reused; `origin/harness/impl/step_01` (an autonomous self-improvement loop on OpenCode: its checker was rejected in 0058; its 13 draft decisions 0060-0072 collide with master's 0060-0066; auto-commit contradicts `lint`'s never-fix rule) and `origin/fix-eval-doc-drift` (a model-first README superseded by 0052 and PR #51; two tables salvaged in 5.3) were not merged; `origin/scale-bootstrap-lint-chunking` (checkpointed bootstrap/lint: `shared/checkpointing.md`, `docs/.kms-checkpoints/`, abandoned when its resume evals failed with `spawn E2BIG`) is deferred with trigger "a reported bootstrap failure on a large repository after 3.6's history-size prompt is in use".

**Done when.** The decision is active and names the three branches (deleted 2026-11-16, tips in 5.7) and two tags.

### 5.5 [pending, mostly absorbed: the consolidation dispositioned 0067-0082; re-run the three queries and paste them] Verify the decision corpus is consistent

**What.** Verification only (dispositions were done inside 2.1-2.8 and 3.2): `python3 plugins/kms/shared/lint_check.py --root .` exits 0; `query` "what governs fact fields", "what is a registry", "may a guardrail be grounded in a decision" each land on the phase-2 decision, not the superseded one; no two active decisions on the taxonomy tags state opposite rules (read them; this is a judgment pass, record the result).

**Done when.** The three query answers are pasted into this step with their `Refs:` lines.

### 5.6 [pending] Full `lint` and `conform` pass on the repo

**What.** Run the shipped `lint` (checker plus judgment checks) on kms, and `conform` on the whole phase-2/3 diff against tag `0.16.0`; fix or explicitly defer every finding with a one-line note here.

**Done when.** Counts per check are pasted here and every finding has a resolution line.

### 5.7 [done 2026-11-16, early, at the owner's request: 3.6, 5.3 and 5.4 had not run] Delete the three parked branches

**What.** After 3.6 and 5.3 took what they needed and 5.4 recorded why: `git push origin --delete harness/impl/step_01 scale-bootstrap-lint-chunking fix-eval-doc-drift`. Done early: the three branches were deleted from `origin` on 2026-11-16. Tips, for restoring with `git push origin <sha>:refs/heads/<name>` while GitHub still holds the objects: `harness/impl/step_01` 206f4aefc50e, `scale-bootstrap-lint-chunking` 0767100ab21f, `fix-eval-doc-drift` 5593e6a4f11b. 3.6 and 5.3 now salvage from those SHAs (or fetch them first), and 5.4 cites them.

**Done when.** `git branch -r` lists only `origin/master` and open feature branches.

### 5.8 [pending] Cut release 0.18.0 (after the 0.17 removal release)

**What.** Bump every manifest to `0.18.0`; CHANGELOG entry (the `changelog` skill leaves in 0.17, so write it by hand or with go-getter's): the format change already shipped in 0.16.0, so list the new checks, the `conform` and `decide` changes and the eval results; tag. Create the GitHub Release from the entry.

**Done when.** Same checks as 1.6 for `0.18.0`; the checker run with `--strict` exits 0 on this repo and without `--strict` exits 0 on a 0.15.0-shaped scratch corpus (`kind: mixed`, scalar `governed-by`, no pins) with only advisory lines.

## Minimal path (two weekends)

Weekend one: 0.3-0.6, 1.2, 1.1 via option (b) plus `INSTALLING.md`'s three per-agent sentences, 1.5, 1.6 (release 0.16.0). Weekend two: 2.1 (facts drop `kind`/`governed-by`, gain optional `source`/`last-verified`, gate 1 reworded), 2.3 (d and e only: draft = proposed, `expires` split), 2.7 (checks 4, 17, 24 deterministic on one 180-day threshold), the schema half of 2.9, a ten-line `migrate.py`, the `kms-declined` line and the `conform` docs pass from 3.2/3.6, release 0.18.0 with a CHANGELOG entry that tells adopters what their first lint run will say. Everything else moves to the Deferred list with its trigger.

## Deferred, with triggers

- `docs/skills/` → `docs/procedures/` rename: a second adopting project asks for it.
- A registry directory (`docs/kms/`): a second tool needs a tooling-readable home.
- A cross-plan registry: a session is seen re-running `roadmap` without finding an open plan.
- Lint checks 14, 22 (role/tag gone cold) and 23 via `enforced-by`: the registries carry dates and three guardrails have `enforced-by` set in a real project.
- Mandatory pins: never, while authoring must stay possible without Python.
- A `PostToolUse`/`PreToolUse` `conform` hook and a lint-nudge signal based on the last lint run: an adopting team reports forgetting `conform` or the lint nudge going stale.
- A standalone `retro` skill: the `roadmap` event paragraph proves too thin on three real incidents.
- A `question` type: the draft-plus-`expires-when` shape fails on real questions.
- Checkpointed `bootstrap`/`lint`: a reported failure on a large repository after the history-size prompt is in use (5.4).
- A `domain` field: 0054's trigger (a real multi-domain monorepo).
- Codex `hooks` wiring: fact 0003's schema for it is confirmed.

## Not in this plan, deliberately

- Becoming a delivery framework (outcomes, meters, unit trees, autonomous runs): go-getter's scope.
- Literal per-role agent invocation (0013 deferred it).
- Abstracting storage away from git plus Markdown (0011).
- Hosted index or vector search: the thesis is a vocabulary, not retrieval.

## Order of execution, summarised

0.2-0.8 (0.1 whenever) → 1.1-1.5 → 1.6 (release 0.16.0) → 2.1 → 2.2 → 2.3 → 2.4 → 2.5 → 2.6 → 2.7 → 2.8 → 2.9 → 2.10 → 3.1-3.6 and 4.1-4.3 (interleaved; 4.2 after 2.10 and 3.4) → 5.1-5.7 → 5.8 (release 0.18.0).
