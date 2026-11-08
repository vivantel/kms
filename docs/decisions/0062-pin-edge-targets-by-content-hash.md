---
id: 0062-pin-edge-targets-by-content-hash
title: Edges pin their targets by content hash in a parallel pinned map, compared by the checker
status: active
date: 2026-11-08
tags: [kms, knowledge-management, eval-harness]
track: process
---

## Decision

A fact or guardrail may carry `pinned: {<id>: <revision>}` next to `governed-by` and `grounded-in`, one entry per edge target. The revision is the first 12 hex digits of the SHA-256 of the target file with `governed-by`, `grounded-in`, `pinned` and `date` removed from its frontmatter and whitespace collapsed. `shared/lint_check.py` compares it (check 13, pinned edges only) and writes it (`--pin FILE`); nobody types a revision. `pinned` keys must be edge ids (check 2). Edges without a pin stay with the model.

## Why

Check 13 asked the model to notice that a source changed since a guardrail was derived, and nothing in the edge said what the source looked like then; step 3 measured recall 0.20 on it. A recorded revision turns the question into a comparison.

## Tradeoffs considered

- **Git commit SHA of the target**: breaks on squash merges and rebases, which the study branch flow uses, needs history at lint time, and counts commits that touched other lines.
- **Version field in the target**: relies on someone bumping it, so a missed bump is silent staleness, the failure this removes.
- **`id@hash` inside `grounded-in`**: more compact, but changes every consumer of the field (checks 1, 2, 7, 9, templates, fixtures).
- **Chosen: content hash, parallel map.** Edge fields and `date` are left out of the hash so re-pinning one file does not make everything pointing at it stale. Cosmetic edits to the body still change the hash, so a pin can over-report; the cost is a re-derive and re-pin. Pins are optional, so existing projects keep working and the check is only as strong as pin adoption. Check 13 stays labelled judgment (decision 0061): its pinned part is mechanical, the rest is not.
