---
id: 0001-no-debug-in-production
title: Debug mode is never enabled in committed server code
status: active
date: 2026-06-01
tags: [ops]
---

## Decision

Committed server code keeps `DEBUG = False`; debugging is enabled by environment only.

## Why

A debug server leaked stack traces in an earlier incident.
