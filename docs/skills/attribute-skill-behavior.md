---
id: attribute-skill-behavior
title: Procedural spec for the attribute skill
status: active
date: 2026-07-29
tags: [kms, git, procedural]
---

## Procedure

This describes how the `attribute` skill (to be implemented at
`plugins/kms/skills/attribute/SKILL.md`, see
`docs/plans/commit-pr-attribution-skills.md`) should decide and act. It is
the procedural counterpart to the decisions in
`docs/decisions/0002-commit-pr-attribution-skill-design.md`,
`docs/decisions/0003-commit-trailer-traceability.md`, and
`docs/decisions/0004-conventional-commits-adoption.md`, and the guardrail
in `docs/guardrails/commit-attribution-format.md`.

### Trigger

Explicit invocation only (e.g. "/kms:attribute", "write this commit with
attribution", "write a PR description for this branch"). Never fires
automatically on a plain `git commit`.

### Writing a commit message

1. Inspect the staged diff (`git diff --staged`).
2. Propose one or more candidate knowledge artifacts (from
   `docs/{facts,decisions,guardrails,skills}/`) that the change appears to
   relate to, based on what the diff touches.
3. Confirm the candidate list with the user before committing — do not
   guess silently. The user may add, remove, or reject all candidates.
4. Draft the message: `type: summary` line (type from the set in
   `docs/guardrails/commit-attribution-format.md`), a blank line, a Why
   paragraph, a blank line, then one `Refs: <path>` trailer per confirmed
   artifact.

### Writing a PR description

1. Determine the branch's base (e.g. `main`) and run
   `git log <base>..HEAD`.
2. Build the `Refs` section by collecting the union of `Refs:` trailers
   already present on those commits — do **not** re-inspect the full
   branch diff or re-ask the user; the commits are the source of truth.
3. Render three sections: `Why` (the intent, drawn from the commits' Why
   bodies), `What changed` (a brief factual summary), `Refs` (the
   collected artifact paths).

## Why this is procedural, not axiomatic

These are "how to decide/act" rules that operationalize decisions already
made elsewhere (cited above); they don't carry independent tradeoffs of
their own beyond what those decisions already settled.
