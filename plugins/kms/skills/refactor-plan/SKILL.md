---
name: refactor-plan
description: Produces a safe, phased refactoring plan that respects existing decisions and guardrails, without writing anything. Use when the user wants a refactor planned against what the project has already committed to, e.g. "plan a refactor of the payment module to use Stripe instead of Braintree", "plan migrating from REST to GraphQL".
---

Given a refactoring goal, produce a phased plan grounded in the project's existing knowledge base — without writing to disk.

## Phase 1: query the knowledge base

Search `docs/{facts,decisions,guardrails,skills}/` for anything relevant — constraining decisions, guardrails the refactor must not violate, facts bearing on feasibility. Cite every artifact by path, the same discipline `query` uses. If nothing relevant is found, say so plainly rather than proceeding as if the knowledge base had settled something it didn't.

## Phase 2: map dependencies

Identify what the refactor touches and what depends on it — call sites, config, other modules, external consumers. Do this directly (read the code, follow references); don't assume access to `lint` or any other skill running as a sub-step. If the knowledge base bears on the dependency map, separately recommend running `lint` before/after for full validation — but the map itself doesn't depend on that recommendation being followed.

## Phase 3: produce the phased plan

Ordered phases, each with:
- **Steps** — concrete, in order.
- **Verification checkpoint** — how to confirm this phase succeeded before starting the next.
- **Rollback strategy** — how to undo this phase specifically, not just "revert everything."

**Guardrail conflicts**: if a planned step would violate a guardrail found in Phase 1, don't silently work around it or drop it — flag it explicitly, cite the guardrail, and ask the user to confirm before including it.

## Phase 4: recommend post-refactor updates

List facts or decisions that will be stale once the refactor lands, and recommend they be updated via `roadmap` or `steward` — not by this skill directly.

## Out of scope

Writing or editing any artifact, and executing any step of the plan — this skill only plans. `roadmap` captures the refactor's own rationale as a decision if the user wants that recorded separately.
