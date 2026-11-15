---
id: 0069-kms-owns-durable-knowledge-not-specs-or-coordination
title: kms owns durable knowledge artifacts and their validation; specs and coordination artifacts stay outside
status: draft
date: 2026-11-15
tags: [kms, scope]
track: process
---

## Decision

- kms owns the four durable knowledge artifacts (fact, decision, guardrail, procedure) and their validation. It does not store product specs, plans, outcome briefs, meters or harness configuration.
- go-getter owns coordination artifacts (outcome brief, unit tree, meter, operating charter, harness config) and the harness. It does not define or validate knowledge artifacts.
- Both detect and tolerate OpenSpec (go-getter decision 0075). Neither copies spec content; a record points at an OpenSpec change with `source`.
- Guardrails that constrain product behaviour ("never log PII") stay in scope: they are enforceable rules, not specs. Requirements, behaviours and acceptance criteria stay out.

## Why

The cut is by artifact ownership: kms owns what outlives the work; go-getter owns what has an owner, state and `Accept`; OpenSpec owns what a change should do. Without it, kms's model drifts toward specs (the `track: product` field was the symptom) and overlaps both neighbours.

## Tradeoffs considered

- **Extend kms to specs**: rejected. A fifth artifact type that collides with OpenSpec and expands onto an unstable base.
- **Full merge into one product**: rejected. kms's small footprint is its adoption funnel.

## Twin and status

Go-getter twin: written in plan step D0 (`docs/decisions/` in the go-getter `feat/adopt-kms-core` branch). Draft by an agent; the owner accepts it (set `status: active` and `accepted-by`) in plan phase I. Recommended option: as written. Plan: `docs/plans/kms-core-and-go-getter-consolidation.md` step A3.
