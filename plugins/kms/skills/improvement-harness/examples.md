# Improvement Harness Examples

## Example 1: Manual Full Run

**Trigger:** "run the improvement harness"

**Interaction:**
```
User: run the improvement harness
Harness: Starting manual improvement harness run...
         Baseline: 0.15.0 (4cdd5bb)
         Worktree: /tmp/kms-improve-xyz123
         Mode: manual
         
         Discovering queue items...
         - Lint scan: 3 violations found (2 token-economy, 1 structure)
         - Eval scan: 1 skill below baseline (roadmap: 0.72 pass rate)
         
         Queue: 4 items (3 lint-fix, 1 skill-rewrite)
         
         Pass 1 (lint-fix):
         - Fixed token-economy in docs/facts/0003-commit-trailer-traceability.md
         - Fixed structure in docs/decisions/0012-guardrail-derivation.md
         - Fixed token-economy in plugins/kms/skills/clarify/SKILL.md
         Lint gate: all 3 passed
         Committed: 3 fixes
         
         Pass 1 (skill-rewrite):
         - Rewrote plugins/kms/skills/roadmap/SKILL.md
         Lint gate: passed
         Eval gate: pass_rate 0.72 → 0.89 (+0.17), score improvement 23% ≥ 5%
         Committed: 1 rewrite
         
         Convergence: semantic hash stable, metrics improved
         Total commits: 4
         
         Logged to docs/improvement-log.md
         Run complete.
```

**Result:** 4 auto-commits with `fix:` and `refactor:` types, each with `Refs:` trailers linking to modified artifacts.

---

## Example 2: Scheduled Daily Run (CI)

**Trigger:** GitHub Actions cron at 02:00 UTC

**Interaction:**
```
GitHub Actions: Running scheduled improvement harness...
                Baseline: latest-tag (0.15.0)
                Mode: scheduled
                Dry-run: false
                
                No new lint violations since last run.
                No eval regressions detected.
                Queue empty — nothing to do.
                
                Run complete (0 commits).
                CI verification gate: passed (no commits to verify)
```

**Result:** No commits, log entry appended noting empty queue.

---

## Example 3: Event-Driven Run on Push

**Trigger:** Push to master with changes to `plugins/kms/skills/lint/SKILL.md`

**Interaction:**
```
GitHub Actions: Running event-driven improvement harness...
                Baseline: latest-tag (0.15.0)
                Mode: event
                Changed files: plugins/kms/skills/lint/SKILL.md
                
                Discovering queue items for changed files...
                - Lint scan on lint/SKILL.md: 1 token-economy violation
                - Eval scan for lint skill: pass_rate 0.95 (baseline 0.95)
                
                Queue: 1 lint-fix item
                
                Pass 1 (lint-fix):
                - Fixed token-economy in plugins/kms/skills/lint/SKILL.md
                Lint gate: passed
                Committed: 1 fix
                
                Convergence: achieved in 1 pass
                Total commits: 1
                
                CI verification gate:
                - Commit format: ✓ Conventional Commits + Refs trailer
                - File scope: ✓ only plugins/kms/skills/lint/SKILL.md
                - Lint gate: ✓ clean
                - Eval gate: N/A (lint-fix only)
                All gates passed.
```

**Result:** 1 auto-commit fixing the introduced violation, all CI gates pass.

---

## Example 4: Dry Run for Testing

**Trigger:** "run the improvement harness in dry-run mode"

**Interaction:**
```
User: run the improvement harness in dry-run mode
Harness: Starting manual improvement harness run (DRY RUN)...
         Baseline: 0.15.0 (4cdd5bb)
         Worktree: /tmp/kms-improve-abc456
         Mode: manual
         Dry-run: true
         
         Would discover: 2 lint-fix items, 1 skill-rewrite item
         Would process: lint-fix pass (2 items), skill-rewrite pass (1 item)
         Would commit: 3 commits (but dry-run, so no merge)
         
         Dry run complete. No changes pushed to main worktree.
```

**Result:** Log entry showing what would happen, no commits, no merge.

---

## Example 5: Skill-Rewrite Requires Human Review

**Trigger:** "run the improvement harness" (when eval gate fails)

**Interaction:**
```
Harness: ...skill-rewrite pass...
         Rewriting plugins/kms/skills/brainstorm/SKILL.md
         Lint gate: passed
         Eval gate: FAILED — pass_rate dropped from 0.85 to 0.78 (regression)
         
         Skill-rewrite staged for human review:
         - Changes saved to worktree branch: improvement-harness-1728000000
         - Logged escalation: eval regression
         
         Commit NOT auto-applied. Review with:
           git fetch origin improvement-harness-1728000000
           git diff improvement-harness-1728000000
```

**Result:** Changes staged in separate branch, logged for review, no auto-commit.