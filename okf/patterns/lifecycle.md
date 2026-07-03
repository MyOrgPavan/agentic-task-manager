---
type: Pattern
title: Plan-Act-Process Lifecycle
description: Three-stage agentic workflow lifecycle — Plan (read-only), Act (execute), Process (evaluate + correct).
tags: [patterns, lifecycle, plan, act, process]
timestamp: "2026-07-03T09:45:00Z"
---

# Plan-Act-Process Lifecycle

## Stages

```
Issue → [Plan] → Plan PR → (approve) → [Act] → Impl PR → [Process] → Merge → [Deploy] → Running on :8080
                     ↘ (reject) → Issue closed
```

### 1. Plan (read-only)

Agent studies the codebase and writes `plans/plan-<ticket>.md`. No code is written. Plan is proposed as a PR.

**Agent tools:** read_file, search_files

**Trigger:** Issue created with scope label, or intent file pushed

### 2. Act (execute)

Agent reads the approved plan and implements changes. Runs tests, lints. Opens implementation PR.

**Agent tools:** write_file, run_tests, run_lint, run_typecheck, create_pr

**Trigger:** `plan-approved` label added to Plan PR

### 3. Process (evaluate)

CI runs on the implementation PR. If CI fails, the Evaluate agent reads logs, identifies the ticket, and adds `needs-human` escalation label.

**Self-correction loop:** Max 3 retries, then human escalation.

**Trigger:** CI workflow completion (failure)

### 4. Deploy (release)

After the Impl PR is merged to `main`, the code is deployed as a Docker container:

| Step | Environment | Trigger | Port |
|------|-------------|---------|------|
| Staging | `task-manager-staging` | Push to `main` (auto) | 8080 |
| Production | `task-manager-prod` | Manual dispatch + approval | 8080 |

**Staging** deploys automatically on every merge. **Production** requires a human to trigger the workflow and a second human to approve via the GitHub Environment gate.

**Deploy workflow:**
1. Build Docker image from merged code
2. Stop any existing container on port 8080
3. Start new container
4. Health check via `curl http://localhost:8080/`

## Separation of Concerns

Strict tool isolation prevents agents from writing files during the Plan phase or reading unrestricted during Evaluate. Each phase gates tool access via `phase_restrictions` in the agent config.

## See Also

- [/workflows/agent-plan](/workflows/agent-plan.md)
- [/workflows/agent-execute](/workflows/agent-execute.md)
- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
- [/workflows/phases](/workflows/phases.md)
- [/patterns/scoping](/patterns/scoping.md)
- [/agents/overview](/agents/overview.md)
