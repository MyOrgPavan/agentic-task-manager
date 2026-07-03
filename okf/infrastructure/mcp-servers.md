---
type: Infrastructure
title: MCP Servers
description: Model Context Protocol servers augmenting opencode's capabilities — memory, CI logs, project config, and validation.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/mcp-servers/
tags: [infrastructure, mcp, servers, python]
timestamp: "2026-07-03T09:45:00Z"
---

# MCP Servers

## agent-memory-server.py

**Port:** 8100

Reads and writes `.github/AGENTS_MEMORY.md`. Provides scope-filtered memory queries.

**Tools:**
- `read_memory(scope: str = None)` — Returns memory entries, optionally filtered by scope regex
- `write_memory(content: str)` — Appends a timestamped entry
- `get_memory_summary()` — Returns a summary of recent entries

## agent-ci-logs-server.py

**Port:** 8100

Reads CI logs for a given PR via GitHub API.

**Tools:**
- `get_failed_jobs(pr_number: int)` — Returns list of failed job names and their log excerpts

## agent-config-server.py

**Port:** 8100

Provides project configuration context — list of files, risk classification rules, agent scopes.

**Tools:**
- `get_project_map()` — Returns all file scopes
- `get_risk_rules()` — Returns risk classification
- `get_agent_config(scope: str)` — Returns agent config for a scope

## agent-validator-server.py

**Port:** 8100

Validates generated plans against required sections.

**Tools:**
- `validate_plan(plan_content: str)` — Checks all required sections exist

## See Also

- [/governance/memory](/governance/memory.md)
- [/infrastructure/scripts](/infrastructure/scripts.md)
- [/agents/overview](/agents/overview.md)
