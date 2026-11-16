# `decide` examples

## 1. Capture a database choice

**Prompt:** "We chose Postgres over MySQL for the orders service. Interview me and save this as knowledge."

**What happens:** One question at a time, each with a recommended answer: why Postgres, what was rejected, whether anything expires it. The environment is searched for existing facts instead of asking. After the interview the skill lists the files it would write (`docs/decisions/0007-orders-use-postgres.md`, plus a fact if a limit was confirmed) and waits for a go-ahead before touching disk.

## 2. A commitment that fails admission

**Prompt:** "Record that we renamed `utils.py` to `helpers.py` last week."

**What happens:** The rename is visible in the diff, so it fails the "not already carried" gate. Nothing is written; the closing summary lists it under "Not recorded" with the failed gate.

## 3. A match already exists

**Prompt:** "Save our decision to cap retries at three."

**What happens:** An existing decision `0004-cap-retry-backoff.md` already covers retries. The change is additive (a cap, not a reversal), so the skill proposes an amendment to it rather than a new file and waits for confirmation.

## 4. A decision is replaced

**Prompt:** "We're switching the rate limiter from the fixed window to a token bucket; interview me and save this."

**What happens:** The active `0001-fixed-window-rate-limit.md` matches. Its sections are frozen, so after the interview the skill proposes a new decision `0002-token-bucket-rate-limit`, setting `0001` to `status: superseded` with `superseded-by: 0002-token-bucket-rate-limit`, moving it to `decisions/archive/` with both `INDEX.md` files updated, and re-deriving each guardrail that cited it. It lists all of that before touching disk and waits for the go-ahead.

## Example: an incident

**Trigger:** "we had an outage when a migration ran twice; turn that into knowledge."

**Interaction:** the skill interviews from the event, one question at a time, to its residue: a fact (the migration runner has no idempotency lock, `source` = the incident ticket), a guardrail (migrations must be idempotent, because the cause generalises) and a procedure for rollback. The incident narrative is listed under "Not recorded: event record, fails admission; stays in the tracker".
