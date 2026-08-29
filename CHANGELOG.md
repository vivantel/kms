# Changelog

## [0.1.0] - 2026-08-29

### Added

- `clarify` — interviews the user relentlessly about a plan, decision, or idea until reaching shared understanding, without writing anything.
- `roadmap` — runs the same interview, then captures the outcome as durable knowledge artifacts (facts, decisions, guardrails, skill prescriptions) under `docs/{facts,decisions,guardrails,skills}/`, plus a self-sufficient standalone implementation plan.
- `bootstrap` — one-time setup of that fact/decision/guardrail/skill system in a project that has none yet, or a gap-fill pass over an incomplete one.
- `steward` — the ongoing session-to-session maintenance pass for that system: new decisions, changed facts, contradictions, human-doc drift, and guardrails that need re-deriving.
- `attribute` — writes commit messages and PR descriptions that lead with intent, not just what changed, using Conventional Commits type prefixes and `Refs:` trailers linking to the knowledge artifacts they implement.
- `changelog` — generates a `CHANGELOG.md` entry from commit history on demand, grouped Keep a Changelog style from Conventional Commit type prefixes and each commit's intent.
