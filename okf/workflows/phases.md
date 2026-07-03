---
type: Workflow
title: Progressive Autonomy Phases
description: Four deployment phases with increasing autonomy levels for risk-based change management.
tags: [workflow, phases, autonomy, deployment]
timestamp: "2026-07-03T09:45:00Z"
---

# Progressive Autonomy Phases

## Phase 1 — Pull Requests Only

**Trigger:** PR opened

Behavior: All changes require a pull request. No auto-merge. Human must review and merge.

## Phase 2 — Auto-Merge Low Risk

**Trigger:** PR labeled `low-risk`

Behavior: After CI passes, the PR is auto-merged without human review. Risk classification determines eligibility.

## Phase 3 — Staging Deploy

**Trigger:** Push to main

Behavior: On every merge to main, the staging environment is automatically deployed. No manual approval needed.

**Docker steps:**
1. `docker compose build staging`
2. `docker compose stop staging && docker compose rm -f staging`
3. `docker compose up -d staging` → container `task-manager-staging` on port `8082`
4. Health check: `curl http://localhost:8082/`

**URL:** `http://localhost:8082`

## Phase 4 — Production Deploy

**Trigger:** `deploy`-labeled issue, or `workflow_dispatch` with ref

Behavior: Production deployment requires manual workflow dispatch and environment approval. Gated by GitHub Environments with 1 required reviewer.

**Docker steps:**
1. `docker compose build production`
2. `docker compose stop production && docker compose rm -f production`
3. `docker compose up -d production` → container `task-manager-prod` on port `8080`
4. Health check: `curl http://localhost:8080/`

**URL:** `http://localhost:8080`

**Note:** Staging runs on port 8082, production on port 8080. Both can run simultaneously.

## Autonomy Mapping

| Risk Level | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Deploy |
|-----------|---------|---------|---------|---------|--------|
| Critical | Required | — | — | Human-gated | Human-gated |
| High | Required | — | Auto | Human-gated | Human-gated |
| Medium | Required | — | Auto | Human-gated | Auto staging |
| Low | — | Auto | Auto | Human-gated | Auto staging |

## See Also

- [/governance/risk-classification](/governance/risk-classification.md)
- [/patterns/phase-gating](/patterns/phase-gating.md)
- [/governance/repository-settings](/governance/repository-settings.md)
