---
id: improvement-harness-free-models-only
title: Improvement harness must use free models only
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "guardrail", "free-tier"]
governed-by: 0058-improvement-harness-execution-model
grounded-in: ["0015-improvement-harness-zero-api-keys"]
derivation-note: Given decision 0058 (OpenCode execution) and fact 0015 (zero API keys), the harness must only use models available through OpenCode's free tier.
---

## Guardrail

The improvement harness shall only invoke models that are available through OpenCode's built-in free tier. No external API keys, paid tiers, or credentialed model access shall be used or configured.

## Derivation

Given:
- Decision `0058`: The harness executes via OpenCode recursively
- Fact `0015`: The harness must work with zero API keys (free only)

Therefore: The harness must only use models accessible through OpenCode's free tier. Any configuration, subagent, or code that references a paid model or requires an API key violates this guardrail.

## Enforcement

- The `lint` skill checks `.opencode/agent/improve/*.md` and `.opencode/improvement.yaml` for model references that imply paid access.
- CI verification gate (`0064`) fails if any subagent specifies a non-free model.
- The orchestrator validates model availability at startup.
