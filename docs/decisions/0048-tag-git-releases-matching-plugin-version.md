---
id: 0048-tag-git-releases-matching-plugin-version
title: Tag git releases with the same version as plugin.json, not a separate sequence
status: active
date: 2026-09-11
tags: [kms, git, release, packaging]
track: process
fitness-functions: ["Once lint or a CI check can verify it cheaply, confirm every plugins/kms manifest version bump commit has a matching git tag of the same version pushed at or shortly after that commit — until then, this is manually maintained debt, not automated."]
---

## Decision

- This repo tags releases with git tags **matching `plugins/kms/.claude-plugin/plugin.json`'s
  own `version` field** (kept in lockstep across manifests by
  `docs/guardrails/plugin-manifest-version-sync.md`) — one number, not two. A tag names the
  exact `plugin.json` version that commit shipped: `0.11.0` on the commit where `plugin.json`
  first read `"version": "0.11.0"`.
- Supersedes `docs/decisions/archive/0046-tag-git-releases-independent-of-plugin-version.md`, which
  chose to start a separate tag sequence at `0.1.0`, deliberately kept independent of
  `plugin.json`'s version. That tag was deleted and replaced with `0.11.0` at the same commit.
- No enforced cadence or automation, unchanged from `0046`: a tag is added by whoever ships a
  change worth marking.

## Why

`0046`'s own tradeoffs section already named this as an option ("Tag to match `plugin.json`'s
current `0.10.0`") and rejected it, reasoning that a repo-level tag and a per-plugin manifest
version track different things and would stop being simple the moment this repo ships more than
one plugin. That reasoning holds in the abstract, but the direct choice made afterward was to
value the simpler, single-number scheme now over guarding against a multi-plugin future that
hasn't materialized — this repo ships exactly one plugin today, and a second tag sequence adds a
number to track for a distinction with no current referent. If a second plugin or a repo-level
release ever needs its own marker independent of any one plugin's version, that's a decision to
make *then*, against a concrete need, not one to pre-empt now.

## Tradeoffs considered

- **Keep `0046`'s independent sequence starting at `0.1.0`**: the more future-proof option if
  this repo ever ships a second plugin or a repo-level release distinct from `kms`'s own
  version. Rejected — no such need exists today, and carrying two numbers for a distinction
  that isn't real yet is exactly the "tracked noise" `docs/decisions/0037-plans-not-a-governed-artifact-type.md`
  warns against for ungrounded governance machinery.
- **Chosen**: one number — git tags mirror `plugin.json`'s version exactly.
