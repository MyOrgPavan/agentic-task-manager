---
type: Governance
title: CODEOWNERS
description: GitHub CODEOWNERS assignment for automatic review requests.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/CODEOWNERS
tags: [governance, codeowners, review]
timestamp: "2026-07-03T09:45:00Z"
---

# CODEOWNERS

## Rules

| Pattern | Owner | Rationale |
|---------|-------|-----------|
| `*` | `@core-maintainers` | Default owner for all files |
| `.github/` | `@core-maintainers` | Infrastructure changes require senior review |
| `backend/models.py` | `@core-maintainers` | Schema changes |
| `requirements.txt` | `@core-maintainers` | Dependency changes |
| `pyproject.toml` | `@core-maintainers` | Build/config changes |
| `backend/` | `@agent-backend` | Backend code |
| `backend/templates/` | `@agent-frontend` | Frontend templates |
| `backend/static/` | `@agent-frontend` | Static assets |
| `Dockerfile` | `@core-maintainers` | Container config |
| `docker-compose.yml` | `@core-maintainers` | Service orchestration |

## Effect

- PRs modifying `.github/` require 2 approvals from `@core-maintainers`
- PRs modifying `backend/templates/` auto-request review from `@agent-frontend`
- Governed by branch protection rulesets

## See Also

- [/governance/repository-settings](/governance/repository-settings.md)
- [/governance/risk-classification](/governance/risk-classification.md)
