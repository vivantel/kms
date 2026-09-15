---
id: checkpoint-file-lifecycle
title: A chunked run's checkpoint file must be cleaned up on success and never silently resumed
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing, guardrail]
governed-by: [0056-chunked-checkpointed-execution-for-bootstrap-and-lint]
grounded-in: [0015-checkpoint-file-location-and-lifecycle]
derivation-note: 0056 commits to chunked, resumable execution; 0015 fixes the checkpoint file's
  location and lifecycle values. Together they require that a completed run leaves no checkpoint
  behind, and that a found checkpoint is never trusted or resumed without the user's say-so and a
  fresh check that nothing moved underneath it.
---

## Guardrail

A chunked `bootstrap` or `lint` run must delete its checkpoint file as its last action on success, and
must never resume from a found checkpoint without both asking the user to confirm and re-verifying the
recorded file/commit set still matches the project's current state.
