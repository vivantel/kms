# `capture` examples

## 1. Routine post-session check

**Prompt:** "Run the knowledge check." (after a session that added a new retry timeout and touched an existing guardrail's grounding fact)

**What happens:** A new decision stub is drafted for the retry-timeout choice; the fact it changed gets its `last-verified` bumped; any doc-drift on watched paths is proposed as a specific update. Whether the touched guardrail itself needs re-deriving is `lint`'s job now, not checked here.

## 2. A contradiction blocks the session

**Prompt:** "Did anything here need capturing as a decision or fact?" (session added code that violates an existing guardrail)

**What happens:** The contradiction is surfaced and the session isn't closed out as clean — either the guardrail is reconciled, the new behavior is rejected, or the conflict is explicitly deferred with a written note. Never silently left open.

## 3. A decision supersedes an older one

**Prompt:** "Capture what we just decided about the payment provider."

**What happens:** A decision stub is drafted (`status: draft`). Because it replaces the earlier provider decision, that decision's `status` becomes `superseded` with `superseded-by` pointing at the new one in the same pass, so two `active` decisions never sit on one topic.
