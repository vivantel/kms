---
name: decide
description: Interview the user about a decision, then write the outcome as durable knowledge artifacts (facts, decisions, guardrails, procedures) — records only, no plan file. Use when the user wants a decision captured as project knowledge, not just discussed, or turn an incident or retro into knowledge, e.g. "interview me and save this as knowledge", "capture this as an ADR", "record what we decided".
---

Interview the user about every aspect of a decision until you reach a shared understanding, then write that understanding as durable knowledge artifacts on disk, in the structure the project already uses. It does not stop at shared understanding. It writes records only: no plan file, no step list.

## Interview mechanics

Walk down each branch of the decision tree, resolving dependencies one by one. Each turn contains exactly one question, never a numbered list of questions, with your recommended answer; then stop and wait for the reply.

If a *fact* can be found by exploring the environment (filesystem, tools), look it up rather than asking. The *decisions* are the user's: put each to them with your recommended answer.

For discrete options:
- Cap at 4 total, free-text catch-all included; merge the most similar options rather than exceed the cap or drop the free-text slot.
- State each option's tradeoff against the others; mark the recommended one "(Recommended)".
- Numeric answer? Skip the list and ask openly with an optional default.
- Selectable-question tool available? Use it; its built-in "Other" is the free-text catch-all. No tool: number options with plain digits and append exactly one final option inviting free text.

## Detect the project's knowledge structure

Before writing, find how the project stores knowledge: a known convention (a skill file describing the formats), else existing decisions/facts/guardrails directories whose format you infer from real examples, else ask the user where and in what format. Never invent a directory convention.

Facts and decisions: `docs/{facts,decisions}/NNNN-slug.md`, 4-digit, 1-based, per directory (next number = highest across the directory and its `archive/`, plus one). Guardrails and procedures: `docs/{guardrails,skills}/slug.md`, no numeric prefix.

## When the input is an event

For an incident, failed experiment, retrospective or dependency breakage, interview from the event to its admissible residue: a root-cause fact with `source` pointing at the incident record, a generalised guardrail (a one-incident prohibition needs a cause that generalises), a procedure, a process decision. The event record itself fails admission and stays in the tracker the fact's `source` names.

## Classify at the end, not during

Keep the interview uncluttered. Once every question is resolved, classify each outcome into exactly one mode:
- **Descriptive**: true right now, about the environment or process (a fact)
- **Axiomatic**: what the team commits to, with context and rationale (a decision)
- **Normative**: what must or must not happen, derived from a decision plus a fact (a guardrail)
- **Procedural**: how to decide or act (a procedure)

Field definitions, lifecycle and the index rule are in `shared/artifact-model.md`; if `docs/skills/tags.md` exists, take tags from it.

## What must be captured

- Check every explicit or implicit commitment (a presupposition clear enough to count as one) against `shared/admission.md`. Never drop one silently.
- A commitment that passes becomes a record of its natural type, written in the detected format and the economy rule from `admission.md`. One that fails is not recorded: list it under "Not recorded" with the failed gate in your closing summary so the author can overrule it.
- Before writing any artifact, search existing ones (title, topic, frontmatter) for a likely match. If one exists, propose updating it and wait for confirmation; never blindly overwrite. A fact is updated in place with a new `last-verified`. An active decision's `## Decision`, `## Why` and `## Tradeoffs considered` are frozen, so replacing it means a new decision (next number), the old one set to `status: superseded` with `superseded-by`, both moved or indexed per the model (retired files go to `archive/`), and every guardrail citing the old one re-derived.
- A decision the user confirmed in this interview is written `status: active` with `accepted-by: <name or role>` (ask once); `draft` is only for stubs nobody confirmed.
- After writing, add or update each artifact's row in its type's `INDEX.md`, if one exists, then run `python3 shared/lint_check.py --root .` (this skill's directory; needs PyYAML, else say so) and fix findings in the files you wrote.

## Before writing anything

List every file you intend to create or update, with path and artifact type, and get one explicit go-ahead before touching disk.

## Hard limits

Write no artifact before that go-ahead, and communicate nothing externally before the user confirms shared understanding. Do not create a plan or implementation file; planning belongs to a separate planning tool.
