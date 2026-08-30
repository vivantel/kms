# Plan: consolidate lint/capture checks, add conform, document kms's architecture

## Context (read this before touching anything)

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace, one plugin (`kms`) at
`plugins/kms/`. See `AGENTS.md` at the repo root, and now also
`docs/skills/kms-architecture.md`, for full structure before making any
change not covered by this plan. This plan came out of a `roadmap`
interview; see `docs/decisions/0031` through `0033` for the decisions
it recorded.

All steps below were already done as of this plan's creation. Re-read
this file rather than assuming anything from a prior conversation.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Three new decisions — status: done

- `docs/decisions/0031-consolidate-kb-checks-rename-capture.md` (process)
- `docs/decisions/0032-conform-skill.md` (process)
- `docs/decisions/0033-kms-architecture-doc.md` (process)

### 2. `steward` renamed to `capture`, narrowed — status: done

`git mv plugins/kms/skills/{steward,capture}`. `SKILL.md` rewritten:
"Global principles" section removed entirely (fully overlapped with
what's now `lint`-only); "Artifact formats" section kept (needed to
draft stubs correctly); checks renumbered 1-6, keeping only new-decision,
fact-changed, new-automatable-rule, contradiction-found, human-doc-drift,
and the session-scoped half of the old role-list check. `examples.md`
and `agents/openai.yaml` updated to match.

Done when: `plugins/kms/skills/steward/` no longer exists;
`plugins/kms/skills/capture/SKILL.md` has exactly 6 numbered checks and
no "Global principles" section.

### 3. `lint` absorbs everything — status: done

Two new checks added (13: derived-artifact-stale, 14: role-list-gone-cold,
the full-history half of the old role-list check), description and intro
paragraph updated to state the clean split explicitly (no more
"complements steward's checks" framing — there's no overlap left to
complement). `examples.md`'s one stale `steward` mention fixed.

Done when: `plugins/kms/skills/lint/SKILL.md` has 14 checks, 0 mentions
of "steward".

### 4. Hook mechanism renamed — status: done

`git mv plugins/kms/hooks/{steward-nudge.sh,capture-nudge.sh}`;
`git mv docs/skills/{automating-steward.md,automating-capture.md}`;
both rewritten (echoed message, window comment, doc title/content) to
say "capture"; `plugins/kms/hooks/hooks.json`'s `command` field updated
to the new script path.

Done when: `plugins/kms/hooks/hooks.json`'s command references
`capture-nudge.sh` and that file exists; `sh -n` on it succeeds.

### 5. `conform` skill — status: done

`plugins/kms/skills/conform/{SKILL.md,examples.md,agents/openai.yaml}`
— flexible target resolution (staged diff / commit range / free-text
like "last 3 PRs"), checks non-KB changes against
`docs/{decisions,guardrails}/`, explicitly excludes KB-artifact changes
(that's `lint`/`capture`'s job). Required by
`docs/guardrails/every-skill-ships-examples.md` to ship `examples.md`;
required by `docs/decisions/0008-native-codex-plugin-support.md` to
ship an `agents/openai.yaml` sidecar.

### 6. `docs/skills/kms-architecture.md` — status: done

Synthesizes the four layers (`docs/` internal, `plugins/kms/skills/`
packaging, `plugins/kms/templates/` product content,
`plugins/kms/hooks/` automation) and the three marker conventions
(`kms-seeded`/`kms-template-version`, `kms-generated`,
`<!-- kms:start/end -->`) in one place, pointing at `bootstrap`/`capture`
for the 4-artifact-type model rather than re-explaining it. `AGENTS.md`
gained one line pointing to it.

### 7. Live cross-reference sweep — status: done

Every *live* mention of `steward` updated to `capture` (or, where the
specific check moved entirely to `lint`, removed and replaced with a
`lint`-only reference) across: `bootstrap`, `onboard`, `query`,
`quickstart` (+ its `examples.md`), `refactor-plan`, `uninstall`
`SKILL.md`s; 9 `docs/guardrails/*.md` files (4 of which are
`kms-seeded` — their `## Derivation` sections were fixed, but
`kms-template-version` was **not** bumped, since the underlying
templates' own `## Guardrail` text never changed — only kms's own
copies' derivation prose did, which sync explicitly never touches);
`docs/skills/scoping-shipped-vs-repo-rules.md`; `AGENTS.md`;
`README.md`. Every *historical* reference (decisions `0009`-`0030`,
completed plans, past `CHANGELOG.md` entries, facts recording a past
audit's findings) was deliberately left untouched.

Done when: `grep -rl "steward" --include="*.md" .` returns only files
in the historical set above, plus `roadmap`'s generic
"knowledge-steward-style" style-descriptor (not a reference to this
plugin's own skill).

### 8. Mechanical updates — status: done

Version bump 0.6.0 → 0.7.0 across both plugin manifests + description
sync (mentioning `conform`, `capture` instead of `steward`);
`.claude-plugin/marketplace.json` description sync; `README.md` (new
`capture`/`conform` rows, `uninstall`'s row's `steward` mention fixed);
`CHANGELOG.md` new `[0.7.0]` entry, explicitly flagging the `steward`→
`capture` rename as breaking for anyone invoking `/kms:steward` directly.

## Explicitly not done in this plan (separate, later work)

- **Committing or pushing any of this** — not requested for this
  session; check `git status`/`git log` before assuming otherwise.
- **Rewriting historical decisions/plans/facts** to say "capture"
  instead of "steward" — deliberately not done; see step 7 and
  `docs/decisions/0031`'s own tradeoffs section for why.
