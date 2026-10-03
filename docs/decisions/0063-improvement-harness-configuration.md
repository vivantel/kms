---
id: 0063-improvement-harness-configuration
title: Improvement harness configuration lives at .opencode/improvement.yaml
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "configuration", "opencode", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness configuration shall live at `.opencode/improvement.yaml` (project level), following OpenCode's native config conventions. This is a single flat file (no layering in MVP); future versions may add user/global layers.

## Configuration Schema

```yaml
# .opencode/improvement.yaml
version: 1

# Baseline commit for worktree pinning (tag, branch, or commit SHA)
baseline_ref: "latest-tag"  # or "v1.2.3", "abc123"

# Trigger modes
triggers:
  scheduled:
    enabled: true
    cron: "0 2 * * *"  # daily at 2am UTC
  event_driven:
    enabled: true
    paths:
      - "plugins/kms/skills/**"
      - "docs/**"
      - "plugins/kms/shared/**"
  manual:
    enabled: true

# Improvement types (registered subagents)
improvement_types:
  - name: lint-fix
    subagent: improve-lint-fix
    auto_commit: true
    verification: [lint_gate]
  - name: skill-rewrite
    subagent: improve-skill-rewrite
    auto_commit: false  # requires high confidence
    verification: [lint_gate, eval_gate]
  - name: kb-repair
    subagent: improve-kb-repair
    auto_commit: false
    verification: [lint_gate, sampling]
  - name: guardrail-update
    subagent: improve-guardrail-update
    auto_commit: true
    verification: [lint_gate]

# Loop prevention
loop_prevention:
  max_passes_per_type: 3
  convergence_threshold: 0.01  # 1% marginal improvement
  semantic_hash_algorithm: "markdown-ast"

# Verification gates
verification:
  lint_gate:
    enabled: true
    require_clean: true
  eval_gate:
    enabled: true
    min_score_improvement: 0.05  # 5%
  sampling:
    enabled: true
    sample_rate: 0.2  # 20% of subjective changes

# Observability
observability:
  log_file: "docs/improvement-log.md"
  commit_attribution:
    name: "kms-improvement-bot"
    email: "kms-improvement@vivantel.dev"
  ci_gate: true

# Safety
safety:
  kill_switch: false
  max_files_per_run: 50
  excluded_paths: []
```

## Rationale

- `.opencode/` is the natural home for OpenCode-specific configuration (agents, plugins, permissions). Colocating keeps related config together.
- YAML is human-readable, supports comments, and is OpenCode's native format.
- Single file for MVP avoids premature complexity; layering can be added when multi-project or multi-user needs arise.
- All tunables are explicit — no hidden defaults that surprise users.

## Consequences

- The orchestrator (`improvement-runner.sh`) must parse this YAML (use `yq` or Python).
- Config changes take effect on next run; no restart needed.
- The config file itself can be improved by the harness (dogfooding `0070`).
