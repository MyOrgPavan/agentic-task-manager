---
type: Governance
title: Risk Classification
description: Maps file patterns to risk levels (critical/high/medium/low) which determine agent autonomy levels.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/risk-classification.yml
tags: [governance, risk, autonomy, classification]
timestamp: "2026-07-03T09:45:00Z"
---

# Risk Classification

## Default Risk Level

`medium`

## File Pattern → Risk Mapping

| Pattern | Risk Level |
|---------|-----------|
| `backend/models.py` | high |
| `backend/routes/*.py` | medium |
| `backend/templates/*.html` | low |
| `backend/static/*` | low |
| `.github/workflows/*.yml` | critical |
| `.github/*.yml` | high |
| `requirements.txt` | high |
| `pyproject.toml` | high |
| `Dockerfile` | medium |
| `docker-compose.yml` | medium |
| `mcp-servers/*.py` | high |
| `scripts/*` | medium |

## Risk → Autonomy Mapping

| Risk Level | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|-----------|---------|---------|---------|---------|
| critical | read_only/propose_only | — | — | — |
| high | propose_only | execute_with_guardrails | — | — |
| medium | propose_only | execute_with_guardrails | — | — |
| low | — | execute_with_guardrails | auto_merge | — |

## See Also

- [/workflows/phases](/workflows/phases.md)
- [/patterns/phase-gating](/patterns/phase-gating.md)
- [/governance/repository-settings](/governance/repository-settings.md)
- [/governance/codeowners](/governance/codeowners.md)
