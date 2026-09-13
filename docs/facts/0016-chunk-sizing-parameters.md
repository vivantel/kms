---
id: 0016-chunk-sizing-parameters
title: Chunk-sizing values for lint's and bootstrap's paged phases
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing]
kind: decision
governed-by: [0056-chunked-checkpointed-execution-for-bootstrap-and-lint]
---

A page accumulates files (lint's per-type phase, bootstrap's file-extraction steps), in stable
alphabetical order, until reaching an estimated 15,000 tokens, then checkpoints. A single file already
over that budget gets a one-file page of its own — a page boundary is always a whole number of complete
files, never a split within one. Bootstrap's git-history mining (step 1) uses the same ~15,000-token
accumulation rule, walking the log oldest-first, checkpointing the last completed commit SHA.
