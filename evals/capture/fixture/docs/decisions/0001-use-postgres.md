---
id: 0001-use-postgres
title: Use PostgreSQL as the primary datastore
status: active
date: 2026-06-01
tags: [datastore]
track: process
---

## Decision

All new services use PostgreSQL as the primary datastore.

## Why

The team already runs Postgres in production for the flagship service;
standardizing avoids operating two different database engines.
