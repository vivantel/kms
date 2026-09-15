---
id: 0001-knowledge-artifact-storage-convention
title: Knowledge artifacts live under docs/{facts,decisions,guardrails,skills}/
status: active
date: 2026-07-29
tags: [kms, roadmap, knowledge-management]
track: process
---

## Decision

Knowledge artifacts produced by the `roadmap` skill are written to a top-level
`docs/` tree, one directory per artifact type:

- `docs/facts/` — descriptive artifacts (what's true now)
- `docs/decisions/` — axiomatic artifacts (what the team commits to, with rationale)
- `docs/guardrails/` — normative artifacts (what must/must not happen)
- `docs/skills/` — procedural artifacts (how to decide or act)

Each artifact is a single Markdown file with YAML frontmatter (`id`, `title`,
`status`, `date`, `tags`) followed by a prose body. Facts and decisions are
additionally numbered (`NNNN-slug.md`, 4-digit, 1-based, per directory) —
see the "Numbering facts and decisions" section of
`plugins/kms/skills/roadmap/SKILL.md` — while guardrails and skill
prescriptions are named by slug only.

## Why

This was the first `roadmap` invocation in this repo, so there was no
existing convention to detect or extend (checked: no `docs/`, no ADR
directory, no fact/guardrail files anywhere in the tree). The alternative of
a single flat `docs/KNOWLEDGE.md` file was rejected because it won't scale
once artifacts multiply and can't be linked to individually by path from
commit trailers (see `docs/decisions/0003-commit-trailer-traceability.md`).

## Tradeoffs considered

- **Single `docs/KNOWLEDGE.md`**: simplest to start, but doesn't scale and
  can't be referenced per-artifact from git trailers.
- **`docs/knowledge/{facts,intents,guardrails,skills}/`**: same shape, less
  conventional naming (`intents` vs `decisions`). Rejected in favor of the
  more ADR-familiar `decisions` name.
- **Chosen: `docs/{facts,decisions,guardrails,skills}/`** — one directory per
  type, individually addressable files, ADR-style naming.
