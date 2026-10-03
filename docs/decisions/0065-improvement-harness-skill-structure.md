---
id: 0065-improvement-harness-skill-structure
title: Improvement skills are implemented as OpenCode subagents
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "subagents", "opencode", "process"]
track: process
accepted-by: sergemso
---

## Decision

Each improvement type shall be implemented as an OpenCode subagent (a `.md` file under `.opencode/agent/improve/`), not as a KMS skill (`plugins/kms/skills/**/SKILL.md`), a promptfoo case, or a plain prompt template.

- Subagent files define the agent's instructions, tools, and behavior in OpenCode's native format.
- The orchestrator invokes subagents via `opencode agent <subagent-name> --prompt "<context>"`.
- Subagents have full tool access (read, write, edit, grep, glob, bash) for multi-step workflows.
- Shared context (repo root, config, queue item) is passed via the prompt and environment variables.

## Rationale

- OpenCode subagents are the native extension mechanism for custom agent behaviors — no adapter layer needed.
- KMS skills (`SKILL.md`) are designed for *human* invocation in a chat session, not for programmatic orchestration. They lack tool declarations, structured I/O, and error handling.
- Promptfoo cases (`0043`) are for *evaluation* (fixed prompt → graded output), not for *execution* (variable context → tool-using workflow).
- Plain prompt templates would require a custom runner; subagents reuse OpenCode's proven execution engine.
- Subagents can be versioned, reviewed, and improved like any other code — and dogfooded by the harness itself (`0070`).

## Consequences

- Each improvement type gets a subagent file: `improve-lint-fix.md`, `improve-skill-rewrite.md`, `improve-kb-repair.md`, `improve-guardrail-update.md`.
- Subagents must follow OpenCode's agent schema (instructions, tools, model preferences).
- The orchestrator manages subagent lifecycle: spawn → feed queue item → collect result → verify → commit.
- Subagent definitions live in `.opencode/agent/improve/` (per `0072`), not in the plugin's skill directory.
- Token economy (`0026`) applies to subagent instructions — they must be concise.
