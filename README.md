# Vivantel KMS

*Give your AI coding agent durable, checkable knowledge — decisions,
facts, and guardrails it won't forget, contradict, or re-litigate.*

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-5A32FB.svg)](https://code.claude.com/docs/en/plugins.md)

## What it looks like

Without `kms`, an agent re-proposes what you already rejected:

```
you:    add a Redis cache in front of the orders API
agent:  Sure — I'll add Redis.
```

With `kms` (illustrative output), the rejection is a recorded decision. `bootstrap` adds a line to your `AGENTS.md` telling the agent to `query` before designing anything that touches one, so it finds it first:

```
you:    add a Redis cache in front of the orders API
agent:  Not yet: decision 0012 (2026-09-03) rejects a cache layer until p95 > 400 ms,
        and guardrail `no-unbounded-caches` derives from it. Current p95 (fact 0007): 210 ms.
        Refs: 0012-no-cache-until-slo-breach, no-unbounded-caches, 0007-orders-p95
```

Measured, not just claimed: on 2026-11-22 an agent running `nvidia/nemotron-3.5-super-vl:free` through Kilo flagged the planted rejected option in 8 of 8 runs (two phrasings) and let an unrelated change through in 4 of 4 ([`evals/rejected-option`](evals/rejected-option)). One run of a small fixture; read it as a smoke test.

That is the whole idea: four typed artifacts — **facts** (what is true now), **decisions** (what you committed to and why), **guardrails** (what must or must not happen, derived from the first two) and **procedures** (how to act) — plain Markdown in `docs/`, checked by a script, so knowledge stays durable instead of a half-remembered guess. [The full case →](https://medium.com/@strebulaev/taxonomy-is-a-language-why-your-ai-agent-needs-a-vocabulary-not-more-memory-000b8023a40a)

## Start here

```
/plugin marketplace add vivantel/kms
/plugin install kms
```

then ask your agent: **"get me started with kms"** (the `quickstart` skill). In one sitting it sets up `docs/`, then interviews you about one decision you are actually facing and writes it down. Every other skill is optional afterwards. Other agents (Codex, Kilo Code CLI): [`INSTALLING.md`](INSTALLING.md).

What stays manual: `capture` (after a work session), `lint` (whenever you want the whole base checked) and `conform` (before committing) run when you or your agent's instructions call for them. On Claude Code, two session-start hooks nudge you; on Codex and Kilo there is no automatic nudge, see [`docs/skills/automating-capture.md`](docs/skills/automating-capture.md).

Works for any git-based project — software, technical documentation, even long-form writing — not just code. The skill content is agent-neutral, so any agent that can follow instructions from a file can use it; `kms` ships one-command packaging for Claude Code, Codex and Kilo Code CLI.

## Words you will see

- **Fact**: something true now (a version, a limit, a behavior); it changes when reality changes.
- **Decision**: a choice you committed to, with the reason and the options you rejected.
- **Guardrail**: a rule (must / must not) that follows from a decision or fact and says how it is enforced.
- **Procedure**: how to act in a recurring situation; lives in `docs/skills/`, not to be confused with an agent skill.
- **Skill** (agent skill): one of this plugin's instruction files, such as `capture`; the thing you invoke.
- **Fitness function**: an automated check (a test, a lint rule, a CI job) that enforces a guardrail.
- **Derivation**: the link from a guardrail back to the decision or fact it comes from.
- **Admission test**: the check a new artifact must pass before it is written, so it adds something not already recorded.
- **Tag / umbrella tag**: a label from `docs/tags.md`; an umbrella tag groups related tags.
- **Schema version**: the format of the artifacts (currently `1.0.0`); it stays stable, so existing knowledge bases keep working.

## Skills

| Skill | What it does | Examples |
|---|---|---|
| `quickstart` | Sets up the knowledge system and captures one real decision live, in the same sitting — for a first-time user. | [examples](plugins/kms/skills/quickstart/examples.md) |
| `decide` | Interviews you about a decision, then writes the outcome as durable knowledge artifacts (facts, decisions, guardrails, procedures) — records only, no plan file. | [examples](plugins/kms/skills/decide/examples.md) |
| `bootstrap` | One-time setup of a fact/decision/guardrail/procedure knowledge system in a project that has none yet, or a gap-fill pass over an incomplete one. | [examples](plugins/kms/skills/bootstrap/examples.md) |
| `capture` | Turns a work session's output into decisions and facts: new decisions, changed facts, contradictions, doc drift. | [examples](plugins/kms/skills/capture/examples.md) |
| `lint` | Full-repo validation on demand — dangling references, missing fields, expired decisions, stale derived artifacts — independent of what changed this session. | [examples](plugins/kms/skills/lint/examples.md) |
| `query` | Answers a question from the knowledge base, with citations, instead of from memory. | [examples](plugins/kms/skills/query/examples.md) |
| `onboard` | Reads the knowledge base to produce a role-tailored, 5-day onboarding plan — writes nothing. | [examples](plugins/kms/skills/onboard/examples.md) |
| `conform` | Checks whether a pending changeset conforms to existing decisions and guardrails before it lands. | [examples](plugins/kms/skills/conform/examples.md) |
| `attribute` | Writes commit messages and PR descriptions that lead with intent, not just what changed, and keeps them traceable to the knowledge artifacts they implement. | [examples](plugins/kms/skills/attribute/examples.md) |
| `uninstall` | Finds everything `bootstrap`/`capture` added and offers to detach or remove it — run manually before uninstalling the plugin. | [examples](plugins/kms/skills/uninstall/examples.md) |

`roadmap`, `brainstorm`, `clarify`, `refactor-plan` and `changelog` moved to go-getter in 0.17; use `decide` for records.

## The knowledge-base core

`kms` is the lightweight knowledge-base plugin and the reference implementation of a versioned core: the schema, the structural checker and the conformance fixtures, which other tools can pin without the skills (see [`docs/skills/core-contract.md`](docs/skills/core-contract.md)). It works alone. [go-getter](https://github.com/vivantel/go-getter) builds on it for coordinating humans and agents toward outcomes: it vendors the core by pinned schema version and ships no fork of it.

Scope: `kms` holds what outlives the work (facts, decisions, guardrails, procedures). Product specs stay in a spec tool such as OpenSpec; a record points at a change with `source` and does not copy it.

## Repo structure

```
.claude-plugin/marketplace.json                     # marketplace manifest
INSTALLING.md                                        # per-agent install steps (Claude Code, Codex, Kilo Code CLI)
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
