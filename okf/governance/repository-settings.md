---
type: Governance
title: Repository Settings
description: Branch protection rulesets, GitHub Environments, and required status checks.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/REPOSITORY-SETTINGS.md
tags: [governance, repository, rulesets, environments]
timestamp: "2026-07-03T09:45:00Z"
---

# Repository Settings

## Main Branch Ruleset

- Require pull request before merging
- Require 1 approval
- Require status checks: **lint**, **typecheck**, **test**
- Block force push

## GitHub Infrastructure Ruleset

- Path: `.github/**`
- Require 2 approvals
- Require CODEOWNERS review
- Block force push

## Environments

### Production

| Setting | Value |
|---------|-------|
| Required reviewers | 1 |
| Branches | main |
| Secrets | DATABASE_URL |
| Wait timer | 0 |

### Staging

| Setting | Value |
|---------|-------|
| Required reviewers | 0 |
| Branches | main |
| Wait timer | 0 |

## MCP Allowlist

Phase-based tool gating per agent scope, defined in `.github/mcp-allowlist.yml`:

- **plan:** read_file, search_files, read_memory, validate_schema
- **execute:** write tools with retry_limit: 3, requires_human_review for db
- **evaluate:** read_ci_logs, read_memory, write_memory, add_label

## See Also

- [/governance/codeowners](/governance/codeowners.md)
- [/governance/risk-classification](/governance/risk-classification.md)
- [/workflows/phases](/workflows/phases.md)
