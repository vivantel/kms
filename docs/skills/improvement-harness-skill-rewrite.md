---
id: improvement-harness-skill-rewrite
title: Skill rewrite improvement skill
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "skill-rewrite", "procedural"]
operationalizes: ["improvement-harness-eval-gate", "improvement-harness-lint-gate", "token-economy", "every-skill-ships-examples", "agent-agnostic-skill-content"]
---

# Skill Rewrite Improvement Skill

Rewrites `SKILL.md` bodies for clarity, structure, token economy, and effectiveness. This is a substantive improvement type requiring eval verification.

## Scope

Improves these aspects of shipped skills (`plugins/kms/skills/**/SKILL.md`):
- **Clarity**: ambiguous instructions, unclear decision points, missing context
- **Structure**: logical flow, section organization, heading hierarchy
- **Token economy**: verbose prose, restatement, redundant examples in body
- **Completeness**: missing trigger phrases, incomplete workflows, edge cases
- **Examples**: updates `examples.md` to match rewritten skill body
- **Agent neutrality**: removes any agent-specific language (`0002`)

## What It Does Not Fix

- Mechanical lint violations (handled by `lint-fix` — runs first in priority order)
- New skill creation (human-only)
- Skill deletion/archival (human-only)

## Algorithm

For each queued skill-rewrite item (from eval failures or lint token-economy violations):
1. Read the current `SKILL.md`, its `examples.md`, and the eval failure details (if any)
2. Read the skill's agent overrides (`agents/*.yaml`) to preserve compatibility
3. Rewrite the skill body preserving: name, description, trigger phrases, core workflow
4. Update `examples.md` to reflect any workflow changes
5. Run eval harness on the skill to verify behavior preserved/improved
6. Run `lint` on both files
7. If both pass and eval score improvement ≥ 5%, auto-commit; otherwise stage for review

## Verification

- Lint gate (mandatory)
- Eval gate (mandatory): skill's eval pass rate must not regress; ≥5% improvement for auto-commit
- No sampling gate (eval is objective)

## Commit Message Format

```
refactor: rewrite <skill-name> skill for clarity and token economy

<Why: specific improvements made, referencing eval/lint findings>

Refs: 0056-improvement-harness-scope, 0043-eval-harness-for-shipped-skill-changes
```

## Configuration

```yaml
- name: skill-rewrite
  subagent: improve-skill-rewrite
  auto_commit: false  # requires high confidence
  verification: [lint_gate, eval_gate]
```
