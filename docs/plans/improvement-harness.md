# Improvement Harness Implementation Plan

**Status Legend**: `[ ]` pending | `[~]` in progress | `[x]` done | `[!]` blocked

## Phase 0: Foundation (Prerequisites)

- [ ] **0.1** Verify OpenCode CLI supports `opencode agent <name> --prompt "<...>"` headless invocation
- [ ] **0.2** Add OpenCode to GitHub Actions setup (CI prerequisite)
- [ ] **0.3** Create `.opencode/improvement.yaml` with MVP config (lint-fix + skill-rewrite only)

## Phase 1: Orchestrator & Bootstrap

- [ ] **1.1** Create `plugins/kms/hooks/improvement-runner.sh`
  - [ ] Git worktree creation from `baseline_ref` (tag/commit)
  - [ ] Pinned skill copy (subagents + shipped skills + shared)
  - [ ] Worktree cleanup on exit (trap)
- [ ] **1.2** Implement unified queue discovery
  - [ ] Lint adapter: run `lint`, parse violations → queue items
  - [ ] Eval adapter: run promptfoo for changed skills → queue items
  - [ ] Capture adapter: run `capture` drift detection → queue items (deferred to v0.2)
  - [ ] Priority queue (JSON file in worktree)
- [ ] **1.3** Implement convergence loop
  - [ ] Outer loop: improvement types in priority order
  - [ ] Inner loop: passes with re-discovery
  - [ ] Semantic hash computation (markdown AST)
  - [ ] Convergence detection (metrics + hash)
  - [ ] Max passes enforcement (3)

## Phase 2: Lint-Fix Subagent (MVP Core)

- [ ] **2.1** Create `.opencode/agent/improve/improve-lint-fix.md`
  - [ ] Instructions for each violation category (token economy, structure, xrefs, formatting, derivation, tags)
  - [ ] Tool declarations (read, write, edit, grep, glob, bash)
  - [ ] Model preferences (free tier)
- [ ] **2.2** Implement fix patterns for each violation type
  - [ ] Token economy: tighten prose, remove restatement
  - [ ] Structure: add missing frontmatter fields
  - [ ] Cross-refs: fix broken links, update stale IDs
  - [ ] INDEX.md: sync CSV rows
  - [ ] Derivation: add missing governed-by/grounded-in/derivation-note
  - [ ] Tags: replace non-canonical tags
- [ ] **2.3** Verify: run `lint` on fixed files, retry on failure (max 3)
- [ ] **2.4** Auto-commit with attribute-format message + Refs: trailers

## Phase 3: Skill-Rewrite Subagent (MVP Core)

- [ ] **3.1** Create `.opencode/agent/improve/improve-skill-rewrite.md`
  - [ ] Instructions for clarity, structure, token economy, completeness, agent neutrality
  - [ ] Preserve: name, description, triggers, core workflow, agent overrides
  - [ ] Update colocated `examples.md`
- [ ] **3.2** Implement eval gate integration
  - [ ] Invoke promptfoo for the specific skill's eval case
  - [ ] Parse pass rate and score
  - [ ] Compare against baseline
- [ ] **3.3** Auto-commit decision logic
  - [ ] If eval pass + lint pass + score improvement ≥ 5% → commit
  - [ ] Else → stage + log for review
- [ ] **3.4** Commit message with Refs: to eval harness decision and scope decision

## Phase 4: Verification & Observability

- [ ] **4.1** Implement three-layer verification in orchestrator
  - [ ] Lint gate (all types)
  - [ ] Eval gate (skill-rewrite)
  - [ ] Sampling gate (deferred)
- [ ] **4.2** Implement improvement log (`docs/improvement-log.md`)
  - [ ] Structured append-only entries
  - [ ] Machine-parseable format (YAML frontmatter + markdown body)
- [ ] **4.3** Implement CI verification gate (GitHub Actions)
  - [ ] Job triggered on push to main (after scheduled run)
  - [ ] Verify auto-commit file scope, lint pass, eval pass, commit format
  - [ ] Fail with annotation on anomaly

## Phase 5: Integration & Polish

- [ ] **5.1** Create skill interface: `plugins/kms/skills/improvement-harness/SKILL.md` + `examples.md`
- [ ] **5.2** Create KB procedure: `docs/skills/improvement-harness.md`
- [ ] **5.3** Update `plugins/kms/skills/index.json` (Kilo remote-skills index)
- [ ] **5.4** Update `plugins/kms/hooks/hooks.json` (optional: SessionStart hook for harness)
- [ ] **5.5** Update `uninstall` skill to remove harness artifacts
- [ ] **5.6** End-to-end test: scheduled run on this repo, verify commits, log, CI gate

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
