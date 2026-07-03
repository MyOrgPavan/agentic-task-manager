---
type: Infrastructure
title: Intent Files
description: Markdown files with YAML frontmatter that encode a developer's intent for agent execution. Pushed to agent-intents/ branches.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/agent-intents/
tags: [infrastructure, intents, dispatch]
timestamp: "2026-07-03T09:45:00Z"
---

# Intent Files

## Format

```yaml
---
scope: backend
ticket: "123"
risk: medium
command: "Add a new API endpoint for listing users"
---
```

## Placement

Pushed to the `agent-intents/` directory at the repository root. Named `<ticket>-<slug>.md`.

## Processing

1. A push to `agent-intents/*.md` triggers `agentic-router.yml`
2. Router parses frontmatter via `scripts/parse_frontmatter.py`
3. Creates a lock file in `locks/` to prevent duplicate processing
4. Dispatches to the appropriate agent workflow

## Relationship to Issues

Intents and Issues are parallel entry points:

| Entry Point | Trigger | Use Case |
|------------|---------|----------|
| Issue | Label + open | Non-developer stakeholders |
| Intent | Push to agent-intents/ | Developer-initiated changes |

## See Also

- [/workflows/agentic-router](/workflows/agentic-router.md)
- [/infrastructure/scripts](/infrastructure/scripts.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
