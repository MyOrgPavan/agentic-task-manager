---
type: Component
title: Authentication Routes
description: Login, logout, and registration endpoints using Flask-Login.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/routes/auth.py
tags: [components, routes, auth, flask-login]
timestamp: "2026-07-03T09:45:00Z"
---

# Authentication Routes

## Endpoints

| Route | Methods | Description |
|-------|---------|-------------|
| `/auth/login` | GET, POST | User login |
| `/auth/logout` | GET | User logout |
| `/auth/register` | GET, POST | User registration |

## Pattern

All auth routes follow the same pattern:
1. GET: Render template
2. POST: Validate form → authenticate/create → log in → redirect

## Middleware

- `login_required` decorator on protected routes (blueprint level)
- `@login_manager.user_loader` in `app.py` for session loading

## See Also

- [/components/frontend-templates](/components/frontend-templates.md)
- [/components/flask-app](/components/flask-app.md)
- [/components/tests](/components/tests.md)
