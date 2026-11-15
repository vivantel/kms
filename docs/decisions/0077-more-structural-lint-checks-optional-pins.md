---
id: 0077-more-structural-lint-checks-optional-pins
title: Make four more lint checks structural; keep pins optional
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, eval-harness]
---

## Decision

With 0073's fields: check 4 on `expires:` dates is structural (`expires-when` stays judgment); check 17 on `TBD`/`draft` with file `date` is structural; check 24 is structural once the step-legend format is fixed (`### N. [done|pending|blocked...]`); check 18 is structural on `fitness-functions[].last-verified` (0074). One threshold, stated once in the model: 180 days, overridable by one line in the AGENTS.md block.

Pins stay optional (0062 stands): an unpinned edge yields one advisory line ("unpinned: run `--pin`"); `bootstrap` and `capture` pin when the checker is available. `PIN_IGNORED` widens to `accepted-by`, `last-verified`, `status`, `superseded-by`, `expires`, `expires-when` (pins track content, not lifecycle). Checks 14, 22 and 23 are deferred until their registries carry dates. Checks 5, 6, 8, 10, 11, 16 stay judgment and the lint output labels them "advisory" (that word only; no recall numbers in user output). Relabel per 0061's rule and record a second-rater pass on the relabelled texts.

Final split: structural 1, 2, 3, 4, 7, 9, 12, 13 (pinned), 15, 17, 18, 19, 20, 21, 24; judgment 5, 6, 8, 10, 11, 13 (unpinned), 14, 16, 22, 23; 3.4 later adds structural check 25.

## Why

`evals/lint-matrix/results-2026-11-08.md`: judgment recall 0.00 on checks 5, 6, 8, 10, 11, 14, 24; 0.20 on 13, 16, 18; 0.40 on 17, 22, 23; precision 0.20 on 23; 0.20 false-alarm rate on a clean corpus. Pinned edges moved check 13 from 0.20 recall to 1.00 with no false alarms. Mandatory pins would make Python plus PyYAML a precondition for authoring a guardrail, against decision 0011's git-plus-Markdown substrate.

## Tradeoffs considered

- **Mandatory pins**: rejected, see Why.
- **Chosen: move date-based checks into the script, keep pins optional.**

## Dispositions

0062 amended (`PIN_IGNORED`). 0061 amended (new labels). 0058 amended (checks 4, 17, 18, 24 join the script). 0040 and 0047 left active. Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.7.
