---
id: kms-remove-deprecated-skills
title: Remove the five kms skills deprecated in favour of go-getter
status: pending; starts one minor release after the deprecation ships (decision 0081)
date: 2026-11-16
---

# Remove the deprecated kms skills

Steps are `[pending]` until the release that deprecated `roadmap`, `brainstorm`, `clarify`, `refactor-plan` and `changelog` is out and one minor release has passed.

### R1 [pending] Delete the skill directories
**What.** Remove `plugins/kms/skills/{roadmap,brainstorm,clarify,refactor-plan,changelog}/` and their `evals/` cases and CI matrix rows.
**Done when.** `ls plugins/kms/skills` lists only the retained skills and `python3 -m unittest discover -s evals/lint -t .` passes.

### R2 [pending] Update indexes and manifests
**What.** Remove the rows from `README.md`, `plugins/kms/skills/index.json`, `docs/skills/kms-architecture.md` and `AGENTS.md`; fix every cross-reference (`grep -rn "roadmap\|brainstorm\|clarify\|refactor-plan\|changelog" plugins docs README.md`); bump all three manifests in lockstep.
**Done when.** The grep finds only history (changelog, archived plans), `python3 -m json.tool` passes on every manifest and versions agree.

### R3 [pending] Changelog and decision
**What.** Add the `Removed` entry with the go-getter pointer; mark decision 0081's deprecation window closed with an amendment.
**Done when.** `CHANGELOG.md` has the entry for the bumped version and 0081 carries a dated `## Amendment`.
