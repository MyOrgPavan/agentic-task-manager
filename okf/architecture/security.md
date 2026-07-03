---
type: Architecture
title: Security Model
description: Authentication, authorization, and security architecture of the Agentic Task Manager.
tags: [security, auth, flask-login, passwords]
timestamp: "2026-07-03T09:45:00Z"
---

# Security Model

## Authentication

Flask-Login manages user sessions. The `login_manager` is initialized in `backend/app.py` with `login_view = "auth.login"`.

```
User submits credentials → POST /auth/login
  → User.check_password(plaintext) → werkzeug check_password_hash
  → flask_login.login_user(user)
  → session cookie set
```

## Password Storage

Passwords are hashed using Werkzeug's `generate_password_hash` (pbkdf2:sha256 by default). Never stored in plaintext.

## CSRF Protection

Flask-WTF CSRF protection is available but **disabled** in config (`WTF_CSRF_ENABLED = False`). This is a development convenience — production deployments should enable it.

## Routes Without Auth

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Landing page |
| `/auth/register` | GET, POST | User registration |
| `/auth/login` | GET, POST | User login |
| `/hello` | GET | Demo page (no auth required) |

## Routes Requiring Auth

| Route | Method | Purpose |
|-------|--------|---------|
| `/auth/logout` | GET | End session |
| `/projects/` | GET, POST | List/create projects |
| `/projects/<id>` | GET, PUT, DELETE | Project CRUD |
| `/projects/<id>/tasks` | GET, POST | List/create tasks |
| `/tasks/<id>` | GET, PUT, DELETE | Task CRUD |
| `/tasks/<id>/comments` | GET, POST | List/create comments |
| `/comments/<id>` | DELETE | Delete comment |

## Production Considerations

- Enable CSRF protection
- Use a strong random `SECRET_KEY`
- Use PostgreSQL with SSL
- Set `FLASK_ENV=production`
- Configure proper CORS if adding API clients

## See Also

- [/components/routes-auth](/components/routes-auth.md)
- [/components/flask-app](/components/flask-app.md)
- [/governance/repository-settings](/governance/repository-settings.md)
