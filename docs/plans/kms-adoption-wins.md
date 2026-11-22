---
id: kms-adoption-wins
title: Make kms measurably useful and cheap to adopt (six wins from the 2026-11-22 review)
status: in progress 2026-11-22; PR #98 carries the first pass of steps 1-4 and 6; steps 2 (lite mode), 5 and 6 (real demo) still open
date: 2026-11-22
---

# Make kms measurably useful and cheap to adopt

## Where this came from

On 2026-11-22 a whole-design review of kms (design, uniqueness, usefulness, onboarding) ended with six recommendations. Two fresh agents then ran `quickstart` cold on unfamiliar repos (`sindresorhus/p-map`, `pallets-eco/blinker`, cloned into a scratch directory, not committed). Both finished, in about 25 tool calls with 7 to 10 self-answered questions, and both hit the same gaps: the checker was not reachable from `bootstrap`/`decide`/`conform`; the INDEX format in the skills contradicted the checker; five seeded guardrails were written without asking and were noise for an ordinary repo; a confirmed decision was left `draft`, so `query` reported it as "proposed" and `conform` ignored it; and the vocabulary ("skill" vs "procedure", guardrail, fitness function, umbrella tag, derivation, admission gate) was not understood. Evidence record: this file's Progress log and PR #98's description; the raw agent reports were not committed.

## State when this plan was saved (2026-11-22)

- Branch `feat/adoption-review` (worktree `.claude/worktrees/adoption-review`, branch cut from master at `33c5ec6`+) is pushed; **PR #98 is open and mergeable** (CLEAN). Commits: README rewrite; skills fix (checker vendored into bootstrap, capture, decide, conform; confirmed decision is `active` with `accepted-by`; bootstrap asks before seeding, literal INDEX row, step 11 runs the checker; quickstart lighter first run and plain close); bootstrap procedure wording; new advisory eval `rejected-option`; an empty CI-rerun commit.
- CI on #98, two runs: unit tests pass. `query` (answerable test) and `rejected-option` (Redis test) died with Kilo `Error: Unexpected error` / `Failed query: CREATE TABLE workspace` in both runs: a Kilo sqlite start-up collision under parallel runs, read as infra, not a graded failure. `decide` and `bootstrap` flipped between runs; `capture` failed both runs with the known "nothing to capture" answer; `uninstall` is advisory and fails (about 1/4).
- Local numbers (kilo 7.8.32 installed here, `npx promptfoo eval ... --repeat 4 --no-cache --no-share`, model `nvidia/nemotron-3.5-super-vl:free`): `capture` 3/4 (meets the 3/4 gate). `decide` and `rejected-option` were still running when the session ended; **no numbers recorded for them**. Re-run them first (step 0).
- Untracked `package-lock.json` in the worktree comes from a local `npm install`; never commit it.
- Nothing is released. These skill changes need a CHANGELOG entry and manifest bump together (`docs/guardrails/version-bump-requires-changelog-entry.md`); latest tag is `0.18.1`.

## Resume protocol

1. `cd` to the worktree `/home/sergei/projects/vivantel/kms/.claude/worktrees/adoption-review` (or recreate: `git worktree add .claude/worktrees/adoption-review feat/adoption-review`), `git status`; a dirty tree other than `package-lock.json` means a step was interrupted: finish or `git restore` it.
2. Read the Progress log below, then take the first step heading not marked `[done]` whose predecessors are done.
3. Re-run that step's "Done when" first; if it already holds, mark it `[done]`.
4. Do the step, run its checks (`python3 plugins/kms/shared/lint_check.py --root . --strict`, `python3 -m unittest discover -s evals/lint/unit`, `python3 scripts/vendor-shared.py --check`; eval cases with `npx promptfoo eval -c evals/<case>/promptfooconfig.yaml --repeat 4 --no-cache --no-share`), flip the heading, add one Progress-log line, and commit code and plan update together. One step, one commit.
5. Stop and tell the owner when a step is "decision needed", is outward-facing (merge, tag, release, publishing a demo), or needs a provider key.
6. Every change under `plugins/kms/skills/**` or `plugins/kms/shared/**` goes through the eval suite on a same-repo PR into `master`; re-read a whole edited `SKILL.md` before calling it done. Shipped text never cites this repo's own `docs/decisions/NNNN` files. Compound shell commands that mention `git` or `eval` are refused in a worktree session: run plain, separate commands (a PR comment containing the word `/eval` cannot be posted from there; use `gh run rerun <run-id>`).

## Progress log

