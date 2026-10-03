---
id: 0016-improvement-harness-token-economy
title: Improvement harness must respect the token-economy guardrail
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "constraint", "token-economy", "guardrail"]
kind: environmental
governed-by: 0026-token-economy-guardrail
---

## Fact

The improvement harness's own prompts, subagent instructions, and generated content must comply with the `token-economy` guardrail (`0026`): "Every fact, guardrail, and procedure must be maximally economical."

This applies to:
- Subagent instruction files (`.opencode/agent/improve/*.md`)
- Orchestrator script prompts and inline documentation
- Skill interface (`plugins/kms/skills/improvement-harness/SKILL.md`)
- KB procedure (`docs/skills/improvement-harness.md`)
- Auto-generated commit messages and improvement log entries

## Source

Direct constraint from stakeholder requirements (interview decision). The `token-economy` guardrail is a governed rule in this repo's KB.

## Implications

- Subagent instructions must be concise — no verbose preambles, examples in instructions, or redundant explanations.
- The harness should prefer structured data (YAML/JSON) over prose for machine-readable context.
- Commit messages and log entries must be terse but complete (Conventional Commits format achieves this).
- The `lint` skill will check the harness's own artifacts for token economy violations — dogfooding in action.
