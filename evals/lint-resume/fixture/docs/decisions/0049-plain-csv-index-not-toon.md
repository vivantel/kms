---
id: 0049-plain-csv-index-not-toon
title: Define the per-type index as plain, strictly-specified CSV, not TOON
status: active
date: 2026-09-12
tags: [kms, knowledge-management, scale, eval-harness]
track: process
---

## Decision

Supersedes `docs/decisions/archive/0041-index-and-archive-for-scale.md`'s choice of TOON for
`docs/{facts,decisions,guardrails,skills}/INDEX.md`. The per-type index and archive mechanism
`0041` introduced are unchanged; only the index's row format changes:

- The format is now defined once, in `plugins/kms/shared/artifact-model.md`, as plain CSV: a
  header line naming the fields (`id, title, tags, status`), then one comma-separated row per
  artifact. A field containing a comma (the only case that occurs today — `tags`) is wrapped in
  double quotes, with its items comma-separated inside the quotes, e.g. `"kms, naming, branding"`.
  A `;`-separated fallback inside quotes is named for a future field that can't just be
  comma-separated, though nothing has needed it yet.
- `bootstrap` (seeding the index) and `roadmap` (updating a row after writing an artifact) both
  point at that one definition by sibling reference instead of each restating it — the three
  near-identical copies this replaced were themselves a real, if minor, token-economy defect
  (`docs/guardrails/token-economy.md`).
- Every `INDEX.md` file's own heading (e.g. `# Facts index (TOON)`) is relabeled `(CSV)` to match.

## Why

`0041` picked TOON specifically for its "low-punctuation-overhead encoding," while flagging its
own risk: "TOON is a comparatively new format; whoever implements the index-generation logic
should verify the current spec rather than assume this decision pins exact syntax." That
verify-the-spec instruction, taken literally in `bootstrap/SKILL.md`, caused a real, observed
failure: a smaller model, unfamiliar with the name "TOON," repeatedly went looking for it
(external fetches to `toonformat.dev`, then local greps for "TOON refs" across sibling skill
files) before it would write the index at all — burning eval time and tokens on format research
for a one-time, small write, not the repeated cheap reads the format was chosen to optimize.

Inlining a definition of TOON syntax under its own name (an earlier fix, `plugins/kms/skills/
bootstrap/SKILL.md`'s step 10) only partly closed this: a model that *does* recognize "TOON"
still has reason to second-guess whether the inlined description is a faithful, complete
subset of the real spec, since the name itself claims conformance to something external.
Naming the format at all invites exactly the verification behavior `0041` warned about and this
session observed.

Auditing every `INDEX.md` actually produced under `0041` (five files, all of `docs/{facts,skills,
guardrails,decisions}/INDEX.md` plus `docs/facts/archive/INDEX.md`) shows none of them use any
TOON feature beyond what plain CSV already expresses: the only multi-value field, `tags`, is
written as ordinary CSV-quoted-comma-in-cell, not TOON's nested-array/object syntax. TOON's actual
differentiator (compact nested-object encoding without full JSON/YAML punctuation) is unused
here — the format's only observed effect on this project is import/verification overhead, not
density.

Plain CSV is not a new format under any name — the strict grammar above matches every
`INDEX.md` on disk byte-for-byte, needs no external reference to write or verify, and preserves
`0041`'s actual point (a compact, cheap-to-read table beats reading every file). Should a genuine
nested-value need show up later, the same CSV-quoting rule already covers it (quote the cell, pick
an inner separator); adopting TOON's fuller grammar at that point would be a new, separately
justified decision, not a reversion to this one.

## Tradeoffs considered

- **Keep TOON, just describe it better (this session's earlier, superseded fix)**: cheaper to
  write than this decision, but doesn't remove the root cause — naming an external spec still
  invites a model to verify conformance to it, regardless of how complete the inlined description
  is.
- **Markdown table index**: `0041` already rejected this, for the same reason it still holds —
  table markup overhead is exactly the cost the index exists to avoid at scale. Not revisited
  here.
- **Chosen: plain, strictly-specified CSV, defined once in `artifact-model.md` and referenced by
  sibling reference from `bootstrap`/`roadmap`; every `INDEX.md` heading relabeled to match.**