- 2026-11-22 plan saved. Cold-start test done (two repos); README, skill fixes and the `rejected-option` eval written and pushed in PR #98; step 0 and the rest open.
- 2026-11-22 step 0(b) done: `summary_lib.harness_reason` plus the runner label the kilo sqlite start-up collision as `=== HARNESS ERROR: kilo start-up collision ===` (exit 1); unit-tested. Branch note: the owner's `feat/team-ee-sharing-gaps` does not exist and is unrelated to this plan; work stays on `feat/adoption-review`. Open for step 0: (a) local numbers, (c) merge (owner), (d) worktree removal after merge.
- 2026-11-22 step 4(a) done: README glossary (10 entries, no decision numbers; says the schema stays `1.0.0`). The `fact/decision/guardrail/skill` grep is already empty. STOPPED: local eval runs (step 0a) are refused in this worktree session (any command containing the word `eval` is blocked), so they must be run by the owner or in a new session outside the worktree guard.
- 2026-11-22 step 4(b) done: `bootstrap`, `capture`, `lint`, `conform` and `onboard` each close in plain words (one added sentence each; `quickstart` already did). Checks: `lint_check.py --strict` silent, vendor check and lint unit tests pass. Skill-text change: needs the CI eval suite on PR #98. Left for 4: (c) rename decision (owner).
- 2026-11-22 step 1: second planted case (read-through cache on `listOrders`) added to `evals/rejected-option`. NOT measured: this session cannot run the eval suite. Open: 3/4 on all three tests with `--repeat 4` on the CI model, the README rate sentence, advisory lists.

## Steps

### 0. [partial: (b) done] Land PR #98

**Why.** Everything else builds on it; CI is red for reasons that look like infra and a known flake, not a regression, but that is unproven.

**What.** (a) Re-run locally `decide` and `rejected-option` with `--repeat 4`; record the numbers here. (b) Teach `evals/providers/kilo-runner.sh` and `evals/providers/summary_lib.py` to print `=== HARNESS ERROR: kilo start-up collision ===` for `Failed query: CREATE TABLE workspace` / `Unexpected error` with exit 1, so the PR summary labels it infra (unit test in `evals/providers/test_summary_lib.py`). (c) Merge #98 if `capture` and `decide` are at least 3/4 and `rejected-option`'s control test passes; set `rejected-option`'s advisory status per its measured stability (advisory under 3/4). (d) Remove the worktree and delete the branch.

**Done when.** #98 is merged; the three local numbers are in the Progress log; the runner labels the sqlite collision as infra with a unit test; `.claude/worktrees/adoption-review` is gone.

### 1. [partial: eval written, not yet graded] Make the headline claim measurable

**Why.** The README promises an agent stops re-proposing rejected options. Until `rejected-option` (`evals/rejected-option/`) is stable on the CI model there is no number behind it.

**What.** Get `rejected-option` to at least 3/4 on both tests with `--repeat 4`. If the Redis test fails because the agent never queries, tighten the fixture's AGENTS.md block or the case prompt (not the skills) first; only then consider a skill change. Add a second planted case (a rejected option phrased differently, for example "put a read-through cache on listOrders") so one phrasing cannot carry the result. Put the measured rate into the README as a sentence with date and model, once it is stable.

**Done when.** Two flagged cases and one control each pass 3 of 4 runs on the CI model, recorded in the Progress log; the README states the rate with date and model; `evals/advisory-cases.txt` and the two workflow `fromJSON` lists match the measured stability (unit-tested).

### 2. [partial: seeding asks and quickstart steers lighter; no real lite mode] Cut the first-run cost

**Why.** The cold starts took about 25 tool calls, 7 to 10 questions, and produced mostly stubs (draft decisions that restate commit messages, a docs manifest for a one-README repo, five meta-guardrails with `governed-by: TBD`, `tags.md` carrying the meta-tags `knowledge-management` and `guardrail`).

