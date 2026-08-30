---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/skill knowledge system — dangling references, missing required fields, numbering collisions, expired decisions, redundant guardrails, and audit-log-style facts — independent of what changed this session. Use when the user wants the whole knowledge base checked for health, e.g. "lint the knowledge base", "check the whole docs/ tree for problems".
---

Scan every fact, decision, guardrail, and skill prescription in the project — not just what changed recently — and report every structural violation found. Complements `steward`'s per-session checks with a full, on-demand sweep; `steward` can't catch rot that predates the session it happens to run in.

## What to check

1. **Dangling references** — any `governed-by` or `grounded-in` value pointing at a decision/fact id that doesn't exist.
2. **Missing required fields** — facts without `kind`/`governed-by`; guardrails without `governed-by`/`grounded-in`/`derivation-note`; decisions without `track`.
3. **Numbering collisions or gaps** — duplicate or skipped numbers in `facts/`/`decisions/`.
4. **Expired decisions** — a decision with an `expires` field whose date has passed or condition has plausibly been met, still standing without re-evaluation.
5. **Redundant guardrails** — a guardrail only ever true "whenever skill X does Y," with no claim broader than that skill's own procedure.
6. **Audit-log facts** — a fact that only records a timestamped event, grounds nothing, and is referenced by nothing.
7. **Orphaned artifacts** — a fact or guardrail nothing references at all.
8. **Unenforced guardrails** — a guardrail describing behavior a shipped skill should perform, where that skill's own body doesn't actually say it.

## Output

Group findings by check, one line per violation with the file path and what's wrong. Never silently fix anything — propose the fix and wait for confirmation, the same way every other skill in this plugin defers to the user before writing.

## Out of scope

Fixing anything without confirmation, and judgment calls about domain-specific correctness beyond structural validity (e.g. whether a decision's rationale is actually convincing) — that's what `clarify`/`roadmap`'s interview is for, not a mechanical scan.
