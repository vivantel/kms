# `onboard` examples

## 1. A project with a healthy knowledge base

**Prompt:** "Onboard me as a frontend developer for this project."

**What happens:** `docs/{facts,decisions,guardrails,skills}/` is read in full. A 5-day plan comes back with frontend-relevant reading each day (e.g. decisions touching UI/API contracts, guardrails on client-side conventions), skills to run (`query` to resolve open questions, `clarify` before a first real decision), and links to the actual artifact paths found — not generic advice.

## 2. Role not given up front

**Prompt:** "Onboard me to this codebase."

**What happens:** The role is asked for first ("backend dev? QA? something else?") before any plan is drafted, since the plan's content depends entirely on it — this isn't guessed.

## 3. An incomplete knowledge base

**Prompt:** "Onboard me as a QA engineer."

**What happens:** The scan finds `docs/decisions/` populated but `docs/facts/` empty. The plan still gets produced, but opens with an explicit warning that no facts exist yet, so the plan reflects only what's been decided, not what's currently true — and suggests running `bootstrap` if that gap should be closed first.
