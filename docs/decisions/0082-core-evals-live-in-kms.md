---
id: 0082-core-evals-live-in-kms
title: Core skill evals stay in kms; go-getter runs conformance fixtures and its own harness evals
status: active
accepted-by: Sergei Strebulaev
date: 2026-11-15
tags: [kms, eval-harness]
---

## Decision

The core's skill evals (Kilo CLI against its free gateway, orchestrated by promptfoo), the lint matrix and the admission eval stay in kms. go-getter runs only the conformance fixtures (`evals/lint/conformance/`) against its vendored checker and its own harness evals. Both repos align on one promptfoo version.

## Why

The same skill behaviour must not be measured twice with two harnesses. kms owns the skills that touch knowledge artifacts, so it owns their evals; go-getter owns coordination and harness behaviour.

## Tradeoffs considered

- **Duplicate the evals in both repos**: two harnesses drift and report different answers for one behaviour.
- **Shared eval repo**: another repo for one maintainer; deferred.

## Twin

go-getter twin: written in D0; its `eval` change is made in D3. Accepted 2026-11-16 by the owner. Plan: `kms-core-and-go-getter-consolidation.md` F1.
