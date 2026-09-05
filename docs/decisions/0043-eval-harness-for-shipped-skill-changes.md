---
id: 0043-eval-harness-for-shipped-skill-changes
title: Adopt Kilo+OpenRouter+promptfoo as the eval harness comparing shipped skill-body changes
status: active
date: 2026-09-04
tags: [kms, eval-harness, kilo, openrouter, github-models]
track: process
governed-facts: [0009-kilo-code-cli-headless-execution, 0010-openrouter-free-tier-terms, 0011-github-models-free-tier-terms]
fitness-functions: ["Once implemented, run the initial 5-case suite against the current (pre-change) skill bodies and confirm every case passes, establishing a clean baseline before any skill-body change is ever compared against it."]
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
