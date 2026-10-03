---
id: 0068-improvement-harness-verification
title: Improvement harness uses three-layer verification (lint gate + eval gate + sampling)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "verification", "testing", "process"]
track: process
accepted-by: sergemso
---

## Decision

Every improvement fix must pass a three-layer verification gate before commit:

1. **Lint gate (mandatory for all types)**: Run the `lint` skill on the modified files. The fix is accepted only if:
   - No new lint violations introduced
   - Existing violations in the modified files are reduced (or unchanged for non-lint-fix types)
   - The `lint` skill exits with code 0

2. **Eval gate (mandatory for skill-rewrite)**: For any `SKILL.md` modification, run the eval harness (`0043`) for that specific skill. The fix is accepted only if:
   - The skill's eval pass rate improves or stays the same
   - No new eval failures introduced
   - Minimum score improvement threshold (configurable, default 5%) for auto-commit eligibility

3. **Sampling gate (for subjective KB repairs)**: For `kb-repair` and `guardrail-update` types where eval doesn't apply:
   - A configurable sample (default 20%) of changes are flagged for human review
   - The sample is stratified by file type and change magnitude
   - Non-sampled changes auto-commit if they pass the lint gate
   - Sampled changes are staged and logged in the improvement log for review

## Rationale

- Lint gate catches mechanical regressions (token economy, formatting, cross-references) universally.
- Eval gate catches semantic regressions in skill behavior — the only objective measure of skill quality.
- Sampling gate acknowledges that KB repairs (contradiction resolution, fact updates) are inherently subjective and can't be fully automated.
- Layered means a fix failing any gate is rejected/escalated; no single gate is a silver bullet.
- Configurable thresholds allow tuning as the harness matures.

## Consequences

- The orchestrator must invoke `lint` and the eval harness (`kilo-runner.sh` or `promptfoo`) programmatically.
- Eval gate adds significant latency (each skill eval takes ~30-60s); the orchestrator should run evals in parallel where possible.
- Sampling requires a deterministic selection algorithm (e.g., hash of file path + change hash) for reproducibility.
- The improvement log (`0064`) records which gate each fix passed/failed.
- CI verification (`0064`) re-runs all three gates on auto-commits as a final safety net.
