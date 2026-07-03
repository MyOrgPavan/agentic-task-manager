---
type: Component
title: Tests
description: Pytest-based test suite covering models and API endpoints.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/backend/tests/
tags: [components, tests, pytest, api]
timestamp: "2026-07-03T09:45:00Z"
---

# Tests

## Structure

```
backend/tests/
├── conftest.py        ← Fixtures: app, client, db, auth_headers
├── test_models.py     ← 16 tests: User, Project, Task, Comment
└── test_api.py        ← 13 tests: CRUD endpoints for all resources
```

## Test Coverage

| Model | Tests | Key Assertions |
|-------|-------|----------------|
| User | 4 | creation, repr, password hashing |
| Project | 4 | creation, relationship to user, string repr |
| Task | 4 | creation, status/priority defaults, relationships |
| Comment | 4 | creation, relationships, content validation |

| API | Tests | Key Assertions |
|-----|-------|----------------|
| Auth | 3 | register, login, logout |
| Projects | 4 | create, list, update, delete |
| Tasks | 3 | create, list, update |
| Comments | 3 | create, list, delete |

## Fixtures

- `app` — Flask test app with in-memory SQLite
- `client` — Test client
- `db` — Database setup/teardown per test
- `auth_headers` — JWT-style auth via token

## Running

```bash
pytest backend/tests/ -v
```

## See Also

- [/workflows/ci](/workflows/ci.md)
- [/components/models](/components/models.md)
- [/components/routes-auth](/components/routes-auth.md)
- [/components/routes-projects](/components/routes-projects.md)
- [/components/routes-tasks](/components/routes-tasks.md)
- [/components/routes-comments](/components/routes-comments.md)
