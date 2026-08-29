---
name: roadmap
description: Interview the user about a plan or decision, then capture the outcome as durable knowledge-management artifacts (facts, intents/decisions, guardrails, skill prescriptions) plus a self-sufficient standalone roadmap. Use when the user wants a decision captured as project knowledge — not just discussed — e.g. "interview me and save this as knowledge", "capture this as an ADR", "turn this into a roadmap".
---

Interview the user relentlessly about every aspect of the plan or decision until you reach a shared understanding, then convert that understanding into durable knowledge artifacts on disk. This skill shares its interview mechanics with the `clarify` skill but does not stop at shared understanding — its job is to generate and save new knowledge as artifacts, following whatever structure the project already uses.

## Interview mechanics

Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

Ask questions one at a time, waiting for feedback before continuing. Asking multiple questions at once is bewildering.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking. The *decisions* are the user's — put each one to them with your recommended answer and wait for theirs.

When a decision has discrete options:
- Cap at 4 total, free-text catch-all included. If more genuine options exist than fit, merge the most similar/adjacent ones rather than exceeding the cap or dropping the free-text slot.
- State each option's tradeoff against the others; mark the recommended one "(Recommended)".
- Numeric answer (count, date, size)? Skip the list, ask openly with an optional default — plain-number answers collide with plain-number labels.
- Selectable-question tool available? Use it; its built-in "Other" option is the free-text catch-all — don't number options yourself or add a second "something else" entry.
- No tool: number each option with plain digits, then append exactly one final option inviting free text — never both an in-list "something else" and a separate "type your own".

## Detect the project's knowledge structure

Before writing anything, determine how this project already stores knowledge:
1. Look for a known convention (e.g. a knowledge-steward-style skill file describing fact/intent/guardrail/skill formats and directories).
2. If none is found, look for existing decisions/ADR, facts, or guardrails directories and infer the format from real examples already there.
3. If neither exists, ask the user where and in what format to write, before proceeding further.

Never invent a directory convention that doesn't match what the project already does.

## Numbering facts and decisions

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md`, where `NNNN` is a 4-digit, 1-based sequence number local to that directory (`0001`, `0002`, ...). Find the next number by counting the existing files in the target directory; the first file in a fresh directory starts at `0001`. Guardrails and skill prescriptions are filed by slug only (`docs/{guardrails,skills}/slug.md`), with no numeric prefix — they're looked up by topic, not by creation order.

## Classify at the end, not during

Do not tag or classify decisions while the interview is running — keep the interview itself as uncluttered as the base `clarify` skill. Once every question is resolved, classify each one into exactly one mode:
- **Descriptive** — this is what is true right now (an environmental fact, or a value the team chose)
- **Axiomatic** — this is what the team commits to, with context and rationale (an intent / decision record)
- **Normative** — this is what must or must not happen, derived from an axiomatic commitment plus a descriptive fact (a guardrail)
- **Procedural** — this is how to decide or act (a skill prescription)

## What must be captured

- Every explicit or implicit intent (a presupposition unambiguous enough to count as a commitment) must be captured as a record — never silently dropped.
- An intent becomes a full ADR/decision-record entry only if it is hard to reverse, surprising without context, or the result of a genuine tradeoff. An intent that fails all three still gets saved, but as a lighter artifact (a decision fact or inline note) rather than a full record.
- Descriptive, Normative, and Procedural decisions are written as real artifacts too (facts, guardrails, skill prescriptions respectively), in the detected format — not just labeled in a summary.

## Avoid duplicates

Before writing any artifact, search existing artifacts (by title, topic, frontmatter) for a likely match. If one is found, propose it ("this looks like an update to X — update it, or is this new?") and wait for confirmation rather than guessing. Extend matched files; never blindly overwrite.

## The changeset implementation plan

Alongside the four knowledge artifacts, produce one more file: a changeset implementation plan for the change the interview was about. This file must be self-sufficient for a **completely fresh session with zero prior context** — not just a resumed one. Every step spells out the full context a cold agent would need: exact file paths, what to do, why it matters, and what "done" looks like — never a reference like "as discussed above." Each step carries a status marker (e.g. done / pending / blocked) updated in place as work progresses, so re-reading the file alone tells any session — the same one, a resumed one, or a brand new one — exactly what remains.

Follow the same structure-detection rule for this file: reuse an existing plans/tasks directory convention if the project has one; otherwise default to `docs/plans/<slug>.md`.

## Before writing anything

List every file this session intends to create or update — path and artifact type (fact / intent / guardrail / skill / plan) — and get one explicit go-ahead before touching disk. This is a wider blast radius than a single-file change, so the extra checkpoint is cheap insurance.

## Hard limits

Never execute or implement the changeset plan yourself. Writing the four knowledge artifacts and the plan file is the deliverable — running the plan is a separate, later action, in a separate session.

Do not externally communicate any part of the plan until the user has confirmed shared understanding, and do not write any artifact file until the final go-ahead in "Before writing anything" above.
