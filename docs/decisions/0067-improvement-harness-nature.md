---
id: 0067-improvement-harness-nature
title: Improvement harness is both a KMS skill (interface) and infrastructure (implementation)
status: draft
date: 2026-10-03
tags: ["kms", "improvement-harness", "skill", "infrastructure", "process"]
track: process
accepted-by: sergemso
---

## Decision

The improvement harness shall have a dual nature:

1. **Skill interface** (`docs/skills/improvement-harness.md`): A KMS procedure skill that documents the harness's contract — what it does, how to invoke it, its configuration, its guarantees, and its observability. This skill can be captured, linted, queried, and improved like any other KMS artifact.

2. **Infrastructure implementation** (`.opencode/agent/improve/`, `plugins/kms/hooks/improvement-runner.sh`, `.opencode/improvement.yaml`): The actual executable code — subagents, orchestrator script, config. This is not a governed artifact; it's the runtime that the skill describes.

The skill's `SKILL.md` (in `plugins/kms/skills/improvement-harness/`) delegates to the infrastructure: "Run the improvement harness by invoking `opencode agent improve-harness` with the appropriate context."

## Rationale

- The skill interface makes the harness discoverable via `query`, `onboard`, `bootstrap`, and `lint` — it's part of the knowledge base.
- The infrastructure is the executable reality; keeping it separate from the governed skill avoids the "skill body too long" problem and allows rapid iteration on implementation without KB process overhead.
- This mirrors the `bootstrap`/`capture`/`lint` pattern: each has a skill interface (in `plugins/kms/skills/`) and implementation logic (in the skill body + shared files).
- Dogfooding (`0070`): the harness can improve its own skill interface (the `SKILL.md`) via the normal improvement flow, while the infrastructure improves itself via subagent rewrites.

## Consequences

- Two files describe the harness: `plugins/kms/skills/improvement-harness/SKILL.md` (skill interface) and `docs/skills/improvement-harness.md` (procedure in KB). They must stay in sync — the skill interface is the source of truth for users; the KB procedure is the source of truth for the harness's own self-knowledge.
- The orchestrator script is the entry point for both scheduled and event-driven runs.
- The harness's own subagents (`.opencode/agent/improve/*.md`) are infrastructure, not skills — they don't go through the plugin packaging layer.
- `uninstall` skill must remove both the skill interface and the infrastructure (or at least document how).
