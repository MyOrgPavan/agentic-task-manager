#!/usr/bin/env python3
# E-01, E-03, C-05
"""MCP Server: Agent Memory - Read/write access to AGENTS_MEMORY.md, filtered by scope."""
import json
import os
import re
import sys
from typing import Any

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "..", ".github", "AGENTS_MEMORY.md")


def get_memory(scope: str | None = None) -> dict[str, Any]:
    if not os.path.exists(MEMORY_FILE):
        return {"error": "Memory file not found", "content": ""}

    with open(MEMORY_FILE) as f:
        content = f.read()

    if scope:
        sections = re.split(r"\n## ", content)
        filtered = [s for s in sections if scope.lower() in s.lower()]
        content = "\n## ".join(filtered) if filtered else f"No entries found for scope: {scope}"

    return {"scope": scope or "all", "content": content}


def write_memory(entry: str) -> dict[str, Any]:
    entry_line = f"\n- {entry} ({__import__('datetime').datetime.now().strftime('%Y-%m-%d')})\n"
    with open(MEMORY_FILE, "a") as f:
        f.write(entry_line)
    return {"status": "written", "entry": entry}


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action", "")
    scope = request.get("scope")

    if action == "read":
        return get_memory(scope)
    elif action == "write":
        entry = request.get("entry", "")
        if not entry:
            return {"error": "No entry provided"}
        return write_memory(entry)
    else:
        return {"error": f"Unknown action: {action}", "available_actions": ["read", "write"]}


def main():
    if len(sys.argv) > 1:
        request = json.loads(sys.argv[1])
    else:
        request = json.loads(sys.stdin.read())

    result = handle_request(request)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
