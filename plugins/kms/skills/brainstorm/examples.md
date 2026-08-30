# `brainstorm` examples

## 1. A concrete technical problem

**Prompt:** "Brainstorm approaches for implementing websocket reconnection logic."

**What happens:** No knowledge-base lookup. 5-7 distinct approaches follow — e.g. fixed-interval retry, exponential backoff with jitter, a heartbeat-driven reconnect, a server-push resume-token scheme, a client-side circuit breaker — each with pros/cons/risks/effort (S/M/L). A `## Synthesis` section closes it out, recommending 2-3 of those directions with one sentence each on why.

## 2. A vague feature idea

**Prompt:** "Brainstorm ways to let users share a saved report with a teammate."

**What happens:** The problem is broad enough (sharing via link? via account invite? read-only vs. editable? expiring vs. permanent?) that one clarifying question is asked first — e.g. "should shared access require the teammate to have an account, or is a public link acceptable?" — before generating the 5-7 approaches, since the answer would send ideation in materially different directions.

## 3. Asking it to also decide

**Prompt:** "Brainstorm caching strategies for this endpoint and just tell me which one to use."

**What happens:** The full approach list and synthesis are still produced — brainstorm doesn't skip straight to one recommendation, since narrowing before generating defeats the point. The synthesis section is where the "which one" answer lives, with reasoning; if the user wants that recommendation captured as an actual decision record afterward, they're pointed at `roadmap` to do that separately.
