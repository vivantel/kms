---
id: eval-harness-baseline-reliability
title: Get the eval harness's real baseline from 3/5 to 5/5, or decide why it shouldn't be
status: pending
date: 2026-09-10
tags: [kms, eval-harness]
---

# Get the eval harness's real baseline from 3/5 to 5/5, or decide why it shouldn't be

## Context for a fresh session

This repo (`vivantel/kms`, working dir `/home/ubuntu/projects/vivantel/kms`,
**public** GitHub repository) ships an eval harness under `evals/` that runs
each of 5 cases (`bootstrap`, `roadmap`, `capture`, `lint`, `attribute`)
through Kilo Code CLI's own free gateway (no account, no API key — see
`docs/facts/0012-kilo-gateway-free-tier-access.md`), orchestrated by
`promptfoo`, wired into CI at `.github/workflows/eval-skills.yml`. Full
background: `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`
and `docs/decisions/0044-eval-harness-ci-safety-gates.md` (including both
files' `## Amendment` sections — read those, they record real corrections
made during execution, not just the original intent).

`docs/plans/eval-harness-for-skill-changes.md` (the harness's build-out
plan) is done; this plan continues from its step 7. **This plan has
already been revised once** (this is the second version) after the harness
itself turned out to have two more bugs, found and fixed while working
step 1 below — read the "Already fixed" list before doing anything, so you
don't re-diagnose something that's settled:

