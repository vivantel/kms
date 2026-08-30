# `refactor-plan` examples

## 1. A vendor swap

**Prompt:** "Plan a refactor of the payment module to use Stripe instead of Braintree."

**What happens:** Phase 1 searches the knowledge base and cites, say, a decision that fixed Braintree as the payment provider and a guardrail about PCI-scope boundaries. Phase 2 maps call sites and config touching the payment module directly (no dependency on `lint` running as a sub-step, though the plan recommends running it before/after). Phase 3 lays out ordered steps with a verification checkpoint and rollback per phase. Phase 4 flags that the Braintree-provider decision and any fact describing the current provider will need updating once this lands.

## 2. A refactor that collides with a guardrail

**Prompt:** "Plan a refactor to cache user session data in localStorage instead of server-side sessions."

**What happens:** Phase 1 turns up a guardrail prohibiting client-side storage of session data for a stated compliance reason. Rather than silently dropping the localStorage step or working around the guardrail, the plan flags the conflict explicitly, cites the guardrail file, and asks the user to confirm before that step is included at all.

## 3. Nothing relevant in the knowledge base

**Prompt:** "Plan a refactor to extract the notification logic into its own module."

**What happens:** Phase 1 finds no decisions or guardrails touching notifications, and says so plainly instead of implying the knowledge base has an opinion it doesn't. Phases 2-4 proceed on dependency-mapping and planning grounds alone.
