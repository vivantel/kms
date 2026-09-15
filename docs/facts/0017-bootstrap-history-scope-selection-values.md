---
id: 0017-bootstrap-history-scope-selection-values
title: Bootstrap's git-history scope question — options, threshold, and default recommendation
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing]
kind: decision
governed-by: [0056-chunked-checkpointed-execution-for-bootstrap-and-lint]
---

Before mining git history (step 1), bootstrap always asks how much to mine, offering four options: all
history, last N commits, last M years, or custom. The recommended option is computed, not fixed: bootstrap
checks the actual commit count (`git rev-list --count`) first. Under 1,000 commits, it recommends "all."
At or above 1,000, it recommends a bounded window of the last 2 years.
