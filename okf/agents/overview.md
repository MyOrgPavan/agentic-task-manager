---
type: Agent
title: Agent System Overview
description: Architecture of the multi-agent coding system — domain-specific agents with phase-based tool gating.
tags: [agents, opencode, architecture]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent System Overview

## Architecture

Three **coding agents** (frontend, backend, database) implement changes. Four **orchestration agents** (audit, integrator, merger, evaluate) coordinate the lifecycle.

## Coding Agents

| Agent | Scope | Config |
|-------|-------|--------|
| [/agents/frontend](/agents/frontend.md) | Templates, CSS | `.github/agents/frontend.agent.md` |
| [/agents/backend](/agents/backend.md) | Routes, models, app | `.github/agents/backend.agent.md` |
| [/agents/database](/agents/database.md) | Models, migrations | `.github/agents/db.agent.md` |

## Orchestration Agents

| Agent | Role |
|-------|------|
| audit | Read-only inspection of PRs across all scopes |
| integrator | Fan-in merge coordination from multiple agents |
| merger | Consume audit reports and execute merges |
| evaluate | Read CI failures and re-invoke agents for self-correction |

## Agent Invocation

Agents are invoked via opencode CLI inside GitHub Actions workflow steps:

```bash
opencode run -m opencode/big-pickle \
  --dangerously-skip-permissions --print-logs \
  "Prompt describing the task..."
```

## Phase-Based Tool Gating

Each agent defines `phase_restrictions`:

| Phase | Tools Allowed |
|-------|---------------|
| plan | read_file, search_files |
| execute | write_file, run_tests, run_lint, run_typecheck, create_pr |
| evaluate | read_ci_logs, read_memory, write_memory, add_label |

## See Also

- [/patterns/scoping](/patterns/scoping.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/governance/memory](/governance/memory.md)
- [/governance/risk-classification](/governance/risk-classification.md)
