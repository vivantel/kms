---
id: improvement-harness-lint-fix
title: Lint auto-fix improvement skill
status: active
date: 2026-10-03
tags: ["kms", "improvement-harness", "lint-fix", "procedural"]
operationalizes: ["improvement-harness-lint-gate", "token-economy", "fact-governance-fields", "guardrail-derivation-fields", "tags-from-canonical-list"]
---

# Lint Auto-Fix Improvement Skill

Fixes mechanical lint violations detected by the `lint` skill. This is the highest-confidence, highest-volume improvement type.

## Scope

Fixes these violation categories:
- **Token economy**: verbose prose, restatement, excessive length in facts/guardrails/procedures
- **Structure**: missing frontmatter fields (id, title, status, date, tags, type-specific fields)
- **Cross-references**: broken decision/fact/guardrail links, stale IDs, missing INDEX.md rows
- **Formatting**: inconsistent CSV in INDEX.md, YAML frontmatter issues
- **Guardrail derivation**: missing `governed-by`, `grounded-in`, `derivation-note` fields
- **Tags**: tags not from canonical list (`tags.md`), missing tags

## What It Does Not Fix

- Semantic content changes (what a decision says, not how it's formatted)
- Contradiction resolution between artifacts
- Stale fact updates (requires human judgment)
- Skill body rewrites (handled by `skill-rewrite` type)

## Algorithm

For each queued lint violation:
1. Read the violating file and the lint output (violation type, location, suggestion)
2. Apply the minimal fix to resolve that specific violation
3. Re-run `lint` on the file to verify the fix
4. If clean, commit with message: `fix: resolve <violation-type> in <file>`

## Verification

- Lint gate only (no eval gate, no sampling)
- Auto-commits on pass
- Max 3 retries per violation with lint feedback

## Configuration

Registered in `.opencode/improvement.yaml`:
```yaml
- name: lint-fix
  subagent: improve-lint-fix
  auto_commit: true
  verification: [lint_gate]
```
