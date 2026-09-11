---
id: 0011-github-models-free-tier-terms
title: GitHub Models' free-tier API, GITHUB_TOKEN access, and context-window limits
status: deprecated
date: 2026-09-04
tags: [kms, github-models]
kind: environmental
governed-by: 0043-eval-harness-for-shipped-skill-changes
---

Confirmed 2026-09-04 via current documentation/aggregator sources:
GitHub Models exposes an OpenAI-compatible Chat Completions endpoint at
`https://models.github.ai/inference/chat/completions`, usable with the
OpenAI SDK directly. Within a GitHub Actions workflow it can be reached
using the workflow's own ambient `GITHUB_TOKEN` — no separate API key
or repo secret needed. Rate limits are per-model and gated by the
caller's GitHub Copilot subscription tier (e.g. Free tier ≈10
requests/minute baseline; higher for Pro/Pro+/Business). Context
windows are small — 8K input / 4K output — and GitHub explicitly frames
this API as suited to prototyping, not production workloads.

**Not confirmed with high confidence**: whether a workflow's
`GITHUB_TOKEN` draws on the *repository owner's* Copilot subscription
tier specifically, or some other, more universal grant for public
repositories. `vivantel/kms` is a public repository. Verify this at
implementation time before relying on a specific rate-limit figure.

**Superseded by events, 2026-09-05**: GitHub Models was fully retired 2026-07-30
(`docs.github.com/en/github-models`'s own retirement notice: "the playground, model catalog,
inference API, and bring your own key (BYOK) are no longer available to any customer") —
predating this fact's own 2026-09-04 snapshot date, meaning it was already stale when written.
`docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`'s amendment records the judge
model falling back to a second free OpenRouter model instead. Kept here, not deleted, as an
accurate record of what this fact claimed and why it no longer holds.
