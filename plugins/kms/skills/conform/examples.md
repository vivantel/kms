# `conform` examples

## 1. A staged change that violates a guardrail

**Prompt:** "Does this diff conform to our guardrails?" (staged change adds a new field to session data, stored in `localStorage`)

**What happens:** The staged diff is read. A guardrail prohibiting client-side storage of session data (for a stated compliance reason) is found relevant and cited, along with the decision behind it. The finding is reported clearly — file, hunk, guardrail violated — with nothing auto-fixed.

## 2. Checking recent PRs, not the working tree

**Prompt:** "Conform check the last 3 PRs."

**What happens:** The target resolves to the combined diff across the last 3 merged PRs, not the staged diff (nothing needs to be staged for this to work). Same conformance check runs against that combined range.

## 3. Nothing relevant found

**Prompt:** "Check this branch against what we've decided." (branch only touches a CSS file)

**What happens:** No decision or guardrail in the knowledge base is relevant to a CSS-only change — the report says so plainly rather than fabricating a concern.
