---
id: 0012-kilo-gateway-free-tier-access
title: Kilo Code CLI's built-in gateway serves :free models with no account or API key
status: active
date: 2026-09-10
tags: [kms, kilo]
source: 'kilo run --auto -m kilo/<model>:free "<prompt>" --print-logs'
last-verified: 2026-11-20
scope:
  component: Kilo Code CLI built-in gateway
---

Confirmed by testing 2026-09-10: Kilo Code CLI's own built-in model gateway (provider id
`kilo`, distinct from routing through a separately-configured OpenRouter/Anthropic/etc.
provider) serves a curated catalog of 300+ models, addressed as `kilo/<vendor>/<model>`. Every
model whose id carries a `:free` suffix in that catalog (e.g. `kilo/poolside/laguna-s-2.1:free`,
`kilo/nvidia/nemotron-3-ultra-550b-a55b:free`, `kilo/cohere/north-mini-code:free`) completes a
real request with **no `kilo auth login`, no API key, and no `hasToken`** — confirmed via
`kilo run --auto -m kilo/<model>:free "..." --print-logs --log-level DEBUG` showing
`hasToken=false` on the `kilo` provider's own auth-resolution log line, and a genuine model
response. A non-`:free` model in the same catalog (e.g. `kilo/qwen/qwen3-coder`) instead errors
`You need to sign in to use this model.` — so the `:free` suffix is the actual gate, not the
`kilo` provider as a whole.

This is a different mechanism from OpenRouter's own `:free` tier
(`docs/facts/archive/0010-openrouter-free-tier-terms.md`, now superseded for this repo's purposes): the
`kilo` provider's catalog is Kilo's own curated subset, not a 1:1 mirror of OpenRouter's — a
model id that's free on OpenRouter directly is not necessarily present, or free, under `kilo/`
(e.g. `kilo/z-ai/glm-5.2:free` doesn't exist in this catalog at all).

**Not confirmed with high confidence**: any rate limit, daily cap, or terms-of-service note for
this anonymous, no-account tier — no published documentation surfaced describing it (Kilo's own
docs mention "500+ models via the Kilo Gateway" without a free/paid breakdown). It's plausible
this is anti-abuse-throttled per IP/machine rather than per account; if the eval harness starts
failing with an auth or rate-limit error where it previously worked, re-verify this fact before
assuming the harness itself broke.

Re-verified 2026-11-20 with `kilo` 7.8.32 (`kilo models`, `kilo run --auto`). The
free tier is not a stable promise: it held in CI 2026-09-10; `poolside/laguna-s-2.1:free`
was withdrawn by 2026-11-08 (every case failed `Model not found`; the harness
now prints one `=== HARNESS ERROR: ... ===` line for that and the PR summary
labels it infra); and `cohere/north-mini-code:free`, the model every CI case
pins, is **no longer in the catalog** on 2026-11-20. The judge model
`kilo/nvidia/nemotron-3-ultra-550b-a55b:free` still exists and answers. The
catalog's `:free` models that day: baidu/ernie-5.5-flash-preview,
dots-studio/dots-3-note-preview, inclusionai/ling-3.2-flash, liquid/lfm-3-1.7b,
nvidia/nemotron-3-nano-omni-30b-a3b-reasoning, nvidia/nemotron-3-ultra-550b-a55b,
nvidia/nemotron-3.5-lightning, nvidia/nemotron-3.5-super-vl, particle-ai/particle-1,
recursive/flint-v1.0. Sign-up and usage limits (0059's amendment) apply from some
machines; "no account or API key" held only for the dates above.
