---
id: 0065-admission-test-for-new-records
title: New records pass an admission test of hard gates and three estimated signals
status: draft
date: 2026-11-08
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

The artifact model gains an Admission section. A change becomes a fact, decision, guardrail or procedure only if it passes three hard gates (not already carried elsewhere, right shape, recurrence for guardrails) and its estimated shelf life times recurrence clearly exceeds its rediscovery cost. A change that fails is not recorded; the agent says which gate failed in one line. `capture` check 1 applies it before drafting a decision stub; `roadmap` applies it to every intent and lists failures under "Not recorded". This changes the state at tag `study-v1` (b517c52), where `capture` drafted a stub for any new decision and `roadmap` saved intents that failed its three-way test as a "lighter artifact". The lighter tier is removed. `bootstrap` and `quickstart` are not changed here.

## Why

At `study-v1` nothing decided what was worth recording. In a model-classifier run over 47 hand-labelled candidate changes, the `study-v1` behaviour recorded 5 of 26 non-record cases (named-person pointers, a `.gitignore` line as a guardrail, trivial renames as "lighter" records). The adopted rule recorded none of the original 26, and recalled 0.93 to 0.95 of the 21 true records over 66 cases (five samples). Details in the author's repo, `docs/plans/knowledge-boundary/round-2.md` and `round-3.md`.

## Tradeoffs considered

- **Static cut (fixed counts of reversal cost, affected parties, alternatives):** auditable, but it recorded a generic "write tests" guardrail in 5 of 5 runs and under-recorded a real model choice (recall 0.82).
- **Three tiers (none, lighter, full):** the lighter tier fired on almost every real record because few state a verification path; the gold set cannot score it. Not adopted.
- **Chosen: gates plus estimated signals.** The signals are estimates by the same model that applies them, so on the development set they add little over fixed gates beyond catching generic advice and one rationale case; the held-out check is the only unseen test.
- **Known misses:** a single-incident prohibition (c73) was recorded by every rule before the recurrence gate was added; the gate is untested. Two real kms decisions (pin by content hash, label lint checks) are still rejected in most runs because the lint code is read as carrying them; kept as contested.

## Limits

Model classifiers, one family, labels by one author, 66 development cases. The sealed held-out set has not been run.
