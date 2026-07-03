---
type: Workflow
title: Agent Execute Workflow
description: Reads an approved plan and runs opencode to implement the changes, then opens an implementation PR.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/workflows/agent-execute.yml
tags: [workflow, execute, opencode, github-actions]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent Execute Workflow

## Trigger

- `pull_request: [opened, synchronize, labeled]` — When a plan PR gets the `plan-approved` label
- `workflow_dispatch` — Manual with `pr_number` input

## Jobs

### check-plan-approved
1. Parse PR body to extract `scope` and `ticket` from plan markdown
2. Check for `plan-approved` label

### execute (needs: check-plan-approved, if: approved)
1. Checkout the plan PR branch
2. Setup Python and install dependencies
3. Install opencode (`npm install -g opencode-ai`)
4. **Implement changes** — Run opencode to read the plan file and make code modifications
5. Run `create_impl_pr.py` — Create branch `impl/<scope>/<ticket>`, commit, push
6. Run tests (`pytest`)
7. Open implementation PR via `gh pr create`

### evaluate (needs: execute, if: always)
Record execution conclusion

## Scope Parsing

Scope is extracted from the PR body's `## Scope` section and normalized to lowercase.

## See Also

- [/workflows/agent-plan](/workflows/agent-plan.md)
- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/infrastructure/scripts](/infrastructure/scripts.md)
