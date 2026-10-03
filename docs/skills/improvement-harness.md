# Improvement Harness Procedure

Knowledge-base procedure for operating the automated KMS improvement harness.

## Overview

The improvement harness is an autonomous system that continuously improves the KMS plugin's own knowledge artifacts (skills, facts, decisions, guardrails) and shipped skills. It runs on a schedule, on events, or on demand.

## Components

| Component | Path | Purpose |
|-----------|------|---------|
| Config | `.opencode/improvement.yaml` | Central configuration |
| Runner | `plugins/kms/hooks/improvement-runner.sh` | Shell orchestrator |
| Orchestrator | `.opencode/agent/improve/improve-harness.md` | Main agent |
| Lint Fix | `.opencode/agent/improve/improve-lint-fix.md` | Subagent for mechanical fixes |
| Skill Rewrite | `.opencode/agent/improve/improve-skill-rewrite.md` | Subagent for skill improvements |
| CI Workflow | `.github/workflows/improvement-harness.yml` | Scheduled/event-driven execution |
| Log | `docs/improvement-log.md` | Structured run history |

## Configuration Reference

### `.opencode/improvement.yaml`

```yaml
version: 1

baseline_ref: "latest-tag"  # Git ref for worktree base (tag/commit/SHA)

triggers:
  scheduled:
    enabled: true
    cron: "0 2 * * *"  # Daily 02:00 UTC
  event_driven:
    enabled: false  # v0.2+
    paths:
      - "plugins/kms/skills/**"
      - "docs/**"
      - "plugins/kms/shared/**"
  manual:
    enabled: true

improvement_types:
  - name: lint-fix
    subagent: improve-lint-fix
    auto_commit: true
    verification: [lint_gate]
  - name: skill-rewrite
    subagent: improve-skill-rewrite
    auto_commit: false
    verification: [lint_gate, eval_gate]

loop_prevention:
  max_passes_per_type: 3
  convergence_threshold: 0.01  # 1% marginal improvement
  semantic_hash_algorithm: "markdown-ast"

verification:
  lint_gate:
    enabled: true
    require_clean: true
  eval_gate:
    enabled: true
    min_score_improvement: 0.05  # 5%
  sampling:
    enabled: true
    sample_rate: 0.2

observability:
  log_file: "docs/improvement-log.md"
  commit_attribution:
    name: "kms-improvement-bot"
    email: "kms-improvement@vivantel.dev"
  ci_gate: true

safety:
  kill_switch: false
  max_files_per_run: 50
  excluded_paths: []
```

## Running the Harness

### Manual Run

```bash
# Full run (lint-fix + skill-rewrite)
bash plugins/kms/hooks/improvement-runner.sh manual

# Dry run (no commits, no merge)
DRY_RUN=true bash plugins/kms/hooks/improvement-runner.sh manual

# With specific changed files (event mode)
bash plugins/kms/hooks/improvement-runner.sh event "plugins/kms/skills/lint/SKILL.md"
```

### Scheduled Run

Automatic via GitHub Actions cron (daily 02:00 UTC). Configured in `.github/workflows/improvement-harness.yml`.

### Event-Driven Run

Automatic on push to master (when `event_driven.enabled: true` in config). Currently disabled (v0.2+).

## Verification Gates

### Lint Gate (All Types)

Runs `lint` skill on all modified files. Requires zero violations.

```bash
opencode run --agent lint "lint <file>" --print-logs
```

### Eval Gate (Skill-Rewrite Only)

Runs promptfoo eval for the specific skill. Requires:
- `pass_rate >= baseline` (no regression)
- `score improvement >= 5%` (threshold configurable)

```bash
promptfoo eval -c evals/<skill>/promptfooconfig.yaml -o json
```

### Sampling Gate (v0.2+)

Random sample of changes for human review. Currently a placeholder.

## Convergence Loop

For each improvement type (priority order: lint-fix → skill-rewrite):

```
passes = 0
while passes < max_passes:
  items = queue.filter(type)
  if items.empty: break
  
  for item in items:
    result = invoke_subagent(type, item)
    verified = verify(result, type)  # Three-layer gate
    if verified:
      commit_or_stage(result, type)
    else:
      escalate(item, result)
  
  if converged(type): break
  passes += 1
  re-discover queue
```

**Convergence criteria:**
- Semantic hash (markdown AST) unchanged from previous pass
- Marginal improvement < 1% over 2 consecutive passes
- Max 3 passes per type (configurable)

## Log Format

Each run appends a structured entry to `docs/improvement-log.md`:

```markdown
---
date: 2026-01-15T10:30:00Z
mode: scheduled
run_number: 42
baseline_ref: "0.15.0"
baseline_sha: "abc123"
queue_depth: 15
processed: 12
committed: 10
escalated: 2
skipped: 1
lint_violations_before: 25
lint_violations_after: 5
eval_scores:
  bootstrap: {before: 0.72, after: 0.89}
  roadmap: {before: 0.68, after: 0.68}
escalated_items:
  - file: plugins/kms/skills/roadmap/SKILL.md
    reason: eval regression
    details: pass_rate dropped from 0.85 to 0.78
---
```

## CI Verification Gate

Runs after harness commits on push/schedule. Verifies:

1. **Commit format**: Conventional Commits + `Refs:` trailers
2. **File scope**: Only expected paths modified
3. **Lint gate**: Full repo lint passes
4. **Eval gate**: Skill-rewrite commits pass eval

Fails with GitHub Actions annotations on any anomaly.

## Safety Features

| Feature | Config | Behavior |
|---------|--------|----------|
| Kill switch | `safety.kill_switch` | Immediate exit if true |
| Max files | `safety.max_files_per_run` | Abort if queue exceeds limit |
| Excluded paths | `safety.excluded_paths` | Never process listed paths |
| Dry run | `DRY_RUN=true` | No commits, no merge |
| Worktree cleanup | `trap` in runner | Auto-remove on exit |

## Troubleshooting

### Harness Didn't Run

1. Check GitHub Actions workflow status
2. Verify `baseline_ref` resolves to a commit
3. Check `safety.kill_switch` is false

### Commits Not Merged

1. Check worktree fast-forward failed (diverged history)
2. Manual merge needed: `git merge improvement-harness-<timestamp>`

### Lint Gate Failing

1. Run lint manually: `opencode run --agent lint "lint the knowledge base"`
2. Fix violations before next run

### Eval Gate Failing

1. Check promptfoo eval output for specific skill
2. Compare against baseline pass rate/score
3. Skill-rewrite changes staged for review

### Model 503 Errors

The free model (`opencode/nemotron-3-ultra-free`) has intermittent availability. Retry or switch model in agent config.

## Related Artifacts

- `docs/plans/improvement-harness.md` — Implementation plan
- `.opencode/improvement.yaml` — Runtime configuration
- `docs/improvement-log.md` — Run history
- `plugins/kms/skills/improvement-harness/SKILL.md` — Skill interface
- `plugins/kms/skills/improvement-harness/examples.md` — Usage examples