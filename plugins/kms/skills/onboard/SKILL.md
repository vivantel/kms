---
name: onboard
description: Creates a role-specific onboarding plan from a project's existing knowledge artifacts, without writing anything. Use when the user wants a ramp-up plan for a specific role, e.g. "onboard me as a frontend developer for this project", "what should a new QA hire read first here".
---

Read `docs/{facts,decisions,guardrails,skills}/` and produce a 5-day, role-tailored onboarding plan — without writing to disk.

## Before producing a plan

1. Ask for the role if not given — it shapes everything else, don't guess it.
2. Read each type's `INDEX.md` first, if present, to identify what's relevant to the role — ignore any `(umbrella)`-marked tag when matching (same exclusion `lint` check 16 applies). Read all four artifact directories directly when no index exists, or when the index-narrowed set looks thin for a role this broad (same staleness caveat `query` applies). If `docs/skills/{product,process}-track-roles.md` exists and lists the given role, weigh its stated scope; otherwise use judgment about what the role would need.
3. **Warn if critical artifacts are missing** before producing the plan — most importantly, no facts at all, but also an empty `decisions/` or `guardrails/` if the project claims to use this system. Say plainly the plan is built on an incomplete base; don't let it read as if the knowledge base were complete when it isn't.
4. No knowledge base at all? Say so and stop — recommend `bootstrap`, don't improvise a plan from nothing.

## Producing the plan

5 days, each stating:
- **Goal** — what the person should understand or do by end of day, specific to the role.
- **Read** — links to the specific artifacts for that day and role (`docs/decisions/000X-....md`, not "the decisions folder").
- **Run** — which of this plugin's skills to try and why.

A reasonable shape (adjust to what actually exists for this role — don't force artifacts onto a day that doesn't need them):
1. Orient — highest-level facts and most consequential decisions.
2. Role-specific decisions and guardrails — what this role must not violate and why.
3. Role-specific facts and current state.
4. First real task, using `query` to resolve anything unclear from days 1-3.
5. Practice a decision end-to-end with `clarify`, run `capture` afterward if they touched anything.

Tailor content, not just headings — two roles should get visibly different reading lists and goals, not the same plan with the role name swapped in.

## Out of scope

Writing or editing any artifact (read-only, like `query`), and generating the underlying facts/decisions/guardrails if they don't exist yet — that's `bootstrap`.
