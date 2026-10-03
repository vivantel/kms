---
name: improvement-harness
description: Run the automated KMS improvement harness — executes lint-fix and skill-rewrite passes with convergence loop, verification gates, and structured logging. Use when you want to trigger a full improvement cycle, e.g. "run the improvement harness", "auto-fix lint violations", "improve skill bodies".
---

Run the improvement harness to automatically fix mechanical lint violations and rewrite skill bodies for clarity and effectiveness.

## When to use

- "run the improvement harness" — full automated improvement cycle
- "auto-fix lint violations" — lint-fix pass only
- "improve skill bodies" — skill-rewrite pass only
- "check if harness made any commits" — review recent auto-commits

## Workflow

The harness operates in a git worktree detached from `baseline_ref` (default: latest tag). It:

1. **Discovers** queue items from lint violations and eval failures
2. **Prioritizes** by severity, impact, confidence, age
3. **Runs convergence loop** per improvement type (lint-fix → skill-rewrite):
   - Up to 3 passes per type (configurable)
   - Re-discovers queue after each pass
   - Stops early if semantic hash converges (<1% marginal improvement)
4. **Verifies** each fix through three gates:
   - **Lint gate**: all fixes must pass `lint` on affected files
   - **Eval gate** (skill-rewrite): pass rate ≥ baseline AND score improvement ≥ 5%
   - **Sampling gate** (v0.2+): random sample for human review
5. **Commits** verified fixes with attribute-format messages + `Refs:` trailers
6. **Logs** run summary to `docs/improvement-log.md`
7. **Merges** worktree back to main (unless dry-run)

## Configuration

Controlled by `.opencode/improvement.yaml`:
- `baseline_ref`: tag/commit/SHA for worktree base
- `improvement_types`: lint-fix (auto-commit), skill-rewrite (human-gated)
- `loop_prevention`: max_passes, convergence_threshold, semantic_hash_algorithm
- `verification`: lint_gate, eval_gate, sampling settings
- `observability`: log_file, commit_attribution, ci_gate
- `safety`: kill_switch, max_files_per_run, excluded_paths

## Modes

- **scheduled**: Full repo scan (daily cron)
- **event**: Targeted scan on changed files (CI push/PR)
- **manual**: On-demand run

## Output

- Auto-commits for lint-fix (type: `fix:`) with `Refs:` to artifacts
- Staged changes for skill-rewrite requiring human review
- Structured log entry in `docs/improvement-log.md`
- CI verification gate on push

## Safety

- Kill switch via config (`safety.kill_switch: true`)
- Max files per run limit
- Dry-run mode for testing
- Worktree auto-cleanup on exit