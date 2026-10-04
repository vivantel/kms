---
name: lint
description: Full-repo validation pass over a project's fact/decision/guardrail/skill knowledge system — outputs violations as JSON
tools:
  read: true
  write: true
  edit: true
  grep: true
  glob: true
  bash: true
model: opencode/nemotron-3-ultra-free
# Fallback models (used if primary returns 503) — must stay on free tiers (0015, improvement-harness-free-models-only):
# model: openrouter/~meta-llama/llama-3-70b:free
# model: openrouter/~google/gemini-flash:free
---

# Lint Agent

Automated lint checks for KMS knowledge artifacts. Outputs violations as JSON for the improvement harness.

## Input (via prompt)

```json
{
  "scope": "all|file",
  "target": "path/to/file.md"  // only when scope=file
}
```

## Workflow

Execute these steps using your available tools (bash).

### 1. Parse Input

Read the prompt as JSON to determine scope and target.

### 2. Run Lint Checks via Python Script

Use the `bash` tool to run the lint check script:

```bash
cd "${repo_root}" && python3 plugins/kms/hooks/lint_check.py --scope ${scope} ${target:+--target "${target}"}
```

The script outputs JSON to stdout with violations and summary.

### 3. Output Result

The script's JSON output is the agent's output. It includes:
- `violations`: Array of violation objects
- `summary`: Files checked, total violations, by type

Exit code: 0 if no violations, 1 if violations found (for CI gate).

## Constraints

- Output ONLY JSON to stdout (no extra text)
- Token economy: be concise
- Free models only

## Lint Verification

After fixing, the improve-lint-fix agent runs this agent on the fixed file to verify.