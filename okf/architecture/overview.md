---
type: Architecture
title: System Architecture Overview
description: High-level architecture of the Agentic Task Manager — a Flask web app with agent-driven development orchestrated via GitHub Actions.
tags: [architecture, flask, github-actions, agents]
timestamp: "2026-07-03T09:45:00Z"
---

# System Architecture Overview

## Design

The Agentic Task Manager is a demonstration platform for **agent-driven software development**. It combines a functional Flask web application with a full CI/CD ecosystem where coding AI agents (opencode) are invoked from GitHub Actions to implement features.

## Layers

### Application Layer
Flask web application with SQLAlchemy ORM, Jinja2 templates, Bootstrap 5 frontend. Supports user authentication, project/task/comment CRUD, and both HTML and JSON API responses.

### Orchestration Layer
21 GitHub Actions workflows implementing a **Plan → Act → Evaluate** lifecycle. Workflows are triggered by issues, PRs, labels, schedule, and workflow_dispatch.

### Agent Layer
Domain-specific coding agents (frontend, backend, database) with phase-based tool restrictions. Agents are invoked via opencode CLI inside workflow steps.

### Governance Layer
Risk classification maps file patterns to autonomy levels. CODEOWNERS enforces review requirements. Repository rulesets and deployment environments gate promotions.

## Key Principles

- **Durable artifacts** — Every agent action produces a GitHub artifact (PRs, workflow logs, plan files)
- **Self-correction** — CI failures trigger analysis and bounded retries with escalation
- **Progressive autonomy** — Low-risk changes auto-merge; high-risk changes require human approval
- **Phase-based gating** — Plan phase is read-only; Execute phase has write access; Evaluate phase is diagnostic

## See Also

- [/architecture/stack](/architecture/stack.md)
- [/architecture/security](/architecture/security.md)
- [/patterns/lifecycle](/patterns/lifecycle.md)
- [/workflows/overview](/workflows/overview.md)
- [/agents/overview](/agents/overview.md)
