---
id: improvement-harness-eval-gate
title: Skill-rewrite fixes must pass the eval gate
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "guardrail", "verification", "eval"]
governed-by: 0068-improvement-harness-verification
grounded-in: ["0043-eval-harness-for-shipped-skill-changes"]
derivation-note: Given decision 0068 (three-layer verification) and decision 0043 (eval harness exists for shipped skills), the eval gate is mandatory for skill-rewrite improvements.
---

## Guardrail

Any improvement fix that modifies a `SKILL.md` file (skill-rewrite type) must pass the eval harness verification before auto-commit. The fix is accepted only if: (1) the skill's eval pass rate improves or stays the same, (2) no new eval failures are introduced, (3) the eval score improvement meets the configurable threshold (default 5%) for auto-commit eligibility.

## Derivation

Given:
- Decision `0068`: Three-layer verification includes an eval gate for skill-rewrite
- Decision `0043`: The eval harness (Kilo + promptfoo) tests shipped skill bodies against fixtures

Therefore: The eval gate is mandatory for skill-rewrite because it provides the only objective, automated measure of whether a skill rewrite preserves or improves the skill's actual behavior.

## Enforcement

- The orchestrator runs the relevant eval case(s) via `promptfoo` (or `kilo-runner.sh`) after a skill-rewrite fix.
- If eval fails or regresses, the fix is rejected and the subagent is re-invoked with the eval output as feedback (max 3 retries per `0061`).
- For auto-commit, the score improvement must exceed the threshold; otherwise the fix is staged for human review.
- CI verification gate re-runs evals on all skill-modifying auto-commits.
