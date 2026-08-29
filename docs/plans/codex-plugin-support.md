---
id: codex-plugin-support
title: Ship a native Codex plugin manifest for the kms skill set
status: steps 1-4 done; step 5 blocked (needs Codex CLI)
date: 2026-07-29
---

# Ship a native Codex plugin manifest for the kms skill set

## Context for a fresh session

This repo (`/home/ubuntu/projects/sergemso/dev_skills`) is a Claude Code
plugin marketplace containing one plugin, `kms`
(`plugins/kms/.claude-plugin/plugin.json`, currently version `2.1.0`),
with four skills under `plugins/kms/skills/{clarify,roadmap,attribute,changelog}/`.

A `roadmap`-skill interview (2026-07-29) reopened an earlier decision
(`docs/decisions/0006-agent-agnostic-scope.md`, now superseded) after
discovering — via OpenAI's own developer docs, not search-engine
summaries — that Codex CLI reads the same `AGENTS.md` file this repo
already has and uses the same `SKILL.md` skill format this repo already
uses. The revised decision,
`docs/decisions/0008-native-codex-plugin-support.md`, is to ship a native
Codex plugin manifest for the existing skills with **no directory
restructuring and no symlinks** — full reasoning and rejected
alternatives are in that file. The manifest schema itself is recorded in
`docs/facts/0003-codex-plugin-manifest-schema.md`.

This plan file is what turns that decision into actual files. A cold
session should be able to execute every step below by reading only this
file plus the two artifacts above — no other prior context required.
**Nothing below has been executed yet.** Writing this plan (and the five
other knowledge artifacts from the same interview —
`docs/decisions/0008-native-codex-plugin-support.md`,
`docs/facts/0003-codex-plugin-manifest-schema.md`,
`docs/guardrails/plugin-manifest-version-sync.md`,
`docs/skills/adding-agent-support.md`, and the edit to
`docs/decisions/0006-agent-agnostic-scope.md`) was the `roadmap` skill's
deliverable; running it is a separate, later action, per that skill's
own hard limit ("never execute the changeset plan yourself").

## Steps

### 1. [done] Create `plugins/kms/.codex-plugin/plugin.json`

Create the directory `plugins/kms/.codex-plugin/` and a `plugin.json`
inside it:

```json
{
  "name": "kms",
  "version": "2.1.0",
  "description": "A growing toolkit of everyday development skills.",
  "skills": "./skills"
}
```

`version` mirrors `plugins/kms/.claude-plugin/plugin.json`'s current
value (`2.1.0`) — this is a new distribution channel for the same,
unchanged skill set, not a skill-content change, so no version bump is
warranted on its own. `skills` is `"./skills"`, relative to this
manifest's own directory (`plugins/kms/`), pointing at the existing
`plugins/kms/skills/` directory — per
`docs/facts/0003-codex-plugin-manifest-schema.md`, Codex discovers
`SKILL.md` files recursively under that one path, so all four existing
skills are picked up with zero changes to them.

**Done when**: the file exists, is valid JSON
(`python3 -m json.tool plugins/kms/.codex-plugin/plugin.json`), and has
exactly the fields shown above (`name`, `version`, `description`,
`skills` — no more, no less, unless a later step in this same plan adds
one deliberately).

### 2. [done] Reword `plugins/kms/.claude-plugin/plugin.json`'s description

Current value: `"description": "A growing toolkit of everyday
development skills for Claude Code."` — change to `"A growing toolkit of
everyday development skills."` (drop the trailing "for Claude Code"),
since that claim becomes inaccurate once step 1 ships a Codex manifest
for the same skills. Leave every other field in this file unchanged.

**Done when**: `plugins/kms/.claude-plugin/plugin.json`'s `description`
field no longer mentions Claude Code, the file is still valid JSON, and
no other field changed.

### 3. [done] Add `agents/openai.yaml` sidecars for all four skills

For each of `clarify`, `roadmap`, `attribute`, `changelog`, create
`plugins/kms/skills/<name>/agents/openai.yaml` with this shape:

```yaml
interface:
  display_name: "<Title Case skill name>"
  short_description: "<short description>"
policy:
  allow_implicit_invocation: false
```

Use these exact values (derived from each skill's existing `SKILL.md`
frontmatter `description`, condensed):

- `plugins/kms/skills/clarify/agents/openai.yaml`:
  `display_name: "Clarify"`,
  `short_description: "Interview to stress-test a plan or decision"`
- `plugins/kms/skills/roadmap/agents/openai.yaml`:
  `display_name: "Roadmap"`,
  `short_description: "Turn a decision into durable knowledge artifacts and a plan"`
- `plugins/kms/skills/attribute/agents/openai.yaml`:
  `display_name: "Attribute"`,
  `short_description: "Write intent-first commit messages and PR descriptions"`
- `plugins/kms/skills/changelog/agents/openai.yaml`:
  `display_name: "Changelog"`,
  `short_description: "Generate a CHANGELOG.md entry from commit history"`

All four get `allow_implicit_invocation: false` — per
`docs/decisions/0008-native-codex-plugin-support.md`, none of these
skills are designed to fire without being explicitly asked.

**Done when**: all four `agents/openai.yaml` files exist with the values
above, and each is valid YAML (e.g.
`python3 -c "import yaml; yaml.safe_load(open('plugins/kms/skills/clarify/agents/openai.yaml'))"`
per file, or equivalent).

### 4. [done] Static schema validation (the only testing this plan performs)

The Codex CLI is not available in this dev environment as of 2026-07-29
(`which codex` / `codex --version` both fail), so this plan cannot run a
real `codex plugin install`/load test. Do not claim one happened.
Instead: confirm `plugins/kms/.codex-plugin/plugin.json` is valid JSON
and contains exactly the required fields (`name`, `version`,
`description`) plus `skills`, per
`docs/facts/0003-codex-plugin-manifest-schema.md`'s documented schema.

**Done when**: the JSON-validity check from step 1 passes, and the field
set has been manually compared against
`docs/facts/0003-codex-plugin-manifest-schema.md`'s "Required fields" /
"Optional fields" lists with no mismatch.

### 5. [blocked: needs an environment with Codex CLI installed] Real install/load test

Once a session has the Codex CLI available, install this plugin from a
local path and confirm all four skills are discovered (e.g. list
available skills/commands and check `clarify`, `roadmap`, `attribute`,
`changelog` all appear). If they don't, revisit
`docs/decisions/0008-native-codex-plugin-support.md` — don't silently
patch around a discovery failure without updating that decision record.

**Done when**: a real Codex CLI session confirms all four skills are
discovered from this plugin.

## Explicitly out of scope for this plan

- A Codex marketplace/registry manifest — deferred per
  `docs/decisions/0008-native-codex-plugin-support.md` (path not
  confirmed with confidence; not required for local-path/git-URL
  installs).
- Any Cursor support — deferred to its own future decision, per the same
  record.
- Any restructuring of `plugins/kms/skills/` — not needed; see
  `docs/decisions/0008-native-codex-plugin-support.md`'s "Tradeoffs
  considered".
- Any change to the four `SKILL.md` bodies themselves — they're already
  agent-neutral per `docs/facts/0002-skill-bodies-already-agent-neutral.md`
  and untouched by this plan.
