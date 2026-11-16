# Release notes, next kms release (paste source)

Released as 0.16.0 with schema `1.0.0` (tag `kms-schema-1.0.0`); decisions 0069-0082 accepted 2026-11-16. Paste:

### Changed

- The artifact model is now schema `1.0.0` (first line of `plugins/kms/shared/artifact-model.md`), split into schema and `admission.md`; facts carry no outgoing edges, guardrail derivation edges are honest (optional `grounded-in`, optional `enforced-by`), lifecycle words are defined, registries are found by marker, skipped numbers are advisory. Decisions 0071 to 0078 (drafts until accepted).
- The decision `track` field and the product/process role lists are gone (0079). Run `python3 plugins/kms/shared/migrate.py --docs docs` once: it is idempotent and removes `track:` lines. A bare-string `fitness-functions` entry becomes `{check: ...}` with no `last-verified`; check 18 then asks for the date, and the script prints each one.
- The checker gained structural checks and optional pins; checks 14 and 15 are retired (numbers stay unused). `lint_check.py --version` prints the schema version.

### Added

- `docs/skills/core-contract.md` and conformance fixtures under `evals/lint/conformance/`: the schema, checker and fixtures are a versioned core other tools can pin (0080). go-getter vendors it by pin.
- `decide` skill: interview to admissible records only, no plan file (0081).

### Deprecated

- `roadmap` (use `decide`), `brainstorm`, `clarify`, `refactor-plan`, `changelog`: moved to go-getter, still working, removed in 0.17 (0081). Upgrade: switch `roadmap` users to `decide`; keep using the others until removal or install go-getter.

### Notes for the owner

- Not done here: version bumps, tag `kms-schema-1.0.0`, `decide` eval run, lint-matrix relabel (need kilo and a provider key).
