---
id: scale-bootstrap-and-lint-chunked-checkpointing
title: Give bootstrap and lint a chunked, checkpointed execution mode, then validate it on a real large repo
status: steps 1-3, 6 done; step 4 files written but not yet run; step 5 pending; steps 7-8 pending
date: 2026-09-13
---

# Give bootstrap and lint a chunked, checkpointed execution mode, then validate it on a real large repo

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`, **public** GitHub repo) is
a Claude Code/Codex/Kilo Code CLI plugin marketplace shipping one plugin, `kms`, with fourteen skills
under `plugins/kms/skills/`. Two of them — `bootstrap` (one-time knowledge-system setup, mining git
history and existing docs) and `lint` (full-repo validation over the knowledge base) — currently run as
one unbroken pass with no checkpointing. There is already direct evidence this doesn't scale:
`bootstrap`'s own eval case needed `timeout_seconds` raised to 1440 (24 min) even on a tiny synthetic
fixture (`docs/plans/archive/eval-harness-baseline-reliability.md`), and
`docs/decisions/archive/0041-index-and-archive-for-scale.md` states outright that `lint`'s structural
checks "inherently require opening every file they validate, index or not" — no ceiling even after the
index/archive scale work already done.

This plan implements the design recorded in `docs/decisions/0056-chunked-checkpointed-execution-for-
bootstrap-and-lint.md` and `docs/decisions/0057-confirming-party-generalizes-human-checkpoint.md` — read
both in full (including their "Why" and "Tradeoffs considered" sections) before starting; this plan does
not repeat their reasoning, only the concrete steps. Also read the three facts they're grounded in:
`docs/facts/0015-checkpoint-file-location-and-lifecycle.md`, `docs/facts/0016-chunk-sizing-parameters.md`,
`docs/facts/0017-bootstrap-history-scope-selection-values.md` — these carry the exact numeric/format
values every step below implements. And read the two new guardrails:
`docs/guardrails/checkpoint-file-lifecycle.md`, `docs/guardrails/confirming-party-acceptable-for-
checkpoint-gates.md`.

Background on the existing eval harness this plan extends: `docs/decisions/0043-eval-harness-for-
shipped-skill-changes.md` and `docs/decisions/0044-eval-harness-ci-safety-gates.md` (read both files'
`## Amendment` sections — they record real corrections made during execution, including that the harness
now runs entirely on Kilo Code CLI's free built-in gateway, no account or API key).

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Write `plugins/kms/shared/checkpointing.md` — status: done

New shared file, same pattern as `plugins/kms/shared/artifact-model.md` (identical, same-voice content
read by more than one skill body). It must define, generically enough that any future skill can adopt it
via `docs/skills/adding-checkpointed-execution.md`:

- The checkpoint file's path convention and naming: `docs/.kms-checkpoints/<skill>-<run-id>.md` (per
  `docs/facts/0015-...`) — pick a simple `run-id` format (e.g. a timestamp) and state it here so every
  adopting skill uses the same one.
- Its required frontmatter/shape: which skill, which run, current phase, per-type (or per-commit-range)
  last-completed offset, and an accumulating findings/output section grouped by check (lint) or a bare
  offset (bootstrap, since its output is the stub files themselves).
- The token-budget paging rule from `docs/facts/0016-...`: accumulate files in stable alphabetical order
  until ~15,000 estimated tokens, checkpoint, continue; a single file already over budget gets a one-file
  page; a page boundary is always a whole number of complete files.
- The two-phase model: a chunkable per-item phase (paged, checkpointed after every page) followed by a
  single non-chunked aggregation phase that runs once, after every page of the first phase completes.
- The resume protocol: on invocation, if a checkpoint file exists for this skill, ask the user (the
  confirming party — see `docs/guardrails/confirming-party-acceptable-for-checkpoint-gates.md`) to resume
  or discard; on resume, re-list the recorded files/commits and compare against the checkpoint's recorded
  set, forcing a fresh start on any mismatch.
