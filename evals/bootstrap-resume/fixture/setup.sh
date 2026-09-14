#!/usr/bin/env bash
# Materializes 16 real commits from this repo's own early history (commit #5 through #20,
# reverse-chronological from the repo's start) as a fresh, non-shallow git history — a full-tree
# snapshot of commit #5 (_seed/, ~240KB) as the first commit, then the following 15 commits
# replayed via `git am` from _patches/*.patch (preserving their real messages/dates/authors).
#
# Two prior approaches were tried and abandoned for this fixture:
# - The full 67-commit history up to tag 0.15.0, via a git bundle: worked for mining (real commit
#   messages/diffs, no INDEX.md-equivalent shortcut — unlike lint's docs/ tree), but the resulting
#   transcript (up to ~220K tokens of diff content alone) blew past the OS's exec argument-size
#   limit when promptfoo spawned the grading subprocess ("Error: spawn E2BIG" — not a grading
#   judgment at all) — workflows 34882535896 and 34885780773 (the second after trimming the final
#   working tree, which wasn't actually the size driver — the transcript itself was).
# - A git-bundle-of-a-shallow-clone for a smaller slice: the shallow boundary's grafted parent
#   isn't portably bundleable without extra `git replace`/`refs/replace` handling that still didn't
#   survive a plain `git clone` of the bundle in isolation.
# This snapshot+patches approach sidesteps both: no shallow-history quirks (git am/format-patch are
# plain diffs), and commits #5-#20 (early in this repo's life) keep the seed snapshot small
# (~240KB) instead of the ~1MB it would be this late in history — real commits, real messages,
# genuinely too much content to shortcut via any index, but sized to stay well under any argument
# limit even accounting for the model's own transcript formatting overhead.
#
# Built in a throwaway subdirectory (_work/) so `git add -A` there never picks up this script's own
# staging materials (_seed/, _patches/, this file) sitting alongside it in the scratch root — those
# are deleted afterward, once the resulting repo is moved up to the scratch root. The final working
# tree is then deleted on disk (uncommitted — a commit removing ~66 files would itself be a large
# diff added to the history bootstrap mines, for no benefit) so bootstrap faces a genuine
# from-scratch extraction, and kilo-resume-runner.sh's own final file listing stays small.
set -eu

SEED_NAME="$(sed -n '1p' _seed_commit_message.txt)"
SEED_EMAIL="$(sed -n '2p' _seed_commit_message.txt)"
SEED_DATE="$(sed -n '3p' _seed_commit_message.txt)"
SEED_MSG="$(tail -n +4 _seed_commit_message.txt)"

mkdir _work
cp -a _seed/. _work/
cd _work
git init -q --initial-branch=main
git add -A
GIT_AUTHOR_NAME="$SEED_NAME" GIT_AUTHOR_EMAIL="$SEED_EMAIL" GIT_AUTHOR_DATE="$SEED_DATE" \
GIT_COMMITTER_NAME="$SEED_NAME" GIT_COMMITTER_EMAIL="$SEED_EMAIL" GIT_COMMITTER_DATE="$SEED_DATE" \
  git commit -q -m "$SEED_MSG"

git config user.email "eval-fixture@example.invalid"
git config user.name "kms eval fixture"
git am -q ../_patches/*.patch

# Deliberately *not* committed: a commit removing ~66 files would itself be a large diff added to
# the very history being mined, costing real token budget for no benefit. Deleting on disk (leaving
# git status dirty) shrinks what kilo-resume-runner.sh's own final file listing sees without
# growing what bootstrap's git-log mining has to read.
find . -mindepth 1 -maxdepth 1 -not -name .git -exec rm -rf {} +
echo "# eval fixture" > README.md
cd ..

shopt -s dotglob
mv _work/* .
rmdir _work
rm -rf _seed _patches _seed_commit_message.txt
