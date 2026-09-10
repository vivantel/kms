---
id: operationalizes-field-and-check
title: Ship the operationalizes field and lint check 23
status: pending
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
hasn't had expert sign-off to move to `active` yet, per the artifact
model's "Decision ... immutable once accepted" — accepting it is a
separate, later action, not part of this plan).

### 5. Generate a CHANGELOG.md entry — status: pending

Not done in this pass — `docs/decisions/0005-changelog-generation-design.md`
scopes the `changelog` skill as on-demand, asking the user for the
version/date at invocation rather than being auto-run as a side effect of
other work. Run it explicitly (`"generate a changelog"`) once this
change is ready to ship, using `0.11.0` as the version.

Done when: `CHANGELOG.md` has a `## [0.11.0] - <date>` entry covering
this change.

### 6. Run the eval suite — status: pending

This change touches `plugins/kms/shared/**` and `plugins/kms/skills/**`
(the `lint` skill specifically) — exactly the paths
`.github/workflows/eval-skills.yml` gates. Opening a PR from a same-repo
branch should trigger the `eval` job automatically (path-filter match on
`opened`); if it doesn't (e.g. reopened same PR, or the paths-filter
didn't match for some reason), trigger it manually with `/eval` as a PR
comment instead.

Done when: the workflow run for this PR shows the `lint` case still
passing — this change doesn't touch `lint`'s *behavior* on the suite's
existing fixtures (check 23 is additive, and none of the 5 eval fixtures
currently have a guardrail shaped to trigger it), so a regression here
would mean something broke unexpectedly, not an intended new finding.

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
