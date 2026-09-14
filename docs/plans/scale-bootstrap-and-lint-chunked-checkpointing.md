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

### 4. Add resume-specific eval cases — status: pending (files written; wired into `.github/workflows/eval-skills.yml`'s matrix after a real CI run showed them being silently skipped — not yet run locally, see step 5)

**Update, 2026-09-14**: a real `/eval` CI run (workflow `34847715310`) showed `eval (matrix.case)` and
`eval summary` as `skipped` — the two new case directories existed on disk but `eval-skills.yml`'s
`matrix.case` list (both the `eval` and `eval-recheck` jobs) was never updated to include
`bootstrap-resume`/`lint-resume`, so CI never actually ran them despite this step's own done-when
criteria implying it would. Fixed: both matrix lists now include them, and each job's `timeout-minutes`
raised 30→45 (`bootstrap-resume`/`lint-resume`'s worst case, `first_timeout_seconds` +
`second_timeout_seconds` = 2160s/36min, would otherwise exceed the prior 30min ceiling sized for the
original cases' single 1440s budget). The `/eval` comment retrigger on PR #52 turned out to hit the same
gap it was meant to test — `issue_comment`-triggered workflows resolve the *workflow YAML itself* from
`master`, not the PR branch (unlike `pull_request`-triggered ones, which do use the branch's version), so
the matrix fix was invisible to it. PR #52 closed and reopened as #53 to get a genuine `opened` event.

**Update, 2026-09-14 (second)**: PR #53's real `pull_request`-triggered run (`34853228741`) did correctly
include both new cases. `bootstrap-resume` passed — its first run genuinely hit `exit 124` (a real kill at
the 720s budget), confirming `bootstrap`'s multi-step task is slow enough on this fixture to interrupt
reliably. `lint-resume` failed: its first run hit `exit 0` (completed cleanly in ~430s, well under the
720s budget) — `lint`'s task on the same tiny fixture is simply faster than `bootstrap`'s, so it never
needed to checkpoint at all regardless of the timeout value, unless the timeout happened to land inside
that ~430s window. Considered and declined a fix via a configurable page-size budget (would let the eval
force pagination on a tiny fixture) — rejected as solving a test problem with a product feature no real
user has asked for, weakening the eval's fidelity to the shipped default rather than strengthening it, and
reopening `0016-...`'s already-considered token-budget value without a real driving need (the same
reasoning `docs/decisions/0054-...` already established for not building ahead of demonstrated need).
Fixed instead: `lint-resume`'s own `first_timeout_seconds` lowered 720→90, tuned to `lint`'s
(considerably faster) actual completion time on this fixture rather than sharing `bootstrap-resume`'s
value. PR #53 closed and reopened as #54 to get a genuine `opened` event (same reason as the #52→#53
reopen).

**Update, 2026-09-14 (third)**: PR #54's run (`34858747933`) showed 90s was still wrong, in the opposite
direction — genuinely interrupted this time (`exit 124`), but the transcript showed the model had only
just finished reading every file (its own `SKILL.md`/`checkpointing.md` plus all 7 fixture doc files) and
never reached writing a checkpoint at all. This fixture is small enough that its entire Phase A corpus is
one page — there's no page-1-vs-page-2 boundary, only a single narrow point (finish-reading-and-write-the-
one-checkpoint) that a timeout has to land after. Two data points now bracket it: 90s lands before that
point, 720s lands well after full completion (~430s). Fixed: raised to 200s — real margin on both sides,
not another small increment against the same boundary. PR #54 closed and reopened as #55.

**Update, 2026-09-14 (fourth)**: PR #55's run showed 200s still didn't work, but for a new reason — this
time `exit 0` at under 200s (the model completed the *entire* task, correctly finding all 3 planted
violations, just fast). Combined with the ~430s completion time observed on PR #53's run, this meant the
same tiny task's total completion time varies more than 2x run to run on this free-tier model — no fixed
timeout can reliably interrupt a moving target, so continuing to tune `first_timeout_seconds` against
`evals/lint/fixture` was a losing battle. Root cause: that fixture is so small its entire Phase A corpus
fits in a single 15K-token page, so there's only ever one narrow, speed-dependent point to land after, not
a stable multi-page window. Fixed properly instead of tuning further: `lint-resume` now uses its own
dedicated `evals/lint-resume/fixture/`, not the shared tiny one — `docs/decisions/` is a real snapshot of
this repo's own `docs/decisions/` at tag `0.15.0` (52 real decisions, ~34K tokens, pinned to a tag from
before this branch's own changes) plus one added synthetic decision carrying the missing-track violation;
`facts/`/`guardrails/`/`skills/` stay exactly as small as the original fixture, carrying the other two
planted violations unchanged. ~34K tokens forces ~3 real Phase A pages, giving a wide, page-count-driven
window instead of a single speed-dependent point. `first_timeout_seconds` raised to 400 (unverified
starting point, sized for the larger corpus). PR #55 closed and reopened as #56.

