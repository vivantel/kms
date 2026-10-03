---
id: 0064-improvement-harness-observability
title: Improvement harness provides multi-layer observability (commits, log, CI gate, dashboard)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "observability", "audit", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall provide observability through four complementary layers:

1. **Structured auto-commits** (via `attribute` skill): Every commit uses Conventional Commits format with a Why-body and `Refs:` trailers linking to the governing decisions/guardrails/facts that motivated the fix. Example:
   ```
   fix: tighten token economy in clarify skill

   The clarify skill body exceeded the token-economy guardrail by 18%.
   Removed redundant prose in the interview mechanics section.

   Refs: 0026-token-economy-guardrail, 0056-improvement-harness-scope
   ```

2. **Append-only improvement log** (`docs/improvement-log.md`): Each run appends a structured entry with timestamp, mode (scheduled/event/manual), queue depth, items processed, commits made, files changed, metrics (lint violations before/after, eval scores), and any escalations. Format:
   ```markdown
   ## 2026-10-03T02:00:00Z — scheduled — run #47

   Queue: 23 items (12 lint-fix, 5 skill-rewrite, 4 kb-repair, 2 guardrail-update)
   Processed: 18 | Committed: 15 | Escalated: 3 | Skipped (idempotent): 2

   Metrics:
   - Lint violations: 47 → 12 (-74%)
   - Eval pass rate: 0.82 → 0.91 (+11%)
   - Files modified: 14

   Escalated (require human review):
   - plugins/kms/skills/roadmap/SKILL.md: skill-rewrite confidence 0.68 < 0.75 threshold
   - docs/decisions/0043-eval-harness-for-shipped-skill-changes.md: kb-repair semantic diff 35%
   ```

3. **CI verification gate**: A GitHub Actions job runs after each improvement run (or on PR merge) that verifies:
   - Auto-commits only touch files under `docs/`, `plugins/kms/skills/`, `plugins/kms/shared/`
   - All modified files pass `lint` skill
   - No new eval regressions introduced
   - Commit messages follow the required format
   - Fails the workflow if anomalies detected (alerts via GitHub notification)

4. **Optional dashboard**: A static HTML report generated from the improvement log (via a simple script) showing trends over time: violation counts, eval scores, commit velocity, escalation rate. Hosted on GitHub Pages or served locally.

## Rationale

- Commits alone are hard to query for trends; the log provides a time-series view.
- CI gate catches harness bugs (e.g., a run that touches source code instead of docs).
- Dashboard makes the harness's value visible to stakeholders without digging through git history.
- All layers are append-only and immutable — the log is the source of truth.

## Consequences

- The orchestrator must generate the log entry atomically with the commits.
- The `attribute` skill must be invoked programmatically for each auto-commit (or its logic inlined).
- CI job needs read access to the improvement log format.
- Dashboard generation is a separate low-priority task; log format must be machine-parseable from day one.
