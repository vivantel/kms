---
id: knowledge-base-scale
title: Add a per-type TOON index, an archive mechanism, a canonical tag vocabulary, tag-scoped contradiction checking, and full supersession-chain citation
status: done (all 9 steps complete)
date: 2026-09-01
tags: [kms, taxonomy, scale, knowledge-management, refactor]
---

# Add a per-type TOON index, an archive mechanism, a canonical tag vocabulary, tag-scoped contradiction checking, and full supersession-chain citation

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`)
is a Claude Code / Codex plugin marketplace, one plugin (`kms`) at
`plugins/kms/`. See `AGENTS.md` at the repo root for full structure and
conventions before making any change not covered by this plan.

This plan implements two new decisions produced by a `roadmap` interview
about knowledge-base scalability — how the model holds up for a project
with a rich history (hundreds of facts/decisions/guardrails/procedures),
where full-repo reads and pairwise scans stop being viable:

- `docs/decisions/0041-index-and-archive-for-scale.md` — a per-type
  `INDEX.md` in TOON format (cheap to read on every `query`/`onboard`
  invocation) and an archive mechanism for `status: superseded`/
  `deprecated` artifacts (`lint`-proposed, human-confirmed, filename/id
  unchanged).
- `docs/decisions/0042-tag-vocabulary-and-scoped-contradiction-check.md` —
  a canonical, `lint`-enforced tag vocabulary (`docs/skills/tags.md`)
  with explicit write-time new-tag detection, and narrows
  `docs/decisions/0040-...`'s check 16 to tag-scoped pairs, excluding
  near-universal ("umbrella") tags from the scoping test.

Supporting guardrail already written:
`docs/guardrails/tags-from-canonical-list.md`.

**A `code-review` pass, run after this plan's first draft, found five
defects**, now folded into the steps below: `roadmap` had no
index-maintenance instruction (asymmetric with `capture`'s new check
7); the tags-generation step didn't mark umbrella tags, so the
tag-scoped contradiction check would have been a no-op on this repo's
own decisions (all 42 share the `kms` tag); the archive-exclusion
clause was ambiguous about whether `lint`'s dangling-reference check
still resolves ids inside the archive; and the archive step's own
Done-when missed several files with literal (not just id-based)
path references to the artifact being archived. There is no separate
errata list — this version already has the fixes.

**Hard dependency: execute `docs/plans/taxonomy-and-plan-organization.md`
in full before this plan.** Every file reference and line quote below
assumes that plan has already landed — specifically: `lint` checks 1–18
exist with the wording that plan produces (including check 16's
forward-reference note pointing at this plan), every skill body says
"procedure" not "skill prescription," `docs/decisions/0006`'s `status`/
`superseded-by` retrofit is done, and `capture`'s check 1 already
updates a superseded decision's `superseded-by` field. If that plan's
own `status` still reads `pending`, run it first; this plan's
step-by-step text will not line up with the actual files otherwise.

A cold session can execute every step below by reading only this file,
the two decisions and one guardrail named above, and (per the
dependency note) the completed `taxonomy-and-plan-organization.md` —
no other prior context required.

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Add the tags clause to `plugins/kms/shared/artifact-model.md` — status: done

Already applied — `docs/plans/taxonomy-and-plan-organization.md` step 2
rewrites this entire file and already includes the tags/`docs/skills/tags.md`
paragraph this step would otherwise have added. No separate edit needed
here; this step exists only so a cold session doesn't wonder where it
went. Verify by confirming the paragraph beginning "For `tags`: if
`docs/skills/tags.md` exists..." is present in
`plugins/kms/shared/artifact-model.md` before proceeding — if it isn't,
the predecessor plan hasn't actually finished and you should stop and
run it first.

### 2. Update `plugins/kms/skills/roadmap/SKILL.md` — status: done

**2a.** In "## Classify at the end, not during", the paragraph produced
by the predecessor plan already ends with "...propose additions there
when none fit." — no further edit needed for tags here (see step 1
above for why).

**2b.** In "## The changeset implementation plan" (or immediately after
it), add one sentence giving `roadmap` the same index-maintenance
responsibility `capture` gets in step 4 below — without it, every
artifact `roadmap` writes directly (which is most of what it produces)
would fail `lint` check 19 the moment it's added:
```
After writing any fact, decision, guardrail, or procedure directly to disk, also add or update its row in that type's `INDEX.md` (`id, title, tags, status`, TOON format).
```

Done when: 2b's sentence is present verbatim; confirm 2a needs nothing
further per step 1's note.

### 3. Update `plugins/kms/skills/bootstrap/SKILL.md` — status: done

**3a.** In step 7 ("Compile the track role lists"), after the existing
paragraph, add: "Using the same repo-scan signals, also compile
`docs/skills/tags.md`: every tag already in use across this project's
artifacts (or, in a fresh project, domain vocabulary drawn from existing
docs), one tag per line with a one-line meaning. Mark any tag carried by
more than half of active decisions as `(umbrella)` — computed from the
scan, not asserted — since `lint` check 16 excludes umbrella tags from
its contradiction-scoping test. Same frontmatter and `kms-generated:
true` marking as the role lists above."

**3b.** Add a new step 10, "Seed the per-type index," after step 9
("Wire into the project's own agent-instructions file"): "For each of
`docs/{facts,decisions,guardrails,skills}/`, write `INDEX.md` in TOON
format: one row per artifact in that directory (excluding `INDEX.md`
itself and anything already under a `archive/` subdirectory) with
fields `id, title, tags, status`, extracted directly from each file's
frontmatter. Mark it `kms-generated: true` in a leading comment line,
since `uninstall` needs to recognize it as this skill's output. Verify
the current TOON spec before finalizing exact syntax — this step only
fixes the field set and source (frontmatter), not the literal encoding."

Done when: 3a and 3b are applied verbatim.

### 4. Update `plugins/kms/skills/capture/SKILL.md` — status: done

Add a new check to "## Checks, one pass per invocation," covering
index-row maintenance for anything this pass drafted or edited.

**Correction (post-execution review)**: this step originally said to
add the new check "after check 7," assuming the predecessor plan's
supersession-pointer addition had landed as its own numbered check.
It hadn't — that addition was folded into the text of check 1 instead
— so `capture` only had 6 checks at the time this step ran, and the
new index-entry check correctly landed as check 7, not check 8. A
later review pass also tightened its wording to point at the artifact
model's own index-maintenance rule (`../../shared/artifact-model.md`)
rather than repeating the TOON format details inline. Both are
reflected in the file as it actually stands.

Done when: `plugins/kms/skills/capture/SKILL.md` has a check covering
index-row maintenance, and no existing check's number changed.

### 5. Update `plugins/kms/skills/lint/SKILL.md` — status: done

**5a.** Replace check 16 (as it reads after the predecessor plan) —
currently:
```
16. **Cross-artifact contradiction** — two `status: active` decisions, or a decision and a guardrail derived from it, making contradictory claims on overlapping subject matter, anywhere in the project's history — not just what one session just produced.
```
with the tag-scoped, umbrella-excluded version:
```
16. **Cross-artifact contradiction** — two `status: active` decisions, or a decision and a guardrail derived from it, sharing at least one non-`(umbrella)` tag from `docs/skills/tags.md`, making contradictory claims on overlapping subject matter — anywhere in the project's history, not just what one session just produced. Bounded by non-umbrella tag-cluster size, not the full corpus; a tag marked `(umbrella)` (carried by more than half of active decisions) never counts toward this test, since otherwise a project-wide tag would put nearly everything in one cluster and defeat the scoping.
```

**5b.** Immediately after check 18 (the last check added by the
predecessor plan), insert four more:
```
19. **Index out of sync** — any type's `INDEX.md` missing a row for a file that exists in its directory, containing a row for a file that doesn't, or a row whose `id`/`title`/`tags`/`status` no longer matches that file's frontmatter.
20. **Archive candidate** — a `status: superseded` or `status: deprecated` artifact still in its live directory (not yet under `docs/<type>/archive/`) — propose the move, filename and `id` unchanged, and propose updating any literal (non-id) path references to it elsewhere in the repo to the new path.
21. **Tag off the list** — a tag in use on any of the four types that isn't in `docs/skills/tags.md`, when that file exists (`docs/guardrails/tags-from-canonical-list.md`).
22. **Tag gone cold** — a tag on `docs/skills/tags.md` unused by any artifact in a long time, judged the same relative way check 14 judges a role gone cold.
```

**5c.** In "## What to check"'s opening line (or wherever the default
scan scope is described), add a clause: "The default invocation's
*health* checks (verbosity, staleness, contradiction-scanning) scan
only the live set — artifacts under `docs/<type>/archive/` are excluded
unless explicitly asked for a deep pass covering them too. This
exclusion does NOT apply to check 1 (dangling references): resolving
whether a `governed-by`/`grounded-in`/`superseded-by` id exists always
searches both the live directory and its `archive/` subdirectory,
otherwise every reference into an archived artifact would start
reading as a false-positive dangling reference the moment that artifact
is archived."

Done when: 5a's replacement is applied verbatim; checks 19–22 are
present immediately after 18 with no gaps; 5c's clause is present, with
the check-1 carve-out stated explicitly.

### 6. Update `plugins/kms/skills/query/SKILL.md` — status: done

**6a.** Replace:
```
1. Search by keyword, topic, and frontmatter `tags` across all four artifact directories for candidates.
```
with:
```
1. Read each type's `INDEX.md` first, if present, to narrow candidates by tag/title before opening full files; fall back to searching all four directories directly by keyword/topic/`tags` when no index exists.
```

**6b.** Replace:
```
3. If a decision has been superseded, cite the superseding one too, not just the original.
```
with:
```
3. If a decision has been superseded, follow `superseded-by` transitively until reaching a decision whose own `status` isn't `superseded` — cite that final active decision alongside the original, not just the immediate next hop.
```

Done when: both edits are applied verbatim.

### 7. Update `plugins/kms/skills/onboard/SKILL.md` — status: done

Replace:
```
2. Read all four artifact directories. If `docs/skills/{product,process}-track-roles.md` exists and lists the given role, weigh its stated scope; otherwise use judgment about what the role would need.
```
with:
```
2. Read each type's `INDEX.md` first, if present, to identify what's actually relevant to the role, then open only those files — read all four artifact directories directly only when no index exists. If `docs/skills/{product,process}-track-roles.md` exists and lists the given role, weigh its stated scope; otherwise use judgment about what the role would need.
```

Done when: the edit is applied verbatim.

### 8. Retrofit this repo's own knowledge base — status: done

This repo dogfoods `kms` on itself, so it needs the same artifacts an
adopting project's `bootstrap`/gap-fill pass would produce.

**8a.** Generate `docs/skills/tags.md`: scan the `tags` frontmatter
across every file in `docs/{facts,decisions,guardrails,skills}/`,
dedupe, write one line per distinct tag with a one-line meaning inferred
from how it's actually used. Mark `kms-generated: true`. Per bootstrap
step 7's updated instruction (step 3a above), mark any tag carried by
more than half of active decisions as `(umbrella)` — verify against the
actual tag distribution at execution time, not against any count quoted
elsewhere, since the corpus will have grown between this plan being
written and run.

**8b.** Generate the four `INDEX.md` files (`docs/{facts,decisions,
guardrails,skills}/INDEX.md`) per bootstrap step 10's algorithm (3b
above): one TOON row per file in that directory, fields `id, title,
tags, status`. Verify the current TOON spec before finalizing exact
syntax.

**8c.** Apply check 20's archive proposal to the one artifact currently
eligible: `docs/decisions/0006-agent-agnostic-scope.md` (`status:
superseded` per the predecessor plan's retrofit). Move it to
`docs/decisions/archive/0006-agent-agnostic-scope.md`, filename
unchanged. Then update every literal (non-id) path reference to the old
location — verified at plan-writing time to be exactly these five
files (three decisions, one guardrail, one fact), but re-grep at
execution time in case something changed —
**except decisions**: `docs/decisions/0007-claude-md-agents-md-symlink.md`,
`docs/decisions/0008-native-codex-plugin-support.md`, and (found by a
later review pass, since this list was written before it existed)
`docs/decisions/0039-unify-lifecycle-and-drop-scope.md` are all
already-accepted decisions, and decisions are immutable once accepted
(`plugins/kms/shared/artifact-model.md`'s own table) — leave their
stale `docs/decisions/0006-agent-agnostic-scope.md` references
untouched, exactly as `docs/decisions/0031-consolidate-kb-checks-rename-capture.md`
already established for this repo's historical references generally
("annotate, don't rewrite"). `lint` check 9 already tolerates this
("a reference a plan already annotates as deliberately-preserved
history") — this sentence is that annotation. Only update the two
non-decision files: `docs/guardrails/agent-agnostic-skill-content.md`
(two occurrences) and `docs/facts/0002-skill-bodies-already-agent-neutral.md`
(one occurrence) — facts and guardrails are refined in place, so
updating their path references is normal maintenance, not a violation.
Do not edit the `governed-by: 0006-agent-agnostic-scope` id fields in
the guardrail or fact either — those are id references, not paths, and
resolve correctly under 5c's carve-out regardless of which directory
`0006` lives in. Update `docs/decisions/INDEX.md` accordingly (it moves
out of the live index) and add a `docs/decisions/archive/INDEX.md` with
`0006`'s row, same TOON format, so archived artifacts stay discoverable
through their own index rather than disappearing from all of them.

Done when: `docs/skills/tags.md` and all four `INDEX.md` files exist and
validate against checks 19/21/22; `0006` is under
`docs/decisions/archive/`; running
`grep -rl "docs/decisions/0006-agent-agnostic-scope.md" --include="*.md" . | grep -v "docs/plans/"`
(excluding `docs/plans/` — both this plan's own text and pre-existing
historical plans legitimately still narrate the old path, same as the
`skill prescription` rename check in the predecessor plan) returns
exactly three results — `docs/decisions/0007-claude-md-agents-md-symlink.md`,
`docs/decisions/0008-native-codex-plugin-support.md`, and
`docs/decisions/0039-unify-lifecycle-and-drop-scope.md`, all three
deliberately unchanged per the decision-immutability exception above —
and no others; every `governed-by`/`superseded-by` pointer naming `0006`
still resolves.

### 9. Verify — status: done

Run `lint` against this repo's own knowledge base (checks 1 through 22).
Confirm zero new violations beyond pre-existing, already-known debt.
Confirm `query` and `onboard`, when invoked, actually read the relevant
`INDEX.md` before opening full files, and that a query about a
superseded decision resolves to the fully-active end of its
`superseded-by` chain, not just the first hop.

Done when: the above holds.

## Explicitly out of scope for this plan

- **Building an embeddings/semantic-search layer** — `docs/decisions/0041-...`
  deliberately leaves this fully optional and out of `kms` itself; the
  index format is structured so a project can add one later without
  revisiting that decision.
- **Adopting `promptfoo`/CI** — already logged as `fitness-functions`
  debt on `docs/decisions/0040-...`, its own separate initiative.
- Committing or pushing — not requested; check `git status`/`git log`
  before assuming otherwise.