- Cleanup: delete the checkpoint file as the run's last action on success.

Done when: the file exists, is referenced correctly by both `bootstrap/SKILL.md` and `lint/SKILL.md`
(steps 2 and 3 below), and contains no `bootstrap`- or `lint`-specific specifics (those stay in each
skill's own body — this file only owns the generic mechanics).

### 2. Rewrite `plugins/kms/skills/bootstrap/SKILL.md` for chunked execution — status: done

Current file is 128 lines, 10 numbered steps (read it fresh before editing — it may have changed since
this plan was written). Changes needed:

- Add a line next to the existing `../../shared/artifact-model.md` reference: `../../shared/
  checkpointing.md` defines this skill's chunked/checkpointed execution — read it before running steps
  1–5 below.
- **Step 1 (intent extraction from history)**: before scanning, ask the user how much git history to
  mine, per `docs/facts/0017-...` exactly: check `git rev-list --count` first, offer the four options
  (all / last N commits / last M years / custom), recommend "all" under 1,000 commits or "last 2 years"
  at/above it, with the reasoning stated inline (not just the number). Then mine oldest-first, paged per
  `checkpointing.md`'s token-budget rule, checkpointing the last completed commit SHA after each page.
- **Steps 2–4 (fact extraction, doc manifest, guardrail audit)**: page by file, same token-budget rule,
  in the same run's Phase A alongside step 1 (these can interleave or run as separate sub-phases within
  Phase A — either is fine as long as each checkpoints independently and step 1's git-mining offset is
  never conflated with a file-paging offset).
- **Step 5 (fitness function inventory)**: same per-file paging where it scans skill/guardrail files;
  the CI/build-config scan is small enough it doesn't need paging (note this explicitly rather than
  silently skipping chunking logic for it).
- **Steps 6–10**: unchanged in content, but now explicitly run once, as Phase B, only after every Phase A
  page (across steps 1–5) has completed — state this ordering directly in the skill body, don't leave it
  implicit.
