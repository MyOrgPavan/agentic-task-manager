---
type: Component
title: Project Routes
description: CRUD endpoints for projects with Flask-Login protection.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/routes/projects.py
tags: [components, routes, projects, crud]
timestamp: "2026-07-03T09:45:00Z"
---

# Project Routes

## Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/projects` | GET | List user's projects |
| `/projects/<id>` | GET | View single project |
| `/projects/create` | GET, POST | Create new project |
| `/projects/<id>/edit` | GET, POST | Edit project |
| `/projects/<id>/delete` | POST | Delete project |

## Pattern

Standard CRUD pattern:
1. GET: Render form or detail view
2. POST: Validate → persist → redirect with flash
3. All routes require login
4. Projects scoped to current user

## Response Format

Supports both HTML (template rendering) and JSON (`request.is_json`) responses.

## See Also

- [/components/models](/components/models.md)
- [/components/frontend-templates](/components/frontend-templates.md)
- [/components/tests](/components/tests.md)
