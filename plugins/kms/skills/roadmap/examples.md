# `roadmap` examples

## 1. Capturing a fresh decision as knowledge

**Prompt:** "Interview me and save this as knowledge: we're moving from REST to gRPC for internal services."

**What happens:** The same interview mechanics as `clarify` run first. Once resolved, every explicit and implicit intent is classified (descriptive/axiomatic/normative/procedural), duplicates are checked against existing artifacts, and — after one explicit go-ahead listing every file to be created — a decision record, any grounding facts, derived guardrails, and a self-sufficient `docs/plans/<slug>.md` implementation plan are written.

## 2. A likely update, not a new artifact

**Prompt:** "Capture this as an ADR: we're extending the retry policy to cover webhook deliveries too."

**What happens:** Before writing anything, existing artifacts are searched by title/topic/frontmatter. Finding a prior retry-policy decision, it's proposed back ("this looks like an update to `docs/decisions/00XX-retry-policy.md` — extend it, or is this a new decision?") rather than silently creating a duplicate or blindly overwriting the original.

## 3. A minor intent that doesn't warrant a full ADR

**Prompt:** "Turn this into a roadmap: we agreed to rename the `worker` service to `job-runner`."

**What happens:** The rename is captured, but since it's easily reversible, unsurprising, and not the result of a real tradeoff, it's saved as a lighter decision fact rather than a full decision record — still written to disk, just not inflated into an ADR it doesn't need.
