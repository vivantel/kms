# `decide` examples

## 1. Capture a database choice

**Prompt:** "We chose Postgres over MySQL for the orders service. Interview me and save this as knowledge."

**What happens:** One question at a time, each with a recommended answer: why Postgres, what was rejected, whether anything expires it. The environment is searched for existing facts instead of asking. After the interview the skill lists the files it would write (`docs/decisions/0007-orders-use-postgres.md`, plus a fact if a limit was confirmed) and waits for a go-ahead before touching disk.

## 2. A commitment that fails admission

**Prompt:** "Record that we renamed `utils.py` to `helpers.py` last week."

**What happens:** The rename is visible in the diff, so it fails the "not already carried" gate. Nothing is written; the closing summary lists it under "Not recorded" with the failed gate.

## 3. A match already exists

**Prompt:** "Save our decision to cap retries at three."

**What happens:** An existing decision `0004-cap-retry-backoff.md` already covers retries. The skill proposes extending it rather than writing a new file and waits for confirmation.
