---
id: product-process-track-and-domain-agnostic-scope
title: Add the decision track field; generalize bootstrap beyond software
status: pending
date: 2026-08-30
---

# Add the decision track field; generalize bootstrap beyond software

## Context for a fresh session

This repo (`vivantel/kms`) is a Claude Code plugin marketplace with one
plugin, `kms`, containing six skills under
`plugins/kms/skills/{clarify,roadmap,bootstrap,steward,attribute,changelog}/`.

A `roadmap`-skill interview (2026-08-30) produced two decisions this
plan implements:

- `docs/decisions/0010-decision-track-field.md` — every decision gets a
  required `track: product | process` field. `product` = decisions about
  what kms is for and who it serves; `process` = decisions about how kms
  is built, organized, or shipped. Full definition and the retrofit
  classification for all 9 existing decisions are in that file.
- `docs/decisions/0011-kms-domain-agnostic-beyond-software.md` —
  `clarify`/`roadmap`/`bootstrap`/`steward` generalize beyond software
  projects; `attribute`/`changelog` and the git+Markdown storage
  substrate are unchanged. `bootstrap` is the only skill with actual
  software-specific wording today.

The corresponding guardrail is `docs/guardrails/decision-track-field.md`.

This plan file is what turns those decisions into actual file edits. A
cold session should be able to execute every step below by reading only
this file plus the three artifacts above — no other prior context
required. **Nothing below has been executed yet.** Writing the three
knowledge artifacts and this plan was `roadmap`'s deliverable; running
this plan is a separate, later action, per that skill's own hard limit
("never execute the changeset plan yourself").

## Steps

### 1. [pending] Add `track` to the 9 existing decisions

For each file below, add `track: <value>` to the YAML frontmatter,
immediately after the `tags:` line (matching the field order other
skills already use: `id, title, status, date, tags`, then type-specific
fields):

- `track: process` — `0001-knowledge-artifact-storage-convention.md`,
  `0002-commit-pr-attribution-skill-design.md`,
  `0003-commit-trailer-traceability.md`,
  `0004-conventional-commits-adoption.md`,
  `0005-changelog-generation-design.md`,
  `0007-claude-md-agents-md-symlink.md`,
  `0009-bootstrap-and-steward-skills.md`
- `track: product` — `0006-agent-agnostic-scope.md`,
  `0008-native-codex-plugin-support.md`

Do not touch any other field or the body prose of any of these files.

**Done when**: all 9 files have a `track` field with the value listed
above, and each file's frontmatter is still valid YAML.

### 2. [pending] Update `roadmap`'s classification step

In `plugins/kms/skills/roadmap/SKILL.md`, under "## Classify at the end,
not during", after the four-item mode list (Descriptive/Axiomatic/
Normative/Procedural), add this paragraph:

```
Decisions additionally carry a `track`: **product** — what the project
is for and who it serves (mission, scope, target audience); or
**process** — how the current deliverable is built, organized, or
maintained (which components exist, formats, packaging, workflow).
```

Do not reference `docs/decisions/0010-...` or any other kms-repo-specific
path from inside `roadmap`'s body — `roadmap` ships to other projects
that won't have that file. The paragraph above is self-contained by
design; keep it that way.

**Done when**: the paragraph is present verbatim, and a grep for
`docs/decisions/0010` in `plugins/kms/skills/roadmap/SKILL.md` returns
nothing.

### 3. [pending] Update `bootstrap`: track field, stub format, generalized wording

All edits are to `plugins/kms/skills/bootstrap/SKILL.md`.

**3a.** In the "File formats" section, change:

```
Decision — optionally add `governed-facts: [<fact-id>, ...]` and `fitness-functions: [<check description>, ...]`.
```

to:

```
Decision — add `track: product | process` (required: product = what the
project is for and who it serves; process = how it's built, organized,
or shipped); optionally `governed-facts: [<fact-id>, ...]` and
`fitness-functions: [<check description>, ...]`.
```

**3b.** In step 1 ("Intent extraction from history"), change:

```
- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `status: draft`.
```

to:

```
- Cluster findings by domain; write one decision stub per cluster: id, title, one-line motivation, `track: product | process`, `status: draft`.
```

**3c.** In step 1's opening sentence, change "architecture notes" to
"planning notes" (keep `git log` — the git+Markdown substrate is
unchanged per `docs/decisions/0011-...`):

```
Scan git log and existing docs (README, planning notes, guardrail/skill files) for decision language: ...
```

**3d.** In step 3 ("Doc manifest bootstrap"), change:

```
mapping the doc's sections to the code/config/decisions they describe,
```

to:

```
mapping the doc's sections to the content and decisions they describe,
```

**3e.** In step 5 ("Fitness function inventory"), change:

```
Scan CI/build config for checks already enforcing a rule and record them.
```

to:

```
Scan any existing automated or procedural checks (CI/build config, review checklists, approval gates) for rules already enforced, and record them.
```

**3f.** In step 6's table ("Skill gap detection"), append three rows
after the existing five (keep all five as-is):

```
| Recurring manual process, no written procedure | Process/procedure documentation |
| External compliance, regulatory, or ethical requirement | Compliance/review skill |
| Repeated reviewer or stakeholder feedback pattern | Review/quality skill |
```

**3g.** In step 6's closing paragraph, change:

```
Domains governing irreversible decisions (published APIs, binary ABI, irreversible schema changes) are the highest priority to formalize first.
```

to:

```
Domains governing irreversible decisions (published APIs, binary ABI, irreversible schema changes — or, outside software, legal/compliance commitments and claims made public) are the highest priority to formalize first.
```

**Done when**: all seven edits (3a–3g) are applied verbatim, the file's
frontmatter is still valid YAML, and a grep for "architecture notes" or
"code/config" in `plugins/kms/skills/bootstrap/SKILL.md` returns nothing.

### 4. [pending] Update `steward`: track field and stub format

Both edits are to `plugins/kms/skills/steward/SKILL.md`.

**4a.** In "## Artifact formats", change:

```
- **Decision** — optionally `governed-facts: [...]`, `fitness-functions: [...]`.
```

to:

```
- **Decision** — add `track: product | process` (required: product =
  what the project is for and who it serves; process = how it's built,
  organized, or shipped); optionally `governed-facts: [...]`,
  `fitness-functions: [...]`.
```

**4b.** In "## Checks, one pass per invocation", check 1, change:

```
1. **New decision?** Draft a stub: next id, title, one-line motivation, `status: draft`. Don't finalize without the owning domain's sign-off.
```

to:

```
1. **New decision?** Draft a stub: next id, title, one-line motivation, `track: product | process`, `status: draft`. Don't finalize without the owning domain's sign-off.
```

**Done when**: both edits are applied verbatim and the file's
frontmatter is still valid YAML.

## Explicitly out of scope for this plan

- Any change to `clarify` — it already has zero software-specific
  language (confirmed by grep across all four bodies during the
  interview) and doesn't handle decisions/facts at all, so there's
  nothing for either decision to change in it.
- Any change to `attribute` or `changelog` — explicitly kept git-scoped
  per `docs/decisions/0011-...`.
- Any change to the storage substrate (git, Markdown,
  `docs/{facts,decisions,guardrails,skills}/`) — explicitly unchanged
  per the same decision.
- A `track` field on facts, guardrails, or skill prescriptions —
  `docs/decisions/0010-...` scopes this to decisions only.
- Updating `README.md`/`AGENTS.md` to describe the track field or the
  broadened domain scope — not requested, and README's current wording
  ("any git-based project ... not just code") already doesn't
  contradict either decision.
