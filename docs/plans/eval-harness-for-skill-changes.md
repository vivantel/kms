---
id: eval-harness-for-skill-changes
title: Build the Kilo+OpenRouter+promptfoo eval harness for comparing shipped skill-body changes, wired into CI with fork/comment safety gates
status: pending
date: 2026-09-04
tags: [kms, eval-harness, taxonomy, refactor]
---

# Build the Kilo+OpenRouter+promptfoo eval harness for comparing shipped skill-body changes, wired into CI with fork/comment safety gates

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`,
**public** GitHub repository) is a Claude Code / Codex / Kilo Code CLI
plugin marketplace, one plugin (`kms`) at `plugins/kms/`. See `AGENTS.md`
at the repo root for full structure and conventions before making any
change not covered by this plan.

This plan implements two decisions produced by a `roadmap` interview
about closing the `fitness-functions` debt logged on
`docs/decisions/0040-lint-contradiction-and-staleness-checks.md`
("adopt a reproducible eval harness... declared debt, no implementation
yet"):

- `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md` — the
  harness architecture: Kilo Code CLI (`kilo run --auto`) runs each
  case against OpenRouter's free tier; `promptfoo` orchestrates cases
  and grading; GitHub Models (via ambient `GITHUB_TOKEN`, no secret)
  judges llm-graded assertions; 5 initial cases (`bootstrap`, `roadmap`,
  `capture`, `lint`, `attribute`); cases live in a centralized `evals/`
  at the repo root.
- `docs/decisions/0044-eval-harness-ci-safety-gates.md` — CI wiring: a
  GitHub Actions workflow triggered on `pull_request` (never
  `pull_request_target`) targeting `master`, path-filtered to
  `plugins/kms/skills/**` and `plugins/kms/shared/**`, skipped entirely
  for fork-originated PRs, running once on PR-open and re-run on demand
  via an `/eval` PR comment gated on the commenter's `author_association`
  being `OWNER`/`MEMBER`/`COLLABORATOR`.

Supporting facts already written: `docs/facts/0009-kilo-code-cli-headless-execution.md`,
`docs/facts/0010-openrouter-free-tier-terms.md`,
`docs/facts/0011-github-models-free-tier-terms.md` — each carries a
"not confirmed with high confidence" caveat about exact syntax or
figures that may have drifted since 2026-09-04. **Re-verify each one
against the named tool/service's own current docs before writing the
file that depends on it** — this plan deliberately does not hardcode
volatile flag syntax or model names for that reason.

`AGENTS.md` and `CONTRIBUTING.md` already carry a forward-looking
sentence ("a change to `plugins/kms/skills/**` ... should pass the eval
suite ... once it exists") — this plan is what makes "once it exists"
true. `CONTRIBUTING.md`'s line "There's no build step and no test
suite" is still accurate until this plan executes; step 8 below updates
it once it no longer is.

**Nothing below has been executed yet.** Writing the decisions/facts
and this plan was `roadmap`'s deliverable; running this plan is a
separate, later action, per that skill's own hard limit ("never execute
the changeset plan yourself").

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Add `package.json` and `.gitignore` — status: pending

This repo has never had either file — first Node dependency of any
kind.

**1a.** Create `package.json` at the repo root: `name` (e.g.
`"vivantel-kms"`), `"private": true` (never published to npm — this is
a plugin marketplace, not an npm package), `"devDependencies": {
"promptfoo": "<latest>" }` — check npm for the actual current version
string rather than guessing one. Add an npm script,
`"eval": "promptfoo eval"`.

**1b.** Create `.gitignore` at the repo root with at minimum
`node_modules/` and promptfoo's own output directory (check
`docs/facts` for the confirmed default — likely `evals/results/` or a
`.promptfoo/` cache dir; verify against promptfoo's current docs, don't
guess).

Done when: `npm install` succeeds from a clean clone; `git status`
shows no `node_modules/` files as untracked-but-not-ignored.

### 2. Configure Kilo to run against OpenRouter's free tier — status: pending

**2a.** Verify `docs/facts/0009-...`'s and `0010-...`'s "not confirmed"
caveats against Kilo's and OpenRouter's own current docs: the exact
`kilo.jsonc` fields for pointing a provider/model at OpenRouter, and
which specific `:free` model to target (the roster rotates — pick a
currently-live, coding-capable one, e.g. checking for something in the
Qwen3 Coder family or equivalent at execution time).

**2b.** Add a provider entry to this repo's root `kilo.jsonc` (already
exists, currently only configures `skills.urls` per
`docs/decisions/0035-native-kilo-code-support.md`) for the eval
harness's own use — do not remove or alter the existing `skills.urls`
entry; add alongside it. The API key is read from an environment
variable (e.g. `OPENROUTER_API_KEY`), never hardcoded into the file.

Done when: running `kilo run --auto "<a trivial test prompt>"` locally,
with `OPENROUTER_API_KEY` set in the environment, completes and
produces output attributable to the configured OpenRouter model (check
Kilo's own verbose/debug output for the model id used).

### 3. Write the 5 eval cases under `evals/` — status: pending

Centralized layout per `docs/decisions/0043-...`: `evals/<case-name>/prompt.md`
plus `evals/<case-name>/graders/*.md`, matching `promptfoo`'s own
convention (verify current exact schema against `promptfoo`'s docs — a
prior investigation this session found frontmatter fields like `name`,
`tags`, `plugins`, `runs`, `max_turns`, `timeout_seconds`,
`allowed_tools`, `model`, on `prompt.md`, and grader files with a
`type:` field of `regex`/`tool_used`/`tool_order`/`file_exists`/`llm`/`baseline`
— re-confirm these are still current before writing, since this is an
early-access, evolving feature).

Provider: every case's `prompt.md` (or a shared `promptfoo` config)
points at a custom exec-type provider — a wrapper script (e.g.
`evals/providers/kilo-runner.sh`) that: (1) creates a fresh scratch
working directory, (2) copies in whatever fixture project state the
case needs (see per-case notes below), (3) runs
`kilo run --auto "<the case's actual invocation prompt>"` inside that
directory, (4) prints a result promptfoo can capture (stdout, plus a
listing of files the run created/modified for `file_exists` graders to
check).

**3a. `evals/bootstrap/`** — fixture: an empty or near-empty project
(no `docs/{facts,decisions,guardrails,skills}/` yet). Invocation
prompt: something a user would say to trigger `bootstrap` (see
`plugins/kms/skills/bootstrap/examples.md` for realistic phrasing).
Graders: `file_exists` for the expected directory structure being
created; an `llm` grader judging whether the produced decision/fact
stubs are reasonable given the fixture's (synthetic) git history.

**3b. `evals/roadmap/`** — fixture: a project with an existing
`docs/{facts,decisions,guardrails,skills}/` (e.g. a snapshot of this
repo's own `docs/` at a known commit, or a smaller synthetic one).
Invocation prompt: a realistic "capture this as a decision" trigger.
Graders: `tool_used`/`tool_order` if the harness can observe Kilo's
tool calls (verify this is exposable through the exec-provider output;
if not, fall back to `file_exists` + `llm` only); an `llm` grader
judging interview quality (one question at a time, recommendation
stated, etc. — `plugins/kms/skills/roadmap/SKILL.md`'s own interview
mechanics section is the rubric).

**3c. `evals/capture/`** — fixture: a project with a KB plus a
deliberately-planted contradiction (two facts/decisions that disagree).
Invocation prompt: "run the knowledge check." Graders: `llm` grader
checking the contradiction gets surfaced (check 4 in `capture`'s own
body: "Contradiction found? Block.").

**3d. `evals/lint/`** — fixture: a project with a KB containing several
deliberately-planted violations, one per check family (e.g. a dangling
`governed-by`, a decision missing `track`, a stale prose reference).
Graders: `regex` assertions that the output actually names each
planted violation — the most mechanically gradable case in the suite,
deliberately chosen as the anchor for validating deterministic grading
works before trusting the `llm`-graded cases.

**3e. `evals/attribute/`** — fixture: a project with a staged git diff
representing one clear, unambiguous change. Invocation prompt: "commit
this with attribution." Graders: `regex` on the resulting commit
message for the `Refs:` trailer format and a Conventional Commits type
prefix. **This is the control case** — since neither `attribute` nor
its fixture change between harness runs, a failure here means the
harness itself regressed, not the skill.

Done when: all 5 cases exist with the fields above; `npx promptfoo eval --case bootstrap`
(and similarly for each other case name) runs to completion locally
without a harness-level error (grading pass/fail is not the bar here —
completing a run is).

### 4. Configure the judge model (GitHub Models) — status: pending

**4a.** Re-verify `docs/facts/0011-...`'s "not confirmed" caveat: whether
`GITHUB_TOKEN`'s Models access in this specific repo is gated by a
Copilot subscription tier, and if so, which tier's rate limits actually
apply. If access turns out to be blocked or below what 5 cases' worth
of `llm` grading needs, fall back to the "strongest free OpenRouter
model" option `docs/decisions/0043-...`'s tradeoffs section names as
the runner-up, and note that substitution as an amendment to this
step — don't silently degrade to same-model self-grading without
recording why.

**4b.** Point every `llm`-type grader at the GitHub Models endpoint
(`https://models.github.ai/inference/chat/completions`, OpenAI-SDK
compatible) using `GITHUB_TOKEN` — configure this once, centrally
(promptfoo's own docs should have a "default provider for graders"
mechanism; verify current syntax rather than repeating it per-grader).

Done when: a local run with a valid `GITHUB_TOKEN` (e.g.
`gh auth token`) in the environment produces `llm`-graded scores, not
harness errors, for at least one case.

### 5. Write the GitHub Actions workflow — status: pending

Create `.github/workflows/eval-skills.yml` (this repo's first-ever
workflow file). Required elements, per `docs/decisions/0044-...`:

- `on: pull_request:` with `types: [opened]`, `branches: [master]`, and
  `paths: ["plugins/kms/skills/**", "plugins/kms/shared/**"]` —
  **never** `pull_request_target`. The `types: [opened]` restriction is
  required: without it, `pull_request` defaults to firing on `opened`,
  `synchronize` (every push), and `reopened`, silently re-running on
  every push and defeating `docs/decisions/0044-...`'s frequency limit.
- `on: issue_comment:` (PRs are issues in GitHub's model) for the
  `/eval` re-run trigger.
- A job-level `if:` guard on the `pull_request`-triggered job:
  `github.event.pull_request.head.repo.fork == false`.
- A job-level `if:` guard on the `issue_comment`-triggered job: the
  comment body matches `/eval` (exact or prefix match — decide at
  implementation time) **and**
  `contains(fromJSON('["OWNER","MEMBER","COLLABORATOR"]'), github.event.comment.author_association)`.
  This alone is not sufficient — `issue_comment` payloads carry no
  `head.repo.fork` field, so a legitimate collaborator commenting
  `/eval` on someone else's fork-originated PR would otherwise still
  trigger a run against that fork's content (`docs/decisions/0044-...`'s
  corrected text). Add an early step in this job that resolves fork
  status via the API before anything else runs, e.g.:
  ```
  - id: fork-check
    run: echo "is_fork=$(gh pr view ${{ github.event.issue.number }} --json isCrossRepository -q .isCrossRepository)" >> "$GITHUB_OUTPUT"
    env:
      GH_TOKEN: ${{ github.token }}
  ```
  (block-style `env:`, not a flow mapping — `{ GH_TOKEN: ${{ ... }} }`
  is invalid YAML, since the `${{ }}` braces collide with flow-mapping
  syntax; verified with `yaml.safe_load`.)
  (verify the exact `gh pr view` JSON field name against the current
  `gh` CLI docs — don't assume `isCrossRepository` is still correct at
  implementation time) — then gate every subsequent step in the job on
  `steps.fork-check.outputs.is_fork == 'false'`.
- `permissions:` block scoped minimally — `contents: read` plus
  whatever the chosen result-posting mechanism needs (likely
  `pull-requests: write` if posting a comment back, `models: read` for
  GitHub Models access — verify the exact permission name against
  GitHub's current Models-in-Actions docs).
- `env: OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}` — sourced
  from a repo secret (step 6), never inline.
- The `promptfoo` invocation itself: `npx promptfoo eval --max-cost-usd <N>`
  with a small defensive ceiling per `docs/decisions/0044-...`'s cost
  safety net, plus `--json` for machine-readable output if the job
  posts a summary back to the PR.

Done when: the workflow file is valid YAML (`python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" .github/workflows/eval-skills.yml`
exits 0) and a test PR from a same-repo branch (not a fork) touching
`plugins/kms/skills/lint/SKILL.md` triggers the job.

### 6. Add the `OPENROUTER_API_KEY` repo secret — status: pending

This step needs a human to actually provision the key value — an
executing agent should not invent or silently source an API key. Ask
whoever is running this plan to either supply an existing OpenRouter
key or create one (openrouter.ai account, no credit card needed for
`:free`-tier usage per `docs/facts/0010-...`), then set it:
`gh secret set OPENROUTER_API_KEY --repo vivantel/kms` (prompts for the
value on stdin), or via the GitHub web UI under Settings → Secrets and
variables → Actions.

Done when: `gh secret list --repo vivantel/kms` shows
`OPENROUTER_API_KEY` present (value itself is never visible, only the
name and last-updated date).

### 7. Run the baseline and confirm the fitness-function — status: pending

Per `docs/decisions/0043-...`'s own `fitness-functions` entry: once
steps 1–5 are done, run the full 5-case suite locally
(`npx promptfoo eval`, using `OPENROUTER_API_KEY` from the local
environment set in step 2 — this doesn't need step 6's CI repo secret,
which only matters once the workflow itself runs) against the current,
unmodified skill bodies and confirm every case passes. Step 6 (the
secret) and step 8 (the `CONTRIBUTING.md` line) can happen before,
after, or in parallel with this step — neither blocks nor is blocked by
it. This establishes the clean baseline every
future comparison measures against — a suite that can't even pass
against its own starting point isn't ready to gate anything.

Done when: `npx promptfoo eval --json baseline.json` exits 0 (all cases
at or above threshold) and `baseline.json` is inspected by hand to
confirm the grader results look sane, not just that the exit code was
0 (an exit code alone can't distinguish "everything actually passed"
from "everything was silently skipped").

### 8. Update `CONTRIBUTING.md`'s now-stale claim — status: pending

Replace "There's no build step and no test suite, so contributing is
mostly about writing clear, well-scoped skill instructions and manifest
edits." with wording that acknowledges the eval suite now exists for
`plugins/kms/skills/**`/`plugins/kms/shared/**` changes specifically,
while keeping the rest of the sentence's point (no build step for the
JSON/Markdown content itself) intact.

Done when: the sentence no longer claims "no test suite" unconditionally.

## Explicitly out of scope for this plan

- **Extending the eval suite beyond the initial 5 cases** — `bootstrap`,
  `roadmap`, `capture`, `lint`, `attribute` only, per
  `docs/decisions/0043-...`. Adding the remaining 9 skills is a natural
  follow-up once this suite has a track record, not part of standing it
  up.
- **A trusted-fork allowlist** — considered and declined in
  `docs/decisions/0044-...`'s tradeoffs; revisit only if external
  contributions become a real pattern for this repo.
- **Posting eval results as an automated PR comment** — step 5 leaves
  the exact result-surfacing mechanism (comment vs. check-run summary
  vs. just the Actions log) to implementation time; `promptfoo-action`
  may already handle this natively, in which case a bespoke posting
  step is unnecessary — verify before building one.
- Committing or pushing — not requested; check `git status`/`git log`
  before assuming otherwise.
