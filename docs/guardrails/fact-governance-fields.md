---
id: fact-governance-fields
title: A fact must carry a `source` or be cited by another artifact
status: active
date: 2026-08-29
tags: [kms, knowledge-management, guardrail]
governed-by: [0071-facts-carry-no-outgoing-edges]
derivation-note: >
  Given decision 0071 (facts carry no outgoing edges; a fact is noise
  unless re-observable or cited), every fact file must carry `source` or be
  cited by another artifact.
pinned:
  0071-facts-carry-no-outgoing-edges: "9a5d50ae1319"
---

## Guardrail

Any fact file MUST carry `source` (a URL, path or command to re-observe it) or be cited by at least one other artifact, and MUST NOT carry `kind` or `governed-by`. A fact with neither `source` nor a citer is noise: flag it for removal.

## Derivation

- **Axiomatic basis**: `docs/decisions/0071-facts-carry-no-outgoing-edges.md` — facts carry no outgoing edges; the arrow runs from consumers to facts.
- **Normative conclusion**: therefore a fact stays admissible only while it can be re-observed or something depends on it.
