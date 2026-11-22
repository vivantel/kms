schema-version: 1.0.0
<!-- Contract for consumers: docs/skills/core-contract.md -->

## Artifact types

| Type | Mode | Where | Verified by |
|------|------|-------|-------------|
| Fact | descriptive: true now | `facts/` | Re-observe from `source` |
| Decision | axiomatic: what the team commits to | `decisions/` | Expert review |
| Guardrail | normative: must or must not happen | `guardrails/` | Re-derive from its sources |
| Procedure | procedural: how to decide or act | `procedures/` | Expert review |

A fact is true of the environment or the process, not a restatement of product behaviour. Behaviour that must hold is a guardrail; what a product should do is a spec, kept in a spec tool. A guardrail is valid only while its sources are current.

The knowledge directory is the one containing `decisions/`. Resolve it once, in order: `--docs`; the `kms-dir:` line inside the AGENTS.md kms block; `.vivantel/akasha/docs/` if it exists; `docs/` if it holds `decisions/`; the first root-level directory holding `decisions/`. A new project's `bootstrap` writes `kms-dir:`. Procedures were `skills/` before the rename: either name is read for one release, and `migrate.py --rename` moves one to the other. Retired files move to `<type>/archive/`, which has its own `INDEX.md`.

## Fields

Every artifact: `id`, `title`, `status`, `date`, `tags`. Optional: `expires: <date>`, `expires-when: <condition>`.

- `id`: `NNNN-slug` for facts and decisions (4-digit, 1-based, per directory); `slug` for guardrails and procedures. Matches the file name.
- `status`: `draft` (proposed, not binding) | `active` | `superseded` (replaced by a named successor) | `deprecated` (retired without replacement; the body's first line says why).
- `date`: creation date; never moves.
- `tags`: from `procedures/tags.md` in the knowledge directory when it exists. A new tag is proposed (name, meaning, why nothing fits) and confirmed before use.
- `superseded-by: <id>`: any type; required when `status: superseded`.
- Fact: optional `source: <url | path | command>`, `last-verified: <date>` (moves only on re-observation; a URL or command `source` older than the stale threshold, or a path `source` that is gone, is stale), `scope: {component, environment, version}` (any non-empty subset; set whenever the claim is limited).
- Guardrail: `governed-by: [<decision-id>, ...]` (non-superseded decisions), `derivation-note: <one sentence naming every id in both edges: given X and Y, Z must or must not follow>`; optional `enforced-by: <code path | ci job | hook>` (the check that enforces it, which also keeps it from counting as orphaned); optional `grounded-in: [<fact-id>, ...]` (absent means a direct consequence of the governing decisions); optional `pinned: {<id>: <revision>}`.
- Decision: optional `governed-facts: [<fact-id>, ...]`, `fitness-functions: [{check, enforced-by, last-verified}, ...]`, `accepted-by: <name | role>` (who is accountable; set when `status` first becomes `active`).
- Procedure: optional `governed-by`, `operationalizes: [<guardrail-id>, ...]`.

Lists are always YAML lists. `TBD` stands for an unresolved id, a debt that ages.

## Lifecycle

`## Decision`, `## Why` and `## Tradeoffs considered` are frozen once a decision is `active`. `status`, `superseded-by`, `accepted-by`, `tags`, expiry, `fitness-functions` and dated, additive `## Amendment <date>` sections stay editable. Retiring a source (a superseded decision, a deprecated fact) triggers re-derivation of every guardrail that cites it in the same pass: re-point and note "re-derived <date> from <id>" if the consequence stands, else deprecate.

A pin is the first 12 hex digits of the SHA-256 of the target without its edge fields, `pinned`, `date`, `accepted-by`, `last-verified`, `status`, `superseded-by`, `expires` and `expires-when`, whitespace collapsed. Write it with `python3 <plugin>/shared/lint_check.py --root <root> --pin <file>`, never by hand. Pins are optional; an unpinned edge is judged by `lint`.

Stale threshold: 180 days, overridable by one line in the project's AGENTS.md block.

## Registries and markers

A registry is a non-governed file: `INDEX.md`, `procedures/tags.md` in the knowledge directory, role lists, the docs manifest. It carries `kms-registry: <name>` in frontmatter, or `<!-- kms-registry: <name> -->` as the first line of a pure CSV, and is skipped by the type checks. Other markers: `kms-seeded`, `kms-generated`, same two forms.

`INDEX.md` per type: CSV, header `id, title, tags, status`, one row per artifact; a value with a comma is double-quoted, and a multi-tag `tags` cell joins its items with comma and space inside the quotes (`"kms, naming"`), exactly as the checker compares it. After writing an artifact, add or update its row.

## Derivation

`Decision (why) + Fact (what is) → Guardrail (ought)`. If a source changes, re-apply and propose updated guardrail text.

<!-- fields: id title status date tags expires expires-when superseded-by source last-verified scope governed-by derivation-note enforced-by grounded-in pinned governed-facts fitness-functions accepted-by operationalizes kms-registry kms-seeded kms-generated -->
