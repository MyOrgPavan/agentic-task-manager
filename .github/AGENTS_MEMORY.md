# Agent Memory — Long-term Project Knowledge
# E-01, E-02, E-03, E-04
# Memory sections are scoped by regex. Agents append to relevant sections after merge.

## Project Overview
Agentic Task Manager is a Flask web application demonstrating agent-driven development with integrated coding LLM agents (opencode).

## Architecture Decisions
- Flask + SQLAlchemy for backend
- Bootstrap 5 for frontend
- SQLite for development, PostgreSQL for production
- GitHub Actions as the sole execution environment
- opencode CLI as the coding agent invoked from workflows
- MCP servers for memory, schema validation, and tool gating
- Phase-based tool permissions (plan=read-only, execute=write, evaluate=diagnostic)

## Agent Scopes
- `agent-backend`: Python files in `backend/` (models, routes, app)
- `agent-frontend`: HTML templates and static files
- `agent-db`: Database schema and migrations
- `agent-audit`: Read-only inspection across all scopes
- `agent-integrator`: Coordinates merging from multiple agents
- `agent-merger`: Consumes audit reports and executes merges
- `agent-evaluate`: Reads CI failures and re-invokes agents for self-correction

## Important Patterns
- Plan -> Act -> Evaluate lifecycle enforced for all changes
- Risk classification drives autonomy level
- PRs are the sole coordination mechanism between agents
- All agent actions produce durable GitHub artifacts
- Self-correction loop: CI failure → agent re-invoke → max 3 retries → escalate
- Phase-based tool gating: plan phase has no write access

## Agent Prompt Templates
- `.github/agents/frontend.agent.md` — frontend agent scope and restrictions
- `.github/agents/backend.agent.md` — backend agent scope and restrictions
- `.github/agents/db.agent.md` — database agent scope and restrictions

## Memory Sections (scoped by regex)
### Memory: Agent Decisions
Format: `YYYY-MM-DD: [agent:<scope>] <decision>`

### Memory: Completed Tasks
Format: `YYYY-MM-DD: Issue #N — <title> (PR #M)`

### Memory: Known Issues
Format: `YYYY-MM-DD: <description> — tracked in issue #N`
