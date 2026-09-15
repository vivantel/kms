---
id: 0015-checkpoint-file-location-and-lifecycle
title: Checkpoint file path, naming, and lifecycle for chunked bootstrap/lint runs
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing]
kind: decision
governed-by: [0056-chunked-checkpointed-execution-for-bootstrap-and-lint]
---

A chunked `bootstrap` or `lint` run's in-progress state lives at
`docs/.kms-checkpoints/<skill>-<run-id>.md`, checked into git, holding an item manifest (the ordered
files/commits enumerated at start) plus the last-completed offset. It is deleted automatically as the
run's last action on success — a file found there always means an interrupted run. When one is found on a
new invocation, the skill asks the confirming party to resume or discard rather than resuming silently;
resuming first re-lists the recorded files/commits and compares against the manifest — any difference
forces a fresh start for file-based paging, while commit-history paging tolerates new commits at the tip
(only a rewritten history forces a fresh start there).
