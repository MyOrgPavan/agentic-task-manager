---
type: Component
title: Task Routes
description: CRUD endpoints for tasks within projects.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/routes/tasks.py
tags: [components, routes, tasks, crud]
timestamp: "2026-07-03T09:45:00Z"
---

# Task Routes

## Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/tasks/<id>` | GET | View single task |
| `/projects/<project_id>/tasks/create` | GET, POST | Create task in project |
| `/tasks/<id>/edit` | GET, POST | Edit task |
| `/tasks/<id>/delete` | POST | Delete task |
| `/tasks/<id>/status` | POST | Toggle task status |

## Task Statuses

- `todo` (default)
- `in_progress`
- `done`

## Task Priorities

- `low`
- `medium` (default)
- `high`

## Pattern

Tasks are scoped to projects. Routes validate that the task belongs to the current user's project. Supports HTML and JSON responses.

## See Also

- [/components/models](/components/models.md)
- [/components/routes-comments](/components/routes-comments.md)
- [/components/frontend-templates](/components/frontend-templates.md)
- [/components/tests](/components/tests.md)
