## Artifact types

| Type | Mode | Origin | Where | Verified by |
|------|------|--------|-------|-------------|
| Environmental fact | descriptive | original | `facts/` | Observe from the world (tool output, docs, benchmarks) |
| Decision fact | descriptive | original | `facts/` | Check the governing decision is still current |
| Decision | axiomatic | original | `decisions/` | Expert review; immutable once accepted |
| Skill prescription | procedural | original | `skills/` | Expert review; can be refined |
| Guardrail | normative | derived | `guardrails/` | Re-derive from its sources; compare |

**Mode** is the kind of claim: descriptive — true right now; axiomatic — what the team commits to, with context and rationale; normative — must or must not happen, derived from an axiomatic commitment plus a descriptive fact; procedural — how to decide or act.

A guardrail is only valid while its sources are current — a source change invalidates it.

## File formats

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md` (4-digit, 1-based, per directory); guardrails and skill prescriptions as `docs/{guardrails,skills}/slug.md`, no numeric prefix.

All four carry the base frontmatter `id, title, status, date, tags`, plus these type-specific fields:

Fact — add `kind: environmental | decision | derived | mixed` (mixed = file has both; label each section inline) and `governed-by: <decision-id>` (`TBD` = debt).

Guardrail — add `governed-by: <decision-id>`, `grounded-in: <fact-id[, ...]>`, and `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. Missing any of the three = undeclared, flag as debt.

Decision — add `track: product | process` (required: product = what the project is for and who it serves; process = how it's built, organized, or shipped); optionally `scope: <what it applies to>`, `expires: <date or condition>`, `governed-facts: [<fact-id>, ...]`, and `fitness-functions: [<check description>, ...]`.

**Derivation recipe**: `Decision (why) + Fact (what is) → Guardrail (ought)`. The `derivation-note` states that step in one sentence; if either source changes, re-apply and propose updated guardrail text.
