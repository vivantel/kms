# `query` examples

## 1. A settled question

**Prompt:** "What did we decide about how skills are named?"

**What happens:** `docs/{facts,decisions,guardrails,skills}/` is searched by keyword/tag. The answer is drawn only from what's found — e.g. citing `docs/decisions/0001-kms-skill-names.md` — and ends with `Refs:` trailers pointing at every artifact used, matching `attribute`'s citation format.

## 2. A superseded decision

**Prompt:** "Why does this guardrail exist?"

**What happens:** If the guardrail's governing decision has since been superseded by a later one, both are cited — not just the original — so the answer reflects the current state, not stale history.

## 3. Nothing found

**Prompt:** "What did we decide about rate limiting?"

**What happens:** No matching artifact exists. The answer says so plainly rather than guessing or synthesizing a plausible-sounding rule the knowledge base never actually settled.
