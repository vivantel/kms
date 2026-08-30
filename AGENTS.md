# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## What this repo is

This repo is a **Claude Code plugin marketplace**: a git repo that Claude Code can add as a marketplace source, from which users install plugins that bundle skills. There is no build step and no test/lint tooling — the repo is almost entirely JSON manifests and Markdown skill definitions, plus one small POSIX shell script (`plugins/kms/hooks/capture-nudge.sh`) backing a Claude Code plugin hook. See `docs/skills/kms-architecture.md` for how the layers and marker conventions below fit together.

## Structure

```
.claude-plugin/marketplace.json                     # marketplace manifest — lists available plugins
INSTALLING.md                                        # per-agent install steps, one section per agent, linked from README
kilo.jsonc                                           # Kilo Code CLI config, points skills.urls at the published plugins/kms/skills/index.json (see docs/decisions/0035-native-kilo-code-support.md)
plugins/<plugin-name>/.claude-plugin/plugin.json     # Claude Code plugin manifest (name, description, version, author)
plugins/<plugin-name>/.codex-plugin/plugin.json      # Codex plugin manifest (name, version, description, skills path)
plugins/<plugin-name>/skills/<skill>/SKILL.md        # one skill definition per subdirectory
plugins/<plugin-name>/skills/<skill>/examples.md     # 2-3 worked usage examples, linked from the README
plugins/<plugin-name>/skills/index.json              # Kilo Code CLI remote-skills manifest (see docs/facts/0008-kilo-code-skills-spec.md)
plugins/<plugin-name>/skills/<skill>/agents/<agent>.yaml  # optional per-agent interface/policy overrides (e.g. agents/openai.yaml)
plugins/<plugin-name>/hooks/hooks.json               # optional Claude Code plugin hooks, auto-activated on install (see docs/facts/0006-claude-code-plugin-hooks-mechanism.md)
plugins/<plugin-name>/templates/<artifact-type>/     # shippable seed content, synced into an adopting project by bootstrap/capture/lint — distinct from this repo's own docs/ (see docs/decisions/0027-baseline-guardrail-seeding.md)
                                                      # in an adopting project: kms-generated: true marks a bootstrap-constructed (non-template) file; <!-- kms:start -->/<!-- kms:end --> marks its AGENTS.md section — both removable via uninstall (see docs/decisions/0029-bootstrap-full-traceability.md)
plugins/<plugin-name>/shared/<topic>.md              # content read by sibling reference from more than one skill body (e.g. artifact-model.md, read by bootstrap and capture) — for identical, same-voice content only (see docs/decisions/0034-shared-artifact-model.md)
```

Currently there is one plugin, `kms` (source `./plugins/kms`), containing fourteen skills: `quickstart` (`plugins/kms/skills/quickstart/SKILL.md`), which runs `bootstrap` then captures one real decision live for a first-time user; `brainstorm` (`plugins/kms/skills/brainstorm/SKILL.md`), which generates and synthesizes distinct approaches to a problem without writing anything or consulting the knowledge base; `clarify` (`plugins/kms/skills/clarify/SKILL.md`), which interrogates the user to clarify a plan without writing anything; `roadmap` (`plugins/kms/skills/roadmap/SKILL.md`), which runs the same kind of interrogation but then writes durable knowledge-management artifacts and a standalone implementation roadmap; `bootstrap` (`plugins/kms/skills/bootstrap/SKILL.md`), which does the one-time setup of a project's fact/decision/guardrail/skill system (or gap-fills an incomplete one); `capture` (`plugins/kms/skills/capture/SKILL.md`), which turns a work session's output into decisions and facts — new decisions, changed facts, contradictions, doc drift; `lint` (`plugins/kms/skills/lint/SKILL.md`), which validates the whole knowledge base on demand, independent of any one session, and owns every check not genuinely session-scoped; `query` (`plugins/kms/skills/query/SKILL.md`), which answers a question from the knowledge base with citations; `onboard` (`plugins/kms/skills/onboard/SKILL.md`), which reads the knowledge base to produce a role-tailored onboarding plan without writing anything; `refactor-plan` (`plugins/kms/skills/refactor-plan/SKILL.md`), which produces a phased refactor plan that respects existing decisions and guardrails, without writing anything; `conform` (`plugins/kms/skills/conform/SKILL.md`), which checks whether a pending changeset conforms to existing decisions and guardrails before it lands; `attribute` (`plugins/kms/skills/attribute/SKILL.md`), which writes intent-first commit messages and PR descriptions traceable to those knowledge artifacts; `changelog` (`plugins/kms/skills/changelog/SKILL.md`), which renders a `CHANGELOG.md` entry from commit history on demand; and `uninstall` (`plugins/kms/skills/uninstall/SKILL.md`), which finds and offers to detach or remove everything `bootstrap`/`capture` added to a project, run manually before actually uninstalling the plugin.

- `.claude-plugin/marketplace.json`'s top-level `plugins` array is the registry: each entry needs `name` and `source`. For plugins living in this same repo, `source` must be a relative path starting with `./` (e.g. `"./plugins/kms"`), resolved from the repo root (the directory containing `.claude-plugin/`).
- The Claude Code plugin manifest (`plugin.json`) must live inside a `.claude-plugin/` subdirectory under the plugin root — a `plugin.json` at the plugin root directly is not recognized.
- The `kms` plugin also ships a Codex plugin manifest at `plugins/kms/.codex-plugin/plugin.json`, pointing at the same `plugins/kms/skills/` directory via a single relative `skills` path (Codex's manifest format accepts a path string, not an array — see `docs/facts/0003-codex-plugin-manifest-schema.md`). Any manifest's `version` field must be bumped in lockstep with every other manifest's, per `docs/guardrails/plugin-manifest-version-sync.md`.
- Kilo Code CLI needs no manifest at all — it reads `SKILL.md` folders directly in the same open Agent Skills format. `plugins/kms/skills/index.json` is a remote-skills manifest for Kilo's `skills.urls` config mechanism, letting Kilo users track this repo without copying files into their own project (see `docs/facts/0008-kilo-code-skills-spec.md`, `docs/decisions/0035-native-kilo-code-support.md`).
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

Also add a colocated `plugins/<plugin-name>/skills/<skill-name>/examples.md` with 2-3 worked usage examples (a realistic trigger prompt plus a sketch of the resulting interaction or output), and link it from the README's skill table — required for every skill per `docs/guardrails/every-skill-ships-examples.md`.

Keep the `SKILL.md` body itself as short as possible while preserving meaning — it's loaded into every invocation's context, per `docs/guardrails/token-economy.md`. This is about `kms`'s own skill bodies specifically; it's not something `lint`/`capture` check (their scope is a project's own `docs/{facts,guardrails,skills}/`, not `kms`'s packaging layer). See `docs/skills/scoping-shipped-vs-repo-rules.md` before adding any new rule that could plausibly belong in a shipped skill's checks — most don't.

## Adding a new plugin

1. Create `plugins/<new-plugin-name>/.claude-plugin/plugin.json` with `name`, `description`, `version`, and `author`.
2. Add a corresponding entry (`name`, `description`, `source: "./plugins/<new-plugin-name>"`) to the `plugins` array in `.claude-plugin/marketplace.json`.

## Validation

There are no automated checks. When editing manifests, verify JSON validity manually (e.g. `python3 -m json.tool <file>` or `jq . <file>`) and confirm each `SKILL.md` has well-formed frontmatter.
