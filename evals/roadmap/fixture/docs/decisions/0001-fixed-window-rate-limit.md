---
id: 0001-fixed-window-rate-limit
title: Rate-limit the public API with a fixed window
status: active
date: 2026-04-01
tags: [api, rate-limiting]
track: process
---

## Decision

The public API is rate-limited using a fixed 60-second window per API key.

## Why

Simplest thing that could work at launch; revisit if traffic patterns show
its edges are a real problem.
