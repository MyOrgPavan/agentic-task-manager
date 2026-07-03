---
type: Infrastructure
title: Supporting Scripts
description: Python scripts that support the agentic workflow — parsing, locking, failure analysis, and PR creation.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/scripts/
tags: [infrastructure, scripts, python]
timestamp: "2026-07-03T09:45:00Z"
---

# Supporting Scripts

## parse_frontmatter.py

Reads an intent file (markdown + YAML frontmatter) and outputs scope, ticket, risk, and command as JSON.

**Used by:** agentic-router.yml (parse-intent job)

## create_impl_pr.py

Takes plan artifacts and creates an implementation branch and PR. Handles the following steps:
1. Creates branch `impl/<scope>/<ticket>`
2. Commits changed files
3. Opens PR via GitHub API

**Used by:** agent-execute.yml (execute job)

## fetch_failures.py

Fetches CI failure logs for a given PR and returns structured error summaries.

**Used by:** agent-ci-evaluate.yml (evaluate-failures job)

## Scope Extraction Convention

Scope is extracted from PR body via regex:

```
## Scope\n\s*\K\w+
```

Normalized to lowercase.

## See Also

- [/workflows/agentic-router](/workflows/agentic-router.md)
- [/workflows/agent-execute](/workflows/agent-execute.md)
- [/workflows/agent-evaluate](/workflows/agent-evaluate.md)
