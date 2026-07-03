---
type: Pattern
title: Phase Gating
description: Per-phase tool restrictions and autonomy levels that limit what agents can do at each stage of the lifecycle.
tags: [patterns, gating, autonomy, tools]
timestamp: "2026-07-03T09:45:00Z"
---

# Phase Gating

## Principle

Agent tools are gated by phase. An agent in Plan phase cannot write files. An agent in Execute phase cannot read CI logs. An Evaluate agent cannot write code.

## Per-Phase Tool Matrix

| Tool | Plan | Execute | Evaluate |
|------|------|---------|----------|
| read_file | ✓ | ✓ | ✗ |
| search_files | ✓ | ✓ | ✗ |
| write_file | ✗ | ✓ | ✗ |
| run_tests | ✗ | ✓ | ✗ |
| run_lint | ✗ | ✓ | ✗ |
| run_typecheck | ✗ | ✓ | ✗ |
| create_pr | ✗ | ✓ | ✗ |
| read_ci_logs | ✗ | ✗ | ✓ |
| read_memory | ✓ | ✓ | ✓ |
| write_memory | ✗ | ✓ | ✓ |
| add_label | ✗ | ✗ | ✓ |

## Implementation

Phase restrictions are configured in each agent's `.github/agents/<scope>.agent.md` file under `phase_restrictions`.

## Gating Workflow

```
                    ┌──────────────┐
                    │  Issue/Intent │
                    └──────┬───────┘
                           ▼
                    ┌──────────────┐
                    │  Router      │  (reads scope label)
                    └──────┬───────┘
                           ▼
  ┌──────────────────────────────────────────┐
  │  Plan Phase (read-only tools)            │
  │  → Generate plan → Plan PR               │
  └──────────────────┬───────────────────────┘
                     │ plan-approved label
                     ▼
  ┌──────────────────────────────────────────┐
  │  Execute Phase (write tools)             │
  │  → Implement → Test → Impl PR            │
  └──────────────────┬───────────────────────┘
                     │ CI pass/fail
                     ▼
  ┌──────────────────────────────────────────┐
  │  Evaluate Phase (CI inspection tools)    │
  │  → Read logs → Escalate or Done          │
  └──────────────────────────────────────────┘
```

## See Also

- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/patterns/scoping](/patterns/scoping.md)
- [/workflows/phases](/workflows/phases.md)
- [/governance/risk-classification](/governance/risk-classification.md)
- [/agents/overview](/agents/overview.md)
