# `bootstrap` examples

## 1. A project with no knowledge system yet

**Prompt:** "Bootstrap the knowledge system here."

**What happens:** `docs/{facts,decisions,guardrails,skills}/` is created. Git log and existing docs are scanned for decision language, producing decision stubs (id, title, one-line motivation, `status: draft`) rather than fully authored records. Fact stubs are drafted from tables/config defaults found in the repo. A doc manifest and a fitness-function inventory are started. Skill-gap domains are proposed from signals in the repo (CI config, test suite, roadmap docs, etc.).

## 2. A gap-fill pass on an incomplete system

**Prompt:** "Set up facts/decisions/guardrails for this repo — we already have a decisions/ folder but nothing else."

**What happens:** The existing `decisions/` format is detected and extended, not replaced. `facts/`, `guardrails/`, and `skills/` are created to match. Every existing guardrail (if any) is audited for missing `governed-by`/`grounded-in`/`derivation-note`, with the most likely sources proposed rather than left blank.

## 3. Compiling the tag vocabulary

**Prompt:** "Bootstrap this project's knowledge base and set up the tag list too."

**What happens:** Alongside the usual setup, every tag already used across the project's artifacts is compiled into `docs/skills/tags.md` — one `tag — meaning` per line, tags carried by over half of active decisions marked `(umbrella)` — so later artifacts draw from one vocabulary.
