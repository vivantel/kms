# Changelog

## [0.12.0] - 2026-09-12

### Added

- `operationalizes: [<guardrail-id>, ...]` — an optional field on `Procedure` (the only one of the four governed types that previously had zero type-specific frontmatter), plus `lint` check 23 flagging a guardrail whose text describes a recurring/multi-step action with no procedure operationalizing it and nothing else already enforcing it (a CI check, a hook, a shipped skill's own logic all count). Motivated by asking whether `kms` needs a 5th "runbook"/"playbook" artifact type — it doesn't; a runbook already fits `Procedure`'s existing definition, and check 23 was the actual missing piece: nothing let a guardrail's required behavior be checked against whether a written procedure exists for it.
- `lint` check 24: a `docs/plans/*.md` file whose own per-step legend is all `done` and still sitting in the live `docs/plans/` directory is now flagged as an archive candidate, mirroring the four governed types' existing archive mechanism (`docs/plans/archive/`) — without imposing any governed `status`/`track` lifecycle on plans, which `docs/decisions/0037-...` deliberately excludes them from. Applied to the current backlog: 9 fully-done plans archived (3 backfilled with minimal frontmatter first, since they predated the plan-frontmatter convention).

### Fixed

- `bootstrap`'s eval case was genuinely flaky post-judge-fix, not resolved as an earlier small sample suggested. Root-caused precisely: `bootstrap/SKILL.md` step 10 literally said "verify the current TOON spec before finalizing exact syntax" — an explicit instruction to research externally, not just an unclear term — and separately, `evals/bootstrap/promptfooconfig.yaml`'s `timeout_seconds` was too tight for otherwise-legitimate thorough exploration. Both fixed (inline definition replacing the research instruction; timeout raised 480s → 1440s). A full self-scan then found the TOON naming itself was the deeper issue — none of this project's own `INDEX.md` files use any TOON feature beyond what plain CSV already expresses, so the format is now defined directly as strict, quoted CSV (`docs/decisions/0049-plain-csv-index-not-toon.md`, superseding `docs/decisions/0041-...`), removing the "verify an external spec" temptation at its root rather than just describing it better.
- `lint`'s own eval case scored a passing grade on a run that had actually timed out mid-exploration without writing any real analysis, because its old bare-substring regex assertions were incidentally satisfied by the model `cat`-ing fixture files containing the same strings. Fixed by grading on synthetic sentinel lines instead (strings that exist nowhere in the fixture, so a match can only come from a deliberate final statement).
- A full `lint` pass over this repo's own knowledge base found and fixed three real, pre-existing defects: two guardrails' `grounded-in` fields were malformed (a comma-joined string instead of a YAML list, traceable to ambiguous notation in `plugins/kms/shared/artifact-model.md`'s own field spec — now unambiguous, and `lint` check 2 now verifies list-shaped fields are actually lists); `docs/skills/tags.md` had no base frontmatter at all (written directly during a plan's execution rather than through an actual `bootstrap` run, and `lint` check 2 never asserted universal base-frontmatter presence — now it does); and `docs/decisions/0047-...` sat at `status: draft` for two days after its own described mechanism had already shipped and been cited as settled fact elsewhere (promoted to `active`).

### Changed

- Adopted a free Kilo Code CLI + promptfoo eval harness (`evals/`) comparing shipped skill-body changes, wired into CI (`.github/workflows/eval-skills.yml`) with fork/comment safety gates — closing fitness-function debt logged against `docs/decisions/0040-...`. Runs 5 cases (`bootstrap`, `roadmap`, `capture`, `lint`, `attribute`) through Kilo's own built-in free gateway, no account or API key needed for a local run. Iterated through a long real-CI-driven debugging pass (invalid regex flags, a promptfoo `exec:`-provider path-resolution quirk, an action that deletes its own output file before a later step can read it, ANSI codes breaking JSON extraction, a judge model reaching for tools on large transcripts instead of answering) before reaching a stable baseline: `capture`, `attribute`, `lint`, and `bootstrap` reliably pass; `roadmap` is an accepted, narrow, known flake on the discrete-options interview mechanic specifically — a genuine free-tier model limitation, not a harness defect (`docs/plans/archive/eval-harness-baseline-reliability.md`).
- Optionally enabled promptfoo's hosted sharing (a `PROMPTFOO_API_KEY` CI secret) so the PR summary comment's result links actually resolve, and consolidated what was briefly 5 separate per-case PR comments into one summary comment with `<details>` failure blocks (prompt, failing assertion, grader reason, output excerpt) for anyone without promptfoo.app org access.
- Git tags now mirror `plugin.json`'s own version directly (`docs/decisions/0048-...`) instead of an independently-incrementing sequence (`docs/decisions/archive/0046-...`, superseded) — one number, not two, since this repo ships exactly one plugin today.

## [0.11.0] - 2026-09-11

### Added

- Executed `docs/plans/eval-harness-for-skill-changes.md` end to end: `package.json`, the 5 promptfoo eval cases under `evals/` (each with a fixture and a Kilo-driven exec provider), and the CI workflow. Discovered mid-execution that GitHub Models (the originally-decided judge) had been fully retired, and that Kilo Code CLI's own built-in gateway serves the exact `:free`-suffixed models this harness needs with no account, login, or API key at all — superseding the OpenRouter-based design and removing every CI secret requirement.

### Fixed

- A string of real-CI-only bugs found by actually running the harness rather than reasoning about it: an invalid empty `tests: [{}]` entry promptfoo rejects outright; each case's `exec:` provider path resolving relative to its config file rather than the process's working directory; `promptfoo-action` deleting its own `-o` output file before a later workflow step could read it (fixed by exporting from promptfoo's persistent local store instead); an inline `(?i)` regex flag `lint`'s case used that plain JS `RegExp` doesn't support (masking that the model's own analysis was actually correct); and the grading judge failing to extract JSON from its own response on long rubric prompts because Kilo's decorative banner/ANSI codes broke the parser, then — after that first fix — reaching for an actual tool on large transcripts instead of just answering (fixed with Kilo's tool-free `--agent summary`).

