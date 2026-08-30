---
id: scoping-shipped-vs-repo-rules
title: Deciding whether a rule belongs in a shipped skill, kms's own contributor docs, or both
status: active
date: 2026-08-30
tags: [kms, knowledge-management, procedural]
---

## Procedure

Before writing a new rule/principle anywhere in this repo, sort it into one of three homes:

1. **Generic knowledge-base rule** — applies to any project's own `docs/{facts,decisions,guardrails,skills}/`, `kms`'s own dogfooded copy included. Belongs in a shipped skill (`lint`/`capture`/`roadmap`/`bootstrap`), restated **inline, self-contained** — never as a reference to a specific file, since a shipped check runs against an arbitrary adopting project that won't have that file. `docs/decisions/0026-token-economy-guardrail.md` is the worked example.
2. **`kms`'s own packaging-layer rule** — concerns `plugins/<plugin-name>/skills/*/SKILL.md`, its `examples.md`, `agents/*.yaml` sidecars, or manifest sync (Claude Code/Codex packaging, not a knowledge-base convention). Belongs only in `AGENTS.md`/`CONTRIBUTING.md`, never referenced from inside a shipped skill's checks. `docs/decisions/0018-per-skill-examples-convention.md` drew this line first.
3. **Both** — a generic rule that also specifically constrains `kms`'s own `SKILL.md` bodies (e.g. token economy). Needs a self-contained version in the shipped skill (home 1) *and* a separate mention in `AGENTS.md`/`CONTRIBUTING.md` for the packaging-layer case (home 2) — one rule, two write-ups, since the two audiences never load the same file.

**Tell-tale bug**: a shipped `SKILL.md` naming a specific file under this repo's own `docs/` tree to justify its own check logic — not just illustrating a citation *format*, like `attribute`'s `Refs:` example — that file won't exist in an adopting project. Grep before merging: `grep -nE "docs/(facts|decisions|guardrails|skills)/[A-Za-z0-9_-]+\.md" plugins/kms/skills/*/SKILL.md`, then judge each hit — a path pattern any project could produce for itself (e.g. `docs/skills/product-track-roles.md`, which `bootstrap` creates *in the target project*) is fine; a hardcoded reference to one of `kms`'s own files isn't.
