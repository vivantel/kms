---
id: 0001-cap-retry-backoff
title: Cap retry backoff at 5 attempts with exponential delay
status: active
date: 2026-07-15
tags: [reliability]
track: process
---

## Decision

Retries against the warehouse API back off exponentially, capped at 5 attempts.

## Why

Unbounded retries during an outage hammered the warehouse API instead of
giving it room to recover.
