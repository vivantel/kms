---
id: 0057-pin-eval-model-north-mini-code
title: Pin the eval harness to cohere/north-mini-code:free after laguna-s-2.1 was withdrawn
status: active
date: 2026-11-08
tags: [kms, eval-harness, kilo]
track: process
---

## Decision

Every eval case and the runner default use `cohere/north-mini-code:free` (run as `kilo/cohere/north-mini-code:free`) in place of `poolside/laguna-s-2.1:free`. The model stays pinned by name, so the choice is ours, not the gateway's.

## Why

On 2026-11-08 all five eval cases failed on unmodified `master` content with "Model not found: kilo/poolside/laguna-s-2.1:free", so the gate was red for infrastructure reasons and no baseline existed. Kilo suggested `cohere/north-mini-code:free` and `kilo-auto/free`.

## Tradeoffs considered

- **`kilo-auto/free`**: never goes stale, but the gateway picks the underlying model, so results are not comparable across runs. The study needs a fixed model.
- **A paid model**: less noisy, but spends budget on every run; `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md` chose free tier on purpose.
- **Chosen: a named free coding model.** Free models can be withdrawn again; if so, supersede this decision and re-record the baseline.

Amends the model choice in `0043`; its other terms stand.
