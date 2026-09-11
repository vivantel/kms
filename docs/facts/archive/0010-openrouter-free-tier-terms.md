---
id: 0010-openrouter-free-tier-terms
title: OpenRouter's free-tier model access, rate limits, and quota-extension mechanism
status: deprecated
date: 2026-09-04
tags: [kms, openrouter]
kind: environmental
governed-by: 0043-eval-harness-for-shipped-skill-changes
---

Confirmed 2026-09-04 via current pricing/aggregator sources: OpenRouter
offers 27+ models at $0/token (id suffix `:free`), usable with a $0
balance and no credit card, including coding-capable options (Qwen3
Coder named specifically among them). Free models are rate-limited to
20 requests/minute and 200 requests/day; a one-time, non-expiring $10
purchase raises the daily `:free` cap from 200 to 1,000 requests.

**Not confirmed with high confidence, and expected to change**: the
free-model roster itself. Providers add, pull, and reprice models on
this tier continuously — re-verify which specific model to target
against OpenRouter's own models page at implementation time, not
against this fact's snapshot.

**Re-verified 2026-09-05**: confirmed via `openrouter.ai/api/v1/models`. The roster already
rotated — Qwen3 Coder is no longer on the free tier. 19 `:free` models are live; the harness
targets `poolside/laguna-s-2.1:free` (Poolside's dedicated coding-agent model, scored on
Terminal-Bench 2.1) as the runner and `z-ai/glm-5.2:free` (a distinct large-context reasoning
model) as the judge, replacing GitHub Models per
`docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`'s amendment. The 20 req/min,
200 req/day free-tier limits above are otherwise unchanged.

**Superseded, 2026-09-10**: the harness no longer talks to OpenRouter directly at all — Kilo's
own built-in gateway serves the same `:free`-suffixed OpenRouter models (e.g.
`kilo/poolside/laguna-s-2.1:free`) with no API key or account, confirmed by testing (see
`docs/facts/0012-kilo-gateway-free-tier-access.md`). This fact's content about OpenRouter itself
is still accurate; it's just no longer what `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`
depends on. Kept here, not deleted, as a record of the path tried first.
