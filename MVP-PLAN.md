# Agentic Task Manager — MVP Implementation Plan

## MVP 1: Project Scaffolding
**Files:** `requirements.txt`, `pyproject.toml`, `.env.example`, `Dockerfile`, `docker-compose.yml`
**Goal:** Python project config + containerization working.

## MVP 2: Flask Backend Core
**Files:** `backend/models.py`, `backend/app.py`, `backend/routes/__init__.py`, `backend/routes/auth.py`, `backend/templates/base.html`, `backend/templates/index.html`, `backend/templates/register.html`, `backend/templates/login.html`, `backend/static/style.css`
**Goal:** Flask app boots, user can register/login/logout via browser.

## MVP 3: Flask Backend Complete
**Files:** `backend/routes/projects.py`, `backend/routes/tasks.py`, `backend/routes/comments.py`, `backend/templates/projects.html`, `backend/templates/project_detail.html`, `backend/templates/task_detail.html`
**Goal:** Full CRUD for projects, tasks, comments.

## MVP 4: Flask Tests
**Files:** `backend/tests/__init__.py`, `backend/tests/test_models.py`, `backend/tests/test_api.py`
**Goal:** pytest suite passes.

## MVP 5: CI + Core Agent Workflows
**Files:** `.github/workflows/ci.yml`, `.github/workflows/agent-plan.yml`, `.github/workflows/agent-execute.yml`, `.github/workflows/agent-backend.yml`, `.github/workflows/agent-frontend.yml`, `.github/workflows/agent-db.yml`
**Goal:** CI pipeline + plan/execute lifecycle + 3 agent personas.

## MVP 6: Orchestration & Observability Workflows
**Files:** `.github/workflows/agent-integrator.yml`, `.github/workflows/agent-audit.yml`, `.github/workflows/agent-merger.yml`, `.github/workflows/conflict-detection.yml`, `.github/workflows/drift-detection.yml`, `.github/workflows/resume-work.yml`, `.github/workflows/failure-analysis.yml`, `.github/workflows/memory-expiry.yml`, `.github/workflows/governance-review.yml`
**Goal:** Multi-agent orchestration, drift detection, failure analysis, memory pruning.

## MVP 7: Phase Workflows & Anti-Patterns
**Files:** `.github/workflows/phase-1-pull-requests.yml`, `.github/workflows/phase-2-auto-merge.yml`, `.github/workflows/phase-3-staging.yml`, `.github/workflows/phase-4-production.yml`, `.github/workflows/anti-pattern-demo.yml`
**Goal:** Progressive autonomy phases + anti-pattern demonstrations.

## MVP 8: Config, Scripts & MCP Servers
**Files:** `.github/CODEOWNERS`, `.github/risk-classification.yml`, `.github/mcp-allowlist.yml`, `.github/AGENTS_MEMORY.md`, `.github/PR_TEMPLATE.md`, `scripts/rollback.sh`, `scripts/drift-check.sh`, `scripts/generate-plan.py`, `mcp-servers/agent-memory-server.py`, `mcp-servers/validate-schema-server.py`
**Goal:** All governance, memory, tooling infrastructure.

## MVP 9: Documentation
**Files:** `DEMONSTRATION.md`
**Goal:** End-to-end scenario walkthroughs (S-01 through S-07).
