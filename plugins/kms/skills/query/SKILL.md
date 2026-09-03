---
name: query
description: Answer a question from a project's fact/decision/guardrail/skill knowledge base, with citations to the artifacts the answer is drawn from — never from memory or inference when the knowledge base already has the answer. Use when the user asks what was decided, why a rule exists, or what's currently true about the project, e.g. "what did we decide about X", "why does this guardrail exist".
---

Search `docs/{facts,decisions,guardrails,skills}/` for the artifacts relevant to the question, then answer using only what they say — never from memory or inference when a real artifact already settles it.

## Answering

1. Read each type's `INDEX.md` first, if present, to narrow candidates by tag/title before opening full files; fall back to searching all four directories by keyword/topic/`tags` when no index exists.
2. If nothing relevant is found, say so plainly — don't guess or synthesize an answer the knowledge base doesn't actually support.
3. If a decision has been superseded, follow `superseded-by` transitively until reaching a decision whose own `status` isn't `superseded` — cite that final active decision alongside the original, not just the next hop.
4. Answer in prose, then list every artifact the answer drew from as `Refs: <repo-relative-path>` — one per artifact, matching `attribute`'s trailer format so this plugin has one citation convention.

## Out of scope

Writing or editing any artifact — this skill only reads and cites. Use `roadmap` to capture new knowledge, `capture` to maintain it, `bootstrap` to set it up.
