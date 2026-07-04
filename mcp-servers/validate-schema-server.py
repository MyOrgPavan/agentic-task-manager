#!/usr/bin/env python3
# C-05
"""MCP Server: Schema Validation - Validate database schema and code patterns."""
import json
import os
import re
import sys
from typing import Any


def validate_schema(schema_path: str | None = None) -> dict[str, Any]:
    if schema_path and not os.path.exists(schema_path):
        return {"valid": False, "errors": [f"File not found: {schema_path}"]}

    path = schema_path or os.path.join(os.path.dirname(__file__), "..", "backend", "models.py")
    if not os.path.exists(path):
        return {"valid": False, "errors": ["models.py not found"]}

    with open(path) as f:
        content = f.read()

    errors = []

    if "db.Column" not in content:
        errors.append("No db.Column definitions found")

    if "class User" not in content:
        errors.append("User model not found")

    if "class Project" not in content:
        errors.append("Project model not found")

    if "class Task" not in content:
        errors.append("Task model not found")

    if "class Comment" not in content:
        errors.append("Comment model not found")

    pk_count = len(re.findall(r"db\.Column\(db\.Integer,\s*primary_key=True\)", content))
    if pk_count < 4:
        errors.append(f"Expected at least 4 primary keys, found {pk_count}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "path": path,
        "model_count": len(re.findall(r"class \w+\(db\.Model\)", content)),
    }


def format_code(file_path: str) -> dict[str, Any]:
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    with open(file_path) as f:
        content = f.read()

    lines = content.split("\n")
    formatted = []
    for line in lines:
        stripped = line.rstrip()
        formatted.append(stripped)

    with open(file_path, "w") as f:
        f.write("\n".join(formatted) + "\n")

    return {
        "status": "formatted",
        "file": file_path,
        "original_lines": len(lines),
        "final_lines": len(formatted),
    }


def run_tests(test_path: str | None = None) -> dict[str, Any]:
    import subprocess

    path = test_path or os.path.join(os.path.dirname(__file__), "..")
    result = subprocess.run(
        ["python", "-m", "pytest", "-x", "--tb=short", path],
        capture_output=True,
        text=True,
        timeout=60,
    )
    return {
        "passed": result.returncode == 0,
        "returncode": result.returncode,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-2000:],
    }


def handle_request(request: dict[str, Any]) -> dict[str, Any]:
    action = request.get("action", "")

    if action == "validate-schema":
        return validate_schema(request.get("path"))
    elif action == "format-code":
        return format_code(request.get("path", ""))
    elif action == "run-tests":
        return run_tests(request.get("path"))
    else:
        return {
            "error": f"Unknown action: {action}",
            "available_actions": ["validate-schema", "format-code", "run-tests"],
        }


def main():
    if len(sys.argv) > 1:
        request = json.loads(sys.argv[1])
    else:
        request = json.loads(sys.stdin.read())

    result = handle_request(request)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
