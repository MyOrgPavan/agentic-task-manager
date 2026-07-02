# E-01
# Agent Memory — Long-term Project Knowledge

## Project Overview (2026-07-01)
Agentic Task Manager is a Flask web application demonstrating agent-driven development.

## Architecture Decisions
- Flask + SQLAlchemy for backend (2026-07-01)
- Bootstrap 5 for frontend (2026-07-01)
- SQLite for development, PostgreSQL for production (2026-07-01)
- GitHub Actions as the sole execution environment (2026-07-01)

## Agent Scopes
- `agent-backend`: Python files in `backend/` (models, routes, app)
- `agent-frontend`: HTML templates and static files
- `agent-db`: Database schema and migrations
- `agent-audit`: Read-only inspection across all scopes
- `agent-integrator`: Coordinates merging from multiple agents
- `agent-merger`: Consumes audit reports and executes merges

## Important Patterns
- Plan -> Act -> Evaluate lifecycle enforced for all changes
- Risk classification drives autonomy level
- PRs are the sole coordination mechanism between agents
- All agent actions produce durable GitHub artifacts
