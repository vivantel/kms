---
name: quickstart
description: Sets up a project's knowledge system and captures one real decision live, in the same sitting, so the value is felt immediately rather than left for later. Use when a user is trying this plugin for the first time, e.g. "get me started with this", "set this up and show me how it works".
---

Run `bootstrap`'s setup, then immediately capture one real, current decision as a full artifact — first value in one sitting, not a cold "now go use `roadmap` sometime."

## Step 1: setup

If `docs/{facts,decisions,guardrails,skills}/` doesn't exist or is clearly incomplete, run `bootstrap`. If it already exists and looks populated, say so and skip straight to step 2 — don't redo setup that's already done.

## Step 2: find one real decision

Ask what decision or plan is currently live for the user — something they're actually facing, not a hypothetical. If they don't have one in mind, look for a candidate: an open question in recent git history, a TODO, or a choice `bootstrap`'s own decision-stub extraction flagged as ambiguous.

## Step 3: capture it

Run `roadmap`'s interview and artifact-writing process on that one decision, in full — same interview mechanics, same before-writing-anything file-list checkpoint, same classification-at-the-end discipline. Don't shortcut it; the point is a real, complete artifact, not a demo.

## Step 4: show what just happened

Close by pointing at the artifact(s) written and naming 2-3 next skills relevant to what just happened (typically `query` to retrieve what was just captured, `capture` for next session, `onboard` if a teammate needs ramping up).

## Out of scope

Everything `bootstrap` and `roadmap` already cover in depth — this skill only sequences them for a first-time user. Don't duplicate their instructions; run them.
