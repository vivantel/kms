# Contributing

Thanks for considering a contribution to Vivantel KMS (Knowledge
Management System, package name `kms`). This repo is a Claude Code
plugin marketplace — the entire product is JSON manifests and Markdown
skill definitions under `plugins/kms/skills/`. There's no build step and
no test suite, so contributing is mostly about writing clear, well-scoped
skill instructions and manifest edits.

Please also read [`AGENTS.md`](AGENTS.md) before making changes — it
documents the repo's actual structure and conventions in more depth than
this file does, and is kept current as the source of truth.

## Before you start

Open a [discussion](../../discussions) or an issue for anything beyond a
small fix — a new skill, a change to an existing skill's behavior, or a
change to the plugin/marketplace manifests — so the direction can be
agreed before you invest time in it.

## Adding or changing a skill

- Follow the pattern in `AGENTS.md`'s "Adding a new skill" section: a
  `SKILL.md` with `name` and `description` frontmatter (the description
  should include concrete trigger phrases), under
  `plugins/kms/skills/<skill-name>/`.
- Keep skill instruction bodies agent-neutral — no naming a specific AI
  product or tool by name, no host-specific invocation syntax baked into
  the instructions (see `docs/guardrails/agent-agnostic-skill-content.md`).
- If you're adding a new skill, only add a per-agent
  `agents/<agent-name>.yaml` sidecar (see the existing skills for the
  pattern) if that agent's behavior genuinely needs to differ — not as a
  placeholder.
- Bump every plugin manifest's `version` field together
  (`plugins/kms/.claude-plugin/plugin.json` and
  `plugins/kms/.codex-plugin/plugin.json`) — see
  `docs/guardrails/plugin-manifest-version-sync.md`.
- Keep the `SKILL.md` body itself economical — see
  `docs/guardrails/token-economy.md`.

## This repo dogfoods its own skills

`kms` maintains its own design rationale as knowledge artifacts under
`docs/{facts,decisions,guardrails,skills}/` — facts (what's true now),
decisions (what the team committed to, and why), guardrails (what must or
must not happen, derived from the first two), and procedural notes. If
your change is a real decision (hard to reverse, non-obvious, or the
result of a real tradeoff), consider capturing it as a decision record
alongside your PR — see `docs/decisions/` for the format and existing
examples, or use this plugin's own `roadmap` skill to generate one.

## Validation

There's no CI. Before opening a PR:

- Any manifest you touched is valid JSON: `python3 -m json.tool <file>` or
  `jq . <file>`.
- Any `SKILL.md` or `agents/*.yaml` you touched has well-formed YAML
  frontmatter.
- Grep your skill body for agent-specific language before submitting:
  `grep -niE "claude|anthropic|bash tool|read tool|slash command" plugins/kms/skills/*/SKILL.md`
  should return nothing.
- Grep for a shipped skill naming one of `kms`'s own files instead of
  stating its check inline: `grep -nE "docs/(facts|decisions|guardrails|skills)/[A-Za-z0-9_-]+\.md" plugins/kms/skills/*/SKILL.md`,
  then judge each hit per `docs/skills/scoping-shipped-vs-repo-rules.md`.

## Pull requests

Describe *why* the change is needed, not just what it does — this repo's
own `attribute` skill exists to encourage exactly that habit; feel free to
use it on your own commits. Link any related knowledge artifact you added
or relied on.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
