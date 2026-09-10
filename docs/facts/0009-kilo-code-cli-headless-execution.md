---
id: 0009-kilo-code-cli-headless-execution
title: Kilo Code CLI's headless execution mode and multi-provider model configuration
status: active
date: 2026-09-04
tags: [kilo, automation]
kind: environmental
governed-by: 0043-eval-harness-for-shipped-skill-changes
---

Confirmed 2026-09-04 via current aggregator/documentation sources: Kilo
Code CLI supports `kilo run "<prompt>"` for one-shot, scriptable
execution, and `kilo run --auto "<prompt>"` for fully autonomous
execution — no human interaction, operations not already auto-approved
are simply disallowed rather than blocking on a prompt, and the process
exits automatically on completion or timeout. This makes it CI-usable
the same way `claude -p`/`--print` is for Claude Code.

Kilo connects to 500+ models across 60+ providers, configured via
`kilo.jsonc`/`.kilo/kilo.jsonc` — the same config file this repo
already ships for the skills-distribution use case
(`docs/decisions/0035-native-kilo-code-support.md`), now also usable to
point Kilo's own execution at an arbitrary model backend rather than a
fixed default.

**Not confirmed with high confidence**: exact flag syntax for combining
`--auto` with a config-specified provider/model override in a single
non-interactive invocation. Verify against Kilo's own CLI docs/`--help`
output at implementation time — the same caution
`docs/facts/0008-kilo-code-skills-spec.md` already states for this
fast-evolving, externally-owned CLI.

**Re-verified 2026-09-05** against the installed `kilo --help`/`kilo run --help` output:
`kilo run --auto -m <provider>/<model> "<prompt>"` combines both in one invocation as expected.
One correction found by testing, not by docs: a *project-scope* `kilo.jsonc`/`.kilo/kilo.jsonc`
(any config file Kilo discovers by walking up from cwd) unconditionally rejects
`${env:VAR}`/`{env:VAR}` credential interpolation in `provider.*.options`, regardless of syntax
variant — confirmed by testing, not documented anywhere found. A custom provider needing a
secret from the environment (e.g. this harness's OpenRouter provider) must instead be supplied
via the `KILO_CONFIG_CONTENT` environment variable (undocumented but present in the CLI binary
alongside `KILO_CONFIG`/`KILO_CONFIG_DIR`), which Kilo treats as trusted, operator-supplied
configuration rather than project configuration. See
`docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`'s amendment and
`evals/providers/kilo-runner.sh`.
