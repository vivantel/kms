---
name: attribute
description: "Write commit messages and PR descriptions that lead with intent (why, not what), using Conventional Commits type prefixes and Refs: trailers linking to docs/{facts,decisions,guardrails,skills}/ artifacts. Use when the user wants to commit changes with attribution, or generate a PR description, e.g. \"commit this with attribution\", \"write a PR description for this branch\"."
---

Write commit messages and PR descriptions that capture *why* a change was made, not just what changed, and keep them traceable to the knowledge artifacts (`docs/{facts,decisions,guardrails,skills}/`) they implement.

This skill only runs when explicitly invoked. Never apply its conventions to a plain `git commit` unless asked.

## Writing a commit message

1. Inspect the staged diff with `git diff --staged`.
2. Propose one or more candidate knowledge artifacts the change appears to relate to, based on what the diff touches. Confirm the candidate list with the user before committing — never guess silently, and let the user add, remove, or reject all candidates.
3. Draft the message:
   - Summary line: `type: summary`, where `type` is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
   - Blank line.
   - A body paragraph explaining the *why* — the intent or rationale behind the change. A message that only restates what changed, with no why, does not satisfy this skill.
   - Blank line.
   - One `Refs: <repo-relative-path>` git trailer per confirmed artifact (e.g. `Refs: docs/decisions/0003-commit-trailer-traceability.md`). Never use an issue number or a prose mention in place of this trailer.

## Writing a PR description

1. Determine the branch's base (e.g. `main`) and run `git log <base>..HEAD`.
2. Build the `Refs` section by collecting the union of `Refs:` trailers already present on those commits. Do not re-inspect the full branch diff or re-ask the user — the commits are the source of truth.
3. Render three sections:
   - `Why` — the intent, drawn from the commits' Why-bodies.
   - `What changed` — a brief factual summary.
   - `Refs` — the collected artifact paths.
