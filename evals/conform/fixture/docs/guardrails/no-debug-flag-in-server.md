---
id: no-debug-flag-in-server
title: Server code must not set DEBUG to True
status: active
date: 2026-06-02
tags: [ops]
governed-by: [0001-no-debug-in-production]
enforced-by: ci job lint-server
derivation-note: Given decision 0001-no-debug-in-production, committed code must not set DEBUG to True.
---
