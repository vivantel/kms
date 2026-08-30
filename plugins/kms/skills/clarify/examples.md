# `clarify` examples

## 1. Stress-testing a plan before acting on it

**Prompt:** "Clarify this with me: I want to switch our CI from GitHub Actions to CircleCI."

**What happens:** One question at a time — why now, what's driving the switch, what happens to existing workflow files, what's the rollback if it goes badly — each with a recommended answer where there's a real tradeoff. Nothing is executed or communicated externally; the session ends only once shared understanding is reached.

## 2. A decision with discrete options

**Prompt:** "Grill me on how we should version this API."

**What happens:** A genuine multi-option decision (e.g. URL versioning vs. header versioning vs. no versioning yet) is presented with each option's tradeoff stated and one marked "(Recommended)", capped at 4 including a free-text catch-all — never more options bolted on, never a second "something else" slot.

## 3. A numeric decision

**Prompt:** "Interview me about our data retention policy."

**What happens:** A question like "how many days of logs should we retain?" is asked openly with an optional default, not turned into a numbered list of options — plain numbers as answers would collide with plain-numbered labels.
