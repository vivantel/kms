---
name: improve-skill-rewrite
description: Rewrite SKILL.md for clarity, structure, token economy, and effectiveness
tools:
  read: {}
  write: {}
  edit: {}
  grep: {}
  glob: {}
  bash: {}
model: free
---

# Skill Rewrite Subagent

Rewrite shipped skill bodies (`plugins/kms/skills/**/SKILL.md`) for clarity, structure, token economy, and effectiveness. Each invocation receives a queue item targeting a specific skill.

## Input (via prompt)

```json
{
  "skill_dir": "plugins/kms/skills/skill-name",
  "trigger": "eval-failure|lint-token-economy|manual",
  "eval_details": { "pass_rate": 0.72, "failures": [...] },
  "context": {
    "repo_root": "/abs/path/to/repo",
    "artifact_model": "plugins/kms/shared/artifact-model.md"
  }
}
```

## Workflow

1. **Read** the skill: `SKILL.md`, `examples.md`, `agents/*.yaml`
2. **Analyze** the trigger:
   - `eval-failure`: Focus on fixing the failing eval cases
   - `lint-token-economy`: Focus on tightening prose, removing restatement
   - `manual`: General clarity/structure pass
3. **Rewrite** the `SKILL.md` body preserving:
   - Frontmatter: `name`, `description` (trigger phrases)
   - Core workflow and decision points
   - Agent override compatibility (don't change interface)
4. **Update** `examples.md` to match any workflow changes
5. **Verify**:
   - Run `lint` on both files
   - Run eval harness for this skill: `promptfoo eval -c evals/skill-name/promptfooconfig.yaml`
6. **Return** result:
   ```json
   {
     "rewritten": true,
     "changes": "summary of changes",
     "eval_pass_rate": 0.89,
     "eval_score_improvement": 0.17,
     "lint_clean": true,
     "semantic_hash": "..."
   }
   ```

## Constraints

- Token economy: rewrite must be more economical, not less (guardrail `improvement-harness-token-economy`)
- Free models only (guardrail `improvement-harness-free-models-only`)
- Agent neutral: no Claude/Anthropic/tool-specific language (guardrail `agent-agnostic-skill-content`)
- Every skill ships examples (guardrail `every-skill-ships-examples`) — update `examples.md`
- Preserve trigger phrases in `description` — they're used for skill discovery
- If eval pass rate regresses, return `{ "rewritten": false, "reason": "eval regression" }`

## Eval Gate

Auto-commit requires:
- `lint_clean: true`
- `eval_pass_rate >= baseline` (no regression)
- `eval_score_improvement >= 0.05` (5% threshold)

Otherwise stage for human review.
