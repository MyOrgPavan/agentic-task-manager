---
type: Workflow
title: Agent Evaluate Workflow
description: Evaluates CI failures, identifies the failed PR, and escalates with a needs-human label.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/workflows/agent-ci-evaluate.yml
tags: [workflow, evaluate, ci, failure-analysis]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent Evaluate Workflow

## Trigger

- `workflow_run: [completed]` — Runs when `CI` workflow completes with failure

## Jobs

### evaluate-failures
1. Identify the failed PR from the CI workflow branch
2. Parse ticket and scope from branch name
3. Fetch CI failure logs via GitHub API
4. Read CI failure details using `scripts/fetch_failures.py`
5. Add `needs-human` label to the PR for escalation

## Self-Correction Loop

```
CI failure → Agent Evaluate → needs-human label → Human reviews
                                                      │
                          ┌───────────────────────────┘
                          │
                    Max 3 retries → escalation issue
```

## See Also

- [/workflows/ci](/workflows/ci.md)
- [/workflows/agent-execute](/workflows/agent-execute.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/infrastructure/scripts](/infrastructure/scripts.md)
