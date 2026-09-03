---
id: 0008-native-codex-plugin-support
title: Ship a native Codex plugin manifest for the kms skill set; keep the current directory layout; defer Cursor
status: active
date: 2026-07-29
tags: [kms, agent-agnostic, codex, packaging]
track: product
---

## Decision

This repo will ship a native Codex plugin manifest,
`plugins/kms/.codex-plugin/plugin.json`, alongside the existing
`plugins/kms/.claude-plugin/plugin.json`, exposing the same four skills
to Codex. This revises the "packaging stays Claude-Code-specific" part of
`docs/decisions/0006-agent-agnostic-scope.md`, which is now superseded by
this record. `0006`'s other conclusion — skill *content* must stay
agent-neutral — is untouched and still governs via
`docs/guardrails/agent-agnostic-skill-content.md`.

Specifically:

- **No directory restructuring.** `plugins/kms/skills/` stays exactly
  where it is. `plugins/kms/.codex-plugin/plugin.json` sits alongside
  `plugins/kms/.claude-plugin/plugin.json` in the same plugin root, with
  `"skills": "./skills"` — a single relative path, which is all Codex's
  manifest format accepts (see
  `docs/facts/0003-codex-plugin-manifest-schema.md`). Because this repo's
  `plugins/kms/skills/` already contains only the four public skills with
  no private/deprecated buckets mixed in, the single-path constraint that
  can force other repos with mixed public/private skill directories to
  *defer* Codex support doesn't apply here.
- **No symlinks.** Codex is documented to drop symlinks when it
  installs/caches a plugin tree, which would ship empty skill
  directories. Not a concern for us since we're not using symlinks for
  this — the Codex manifest points directly at the real
  `plugins/kms/skills/` directory.
- **`plugins/kms/.claude-plugin/plugin.json`'s `description` field is
  reworded** to drop "for Claude Code," since that's no longer accurate
  once a Codex manifest ships for the same skills.
- **Per-skill `agents/openai.yaml` sidecars are added now** (one per
  skill, under each skill's own directory, e.g.
  `plugins/kms/skills/clarify/agents/openai.yaml`).
  Each declares `interface.display_name`, `interface.short_description`,
  and `policy.allow_implicit_invocation: false` — consistent with this
  repo's existing convention that all four skills are explicit-invocation-
  only (already stated outright for `attribute`/`changelog`; extended here
  to `clarify`/`roadmap` too, since none of the four skills are designed
  to fire without being asked).
- **Cursor support is explicitly deferred**, per the earlier interview
  decision to land Codex first (Codex is documented, drop-in, and
  structurally free for us; Cursor has no equivalent auto-skill format and
  would need real content translation into `.cursor/commands/*.md`,
  which is a separate design problem).
- **A Codex marketplace/registry manifest is deferred.** Local-path and
  git-URL plugin installs don't require one, so it isn't a blocker for
  shipping or testing the plugin manifest itself. See
  `docs/facts/0003-codex-plugin-manifest-schema.md` for why its exact path
  wasn't confirmed with enough confidence to commit to here.
- **Testing is scoped to static schema validation** (valid JSON, required
  fields present, matches the documented shape) rather than a live
  `codex plugin install` — the Codex CLI isn't available in this dev
  environment. A real install/load test is left as an explicit follow-up
  in `docs/plans/codex-plugin-support.md`, not claimed as done here.

## Why

The original `0006` decision to keep packaging Claude-Code-specific was
made without knowing Codex uses the *same* `SKILL.md` format and reads
`AGENTS.md` — once that was confirmed (via primary OpenAI docs, not the
initial low-trust SEO search results), the cost of adding Codex support
dropped from "a second packaging system" to "one more manifest file
pointing at content we already have." That changes the calculus enough
to revisit the scope decision rather than let it stand as stale.

## Tradeoffs considered

- **Flatten to a top-level `skills/` layout**: rejected — that pattern
  exists to solve a *curation* problem (excluding private/deprecated
  skills from a single-path manifest) that this repo doesn't have.
  Flattening here would cost a large blast radius (marketplace.json, both
  plugin.json files,
  AGENTS.md, every skill path) for no corresponding benefit, and would
  abandon this repo's multi-plugin-marketplace design
  (`docs/decisions/0001-knowledge-artifact-storage-convention.md`'s
  sibling intent — `marketplace.json` supporting more than one plugin).
- **Both Codex and Cursor now**: rejected in the interview — Cursor
  requires lossy content translation into a different command format,
  which is a genuinely different design problem deserving its own scoped
  decision rather than being bundled in under time pressure.
- **Skip per-skill `agents/*.yaml` for now**: considered, but the user
  chose to establish the pattern upfront even without a concrete
  behavioral difference to encode yet, so future per-agent tuning has a
  place to go without a structural change.
