# Plan: quickstart skill, steward-nudge hook, discoverability improvements

## Context (read this before touching anything)

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace, one plugin (`kms`) at
`plugins/kms/`. See `AGENTS.md` at the repo root for full structure and
conventions before making any change not covered by this plan. This plan
came out of a `brainstorm` session (3 of 7 approaches picked) followed by
a `roadmap` interview; see `docs/decisions/0023` through `0025` for the
decisions it recorded.

All steps below were already done as of this plan's creation, except the
GitHub metadata step, which depends on live confirmation. Re-read this
file rather than assuming anything from a prior conversation.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. New fact — status: done

`docs/facts/0007-claude-code-plugin-hooks-mechanism.md` — primary-sourced
facts about `hooks/hooks.json`, confirmed event fields, and the
unconfirmed cross-hook-state gap (including a note that a subagent
consulted for this returned harness-flagged output that was discarded,
not acted on).

### 2. Three new decisions — status: done

- `docs/decisions/0023-quickstart-skill.md` (track: process)
- `docs/decisions/0024-automate-steward-nudge-hook.md` (track: process)
- `docs/decisions/0025-discoverability-improvements.md` (track: product)

### 3. `quickstart` skill — status: done

`plugins/kms/skills/quickstart/{SKILL.md,examples.md,agents/openai.yaml}`
— sequences `bootstrap` then `roadmap` on one real decision. Required by
`docs/guardrails/every-skill-ships-examples.md` to ship `examples.md`;
required by `docs/decisions/0008-native-codex-plugin-support.md` to ship
an `agents/openai.yaml` sidecar, matching every other skill.

Done when: `lint`'s check 9 (missing `examples.md`) would find nothing
wrong with this skill.

### 4. Steward-nudge hook — status: done (revised after /code-review)

- `plugins/kms/hooks/hooks.json` — `SessionStart` hook calling
  `plugins/kms/hooks/steward-nudge.sh` via `${CLAUDE_PLUGIN_ROOT}`,
  commit-recency gated. Originally shipped as a `SessionEnd` hook with
  inline shell in `hooks.json`; a `/code-review` pass found it was a
  complete no-op (`SessionEnd` output is discarded entirely) plus two
  shell bugs (an exit-code-only work-tree check, and an unguarded
  negative `age` on clock skew) — all three fixed, see decision 0024's
  revised text for the full history.
- `plugins/kms/hooks/steward-nudge.sh` — the extracted, tested,
  executable shell script; the single source of truth for the `window`
  value.
- `docs/skills/automating-steward.md` — explains the corrected mechanism
  (agent-facing context, not a guaranteed user-visible message), the
  time window, how to disable it, how to test it standalone, and the
  manual recipe for non–Claude-Code agents.

Done when: `python3 -m json.tool plugins/kms/hooks/hooks.json` succeeds;
`sh -n plugins/kms/hooks/steward-nudge.sh` succeeds; running the script
against a repo with a <4h-old commit prints the note, a >4h-old commit
prints nothing, a bare repo prints nothing, and a future-dated commit
prints nothing — all four verified empirically during this session.

### 5. Manifest version bump — status: done

Per `docs/guardrails/plugin-manifest-version-sync.md`, both manifests'
`version` moved from `0.3.0` to `0.4.0`:
- `plugins/kms/.claude-plugin/plugin.json`
- `plugins/kms/.codex-plugin/plugin.json`

Descriptions and `.claude-plugin/marketplace.json`'s descriptions synced
to mention `quickstart` alongside the other 11 skills.

Done when: all three files parse as valid JSON, all three `version`
fields read `0.4.0`.

### 6. README — status: done

- Static shields.io badges added near the top: MIT license, "Claude Code
  Plugin". No version badge (see decision 0025's rationale).
- New `quickstart` row in the skill table with an `examples.md` link,
  consistent with `docs/guardrails/every-skill-ships-examples.md`.

Done when: the table has 12 data rows and the two badges render as valid
Markdown image-link syntax.

### 7. CHANGELOG — status: done

New `## [0.4.0]` section (prepended above `## [0.3.0]`), `### Added`
covering `quickstart`, the steward-nudge hook, and the discoverability
changes.

### 8. AGENTS.md — status: done

- Skill enumeration: "eleven skills" → "twelve skills", `quickstart`
  added to the list.
- "Structure" code block gained a
  `plugins/<plugin-name>/hooks/hooks.json` line describing the
  auto-activating plugin-hook mechanism.

### 9. GitHub repo metadata — status: done, confirmed live

Run (exact values decided during this session's interview):

```sh
gh repo edit vivantel/kms \
  --description "Vivantel KMS: a Claude Code / Codex plugin marketplace of knowledge-management skills — capture decisions as durable, traceable artifacts and keep them current, queryable, and attributable across sessions." \
  --add-topic claude-code --add-topic claude-code-plugin --add-topic ai-agent \
  --add-topic knowledge-management --add-topic architecture-decision-records \
  --add-topic developer-tools --add-topic documentation --add-topic marketplace
```

Done when: `gh api repos/vivantel/kms --jq '{description,topics}'` shows
the description and all 8 topics above.

## Explicitly not done in this plan (separate, later work)

- **Committing or pushing any of this** — not requested for this
  session; check `git status`/`git log` before assuming otherwise.
- **A confirmed Codex hook equivalent** — left as an open gap in
  `docs/facts/0007` and `docs/skills/automating-steward.md`, not solved
  here.
- Higher-effort discoverability work considered in the brainstorm session
  but out of scope for a text-only session — screenshots/GIFs, an
  external docs site, an "awesome-list" submission.
