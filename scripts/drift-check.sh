#!/usr/bin/env bash
# E-06
# Drift detection script - compares PR changes against plan success criteria
set -euo pipefail

PR_NUMBER="${1:-}"
if [ -z "$PR_NUMBER" ]; then
    echo "Usage: $0 <pr-number>"
    exit 1
fi

DRIFT_REPORT="drift-report.json"

echo "Checking for drift in PR #$PR_NUMBER..."

PR_BODY=$(gh pr view "$PR_NUMBER" --json body --jq '.body' 2>/dev/null || echo "")
PLAN_FILES=$(echo "$PR_BODY" | grep -oP '(?<=## Files to Modify\n).*' || echo "")
CHANGED_FILES=$(gh pr diff "$PR_NUMBER" --name-only 2>/dev/null || echo "")

DRIFT_DETECTED=false

while IFS= read -r file; do
    if [ -n "$file" ] && ! echo "$PLAN_FILES" | grep -q "$file"; then
        echo "DRIFT: File '$file' was changed but not in plan."
        DRIFT_DETECTED=true
    fi
done <<< "$CHANGED_FILES"

cat > "$DRIFT_REPORT" <<EOF
{
    "pr_number": $PR_NUMBER,
    "drift_detected": $DRIFT_DETECTED,
    "plan_files": "$(echo "$PLAN_FILES" | tr '\n' ' ')",
    "changed_files": "$(echo "$CHANGED_FILES" | tr '\n' ' ')"
}
EOF

if [ "$DRIFT_DETECTED" = true ]; then
    echo "Drift detected! See $DRIFT_REPORT"
    exit 1
else
    echo "No drift detected."
fi
