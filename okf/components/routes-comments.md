---
type: Component
title: Comment Routes
description: Comment creation and management on tasks.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/routes/comments.py
tags: [components, routes, comments, crud]
timestamp: "2026-07-03T09:45:00Z"
---

# Comment Routes

## Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/tasks/<task_id>/comments/create` | POST | Add comment to task |
| `/comments/<id>/delete` | POST | Delete own comment |

## Pattern

- Comments linked to both task and user
- Only the comment author can delete
- No edit endpoint (immutable after creation)
- Supports HTML redirect and JSON response

## See Also

- [/components/models](/components/models.md)
- [/components/routes-tasks](/components/routes-tasks.md)
- [/components/frontend-templates](/components/frontend-templates.md)
- [/components/tests](/components/tests.md)
