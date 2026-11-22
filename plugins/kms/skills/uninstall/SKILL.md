---
name: uninstall
description: Finds everything bootstrap/capture added to this project and offers to detach or remove it, before you actually uninstall the kms plugin. Use when a team is winding down use of kms, e.g. "we're uninstalling kms, clean up what it added", "remove kms's guardrails from this repo".
---

Run this *before* uninstalling the `kms` plugin — nothing can act automatically afterward, so this is the only window for cleanup. Finds every trace `bootstrap`/`capture` left in this project and offers to detach (keep the content, stop tracking it as kms's) or remove it.

## What to scan for

1. **`kms-seeded: true` files** — anywhere under the knowledge directory, matching this skill's `templates/` (one subdirectory per artifact type; currently just `guardrails/`).
2. **`kms-generated: true` files** — scan for the marker anywhere under the knowledge directory, the same way as category 1; don't hardcode which files carry it, since `bootstrap` may stamp more of them over time.
3. **Registries** — files carrying `kms-registry` (indexes, `tags.md`, the docs manifest), reported as one group; usually also `kms-generated`.
3b. **The `<!-- kms:start -->`/`<!-- kms:end -->` block** in the project's agent-instructions file (`AGENTS.md` or whatever host-specific equivalent it uses), if present (its `kms-dir:` line goes with it). After removals, offer to delete a now-empty knowledge directory or `.vivantel/`.
3c. **CI recipes** — `.git/hooks/pre-commit`, `.githooks/pre-commit` and `.github/workflows/kms-lint.yml`, only when they carry a `kms-generated: true` comment; also `.vivantel/akasha/lint_check.py` if present. Offer to remove (detach: delete the marker comment).
4. **Still-`status: draft` decisions** — a proposal (from `bootstrap` or from `capture`'s own check 1, which drafts stubs the same way) that nobody has acted on yet. Skip a draft that carries `expires-when`: that is an open question the team is keeping. Report these separately from categories 1-3 and note plainly that they carry no `kms-seeded`/`kms-generated` marker — they're identified by status, not by marker.

## Report first, then act

List everything found, grouped by category, before asking about any of it — never surface per-file prompts one at a time with no overview. Then, per finding, ask: **detach** (strip `kms-seeded`/`kms-generated`, or the AGENTS.md markers alone leaving the section text, keeping everything else as the team's own) or **remove** (delete the file — for a seeded guardrail, removal happens only here; if the team wants it gone while keeping kms, add its id to the AGENTS.md block's `kms-declined: [<id>, ...]` line, which `lint` check 12 and `bootstrap` step 8 honour, or delete just the marked block from AGENTS.md, or delete the still-draft decision). Same confirmation for both — propose, wait for an explicit yes, exactly like every other skill in this plugin.

## Never touch

Any decision past `status: draft`, and any draft carrying `expires-when`, and any fact — that's the team's own commitment, regardless of topic, marker or no marker. Any guardrail without a `kms-seeded` marker, or any other file without `kms-generated`, outside of category 4 above — that's project-owned. Custom guardrails the team wrote themselves, even ones that resemble something `kms` seeds.

## Out of scope

`plugins/kms/hooks/hooks.json` — it lives in the plugin's own installed directory, not this project's repo, and the host removes it automatically when the plugin is uninstalled. Actually uninstalling the plugin itself — that's a host command, not this skill's job.
