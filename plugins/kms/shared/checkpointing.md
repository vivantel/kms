## Chunked, checkpointed execution

For a skill whose work can grow unbounded with project size (opening every file of a type, or mining a
whole git history). Applies to a skill's own body when it says so; not every skill uses this.

**Two phases.** Phase A: a chunkable per-item pass (paged, checkpointed after every page). Phase B: a
single pass over the whole corpus, run once, only after every Phase A page has completed — not itself
divided into pages up front, though an individual step within it may still need its own paging (e.g.
opening a large shortlist of candidate files) if the consuming skill's own body says so.

**Paging.** Within Phase A, process items (files, or commits for history mining) in a stable order —
alphabetical by filename for files, oldest-first by commit for git history. Accumulate items into a page
until the page reaches an estimated 15,000 tokens, then checkpoint and continue. A page boundary is
always a whole number of complete items — a single item already over budget gets a one-item page of its
own, never split.

**Checkpoint file.** `docs/.kms-checkpoints/<skill>-<run-id>.md`, checked into git (`<run-id>` — a
timestamp, e.g. `20260913-143000`). Holds: which skill, which run, current phase, the full ordered list
of items (filenames, or commit SHAs) this run enumerated at start (the "item manifest" — small: names or
SHAs only, not content) plus which one was last completed, and — for a skill whose output is findings
rather than written files — those findings so far, grouped by check, so a resume never re-derives what a
prior page already found. A skill whose output is files it writes directly only needs the manifest and
offset — the output already lives at its real path.

**Resume protocol.** On invocation, if a checkpoint file exists for this skill, ask the confirming party
(see `docs/guardrails/confirming-party-acceptable-for-checkpoint-gates.md`) whether to resume or discard
it — never resume silently. To resume: re-list the files/commits the current run would process and
compare against the checkpoint's item manifest.

- **File-based paging** (any type under `docs/`): files can be added, edited, or removed at any position,
  so any difference at all between the fresh listing and the manifest forces a fresh start.
- **Commit-history paging**: history already mined is immutable and append-only under normal use — a new
  commit landing at the tip doesn't invalidate what was already mined. Resume from the recorded SHA as
  long as it's still reachable in the log; force a fresh start only if it isn't (history was rewritten —
  a rebase or force-push), not merely because new commits exist.

Otherwise, continue from the recorded offset.

**Cleanup.** Delete the checkpoint file as the run's last action on success. A checkpoint file found on
disk always means an interrupted run — nothing else leaves one behind.