**Update, 2026-09-14 (fifth)**: PR #56's run showed two things. `lint-resume` still failed, but the real
cause is deeper than fixture size: the model got a genuine `exit 124` kill at 400s, but in that time did
only 12 Read actions — it read the cheap `INDEX.md` files (which already summarize id/title/tags/status
for every decision) plus a handful of individually-suspicious files, using that as a shortcut to answer
the 3 sentinel questions instead of mechanically walking every decision file. A bigger *fixture* doesn't
force real multi-page chunking if the model never needs to open most of the files at all — this needs a
different fix (a more explicit, exhaustive-processing prompt, or accepting it as a known-hard case) than
anything tried so far. Separately, `bootstrap-resume` — unrelated to this run's changes — failed for the
first time (passed twice before, PR #53), genuine `exit 124` but cut off during early setup before
reaching a checkpoint; read as the same run-to-run model-speed variance already established for
`lint-resume`, not a regression.

That second finding motivated a fix for `bootstrap-resume` specifically: unlike `lint`'s `docs/` tree
(where `INDEX.md` is an intentional, designed-in shortcut a model can read instead of every file —
exactly what defeated `lint-resume`'s bigger fixture), git-history mining has **no equivalent shortcut** —
extracting decision stubs genuinely requires walking real commit messages/diffs. `bootstrap-resume` now
uses its own dedicated `evals/bootstrap-resume/fixture/`: this repo's own real commit history up to tag
`0.15.0` (67 commits — the repo's entire history at that point, since only 67 total commits exist — full
patch content ~220K tokens, commit messages alone ~13K tokens), materialized from a checked-in git bundle
(`kms-history-0.15.0.bundle`) by `setup.sh`, with `docs/{facts,decisions,guardrails,skills}/` removed
after checkout (as one final synthetic commit) so bootstrap faces a genuine from-scratch extraction, not a
gap-fill pass. `first_timeout_seconds` kept at 720 (already reliably interrupted the much smaller 2-commit
fixture); `second_timeout_seconds` kept at 1440 but flagged as the real risk this time — a full mine of
much more real content might not finish in that budget, unverified until the next real CI run.
`lint-resume` is left as-is pending a decision on which further fix to pursue. PR #56 closed and reopened
as #57.

**Update, 2026-09-14 (sixth)**: PR #57's run showed a completely different failure for `bootstrap-resume` —
not a grading judgment at all. `Error: spawn E2BIG` (an OS-level "argument list too long" error) when
promptfoo tried to spawn the judge grading subprocess. Cause: `setup.sh` only stripped
`docs/{facts,decisions,guardrails,skills}/`, leaving the rest of the historical repo tree (`plugins/`,
`evals/`, everything else) in place — `kilo-resume-runner.sh`'s own final file listing (`find . -type f`)
enumerated hundreds of files, and that giant string exceeded the OS's exec argument-size limit. Fixed:
`setup.sh` now resets the working tree to near-empty (just a placeholder `README.md`) after checkout,
keeping full git history for mining but keeping the file listing small. Not yet verified — needs another
fresh PR.

New files, sibling to the existing cases (original design — since superseded per the updates above for
both cases' actual fixtures):

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

**Update, 2026-09-14**: PR #52 opened. Its only `pull_request`-triggered run (`34766744874`) tested the
pre-code-review-fix commit — `eval-skills.yml` deliberately doesn't re-trigger on a force-push (`0044-...`
excludes `synchronize`), so a subsequent `/eval` comment was needed to test the amended commit. That
recheck run (`34847715310`) found `capture` failing on `Read AGENTS.md failed: File not found` —
`evals/capture/fixture/` has never had an `AGENTS.md` (unchanged since PR #3, predates this branch
entirely, and `capture/SKILL.md` isn't touched by this change) — read as pre-existing free-tier-model
flakiness, not a regression this PR caused. `bootstrap`, `lint`, `attribute`, and even `roadmap` (the
documented known-flaky case) all passed in the same run. The same run also surfaced step 4's matrix-wiring
gap (see that step's update) — re-triggered again after fixing it; not yet confirmed.

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
