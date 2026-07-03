---
type: Governance
title: Agent Memory System
description: Hierarchical memory system for long-term project knowledge across agent sessions.
resource: /home/pavan/Workspace/Projects/Github sdlc/agentic-task-manager/.github/AGENTS_MEMORY.md
tags: [governance, memory, agents, persistence]
timestamp: "2026-07-03T09:45:00Z"
---

# Agent Memory System

## Architecture

Three-tier memory hierarchy:

| Tier | Storage | Duration | Scope |
|------|---------|----------|-------|
| Short-term | GitHub PRs, issues, comments | Per-session | Single feature |
| Long-term | `.github/AGENTS_MEMORY.md` | Persistent | Cross-session |
| External | GitHub Issues | Indefinite | Escalations, decisions |

## Long-Term Memory Format

Stored in `.github/AGENTS_MEMORY.md` with scoped sections:

```
### Memory: Agent Decisions
YYYY-MM-DD: [agent:<scope>] <decision>

### Memory: Completed Tasks
YYYY-MM-DD: Issue #N — <title> (PR #M)

### Memory: Known Issues
YYYY-MM-DD: <description> — tracked in issue #N
```

## Memory Access

- **Read:** MCP server `agent-memory-server.py` — reads `.github/AGENTS_MEMORY.md` with optional scope filtering (regex)
- **Write:** MCP server appends new entries with date stamp

## Expiry

Weekly cleanup via `memory-cleanup.yml` workflow — prunes entries older than 30 days.

## See Also

- [/infrastructure/mcp-servers](/infrastructure/mcp-servers.md)
- [/agents/overview](/agents/overview.md)
