# kms

A knowledge-management system for any codebase — capture decisions,
facts, and guardrails as durable, traceable artifacts, maintained
automatically as your project evolves. Works for any git-based project
where decisions and facts are worth tracking durably — software repos,
technical documentation, even long-form writing like research papers,
not just code.

A curated marketplace of Claude Code plugins for everyday development
workflows. The `kms` plugin bundles six knowledge-management skills:

| Skill | What it does |
|---|---|
| `clarify` | Interviews you relentlessly about a plan, decision, or idea until reaching shared understanding — writes nothing. |
| `roadmap` | Runs the same interview, then captures the outcome as durable knowledge artifacts (facts, decisions, guardrails, skill prescriptions) plus a self-sufficient implementation plan. |
| `bootstrap` | One-time setup of a fact/decision/guardrail/skill knowledge system in a project that has none yet, or a gap-fill pass over an incomplete one. |
| `steward` | The ongoing, session-to-session maintenance pass for that system: new decisions, changed facts, contradictions, doc drift, stale guardrails. |
| `attribute` | Writes commit messages and PR descriptions that lead with intent, not just what changed, and keeps them traceable to the knowledge artifacts they implement. |
| `changelog` | Generates a `CHANGELOG.md` entry from commit history on demand. |

## Installing

Add this repo as a marketplace source, then install the `kms` plugin:

```
/plugin marketplace add vivantel/kms
/plugin install kms
```

If that plugin name doesn't resolve (e.g. you have another marketplace
with a same-named plugin), run `/plugin marketplace list` to find this
marketplace's registered name and install as `kms@<that-name>` instead.

Codex users can install the same skill set via the plugin manifest at
`plugins/kms/.codex-plugin/plugin.json`.

## Repo structure

```
.claude-plugin/marketplace.json                     # marketplace manifest
plugins/kms/.claude-plugin/plugin.json               # Claude Code plugin manifest
plugins/kms/.codex-plugin/plugin.json                # Codex plugin manifest
plugins/kms/skills/<skill>/SKILL.md                  # one skill definition per subdirectory
docs/{facts,decisions,guardrails,skills}/            # this repo's own knowledge base — see below
```

## This repo dogfoods its own skills

`kms`'s design rationale — why each skill works the way it does, what
must or must not happen, and what's currently true about the repo — is
recorded as knowledge artifacts under `docs/`, maintained with the same
`bootstrap`/`steward` skills this plugin ships. See
[`AGENTS.md`](AGENTS.md) for the full structure and conventions.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). This project follows the
[Contributor Covenant](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)
