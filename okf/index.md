---
okf_version: "0.1"
type: Bundle
title: Agentic Task Manager Knowledge Bundle
description: OKF knowledge bundle for the Agentic Task Manager project — a Flask web app driven by agentic AI with GitHub Actions orchestration and opencode coding agents.
resource: https://github.com/MyOrgPavan/agentic-task-manager
tags: [flask, github-actions, opencode, agentic-ai, task-manager]
timestamp: "2026-07-03T09:45:00Z"
---

# Agentic Task Manager Knowledge Bundle

This bundle documents the architecture, components, workflows, agents, governance, and patterns of the Agentic Task Manager project.

## Architecture

- [/architecture/overview](/architecture/overview.md) — System architecture and design
- [/architecture/stack](/architecture/stack.md) — Technology stack details
- [/architecture/security](/architecture/security.md) — Authentication and security model

## Components

- [/components/flask-app](/components/flask-app.md) — Flask application factory and entry point
- [/components/models](/components/models.md) — SQLAlchemy data models (User, Project, Task, Comment)
- [/components/routes-auth](/components/routes-auth.md) — Authentication routes (register, login, logout)
- [/components/routes-projects](/components/routes-projects.md) — Project CRUD routes
- [/components/routes-tasks](/components/routes-tasks.md) — Task CRUD routes
- [/components/routes-comments](/components/routes-comments.md) — Comment routes
- [/components/frontend-templates](/components/frontend-templates.md) — Jinja2 HTML templates
- [/components/static-assets](/components/static-assets.md) — Static CSS assets
- [/components/tests](/components/tests.md) — Test suite (pytest)

## Workflows

- [/workflows/overview](/workflows/overview.md) — CI/CD pipeline ecosystem
- [/workflows/agent-plan](/workflows/agent-plan.md) — Plan phase workflow
- [/workflows/agent-execute](/workflows/agent-execute.md) — Execute phase workflow
- [/workflows/agent-evaluate](/workflows/agent-evaluate.md) — Evaluate phase workflow
- [/workflows/agentic-router](/workflows/agentic-router.md) — Intent routing and dispatch
- [/workflows/ci](/workflows/ci.md) — Continuous integration pipeline
- [/workflows/phases](/workflows/phases.md) — Progressive autonomy deployment phases

## Agents

- [/agents/overview](/agents/overview.md) — Agent system architecture
- [/agents/frontend](/agents/frontend.md) — Frontend coding agent
- [/agents/backend](/agents/backend.md) — Backend coding agent
- [/agents/database](/agents/database.md) — Database agent
- [/agents/orchestration](/agents/orchestration.md) — Orchestration agents (audit, integrator, merger)

## Governance

- [/governance/risk-classification](/governance/risk-classification.md) — Risk levels and autonomy mapping
- [/governance/codeowners](/governance/codeowners.md) — CODEOWNERS assignment
- [/governance/repository-settings](/governance/repository-settings.md) — Rulesets, environments, protections
- [/governance/memory](/governance/memory.md) — Agent memory system

## Patterns

- [/patterns/lifecycle](/patterns/lifecycle.md) — Plan-Act-Evaluate software lifecycle
- [/patterns/scoping](/patterns/scoping.md) — Agent scoping and phase restrictions
- [/patterns/phase-gating](/patterns/phase-gating.md) — Autonomy phase progression
- [/patterns/rollback](/patterns/rollback.md) — Rollback procedures
- [/patterns/drift-detection](/patterns/drift-detection.md) — Context drift detection and correction

## Infrastructure

- [/infrastructure/docker](/infrastructure/docker.md) — Docker and containerization
- [/infrastructure/mcp-servers](/infrastructure/mcp-servers.md) — MCP servers for memory and validation
- [/infrastructure/scripts](/infrastructure/scripts.md) — Utility scripts
- [/infrastructure/intents](/infrastructure/intents.md) — Agent intent files
