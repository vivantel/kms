---
id: 0056-chunked-checkpointed-execution-for-bootstrap-and-lint
title: Give bootstrap and lint a chunked, checkpointed execution mode so neither requires one unbroken pass
status: active
date: 2026-09-13
tags: [kms, knowledge-management, scale, checkpointing, eval-harness]
track: process
governed-facts: [0015-checkpoint-file-location-and-lifecycle, 0016-chunk-sizing-parameters, 0017-bootstrap-history-scope-selection-values]
---

## Decision

`bootstrap` and `lint` both execute as chunked, self-checkpointing passes instead of one unbroken run:

- **Shared convention**: `plugins/kms/shared/checkpointing.md` defines the checkpoint file format and
  resume protocol once; both `bootstrap/SKILL.md` and `lint/SKILL.md` reference it, the same way both
  already reference `shared/artifact-model.md`.
- **lint, two phases**: Phase A pages every per-file check (missing fields, dangling references,
  verbosity, etc.) by artifact type (`facts/`, `decisions/`, `guardrails/`, `skills/`), accumulating
  files in stable alphabetical order until an estimated token budget is hit (`0016-...`), checkpointing
  after each page. A single file over budget gets a one-file page of its own rather than ever being
  split mid-file. Phase B runs once, after every Phase A page completes, for the small set of checks that
  need a second, specific project artifact identified only from Phase A's own findings (stale-derived-
  artifact, cross-artifact contradiction, role-gone-cold, archive-candidate's repo-wide reference search):
  these shortlist candidates first from the already-cheap `INDEX.md` tables — matching `docs/decisions/
  archive/0041-...`'s existing tag-scoping design — then open only the shortlisted files, itself paged the
  same way if the shortlist is large. Every other check (including tag-gone-cold and numbering-collision
  checks, both resolvable from a type's own `INDEX.md` with no further file opens) stays in Phase A.
- **bootstrap, two phases**: Phase A chunks steps 1–5 (git-history mining, fact/guardrail/doc
  extraction) — git-history mining walks the log oldest-first, same token-budget accumulation, checkpoint
  records the last completed commit SHA (`0016-...`); extraction pages by file exactly like lint's
  Phase A. Phase B runs steps 6–10 (skill-gap detection, role/tag compilation, template seeding,
  `AGENTS.md` wiring, index seeding) once, as a single final aggregation pass, since those steps consume
  Phase A's aggregate output and don't chunk meaningfully on their own.
- **Checkpoint state**: `docs/.kms-checkpoints/<skill>-<run-id>.md`, checked in — path/lifecycle details
  in `0015-...`. Findings (lint) or progress offsets (bootstrap — the actual output is the stub files
  already written to their real paths) accumulate inline in the checkpoint, grouped by check, so a
  resume never needs to reconstruct prior results.
- **Resume protocol**: a checkpoint's existence on a new invocation triggers a resume-or-discard
  question to the confirming party, never silent auto-resume. Resuming first re-lists the recorded
  files/commits and compares against the checkpoint's item manifest. For file-based paging, any
  difference (a file added/removed) forces a fresh start instead of trusting a possibly-stale offset. For
  git-history paging, new commits landing at the tip don't invalidate already-mined, immutable history —
  only a rewritten history (rebase/force-push) forces a fresh start there.
- **Cleanup**: the checkpoint file is deleted automatically as the run's last action on success. A
  leftover checkpoint therefore always means, unambiguously, an interrupted run.
- **User-facing behavior**: unchanged for the normal, uninterrupted case — one invocation, the agent
  loops through chunks internally, reports the same final output as today. The one deliberate exception:
  `bootstrap` now asks up front how much git history to mine (`0017-...`), a new question independent of
  the chunking mechanism's own invisibility.
- **Eval harness**: the existing `evals/bootstrap` and `evals/lint` cases (which test "does the skill do
  its job") are unchanged. Each gets a new, separate resume-specific case — a shortened `timeout_seconds`
  forces a kill mid-run, the runner restarts against the same fixture, and the case asserts completion
  plus no duplicated stubs/findings.

This resolves the scaling gap `docs/decisions/archive/0041-index-and-archive-for-scale.md` left open —
that decision's own text says outright that `lint`'s structural checks "inherently require opening every
file they validate, index or not," meaning the index/archive work already done reduces retrieval cost but
puts no ceiling on a full-repo `lint` or `bootstrap` pass.

## Why

Two concrete data points already show this isn't a hypothetical scaling concern. `bootstrap`'s own eval
case needed `timeout_seconds` raised to 1440 (24 minutes) even against a tiny synthetic fixture
(`docs/plans/archive/eval-harness-baseline-reliability.md`), and `0041-...` names the exact mechanism
(no-ceiling per-file structural checks) that makes a real project — hundreds to thousands of artifacts,
or a large unfamiliar git history — hit that wall harder than the eval fixture already does. Chunking
plus checkpointing is the direct fix: bound each unit of work to a token budget the runner can reliably
finish, and make an interruption (timeout, context limit, a killed process) lose at most one chunk's
worth of work instead of the entire pass.

The two-phase split (per-file phase, then an index-narrowed relational phase) exists because most of
`lint`'s and `bootstrap`'s checks are genuinely per-file (or resolvable from a type's own cheap `INDEX.md`
with no further opens) and can page cleanly, but a real minority (contradiction-scanning, stale-derived-
artifact, role-gone-cold, archive-candidate's repo-wide search) need to open a second, specific file that
may land on different pages under simple sequential paging — folding them into the same per-file pages
risks re-opening already-paged files or missing a contradiction between page 1 and page 40 entirely. A
separate relational phase, narrowed first by the cheap `INDEX.md` tables the same way `0041-...` already
narrows contradiction-scoping by tag, avoids both problems without inventing a new retrieval mechanism.

Checking the checkpoint file into git (rather than a gitignored scratch file) is what makes cross-session
resume actually possible: a different session, a different machine, or a crashed process can all pick up
an interrupted run by reading the same file a fresh invocation would find. The resume-or-discard question
and the re-verification-before-resume step both exist because a stale checkpoint is a real correctness
risk, not just a UX nicety — silently trusting an old offset against a docs/ tree or git history that's
since changed could skip newly-added files or misalign an offset with no warning at all.

Keeping the uninterrupted case's user-facing behavior identical to today matters because this plan is
adding infrastructure whose entire payoff is in the interrupted path — a chattier "chunk 3/12 done" style
of output for every run would be a new interaction pattern imposed on the common case to serve the rare
one. Making the checkpointing convention shared (`shared/checkpointing.md`) rather than reinventing it per
skill follows the same reasoning `artifact-model.md` already established: identical, same-voice content
read by more than one skill body belongs in one file, not duplicated and left to drift.

## Tradeoffs considered

- **Chunk by fixed file count, not token budget**: simpler to implement, but a directory of unevenly
  sized files (a terse fact next to a long guardrail with a full derivation section) either wastes budget
  on small pages or blows it on large ones — token-budget accumulation adapts to actual file size instead
  of guessing a flat count.
- **Chunk by check number instead of by file/type**: maps cleanly onto lint's own enumerated checklist,
  but most checks need to open the same files repeatedly across different checks — chunking this way
  means re-reading the whole corpus once per check instead of once per file, the opposite of the point.
- **Fold relational checks into the same per-type pages, best-effort**: one phase instead of two, but a
  contradiction spanning two pages could be missed or force re-opening already-paged files — the
  two-phase split with index-narrowed shortlisting avoids both at a small added-complexity cost.
- **Gitignored, local-only checkpoint file**: never pollutes the adopting project's tracked tree, but a
  checkpoint only visible to the machine that wrote it can't be resumed by a different session or after
  `git clean` — defeats the point of checkpointing for anything but a same-machine retry.
- **Always auto-resume a found checkpoint, no question asked**: never interrupts the user with a
  mechanical question, but risks silently continuing a stale or now-invalid run with no signal that
  anything unusual is happening.
- **Chosen**: token-budget-based two-level (type × page) chunking, shared checkpointing convention,
  checked-in checkpoint file, resume-or-discard with staleness re-verification, checkpoint deleted on
  success, uninterrupted-case behavior unchanged, new resume-specific eval cases alongside the existing
  ones.
