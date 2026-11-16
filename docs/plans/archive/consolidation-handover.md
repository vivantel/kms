---
title: Consolidation handover (plan step I1)
date: 2026-11-16
---

# Handover

## Branches (nothing pushed, tagged, released; master untouched)
- kms: `feat/kms-core-consolidation` @ 067ee6c (per-step work done on worktree branch `wt/consolidation`, fast-forward merged into it after each step).
- go-getter: `feat/adopt-kms-core` @ 168ae02.

## Results at the tips
- kms: `python3 -m unittest discover -s evals/lint -t .` OK (58 tests incl. conformance); `lint_check.py --root .` clean; all manifests valid JSON, versions unchanged (0.15.0).
- go-getter: `npm test` 1439 pass, 0 fail; check:generated, docs-consistency, indexes, versions, core-pin ok; core checker on its own docs/ has no findings (only advisory warnings: unpinned guardrails, skipped numbers).

## Owner decisions pending (all `status: draft`; same list as the plan)
kms 0069-0082: accept = `status: active` + `accepted-by`; revert hints are in the plan's table. go-getter 0210-0214: revert = the D0 commit. Accepting 0070/0211 means archive kms 0067 and go-getter 0066 with index rows.

## Blocked / not done
- D3: `npm run eval`, `eval:bypass`, `e2e:lifecycle` call paid providers and read ~/.claude credentials; run them yourself before merging go-getter.
- `decide` eval and lint-matrix relabel: need kilo CLI and a provider key.
- E3 residual: clarify to discover and changelog to release folds not done (no `release` skill exists; all five kept, skill count unchanged).
- `lint`, `conform`, `decide` skills are model-run and were not executed; only the structural checker ran.

## Code-review fixes (after the handover)
Nine findings fixed in six commits on the kms branch: checker crashes (invalid date, absolute `--docs`, scalar `fitness-functions`), check 18 for open questions, plan/tag/prose-ref regexes, `migrate.py` (compute before write, CRLF, registry index rows, None and broken YAML), the check-3 matrix mutation, the CI unit job and `npm run eval`, the `decide` sidecar, `uninstall` category 4 and `bootstrap` step 8. Unit tests cover each (71 pass). The go-getter pin must be refreshed to the new kms tip before release.

**Design call left for you (not a bug fix):** decisions 0073/0077 make pins ignore lifecycle fields, so superseding and archiving a pinned source with a plain `status`/`superseded-by` flip no longer fails the checker (master: check 13; here: a stderr warning, exit 0; `--strict` exits 1). Options: count the advisory in the exit code, or make check 13 fire again when a pinned source is retired. Decide when you accept 0073 and 0077.

## Release sequence
1. Review and accept the drafts; run the blocked evals.
2. kms: bump three manifests in lockstep, rename `[Unreleased]`, set schema-version to `1.0.0`, tag `kms-schema-1.0.0` (notes: `docs/plans/release-notes-next.md`).
3. go-getter: `go-getter core update kms-schema-1.0.0 --from <kms checkout>`, then release (changelog entry exists).
4. One minor release later, run `docs/plans/kms-remove-deprecated-skills.md`.
