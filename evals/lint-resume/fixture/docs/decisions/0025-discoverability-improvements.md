---
id: 0025-discoverability-improvements
title: Improve discoverability — README badges, GitHub topics and description sync
status: active
date: 2026-08-30
tags: [kms, discoverability, marketing]
track: product
---

## Decision

Two concrete, low-effort discoverability improvements, chosen over
higher-effort content work (screenshots, comparison sections, an
external docs site) that a text-only session can't actually produce:

1. **README badges**: static (non-CI-backed) shields.io badges for
   license (MIT) and "Claude Code Plugin" only. No version badge — this
   repo already keeps `version` in lockstep across the two plugin
   manifests (`docs/guardrails/plugin-manifest-version-sync.md`;
   `marketplace.json` carries no `version` field at all, so it's outside
   that guardrail's scope); a third README-badge copy of the same number
   would be a third place that sync has to cover for no real benefit.
2. **GitHub repo topics and description**: both were empty/stale before
   this decision (topics: none set; description: named only 6 of the
   plugin's 11 skills at the time of the previous session). Synced via
   `gh repo edit` to a description matching the plugin's actual current
   scope, and a topic list a prospective user might actually search:
   `claude-code`, `claude-code-plugin`, `ai-agent`,
   `knowledge-management`, `architecture-decision-records`,
   `developer-tools`, `documentation`, `marketplace`.

## Why

A tool that's genuinely useful once found still needs to be found first
— GitHub's own topic search and repo description are free surface area
that was simply unused. No CI exists in this repo to back a build/test
badge honestly, so limiting badges to static, always-accurate claims
(license, plugin type) avoids the credibility cost of a badge that
implies more automation than actually exists.

## Tradeoffs considered

- **Also add a version badge**: more informative at a glance, but adds a
  third manifest-version-sync target for no functional benefit — every
  other consumer of the version number is a manifest file an installer
  actually reads; a README badge is purely decorative by comparison.
  Rejected.
- **Skip badges entirely, topics/description only**: cheaper, but static
  badges cost nothing to maintain (they don't reference a moving number)
  and are a near-universal convention prospective users scan for.
  Rejected — chosen explicitly over this option when interviewed.
- **Chosen: static license/plugin badges plus a synced GitHub topics and
  description.**
