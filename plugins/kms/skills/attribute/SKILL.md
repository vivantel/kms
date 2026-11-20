---
name: attribute
description: "Write commit messages and PR descriptions that lead with intent (why, not what), using Conventional Commits type prefixes and Refs: trailers linking to docs/{facts,decisions,guardrails,skills}/ artifacts. Use when the user wants to commit changes with attribution, or generate a PR description, e.g. \"commit this with attribution\", \"write a PR description for this branch\"."
---

Commit messages and PR descriptions that lead with *why* and trace to `docs/{facts,decisions,guardrails,skills}/` artifacts. Runs only when invoked; never apply to a plain `git commit`.

## Commit

1. `git diff --staged` yourself; never ask for the changes. Nothing staged: say so, stop.
2. Find artifacts the diff touches or implements. Use clear matches; ask once, before committing, only if candidates conflict or none clearly match.
3. Message: `type: summary` (`feat|fix|docs|style|refactor|perf|test|build|ci|chore`), blank line, body on intent (not what), blank line, one `Refs: <repo-relative-path>` trailer per artifact (never an issue number or prose; omit only if none apply).
4. `git commit` with it.

## PR description

1. `git log <base>..HEAD`.
2. `Refs` = union of the commits' `Refs:` trailers; don't re-inspect the diff or re-ask.
3. Sections: `Intent` (from commit bodies), `What changed` (brief, factual), `Refs`.
