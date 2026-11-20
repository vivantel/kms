# `lint` examples

## 1. A full-repo health check

**Prompt:** "Lint the knowledge base."

**What happens:** The deterministic checker runs first and its lines are reported as findings; then every fact, decision, guardrail, and procedure is scanned, not just recently changed ones. Findings are grouped by check — e.g. a `governed-by` pointing at a decision id that no longer exists (dangling reference), a fact whose `source` path no longer exists (stale or unverified fact, check 25). Nothing is fixed automatically; each finding is proposed with a fix, awaiting confirmation.

## 2. Rot that predates any one session

**Prompt:** "Check the whole docs/ tree for problems."

**What happens:** A decision with an `expires` date that passed months ago, which no session has touched since (so `capture` never had a reason to look at it), is flagged as expired and needing re-evaluation — exactly the gap a session-scoped check can't close on its own.

## 3. Structural gaps `lint` won't judge

**Prompt:** "Lint the knowledge base and tell me if decision 0012's reasoning still holds up."

**What happens:** Structural findings (numbering collisions, orphaned facts) and judgment findings (redundant guardrails) are reported as usual, but whether 0012's rationale is still convincing is explicitly out of scope — that's a `decide` interview, not a mechanical scan, not a mechanical scan.
