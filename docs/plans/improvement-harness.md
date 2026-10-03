# Improvement Harness Implementation Plan

**Status Legend**: `[ ]` pending | `[~]` in progress | `[x]` done | `[!]` blocked

## Phase 0: Foundation (Prerequisites)

- [x] **0.1** Verify OpenCode CLI supports `opencode agent <name> --prompt "<...>"` headless invocation
- [x] **0.2** Add OpenCode to GitHub Actions setup (CI prerequisite)
- [x] **0.3** Create `.opencode/improvement.yaml` with MVP config (lint-fix + skill-rewrite only)

## Phase 1: Orchestrator & Bootstrap

- [x] **1.1** Create `plugins/kms/hooks/improvement-runner.sh`
  - [x] Git worktree creation from `baseline_ref` (tag/commit)
  - [x] Pinned skill copy (subagents + shipped skills + shared)
  - [x] Worktree cleanup on exit (trap)
- [x] **1.2** Implement unified queue discovery
  - [x] Lint adapter: run `lint`, parse violations → queue items
  - [x] Eval adapter: run promptfoo for changed skills → queue items
  - [ ] Capture adapter: run `capture` drift detection → queue items (deferred to v0.2)
  - [x] Priority queue (JSON file in worktree)
- [x] **1.3** Implement convergence loop
  - [x] Outer loop: improvement types in priority order
  - [x] Inner loop: passes with re-discovery
  - [x] Semantic hash computation (markdown AST)
  - [x] Convergence detection (metrics + hash)
  - [x] Max passes enforcement (3)

## Phase 2: Lint-Fix Subagent (MVP Core)

- [x] **2.1** Create `.opencode/agent/improve/improve-lint-fix.md`
  - [x] Instructions for each violation category (token economy, structure, xrefs, formatting, derivation, tags)
  - [x] Tool declarations (read, write, edit, grep, glob, bash)
  - [x] Model preferences (free tier)
- [x] **2.2** Implement fix patterns for each violation type
  - [x] Token economy: tighten prose, remove restatement
  - [x] Structure: add missing frontmatter fields
  - [x] Cross-refs: fix broken links, update stale IDs
  - [x] INDEX.md: sync CSV rows
  - [x] Derivation: add missing governed-by/grounded-in/derivation-note
  - [x] Tags: replace non-canonical tags
- [x] **2.3** Verify: run `lint` on fixed files, retry on failure (max 3)
- [x] **2.4** Auto-commit with attribute-format message + Refs: trailers

## Phase 3: Skill-Rewrite Subagent (MVP Core)

- [x] **3.1** Create `.opencode/agent/improve/improve-skill-rewrite.md`
  - [x] Instructions for clarity, structure, token economy, completeness, agent neutrality
  - [x] Preserve: name, description, triggers, core workflow, agent overrides
  - [x] Update colocated `examples.md`
- [x] **3.2** Implement eval gate integration
  - [x] Invoke promptfoo for the specific skill's eval case
  - [x] Parse pass rate and score
  - [x] Compare against baseline
- [x] **3.3** Auto-commit decision logic
  - [x] If eval pass + lint pass + score improvement ≥ 5% → commit
  - [x] Else → stage + log for review
- [x] **3.4** Commit message with Refs: to eval harness decision and scope decision

## Phase 4: Verification & Observability

- [x] **4.1** Implement three-layer verification in orchestrator
  - [x] Lint gate (all types)
  - [x] Eval gate (skill-rewrite)
  - [ ] Sampling gate (deferred)
- [x] **4.2** Implement improvement log (`docs/improvement-log.md`)
  - [x] Structured append-only entries
  - [x] Machine-parseable format (YAML frontmatter + markdown body)
- [x] **4.3** Implement CI verification gate (GitHub Actions)
  - [x] Job triggered on push to main (after scheduled run)
  - [x] Verify auto-commit file scope, lint pass, eval pass, commit format
  - [x] Fail with annotation on anomaly

## Phase 5: Integration & Polish

- [x] **5.1** Create skill interface: `plugins/kms/skills/improvement-harness/SKILL.md` + `examples.md`
- [x] **5.2** Create KB procedure: `docs/skills/improvement-harness.md`
- [x] **5.3** Update `plugins/kms/skills/index.json` (Kilo remote-skills index)
- [x] **5.4** Update `plugins/kms/hooks/hooks.json` (optional: SessionStart hook for harness)
- [x] **5.5** Update `uninstall` skill to remove harness artifacts
- [x] **5.6** End-to-end test: scheduled run on this repo, verify commits, log, CI gate

## Phase 6: v0.2+ (Deferred)

- [ ] KB-repair subagent (contradictions, stale facts, gaps)
- [ ] Guardrail-update subagent (re-derivation)
- [ ] Event-driven trigger (GitHub Actions on push/PR)
- [ ] Dashboard generation from improvement log
- [ ] Layered configuration (project/user/global)
- [ ] Multi-repo support (harness as installed plugin)

## Done-When Criteria

The plan is complete when:
1. A scheduled run executes on this repo, produces auto-commits for lint fixes and skill rewrites
2. All auto-commits pass the CI verification gate
3. `docs/improvement-log.md` has structured entries for each run
4. The harness's own subagents and config pass `lint` and are token-economical
5. `opencode agent improve-harness` works manually
6. `uninstall` skill can remove all harness artifacts

(End of file - total 100 lines)