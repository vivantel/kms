---
id: no-session-ttl-above-hour
title: No session lifetime may exceed one hour of inactivity
status: active
date: 2026-06-03
tags: [auth]
governed-by: [0001-session-ttl-30-minutes]
enforced-by: ci job session-timeout-test
derivation-note: Given decision 0001-session-ttl-30-minutes, a session idle timeout above one hour must not ship.
---
