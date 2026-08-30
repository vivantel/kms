# Vivantel KMS

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-5A32FB.svg)](https://code.claude.com/docs/en/plugins.md)

Vivantel KMS (Knowledge Management System) — for any git-based
project, capture decisions, facts, and guardrails as durable, traceable artifacts,
maintained automatically as the project evolves. Works for software
repos, technical documentation, even long-form writing like research
papers, not just code.

The skill content itself is agent-neutral — no product-specific language
or tooling assumptions — so any AI coding agent that can read and follow
instructions from a file can use it. `kms` additionally ships one-command
install packaging for three: a Claude Code plugin marketplace, a native
Codex plugin, and a self-hosted remote-skills manifest for Kilo Code CLI.

| Skill | What it does | Examples |
|---|---|---|
| `quickstart` | Sets up the knowledge system and captures one real decision live, in the same sitting — for a first-time user. | [examples](plugins/kms/skills/quickstart/examples.md) |
| `brainstorm` | Generates and synthesizes distinct approaches to a problem or feature — writes nothing, never consults the knowledge base. | [examples](plugins/kms/skills/brainstorm/examples.md) |
| `clarify` | Interviews you relentlessly about a plan, decision, or idea until reaching shared understanding — writes nothing. | [examples](plugins/kms/skills/clarify/examples.md) |
| `roadmap` | Runs the same interview, then captures the outcome as durable knowledge artifacts (facts, decisions, guardrails, skill prescriptions) plus a self-sufficient implementation plan. | [examples](plugins/kms/skills/roadmap/examples.md) |
| `bootstrap` | One-time setup of a fact/decision/guardrail/skill knowledge system in a project that has none yet, or a gap-fill pass over an incomplete one. | [examples](plugins/kms/skills/bootstrap/examples.md) |
| `capture` | Turns a work session's output into decisions and facts: new decisions, changed facts, contradictions, doc drift. | [examples](plugins/kms/skills/capture/examples.md) |
| `lint` | Full-repo validation on demand — dangling references, missing fields, expired decisions, stale derived artifacts — independent of what changed this session. | [examples](plugins/kms/skills/lint/examples.md) |
| `query` | Answers a question from the knowledge base, with citations, instead of from memory. | [examples](plugins/kms/skills/query/examples.md) |
| `onboard` | Reads the knowledge base to produce a role-tailored, 5-day onboarding plan — writes nothing. | [examples](plugins/kms/skills/onboard/examples.md) |
| `refactor-plan` | Produces a phased refactor plan that respects existing decisions and guardrails — writes nothing. | [examples](plugins/kms/skills/refactor-plan/examples.md) |
| `conform` | Checks whether a pending changeset conforms to existing decisions and guardrails before it lands. | [examples](plugins/kms/skills/conform/examples.md) |
| `attribute` | Writes commit messages and PR descriptions that lead with intent, not just what changed, and keeps them traceable to the knowledge artifacts they implement. | [examples](plugins/kms/skills/attribute/examples.md) |
| `changelog` | Generates a `CHANGELOG.md` entry from commit history on demand. | [examples](plugins/kms/skills/changelog/examples.md) |
| `uninstall` | Finds everything `bootstrap`/`capture` added and offers to detach or remove it — run manually before uninstalling the plugin. | [examples](plugins/kms/skills/uninstall/examples.md) |

## Installing

Add this repo as a marketplace source, then install the `kms` plugin:

```
/plugin marketplace add vivantel/kms
/plugin install kms
```

If that plugin name doesn't resolve (e.g. you have another marketplace
with a same-named plugin), run `/plugin marketplace list` to find this
marketplace's registered name and install as `kms@<that-name>` instead.

Codex ships the same skill set via the plugin manifest at
`plugins/kms/.codex-plugin/plugin.json`. The exact end-user install
command isn't confirmed (Codex's own docs describe an interactive
`codex /plugins` browser, with no documented git-URL/local-path syntax
for adding a custom source) — see
`docs/facts/0003-codex-plugin-manifest-schema.md` for what is and isn't
verified.

Kilo Code CLI users can track this skill set with no per-project
copying by adding to `kilo.jsonc`:

```json
{ "skills": { "urls": ["https://raw.githubusercontent.com/vivantel/kms/master/plugins/kms/skills"] } }
```

Kilo re-fetches automatically whenever a skill's version changes — see
`plugins/kms/skills/index.json`.

## Repo structure

```
.claude-plugin/marketplace.json                     # marketplace manifest
plugins/kms/.claude-plugin/plugin.json               # Claude Code plugin manifest
plugins/kms/.codex-plugin/plugin.json                # Codex plugin manifest
plugins/kms/skills/index.json                        # Kilo Code CLI remote-skills manifest
plugins/kms/skills/<skill>/SKILL.md                  # one skill definition per subdirectory
docs/{facts,decisions,guardrails,skills}/            # this repo's own knowledge base — see below
```

## This repo dogfoods its own skills

`kms`'s design rationale — why each skill works the way it does, what
must or must not happen, and what's currently true about the repo — is
recorded as knowledge artifacts under `docs/`, maintained with the same
`bootstrap`/`capture` skills this plugin ships, and checkable with the
same `lint`/`query` skills too. See [`AGENTS.md`](AGENTS.md) for the
full structure and conventions.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). This project follows the
[Contributor Covenant](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)
