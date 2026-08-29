## Why

<!-- What's the intent behind this change, not just what changed? -->

## What changed

<!-- Brief factual summary. -->

## Refs

<!-- Path(s) to any docs/{facts,decisions,guardrails,skills}/ artifact this PR implements or relates to, if any. -->

## Checklist

- [ ] Any manifest touched is valid JSON (`python3 -m json.tool <file>`)
- [ ] Any `SKILL.md`/`agents/*.yaml` touched has well-formed frontmatter
- [ ] Skill bodies stay agent-neutral (see `docs/guardrails/agent-agnostic-skill-content.md`)
- [ ] Every plugin manifest's `version` was bumped together, if applicable (`docs/guardrails/plugin-manifest-version-sync.md`)
