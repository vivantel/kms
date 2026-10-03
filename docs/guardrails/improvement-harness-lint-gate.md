---
id: improvement-harness-lint-gate
title: All improvement fixes must pass the lint gate
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "guardrail", "verification", "lint"]
governed-by: 0068-improvement-harness-verification
grounded-in: ["0016-lint-skill"]
derivation-note: Given decision 0068 (three-layer verification) and decision 0016 (lint skill exists), the lint gate is a mandatory verification layer for all improvement types.
---

## Guardrail

Every improvement fix (lint-fix, skill-rewrite, kb-repair, guardrail-update) must pass the `lint` skill verification before commit. The fix is accepted only if: (1) no new lint violations are introduced in modified files, (2) existing violations in modified files are reduced or unchanged, (3) the `lint` skill exits with code 0.

## Derivation

Given:
- Decision `0068`: Three-layer verification (lint gate + eval gate + sampling)
- Decision `0016`: The `lint` skill exists and validates the whole knowledge base

Therefore: The lint gate is a mandatory, universal verification layer. It applies to all improvement types because lint violations (token economy, cross-references, structure) are universal concerns.

## Enforcement

- The orchestrator runs `lint` on modified files after each fix, before commit.
- If lint fails, the fix is rejected, the subagent is re-invoked with the lint output as feedback (max 3 retries per `0061`).
- CI verification gate re-runs lint on all auto-commits as a final check.
