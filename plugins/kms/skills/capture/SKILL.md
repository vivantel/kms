---
name: capture
description: Turn what a work session produced into durable knowledge — draft new decisions, update changed facts, flag contradictions, catch human-doc drift. Use after a work session that touched decisions, facts, or documented behavior, e.g. "capture what this session decided", "run the knowledge check on what this session changed", "did anything here need capturing as a decision or fact". Writes records; for whole-repo health use lint, for a diff before commit use conform.
---

If the project has no knowledge system yet, run `bootstrap` first — this skill maintains what that one sets up. For whole-knowledge-base health, independent of any one session, run `lint` instead — this skill only reasons about what just happened.

## Artifact model

In this skill's directory: `shared/artifact-model.md` (the schema: types, fields, lifecycle) and `shared/admission.md` (the gates and economy rule for anything drafted here) — read both before drafting anything.

## Checks, one pass per invocation

1. **New decision?** Apply `admission.md` first; if the change fails it, draft nothing and say which gate failed in one line. Otherwise draft a stub: next id, title, one-line motivation, `status: draft`. Don't finalize without the owning domain's sign-off — once given, set `status: active` and `accepted-by: <name>` in the same edit, not just the former. If it explicitly replaces an existing decision, also update that decision's `status` to `superseded` and add `superseded-by: <new-decision-id>` — don't leave two `active` decisions on the same topic for a later `lint` pass to catch. Re-point every guardrail whose `governed-by` named the old decision to the new one in the same pass, noting "re-derived <date> from <id>" where the consequence stands, else deprecate it.
2. **Fact changed?** Re-observe every fact whose `source` is a path the session changed, or whose `scope.component` overlaps the diff; correct it if changed, and bump `last-verified` only if re-observed. If a file with a `pinned` map is derived from it, re-apply the derivation recipe, then re-pin that file with `lint_check.py --pin` (see the artifact model). If the governing decision is no longer current, surface the contradiction now.
3. **New automatable rule?** Append `{check: <rule text>, enforced-by: none, last-verified: <today>}` to the governing decision's `fitness-functions`, or draft a `status: draft` decision stub when no decision governs it.
4. **Contradiction found?** Block. Don't close the session until resolved or explicitly deferred with a written note (decision, fact, or stub).
5. **Human-doc drift?** If watched paths overlap what changed this session, propose the specific update; if the doc's still accurate, bump its verified date.
6. *(retired; the number stays unused)*
7. **Index entry?** Add or update the row for anything drafted or edited this pass, per the artifact model's index rule.
8. **Checker.** Run `python3 shared/lint_check.py --root .` (this skill's directory; needs PyYAML, else say so) and fix findings in files you touched.

## Recommending a new skill

When proposing a domain for its own skill, state: domain name, trigger condition, one hard constraint, one fitness-function candidate. Proposals — the team decides adoption and naming.

## Out of scope

Authoring final decision records (owning domain), choosing which domains become skills, writing behavioral rules in skill files, arbitrating domain conflicts — surface to the team. Structural validity independent of this session (dangling references, missing fields, expired decisions, redundant/unenforced guardrails, verbosity, sync drift) — that's all `lint`'s job now, checked there once, not duplicated here.
