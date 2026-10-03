---
id: 0056-improvement-harness-scope
title: Improvement harness covers lint auto-fix, skill rewrites, and knowledge base repairs
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

The incremental automatic KMS improvement harness shall address all three improvement dimensions from day one:

1. **Lint auto-fix** — mechanical fixes for token-economy, verbosity, drift, and other guardrail violations detected by the `lint` skill
2. **Skill body rewrites** — substantive rewrites of `SKILL.md` files for clarity, structure, examples, and effectiveness
3. **Knowledge base repairs** — fixing contradictions, stale facts, missing derivations, cross-reference drift, and gaps detected by `lint`/`capture`/`query`

A fourth dimension, **guardrail derivation updates** (re-deriving guardrails when source decisions/facts change), is included as a natural consequence of KB repairs.

## Rationale

- These dimensions are interdependent: a skill rewrite may introduce lint violations; a KB repair may require a guardrail re-derivation; a lint fix may reveal a deeper skill clarity issue.
- Building a generic framework that can dispatch any "improvement skill" (as an opencode subagent) makes adding dimensions trivial — the MVP just registers three.
- Deferring any dimension creates technical debt: the harness architecture must accommodate it later anyway, and the signal sources (lint, evals, capture) already exist for all three.
- The eval harness (`0043`) already tests shipped skills; the improvement harness closes the loop by fixing what evals/lint/capture find.

## Consequences

- The harness must orchestrate multiple improvement skill types, each with different verification strategies (lint gate for mechanical, eval gate for skill rewrites, sampling for subjective KB repairs).
- Loop prevention (`0061`) is critical because all three dimensions can trigger each other.
- The unified discovery queue (`0062`) must prioritize across heterogeneous signals.
