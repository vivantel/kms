---
id: 0041-index-and-archive-for-scale
title: Add a per-type TOON index and an archive mechanism for superseded/deprecated artifacts
status: active
date: 2026-09-01
tags: [kms, knowledge-management, scale]
track: process
---

## Decision

Two additions to the knowledge base's structure, aimed at a project with
a rich history (hundreds of artifacts), where full-repo reads and
pairwise scans stop being viable:

- **Per-type index** — `docs/{facts,decisions,guardrails,skills}/INDEX.md`,
  one compact row per artifact (`id`, `title`, `tags`, `status`), written
  in TOON (Token-Oriented Object Notation) rather than Markdown: its
  whole purpose is being cheap to read on every `query`/`onboard`
  invocation, so its own token cost matters more than any other file in
  the system. `capture` writes/updates entries as it drafts or edits an
  artifact; `lint` gains a check verifying the index matches its
  directory's actual contents. `query`/`onboard` read the index first
  and open only the files actually relevant, instead of reading every
  file in a directory. The index does not reduce `lint`'s own structural
  checks (dangling references, missing fields) — those inherently
  require opening every file they validate, index or not.
- **Archive** — any artifact reaching `status: superseded` or `status:
  deprecated` (`docs/decisions/0039-unify-lifecycle-and-drop-scope.md`)
  is a candidate to move to `docs/<type>/archive/`, filename and `id`
  unchanged, so every `governed-by`/`grounded-in`/`superseded-by`
  reference keeps resolving regardless of which side of the move it's
  on. `lint` gains a check proposing the move for any such artifact
  still in the live directory; nothing moves without human confirmation,
  matching every other `lint` finding's propose-don't-silently-fix
  behavior. `lint`'s default invocation scans only the live (non-archived)
  set; archived artifacts are validated on a separate, explicitly-invoked
  deep pass, not every routine run.

A vector/embeddings-based search layer is deliberately not built as part
of this decision. The index's structured, one-row-per-artifact format is
designed to also serve as a reasonable feed for a future semantic-search
layer without revisiting this decision, but building one is left fully
optional, decided per project — not something `kms` itself ships or
requires.

## Why

Two skills read the *entire* knowledge base today: `lint`'s full scan
and `onboard`'s "read all four artifact directories." That's linear
token cost in corpus size with no ceiling — tolerable at dozens of
files, a real cost (and eventually a context-limit) problem at hundreds.
An index turns "read everything to find the 5 relevant files" into
"read one cheap table, open 5 files."

This is a materialized cache, not the kind of stored rollup
`docs/decisions/0038-track-field-mutual-exclusivity.md` rejected. `0038`
ruled out storing a *computed judgment* with no single source file
behind it (a `both` track value synthesizing several decisions at
once) — the index instead mirrors fields that already exist, verbatim,
in one file each, and `lint`'s new check 19 exists specifically to
catch drift between the copy and the source, the same role check 12
already plays for `kms-seeded` templates. Reading frontmatter directly
every time, with no cache, avoids the sync question entirely but
reintroduces the exact full-read cost this decision exists to remove —
a checked cache is the standard resolution to that tradeoff, not an
exception to `0038`'s reasoning about not inventing ungrounded values.

TOON specifically, not another Markdown table, because the index's one
job is being read often and cheaply — the exact case TOON's tabular,
low-punctuation-overhead encoding was built for, and unlike adopting a
CI/eval tool, it costs nothing beyond a syntax choice for one generated
file: no dependency, no build step, still plain text an agent reads and
writes directly. (TOON is a comparatively new format; whoever implements
the index-generation logic should verify the current spec rather than
assume this decision pins exact syntax.)

Archiving complements the index rather than duplicating it: the index
helps *retrieval* cost, but `lint`'s own structural checks (dangling
references, missing fields) inherently have to open every file they
validate — no index changes that. Shrinking the *live* set is the only
lever for that cost, and `0039` already handed the model a clean
terminal state (`superseded`/`deprecated`) to trigger it from. It also
directly shrinks the pair count for `docs/decisions/0040`'s contradiction
check, which already excludes non-`active` decisions from comparison —
archiving just means fewer files even have to be opened to know that.

Keeping the move human-confirmed rather than automatic matches every
other `lint`/`capture` finding in this plugin — none of them silently
mutate the tree; all of them propose and wait.

Embeddings/semantic search is a real, more powerful option for a
project that wants it, but it's a genuine infrastructure decision on the
order of the `promptfoo`/CI question already deferred in
`docs/decisions/0040-...` — an external dependency, a build/refresh
step, its own staleness tracking. Structuring the index so that door
stays open, without walking through it now, gets the benefit without
forcing the cost onto every project that adopts `kms`.

## Tradeoffs considered

- **No index, tags/grep only**: costs nothing to build, but doesn't
  reduce `lint`'s per-file cost and, without a controlled tag vocabulary
  (`docs/decisions/0042-...`), degrades right alongside the growth it's
  meant to handle.
- **Embeddings/semantic search now**: better ranking than a flat index,
  but real infrastructure (dependency, build step, staleness tracking)
  at the same weight class as the already-deferred `promptfoo` decision
  — a separate initiative, not a rider here.
- **Markdown table index instead of TOON**: zero new format to explain,
  but undermines the reason the index exists — at hundreds of artifacts,
  table markup overhead is exactly the cost this file is meant to avoid.
- **Automatic archiving on status change**: faster, but breaks the
  propose-then-confirm pattern every other skill in this plugin follows.
- **Manual-only archiving, `lint` just flags it**: safer, but likely to
  accumulate the exact backlog this mechanism exists to prevent, since
  nothing ever proposes the actual move.
- **Chosen: a TOON index maintained by `capture`/verified by `lint`; an
  archive `lint` proposes and a human confirms; embeddings left fully
  optional.**
