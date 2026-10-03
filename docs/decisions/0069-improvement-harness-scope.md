---
id: 0069-improvement-harness-scope
title: Improvement harness scans the whole repository each run
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "scope", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

Each improvement run (scheduled or event-driven) shall perform a whole-repository scan of the knowledge base (`docs/{facts,decisions,guardrails,skills}/`, `plugins/kms/skills/`, `plugins/kms/shared/`) rather than limiting to changed files.

- Scheduled runs: full scan of all artifact types.
- Event-driven runs: full scan, but the unified queue (`0062`) prioritizes items related to changed files and their dependents. The scan still discovers cross-cutting issues (e.g., a decision change that invalidates a guardrail in an unrelated file).
- The scan runs `lint`, `capture` (drift detection), and eval harness (for skills) in parallel to populate the queue.

## Rationale

- The knowledge base is highly interconnected: decisions → facts → guardrails → skills. A change anywhere can ripple everywhere.
- Changed-file-only scanning misses:
  - Stale facts that haven't been touched but are now contradicted by a new decision
  - Guardrails that need re-derivation because a grounding fact changed
  - Cross-references that drifted in files not directly modified
- The repo is small enough (hundreds of files, not millions) that a full scan is fast (~30-60s for lint + capture + evals).
- The event-driven prioritization still provides fast feedback for the most likely issues.

## Consequences

- The orchestrator must run `lint`, `capture`, and eval discovery in parallel for speed.
- The unified queue (`0062`) must handle deduplication when the same issue is discovered by multiple scanners.
- Resource usage is higher than changed-only; CI runners need adequate memory/CPU.
- The `max_files_per_run` config (`0063`) provides a safety cap if the repo grows.
