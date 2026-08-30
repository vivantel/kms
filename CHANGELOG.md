# Changelog

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
