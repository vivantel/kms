# Installing Vivantel KMS

`kms`'s skill content is agent-neutral, but each agent's own install
mechanism differs. Pick yours:

- [Claude Code](#claude-code)
- [Codex](#codex)
- [Kilo Code CLI](#kilo-code-cli)

## Claude Code

Add this repo as a marketplace source, then install the `kms` plugin:

```
/plugin marketplace add vivantel/kms
/plugin install kms
```

If that plugin name doesn't resolve (e.g. you have another marketplace
with a same-named plugin), run `/plugin marketplace list` to find this
marketplace's registered name and install as `kms@<that-name>` instead.

## Codex

Codex ships the same skill set via the plugin manifest at
[`plugins/kms/.codex-plugin/plugin.json`](plugins/kms/.codex-plugin/plugin.json).

The exact end-user install command isn't confirmed. Codex's own docs
describe an interactive `codex /plugins` browser (browse/install from
configured marketplace sources), with no documented git-URL or
local-path syntax for adding a custom source as an end user — see
[`docs/facts/0003-codex-plugin-manifest-schema.md`](docs/facts/0003-codex-plugin-manifest-schema.md)
for exactly what is and isn't verified about Codex's plugin system.

## Kilo Code CLI

Track this skill set with no per-project copying by adding to your
`kilo.jsonc`:

```json
{ "skills": { "urls": ["https://raw.githubusercontent.com/vivantel/kms/master/plugins/kms/skills"] } }
```

Kilo re-fetches automatically whenever a skill's version changes — see
[`plugins/kms/skills/index.json`](plugins/kms/skills/index.json) and
[`docs/facts/0008-kilo-code-skills-spec.md`](docs/facts/0008-kilo-code-skills-spec.md).
