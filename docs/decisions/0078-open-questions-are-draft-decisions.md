---
id: 0078-open-questions-are-draft-decisions
title: Open questions and hypotheses are draft decisions with expires-when
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
---

## Decision

No fifth governed type, no registry.

1. An open question or hypothesis is a decision in `status: draft` carrying `expires-when: <the test or event that closes it>` and the tag `question`. `uninstall` category 4 and lint check 17 exempt a draft that carries `expires-when` (a question, not an abandoned stub). Admission's "Typical rejections" says so.
2. Goals and open plans: each plan's own `status:` line is the record; check 24 reads it; no cross-plan file.
3. Experiment results stay in the decision that cites them, with raw data committed under `evals/` or named as not committed.
4. Risks and assumptions are rejections, with the pointer: "a risk that changes behaviour becomes a guardrail; an assumption a decision rests on becomes a fact with `source`".

## Why

Open questions (0053 refers to a "still-open question" living only in prose), hypotheses (0014's example `expires` condition is a hypothesis test with no record), goals (every plan is disposable per 0037), experiment results (0065's tables live in a decision body) and risks have no home, so agents invent shapes.

## Tradeoffs considered

- **A fifth artifact type for questions**: more surface for little recurring value.
- **Chosen: reuse `draft` plus `expires-when`.**

## Dispositions

0037 left active (reaffirmed). 0030 amended (uninstall category 4 exemption). Rejection sentences listed above go verbatim into `admission.md` (2.9). Draft; owner acceptance in plan phase I. Plan: `kms-review-and-redesign.md` 2.8.
