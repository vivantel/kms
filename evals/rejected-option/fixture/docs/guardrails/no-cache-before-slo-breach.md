---
id: no-cache-before-slo-breach
title: Do not add a cache layer to the orders API while its p95 is under the SLO
status: active
date: 2026-09-04
tags: [performance, guardrail]
governed-by: [0001-no-cache-layer-until-latency-slo-breach]
grounded-in: [0001-orders-p95-latency]
enforced-by: ci job latency-budget-check
derivation-note: Given decision 0001-no-cache-layer-until-latency-slo-breach and fact 0001-orders-p95-latency (p95 is 210 ms against 400 ms), no cache layer may be added to the orders API.
pinned:
  0001-no-cache-layer-until-latency-slo-breach: "4f43800a6041"
  0001-orders-p95-latency: "03cabf0ded3c"
---

## Guardrail

A change MUST NOT introduce a cache layer in front of the orders API while its p95 latency is under 400 ms.
