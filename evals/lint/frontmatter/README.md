# Frontmatter parse fixtures

What a reader must make of the block between the first `---` line and the next. Each `cases/<name>.md` has a `<name>.expected.json` with
`data` (the parsed mapping, dates as ISO strings, or `null`) and `error` (`null`, or the start of the checker's message: `no frontmatter`,
`unparseable frontmatter`, `frontmatter is not a mapping`, `unterminated frontmatter`).

`test_frontmatter.py` runs the checker's own `split_frontmatter` over every case. A vendored checker or another reader (go-getter's JS
reader) is held to the same cases: `CHECKER=path/to/lint_check.py python3 -m unittest discover evals/lint/frontmatter`, or an equivalent
runner that prints the same pairs.

`undecided/` holds cases where the readers differ and the contract has not chosen. They are not run. Today: `yaml-1-1-words` (PyYAML reads
`no` and `yes` as booleans; a subset reader keeps them strings). Decide in the schema (`artifact-model.md`), then move the case to `cases/`.
