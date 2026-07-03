---
type: Workflow
title: CI Pipeline
description: Continuous integration pipeline running lint, typecheck, and tests on every push/PR to main.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/workflows/ci.yml
tags: [workflow, ci, lint, typecheck, test]
timestamp: "2026-07-03T09:45:00Z"
---

# CI Pipeline

## Trigger

- `push` to main
- `pull_request` to main

## Jobs (parallel)

### lint
- Install ruff
- Run `ruff check backend/ scripts/ mcp-servers/`

### typecheck
- Install dependencies
- Run `mypy backend/ scripts/ mcp-servers/ --ignore-missing-imports`

### test
- Install dependencies
- Run `pytest backend/tests/ -v`
- Upload test results artifact

## Required Status Checks

All three jobs must pass before a PR can be merged. Enforced via branch protection rulesets.

## Per-Phase Behavior

| Phase | CI Behavior |
|-------|-------------|
| Plan PRs | CI runs but does not block |
| Implementation PRs | CI must pass for merge |
| Auto-merge (low risk) | CI passes → auto-merge |
| Staging deploy | CI passes on main → deploy |

## See Also

- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
- [/governance/repository-settings](/governance/repository-settings.md)
- [/components/tests](/components/tests.md)
