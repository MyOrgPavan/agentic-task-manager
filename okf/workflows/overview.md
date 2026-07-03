---
type: Workflow
title: CI/CD Workflow Ecosystem
description: Overview of the 21 GitHub Actions workflows that implement the Plan-Act-Evaluate lifecycle.
tags: [workflows, github-actions, ci-cd, orchestration]
timestamp: "2026-07-03T09:45:00Z"
---

# CI/CD Workflow Ecosystem

## Totals

21 workflows across 4 categories.

## Core Agent Workflows (5)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [/workflows/ci](/workflows/ci.md) | push/PR to main | Lint, typecheck, test |
| [/workflows/agent-plan](/workflows/agent-plan.md) | issue_comment, workflow_dispatch | Generate plan with opencode |
| [/workflows/agent-execute](/workflows/agent-execute.md) | PR labeled, workflow_dispatch | Implement plan with opencode |
| agent-frontend.yml | workflow_dispatch | Frontend-specific changes |
| agent-backend.yml | workflow_dispatch, workflow_run | Backend-specific changes |
| agent-db.yml | workflow_dispatch | Database schema changes |

## Orchestration & Observability (10)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| [/workflows/agentic-router](/workflows/agentic-router.md) | push intents, issues | Route to correct agent |
| agent-integrator.yml | workflow_run | Fan-in merge coordination |
| agent-audit.yml | workflow_dispatch | Read-only inspection |
| agent-merger.yml | workflow_run | Consume audit, merge |
| [/workflows/agent-evaluate](/workflows/agent-evaluate.md) | workflow_run (CI) | Analyze CI failures |
| conflict-detection.yml | PR events | Detect merge conflicts |
| drift-detection.yml | PR events | Detect context drift |
| failure-analysis.yml | workflow_run (CI) | Create failure issues |
| memory-cleanup.yml | schedule (weekly) | Prune old memory |
| governance-review.yml | schedule (monthly) | Governance report |

## Phase Workflows (4)

| Workflow | Trigger | Autonomy |
|----------|---------|---------|
| phase-1-pull-requests.yml | PR opened | Propose-only |
| phase-2-auto-merge.yml | PR labeled | Auto-merge low risk |
| phase-3-staging.yml | push to main | Auto-deploy staging |
| phase-4-production.yml | workflow_dispatch | Human-gated prod |

## Anti-Pattern Demo (1)

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| anti-pattern-demo.yml | workflow_dispatch | Demo bad vs good patterns |

## See Also

- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/patterns/phase-gating](/patterns/phase-gating.md)
- [/governance/risk-classification](/governance/risk-classification.md)
