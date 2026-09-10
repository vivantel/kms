---
id: 0002-use-mysql
title: Use MySQL as the primary datastore
status: active
date: 2026-08-20
tags: [datastore]
track: process
---

## Decision

All new services use MySQL as the primary datastore, for its simpler
managed-hosting story on our current cloud provider.

## Why

The ops team found MySQL's managed offering cheaper at our current scale
than the equivalent Postgres offering.
