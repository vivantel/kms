---
id: 0043-eval-harness-for-shipped-skill-changes
title: Adopt Kilo+OpenRouter+promptfoo as the eval harness comparing shipped skill-body changes
status: active
date: 2026-09-04
tags: [kms, eval-harness, kilo, openrouter, github-models]
track: process
governed-facts: [0009-kilo-code-cli-headless-execution, 0012-kilo-gateway-free-tier-access]
fitness-functions: ["Resolved: docs/plans/archive/eval-harness-baseline-reliability.md and docs/plans/archive/eval-harness-for-skill-changes.md's own step 7 established and recorded the accepted baseline via many real CI runs — capture, attribute, lint, and bootstrap reliably pass; roadmap is an accepted, narrow, known flake on the discrete-options mechanic specifically. Originally declared here as: 'Once implemented, run the initial 5-case suite against the current (pre-change) skill bodies and confirm every case passes, establishing a clean baseline before any skill-body change is ever compared against it.'"]
---

## Decision

- **Harness**: Kilo Code CLI (`kilo run --auto`), executing the identical `SKILL.md` content `kms` ships — not a Claude-specific reimplementation or reinterpretation of it.
- **Runner model backend**: OpenRouter's free (`:free`) tier, configured via `kilo.jsonc`.
- **Orchestrator**: `promptfoo` — the first npm dependency and `package.json` this repo will carry.
- **Judge model**: GitHub Models, accessed via the ambient `GITHUB_TOKEN` in CI — a quota independent of OpenRouter's, requiring no secret of its own.
- **Initial case scope**: 5 skills — `bootstrap`, `roadmap`, `capture`, `lint`, `attribute`. The first four were the most heavily revised this session; `attribute` is deliberately untouched, serving as a control case that should show zero regression, validating the harness itself rather than any actual change.
- **Case layout**: centralized `evals/` at the repo root, matching `promptfoo`'s own convention.

This resolves the `fitness-functions` debt logged on `docs/decisions/0040-lint-contradiction-and-staleness-checks.md`.

## Why

`kms`'s own skill bodies are already committed to being agent-neutral (`docs/decisions/archive/0006-agent-agnostic-scope.md`, `docs/decisions/0011-kms-domain-agnostic-beyond-software.md`, enforced by `docs/guardrails/agent-agnostic-skill-content.md`). Running the eval suite through Kilo rather than Claude isn't a workaround forced by cost alone — it's a legitimate first-class target that also exercises the "any agent can run these skills identically" claim directly, something a Claude-only harness never would.

`0040`'s fitness-functions entry deferred adopting an eval harness at all because doing so meant bootstrapping CI, a dependency, secrets, and an adapter all at once — an infrastructure decision on its own, not a rider on a taxonomy/lifecycle-field revision. Revisiting it now, free-tier over a paid model removes an additional objection that would otherwise apply on top of that: running comparisons on a paid model compounds cost with every trial, which a repo that had zero CI or dependencies until this same initiative shouldn't take on by default. Free-tier models make the running cost genuinely zero, at an honest tradeoff: weaker models follow nuanced, multi-step instructions less reliably than Claude/GPT-5-class models, so per-trial fidelity is noisier. The 5-case scope is chosen to surface that tradeoff rather than hide it — `lint`'s checks are mechanically gradable (deterministic assertions), while `capture`/`roadmap` require real judgment calls (llm-graded), so the suite's own results will show whether free-tier fidelity is actually sufficient for the judgment-heavy cases, rather than assuming it either way going in.

`promptfoo` over a bespoke harness: reuses a maintained assertion/grading framework (regex, `file_exists`, an `llm`-judge grader with built-in multi-run variance-averaging) and a GitHub Action that already performs before/after PR comparison natively — exactly this problem's shape — rather than reimplementing that logic by hand, the standard failure mode of an ad hoc test harness accreting complexity as more cases get added over time.

A separate judge model (GitHub Models) rather than reusing the OpenRouter runner model avoids two problems at once: self-grading bias (a model judging its own class of mistakes, especially paired with a similarly-capable model doing the judging, shares the same blind spots), and quota contention (running and judging would otherwise compete for the same 200-request/day OpenRouter cap).

## Tradeoffs considered

- **Claude or another paid model as runner**: highest per-trial fidelity, but reopens the exact ongoing-cost objection that shelved this initiative the first time it came up.
- **Same free OpenRouter model for both running and judging**: simplest, fully free, but carries real self-grading-bias risk and no independent quota headroom.
- **NVIDIA NIM instead of OpenRouter for running**: also genuinely free (forever-free as of Aug 2026), but its actually-free models skew general-purpose — Nemotron's stronger coding-oriented models sit behind paid partner endpoints, not NIM's own free tier — a weaker fit for agentic instruction-following than OpenRouter's coding-focused free models.
- **A bespoke bash/python harness instead of `promptfoo`**: zero new dependency, but reimplements variance-averaging, structured reporting, and the before/after diff mechanic that `promptfoo` already provides and maintains.
- **Colocated `evals/` per skill**, matching `examples.md`'s placement convention: more consistent with `kms`'s existing colocation habit, but needs `promptfoo --eval-dir` overrides or a wrapper script to aggregate 5 scattered directories — more moving parts than a first suite this size warrants.
- **Chosen**: Kilo+OpenRouter running, GitHub Models judging, `promptfoo` orchestrating, 5 cases, centralized `evals/`.

## Amendment (implementation-time, 2026-09-05)

Executing this decision surfaced four deviations from what's written above. The decision's
substance (Kilo+OpenRouter running, `promptfoo` orchestrating, 5 centralized cases) stands;
these are corrections to implementation details this decision got wrong or left unverified,
recorded here rather than silently reconciled, per this decision's own re-verification caveats.

