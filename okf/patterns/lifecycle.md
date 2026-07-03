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
Issue → [Plan] → Plan PR → (approve) → [Act] → Impl PR → [Process] → Done
                                     ↘ (reject) → Issue closed
```

### 1. Plan (read-only)

Agent studies the codebase and writes `plans/plan-<ticket>.md`. No code is written. Plan is proposed as a PR.

**Agent tools:** read_file, search_files

### 2. Act (execute)

Agent reads the approved plan and implements changes. Runs tests, lints. Opens implementation PR.

**Agent tools:** write_file, run_tests, run_lint, run_typecheck, create_pr

### 3. Process (evaluate)

CI runs on the implementation PR. If CI fails, the Evaluate agent reads logs, identifies the ticket, and adds `needs-human` escalation label.

**Self-correction loop:** Max 3 retries, then human escalation.

## Separation of Concerns

Strict tool isolation prevents agents from writing files during the Plan phase or reading unrestricted during Evaluate. Each phase gates tool access via `phase_restrictions` in the agent config.

## See Also

- [/workflows/agent-plan](/workflows/agent-plan.md)
- [/workflows/agent-execute](/workflows/agent-execute.md)
- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
- [/patterns/scoping](/patterns/scoping.md)
- [/agents/overview](/agents/overview.md)
