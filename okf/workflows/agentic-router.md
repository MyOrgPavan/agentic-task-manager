---
type: Workflow
title: Agentic Router Workflow
description: Routes issues and intent files to the correct agent scope (frontend, backend, db, docs, infra).
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/workflows/agentic-router.yml
tags: [workflow, router, intents, dispatch]
timestamp: "2026-07-03T09:45:00Z"
---

# Agentic Router Workflow

## Trigger

- `push` on `agent-intents/*.md`
- `workflow_dispatch` with `intent_file` input
- `issues: [opened, labeled]`

## Jobs

### route-from-issue (when triggered by issues)
1. Read issue labels to determine scope (frontend, backend, db, docs, infra)
2. Trigger the `Agent - Plan` workflow with the appropriate scope and ticket

### parse-intent (when triggered by push or dispatch)
1. Read markdown intent file with YAML frontmatter
2. Parse frontmatter using `scripts/parse_frontmatter.py`
3. Create a lock file in `locks/` to prevent duplicate processing
4. Dispatch to the appropriate agent workflow

## Intent File Format

```yaml
---
scope: backend
ticket: "123"
risk: medium
command: "Description of the task"
---
```

## See Also

- [/workflows/agent-plan](/workflows/agent-plan.md)
- [/infrastructure/intents](/infrastructure/intents.md)
- [/infrastructure/scripts](/infrastructure/scripts.md)