- Confirm no step's existing wording assumes a human specifically where `confirming-party-acceptable-
  for-checkpoint-gates.md` now applies — bootstrap's current body has no explicit "wait for confirmation"
  gate (it writes files directly), so this is likely a no-op here; verify rather than assume.

Done when: `bootstrap/SKILL.md` references `checkpointing.md`, step 1 asks the scope question exactly as
`0017-...` specifies, steps 1–5 are explicitly Phase A (paged, checkpointed) and steps 6–10 are explicitly
Phase B (single aggregation pass after Phase A completes) — confirmed by reading the whole file once
more after editing, per this repo's own `AGENTS.md` rule to re-read a shipped `SKILL.md` in full after any
edit, not just the touched lines.

### 3. Rewrite `plugins/kms/skills/lint/SKILL.md` for chunked execution — status: done

Current file is 43 lines: a preamble, 24 numbered checks, an "Output" section, an "Out of scope" section.
Read it fresh before editing. Changes needed:

- Add a `../../shared/checkpointing.md` reference next to the file's existing archive-scoping preamble.
- Add a short new section (after the preamble, before "What to check") stating the two-phase execution
  model: Phase A pages, by artifact type, every check resolvable from the file being read plus a bounded
  lookup already loaded (a type's own `INDEX.md`, or kms's own small fixed shipped-content set) — checks
  1–12, 15, 17–19, 21–24 (verify this list against the checks' actual text before finalizing — several,
  e.g. check 3's numbering check or check 8's cross-reference to a shipped skill body, are not simply
  "one file at a time" and need the reasoning spelled out in the skill body, not just a bare number list).
  Phase B runs once, after Phase A completes, only for checks needing a second, specific project artifact
  identified from Phase A's own findings (13, 14, 16, 20): shortlist first from each type's `INDEX.md` (the
  same tag-scoping approach `docs/decisions/archive/0041-...` already established for check 16), then open
  only the shortlisted files, itself paged if the shortlist is large. State plainly that the 24 checks
  themselves are unchanged — this is a change to execution order and checkpointing, not to what gets
  checked.
- The existing "Output" section's "never silently fix anything — propose the fix and wait for
  confirmation" line: reword to "wait for the confirming party's go-ahead" per `docs/guardrails/
  confirming-party-acceptable-for-checkpoint-gates.md`, with a one-clause note that the confirming party
  is ordinarily the user but may be an authorized reviewing subagent acting within its own configured
  authority (kms does not define that authorization mechanism).

Done when: `lint/SKILL.md` references `checkpointing.md`, states the Phase A/Phase B split with which
checks fall in each phase, and the "Output" section's confirmation language matches the new guardrail —
confirmed by re-reading the whole file once more after editing, same rule as step 2.

### 4. Add resume-specific eval cases — status: pending (files written, not yet run locally — see step 5)

New files, sibling to the existing cases:

- `evals/bootstrap-resume/promptfooconfig.yaml` — reuses `evals/bootstrap/fixture/` (point `fixture_dir`
  at the existing path, don't duplicate the fixture). Sets `timeout_seconds` low enough to force a kill
  partway through a real run against that fixture (tune this empirically — start around half of
  `evals/bootstrap/promptfooconfig.yaml`'s current `timeout_seconds`), then a second provider stage (or a
  second `kilo run --auto` invocation in the same case, matching how `evals/providers/kilo-runner.sh`
  already shells out) restarts against the same fixture directory, which should now contain a checkpoint
  file from the killed run. Assertions: the second run's transcript/output shows it detected and offered
  to resume the checkpoint (not started fully over), the final file listing has no duplicate-numbered
  stub files, and `docs/.kms-checkpoints/` is empty afterward (cleaned up on success).
- `evals/lint-resume/promptfooconfig.yaml` — same shape, reusing `evals/lint/fixture/`. Assertions:
  second run's sentinel-line output (same `LINT_CHECK_*: YES|NO` convention as the existing `evals/lint`
  case) shows every finding from the interrupted run still present in the final report — none dropped,
  none duplicated.
- Both new cases need their own `# Run standalone:` comment header and description, matching the existing
  cases' style exactly (see `evals/bootstrap/promptfooconfig.yaml` and `evals/lint/promptfooconfig.yaml`
  for the pattern).

Done when: both new `promptfooconfig.yaml` files exist, run cleanly with `npx promptfoo eval -c
evals/bootstrap-resume/promptfooconfig.yaml` (and the `lint-resume` equivalent) at least once locally, and
`docs/decisions/0056-...`'s `governed-facts`/description of "new resume-specific eval cases" is verifiably
true against the actual `evals/` directory contents.

### 5. Verify the full suite locally — status: pending

`npm install && npm install -g @kilocode/cli && npm run eval` — confirm the existing 5 cases still pass
(no regression from the `SKILL.md` edits in steps 2–3) and the 2 new resume cases pass. Per `docs/plans/
archive/eval-harness-baseline-reliability.md`'s established baseline, `roadmap` is an accepted known flake
unrelated to this change — don't chase it if it fails here.

Done when: `capture`, `attribute`, `lint`, `bootstrap`, `bootstrap-resume`, `lint-resume` all pass in a
local run; `roadmap`'s status is noted but not blocking.

### 6. Bump manifest versions and CHANGELOG — status: done (bumped to 0.16.0, CHANGELOG.md entry added)

Per `docs/guardrails/plugin-manifest-version-sync.md` and `docs/guardrails/version-bump-requires-
changelog-entry.md`: bump `plugins/kms/.claude-plugin/plugin.json` and `plugins/kms/.codex-plugin/
plugin.json`'s `version` fields together, and add a matching `CHANGELOG.md` entry describing the chunked/
checkpointed execution mode and the confirming-party wording generalization.

