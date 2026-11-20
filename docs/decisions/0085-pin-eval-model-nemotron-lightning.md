---
id: 0085-pin-eval-model-nemotron-lightning
title: Pin the eval harness to nvidia/nemotron-3.5-lightning:free after north-mini-code was withdrawn
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-20
tags: [kms, eval-harness, kilo]
---

## Decision

Every CI eval case uses `nvidia/nemotron-3.5-lightning:free`, run as `kilo/nvidia/nemotron-3.5-lightning:free` through the Kilo gateway. The runner and judge send only ids beginning `nvidia/nvidia/` to the separate keyed NVIDIA provider; every other id gets the `kilo/` prefix. The model stays pinned by name.

## Why

On 2026-11-20 `cohere/north-mini-code:free` (the pin of 0057) was no longer in the gateway catalog, so every case would fail with `Model not found`. This is the second withdrawal in two weeks (0057 followed `laguna-s-2.1`). The nemotron-3.5-lightning family already grades the `bootstrap` variants and the matrix and admission evals, and it is free through the gateway without a key, which also lets those two run without an NVIDIA key.

## Tradeoffs considered

- **`inclusionai/ling-3.2-flash:free`**: needs no runner change but has no track record on these skills.
- **A keyed NVIDIA provider for CI**: stable, but needs a CI secret and ends the no-account contributor path chosen in 0043.
- **`kilo-auto/free`**: rejected in 0057 for the same reason: results are not comparable across runs.
- **Chosen: a named free model, plus a harness that reports withdrawal as infrastructure.** Withdrawal will recur; the harness now prints `=== HARNESS ERROR ===` and the PR summary labels it infra, so the next one is a one-line change here, not a red gate that looks like skill regressions.

Supersedes 0057. Baselines recorded on north-mini-code are not comparable; re-record on this model.

## Amendment 2026-11-20

The first CI `/eval` on `nemotron-3.5-lightning:free` passed 2 of 6 cases (`bootstrap`, `lint`), and a 14-request routing eval hit about 86% with a different two misses each run. A trial of the four failing cases (`decide`, `capture`, `roadmap`, `attribute`), 4 runs each, `--repeat 4`, kilo 7.8.32, on this tree:

| Model | Passed of 16 | Notes |
|---|---|---|
| `nvidia/nemotron-3.5-super-vl:free` | 15 | decide 3/4, the others 4/4 |
| `inclusionai/ling-3.2-flash:free` | 1 | provider errors on roadmap |

Every CI case now pins `nvidia/nemotron-3.5-super-vl:free`. The id of this file keeps the lightning name because ids do not change; the Decision text above names the first choice, which this amendment replaces. The `lint`, `bootstrap`, `query`, `conform` and `uninstall` cases have not yet run on the new model.

