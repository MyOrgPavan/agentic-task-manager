#!/usr/bin/env bash
# A-01, A-02, A-03, A-04
# Agent wrapper: invokes opencode with proper context from environment
# Usage: agent-wrapper.sh <phase> <scope> <ticket_id> <command>

set -euo pipefail

PHASE="${1:?phase required (plan/execute/evaluate)}"
SCOPE="${2:?scope required (frontend/backend/db)}"
TICKET="${3:?ticket_id required}"
COMMAND="${4:?command required}"
MAX_RETRIES="${MAX_RETRIES:-3}"
RETRY_DELAY="${RETRY_DELAY:-10}"

echo "[agent-wrapper] Phase=$PHASE Scope=$SCOPE Ticket=$TICKET"

# Read agent prompt template
AGENT_PROMPT=".github/agents/${SCOPE}.agent.md"
if [ -f "$AGENT_PROMPT" ]; then
  PROMPT=$(cat "$AGENT_PROMPT")
else
  PROMPT="role: generic coding agent"
fi

# Read memory context
MEMORY=".github/AGENTS_MEMORY.md"
MEMORY_CTX=""
if [ -f "$MEMORY" ]; then
  MEMORY_CTX=$(python3 -c "
import re
with open('$MEMORY') as f:
    content = f.read()
# Extract sections relevant to this scope
sections = re.findall(r'## (.*?)\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
for title, body in sections:
    if '$SCOPE' in title.lower() or 'project' in title.lower() or 'architecture' in title.lower():
        print(f'## {title}\n{body}')
")
fi

# Build task description
TASK="Phase: $PHASE
Scope: $SCOPE
Issue: #$TICKET
Command: $COMMAND

$PROMPT

## Repository Context
$MEMORY_CTX
"

# Execute opencode
export OPENCODE_GITHUB_TOKEN="${GITHUB_TOKEN:-}"
opencode --no-ask-user "$TASK"
