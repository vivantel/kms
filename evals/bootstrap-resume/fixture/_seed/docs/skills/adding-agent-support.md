---
id: adding-agent-support
title: Procedure for adding a new coding-agent target to this repo
status: active
date: 2026-07-29
tags: [kms, agent-agnostic, packaging, procedural]
---

## Procedure

This describes how to decide whether and how to add native packaging
support for a new coding agent (the way `docs/decisions/0008-native-codex-plugin-support.md`
added Codex) to this repo, without redoing that whole interview from
scratch each time.

### 1. Confirm the agent's actual manifest format from primary sources

Don't trust search-engine-summarized SEO content for this — it produces
specific-sounding but uncorroborated claims (per
`docs/facts/0003-codex-plugin-manifest-schema.md`'s own note on this).
Fetch the agent vendor's own developer documentation directly. Record
what you find as a fact in `docs/facts/`, including anything you could
*not* confirm with confidence — don't silently drop the uncertain parts.

### 2. Check for the two failure modes that force a restructure

Before assuming "just add a manifest" is enough, check whether the new
agent's manifest format has either of these constraints — both are
known failure modes that can force a real restructuring decision:

- **Single-path-only skill selection** (no array, no include-list): only
  a problem if this repo's `plugins/<name>/skills/` directory contains
  skills that shouldn't ship to that agent. As of 2026-07-29 it doesn't
  (all skills under `plugins/kms/skills/` are public), so this constraint
  is currently harmless — but re-check if a private/draft skill bucket is
  ever introduced.
- **Symlinks dropped on install**: rules out any packaging approach that
  relies on symlinking a curated subset into an agent-specific directory.
  If the new agent has this behavior and constraint 1 also applies
  (private skills exist and need excluding), that combination forces an
  actual restructuring decision — treat it as its own scoped
  decision/interview, don't bolt it onto the "add agent X" plan.

### 3. Default to no restructuring

Point the new agent's manifest directly at the existing
`plugins/<name>/skills/` directory if its format allows a path pointer
(most do). Only propose restructuring the repo layout if step 2 found a
real blocker — restructuring is a much larger blast radius than adding
one manifest file, and should get its own decision record and go-ahead
checkpoint, not be folded into an "add agent X" plan.

### 4. Keep skill content agent-neutral

Adding a manifest for a new agent doesn't require touching any
`SKILL.md` body — per `docs/guardrails/agent-agnostic-skill-content.md`,
they're already written to be agent-neutral. If the new agent's docs
reveal a content requirement that conflicts with that guardrail, resolve
the conflict as its own decision rather than quietly violating the
guardrail.

### 5. Add per-skill `agents/<agent-name>.yaml` sidecars only for real differences

Follow the pattern established for Codex
(`plugins/kms/skills/<name>/agents/<agent-name>.yaml`, fields like
`interface.display_name`, `interface.short_description`,
`policy.allow_implicit_invocation`) when a skill's behavior should
actually differ per agent. Don't add empty/boilerplate sidecars "just in
case" — `docs/decisions/0008-native-codex-plugin-support.md` added them
for Codex because this repo already has a real, stated position
(explicit-invocation-only) to encode, not as a pattern-establishing
exercise on its own.

### 6. Apply the version-sync guardrail

Any new manifest with its own `version` field joins
`docs/guardrails/plugin-manifest-version-sync.md` — bump it alongside
every other manifest's version on every release from then on.

### 7. Scope "testing" honestly

If the new agent's CLI/runtime isn't available in the current
environment, testing is limited to static validation (valid JSON,
required fields present, matches the documented schema). Say so
explicitly in the plan rather than claiming a live install/load test
happened. Leave the real test as a named, not-yet-done follow-up step.

## Why this is procedural, not axiomatic

This captures *how* to repeat a decision-making process this repo has
already been through once (for Codex), so the next agent (e.g. Cursor,
whenever that gets scoped) doesn't require re-deriving the same
judgment calls from zero. It doesn't carry independent tradeoffs beyond
what `docs/decisions/0008-native-codex-plugin-support.md` already
settled for the Codex case.
