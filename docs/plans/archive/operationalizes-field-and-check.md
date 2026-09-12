---
id: operationalizes-field-and-check
title: Ship the operationalizes field and lint check 23
status: done (all 6 steps complete)
date: 2026-09-10
tags: [kms, knowledge-management, taxonomy, guardrail]
---

# Ship the operationalizes field and lint check 23

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`,
public GitHub repository) is a Claude Code / Codex / Kilo Code CLI plugin
marketplace, one plugin (`kms`) at `plugins/kms/`. See `AGENTS.md` for
structure/conventions.

This plan implements `docs/decisions/0047-operationalizes-field-and-unoperationalized-guardrail-check.md`:
an optional `operationalizes: [<guardrail-id>, ...]` frontmatter field on
the `Procedure` artifact type, plus a new `lint` check (23) flagging a
guardrail that describes a recurring/multi-step action with no procedure
operationalizing it. Read that decision for the full rationale (why not a
5th "runbook" artifact type, why the field lives on `Procedure` not
`Guardrail`, why many-to-many, why shipped together rather than phased)
before touching anything below — this plan only tracks execution status,
not the reasoning.

**Everything below has already been done in this session** — this plan
exists per `roadmap`'s own requirement to always produce one alongside a
captured decision, not because a fresh session needs to start from
scratch. If you're picking this up cold: check `git log`/`git status`
first, since it's likely already merged.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Add the field to the artifact model — status: done

`plugins/kms/shared/artifact-model.md`: added a `Procedure —` line
(the only one of the four types previously missing one) documenting
`operationalizes: [<guardrail-id>, ...]`, optional, many-to-many, "most
procedures won't carry this field at all."

Done when: the line exists and reads consistently with the existing
`Fact —`/`Guardrail —`/`Decision —` lines above it. (Verified: it does.)

### 2. Add lint check 23 — status: done

`plugins/kms/skills/lint/SKILL.md`'s "What to check" list: added item 23,
worded as a judgment call (like checks 5/6/8), not a mechanical
field-presence test — a guardrail describing a recurring/multi-step
action with nothing operationalizing it is flagged; a simple one-line
prohibition never is.

Done when: item 23 exists, and the whole file was re-read once after
editing (per `AGENTS.md`'s rule for shipped `SKILL.md` edits) to confirm
no other section needed a matching update. (Verified: none did — `capture`,
`roadmap`, and `bootstrap`'s bodies reference the shared artifact-model
file generically, without naming `Procedure`'s fields inline, so they
pick up the new field automatically with no edit needed.)

### 3. Bump every plugin manifest version together — status: done

Per `docs/guardrails/plugin-manifest-version-sync.md`: `0.10.0` →
`0.11.0` in `plugins/kms/.claude-plugin/plugin.json`,
`plugins/kms/.codex-plugin/plugin.json`, and every one of the 14
per-skill `version` fields in `plugins/kms/skills/index.json` — all in
this same change, all to the same value.

Done when: `grep -c '"version": "0.11.0"' plugins/kms/skills/index.json`
returns 14, and both `plugin.json` files show `0.11.0`. (Verified.)

### 4. Update the decisions index — status: done

`docs/decisions/INDEX.md`: added the row for `0047-operationalizes-field-and-unoperationalized-guardrail-check`,
`status: draft` (matches the decision file's own frontmatter — this
hadn't had expert sign-off to move to `active` yet, per the artifact
model's "Decision ... immutable once accepted" — accepting it was a
separate, later action, not part of this plan).

**Update, 2026-09-12**: sign-off given retroactively — a full `lint` pass over this repo's own
knowledge base found the decision still sitting at `draft` despite its described mechanism
(the `operationalizes` field, check 23) having shipped, merged, and been in active, confirmed
use for two days (even cited as settled fact by `docs/decisions/0049-...`). Promoted to
`status: active` in both the decision file and `docs/decisions/INDEX.md`.

### 5. Generate a CHANGELOG.md entry — status: done

**Update, 2026-09-12**: satisfied via `docs/decisions/0050-version-bump-changelog-linkage.md`'s
backfill — `CHANGELOG.md`'s `## [0.11.0] - 2026-09-11` entry now has an `### Added` bullet
covering this change (the `operationalizes` field and lint check 23), correctly attributed to
`0.11.0` (the version this change's own bump commit produced), not the later `0.12.0`.

### 6. Run the eval suite — status: done

**Update, 2026-09-12**: not run as its own dedicated PR at the time, but satisfied
retroactively many times over since — every eval run in
`docs/plans/archive/eval-harness-baseline-reliability.md`'s history from PR #33 onward exercised
`lint`'s `SKILL.md` with check 23 already present, including PR #40's full-suite run
(workflow `34680485606`), and `lint` passed every time. Check 23 stayed additive as predicted
(no eval fixture has a guardrail shaped to trigger it) — no regression ever surfaced.

## Explicitly out of scope

- **Retrofitting `operationalizes` onto this repo's own 4 existing
  procedures** — none of them (`adding-agent-support`,
  `automating-capture`, `kms-architecture`, `scoping-shipped-vs-repo-rules`)
  are runbooks for a specific guardrail; forcing the field onto them
  would misuse it. `docs/decisions/0047-...` says so explicitly.
- **Running `lint` against this repo's own knowledge base** to see what
  check 23 finds here — a natural next action, but a separate,
  deliberate invocation, not a step this plan owns.
- **Backfilling `operationalizes` on any adopting project's existing
  procedures** — this plan only ships the mechanism; populating it is
  each adopting project's own, later work.
