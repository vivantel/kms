---
id: 0036-standalone-installing-doc
title: Extract per-agent install steps into a standalone INSTALLING.md
status: accepted
date: 2026-08-30
tags: [kms, discoverability, packaging]
track: product
---

## Decision

Per-agent install steps (Claude Code, Codex, Kilo Code CLI) move out of
`README.md`'s prose "Installing" section into a standalone
`INSTALLING.md` at repo root, one `##` section per agent
(`#claude-code`, `#codex`, `#kilo-code-cli`) with a short nav list at
the top. `README.md`'s "Installing" section shrinks to a one-line
summary, a link to `INSTALLING.md`, and the Claude Code quick-start
only (since this repo is packaged and badged as a Claude Code plugin
marketplace first). Content lives in exactly one place — README doesn't
duplicate the Codex/Kilo steps, only points at them — so there's no
second copy for future edits to drift out of sync with.

## Why

Three agents' install instructions as consecutive prose paragraphs in
one README section weren't scannable for a newcomer looking for their
specific agent, and had no way to deep-link to just one agent's steps.
Per-agent `##` headers in a standalone file fix both: GitHub renders an
auto-ToC from them, they're grep/search-friendly, and each is a stable
anchor link. This was raised directly by the user after looking at the
rendered README — an earlier, informal in-conversation judgment call
("not worth a file split yet, content's still short") weighed content
*volume* and concluded three short sections could stay inline; the
actual problem turned out to be scannability of mixed prose regardless
of length, which volume-based reasoning didn't address. That earlier
judgment was never written down as a decision record, so there's
nothing to formally supersede — this is the first recorded decision on
the question.

## Tradeoffs considered

- **Keep inline in README**: rejected — the exact problem reported.
- **One file per agent** (`docs/installing/claude-code.md`, etc.):
  rejected — three agents don't need three files; a single file with
  `##` anchors already gives deep-linkability and scannability without
  spreading related content across a directory for no added benefit.
