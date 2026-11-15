---
id: 0071-facts-carry-no-outgoing-edges
title: Facts carry no outgoing edges; plain facts become admissible
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

1. Facts carry no outgoing edges: `kind` and `governed-by` are removed from facts. Edges live on the consumers that already have them (`grounded-in` on guardrails, `governed-facts` on decisions); backlinks are computed (`lint_check.py --refs <id>`; `query` prints "cited by").
2. Facts gain optional `source: <url | path | command>` (where to re-observe) and `last-verified: <date>` (last confirmed against `source`; moves only on re-observation, never on another edit).
3. Admission gate 1: "carried" means recoverable by one grep of the fact's own `source` path or of one file the reader would find first. A fact that aggregates two or more sources or locates something not greppable (external system, vault path, dashboard, vendor limit) is admissible uncited; a mechanical repeat of one value in one file is not.
4. Check 7 for facts is bounded: a fact with neither `source` nor any citer is noise; one with a `source` is not. `fact-not-audit-log` is rewritten: a fact is noise when it records an event, not when it is unreferenced.
5. Sprawl guards: `bootstrap` step 2 writes location/aggregation facts only on request and with a stated cap; the stale-fact check (3.4) applies only to facts whose `source` is external (URL or command).

Facts are environmental or process facts: true of the world or the workflow, not a restatement of product behaviour. Behaviour that must hold is a guardrail; what the product should do is a spec and lives in OpenSpec (0069).

## Why

Today a fact must carry `governed-by` (else `TBD` = debt), must ground or plausibly ground a decision or guardrail, must be referenced (check 7) and must not be stated in code (gate 1). `ARCHITECTURE.md`'s own example "The service runs on port 8080" fails all four. `governed-by` means two things never separated: on a `kind: decision` fact the decision that fixes the value; on every live environmental fact an inverted arrow (fact 0003 is the basis for 0008 yet carries `governed-by: 0008`). `kind: decision` facts are inadmissible by construction under gate 1, and all seven live facts are environmental. `last-verified` is used by `capture` check 2, `bootstrap` step 3 and `capture/examples.md` but is not in the model.

## Tradeoffs considered

- **Keep `governed-by` optional**: cheaper, but keeps the inverted arrow.
- **Chosen: no outgoing edges, bounded orphan check, `source` plus `last-verified`.**

## Dispositions

0064 superseded by this decision (`kind` removed; its definitions are not disputed, 0065's gate 1 emptied the `decision` value). 0009 amended (fact fields). 0015 left active; its "one-time observation" sentence is reconciled in 2.6. Guardrail `fact-governance-fields` is re-derived in 2.10 to require `source` or a citer. `uninstall` category 4 and `bootstrap` steps 2 and 8 (`governed-by: TBD`) change in 2.9/2.10. Texts 2.9/2.10 will change: the model's Fact paragraph, Admission gate 1, `docs/guardrails/fact-governance-fields.md`, `docs/guardrails/fact-not-audit-log.md`, `bootstrap`/`uninstall`/`capture` fact steps.

Draft; accepting it (owner, plan phase I) means `status: active` and `accepted-by`. Plan: `kms-review-and-redesign.md` 2.1 and consolidation B2.
