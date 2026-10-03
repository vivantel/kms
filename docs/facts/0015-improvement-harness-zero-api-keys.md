---
id: 0015-improvement-harness-zero-api-keys
title: Improvement harness must work with zero API keys (free models only)
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "constraint", "kilo", "free-tier"]
kind: environmental
governed-by: 0058-improvement-harness-execution-model
---

## Fact

The improvement harness must operate entirely on free model tiers with no API keys required. This is a hard constraint inherited from the project's philosophy and the eval harness precedent (`0012-kilo-gateway-free-tier-access`).

The harness achieves this by:
- Using OpenCode's built-in model access (which provides free tier models)
- Not requiring any external API credentials (OpenRouter, Anthropic, OpenAI, etc.)
- Running in environments where only OpenCode is installed (CI, local dev)

## Source

Direct constraint from stakeholder requirements (interview decision). Confirmed by the eval harness (`0043`) which uses Kilo's free gateway successfully.

## Implications

- No secrets management needed for the harness.
- CI runs need only `opencode` installed, no credential setup.
- Model quality is limited to free tiers; the harness must be prompt-efficient (token economy `0026`).
- If free tier models degrade, the harness degrades gracefully (more escalations, fewer auto-commits).