**Already fixed** (each its own merged PR — #13, #14 — on top of the
artifact-upload fix from #12):

- **`lint`'s own regex was invalid**, not the model: `(?i)track` uses a
  Python/PCRE-style inline flag JS `RegExp` doesn't support, so that one
  assertion always failed with "Invalid regex pattern" regardless of what
  the model said — confirmed via a downloaded `eval-results-lint`
  artifact showing the other 3 assertions in the same case genuinely
  passing. Fixed in `evals/lint/promptfooconfig.yaml` by dropping the
  flag (`"track"` alone is unambiguous). **`lint` now passes reliably**
  (2/2 real CI runs since the fix).
- **The judge (`evals/providers/kilo-judge.sh`) couldn't always produce
  parseable JSON** on the real (long) rubric prompt — Kilo's own
  decorative banner/ANSI codes around the model's JSON answer broke
  promptfoo's extraction on `roadmap`'s case specifically (a short manual
  test of the judge script never exercised this, since it used a much
  shorter prompt). Fixed by stripping ANSI escapes and extracting just
  the last balanced `{...}` object before returning the judge's response.

**Current real baseline, after those two fixes** (3 real CI runs; workflow
run IDs `34446496455`, `34452564880`, `34453513003` — download any
`eval-recheck-results-<case>` artifact to see a specific run's full
transcript and grading reason):

- **Reliably pass**: `capture`, `attribute`, `lint` (post-fix).
- **`bootstrap`**: flaky — timed out at its `timeout_seconds` ceiling in
  2 of 4 observed real runs (once with `timeout_seconds: 480`, once after
  raising it), passed the other 2. One timed-out run's transcript showed
  the model going down a research tangent on what "TOON format" (a term
  in `plugins/kms/shared/artifact-model.md`) means, fetching external web
  pages about it instead of proceeding — a real capability/task-scope
  finding, not a fluke of that one run, but not consistent enough to call
  "always fails" either.
- **`roadmap`**: **reliably fails, for a genuine reason** — the model
  bundles two questions into a single turn ("Question 1 of ~7: what's the
  refill rate... also, capacity/burst?"), which directly violates
  `plugins/kms/skills/roadmap/SKILL.md`'s own interview mechanics ("Ask
  questions one at a time... Asking multiple questions at once is
  bewildering"). The judge's reasoning (in the artifact) confirms this
  precisely: it also credits the model for recommending an option and not
  writing files prematurely — it fails on the bundling alone. This
  reclassifies `roadmap` from "passed for real" (the first version of
  this plan's understanding, before the judge-extraction bug was found)
  to "fails for a real, substantive reason."

## Status legend

`done` / `pending` / `blocked`.

## Steps

### 1. Read `lint`'s actual failure from the artifact — status: done

Finding: `lint`'s own regex config was broken (see "Already fixed"
above), not a model failure. Fixed in PR #13.

### 2. Fix `lint` per what step 1 found — status: done

Dropped the invalid `(?i)` flag. Confirmed passing in 2 subsequent real
CI runs (`34452564880`, `34453513003`).

**Update, 2026-09-11**: that "passing" turned out weaker evidence than it looked. Inspecting a
*different* run (workflow `34492665844`) found the model timing out mid-exploration — never
writing a single line of actual analysis — yet still scoring 3 of 4 assertions, because the
bare-substring regexes (`0099-nonexistent-decision`, `0001-weekly-releases`, `require-two-approvals`)
were satisfied by the model incidentally `cat`-ing fixture files containing those strings while
exploring, not by it reaching any conclusion. Only the 4th assertion (`track`, which never
appears literally in any fixture file) actually required real analysis — which is exactly why it
was the one that failed. Fixed: the case's invocation prompt now asks for three synthetic
sentinel lines (`LINT_CHECK_DANGLING_REF: YES|NO`, etc. — strings that don't exist anywhere in
the fixture, so a match can only come from a deliberate final statement) instead of grading on
bare substrings; `timeout_seconds` also raised 480→600. Verified locally: a real run now
completes a genuine, thorough analysis (correctly identifying all 3 planted violations plus two
bonus findings) and ends with the exact expected sentinel lines.

### 3. Decide `bootstrap`'s fix — status: partial

**Update, 2026-09-11**: one real cause of `bootstrap` failures turned out
to be a harness bug, not the runner model at all — a *separate* problem
from the timeout this step originally tracked. `bootstrap`'s transcript
is large enough that its `llm-rubric` grading prompt (which embeds the
whole transcript) sometimes made the *judge* model reach for a real tool
instead of just answering, burning the judge's own timeout and producing
no gradable response at all ("Could not extract JSON from llm-rubric
response" — because there was no response). Fixed: `evals/providers/kilo-judge.sh`
now runs the judge with `--agent summary` (Kilo's built-in tool-free
agent), confirmed by a real CI run (workflow `34632007293`) where
`bootstrap` passed. This does not fix the *other*, still-open cause below
(the runner itself timing out on a research tangent) — that's a
different failure mode, on the runner side, not the judge side. Treat
this step as still open until 3a–3d below are actually tried.

Options, roughly cheapest-to-most-invasive (unchanged from this plan's
first version, since none have been tried yet):

**3a. Raise `timeout_seconds` further** (currently 480 in
`evals/bootstrap/promptfooconfig.yaml`; the workflow's own
`timeout-minutes: 20` per job leaves headroom to go to ~1000s before
hitting that ceiling too). Cheapest test, and the flakiness observed so
far (pass/fail roughly split) suggests this alone might be enough to tip
most runs into passing — try this first.

**3b. Make `shared/artifact-model.md`'s "TOON format" mention
self-explanatory inline**, since the one timed-out run whose transcript
was inspected specifically got stuck on that term. This would be a real,
if small, product finding about `kms`'s own skill-body clarity — not
just an eval-harness tuning knob. If pursued, treat it as its own small
change to `plugins/kms/shared/artifact-model.md` with a reason recorded
(a one-line inline clarification, e.g. spelling out that TOON is a
compact CSV-like tabular notation, not a name requiring lookup), separate
from this eval-harness plan, and note here which commit made it.

**3c. Try a different free model** for the runner (`poolside/laguna-s-2.1:free`
currently). `evals/providers/kilo-runner.sh`'s `model` config field
already supports overriding per-case without code changes — check
`kilo/nvidia/nemotron-3-ultra-550b-a55b:free` (the harness's own judge
model, already confirmed free/no-account/reliable) or another `:free`
model from Kilo's gateway catalog (`kilo models` lists them;
cross-reference against `docs/facts/0012-kilo-gateway-free-tier-access.md`'s
caveat that this catalog is a curated subset, not a 1:1 OpenRouter mirror)
for one with stronger multi-step planning.

**3d. Accept the flakiness as `bootstrap`'s honest result** and record
that a free, small coding-agent model is borderline-but-not-reliable on
this specific task — matching `docs/decisions/0043-...`'s own stated
tradeoff going in. Legitimate if 3a–3c are tried first and don't move the
needle enough.

**Update, 2026-09-11 (second)**: gathered 2 more real runs specifically to check whether the
judge fix alone had resolved this (it had looked like 2/2 clean passes right after that fix
landed). It hadn't — the fuller run history (8 real runs total; see this plan's git history for
the exact table) puts `bootstrap` back at a genuinely flaky ~50% post-judge-fix, not fixed. Both
new failures reproduced the *exact* same transcript pattern as the very first one found: `exit
124`, transcript ending mid-`WebFetch` to `toonformat.dev`/the TOON spec's GitHub repo. Root
cause pinned down precisely: `plugins/kms/skills/bootstrap/SKILL.md` step 10 literally said
*"Verify the current TOON spec before finalizing exact syntax"* — an explicit instruction to
research externally, not just an unclear term as originally guessed. **3b implemented**: that
instruction removed and replaced with a two-line inline definition (a header line + comma-separated
rows, matching any `INDEX.md` already in the project) — no external lookup implied at all.
Also softened the two other, lower-risk "TOON format" mentions in `shared/artifact-model.md` and
`roadmap/SKILL.md` the same way. Verified locally before shipping: a fresh run produced zero
TOON/WebFetch/WebSearch activity and completed the *entire* bootstrap task for real (all 4
artifact types, both INDEX.mds, `docs-manifest.md`, `tags.md`, both role lists) — the only reason
it still shows `exit 124` is that it went on to proactively run its own `lint` self-check
afterward and ran past the ceiling doing that extra, unrequested step, not the original task.

**Update, 2026-09-12**: 3b confirmed as a genuine, permanent fix, not a fluke — 3 real post-merge
CI runs (`34655665753`, and two more from throwaway PRs #37/#38) all show **zero** TOON/WebFetch/
WebSearch activity. 2 of those 3 passed outright. The 1 failure (`34657052079`) is a *different*,
more generic problem: an unusually long, thorough exploration pass (43K chars of transcript vs.
~11K for the passing runs) that used up the full 480s budget before ever writing a file — nothing
to do with TOON, no wrong instruction to point at, just "explored more than the clock allowed."
That's exactly 3a's territory. **3a implemented**: `timeout_seconds` raised 480→1440 (24min,
under the workflow's already-30min job ceiling — no separate workflow change needed, that
ceiling was already raised alongside `lint`'s fix). Not yet re-verified with a live run.

Done when: one of 3a/3b/3c is tried and either fixes `bootstrap` (a few
consecutive real CI runs passing), or all three are tried without success
and 3d is explicitly chosen and recorded here with why. 3b is confirmed and closed (the TOON
tangent itself is gone for good); 3a is implemented but not yet verified — still needs a few
real CI runs post-merge before this step as a whole can close.

### 4. Decide `roadmap`'s fix — status: pending

New step, added after the judge-extraction fix revealed this is a real,
reliable failure (see "Current real baseline" above), not the flaky
harness error this plan originally thought it needed to investigate.

**Update, 2026-09-11**: the *specific* violation isn't stable across
runs, which matters for how to read this step. The run this step was
originally written from failed on question-bundling (two questions in
one turn). A later run (workflow `34632007293`, same unmodified prompt
and skill) asked exactly one question — no bundling — but failed
instead on not stating a recommended option among three it listed. Two
different instructions in the same rubric, both violated, just not on
the same run. Read this as: this free model reliably violates *something*
in the rubric, not that it reliably violates the *same* thing — which
weakens 4b below somewhat (there's no one fix in the wording that would
address both observed failures) and strengthens 4a.

Options:

**4a. Accept it as this free model's genuine limitation** on multi-step
conversational discipline — matching `docs/decisions/0043-...`'s stated
tradeoff about free-tier fidelity on judgment-heavy cases most directly
of anything found so far. `roadmap`'s own `SKILL.md` instruction is
already explicit and unambiguous ("Ask questions one at a time... Asking
multiple questions at once is bewildering") — there's no obvious
wording gap to fix here the way `bootstrap`'s "TOON" tangent suggested
one. This is the most likely right answer; try 4b only if there's a
concrete reason to think the instruction itself is the problem.

**4b. Reinforce the one-question-at-a-time instruction** in
`plugins/kms/skills/roadmap/SKILL.md` if a fresh read of it suggests real
ambiguity (e.g. whether "Q1 of ~7" framing itself invites bundling related
sub-questions under one numbered item) — but weigh this against
`docs/guardrails/token-economy.md` and the general principle that a
shipped skill's body shouldn't be rewritten to chase one weak model's
behavior; a stronger model (or a human) already reads the existing
instruction correctly. Get a second read of the instruction's actual
wording before concluding it needs a change.

**4c. Try a different free runner model**, same mechanism as `bootstrap`'s
3c — if `roadmap`'s failure turns out to be this specific model's weakness
rather than an instruction-clarity problem, a stronger free model might
just follow the existing instruction correctly.

Done when: 4a is explicitly chosen and recorded, or 4b/4c is tried and a
fresh CI run shows `roadmap` passing.

### 5. Record the final baseline state — status: pending

Once steps 3–4 settle (whether that means 5/5 passing, or fewer with an
explicit reason recorded), update
`docs/plans/eval-harness-for-skill-changes.md`'s step 7 status to reflect
the final outcome — that file's own step 7 is currently marked `partial`;
it should end up `done` (if 5/5) or otherwise say plainly what the
accepted baseline is and why, so a future skill-body change being
compared against it has an honest reference point.

Done when: `docs/plans/eval-harness-for-skill-changes.md`'s step 7 no
longer says `partial`.

## Explicitly out of scope

- **Re-litigating the harness's architecture** (Kilo's free gateway,
  `promptfoo`, the 5-case scope) — settled by
  `docs/decisions/0043-...`/`0044-...` and their amendments; this plan is
  about getting the existing design's baseline to a settled state, not
  redesigning it.
- **Extending the suite beyond the initial 5 cases** — explicitly out of
  scope for the parent plan too; still not this plan's job.
- **Touching `capture` or `attribute`** unless a step above finds a
  genuine shared root cause — they already pass reliably; don't
  destabilize them chasing `bootstrap`/`roadmap`.
