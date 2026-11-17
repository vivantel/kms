---
name: attribute
description: "Write commit messages and PR descriptions that lead with intent (why, not what), using Conventional Commits type prefixes and Refs: trailers linking to docs/{facts,decisions,guardrails,skills}/ artifacts. Use when the user wants to commit changes with attribution, or generate a PR description, e.g. \"commit this with attribution\", \"write a PR description for this branch\"."
---

Write commit messages and PR descriptions that capture *why* a change was made, not just what changed, and keep them traceable to the knowledge artifacts (`docs/{facts,decisions,guardrails,skills}/`) they implement.

This skill only runs when explicitly invoked. Never apply its conventions to a plain `git commit` unless asked.

## Writing a commit message

1. Run `git diff --staged` yourself; never ask the user for the changes. If nothing is staged, say so and stop.
2. Search `docs/{facts,decisions,guardrails,skills}/` for artifacts the diff touches or implements. If one or more clearly match, use them: list them in the trailers. Ask the user (once, before committing) only when candidates conflict or none clearly match.
3. Draft the message:
   - Summary line: `type: summary`, where `type` is one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
   - Blank line.
   - A body paragraph explaining the intent — not merely what changed.
   - Blank line.
   - One `Refs: <repo-relative-path>` git trailer per chosen artifact (e.g. `Refs: docs/decisions/000X-slug.md`). Never use an issue number or a prose mention in place of this trailer. Omit only if no artifact applies.
4. Run `git commit` with that message.

## Writing a PR description

1. Determine the branch's base (e.g. `main`) and run `git log <base>..HEAD`.
2. Build the `Refs` section by collecting the union of `Refs:` trailers already present on those commits. Do not re-inspect the full branch diff or re-ask the user — the commits are the source of truth.
3. Render three sections:
   - `Intent` — drawn from the commits' body paragraphs.
   - `What changed` — a brief factual summary.
   - `Refs` — the collected artifact paths.