Done when: both manifests carry the same new version, and `CHANGELOG.md` has a corresponding entry —
verify by reading both manifest files and the changelog's latest entry after editing.

### 7. Open a PR, let CI's eval workflow run — status: pending

Push this branch (`scale-bootstrap-lint-chunking`), open a PR against `master`. Per `docs/decisions/0044-
...`, `.github/workflows/eval-skills.yml` triggers automatically on a same-repo PR touching `plugins/kms/
skills/**` or `plugins/kms/shared/**` — this change touches both. Confirm the workflow's consolidated
summary comment shows all cases (including the 2 new resume cases) passing.

Done when: a real CI run on this PR shows the full suite passing, matching step 5's local result.

### 8. Validation phase — fork `redis/redis`, run unattended — status: pending

Per `docs/decisions/0056-...`'s validation intent and `docs/decisions/0057-...`'s confirming-party
generalization:

1. Fork `redis/redis` (or use a local clone if a fork isn't practical for this session's environment —
   either way, work against a real, full `redis/redis` history, not a synthetic fixture).
2. Run `bootstrap` against it, unattended, using whichever agent this session has available (kms's own
   `agent-agnostic-scope` guardrail means this plan does not pin a specific runner). When bootstrap asks
   the git-history scope question (step 2 above), the confirming party answers it — for this validation,
   pick "last 2 years" or "last ~3,000–5,000 commits" (a bounded window per this decision's interview
   outcome — not `redis/redis`'s full 20+-year history, which would make the run impractically long)
   unless the actual commit count in the chosen window turns out unexpectedly small, in which case widen
   it rather than run an under-scoped validation.
3. Run `lint` against the resulting knowledge base, unattended, with a reviewing subagent standing in as
   the confirming party for any proposed fix — per `docs/decisions/0057-...`, this session must configure
   that subagent's authority itself (kms does not ship or define this); a reasonable, defensible split is
   auto-approving lint's mechanical/structural findings (index resync, archive-candidate moves, missing
   required fields) and escalating judgment-laden ones (contradiction resolution, stale-derived-artifact
   rewrites, role-gone-cold removal) — but the specific split is this session's call to make and record,
   not something this plan pre-decides.
4. Record, in this file (append a `## Validation results` section below), for both bootstrap and lint:
   how many chunks/pages ran, how many checkpoint write/resume cycles occurred, whether any occurred
   naturally (a real timeout or rate/quota limit interrupting the run — expected and desired evidence,
   not a failure) versus needed to be staged deliberately, and the final output summary (stub counts,
   finding counts).
5. If no interruption occurs naturally across a reasonable number of attempts, deliberately stage one
   (kill the process or clear the session mid-run) at least once each for bootstrap and lint, and resume
   from a genuinely new session — the property this whole plan exists to prove is cross-session resume,
   and it must be demonstrated at least once, staged or organic.

Done when: both bootstrap and lint complete against the bounded `redis/redis` window, at least one real
interrupt-and-resume cycle (organic or staged) is demonstrated for each, and the "Validation results"
section below is filled in with concrete numbers, not just a pass/fail statement.

## Validation results

Not yet run — fill in after step 8.

## Explicitly out of scope

- Extending chunked/checkpointed execution to any skill besides `bootstrap`/`lint` — `docs/skills/adding-
  checkpointed-execution.md` exists so a future skill can adopt this pattern, but adopting it elsewhere is
  a separate initiative.
- Designing a reviewing subagent's authority-configuration mechanism as a kms feature — `docs/decisions/
  0057-...` explicitly declines this; the validation phase's own subagent authority is configured ad hoc
  for that one run, not built as shipped kms infrastructure.
- Re-litigating the eval harness's architecture (Kilo's free gateway, `promptfoo`, the original 5-case
  scope) — settled by `docs/decisions/0043-...`/`0044-...`; this plan only adds 2 cases to it.
