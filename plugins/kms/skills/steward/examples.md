# `steward` examples

## 1. Routine post-session check

**Prompt:** "Run the knowledge check." (after a session that added a new retry timeout and touched an existing guardrail)

**What happens:** The eleven checks run: a new decision stub is drafted for the retry-timeout choice; the fact it changed gets its `last-verified` bumped; the guardrail it touched is re-derived if its grounding fact or governing decision moved; any doc-drift on watched paths is proposed as a specific update.

## 2. A contradiction blocks the session

**Prompt:** "Did anything here need capturing as a decision or fact?" (session added code that violates an existing guardrail)

**What happens:** The contradiction is surfaced and the session is not closed out as clean — either the guardrail is reconciled, the new behavior is rejected, or the conflict is explicitly deferred with a written note. It's never silently left open.

## 3. An unenforced guardrail found

**Prompt:** "Run steward."

**What happens:** A guardrail is found describing behavior a shipped skill should perform, but that skill's own body doesn't actually say it. The skill is updated in the same pass — not deferred — since a guardrail alone in `docs/guardrails/` never reaches anyone who only installs the skill.
