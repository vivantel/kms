# `quickstart` examples

## 1. Brand-new project, no knowledge system yet

**Prompt:** "Get me started with this plugin."

**What happens:** `bootstrap` runs first, creating `docs/{facts,decisions,guardrails,skills}/`. Then the user is asked what decision is currently live for them — they mention they're deciding between two auth providers. `roadmap`'s full interview runs on that decision, ending with a real decision record on disk. The session closes by pointing at that file and suggesting `query` to retrieve it later and `steward` for next session.

## 2. Knowledge system already exists

**Prompt:** "Set this up and show me how it works." (repo already has populated `docs/decisions/`)

**What happens:** Setup is skipped — the existing structure is detected and said so plainly — and the session goes straight to finding a live decision to capture.

## 3. No decision comes to mind

**Prompt:** "Get me started, but I don't have anything specific in mind right now."

**What happens:** Recent git history and any TODOs are scanned for a candidate — e.g. an ambiguous choice `bootstrap`'s own extraction step would flag — and offered as a starting point rather than stalling on a decision that doesn't yet exist.
