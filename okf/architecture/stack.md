---
type: Architecture
title: Technology Stack
description: Complete technology stack used by the Agentic Task Manager project.
tags: [stack, flask, python, bootstrap, sqlalchemy]
timestamp: "2026-07-03T09:45:00Z"
---

# Technology Stack

## Backend

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Flask | >=3.1 | HTTP routing, request handling, templating |
| ORM | SQLAlchemy | >=2.0 | Database abstraction and model management |
| Auth | Flask-Login | >=0.6 | Session-based user authentication |
| Forms | Flask-WTF / WTForms | >=1.2 / >=3.2 | Form validation and CSRF protection |
| Password Hashing | Werkzeug | >=3.1 | `generate_password_hash` / `check_password_hash` |
| WSGI Server | Gunicorn | >=23.0 | Production HTTP server |
| Runtime | Python | >=3.11 | Application runtime |

## Frontend

| Component | Technology | Purpose |
|-----------|-----------|---------|
| CSS Framework | Bootstrap 5.3.3 | Responsive layout, components, utilities |
| Templating | Jinja2 | Server-side HTML rendering with inheritance |
| Custom CSS | style.css | Sticky footer layout, background color |

## Database

| Environment | Database | Driver |
|-------------|----------|--------|
| Development | SQLite | Built-in |
| Production | PostgreSQL | psycopg2-binary (commented) |

## CI/CD & Orchestration

| Component | Technology | Purpose |
|-----------|-----------|---------|
| CI Platform | GitHub Actions | All workflow execution |
| Coding Agent | opencode CLI | Plan generation and code implementation |
| Model | opencode/big-pickle | LLM used by opencode |
| Linter | ruff | Python linting |
| Type Checker | mypy | Static type checking |
| Test Runner | pytest | Unit and integration tests |

## Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Containerization | Docker | Consistent runtime environment |
| Orchestration | docker-compose | Multi-service local development |
| MCP Servers | Python | Memory management and schema validation |

## See Also

- [/architecture/overview](/architecture/overview.md)
- [/components/flask-app](/components/flask-app.md)
- [/components/models](/components/models.md)
- [/infrastructure/docker](/infrastructure/docker.md)
