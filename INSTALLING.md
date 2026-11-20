# Installing Vivantel KMS

`kms`'s skill content is agent-neutral, but each agent's own install
mechanism differs. Pick yours:

- [Claude Code](#claude-code)
- [Codex](#codex)
- [Kilo Code CLI](#kilo-code-cli)

`kms` works alone. To coordinate humans and agents on top of it, see [go-getter](https://github.com/vivantel/go-getter), which pins the same knowledge-base core ([contract](docs/skills/core-contract.md)).

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

Add this repo as a marketplace source, then install the plugin
(verified 2026-11-20 with `codex-cli 0.166.0`):

```
codex plugin marketplace add vivantel/kms
codex plugin add kms@kms
```

Codex copies the whole plugin root, so the skills, `shared/` and
`templates/` arrive together. See
[`docs/facts/0003-codex-plugin-manifest-schema.md`](docs/facts/0003-codex-plugin-manifest-schema.md)
for what was and was not tested (the `owner/repo` form and hook execution
are untested; a local checkout path was tested).

## Kilo Code CLI

Track this skill set with no per-project copying by adding to your
`kilo.jsonc`:

```json
{ "skills": { "urls": ["https://raw.githubusercontent.com/vivantel/kms/master/plugins/kms/skills"] } }
```

Kilo re-fetches automatically whenever a skill's version changes — see
[`plugins/kms/skills/index.json`](plugins/kms/skills/index.json) and
[`docs/facts/0008-kilo-code-skills-spec.md`](docs/facts/0008-kilo-code-skills-spec.md).

## What each agent receives

- **Claude Code** installs the whole plugin: skills, `shared/` (schema, writing guide, checker, migration script), `templates/` and the two `SessionStart` nudge hooks.
- **Codex** installs the whole plugin root: skills, `shared/` and `templates/` arrive (tested 2026-11-20). Whether it runs the nudge hooks is untested; use the recipe by hand (`docs/skills/automating-capture.md`).
- **Kilo Code CLI** fetches only what `plugins/kms/skills/index.json` lists: `SKILL.md` and `examples.md` per skill. `shared/` and `templates/` are not delivered through the remote-skills channel, so skills that read them (`bootstrap`, `capture`, `lint`, `uninstall`, `decide`) need a checkout of this repo or the files copied beside the skills. No hooks.
- **`lint`'s checker** needs `python3` plus PyYAML on every agent.
