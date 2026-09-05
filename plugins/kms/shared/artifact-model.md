## Artifact types

| Type | Mode | Origin | Where | Verified by |
|------|------|--------|-------|-------------|
| Environmental fact | descriptive | original | `facts/` | Observe from the world (tool output, docs, benchmarks) |
| Decision fact | descriptive | original | `facts/` | Check the governing decision is still current |
| Decision | axiomatic | original | `decisions/` | Expert review; immutable once accepted |
| Procedure | procedural | original | `skills/` | Expert review; can be refined |
| Guardrail | normative | derived | `guardrails/` | Re-derive from its sources; compare |

**Mode** is the kind of claim: descriptive — true right now; axiomatic — what the team commits to, with context and rationale; normative — must or must not happen, derived from an axiomatic commitment plus a descriptive fact; procedural — how to decide or act. A procedure covers both a shipped skill's own prescription and a project-specific workflow — both live in `skills/`.

A guardrail is only valid while its sources are current — a source change invalidates it.

## File formats

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md` (4-digit, 1-based, per directory); guardrails and procedures as `docs/{guardrails,skills}/slug.md`, no numeric prefix.

All four carry the base frontmatter `id, title, status, date, tags` — `status` is one of `draft | active | superseded | deprecated` — plus an optional `expires: <date or condition>` (when this stops being current), and these type-specific fields:

For `tags`: if `docs/skills/tags.md` exists, every tag assigned to any of the four types MUST come from it — check each intended tag against the list's stated meanings before writing it. If none fit, propose a new tag (name, one-line meaning, why nothing existing covers it) and get confirmation before using it and adding it to the list.

After writing any of the four types directly to disk, also add or update its row in that type's `INDEX.md` (`id, title, tags, status`, TOON format), if one exists.

Fact — add `kind: environmental | decision | derived | mixed` (mixed = file has both; label each section inline) and `governed-by: <decision-id>` (`TBD` = debt).

Guardrail — add `governed-by: <decision-id>`, `grounded-in: <fact-id[, ...]>`, and `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. Missing any of the three = undeclared, flag as debt.

Decision — add `track: product | process` (required, exactly one — never `both`/`mixed`: product = what the project is for and who it serves; process = how it's built, organized, or shipped); `superseded-by: <decision-id>`, required when `status: superseded`; optionally `governed-facts: [<fact-id>, ...]` and `fitness-functions: [<check description>, ...]`.

**Derivation recipe**: `Decision (why) + Fact (what is) → Guardrail (ought)`. The `derivation-note` states that step in one sentence; if either source changes, re-apply and propose updated guardrail text.
