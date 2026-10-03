---
id: 0071-improvement-harness-mvp
title: Improvement harness MVP delivers framework + lint-fix + skill-rewrite
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "mvp", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

The MVP (v0.1) of the improvement harness shall deliver:

1. **Framework infrastructure**:
   - Orchestrator script (`plugins/kms/hooks/improvement-runner.sh`)
   - Configuration (`.opencode/improvement.yaml`)
   - Git worktree bootstrap (`0060`)
   - Unified queue with lint + eval signal adapters (`0062`)
   - Convergence loop with loop prevention (`0061`, `0066`)
   - Three-layer verification (`0068`)
   - Observability: structured commits + improvement log (`0064`)
   - CI verification gate

2. **Lint-fix improvement type** (subagent `improve-lint-fix`):
   - Fixes token-economy violations (verbose prose, restatement, length)
   - Fixes formatting/structure violations (missing frontmatter fields, INDEX.md sync)
   - Fixes cross-reference drift (broken links, stale decision IDs)
   - Auto-commits on lint gate pass

3. **Skill-rewrite improvement type** (subagent `improve-skill-rewrite`):
   - Rewrites `SKILL.md` bodies for clarity, structure, and token economy
   - Updates `examples.md` to match rewritten skill
   - Requires eval gate pass + high confidence for auto-commit; otherwise stages for review

The following are explicitly **deferred to v0.2+**:
- KB-repair improvement type (contradictions, stale facts, gaps)
- Guardrail-update improvement type (re-derivation on source change)
- Event-driven trigger integration with GitHub Actions
- Dashboard generation from improvement log
- Multi-project/layered configuration

## Rationale

- Lint-fix and skill-rewrite cover the highest-volume, highest-confidence improvements.
- Lint-fix is mechanical and verifiable; skill-rewrite has the eval harness as objective ground truth.
- KB-repair and guardrail-update require more nuanced judgment and better signal extraction from `capture`/`lint`.
- The framework must be solid before adding more improvement types — otherwise each type reinvents orchestration.
- MVP scope is achievable in 2-3 focused sessions; broader scope risks indefinite delay.

## Consequences

- The MVP config (`.opencode/improvement.yaml`) only registers `lint-fix` and `skill-rewite` types.
- The `kb-repair` and `guardrail-update` subagents don't exist yet; their queue items are logged but not processed.
- Event-driven runs in MVP only work for scheduled; push/PR integration comes in v0.2.
- The improvement log format must be designed for future extensibility (new types, new metrics).
