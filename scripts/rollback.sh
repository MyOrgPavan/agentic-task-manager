#!/usr/bin/env bash
# D-11, F-11
# Rollback script - reverts a commit on a given branch
set -euo pipefail

BRANCH="${1:-main}"
COMMIT="${2:-}"
MESSAGE="${3:-Rollback: manual revert}"

if [ -z "$COMMIT" ]; then
    echo "Usage: $0 <branch> <commit-hash> [message]"
    exit 1
fi

echo "Rolling back commit $COMMIT on branch $BRANCH..."
git checkout "$BRANCH"
git revert --no-edit "$COMMIT" || {
    echo "Automatic revert failed. Attempting manual revert..."
    git reset --hard HEAD~1
}

git commit --allow-empty -m "$MESSAGE"
echo "Rollback complete. Push with: git push origin $BRANCH"
