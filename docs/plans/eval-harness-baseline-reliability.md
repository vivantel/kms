---
id: eval-harness-baseline-reliability
title: Get the eval harness's real baseline from 3/5 to 5/5, or decide why it shouldn't be
status: pending
date: 2026-09-10
tags: [kms, eval-harness]
---

# Get the eval harness's real baseline from 3/5 to 5/5, or decide why it shouldn't be

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`,
**public** GitHub repository) ships an eval harness under `evals/` that runs
each of 5 cases (`bootstrap`, `roadmap`, `capture`, `lint`, `attribute`)
through Kilo Code CLI's own free gateway (no account, no API key — see
`docs/facts/0012-kilo-gateway-free-tier-access.md`), orchestrated by
`promptfoo`, wired into CI at `.github/workflows/eval-skills.yml`. Full
background: `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`
and `docs/decisions/0044-eval-harness-ci-safety-gates.md` (including both
files' `## Amendment` sections — read those, they record real corrections
made during execution, not just the original intent).

`docs/plans/eval-harness-for-skill-changes.md` (the harness's build-out
plan) is done; this plan picks up exactly where its step 7 left off. Its
own step 7 section has the first real baseline result recorded — read it
before starting here, don't re-derive it:

- **Passed for real**: `capture`, `roadmap`, `attribute` — actual Kilo runs
  through the free gateway, actual grading, no harness errors. These are
  not in scope for this plan; don't touch them without a reason found while
  working the steps below.
- **`bootstrap`**: times out at its `timeout_seconds: 480` ceiling
  (`evals/bootstrap/promptfooconfig.yaml`) without writing any files.
  Reproduced twice — once in a local sandbox run, once for real in CI
  (workflow run `34446496455`). The local run's transcript showed the
  model going down a research tangent on what "TOON format" (a term in
  `plugins/kms/shared/artifact-model.md`, referenced from
  `plugins/kms/skills/capture/SKILL.md` and others) means, rather than
  treating it as a simple inline CSV-like convention — fetching external
  web pages about it instead of proceeding.
- **`lint`**: completed within its timeout (`exit 0`) but failed its 3
  `regex` assertions (`evals/lint/promptfooconfig.yaml`). *Why* is not yet
  known — the CI log's printed transcript table truncates, and at the time
  this plan was written, no artifact retained the full output.

Since this plan was written, `docs/decisions/0043-...`'s amendment records
one relevant fix already merged: `.github/workflows/eval-skills.yml` now
uploads each case's full promptfoo output JSON as a build artifact
(`eval-results-<case>` / `eval-recheck-results-<case>`, `if: always()`, 14
day retention) — **step 1 below is likely already unblocked by the time
you read this; check for the artifact before assuming you need to add
upload logic yourself.**

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Read `lint`'s actual failure from the artifact — status: pending

