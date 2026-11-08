---
id: 0065-admission-test-for-new-records
title: New records pass an admission test of hard gates and three estimated signals
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-08
tags: [kms, knowledge-management, taxonomy]
track: process
---

## Decision

The artifact model gains an Admission section. A change becomes a fact, decision, guardrail or procedure only if it passes three hard gates (not already carried elsewhere, right shape, recurrence for guardrails) and its estimated shelf life times recurrence clearly exceeds its rediscovery cost. A change that fails is not recorded; the agent says which gate failed in one line. `capture` check 1 applies it before drafting a decision stub; `roadmap` applies it to every intent and lists failures under "Not recorded". This changes the state at tag `study-v1` (b517c52), where `capture` drafted a stub for any new decision and `roadmap` saved intents that failed its three-way test as a "lighter artifact". The lighter tier is removed. `bootstrap` applies it to every finding before writing a stub; `quickstart` inherits it through `roadmap` and says so.

## Why

At `study-v1` nothing decided what was worth recording. Model-classifier runs over hand-labelled candidate changes (mean of samples, 66 development cases unless noted):

| Rule | Precision | Recall |
|---|---|---|
| `study-v1` behaviour (47 cases, 1 sample) | 0.81 | not scored |
| Static cut, reworded gate | 0.92 | 0.85 |
| Dynamic signals | 0.96 | 0.93 |
| Dynamic signals, reworded gate (adopted, before the recurrence sentence) | 0.96 | 0.95 |
| Shipped text, run on the branch (5 samples, 330 judgments) | 1.00 | 0.95 |

The `study-v1` behaviour recorded 5 of 26 non-record cases (named-person pointers, a `.gitignore` line as a guardrail, trivial renames as "lighter" records). On the shipped text, no group but `significant` had a record/none error; the single-incident guardrail (c73) was rejected in every sample, so the recurrence sentence worked on its first test. The always-record control fails the trivial group and the never-record control has recall 0, so the scorer can fail a degenerate rule.

## Tradeoffs considered

- **Static cut (fixed counts of reversal cost, affected parties, alternatives):** auditable, but it recorded a generic "write tests" guardrail in 5 of 5 runs and under-recorded a real model choice (recall 0.82).
- **Three tiers (none, lighter, full):** the lighter tier fired on almost every real record because few state a verification path; the gold set cannot score it. Not adopted.
- **Chosen: gates plus estimated signals.** The signals are estimates by the same model that applies them, so on the development set they add little over fixed gates beyond catching generic advice and one rationale case; the held-out check is the only unseen test.
- **Known misses:** a single-incident prohibition (c73) was recorded by every rule before the recurrence gate; on the shipped text it is rejected 5 of 5. Two real kms decisions are contested: label lint checks (c26) is rejected in 4 of 5 samples, pin by content hash (c10) is recorded in 4 of 5. Of 7 record/none errors in 330 judgments, all are in the `significant` group (c10 1, c14 2, c26 4).

## Limits

Model classifiers (sonnet subagents, one family), labels by one author, 66 development cases. The CI model (nemotron) and the kilo skill-loading path were not run on `evals/admission` (kilo is not installed where the samples were taken). The sealed held-out set has not been run.
