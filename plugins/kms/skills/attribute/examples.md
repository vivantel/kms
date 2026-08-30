# `attribute` examples

## 1. Committing with attribution

**Prompt:** "Commit this with attribution."

**What happens:** The staged diff is inspected, candidate knowledge artifacts it likely implements are proposed and confirmed with the user, then a message is drafted: `type: summary`, a body paragraph on intent (not just what changed), and one `Refs: docs/decisions/00XX-....md` trailer per confirmed artifact — never an issue number or prose mention in its place.

## 2. Writing a PR description

**Prompt:** "Write a PR description for this branch."

**What happens:** The branch's commits since its base are read via `git log <base>..HEAD`. The `Refs` section is the union of `Refs:` trailers already on those commits — the diff isn't re-inspected and the user isn't re-asked, since the commits are the source of truth. Three sections come back: `Intent`, `What changed`, `Refs`.

## 3. A plain commit, not asked for

**Prompt:** "git commit -m 'fix typo'"

**What happens:** Nothing — `attribute`'s conventions only apply when explicitly invoked, never layered onto an ordinary `git commit` the user didn't ask to have attributed.
