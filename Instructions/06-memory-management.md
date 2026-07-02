# 06 — Memory Management

How to manage the agent memory hierarchy and expiry.

## Memory Hierarchy (E-01)

| Level | Storage | Purpose | Scope |
|-------|---------|---------|-------|
| Short-term | PR description | Current task context | Per PR |
| Long-term | `.github/AGENTS_MEMORY.md` | Curated project knowledge | Global |
| External | Issues, PRs, workflow logs | Durable evidence | Global |

---

## Long-term Memory Structure

The `AGENTS_MEMORY.md` file contains:

```markdown
# Agent Memory — Long-term Project Knowledge

## Project Overview (2026-07-01)
Agentic Task Manager is a Flask web application...

## Architecture Decisions (scope: backend)
- Flask + SQLAlchemy for backend
- Bootstrap 5 for frontend

## Agent Scopes
- `agent-backend`: Python files in `backend/`
- `agent-frontend`: HTML templates and static files

## Important Patterns
- Plan → Act → Evaluate lifecycle enforced
- PRs are the sole coordination mechanism
```

---

## Reading Memory

### Via MCP Server

```bash
# Read all memory
echo '{"action": "read"}' | python3 mcp-servers/agent-memory-server.py

# Read scoped memory
echo '{"action": "read", "scope": "backend"}' | python3 mcp-servers/agent-memory-server.py
```

### Via Workflow

Agent workflows read memory automatically:
- Short-term: from PR description
- Long-term: from `AGENTS_MEMORY.md`
- External: from linked issues/PRs

---

## Writing Memory

### Via MCP Server

```bash
echo '{"action": "write", "entry": "Task filtering endpoint implemented"}' | python3 mcp-servers/agent-memory-server.py
```

### Manually

Edit `.github/AGENTS_MEMORY.md` and add entries:
```markdown
## Feature Decisions (2026-07-15)
- Task filtering supports comma-separated priorities (PR #42)
```

---

## Memory Expiry (E-04)

The `memory-expiry.yml` workflow runs weekly:

```yaml
on:
  schedule:
    - cron: "0 6 * * 1"  # Every Monday at 06:00 UTC
```

### What It Does

1. Reads `AGENTS_MEMORY.md`
2. Prunes entries older than 30 days
3. Archives pruned entries to a GitHub Issue
4. Updates memory file

### Manual Trigger

```bash
gh workflow run "Memory Expiry"
```

---

## Memory Scoping (E-03)

Each agent only reads memory relevant to its scope:

```yaml
# In agent-memory-server.py
if scope:
    sections = re.split(r"\n## ", content)
    filtered = [s for s in sections if scope.lower() in s.lower()]
```

### Adding Scoped Entries

```markdown
## Backend Patterns (scope: backend)
- Use Flask blueprints for route organization
- Always validate inputs in routes

## Frontend Patterns (scope: frontend)
- Use Bootstrap 5 for responsive design
- Keep templates minimal
```

---

## Source of Truth (E-02)

| Information | Location | Example |
|-------------|----------|---------|
| Requirements | GitHub Issues | Issue #42: "Add task filtering" |
| Decisions | PR descriptions | PR #45: "Using comma-separated priorities" |
| Validation rules | `.github/` configs | `risk-classification.yml` |
| Results | Workflow logs | CI run logs, artifact uploads |

---

## Context Drift Detection (E-06, E-07)

### How It Works

1. `drift-detection.yml` triggers on PR changes
2. Compares PR changes against plan success criteria
3. Flags contradictions or scope creep
4. Adds drift report to PR

### Running Manually

```bash
gh workflow run "Drift Detection" --field pr_number=45
```

### Drift Report Format

```json
{
  "pr_number": 45,
  "drift_detected": true,
  "plan_files": "backend/routes/tasks.py",
  "changed_files": "backend/routes/tasks.py backend/models.py"
}
```

---

## Best Practices

1. **Keep memory concise** — summarize decisions, not implementation details
2. **Use scopes** — tag entries with `(scope: backend)` etc.
3. **Archive old entries** — let expiry workflow handle cleanup
4. **Reference PRs/Issues** — link to durable evidence
5. **Review memory monthly** — governance review should assess quality