# Plan: uninstall skill, bootstrap full traceability, generalized templates sync

## Context (read this before touching anything)

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace, one plugin (`kms`) at
`plugins/kms/`. See `AGENTS.md` at the repo root for full structure and
conventions before making any change not covered by this plan. This plan
came out of a `roadmap` interview; see `docs/decisions/0028` through
`0030` for the decisions it recorded, and
`docs/facts/0007-claude-code-plugin-uninstall-lifecycle.md` for the
platform-constraint fact behind them.

Most steps below were already done as of this plan's creation; step 6
was, and remains, deliberately left open (see its own status marker).
Re-read this file rather than assuming anything from a prior
conversation.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Three new decisions + one new fact — status: done

- `docs/decisions/0028-generalize-templates-sync-scope.md` (process)
- `docs/decisions/0029-bootstrap-full-traceability.md` (process)
- `docs/decisions/0030-uninstall-skill.md` (process)
- `docs/facts/0007-claude-code-plugin-uninstall-lifecycle.md` — governed
  by 0030, backs the "no automatic cleanup is possible" claim with
  primary-source research (33 documented hook events, none uninstall-
  related; a plugin's own directory is cleaned up by the host, but
  nothing it wrote into a target project is).

### 2. `bootstrap` changes — status: done

- Step 3 (doc manifest): `docs/facts/docs-manifest.md` now stamped
  `kms-generated: true`.
- Step 7 (track role lists): both role-list files now stamped
  `kms-generated: true`.
- Step 8 (renamed "Seed baseline artifacts"): generalized from
  hardcoding `templates/guardrails/` to scanning every subdirectory of
  `templates/`, mapping `<type>/` to `docs/<type>/`.
- New step 9 ("Wire into the project's own agent-instructions file"):
  inserts a `<!-- kms:start -->`/`<!-- kms:end -->`-marked section into
  the target project's `AGENTS.md` (or `CLAUDE.md`; creates a minimal
  `AGENTS.md` if neither exists), pointing at
  `docs/{facts,decisions,guardrails,skills}/` and naming
  `steward`/`lint`/`query`.

Done when: a fresh `bootstrap` run on a project with none of this yet
produces a `docs/facts/docs-manifest.md` and both role-list files with
`kms-generated: true`, and an `AGENTS.md` (or `CLAUDE.md`) with the
marked block present.

### 3. `steward` check 14 / `lint` check 12 — status: done

Both renamed ("Baseline artifacts synced?" / "Baseline artifacts out of
sync") and generalized the same way as `bootstrap` step 8 — scanning
every `templates/<type>/` subdirectory, not just `guardrails/`.

### 4. `uninstall` skill — status: done

`plugins/kms/skills/uninstall/{SKILL.md,examples.md,agents/openai.yaml}`
— scans for all four categories (`kms-seeded`, `kms-generated`, the
AGENTS.md block, still-draft stubs), reports first, then asks per-file
detach/remove. Required by `docs/guardrails/every-skill-ships-examples.md`
to ship `examples.md`; required by
`docs/decisions/0008-native-codex-plugin-support.md` to ship an
`agents/openai.yaml` sidecar.

Done when: run against this repo's own `docs/` tree (dogfooding), it
correctly reports the 4 `kms-seeded` guardrails already present and
finds no `kms-generated` files or AGENTS.md block yet (since `bootstrap`
hasn't been re-run here to add those retroactively — see step 6 below).

### 5. Mechanical updates — status: done

Version bump 0.5.0 → 0.6.0 across both plugin manifests + description
sync; `.claude-plugin/marketplace.json` description sync;
`README.md` (new `uninstall` row + Examples link); `CHANGELOG.md` new
`[0.6.0]` entry; `AGENTS.md` skill count (twelve → thirteen) and a new
Structure line for the `kms-generated`/`<!-- kms:start/end -->`
conventions (added after a `/code-review` pass caught the gap).

### 6. Retrofit this repo's own AGENTS.md / bootstrap outputs — status: pending, open question

This repo's own `AGENTS.md` doesn't yet have the `<!-- kms:start -->`
block (that only makes sense for a project consuming `kms`, and this
repo simultaneously *builds* `kms` and *dogfoods* the resulting
knowledge system — its `AGENTS.md` already documents that system in its
own words, arguably making the boilerplate `kms:start` block
redundant here specifically). Similarly, `docs/facts/docs-manifest.md`
and the track-role-lists don't exist in this repo. **Not resolved by
this plan** — whether this repo's own `AGENTS.md`/`docs/` should carry
these `bootstrap`-style artifacts too, or whether kms's own repo is a
legitimate exception to a convention meant for adopting projects, is an
open question for a future session, not assumed either way here.

## Explicitly not done in this plan (separate, later work)

- **Committing or pushing any of this** — not requested for this
  session; check `git status`/`git log` before assuming otherwise.
- **Retrofitting existing adopted projects** that bootstrapped before
  this plan — `steward`'s existing sync check (14) already surfaces
  missing `kms-seeded` artifacts on its own; nothing here backfills the
  new `kms-generated`/AGENTS.md wiring into a project that already ran
  an older `bootstrap`. That's future `steward`/`bootstrap` gap-fill
  work, not solved here.
- Step 6 above (whether this repo retrofits its own `AGENTS.md`/
  `docs-manifest.md`/role-lists) — explicitly left open.
