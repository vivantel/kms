---
title: Consolidation handover (plan step I1, after owner review)
date: 2026-11-16
---

# Handover

## State
- kms `feat/kms-core-consolidation`: release commit tagged locally `0.16.0` and `kms-schema-1.0.0` (not pushed). Manifests 0.16.0, schema 1.0.0.
- go-getter `feat/adopt-kms-core`: decisions accepted; pin moves to tag `kms-schema-1.0.0` (see the go-getter changelog). Not pushed, not released, version not bumped.
- Nothing is merged to either `master`.

## Owner decisions taken 2026-11-16
Accepted: kms 0069-0082 (0067 superseded by 0070), go-getter 0210-0214 and plan autonomy (0066 superseded by 0211). Pin retirement: a retired source of a pinned guardrail is a check-1 finding. Skills: all five moved skills stay unchanged in go-getter (folds deferred). Plan autonomy: `plan start --auto` as built, `run` deprecated one release. Release: kms 0.16.0 + tag `kms-schema-1.0.0`.

## Evals (Kilo free gateway, model cohere/north-mini-code:free)
- Pass: `decide` (after rewording to one question per turn), `bootstrap`, `lint`.
- Fail, and fail identically on `master`, so not regressions: `capture` (the model loads the skill and stops), `attribute` (no `Refs:` line), `roadmap` (bundles questions; deprecated skill).
- Not run: lint matrix and admission (need a provider key), go-getter `npm run eval`, `eval:bypass`, `e2e:lifecycle` (paid, read `~/.claude`).

## Open
- Eight archived deprecated facts lack the first body line saying why (model, decision 0073).
- Single-line mutants of `lint_check.py` survive the unit and conformance suites (review item 8); some tests pass for the wrong reason.
- `clarify` into `discover` and `changelog` into `release` folds, deferred.
- Push, open PRs, release go-getter (version bump, tag), then one minor release later `docs/plans/kms-remove-deprecated-skills.md`.
