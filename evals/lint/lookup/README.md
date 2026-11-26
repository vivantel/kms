# Lookup fixtures

How a reference in plan text resolves to an artifact: `(corpus, text) -> artifact ids`. They pin what go-getter's `namedArtifacts` does today
(decision b3-2, starting from today's behaviour); the numbering rule B2 may later move into kms changes them here first.

- `corpus/docs/` is a small artifact tree: live and `archive/` files, a superseded decision, an `INDEX.md` that is no artifact.
- `queries.json` lists `{name, text, ids}`: the ids a reader must return for the text, in order, with the superseded-filter applied.

`test_lookup.py` checks the fixtures against themselves (every expected id is a file in the corpus, names are unique). A reader is held to the
same cases by its own test (go-getter: `compiler/test/lookup-fixtures.test.mjs`). No resolver code lives here.
