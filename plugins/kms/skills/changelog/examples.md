# `changelog` examples

## 1. Generating a release entry since the last tag

**Prompt:** "Generate a changelog for this release."

**What happens:** The most recent tag is found and `git log <tag>..HEAD` is read. Each commit's Conventional Commit type maps to a category (`feat`→Added, `fix`→Fixed, `docs`→Documentation, the rest→Changed), rendered as one bullet per commit using its Why-body, not its raw subject line. The version and date are asked for before anything is written — never inferred.

## 2. No tags yet

**Prompt:** "Update the changelog for this release." (repo has no tags)

**What happens:** Full history (`git log`) is used instead of a tag-bounded range. `CHANGELOG.md` is created with a `# Changelog` heading if it doesn't already exist, and the new section is prepended above any prior entries.

## 3. Asked to auto-version or write "Unreleased"

**Prompt:** "Just add whatever's changed to an Unreleased section."

**What happens:** Declined as stated — this skill never writes to or invents an `[Unreleased]` section and never infers a version number itself; a version and date are asked for first.
