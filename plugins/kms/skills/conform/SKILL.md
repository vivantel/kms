---
name: conform
description: Checks whether a pending changeset conforms to existing decisions and guardrails before it lands. Use before committing or merging, e.g. "does this diff conform to our guardrails", "check this PR against what we've decided", "conform check the last 3 PRs".
---

Given a pending changeset, flag anything in it that violates an existing guardrail — before it's committed or merged. Read-only: reports findings, never edits the changeset or the knowledge base.

## Determining the target

No argument and something's staged: the staged diff (`git diff --staged`). No argument and nothing's staged: the diff against the branch's upstream/base. A number ("last 3 PRs", "last 5 commits"): resolve to that many merged PRs or commits and diff across the combined range. A branch name, commit range, or PR reference: use it directly.

## Checking conformance

1. Search `docs/{decisions,guardrails}/` for anything relevant to what the diff touches — by keyword, topic, path overlap, the same approach `query` uses.
2. For each relevant guardrail, check whether the diff's actual changes appear to violate it. Cite the guardrail by path; cite the decision behind it too, for context on *why*, the same way `query` cites a superseding decision alongside the original.
3. If nothing relevant is found, say so plainly rather than implying the knowledge base had an opinion it doesn't.
4. Report every finding — don't stop at the first. Group by guardrail violated, one line per finding with the file/hunk and what's wrong.

## Out of scope

Changes to the knowledge base's own artifacts (`docs/{facts,decisions,guardrails,skills}/`) — that's `lint`/`capture`'s job, not this skill's; if the diff touches those, say so and defer, don't check them here. Fixing anything — this skill only reports. Planning a refactor (`refactor-plan`) or drafting a commit message (`attribute`) — this skill checks a diff that already exists, for any reason, not just a refactor, and never writes prose about it.
