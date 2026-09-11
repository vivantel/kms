# Vivantel KMS

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-5A32FB.svg)](https://code.claude.com/docs/en/plugins.md)

Vivantel KMS (Knowledge Management System) — for any git-based project, capture decisions, facts, and guardrails as durable, traceable artifacts, maintained automatically as the project evolves. Works for software repos, technical documentation, even long-form writing like research papers, not just code.

The skill content itself is agent-neutral — no product-specific language or tooling assumptions — so any AI coding agent that can read and follow instructions from a file can use it. `kms` additionally ships one-command install packaging for three: a Claude Code plugin marketplace, a native Codex plugin, and a self-hosted remote-skills manifest for Kilo Code CLI.

---

## The model, before the skill list

KMS is a **knowledge architecture**, not a plugin marketplace. Every artifact in the system is classified along four axes, and the system's behavior is defined by two planes. Understanding these is necessary before the skill list makes sense.

### Artifact axes

Every artifact carries these classifications:

| Axis | Values | Required | Notes |
|------|--------|----------|-------|
| **Type** | fact, decision, guardrail, skill (procedure) | Yes | Determines mode, origin, and derivation |
| **Track** | product, process | Yes (decisions); inherited (facts, guardrails, skills) | `product` = what the project is for; `process` = how it's built |
| **Domain** | business domain (billing, auth, …) | Optional | For monorepos; tags carry this |
| **Lifecycle** | draft, active, superseded, deprecated | Yes | Unified across all four types |

**Type** determines the *mode of claim*:
- **Fact** (descriptive) — what's true right now. Sub-kinds: *environmental* (observed from the world), *decision* (a value the team chose), *derived* (computed from other artifacts), *mixed*.
- **Decision** (axiomatic) — what the team commits to, with context and rationale. Immutable once accepted.
- **Guardrail** (normative) — what must or must not happen. **Derived** from a decision + a fact via the derivation recipe: `Decision (why) + Fact (what is) → Guardrail (ought)`.
- **Skill / Procedure** (procedural) — how to decide or act. Can be refined.

**Track** answers: is this knowledge about *what we make* (product) or *how we make it* (process)? **Any artifact type can be either.** Decisions declare `track` explicitly; facts, guardrails, and skills inherit relevance from their governing decision. The line: does the decision change what the project serves (`product`), or how it's built to serve that audience (`process`)? Skill existence, format, and packaging are `process`; mission, scope, and target agents are `product`.

**Lifecycle** uses one shared enum across all four types:
- `draft` — proposed, not yet accepted
- `active` — current and in force
- `superseded` — replaced by a newer artifact; decisions **must** carry `superseded-by: <decision-id>` pointing at the replacement
- `deprecated` — no longer applicable, not replaced
- Optional `expires` (date or condition) — when the artifact stops being current

**Invariants the system enforces:**
- No session closes with an unresolved contradiction (`capture` check 4 blocks)
- No two `active` decisions on the same topic (`lint` check 16)
- Every guardrail declares its derivation: `governed-by` (decision), `grounded-in` (fact(s)), `derivation-note` (one sentence) — missing any = debt (`lint` check 2)
- Every fact carries `kind` and `governed-by`; `governed-by: TBD` = debt
- Track is exactly one of `product` | `process` — never `both`/`mixed` (`lint` check 15)

### System planes

| Plane | What it covers |
|-------|----------------|
| **Quality Attributes** | Traceability (commit trailers → artifacts), Durability (git-backed, no DB), Queryability (`INDEX.md` + `query`), Consistency (`lint` 22 checks), Evolvability (lifecycle, supersession, archive) |
| **Governance** | **Distributed**, not absent. Lives in: git merge (authority), domain sign-off (`track` role lists), lifecycle status (`draft` → `active` requires sign-off), `superseded-by` (explicit replacement), fitness-function debt (declared, not hidden), role lists (`product-track-roles.md`, `process-track-roles.md`) |

**Governance is distributed** — there is no central approver. A decision becomes `active` when its owning domain signs off (recorded in the decision's prose and reflected in the role list for that track). Guardrails are only valid while their sources are current; a source change invalidates them (`lint` check 13 re-derives). Fitness functions are declared on decisions and tracked as debt until automated. The system makes governance *visible*, not *automated* — approval is delegated to git merge and domain review, not absent.

### Division of responsibility between skills

| Skill | Scope | Reads | Writes | Blocks |
|-------|-------|-------|--------|--------|
| `bootstrap` | One-time setup / gap-fill | git history, existing docs | `docs/` artifacts, `INDEX.md`, role lists, tags | — |
| `capture` | Session-scoped maintenance | session output, `docs/` | decision stubs, fact updates, `INDEX.md` | **Yes** — blocks on unresolved contradiction |
| `lint` | Whole knowledge base | all `docs/` | — (reports only) | — |
| `query` | Read-only Q&A | `docs/` + `INDEX.md` | — | — |
| `roadmap` | Interview → durable artifacts | `docs/` (structure detection) | decisions, facts, guardrails, skills, plan | — (checkpoint before write) |
| `conform` | Pre-merge diff check | diff + `docs/` | — (reports only) | — |
| `refactor-plan` | Phased refactor plan | `docs/` + code | — | — (flags guardrail conflicts) |
| `onboard` | Read-only onboarding | `docs/` + `INDEX.md` | — | — |
| `brainstorm` | Ideation only | — | — | — (never queries KB) |
| `clarify` | Interview only | env facts | — | — |
| `attribute` | Commit/PR prose | staged diff | — (proposes message) | — |
| `changelog` | History rendering | git log | `CHANGELOG.md` | — |
| `uninstall` | Cleanup | `docs/` markers | strips markers / deletes | — |

**Key boundaries:**
- `capture` = session-scoped; `lint` = whole-repo, independent of session
- `roadmap` writes artifacts; `clarify`/`brainstorm`/`refactor-plan`/`onboard`/`query` are read-only
- `conform` checks code against KB; `lint` checks KB against itself
- `bootstrap` seeds templates (`kms-seeded`); `capture` creates project artifacts (`kms-generated`)

---

## Skills described by behavior and invariants

| Skill | What it enforces / blocks / refuses |
|-------|--------------------------------------|
| **`quickstart`** | Sequences `bootstrap` + one full `roadmap` run for a first-time user. Refuses to re-run setup if `docs/` already populated. |
| **`bootstrap`** | Extracts intents from git history as decision *stubs* (not full records — final authorship belongs to the owning domain). Extracts facts from embedded tables/defaults. Audits guardrails for missing `governed-by`/`grounded-in`/`derivation-note` (flags as debt). Inventories fitness functions (automated + not-yet-automated). Seeds baseline guardrails from `templates/`. Writes `kms-generated` role lists, tags, docs-manifest, and `INDEX.md` files. **Refuses** to finalize decisions, choose which domains become skills, or arbitrate domain conflicts. |
| **`brainstorm`** | Generates 5–7 *distinct* approaches (differs in mechanism/tradeoff, not parameters). **Never queries the knowledge base** — ideation stays unanchored. **Writes nothing to disk**. Refuses to rank/filter during generation; synthesis is a separate, explicit phase. Refuses to capture an approach as knowledge (that's `roadmap`). |
| **`clarify`** | Interviews one question at a time. **Looks up facts from the environment** instead of asking. Puts each decision to the user with a recommended answer. Caps discrete options at 4 + free-text. **Refuses** to execute, implement, or externally communicate any part of the plan until shared understanding is confirmed. |
| **`roadmap`** | Same interview mechanics as `clarify`, but **writes durable artifacts** after classification. Classifies at the end: Descriptive → fact, Axiomatic → decision, Normative → guardrail, Procedural → skill. Every intent captured — full ADR if hard to reverse/surprising/tradeoff; lighter artifact otherwise. **Deduplicates** against existing artifacts before writing. Produces a self-sufficient changeset implementation plan (concrete files, steps, done/pending/blocked per step). **Checkpoint**: lists every file to create/update and gets explicit go-ahead before writing. **Hard limit**: never executes the plan; never communicates externally before confirmation. |
| **`capture`** | Runs 7 checks per invocation: (1) new decision → draft stub with `track`, `status: draft`; if replacing existing, also marks old `superseded` + `superseded-by` — **no two active decisions on same topic left for lint**. (2) changed fact → update + `last-verified`; surfaces contradiction if governing decision stale. (3) new automatable rule → fitness-function debt entry. (4) **contradiction found → BLOCKS**; session doesn't close until resolved or explicitly deferred with written note. (5) human-doc drift → proposes update or bumps verified date. (6) role list gap → proposes addition. (7) index entry → updates `INDEX.md`. **Defers** to `lint`: structural validity, expired decisions, redundant guardrails, verbosity, stale derived artifacts, archive candidates, tag hygiene, role-list-gone-cold, draft/TBD staleness. |
| **`lint`** | 22 structural checks over the **entire** knowledge base (live + `archive/` for refs): dangling refs, missing fields, numbering collisions, expired decisions, redundant guardrails, audit-log facts, orphaned artifacts, unenforced guardrails, stale prose refs, verbosity, unsplit statements, baseline sync, derived artifact stale, role list cold, track exclusivity, cross-artifact contradiction (by non-umbrella tag), stale draft/TBD debt, stale fitness functions, index sync, archive candidates, tag off-list, tag cold. **Reports only** — never fixes without confirmation. **Excludes** `docs/plans/` (not a governed type) and `kms`'s own packaging layer (`plugins/kms/skills/`). |
| **`query`** | Reads `INDEX.md` first (ignores `(umbrella)` tags), falls back to direct search. **Never guesses** — if KB doesn't settle it, says so. Follows `superseded-by` transitively to the final active decision. Cites every artifact as `Refs: <path>` (matches `attribute` trailer format). **Refuses** to write or edit any artifact. |
| **`onboard`** | Produces 5-day role-tailored plan with specific artifact links and skill runs. **Warns** if critical artifacts missing (no facts, empty decisions/guardrails). **Stops** if no KB at all — recommends `bootstrap`. **Refuses** to write artifacts or generate missing KB. |
| **`refactor-plan`** | Queries KB for constraints, maps dependencies from code, produces phased plan with verification checkpoints and per-phase rollback. **Flags guardrail conflicts explicitly** — doesn't work around or drop them. Recommends post-refactor KB updates via `roadmap`/`capture`. **Refuses** to write artifacts or execute steps. |
| **`conform`** | Checks a pending changeset (staged diff, base diff, PR range, or commit range) against relevant guardrails. **Reports every finding**, grouped by guardrail. **Refuses** to check changes to `docs/{facts,decisions,guardrails,skills}/` — defers to `lint`/`capture`. **Refuses** to fix anything, plan refactors, or draft commit messages. |
| **`attribute`** | Drafts Conventional Commit message: `type: summary` + intent body + `Refs:` trailers (one per confirmed artifact). **Confirms artifact list with user** before committing — never guesses silently. PR description: collects union of `Refs:` from branch commits, renders Intent / What changed / Refs. **Refuses** to apply conventions to plain `git commit` unless invoked. |
| **`changelog`** | Generates Keep a Changelog entry from git history since last tag (or full history). Maps Conventional Commit types → categories. Uses Why-body from commits. **Asks for version + date** before writing. **Refuses** auto-versioning, release automation, `[Unreleased]` section. |
| **`uninstall`** | Scans for: (1) `kms-seeded` files matching `templates/`, (2) `kms-generated` files, (3) `<!-- kms:start/end -->` block in AGENTS.md, (4) still-draft decisions / `governed-by: TBD` facts. **Reports all findings grouped** before any action. Per finding: **detach** (strip markers, keep content) or **remove** (delete). **Never touches**: decisions/facts past `draft`/`TBD`, guardrails without `kms-seeded`, any file without `kms-generated` (project-owned). **Refuses** to uninstall the plugin itself (host command). |

---

## What this system does not do

Aggregated from every skill's `Out of scope`:

| Category | What's missing | Why / delegation |
|----------|----------------|------------------|
| **Approval / sign-off** | No automated approval gate | Delegated to git merge + domain sign-off (track role lists) |
| **Execution** | No skill runs code, deploys, or implements plans | `roadmap` writes a plan; a separate session runs it |
| **Domain arbitration** | No skill chooses which domain owns a decision | Surfaces to the team |
| **Skill adoption** | No skill decides a proposed domain becomes a skill | Proposes only; team decides |
| **Finalizing decisions** | `bootstrap`/`capture` write stubs only | Owning domain authors the full record |
| **Cross-project sync** | No multi-repo knowledge sync | Out of scope for this system |
| **Release automation** | No version bumping, tagging, publishing | `changelog` only renders history |
| **KB structural validation of plans** | `lint` doesn't validate `docs/plans/` | Plans are disposable, not governed artifacts |
| **Agent-specific behavior in skills** | Skills are agent-neutral by guardrail | Per-agent overrides only via optional `agents/<agent>.yaml` sidecars |
| **Auto-running skills** | No hooks that run `capture`/`lint` automatically | Explicit invocation only (except the install-time `capture` nudge hook) |

---

## Reading guide

For a new reader, in order:

1. **`AGENTS.md`** — repository structure, conventions, how to add skills/plugins, the marker conventions (`kms-seeded`, `kms-generated`, `<!-- kms:start/end -->`), and the packaging layer (`plugins/kms/` vs `docs/`).
2. **`docs/skills/kms-architecture.md`** — the four layers (internal KB, packaging, templates, hooks) and how `bootstrap`/`capture`/`lint`/`conform` relate.
3. **`plugins/kms/shared/artifact-model.md`** — the four artifact types, their fields, and the derivation recipe (`Decision + Fact → Guardrail`).
4. **`docs/decisions/0039-unify-lifecycle-and-drop-scope.md`** — unified lifecycle (`draft|active|superseded|deprecated`), `expires`, `superseded-by`, why `scope` was dropped.
5. **`docs/decisions/0010-decision-track-field.md`** — `track: product | process`, why required, why decisions only.
6. **`docs/guardrails/`** — each guardrail shows the derivation pattern: axiomatic basis (decision) + descriptive basis (fact) → normative conclusion.
7. **`plugins/kms/skills/<skill>/SKILL.md`** — each skill's actual behavior, constraints, and `Out of scope`.
8. **`evals/<skill>/promptfooconfig.yaml`** — what the system guarantees (tested behavior), e.g. `capture` blocks on contradiction, `lint` catches dangling refs, `roadmap` asks one question per turn.

---

## End-to-end example

A decision is drafted, a guardrail derives from it, a skill enforces it, `conform` checks a diff against it.

1. **Draft the decision** (`roadmap`):
   - Interview: "We're switching the public API rate limiter from a fixed 60s window to a token bucket."
   - Questions resolve: burst tolerance, bucket capacity, refill rate, client migration path.
   - Classification: Axiomatic → **decision** `0047-token-bucket-rate-limit.md` with `track: product`, `status: active`, `expires: 2027-01-01` (provisional until GA).
   - Decision records: rationale (bursty traffic trips fixed window), tradeoffs (complexity vs fairness), fitness functions (load test burst scenarios).

2. **Derive the guardrail** (`roadmap` or `capture`):
   - Normative → **guardrail** `token-bucket-enforcement.md`:
     - `governed-by: 0047-token-bucket-rate-limit`
     - `grounded-in: 0012-api-traffic-profile` (fact: observed burst pattern)
     - `derivation-note: "Given decision 0047 (token bucket for burst tolerance) and fact 0012 (clients burst at window edges), the rate limiter MUST enforce token-bucket semantics, not fixed-window."`
   - Guardrail is only valid while decision 0047 and fact 0012 are current.

3. **Skill enforces it** (existing skill, e.g. the rate-limiter implementation skill):
   - The skill's body implements token-bucket logic.
   - `lint` check 8 (`Unenforced guardrails`) verifies the skill's body actually says what the guardrail requires — if not, flagged.

4. **`conform` checks a pending diff**:
   - Developer opens PR changing the rate limiter to a sliding-window algorithm.
   - `conform` finds guardrail `token-bucket-enforcement.md`, sees the diff violates it (removes token-bucket logic).
   - Reports: `guardrails/token-bucket-enforcement.md` violated in `src/ratelimit.go:42-58` — fixed-window logic replaces token-bucket; governed by decision 0047.
   - PR cannot land without resolving: either update the decision (new `roadmap` run) or revert the diff.

**Traceability chain:** commit trailer `Refs: docs/decisions/0047-token-bucket-rate-limit.md` → decision → guardrail → skill behavior → `conform` check → PR gate.

---

## Installing

Supports Claude Code, Codex, and Kilo Code CLI — full per-agent steps in [`INSTALLING.md`](INSTALLING.md). Quick start for Claude Code:

```
/plugin marketplace add vivantel/kms
/plugin install kms
```

## Repo structure

```
.claude-plugin/marketplace.json                     # marketplace manifest
INSTALLING.md                                        # per-agent install steps (Claude Code, Codex, Kilo Code CLI)
plugins/kms/.claude-plugin/plugin.json               # Claude Code plugin manifest
plugins/kms/.codex-plugin/plugin.json                # Codex plugin manifest
plugins/kms/skills/index.json                        # Kilo Code CLI remote-skills manifest
plugins/kms/skills/<skill>/SKILL.md                  # one skill definition per subdirectory
plugins/kms/skills/<skill>/examples.md               # 2-3 worked usage examples per skill
plugins/kms/shared/artifact-model.md                 # artifact types, fields, derivation recipe
plugins/kms/templates/<artifact-type>/               # shippable seed content (currently guardrails/)
plugins/kms/hooks/hooks.json                         # Claude Code plugin hooks (e.g. capture nudge)
docs/{facts,decisions,guardrails,skills}/            # this repo's own knowledge base (dogfooded)
docs/plans/                                          # implementation plans from roadmap (not governed)
evals/<skill>/                                       # promptfoo eval cases per shipped skill
```

## This repo dogfoods its own skills

`kms`'s design rationale — why each skill works the way it does, what must or must not happen, and what's currently true about the repo — is recorded as knowledge artifacts under `docs/`, maintained with the same `bootstrap`/`capture` skills this plugin ships, and checkable with the same `lint`/`query` skills too. See [`AGENTS.md`](AGENTS.md) for the full structure and conventions.

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md). This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).

## License

[MIT](LICENSE)