---
type: Component
title: Database Models
description: SQLAlchemy ORM models for the task management application.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/models.py
tags: [components, database, models, sqlalchemy]
timestamp: "2026-07-03T09:45:00Z"
---

# Database Models

## Model Hierarchy

```
User
 ├── projects (one-to-many via user_id)
 ├── tasks (one-to-many via user_id)
 └── comments (one-to-many via user_id)

Project
 ├── tasks (one-to-many via project_id)
 └── comments (one-to-many via project_id)

Task
 ├── comments (one-to-many via task_id)
 └── project (many-to-one via project_id)

Comment
 ├── user (many-to-one via user_id)
 └── task (many-to-one via task_id)
```

## User Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PK, auto |
| username | String(80) | Unique, non-null |
| email | String(120) | Unique, non-null |
| password_hash | String(256) | Non-null |

## Project Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PK, auto |
| title | String(200) | Non-null |
| description | Text | Nullable |
| user_id | Integer | FK to user.id |

## Task Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PK, auto |
| title | String(200) | Non-null |
| description | Text | Nullable |
| status | String(20) | Default 'todo' |
| priority | String(20) | Default 'medium' |
| due_date | DateTime | Nullable |
| project_id | Integer | FK to project.id |
| user_id | Integer | FK to user.id |

## Comment Model

| Field | Type | Constraints |
|-------|------|-------------|
| id | Integer | PK, auto |
| content | Text | Non-null |
| user_id | Integer | FK to user.id |
| task_id | Integer | FK to task.id |

## Key Patterns

- All models use `db.Model` base and `db.Column` type annotations
- Timestamps use `datetime.now(UTC)` for timezone awareness
- Relationships use `lazy="dynamic"` for collection attributes
- Cascade deletes: `project` → `tasks`, `task` → `comments`

## See Also

- [/components/routes-tasks](/components/routes-tasks.md)
- [/components/routes-projects](/components/routes-projects.md)
- [/components/tests](/components/tests.md)
- [/agents/database](/agents/database.md)
