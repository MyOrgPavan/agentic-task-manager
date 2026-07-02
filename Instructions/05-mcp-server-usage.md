# 05 — MCP Server Usage

How to use and extend the Model Context Protocol (MCP) servers for agent tooling.

## Overview

MCP servers expose tools that agents can call. The tool access is controlled by `.github/mcp-allowlist.yml`.

| Server | Purpose | Tools |
|--------|---------|-------|
| `agent-memory-server.py` | Read/write AGENTS_MEMORY.md | `read-memory`, `write-memory` |
| `validate-schema-server.py` | Validate schema, format code, run tests | `validate-schema`, `format-code`, `run-tests` |

---

## Using MCP Servers Directly

### Agent Memory Server

**Read memory (all scopes):**
```bash
echo '{"action": "read"}' | python3 mcp-servers/agent-memory-server.py
```

**Read memory (filtered by scope):**
```bash
echo '{"action": "read", "scope": "backend"}' | python3 mcp-servers/agent-memory-server.py
```

**Write to memory:**
```bash
echo '{"action": "write", "entry": "Task filtering implemented in GET /tasks endpoint"}' | python3 mcp-servers/agent-memory-server.py
```

### Validate Schema Server

**Validate models:**
```bash
echo '{"action": "validate-schema"}' | python3 mcp-servers/validate-schema-server.py
```

**Validate specific file:**
```bash
echo '{"action": "validate-schema", "path": "backend/models.py"}' | python3 mcp-servers/validate-schema-server.py
```

**Format code:**
```bash
echo '{"action": "format-code", "path": "backend/routes/tasks.py"}' | python3 mcp-servers/validate-schema-server.py
```

**Run tests:**
```bash
echo '{"action": "run-tests"}' | python3 mcp-servers/validate-schema-server.py
```

---

## MCP Allowlist Configuration

The allowlist in `.github/mcp-allowlist.yml` controls which tools each agent can access:

```yaml
agent-backend:
  servers:
    - validate-schema-server
    - agent-memory-server
  tools:
    - validate-schema
    - format-code
    - run-tests
    - read-memory
    - write-memory

agent-frontend:
  servers:
    - agent-memory-server
  tools:
    - format-code
    - read-memory
```

### Adding a New Tool

1. **Create the tool function** in the MCP server:
   ```python
   def my_new_tool(param1, param2):
       # Tool logic
       return {"result": "success"}
   ```

2. **Add to handler:**
   ```python
   elif action == "my-new-tool":
       return my_new_tool(request.get("param1"), request.get("param2"))
   ```

3. **Update allowlist:**
   ```yaml
   agent-backend:
     tools:
       - my-new-tool  # Add here
   ```

4. **Test locally:**
   ```bash
   echo '{"action": "my-new-tool", "param1": "test"}' | python3 mcp-servers/validate-schema-server.py
   ```

---

## Creating a New MCP Server

1. **Create Python file** in `mcp-servers/`:
   ```python
   # mcp-servers/my-server.py
   # C-05
   """MCP Server: My Custom Tool"""
   import json
   import sys

   def handle_request(request):
       action = request.get("action", "")
       if action == "my-tool":
           return {"result": "tool executed"}
       return {"error": f"Unknown action: {action}"}

   def main():
       if len(sys.argv) > 1:
           request = json.loads(sys.argv[1])
       else:
           request = json.loads(sys.stdin.read())
       print(json.dumps(handle_request(request), indent=2))

   if __name__ == "__main__":
       main()
   ```

2. **Add to allowlist:**
   ```yaml
   my-server:
     tools: [my-tool]
   ```

3. **Reference in workflow** (optional):
   ```yaml
   - name: Use custom tool
     run: echo '{"action": "my-tool"}' | python3 mcp-servers/my-server.py
   ```

---

## Agent Memory Scope Filtering

The memory server filters content by agent scope:

```bash
# Backend agent only sees backend-related entries
echo '{"action": "read", "scope": "backend"}' | python3 mcp-servers/agent-memory-server.py
```

Memory entries format in `AGENTS_MEMORY.md`:
```markdown
## Architecture Decisions (scope: backend)
- Flask + SQLAlchemy for backend (2026-07-01)

## Frontend Patterns (scope: frontend)
- Bootstrap 5 for UI (2026-07-01)
```

---

## Best Practices

1. **Keep servers stateless** — no persistent state between calls
2. **Use structured output** — always return JSON
3. **Validate inputs** — check required fields exist
4. **Log errors** — include context for debugging
5. **One tool per action** — keep actions focused