# Changelog

## [2.1.0] - 2026-07-29

### Added

- Added `attribute` and `changelog` skills so commit history stays traceable to the intent behind a change, not just what changed — commit/PR messages now lead with why and link to `docs/{facts,decisions,guardrails,skills}/` artifacts via `Refs:` trailers, and a changelog can be rendered from that history on demand.

### Changed

- Rename plugin to kms, add roadmap skill, trim token cost
- Fix AskUserQuestion overflow when interview skill uses tool path
- Redesign interview skill for scannable, comparable options
- Fix plugin manifest format and polish marketplace copy
- initial commit