Trigger a fresh `lint`-only run if no recent artifact exists (comment
`/eval` on any open PR against `master`, or open a trivial PR touching a
file under `plugins/kms/skills/**` to fire the `pull_request` path — see
`docs/decisions/0044-...`'s trigger conditions). Download the
`eval-results-lint` (or `eval-recheck-results-lint`) artifact via
`gh run download <run-id> -n eval-results-lint` and inspect the JSON's
`results[].response.output` (or equivalent field — check the actual shape,
promptfoo's exact JSON schema wasn't verified when this plan was written)
for the full, untruncated transcript `evals/providers/kilo-runner.sh`
printed.

Determine which of these actually happened:
- The model never named the specific violations (`0099-nonexistent-decision`,
  `0001-weekly-releases`, `track`, `require-two-approvals`) in its final
  output at all — a real model-competence gap.
- The model named them but phrased differently than the regexes expect
  (e.g. quoted differently, referred to the guardrail by a different
  name) — a grader-too-strict problem, fixable in
  `evals/lint/promptfooconfig.yaml` alone.
- The model ran out of turns/time before reaching a final summary — a
  timeout-adjacent problem like `bootstrap`'s.

Done when: the actual cause is known and written down (amend this step
with the finding before moving to step 2 — don't fix blindly).

### 2. Fix `lint` per what step 1 found — status: pending

- If it's a regex-too-strict problem: loosen the specific regex(es) in
  `evals/lint/promptfooconfig.yaml` to match what a correct answer
  actually looks like, without loosening past the point where a genuinely
  wrong answer could pass (the whole reason `lint` was chosen as this
  suite's mechanically-gradable anchor,
  `docs/decisions/0043-...`'s case-scope rationale).
- If it's a competence/timeout problem: fold it into step 3 below rather
  than fixing it in isolation — `bootstrap` and `lint` may share one root
  cause (see step 3's own note about this).

Done when: a fresh CI run (same trigger mechanism as step 1) shows `lint`
passing, or an explicit decision recorded here that it shouldn't (e.g. the
regexes were already correct and the model is genuinely not capable
enough — see step 4).

### 3. Decide `bootstrap`'s fix — status: pending

Options, roughly cheapest-to-most-invasive:

**3a. Raise `timeout_seconds` further** (currently 480 in
`evals/bootstrap/promptfooconfig.yaml`; the workflow's own
`timeout-minutes: 20` per job leaves headroom to go to ~1000s before
hitting that ceiling too). Cheapest test — try this first. Re-run per
step 1's trigger mechanism and check whether `bootstrap` completes with
more time, not just times out later.

**3b. Make `shared/artifact-model.md`'s "TOON format" mention
self-explanatory inline**, if research confirms the model's tangent is
specifically triggered by that unfamiliar term rather than the task's
overall scope. This would be a real, if small, product finding about
`kms`'s own skill-body clarity — not just an eval-harness tuning knob. If
pursued, treat it as its own small change to
`plugins/kms/shared/artifact-model.md` with a reason recorded (a
one-line inline clarification, e.g. spelling out that TOON is a compact
CSV-like tabular notation, not a name requiring lookup), separate from
this eval-harness plan, and note here which commit made it.

**3c. Try a different free model** for the runner (`poolside/laguna-s-2.1:free`
currently). `evals/providers/kilo-runner.sh`'s `model` config field
already supports overriding per-case without code changes — check
`kilo/nvidia/nemotron-3-ultra-550b-a55b:free` (the harness's own judge
model, already confirmed free/no-account/reliable for a rubric-shaped
completion) or another `:free` model from Kilo's gateway catalog
(`kilo models` lists them; cross-reference against
`docs/facts/0012-kilo-gateway-free-tier-access.md`'s caveat that this
catalog is a curated subset, not a 1:1 OpenRouter mirror) for one with
stronger multi-step planning, even if it's a general-reasoning model
rather than `laguna`'s coding-agent specialization.

**3d. Accept 480s-timeout as `bootstrap`'s honest result** and record
that a free, small coding-agent model genuinely can't complete this
specific task in this specific time — matching
`docs/decisions/0043-...`'s own stated tradeoff going in ("the suite's
own results will show whether free-tier fidelity is actually sufficient
for the judgment-heavy cases, rather than assuming it either way going
in"). This is a legitimate outcome, not a failure of this plan, if 3a–3c
are tried first and don't move the needle.

Done when: one of 3a/3b/3c is tried and either fixes `bootstrap`, or all
three are tried without success and 3d is explicitly chosen and recorded
here with why.

### 4. Record the final baseline state — status: pending

Once steps 1–3 settle (whether that means 5/5 passing, or fewer with an
explicit reason recorded), update
`docs/plans/eval-harness-for-skill-changes.md`'s step 7 status to reflect
the final outcome — that file's own step 7 is currently marked `partial`
pointing at the 3/5 result this plan started from; it should end up
`done` (if 5/5) or otherwise say plainly what the accepted baseline is and
why, so a future skill-body change being compared against it has an
honest reference point.

Done when: `docs/plans/eval-harness-for-skill-changes.md`'s step 7 no
longer says `partial`.

## Explicitly out of scope

- **Re-litigating the harness's architecture** (Kilo's free gateway,
  `promptfoo`, the 5-case scope) — settled by
  `docs/decisions/0043-...`/`0044-...` and their amendments; this plan is
  about getting the existing design's baseline to a settled state, not
  redesigning it.
- **Extending the suite beyond the initial 5 cases** — explicitly out of
  scope for the parent plan too; still not this plan's job.
- **Touching `capture`, `roadmap`, or `attribute`** unless a step above
  finds a genuine shared root cause — they already pass for real; don't
  destabilize them chasing `bootstrap`/`lint`.
