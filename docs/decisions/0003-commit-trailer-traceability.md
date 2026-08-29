---
id: 0003-commit-trailer-traceability
title: Use a "Refs:" git trailer to link commits to knowledge artifacts, one-directionally
status: accepted
date: 2026-07-29
tags: [kms, git, traceability]
---

## Decision

A commit that implements or relates to a knowledge artifact carries one
`Refs: <repo-relative-path>` git trailer per referenced artifact, e.g.:

```
Refs: docs/decisions/0003-commit-trailer-traceability.md
```

This is a standard git trailer (same mechanism as `Co-authored-by:`),
parseable with `git log --pretty` / `git interpret-trailers`. The value is
the artifact's repo-relative file path, not a minted ID.

Traceability is **one-directional**: commit → artifact only. Artifact
files do not carry a backlink list of the commits that reference them. To
go artifact → commits, run:

```
git log --all --grep="Refs: docs/path/to/artifact.md"
```

## Why

A path-based trailer needs no extra id-minting step on every artifact (the
alternative — giving every artifact a stable short id in frontmatter, then
referencing the id — was rejected as unnecessary overhead for a repo this
size). A free-text "Relates to: ..." footer was rejected because it isn't
machine-parseable by standard git tooling, which would weaken the
`changelog` skill's ability to extract references reliably.

Bidirectional backlinks were rejected because they would require the
`attribute` skill to edit knowledge-artifact files on every commit, and
those lists can drift or duplicate under rebase/amend. `git log --grep` is
cheap enough on demand that the write-on-every-commit cost isn't worth it.

## Tradeoffs considered

- **Frontmatter `id:` + `Refs: <id>` trailer**: survives file renames, but
  requires minting and maintaining ids.
- **Free-text footer mention**: easiest to write, not machine-parseable.
- **Chosen: `Refs: <repo-relative-path>` git trailer**, one-directional.
- **Bidirectional backlinks in artifact frontmatter**: rejected — extra
  writes on every commit, drift risk under rebase/amend.
