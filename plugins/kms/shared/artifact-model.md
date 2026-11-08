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

## Admission

Before drafting any of the four types, decide whether the change is worth a record at all. Reject if a hard gate fails.

Hard gates:
- **Not already carried**: not stated in code, tests, config, tooling, history or a sibling record, and not a mechanical repeat of an enforced check. A decision is carried by those only if they also state its reason and the rejected alternative; a value or call visible in the code does not carry the reason for it.
- **Right shape**: one claim; no named person, contact details or secret. Name a role or system, not a person.
- **Recurrence (guardrails)**: applies to every future occurrence of a kind of change. A prohibition from one incident is admitted only with a stated cause that generalises.

Then estimate from the change: **shelf life** (how long it stays true; a decision is valid until superseded), **recurrence** (how likely a different future task meets the same question), **rediscovery cost** (tool calls, minutes, or asking another actor, which raises it). Admit when shelf life times recurrence clearly exceeds rediscovery cost and a future agent would act differently knowing it. Reject a raw reading, run result, status or timestamped event; a scoped claim with a source (a contract term, a vendor limit, a permanent state change) can be a fact. If the knowledge base already holds a record the change contradicts or supersedes, that is a reason to update it, not a new record.

Rejected means no record: say so in one line with the failed gate. Typical rejections: a rename or move visible in the diff, a one-line config or hygiene change, a CI result, who did what when, a meeting or on-call entry, "be careful" or "write tests" rules, a rule a lint or test already enforces.

Type for a pointer: a required path through another actor is a procedure; a static location (dashboard URL, vault path) is a fact; a standing consent before an action is a guardrail.

## File formats

Facts and decisions are filed as `docs/{facts,decisions}/NNNN-slug.md` (4-digit, 1-based, per directory); guardrails and procedures as `docs/{guardrails,skills}/slug.md`, no numeric prefix.

All four carry the base frontmatter `id, title, status, date, tags` — `status` is one of `draft | active | superseded | deprecated` — plus an optional `expires: <date or condition>` (when this stops being current), and these type-specific fields:

For `tags`: if `docs/skills/tags.md` exists, every tag assigned to any of the four types MUST come from it — check each intended tag against the list's stated meanings before writing it. If none fit, propose a new tag (name, one-line meaning, why nothing existing covers it) and get confirmation before using it and adding it to the list.

After writing any of the four types directly to disk, also add or update its row in that type's `INDEX.md`, if one exists: CSV — a header line naming the fields (`id, title, tags, status`), then one comma-separated row per artifact. A field containing a comma (e.g. `tags`) is wrapped in double quotes, with its items comma-separated inside the quotes — e.g. `"kms, naming, branding"`. If a value ever needs multiple parts that can't just be comma-separated inside quotes, quote the cell and separate with `;` instead — no field has needed this yet.

Fact — add `kind: environmental | decision`, chosen by how the fact is verified: `environmental` is true or false independent of any team decision and is checked by observing the world (tool output, upstream docs, repository contents, history; a figure recomputed from observations counts); `decision` restates what a governing decision fixed (a chosen name, value or rule) and is checked by confirming that decision still says so. A claim that needs both is written as two facts and `governed-by: <decision-id>` (`TBD` = debt). Optional `scope: {component: <str>, environment: <str>, version: <str>}` (any non-empty subset of the three keys; no others) says where the fact holds: the part of the system, the environment (e.g. `production`, `ci`), and the version or range it was observed on. A fact without `scope` makes an unqualified claim that holds everywhere. Set `scope` whenever the claim is limited; don't repeat it in the body. Facts only (`docs/decisions/0063-...`).

Guardrail — add `governed-by: <decision-id>`, `grounded-in: [<fact-id, decision-id, or guardrail-id>, ...]`, and `derivation-note: <one sentence: given decision X and fact Y, Z must/must not follow>`. `grounded-in` normally holds the independent fact a guardrail rests on; when no such fact exists, it may instead hold a decision or sibling-guardrail id — including the same id already in `governed-by`, when the guardrail is a direct, unmediated consequence of that decision alone (`docs/decisions/0051-...`). Always a YAML list, even with one entry — never a comma-joined string. Missing any of the three = undeclared, flag as debt.

Decision — add `track: product | process` (required, exactly one — never `both`/`mixed`: product = what the project is for and who it serves; process = how it's built, organized, or shipped); `superseded-by: <decision-id>`, required when `status: superseded`; optionally `governed-facts: [<fact-id>, ...]`, `fitness-functions: [<check description>, ...]`, and `accepted-by: <name>` (who is accountable for this decision, independent of who committed it — a human directing an AI agent's commits is still the accountable party; set when `status` first becomes `active`).

Procedure — optionally add `operationalizes: [<guardrail-id>, ...]` when this procedure is a runbook/playbook for a guardrail's required behavior, not general reference material. Many-to-many: a procedure may list several guardrails, and more than one procedure may list the same guardrail. Most procedures won't carry this field at all.

**Pinned edges** (optional, on facts and guardrails): a `pinned: {<id>: <revision>, ...}` map beside `governed-by`/`grounded-in`, one entry per edge target, records what each target looked like when the file was derived from it. Never write a revision by hand or from memory: after writing or re-deriving a file's edges, run `python3 <plugin>/shared/lint_check.py --root <project root> --pin <file>`, which recomputes every entry (the first 12 hex digits of a SHA-256 of the target without its edge fields and `date`, whitespace-insensitive). `lint` check 13 then flags a pinned edge by comparison when the target has changed since; edges without a pin are still judged by `lint`. Re-pin only after re-applying the derivation recipe against the changed target.

**Derivation recipe**: `Decision (why) + Fact (what is) → Guardrail (ought)`. The `derivation-note` states that step in one sentence; if either source changes, re-apply and propose updated guardrail text.

**Economy**: a fact, guardrail, or procedure stub (decisions and plans exempt) uses the shortest phrasing that preserves meaning. Before considering a newly-drafted one done, re-read it once specifically for restatement (a point already made earlier in this file, or in a sibling artifact from the same drafting pass) and length — tighten before finishing, not after, the same way a shipped `SKILL.md` edit gets one full re-read before being considered done.