**Decision needed (owner):** a "lite" first run as a defined mode. Recommendation: `quickstart` runs `bootstrap` steps 1, 2, 9, 10 and 11 only (history stubs, AGENTS.md block, INDEX files, checker), skips seeding, manifest, fitness functions, domain proposals and tag vocabulary, and writes `kms-declined:` for the five seeded ids so check 12 stays quiet; `bootstrap` run by name keeps the full path; advisory lint, no pins. Alternative: keep one path and rely on the ask. Record the choice as a decision (supersedes or amends the seeding decision 0027 and 0072; `capture`'s Admission applies).

**What.** After the decision: implement in `quickstart/SKILL.md` and `bootstrap/SKILL.md` (net words must not grow; compress elsewhere), keep the meta-tags out of a new project's `tags.md`, make history stubs that only restate a commit message fail admission, update both `examples.md`, extend the `bootstrap` eval or add a `quickstart` eval case that asserts the lite file set.

**Done when.** The decision is active with `accepted-by`; a cold `quickstart` on a scratch repo (repeat step 3's test) writes at most one decision, `AGENTS.md`, four `INDEX.md` files and nothing seeded without a yes, in 15 tool calls or fewer, and the checker prints nothing.

### 3. [partial: fixes made, not re-verified cold] Remove sharp edges that make first runs fail

**Why.** Both cold starts hit: checker not reachable (now vendored into bootstrap, capture, decide, conform and run at the end), INDEX format contradicted the checker (literal row added), a confirmed decision left `draft` (now `active` with `accepted-by`), "ask once" in bootstrap against "one question per turn" in decide (bootstrap batches asks at the end; decide asks one at a time; unchanged, documented only by the order of steps), a `docs/` that is already a Sphinx tree (not handled), and unclear status for a decision whose reason sits only in a commit message (admission "carried" is hard to apply to history).

**What.** Re-run the cold-start test on three unfamiliar repos (one Python, one JS, one with an existing `docs/`) with fresh agents and the brief used on 2026-11-22: follow `quickstart` literally, simulate the human, report friction (the brief is in this plan's Why; clone into an empty scratch directory, never into the kms repo, never commit there). Fix what recurs; resolve the three leftovers above in the skill text.

**Done when.** The three runs finish with the checker silent on first try and no step the agent reports as ambiguous more than once across runs; the report summary is pasted into the Progress log.

### 4. [partial: glossary done; closing summaries done; rename decision (c) open, owner] Fix the vocabulary

**Why.** "skill" means an agent skill and a procedure; the directory `docs/skills/` holds procedures; guardrail, fitness function, derivation, umbrella tag, admission gate and registry were unexplained to a first-time reader.

**What.** (a) A glossary in the README under "Words you will see", at most 10 entries of one line each (and none of this repo's decision numbers). (b) Every skill's closing summary uses the plain-word form (`quickstart` does; check `bootstrap`, `capture`, `lint`, `conform`, `onboard`). (c) Decide the `docs/skills/` to `docs/procedures/` rename: deferred in decision 2.5 of the archived review plan with trigger "a second adopting project asks"; the cold-start reports are two such signals, so **decision needed (owner)**. Recommendation: do it in the same release as `migrate.py` support (detect both names for one release, rewrite on migrate), because every later adopter makes it costlier.

**Done when.** The README glossary exists; the grep `grep -rn "fact/decision/guardrail/skill" plugins README.md AGENTS.md docs/skills` returns nothing; the rename decision is recorded either way.

### 5. [pending] Make the automation real outside Claude Code

**Why.** The only automation is two `SessionStart` hooks, Claude Code only. The README now says so, but a team on Codex or Kilo, or one that never runs a skill, has no trigger.

**What.** Ship (1) a git `pre-commit` recipe and (2) a GitHub Actions job (`docs/skills/` procedure plus a copy-paste workflow under `plugins/kms/templates/ci/` or documented in `INSTALLING.md`) that run `python3 lint_check.py --root . --strict` and, for pull requests, `conform`'s structural docs pass. Keep it opt-in; `bootstrap` mentions it in its close, does not install it. Must not need a model: the deterministic checker only.

**Decision needed (owner):** whether a shipped CI template is in scope (adds a file class under `templates/`; amends decision 0027 and the uninstall inventory). Alternative: documentation only, no shipped file.

**Done when.** A scratch repo with the recipe fails a commit that breaks a pin and passes a clean one (recorded in the Progress log with commands); `uninstall` knows about any shipped file; INSTALLING.md names it per agent.

### 6. [partial: illustrative README example only] Show, don't tell

**Why.** The README's before/after is invented ("illustrative"). A real run is stronger and is also the proof for step 1.

**What.** Use the output of step 1's `rejected-option` run, or a real small repo with the owner's permission, to write a real before/after (agent proposes the rejected option without `kms`; is stopped with a citation with it). Commit the transcript excerpt under `docs/` or the README, with date, model and agent. Add a sample `docs/` tree link (the `evals/rejected-option/fixture` is a candidate; it passes `lint_check.py --strict` apart from check 12). Outward-facing if published elsewhere (blog, release notes): owner's call.

**Done when.** The README example is replaced by a captured one with date and model; the fixture or sample tree is linked from the README; owner has seen it.

### 7. [pending] Release the lot

**What.** After steps 0 to 3 at least: bump all manifests and `index.json` together, add the CHANGELOG entry (what changed for adopters: the checker beside the skills that write, the confirmed-decision status, seeding asks first, the lite first run if step 2 is done, the new eval), tag, GitHub Release. Owner tags and publishes.

**Done when.** Same checks as the 0.18.1 release: three manifests agree, the CHANGELOG entry exists, tag and Release exist, `lint_check.py --strict` exits 0.

## Not in this plan

- Becoming a delivery framework (go-getter's scope).
- Schema changes: the review's recommendation 7 is a statement of intent, not work: keep schema `1.0.0` stable and say so in the README when step 4's glossary lands.
- Retrieval or vector search (the thesis is a vocabulary).
- Scale testing at hundreds of artifacts: worth a separate step once step 1's number exists; trigger: an adopter with more than 100 artifacts.
