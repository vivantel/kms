---
id: 0052-state-the-core-thesis-in-positioning-copy
title: State kms's core thesis in its own positioning copy, not just its feature list
status: active
date: 2026-09-12
tags: [kms, discoverability, marketing]
track: product
---

## Decision

Every surface describing what `kms` *is* — `README.md`, the GitHub repo
description, and all three plugin-manifest `description` fields
(`marketplace.json`, `plugin.json`, `.codex-plugin/plugin.json`) — led
with a feature/skill list and never stated why it's worth adopting: an
agent's problem isn't memory capacity, it's having no vocabulary
distinguishing a fact from a decision from a guardrail. All four now
open with (or are prefixed by) an outcome-first statement of that
differentiator — "give your AI coding agent durable, checkable
knowledge... it won't forget, contradict, or re-litigate" — and
`README.md` links out to
[the author's own fuller treatment](https://medium.com/@strebulaev/taxonomy-is-a-language-why-your-ai-agent-needs-a-vocabulary-not-more-memory-000b8023a40a)
for readers who want the deeper argument.

A first draft of this same change led every terse surface with the
article's own conceptual term, "a controlled vocabulary for AI agent
knowledge," and added `taxonomy` as a GitHub topic. Reviewed and
reverted before shipping: a one-line plugin-marketplace description or
GitHub summary gets one skim-pass, and "controlled vocabulary" answers
"what abstract category is this" rather than "what does it do for me"
— exactly the kind of insider framing a first-glance visitor bounces
off. `taxonomy` as a topic was reaching for thematic accuracy over real
discoverability too — that topic is dominated by actual
taxonomy/ontology projects, not AI tooling, so it wouldn't have reached
the intended audience. The deeper term still earns its place in
`README.md`'s longer paragraph, which has room to build up to it
(pain → mechanism → term) the way the terse surfaces don't.

## Why

A prospective user or contributor hitting any of these surfaces for the
first time saw only *how* to use `kms` (a skill list), never *why* it's
different from a vector database or a plain notes file — the exact
differentiator that makes it worth adopting over ad hoc memory. This
isn't hypothetical: the same gap was independently identified from
outside the repo, by the person best positioned to state it precisely.

This extends `docs/decisions/0025-discoverability-improvements.md`
rather than reopening it: `0025` explicitly deferred "higher-effort
content work (screenshots, comparison sections, an external docs site)
that a text-only session can't actually produce" — true at the time,
since no such content existed yet to draw from. It now does, in the
form of a complete, already-written article stating the thesis more
sharply than a `kms` session composing from scratch could reasonably
attempt on its own.

## Tradeoffs considered

- **Write the README's own version of this argument from scratch**:
  avoids leaning on external content, but risks a weaker, less precise
  restatement of an argument someone already made well — and the
  Medium link gives full credit and drives traffic both ways.
- **Only fix `README.md`, leave the manifest descriptions alone**:
  cheaper, but the manifest descriptions are the primary discovery
  surface for anyone browsing plugins from inside Claude Code or Codex
  directly — exactly the audience least likely to have found the GitHub
  README first.
- **Chosen: state the thesis, briefly, on every surface that claims to
  say what `kms` is — full argument via the linked article only in the
  README, not duplicated at length across manifests where token/character
  budgets are tighter.**
