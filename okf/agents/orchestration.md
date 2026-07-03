---
type: Agent
title: Orchestration Agents
description: Non-coding agents that coordinate the development lifecycle — audit, integrator, merger, evaluate.
tags: [agents, orchestration, audit, integrator, merger, evaluate]
timestamp: "2026-07-03T09:45:00Z"
---

# Orchestration Agents

## Audit Agent

**Trigger:** `workflow_dispatch`

Read-only inspection across all scopes. Reviews PRs for compliance, quality, and adherence to the plan. Produces audit reports.

**Permissions:** `contents: read` only.

## Integrator Agent

**Trigger:** `workflow_run` (after backend or frontend workflow completes)

Fan-in merge coordination. When multiple agents produce changes to the same areas, the integrator merges their work into a cohesive PR.

## Merger Agent

**Trigger:** `workflow_run` (after audit completes)

Consumes audit reports and executes merges. Only merges when audit passes.

## Evaluate Agent

**Trigger:** `workflow_run` (when CI completes with failure)

Reads CI failure logs, identifies the failed PR and ticket, and adds a `needs-human` escalation label. Part of the self-correction loop with max 3 retries.

```
CI failure → Evaluate → needs-human → Human reviews
                                         │
                  Max 3 retries ─────────┘
                          │
                    Escalation issue
```

## See Also

- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
- [/agents/overview](/agents/overview.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
