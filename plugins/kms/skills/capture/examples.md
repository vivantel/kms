# `capture` examples

## 1. Routine post-session check

**Prompt:** "Run the knowledge check." (after a session that added a new retry timeout and touched an existing guardrail's grounding fact)

**What happens:** A new decision stub is drafted for the retry-timeout choice; the fact it changed gets its `last-verified` bumped; any doc-drift on watched paths is proposed as a specific update. Whether the touched guardrail itself needs re-deriving is `lint`'s job now, not checked here.

## 2. A contradiction blocks the session

**Prompt:** "Did anything here need capturing as a decision or fact?" (session added code that violates an existing guardrail)

**What happens:** The contradiction is surfaced and the session isn't closed out as clean — either the guardrail is reconciled, the new behavior is rejected, or the conflict is explicitly deferred with a written note. Never silently left open.

## 3. A new decision reveals a role gap

**Prompt:** "Capture what we just decided about the payment provider."

**What happens:** A decision stub is drafted (`track: product`, `status: draft`). If the decision's domain suggests a review role not yet on `docs/skills/product-track-roles.md`, adding it is proposed in the same pass — a role that's simply gone unused for a long time, unrelated to today's session, is left for `lint` to catch instead.
