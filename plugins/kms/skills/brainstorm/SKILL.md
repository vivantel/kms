---
name: brainstorm
description: Generative ideation partner that explores multiple approaches to a problem or feature without writing anything or consulting the knowledge base. Use when the user wants options generated before any decision exists, e.g. "brainstorm approaches for implementing websocket reconnection logic", "what are some ways to solve X".
---

Generate distinct approaches to a problem, then synthesize a recommendation — without writing to disk or querying `docs/{facts,decisions,guardrails,skills}/`.

## Constraints

- **Never query the knowledge base.** Even if one exists, ideation stays unanchored — filtering options through existing decisions before generating them defeats the point. `refactor-plan`/`roadmap` are where existing decisions and guardrails belong.
- **Writes nothing to disk.** Output stays in chat; capturing an approach as durable knowledge afterward is `roadmap`'s job, run separately.
- **Stay generative before synthesis.** Don't rank, filter, or dismiss while producing the list — pros/cons/risks are recorded neutrally. Evaluation is a distinct, later phase.

## Producing approaches

1. If the problem is ambiguous enough to send ideation in very different directions, ask one clarifying question first; otherwise proceed directly.
2. Generate 5-7 distinct approaches — differing in mechanism or tradeoff shape, not superficial variation (two caching strategies with different TTLs count as one approach, not two).
3. For each, state:
   - **What it is** — one or two sentences.
   - **Pros** — what it's genuinely good at.
   - **Cons** — what it costs or gives up.
   - **Risks** — what could go wrong, or is uncertain.
   - **Effort** — S/M/L, relative to the other approaches, not absolute.
4. If fewer than 5 genuinely distinct approaches exist, say so — don't pad with near-duplicates.

## Synthesis

Switch modes explicitly (a `## Synthesis` heading) and recommend 2-3 directions, one sentence each on why those and not the others — the only point evaluation happens.

## Out of scope

Capturing an approach as a decision or fact (`roadmap`), checking one against existing guardrails (`refactor-plan`), and interviewing about a plan the user already has in mind (`clarify`).
