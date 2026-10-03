---
id: improvement-harness-token-economy
title: Improvement harness artifacts must comply with token economy
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "guardrail", "token-economy"]
governed-by: 0026-token-economy-guardrail
grounded-in: ["0016-improvement-harness-token-economy"]
derivation-note: Given the token-economy guardrail (0026) applies to all procedures, and fact 0016 confirms the harness is subject to it, all harness artifacts must be maximally economical.
---

## Guardrail

All improvement harness artifacts — subagent instructions, orchestrator prompts, skill interfaces, KB procedures, commit messages, and log entries — must be maximally economical: the shortest phrasing that preserves meaning, no restatement, no redundant examples in instructions.

## Derivation

Given:
- Guardrail `0026`: "Every fact, guardrail, and procedure must be maximally economical"
- Fact `0016`: The improvement harness's own artifacts are subject to the token-economy guardrail

Therefore: All harness artifacts must comply with token economy. This is a direct, unmediated consequence of the guardrail applying universally.

## Enforcement

- The `lint` skill validates harness artifacts (subagents, config, skill interface, KB procedure) for token economy violations.
- Subagent instructions are checked for: verbose preambles, in-instruction examples (use examples.md instead), redundant explanations, restatement.
- Commit messages and log entries are checked for: unnecessary words, restatement of diff content, verbose explanations.
- Violations are auto-fixed by the `lint-fix` improvement type (`0056`).
