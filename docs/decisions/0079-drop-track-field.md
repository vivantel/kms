---
id: 0079-drop-track-field
title: Drop the decision track field and the role lists built on it
status: draft
date: 2026-11-15
tags: [kms, knowledge-management, taxonomy]
---

## Decision

Decisions no longer carry a `track` field. The product/process split was consumed by nothing but two role lists, a required-field check and an exclusivity check (8 of 64 kms decisions were `product`). Retired with it: the product/process role lists (`docs/skills/{product,process}-track-roles.md`, decision 0013), lint check 14 (role list gone cold) and check 15 (track exclusivity), whose numbers stay unused so the others keep theirs, and `bootstrap` step 7's role-list compilation (tag vocabulary stays). The `track:` line is deleted from every decision by `migrate.py`; existing projects keep working because the checker reads a leftover `track` as an older-shape advisory.

## Why

Plan consolidation B1: kms owns durable knowledge, not product specs (0069), so the product/process distinction no longer separates anything kms needs. A one-claim-per-field model is smaller and the same split is recoverable from tags.

## Tradeoffs considered

- **Keep `track` optional**: leaves a dead field for adopters to guess about.
- **Chosen: remove it with a one-pass migration.**

## Dispositions

0010 and 0038 superseded by this decision; 0013 superseded (role lists retired); guardrail `decision-track-field` archived. Draft; owner acceptance in plan phase I. Plan: `kms-core-and-go-getter-consolidation.md` B1.
