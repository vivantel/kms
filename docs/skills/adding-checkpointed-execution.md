---
id: adding-checkpointed-execution
title: Procedure for adding chunked, checkpointed execution to a shipped skill
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing, procedural]
---

# Adding chunked, checkpointed execution to a shipped skill

Applies when a skill's own work can grow unbounded with project size (opening every file of a type, or
mining a whole git history) the way `bootstrap`'s and `lint`'s did — see
`docs/decisions/0056-chunked-checkpointed-execution-for-bootstrap-and-lint.md`.

1. Read `plugins/kms/shared/checkpointing.md` — it defines the checkpoint format and resume protocol once;
   never redefine it inline in a skill body.
2. Identify the skill's per-item, per-file, or per-commit work (chunkable) versus its aggregate,
   consumes-everything-else work (not chunkable, runs once at the end) — most skills split into exactly
   these two phases.
3. Add one line to the skill's `SKILL.md` pointing at `shared/checkpointing.md` for the chunked phase's
   mechanics, the same way `bootstrap`/`lint` already point at `shared/artifact-model.md`.
4. Add a resume-specific eval case (`evals/<skill>-resume/promptfooconfig.yaml`) alongside the skill's
   existing case: a shortened timeout forces a kill mid-run, the runner restarts, asserting completion and
   no duplicated output.
5. Confirm the skill's own confirmation gates, if any, are worded as "a confirming party" per
   `docs/guardrails/confirming-party-acceptable-for-checkpoint-gates.md` — unattended chunked execution and
   a human-only-worded gate don't mix.
