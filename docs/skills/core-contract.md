---
id: core-contract
title: What a consumer of the knowledge-base core pins
status: active
date: 2026-11-15
tags: [kms, packaging]
---

The core is the part of kms another product can depend on without taking its skills: the schema, the structural checker and the conformance fixtures. A consumer pins a schema version.

## Contract

- **Schema**: `plugins/kms/shared/artifact-model.md` (frontmatter per type, lifecycle words, id format, archive layout, marker forms). Its first line is `schema-version: <semver>`.
- **Checker CLI**: `python3 plugins/kms/shared/lint_check.py --root <dir> [--docs <dir>] [--json] [--strict] [--stale-days N] [--today DATE]`; `--pin FILE`, `--refs ID` and `--version` are the other modes. Exit status 0 when nothing is found, 1 otherwise. `--json` prints an array of `{check, file, message}`; the pair `(check, file)` is the contract, messages are not. Advisories (older shapes, unpinned edges) go to stderr as `warning:` lines and never change the exit status.
- **Check numbers**: stable; 14 and 15 are retired and stay unused.
- **Markers**: `kms-seeded`, `kms-generated`, `kms-registry`, in frontmatter or as a first-line `<!-- ... -->` comment.
- **Migration**: `plugins/kms/shared/migrate.py --docs <dir>` is idempotent and moves a corpus from the previous schema to this one.
- **Conformance fixtures**: `evals/lint/conformance/cases/` (each `<case>/` tree with `<case>.expected.json`); a checker conforms when `evals/lint/conformance/test_conformance.py` passes against it (`CHECKER=<path>`).

Not part of the contract: skill bodies, the eval harness, the wording of templates and `admission.md`.

## Compatibility

A patch release never changes accept or reject on a previously valid corpus. A minor release may add optional fields or new advisory checks. A major release may reject what was valid and ships a migration note. The schema version moves independently of the plugin version; each release note links the two.

## Consuming

Vendor by pin: copy `artifact-model.md`, `lint_check.py`, `migrate.py` and `evals/lint/conformance/` from a named kms release tag (`kms-schema-<version>`) and fail CI when the copy differs from the tag. Install the kms plugin as a prerequisite instead only when a project wants the skills too. Rationale: `docs/decisions/0080-core-is-vendored-by-pin.md`.
