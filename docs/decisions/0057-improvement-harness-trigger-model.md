---
id: 0057-improvement-harness-trigger-model
title: Improvement harness uses a hybrid trigger model (scheduled + event-driven)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "automation", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall use a hybrid trigger model:

- **Scheduled (baseline)**: A daily cron job (via GitHub Actions) runs a full repo scan and improvement cycle. This catches drift, staleness, and contradictions that accumulate silently.
- **Event-driven (critical paths)**: On push/PR to `plugins/kms/skills/**`, `docs/**`, or `plugins/kms/shared/**`, a targeted improvement cycle runs only on changed files and their direct dependents. This catches regressions immediately.
- **Manual invocation**: Developers can run `opencode agent improve` (or a wrapper script) on demand.

## Rationale

- Pure scheduled misses the "fast feedback" loop — a skill change that breaks something should be caught before it lands or immediately after.
- Pure event-driven misses cross-file issues (a decision change that invalidates a guardrail in another file) and silent drift (no commits touching a stale fact for weeks).
- The existing nudge hooks (`capture-nudge.sh`, `lint-nudge.sh`) already use heuristic triggers; the improvement harness formalizes and extends this.
- CI integration for event-driven runs uses the same `kilo-runner.sh` pattern as the eval harness (`0043`), but with the improvement harness's own entry point.

## Consequences

- Two distinct entry points: `improvement-runner.sh --mode=scheduled` and `improvement-runner.sh --mode=event --changed-files=...`
- The event-driven mode must compute the transitive closure of dependents (via cross-references in frontmatter and prose).
- Scheduled runs need a longer timeout and higher resource allocation (full repo scan).