- **Judge model**: GitHub Models was fully retired 2026-07-30 (confirmed against
  `docs.github.com/en/github-models`'s own retirement notice) — it is not a temporary outage,
  and `docs/facts/0011-github-models-free-tier-terms.md` is stale. Rather than fall back to
  self-grading on the same OpenRouter model doing the running (the literal runner-up this
  decision's tradeoffs section named), the judge uses a *second*, distinct free OpenRouter model
  (`z-ai/glm-5.2:free`, a large-context reasoning model, vs. the runner's
  `poolside/laguna-s-2.1:free`, a dedicated coding-agent model) — preserving this decision's
  anti-self-grading-bias intent without a working GitHub Models to depend on.
- **Runner model**: `docs/facts/0010-openrouter-free-tier-terms.md`'s named example
  (Qwen3 Coder) has rotated off OpenRouter's free tier entirely, confirming that fact's own
  "expected to change" caveat. `poolside/laguna-s-2.1:free` — explicitly marketed by Poolside as
  a coding-agent model, scored on Terminal-Bench — is the current equivalent.
- **Case layout**: "matching `promptfoo`'s own convention" turned out to mean one self-contained
  `evals/<case>/promptfooconfig.yaml` per case (providers/prompts/tests/assert inline, per
  `promptfoo`'s real schema), not the `prompt.md` + `graders/*.md` directory shape with
  `type: regex/tool_used/tool_order/file_exists/llm/baseline` frontmatter this decision
  speculated — that shape does not exist in `promptfoo`; it appears to have been conflated with
  a different, Claude-Code-specific plugin-eval format. `evals/<case>/` still centralizes one
  directory per case, plus an optional fixture/ and setup.sh, matching this decision's intent.
- **Provider config location**: Kilo's project-scope `kilo.jsonc`/`.kilo/kilo.jsonc` (any config
  file discovered by walking up from cwd) categorically rejects `${env:...}`-style credential
  interpolation — a deliberate guard against a checked-in, shared config exfiltrating arbitrary
  env vars. This repo's own committed `kilo.jsonc` is therefore left untouched (`skills.urls`
  only, per `docs/decisions/0035-native-kilo-code-support.md`); the OpenRouter provider is
  supplied per-invocation via the `KILO_CONFIG_CONTENT` env var instead (see
  `evals/providers/kilo-runner.sh`), which Kilo treats as trusted, operator-supplied
  configuration rather than project configuration.

## Amendment (implementation-time, 2026-09-10)

The 2026-09-05 amendment above patched OpenRouter access around GitHub Models' retirement.
Further testing found something better, superseding OpenRouter entirely rather than just its
judge role: **Kilo Code CLI has its own built-in gateway serving `:free`-suffixed models with
no account, no `kilo auth login`, and no API key at all** — confirmed by testing (`hasToken=false`
on the `kilo` provider, a real completion returned regardless) — see
`docs/facts/0012-kilo-gateway-free-tier-access.md`.

- **Runner**: `kilo run --auto -m kilo/poolside/laguna-s-2.1:free "..."` — same model as the
  09-05 amendment chose, just addressed through Kilo's own gateway instead of a separately
  registered OpenRouter provider. No `KILO_CONFIG_CONTENT`, no custom `provider` block, no
  `OPENROUTER_API_KEY` anywhere — the 09-05 amendment's "provider config location" workaround is
  now moot, not just relocated.
- **Judge**: `kilo/nvidia/nemotron-3-ultra-550b-a55b:free` (a large, general-reasoning model,
  distinct from the runner's coding-agent model) via a second, minimal exec provider
  (`evals/providers/kilo-judge.sh`) that promptfoo's `llm-rubric` assertions point at directly —
  confirmed on a rubric-shaped grading prompt to return clean, parseable output rather than
  reaching for tools (`kilo/z-ai/glm-5.2:free`, the 09-05 amendment's judge pick, doesn't exist in
  Kilo's own gateway catalog, which curates a different subset than OpenRouter's raw catalog —
  confirmed by testing, not assumed).
- **Net effect**: `docs/decisions/0044-eval-harness-ci-safety-gates.md`'s CI workflow needs no
  secret at all now — `OPENROUTER_API_KEY` is gone from every job, and the CI-secret step in
  `docs/plans/eval-harness-for-skill-changes.md` (step 6) is moot. `@kilocode/cli` (the npm
  package backing the `kilo` binary) is installed globally as a CI/local prerequisite instead.
- `docs/facts/0010-openrouter-free-tier-terms.md` and `docs/facts/0011-github-models-free-tier-terms.md`
  are marked `deprecated` — accurate records of paths tried and abandoned, not deleted.

## Amendment (implementation-time, 2026-09-10)

Without a `PROMPTFOO_API_KEY`, `promptfoo-action`'s own PR comment falls back to plain text
("» View eval results in CI console «", not a link) instead of a real link to the eval's
results — confirmed by reading the action's own source. Fixing that requires promptfoo's
hosted "share" feature, which needs a `promptfoo.dev` account: **knowingly reopening the
external-account dependency the runner/judge choices above spent two amendments removing**, for
this one, narrower benefit. Chosen anyway, by direct request, weighing that this account
requirement is scoped to the *judge/reporting* side only (still free tier; still no cost) and
produces genuinely private links ("visible only to you and your organization" per promptfoo's
own docs — not a public leak of eval content), unlike the OpenRouter/GitHub Models
dependencies removed earlier for cost/reliability reasons specific to the *runner*.
`PROMPTFOO_API_KEY` is now a CI secret; see `docs/decisions/0044-...`'s matching amendment.
