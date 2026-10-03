---
id: improvement-harness-subagent-structure
title: Improvement skills must be implemented as OpenCode subagents
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "guardrail", "subagents", "opencode"]
governed-by: 0065-improvement-harness-skill-structure
grounded-in: ["0058-improvement-harness-execution-model"]
derivation-note: Given decision 0058 (OpenCode recursive execution) and decision 0065 (subagent structure), improvement skills must be OpenCode subagents.
---

## Guardrail

All improvement skills (lint-fix, skill-rewrite, kb-repair, guardrail-update, and any future types) must be implemented as OpenCode subagents (`.md` files under `.opencode/agent/improve/`). No improvement skill shall be implemented as a KMS skill (`plugins/kms/skills/**/SKILL.md`), a promptfoo case, a plain prompt template, or any other format.

## Derivation

Given:
- Decision `0058`: The harness executes via OpenCode recursively
- Decision `0065`: Improvement skills are OpenCode subagents

Therefore: The subagent format is the required implementation vehicle. It provides native tool access, structured I/O, error handling, and versioning — all essential for the harness's multi-step, tool-using workflows.

## Enforcement

- The orchestrator only discovers and invokes subagents from `.opencode/agent/improve/`.
- The `lint` skill checks that no improvement logic exists in `plugins/kms/skills/` (except the harness's own skill interface).
- New improvement types must add a subagent file and register it in `.opencode/improvement.yaml`.
