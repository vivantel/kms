#!/usr/bin/env bash
# Commits the base tree, then stages a diff that changes the port a fact `source`s and
# violates one guardrail (DEBUG = True).
set -eu
git init -q --initial-branch=main
git config user.email "eval-fixture@example.invalid"
git config user.name "kms eval fixture"
git add -A
git commit -q -m "chore: base"
sed -i 's/PORT = 8080/PORT = 9090/; s/DEBUG = False/DEBUG = True/' src/server.py
git add src/server.py
