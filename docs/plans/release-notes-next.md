# Release notes, next kms release (paste source)

Schema version `1.0.0` stays `1.0.0-draft` in the checker until the owner accepts decisions 0069-0082 and tags `kms-schema-1.0.0`. Then bump the three manifests in lockstep (`docs/guardrails/plugin-manifest-version-sync.md`), rename `[Unreleased]` in `CHANGELOG.md` to the version and date, and paste:

### Changed

- The artifact model is now schema `1.0.0` (first line of `plugins/kms/shared/artifact-model.md`), split into schema and `admission.md`; facts carry no outgoing edges, guardrail derivation edges are honest (optional `grounded-in`, optional `enforced-by`), lifecycle words are defined, registries are found by marker, skipped numbers are advisory. Decisions 0071 to 0078 (drafts until accepted).
- The decision `track` field and the product/process role lists are gone (0079). Run `python3 plugins/kms/shared/migrate.py --docs docs` once: it is idempotent and removes `track:` lines.
- The checker gained structural checks and optional pins; checks 14 and 15 are retired (numbers stay unused). `lint_check.py --version` prints the schema version.

### Added

- `docs/skills/core-contract.md` and conformance fixtures under `evals/lint/conformance/`: the schema, checker and fixtures are a versioned core other tools can pin (0080). go-getter vendors it by pin.
- `decide` skill: interview to admissible records only, no plan file (0081).

### Deprecated

- `roadmap` (use `decide`), `brainstorm`, `clarify`, `refactor-plan`, `changelog`: moved to go-getter, still working, removed in 0.19 (0081). Upgrade: switch `roadmap` users to `decide`; keep using the others until removal or install go-getter.

### Notes for the owner

- Not done here: version bumps, tag `kms-schema-1.0.0`, `decide` eval run, lint-matrix relabel (need kilo and a provider key).
