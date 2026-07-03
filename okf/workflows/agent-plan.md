---
type: Workflow
title: Agent Plan Workflow
description: Generates a structured implementation plan using opencode, then proposes it as a pull request.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/workflows/agent-plan.yml
tags: [workflow, plan, opencode, github-actions]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent Plan Workflow

## Trigger

- `issue_comment: [created]` — Comment on an issue
- `workflow_dispatch` — Manual with `scope` and `ticket_id` inputs

## Jobs

### generate-plan
1. Checkout code + setup Python
2. Install opencode (`npm install -g opencode-ai`)
3. Fetch issue description via `gh issue view`
4. Run opencode to study the codebase and generate `plans/plan-<ticket>.md`
5. Upload plan as artifact

### propose-plan (needs: generate-plan)
1. Download plan artifact
2. Create branch `agent/<scope>/<ticket>`
3. Commit plan file and push
4. Open a Plan PR with the plan as PR body

## Plan Format

Plans are markdown with sections:
- Scope, Ticket / Issue, Risk Level
- Description, Success Criteria (checklist)
- Files to Modify (specific paths)
- Implementation Steps (numbered)
- Rollback Strategy

## Permissions

- generate-plan: contents read
- propose-plan: contents write, PRs write

## Phase Restriction

Plan phase is **read-only** — opencode can read files and generate the plan but has no write access to the codebase.

## See Also

- [/workflows/agent-execute](/workflows/agent-execute.md)
- [/workflows/agentic-router](/workflows/agentic-router.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/patterns/scoping](/patterns/scoping.md)
