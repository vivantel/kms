# `uninstall` examples

## 1. Full cleanup before uninstalling

**Prompt:** "We're uninstalling kms, clean up what it added."

**What happens:** A report lists everything found: 4 seeded guardrails (`docs/guardrails/token-economy.md` and 3 siblings), 3 generated files (`docs/facts/docs-manifest.md`, `docs/skills/product-track-roles.md`, `docs/skills/process-track-roles.md`), the AGENTS.md `<!-- kms:start -->` block, and 1 still-draft decision stub nobody finalized. For each, the user is asked detach or remove; the draft stub is removed, the guardrails are removed, and the AGENTS.md block is removed — each confirmed individually before anything is written or deleted.

## 2. Keep the guardrails, just remove the kms wiring

**Prompt:** "Remove kms's guardrails from this repo, but I like the token-economy one — keep it."

**What happens:** For `token-economy.md`, detach is chosen — its `kms-seeded`/`kms-template-version` fields are stripped, the file and its `## Guardrail` text stay exactly as they are, now just a normal project guardrail no longer tracked by `kms`. The other three are removed. The AGENTS.md block and generated files are handled the same way as any other finding, asked about individually.

## 3. Nothing to clean up

**Prompt:** "Check what kms left behind before I uninstall it."

**What happens:** No `kms-seeded`/`kms-generated` markers, no AGENTS.md block, no draft stubs found — the report says so plainly, nothing further to do.
