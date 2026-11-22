---
id: 0001-no-cache-layer-until-latency-slo-breach
title: No cache layer in front of the orders API until p95 latency breaches 400 ms
status: active
date: 2026-09-03
tags: [performance]
governed-facts: [0001-orders-p95-latency]
accepted-by: tech lead
---

## Decision

Do not add a cache layer (Redis, Memcached or in-process) in front of the orders API until its p95 latency exceeds 400 ms for a week.

## Why

A cache adds an invalidation path and a second source of truth for orders; at current load Postgres alone meets the SLO.

## Tradeoffs considered

- Redis read-through cache: rejected for now; stale reads on order status were an incident in the previous system.
- Postgres read replica: kept as the first step if the SLO is breached.
