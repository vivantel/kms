---
id: tags
title: Canonical tag vocabulary
status: active
date: 2026-09-01
tags: [kms, knowledge-management, scale]
kms-generated: true
---

# Canonical tag vocabulary

Each tag listed below is the single authoritative spelling for that concept. When `docs/skills/tags.md` exists, every artifact's `tags` frontmatter MUST draw from this list — see `docs/guardrails/tags-from-canonical-list.md`.

Tags marked `(umbrella)` are carried by more than half of active decisions and are excluded from `lint` check 16's contradiction-scoping test.

agent-agnostic — the skill or artifact is designed to work across coding agents, not tied to one tool's idioms
agents-md — concerns the AGENTS.md cross-agent convention file
automation — concerns a mechanism that runs without human invocation (hooks, CI, scheduled jobs)
audit — concerns an audit trail or verification record
bootstrap — concerns the improvement harness's isolated worktree/setup phase for a run
branding — concerns the project's display name or public identity
changelog — concerns the CHANGELOG.md generation design
claude-code — specific to Claude Code's plugin/hooks mechanisms
claude-md — concerns the CLAUDE.md/AGENTS.md file and its conventions
codex — concerns Codex plugin manifest or packaging
commit-messages — concerns the format or content of commit messages
configuration — concerns where and how a mechanism's settings are declared
constraint — concerns a hard operating limit a mechanism must respect
data-flow — concerns how data or state moves through a mechanism's pipeline
discoverability — concerns how the project is found (README badges, GitHub topics, marketplace listings)
discovery — concerns how a mechanism finds or enumerates work items
documentation — concerns docs structure, conventions, or prose quality
dogfooding — concerns a mechanism being used on its own producing project
eval — concerns a specific eval-gate verification step, distinct from eval-harness below
eval-harness — concerns the promptfoo/Kilo/OpenRouter mechanism for comparing shipped skill-body changes
free-tier — concerns a free-tier model/API constraint
git — concerns git workflow, history, or conventions
github-models — concerns GitHub Models' free-tier API or GITHUB_TOKEN-based access
guardrail — a normative artifact (in guardrails/) or a decision about guardrails
hooks — concerns Claude Code SessionStart/PreToolUse/etc. hooks
ideation — concerns the brainstorm skill or generative, write-nothing workflows
improvement-harness — the automated KMS improvement harness; its skills, agents, or verification gates
infrastructure — concerns a mechanism's implementation substrate rather than its user-facing interface
kms (umbrella) — the kms plugin itself; its skills, packaging, or architecture
knowledge-management (umbrella) — the fact/decision/guardrail/skill knowledge system this plugin manages
kilo — concerns Kilo Code CLI's skill format or remote-skills mechanism
lint-fix — concerns the improvement harness's mechanical lint-violation-fixing improvement type
location — concerns where a mechanism's code or config physically lives
marketing — concerns public-facing positioning, description sync, or badges
mvp — concerns a minimum-viable-product scoping decision
naming — concerns identifier or display-name conventions
observability — concerns logging, dashboards, or audit visibility into a running mechanism
onboarding — concerns the quickstart or onboard skills
opencode — concerns the OpenCode CLI/agent execution environment
openrouter — concerns OpenRouter's model-routing API or free-tier terms
packaging — concerns plugin manifests, templates, version sync, or distribution
procedural — a procedure artifact (in skills/) or a decision about procedures
process — marks improvement-harness automation/governance decisions on the process track
pull-requests — concerns PR description generation or review
release — concerns version numbering, git tags, or the release/changelog process
roadmap — concerns the roadmap skill or decision-capture workflow
safety — concerns loop prevention, kill switches, or other harm-limiting mechanisms
scale — concerns knowledge-base scalability (index, archive, tag vocabulary, scoped checks)
scope — concerns the bounds or applicability of a decision (legacy tag, retained for 0006)
skill — concerns a mechanism's identity as a KMS skill (interface), as distinct from its implementation
skill-rewrite — concerns the improvement harness's skill-body-rewriting improvement type
subagents — concerns implementation as OpenCode subagents
taxonomy — concerns the artifact-type model, lifecycle fields, or track exclusivity
testing — concerns test or eval execution as a verification step
token-economy — concerns the token-economy guardrail's application to a specific artifact set
traceability — concerns linking commits/PRs to knowledge artifacts via Refs trailers
verification — concerns a gate or check a change must pass before it lands
