---
type: Component
title: Flask Application Factory
description: Application entry point and factory that initializes the Flask app, database, blueprints, and error handlers.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/app.py
tags: [components, flask, application]
timestamp: "2026-07-03T09:45:00Z"
---

# Flask Application Factory

## Structure

```
create_app()
 ├── init SQLAlchemy
 ├── init Flask-Login
 ├── register_blueprints
 │   ├── auth_bp    → /auth
 │   ├── projects_bp → /projects
 │   ├── tasks_bp   → /tasks
 │   ├── comments_bp → /comments
 │   └── main_bp    → /
 └── error handlers
     ├── 404 → page_not_found
     └── 500 → internal_error
```

## Configuration

- Database: SQLite by default, configurable via `DATABASE_URL`
- Template folder: `templates/`
- Static folder: `static/`
- Debug: configurable

## Blueprint Registration

All blueprints registered via `app.register_blueprint()` with url_prefix:
- `/auth` — Authentication routes
- `/projects` — Project CRUD
- `/tasks` — Task CRUD
- `/comments` — Comment CRUD
- `/` — Main and dashboard routes

## See Also

- [/components/routes-auth](/components/routes-auth.md)
- [/components/routes-projects](/components/routes-projects.md)
- [/components/routes-tasks](/components/routes-tasks.md)
- [/components/routes-comments](/components/routes-comments.md)
- [/components/frontend-templates](/components/frontend-templates.md)