### Changed

- Enabled promptfoo's hosted sharing via a `PROMPTFOO_API_KEY` CI secret, then replaced 5 separate per-case PR comments (one per matrix leg, indistinguishable at a glance, and 5 notifications per run) with a single consolidated summary comment, later extended with a collapsed `<details>` block per *failed* case showing the actual prompt, failing assertion, grader reasoning, and an output excerpt directly in the PR.

### Documentation

- Recorded the real, evolving eval-harness baseline as it was actually measured across many live CI runs (`docs/plans/archive/eval-harness-baseline-reliability.md`), rather than assumed from a single early sample — the initial "3/5 passing" reading turned out to hide two harness bugs, and a later "2/2 clean passes" reading of `bootstrap` after one fix turned out to be too small a sample once more runs came in.
- Captured, then corrected, the release-tagging scheme: first as an independent sequence starting at `0.1.0` (`docs/decisions/archive/0046-...`), then superseded in favor of mirroring `plugin.json`'s own version directly (see `[0.12.0]` above).

## [0.10.0] - 2026-09-04

### Added

- A code-review pass found the prior taxonomy/plan-organization plan structurally broken (its Done-when criteria couldn't be satisfied by its own steps). Reopening it via a `roadmap` interview surfaced that the underlying artifact model itself needed revision: plans are not a 5th governed artifact type (`docs/decisions/0037-...`); `track` is mutually exclusive everywhere it's stored, `both`/`mixed` is never a literal value (`0038`); `status` is unified into one enum across all four governed types, `expires` extends to all four, `scope` is dropped, decisions gain a structured `superseded-by` field (`0039`); `lint` gains cross-artifact-contradiction, stale-debt, and stale-fitness-function checks (`0040`). A follow-up scale-focused interview added a per-type TOON-format `INDEX.md` so `query`/`onboard` don't have to read every file, an archive mechanism for superseded/deprecated artifacts, and a canonical tag vocabulary with tag-scoped contradiction checking (`0041`, `0042`).
- Executed both resulting plans: the lifecycle/taxonomy retrofit (35 decisions' `status` migrated, "skill prescription" renamed to "procedure" across README/skill bodies) and the KB-scale plan (per-type `INDEX.md` files, `docs/skills/tags.md`, `0006` archived). Both executions surfaced and fixed real defects a review pass caught: leaked dogfooding-repo-specific citations in shipped skill-body text, and a decision-immutability violation (three already-accepted decisions had been edited to point at 0006's new archive path — reverted, since decisions are immutable once accepted and a stale reference in one is an accurate record of what was true when it was written, not an error).
- Adopted a free Kilo Code CLI + OpenRouter + promptfoo eval harness design for comparing shipped skill-body changes (`docs/decisions/0043-...`, `0044-...`), closing fitness-function debt logged against `0040`. Not yet built at this point — see `[0.11.0]`.

## [0.9.0] - 2026-08-30

### Added

- Native Kilo Code CLI support: `plugins/kms/skills/index.json`, a remote-skills manifest matching Kilo's `skills.urls` config mechanism, letting a Kilo user track this repo without copying files into their own project. Kilo Code CLI itself needs no manifest — it reads plain `SKILL.md` folders directly in the same open Agent Skills format Claude Code and Codex use. The version-sync guardrail (`docs/guardrails/plugin-manifest-version-sync.md`) extends to cover `index.json`'s per-skill version fields.

### Documentation

- Extracted per-agent install steps into a standalone `INSTALLING.md` — README's Installing section previously mixed three agents' setup instructions as consecutive prose with no way to deep-link or scan for just one agent's steps.
- While tightening README's setup instructions, re-verified the Codex install-command claim in `docs/facts/0003-...` against a second primary source; it didn't corroborate. Retracted the unconfirmed claim with a dated note rather than leave an unverified command in a user-facing doc.

## [0.8.0] - 2026-08-30

### Changed

- `bootstrap` and `capture` no longer each fully restate the fact/decision/guardrail/skill-prescription field model — it moved to `plugins/kms/shared/artifact-model.md`, read via the same sibling-reference mechanism the templates-sync feature already depends on reliably. Reverses part of the reasoning in `docs/decisions/0016-lint-skill.md` (full duplication over cross-referencing), now that a real precedent exists for a shipped skill reading a sibling file at runtime. `clarify`/`roadmap`'s shared interview mechanics were considered for the same treatment and left alone — that content differs in voice (first-person vs. third-person) between the two, not just location, so extracting it would force a real rewrite rather than a pure duplication removal.

## [0.7.0] - 2026-08-30

### Changed

- **`steward` renamed to `capture`, and narrowed.** Every check duplicated between `steward` and `lint` (redundant/unenforced guardrails, expired decisions, audit-log facts, verbosity, statement-split, baseline-artifact sync) now lives only in `lint` — one source of truth per check, instead of two copies that had to be edited identically. `capture` keeps only the genuinely session-driven checks: new decision, fact changed, new automatable rule, contradiction found, human-doc drift, and the session-scoped half of the old role-list check. The hook (`capture-nudge.sh`) and its doc (`docs/skills/automating-capture.md`) are renamed to match. This is a breaking rename for anyone invoking `/kms:steward` directly.

### Added

- `conform` — checks whether a pending changeset (staged diff, a commit range, or a flexible target like "the last 3 PRs") conforms to existing decisions and guardrails before it lands. Read-only; excludes changes to the knowledge base's own artifacts entirely, which stays `lint`/`capture`'s job.
- `docs/skills/kms-architecture.md` — one reference doc synthesizing kms's own layers (`docs/` internal knowledge vs. `plugins/kms/skills/` packaging vs. `plugins/kms/templates/` shippable product content vs. `plugins/kms/hooks/` automation) and marker conventions (`kms-seeded`, `kms-generated`, `<!-- kms:start/end -->`) in one place, linked from `AGENTS.md`.

## [0.6.0] - 2026-08-30

### Added

- `uninstall` — finds everything `bootstrap`/`steward` added to a project (seeded guardrails, generated track-role-lists/doc-manifest, the AGENTS.md knowledge-base pointer, still-draft stubs nobody finalized) and offers to detach or remove each, reported up front rather than one at a time. Run manually before actually uninstalling the plugin — Claude Code has no uninstall lifecycle hook, so nothing here can ever be automatic.
- `bootstrap` now wires a marked `<!-- kms:start -->`/`<!-- kms:end -->` section into the target project's own `AGENTS.md`/`CLAUDE.md`, pointing at its knowledge base — mirroring how `kms`'s own `AGENTS.md` documents itself — and stamps `kms-generated: true` on the three files it dynamically constructs per project (`docs-manifest.md` and both product/process track-role-lists), so `uninstall` can find them.
- The baseline-artifact sync mechanism (`bootstrap`/`steward`/`lint`) generalized from hardcoding `templates/guardrails/` to scanning every subdirectory of `templates/`, ready for a second template type without touching all three again.

## [0.5.0] - 2026-08-30

### Added

- Four of `steward`'s "Global principles" (token economy, one-statement-one-job, no-redundant-guardrails, no-unenforced-guardrail) are now real, checked guardrails instead of unenforced prose — `lint`/`steward` each gained matching checks, self-contained inline (never referencing a `kms`-repo-specific file, so they work correctly when run against an arbitrary adopting project).
- `plugins/kms/templates/guardrails/` — these four guardrails ship as actual product assets, distinct from this repo's own `docs/{facts,decisions,guardrails,skills}/`. `bootstrap` seeds any missing one into a project's own `docs/guardrails/` at setup; `steward`/`lint` keep them synced afterward (add what's missing, update what's stale, remove what's retired upstream, never touch what a team has deliberately detached via a documented escape hatch).
- `docs/skills/scoping-shipped-vs-repo-rules.md` — the general procedure this whole change follows for deciding whether a new rule belongs in a shipped skill, `kms`'s own contributor docs, or both, with a concrete grep to catch the exact bug pattern this session hit twice while designing it.

### Fixed

- `lint`'s "Out of scope" note named "Claude Code" explicitly, violating this repo's own agent-neutrality guardrail — caught by re-running `docs/facts/0002`'s own stated audit grep, not by inspection.
- `docs/facts/0002` claimed an audit of "eight skill instruction bodies"; four more (`quickstart`, `brainstorm`, `onboard`, `refactor-plan`) had been added since and were never covered. Re-ran the audit against all twelve — still clean — and updated the fact.
- `docs/guardrails/every-skill-ships-examples.md` claimed `lint` check 9 enforced it automatically; that check was later repurposed to "stale prose references" with no replacement, silently disabling enforcement. Corrected to state the real mechanism (`AGENTS.md`/`CONTRIBUTING.md` review, per `docs/skills/scoping-shipped-vs-repo-rules.md`), and annotated the one stale plan reference to the old check number rather than silently rewriting it.
- `docs/guardrails/token-economy.md` was missing the `kms-seeded`/`kms-template-version` marker fields its three sibling seeded guardrails carry, making it permanently invisible to the new sync mechanism. Added, plus a clarification that a sync "refresh" only ever touches a seeded file's `## Guardrail` rule text, never a `## Derivation` section a team has since filled in.
- Inconsistent token-economy exemption wording across `bootstrap`/`steward`/`roadmap`/the guardrail itself ("decisions" vs. "decisions and plans" exempt) — aligned.
- `AGENTS.md` claimed "no application code" while this same batch ships `plugins/kms/hooks/steward-nudge.sh`, a real shell script — corrected.
- A dead redundant guard clause in `steward-nudge.sh` (a case already covered by the age-bounds check two lines later) — removed.
- Fact renumbering (`0005` removed as audit-log noise, `0006`→`0005`, `0007`→`0006`, from the previous release) was never recorded anywhere — noted here.

### Known open risk

Whether Codex's plugin install mechanism copies sibling directories like `templates/` (or `hooks/`) at all, versus only the `skills` path its manifest declares, is unconfirmed — flagged in `docs/decisions/0027-baseline-guardrail-seeding.md` rather than assumed away.

## [0.4.0] - 2026-08-30

### Added

- `quickstart` — runs `bootstrap`'s setup, then immediately captures one real, current decision as a full artifact in the same sitting, so a first-time user feels the value before deciding whether to keep using the system.
- A Claude Code `SessionStart` hook (`plugins/kms/hooks/hooks.json`, logic in `plugins/kms/hooks/steward-nudge.sh`) that surfaces a note to the agent when `HEAD`'s commit is under 4 hours old, suggesting it mention running `steward` to the user — auto-activates for anyone who installs the plugin, no manual setup. Documented in the new `docs/skills/automating-steward.md`, including its known imprecision and a manual recipe for non–Claude-Code agents.
- README gained static license/plugin badges and GitHub repo topics/description were synced (previously empty/stale) — cheap discoverability wins with no CI or moving-number maintenance cost.

## [0.3.0] - 2026-08-30

### Added

- `brainstorm` — generates 5-7 distinct approaches to a problem or feature (pros/cons/risks/effort each), then synthesizes 2-3 recommended directions. Writes nothing and never consults the knowledge base, unlike every other skill in this plugin — deliberately unanchored ideation.
- `onboard` — reads the knowledge base to produce a role-tailored, 5-day onboarding plan (daily goals, skills to run, links to specific artifacts). Warns explicitly if critical artifact types (most importantly facts) are missing, rather than producing a plan that looks more complete than the knowledge base actually is.
- `refactor-plan` — produces a phased refactor plan grounded in existing decisions and guardrails: queries the knowledge base, maps dependencies directly (no runtime dependency on `lint` running as a sub-step), lays out steps with verification checkpoints and rollback strategies per phase, and flags any step that would violate a guardrail for explicit confirmation rather than dropping or working around it silently.
- Every skill now ships a colocated `examples.md` with 2-3 worked usage examples, linked from the README's new "Examples" column — retrofitted onto all 8 pre-existing skills, not just the 3 above, so the plugin doesn't ship in a half-documented state. Required for every future skill by the new `docs/guardrails/every-skill-ships-examples.md`, enforced by a new `lint` check.

### Changed

- Display name changed from "KMS Dev Skills" to "Vivantel KMS", expanded on first mention as "Vivantel KMS (Knowledge Management System)" in the README, `CONTRIBUTING.md`, and both plugin manifests' descriptions — "KMS" alone read as an unexplained acronym to a first-time reader. The technical identifier (`name: "kms"`, the `/plugin install kms` slug, the `plugins/kms/` directory) is unchanged.

### Fixed

- `CLAUDE.md` had drifted into a plain stale copy of `AGENTS.md` (still describing "eight skills") instead of the symlink `docs/decisions/0007-claude-md-agents-md-symlink.md` requires — restored as a symlink so there's exactly one copy of the text on disk again.

## [0.2.1] - 2026-08-30

### Fixed

- Every guardrail in this repo stated its derivation only in prose, never as the `governed-by`/`grounded-in`/`derivation-note` frontmatter `guardrail-derivation-fields.md` itself requires — including that guardrail, about itself. All 5 pre-existing facts were missing `kind`/`governed-by` the same way. Caught by running `lint` (this plugin's own new skill) against this repo's own knowledge base, then fixed across all 13 files.
- One dangling reference (a fact pointing at a guardrail that was split and deleted) and one orphaned fact (referenced by nothing) found by the same `lint` pass.
- `steward`'s "No unenforced guardrail" principle had no matching numbered check, unlike its sibling "No redundant guardrails"; added, and mirrored into `lint`'s checklist.
- `bootstrap`'s role-list step never said to give the two files it writes their base frontmatter, and gave no tiebreaker for a role whose track is genuinely ambiguous (compliance, quality, process-documentation roles) — both added.
- A historical plan's "done when" criterion quoted `roadmap`'s classification paragraph verbatim; later work changed that paragraph without updating the quote. Annotated as stale rather than left to confuse a future reader.

## [0.2.0] - 2026-08-30

### Added

- Decisions now carry a required `track` (`product` = what kms is for and who it serves; `process` = how it's built) — the two were being conflated, making a mission-scope commitment indistinguishable from an implementation choice at a glance.
- `clarify`/`roadmap`/`bootstrap`/`steward` generalized to work for any git-based project, not only software ones; `attribute`/`changelog` and the git+Markdown storage substrate stay as they are, since both require commit history to act on at all.
- Decisions may carry optional `scope`/`expires` fields for work that's bounded or provisional (a hypothesis test, a temporary workaround), instead of being treated as permanent once accepted.
- `bootstrap` compiles two AI-agent role lists (`product`/`process` track) from its existing skill-gap scan; `roadmap` consults them while drafting a decision of that track, when they exist.
- Facts that read as ungrounded, unreferenced event logs are now explicitly out of bounds — kms is a knowledge base, not a dashboard or log.
- `lint` — full-repo, on-demand validation (dangling references, missing fields, expired decisions, redundant guardrails, audit-log-style facts), independent of what changed in any one session.
- `query` — answers a question from the knowledge base with citations, instead of leaving that to manual grep.

### Changed

- Removed two guardrails that only restated what `attribute`'s and `clarify`/`roadmap`'s own skill bodies already said in full — kms authoring duplicate copies of its own skills' behavior is exactly the clutter `bootstrap`/`steward` must not leave behind in a target repo either. Two more with the same skill-name-scoping issue but a genuinely system-wide policy underneath were reworded instead of deleted.
- `steward` gained a principle and checks so a guardrail is never left unenforced: a guardrail describing behavior a shipped skill should enforce now gets that skill updated in the same pass, not deferred.
- Added `LICENSE` (MIT), `README`, `CONTRIBUTING`, `CODE_OF_CONDUCT`, and issue/PR templates tailored to this repo's actual issue types, so it's set up for outside contribution and use as a public marketplace, not just internal reference.
- Fixed stale Claude-Code-only framing and duplicate intro paragraphs in the README; stated that the skill content itself is agent-neutral, not tied to the two packaged agents.
- Synced the plugin manifest descriptions and README with the current 8 skills.

## [0.1.0] - 2026-08-29

### Added

- `clarify` — interviews the user relentlessly about a plan, decision, or idea until reaching shared understanding, without writing anything.
- `roadmap` — runs the same interview, then captures the outcome as durable knowledge artifacts (facts, decisions, guardrails, skill prescriptions) under `docs/{facts,decisions,guardrails,skills}/`, plus a self-sufficient standalone implementation plan.
- `bootstrap` — one-time setup of that fact/decision/guardrail/skill system in a project that has none yet, or a gap-fill pass over an incomplete one.
- `steward` — the ongoing session-to-session maintenance pass for that system: new decisions, changed facts, contradictions, human-doc drift, and guardrails that need re-deriving.
- `attribute` — writes commit messages and PR descriptions that lead with intent, not just what changed, using Conventional Commits type prefixes and `Refs:` trailers linking to the knowledge artifacts they implement.
- `changelog` — generates a `CHANGELOG.md` entry from commit history on demand, grouped Keep a Changelog style from Conventional Commit type prefixes and each commit's intent.
