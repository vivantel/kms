---
id: 0005-global-principles-applied-to-existing-artifacts
title: Result of auditing existing artifacts against the global writing principles
status: current
date: 2026-08-29
tags: [kms, knowledge-management, audit]
---

As of 2026-08-29, every artifact under `docs/{facts,decisions,guardrails,skills}/`
and every `plugins/kms/skills/*/SKILL.md` was checked against the global
principles stated in `plugins/kms/skills/steward/SKILL.md` (token
economy, one statement one job). Two violations found and fixed:

- `docs/guardrails/knowledge-artifact-derivation-fields.md` bundled three
  distinct normative claims (guardrail frontmatter, fact frontmatter,
  re-derivation-on-change) in one file — split into
  `guardrail-derivation-fields.md`, `fact-governance-fields.md`, and
  `guardrail-re-derivation-on-source-change.md`.
- `docs/skills/adding-agent-support.md` embedded an incident narrative
  (a past SEO-search-result failure) inline in a procedural step — moved
  to `docs/facts/0003-codex-plugin-manifest-schema.md`, replaced with a
  pointer.

Everything else — all four pre-existing guardrails, all facts, all six
`SKILL.md` bodies — was judged already economical, and each guardrail's
several numbered sub-rules judged to be one derivation with several
clauses (not multiple jobs), so left unchanged. Decisions and plans were
excluded from the audit — a decision's job is to carry rationale, and a
plan must stay self-sufficient for a cold agent.
