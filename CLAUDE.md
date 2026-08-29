# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## What this repo is

This repo is a **Claude Code plugin marketplace**: a git repo that Claude Code can add as a marketplace source, from which users install plugins that bundle skills. There is no application code, no build step, and no test/lint tooling — the entire repo is JSON manifests and Markdown skill definitions.

## Structure

```
.claude-plugin/marketplace.json                     # marketplace manifest — lists available plugins
plugins/<plugin-name>/.claude-plugin/plugin.json     # Claude Code plugin manifest (name, description, version, author)
plugins/<plugin-name>/.codex-plugin/plugin.json      # Codex plugin manifest (name, version, description, skills path)
plugins/<plugin-name>/skills/<skill>/SKILL.md        # one skill definition per subdirectory
plugins/<plugin-name>/skills/<skill>/agents/<agent>.yaml  # optional per-agent interface/policy overrides (e.g. agents/openai.yaml)
```

Currently there is one plugin, `kms` (source `./plugins/kms`), containing six skills: `clarify` (`plugins/kms/skills/clarify/SKILL.md`), which interrogates the user to clarify a plan without writing anything; `roadmap` (`plugins/kms/skills/roadmap/SKILL.md`), which runs the same kind of interrogation but then writes durable knowledge-management artifacts and a standalone implementation roadmap; `bootstrap` (`plugins/kms/skills/bootstrap/SKILL.md`), which does the one-time setup of a project's fact/decision/guardrail/skill system (or gap-fills an incomplete one); `steward` (`plugins/kms/skills/steward/SKILL.md`), which maintains that system session to session — new decisions, stale facts, contradictions, doc drift, and re-derived guardrails; `attribute` (`plugins/kms/skills/attribute/SKILL.md`), which writes intent-first commit messages and PR descriptions traceable to those knowledge artifacts; and `changelog` (`plugins/kms/skills/changelog/SKILL.md`), which renders a `CHANGELOG.md` entry from commit history on demand.

- `.claude-plugin/marketplace.json`'s top-level `plugins` array is the registry: each entry needs `name` and `source`. For plugins living in this same repo, `source` must be a relative path starting with `./` (e.g. `"./plugins/kms"`), resolved from the repo root (the directory containing `.claude-plugin/`).
- The Claude Code plugin manifest (`plugin.json`) must live inside a `.claude-plugin/` subdirectory under the plugin root — a `plugin.json` at the plugin root directly is not recognized.
- The `kms` plugin also ships a Codex plugin manifest at `plugins/kms/.codex-plugin/plugin.json`, pointing at the same `plugins/kms/skills/` directory via a single relative `skills` path (Codex's manifest format accepts a path string, not an array — see `docs/facts/0003-codex-plugin-manifest-schema.md`). Any manifest's `version` field must be bumped in lockstep with every other manifest's, per `docs/guardrails/plugin-manifest-version-sync.md`.
- A plugin's `skills/` directory is scanned for subdirectories containing a `SKILL.md`; there is no separate per-skill registration file. A skill directory may optionally include `agents/<agent-name>.yaml` sidecars for per-agent interface/policy overrides (e.g. `agents/openai.yaml`); see `docs/skills/adding-agent-support.md` for when to add one.

## Adding a new skill

Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: One-line description, including trigger phrases for when it should be used.
---
```

Followed by the skill's instructions in the body. See `plugins/kms/skills/clarify/SKILL.md` for the pattern — it defines an interview-style skill with explicit turn-taking rules (ask one question at a time, prefer looking up facts over asking, only ask about genuine decisions).

## Adding a new plugin

1. Create `plugins/<new-plugin-name>/.claude-plugin/plugin.json` with `name`, `description`, `version`, and `author`.
2. Add a corresponding entry (`name`, `description`, `source: "./plugins/<new-plugin-name>"`) to the `plugins` array in `.claude-plugin/marketplace.json`.

## Validation

There are no automated checks. When editing manifests, verify JSON validity manually (e.g. `python3 -m json.tool <file>` or `jq . <file>`) and confirm each `SKILL.md` has well-formed frontmatter.
