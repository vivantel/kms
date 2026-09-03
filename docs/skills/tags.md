<!-- kms-generated: true -->
# Canonical tag vocabulary

Each tag listed below is the single authoritative spelling for that concept. When `docs/skills/tags.md` exists, every artifact's `tags` frontmatter MUST draw from this list — see `docs/guardrails/tags-from-canonical-list.md`.

Tags marked `(umbrella)` are carried by more than half of active decisions and are excluded from `lint` check 16's contradiction-scoping test.

agent-agnostic — the skill or artifact is designed to work across coding agents, not tied to one tool's idioms
agents-md — concerns the AGENTS.md cross-agent convention file
automation — concerns a mechanism that runs without human invocation (hooks, CI, scheduled jobs)
audit — concerns an audit trail or verification record
branding — concerns the project's display name or public identity
changelog — concerns the CHANGELOG.md generation design
claude-code — specific to Claude Code's plugin/hooks mechanisms
claude-md — concerns the CLAUDE.md/AGENTS.md file and its conventions
codex — concerns Codex plugin manifest or packaging
commit-messages — concerns the format or content of commit messages
discoverability — concerns how the project is found (README badges, GitHub topics, marketplace listings)
documentation — concerns docs structure, conventions, or prose quality
git — concerns git workflow, history, or conventions
guardrail — a normative artifact (in guardrails/) or a decision about guardrails
hooks — concerns Claude Code SessionStart/PreToolUse/etc. hooks
ideation — concerns the brainstorm skill or generative, write-nothing workflows
kms (umbrella) — the kms plugin itself; its skills, packaging, or architecture
knowledge-management (umbrella) — the fact/decision/guardrail/skill knowledge system this plugin manages
kilo — concerns Kilo Code CLI's skill format or remote-skills mechanism
marketing — concerns public-facing positioning, description sync, or badges
naming — concerns identifier or display-name conventions
onboarding — concerns the quickstart or onboard skills
packaging — concerns plugin manifests, templates, version sync, or distribution
procedural — a procedure artifact (in skills/) or a decision about procedures
pull-requests — concerns PR description generation or review
roadmap — concerns the roadmap skill or decision-capture workflow
scale — concerns knowledge-base scalability (index, archive, tag vocabulary, scoped checks)
scope — concerns the bounds or applicability of a decision (legacy tag, retained for 0006)
taxonomy — concerns the artifact-type model, lifecycle fields, or track exclusivity
traceability — concerns linking commits/PRs to knowledge artifacts via Refs trailers