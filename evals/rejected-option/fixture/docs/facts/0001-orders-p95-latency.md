---
id: 0001-orders-p95-latency
title: Orders API p95 latency is about 210 ms
status: active
date: 2026-09-03
tags: [performance]
source: dashboard "orders-api / latency" (Grafana)
last-verified: 2026-11-15
scope: {component: orders-api, environment: production}
---

p95 latency of `GET /orders` is about 210 ms against a 400 ms SLO.
