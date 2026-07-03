---
type: Pattern
title: Agent Scoping
description: Each agent operates within a defined scope path. Cross-scope changes require the integrator agent.
tags: [patterns, scoping, agents, domain]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent Scoping

## Principle

Agents operate within strict path-based scopes. A frontend agent never modifies `backend/routes/`. A backend agent never modifies `backend/templates/`.

## Scope Definitions

| Agent | Scope Pattern |
|-------|--------------|
| Frontend | `backend/templates/**`, `backend/static/**` |
| Backend | `backend/routes/**`, `backend/models.py`, `backend/app.py` |
| Database | `backend/models.py`, `migrations/**` |

## Cross-Scope Changes

When a change spans multiple scopes (e.g., add a database column and update a route and a template), the **integrator** agent coordinates:

1. Plan phase identifies cross-scope dependencies
2. Each domain agent implements its scope
3. Integrator merges branches into a single PR

## Scope Extraction

Scope is extracted from PR body regex:

```
## Scope\n\s*\K\w+
```

Normalized to lowercase via `tr '[:upper:]' '[:lower:]'`.

## Branch Naming

```
agent/<scope>/<ticket>   — Plan phase
impl/<scope>/<ticket>    — Execute phase
```

## See Also

- [/agents/overview](/agents/overview.md)
- [/agents/orchestration](/agents/orchestration.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/patterns/phase-gating](/patterns/phase-gating.md)
