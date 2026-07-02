# Add a Refresh Button — Agentic SDLC Walkthrough

This guide walks through adding a **Refresh button** to the `/hello` page using the **Issue → Plan → PR → Review → Merge** lifecycle.

## Prerequisites

- GitHub CLI (`gh`) authenticated, or use `curl` with a token
- Write access to `MyOrgPavan/agentic-task-manager`
- Local clone of the repo

## Step 1: Create a GitHub Issue

```bash
curl -sL -X POST \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/issues \
  -d '{
    "title": "Add refresh button to Hello World page",
    "body": "Add a Refresh button to /hello that reloads the page.\n\n- [ ] Add button to backend/templates/hello.html\n- [ ] All tests must still pass"
  }'
```

Records the returned issue number (e.g., `#4`).

## Step 2: Create a Plan (Branch + Plan Artifact + Plan PR)

### 2a. Generate the plan artifact

```bash
python3 scripts/generate-plan.py \
  --scope frontend \
  --ticket 4 \
  --risk low
```

### 2b. Customize the plan file

Edit `plans/plan-4.md` to include:

```
## Files to Modify
- `backend/templates/hello.html` — add Refresh button

## Plan
1. Add a Bootstrap-styled Refresh button to `hello.html`
2. Verify all 30 tests pass
```

### 2c. Push plan branch and create Plan PR

```bash
git checkout -b agent/frontend/4
git add plans/plan-4.md
git commit -m "Plan: scope=frontend ticket=4"
git push origin agent/frontend/4

BODY=$(cat plans/plan-4.md)
curl -sL -X POST \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/pulls \
  -d "{
    \"title\": \"Plan: frontend / 4 - Add refresh button\",
    \"head\": \"agent/frontend/4\",
    \"base\": \"main\",
    \"body\": $(echo \"$BODY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))'),
    \"labels\": [\"plan\"]
  }"
```

## Step 3: Approve the Plan

```bash
# Add plan-approved label to the Plan PR (replace 4 with your PR number)
curl -sL -X POST \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/issues/4/labels \
  -d '{"labels":["plan-approved"]}'
```

> **Principle A-01 enforced:** No code is written until the plan is approved.

## Step 4: Implement the Code

### 4a. Switch to main and create implementation branch

```bash
git checkout main
git pull origin main
git checkout -b impl/frontend/4
```

### 4b. Add the Refresh button

Edit `backend/templates/hello.html` to add:

```html
{% extends "base.html" %}
{% block title %}Hello World{% endblock %}
{% block content %}
<div class="text-center mt-5">
    <h1>Hello, World!</h1>
    <p class="lead">Welcome to the Agentic Task Manager.</p>
    <button onclick="location.reload()" class="btn btn-primary mt-3">
        Refresh
    </button>
</div>
{% endblock %}
```

### 4c. Verify tests pass

```bash
.venv/bin/pytest
# Expect: 30 passed
```

### 4d. Push and create Implementation PR

```bash
git add -A
git commit -m "Add Refresh button to /hello page"
git push origin impl/frontend/4

curl -sL -X POST \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/pulls \
  -d '{
    "title": "Add Refresh button to Hello World page (Issue #4)",
    "head": "impl/frontend/4",
    "base": "main",
    "body": "Implements plan PR #5\n\nCloses #4\n\n## Changes\n- `backend/templates/hello.html` — added Refresh button",
    "maintainer_can_modify": true
  }'
```

## Step 5: CI Validates

CI (`ci.yml`) runs automatically on the PR:

| Check | What it does |
|-------|-------------|
| `lint` | `ruff check backend/ scripts/ mcp-servers/` |
| `typecheck` | `mypy backend/ scripts/ mcp-servers/ --ignore-missing-imports` |
| `test` | `pytest backend/tests/ -v` |

Monitor status:

```bash
curl -sL -H "Authorization: token ghp_yOUR_TOKEN" \
  "https://api.github.com/repos/MyOrgPavan/agentic-task-manager/commits/$(git rev-parse HEAD)/check-runs" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin)['check_runs']:
    print(r['name'], r['status'], r.get('conclusion'))
"
```

## Step 6: Merge to Main

```bash
# Squash merge the implementation PR (replace 6 with PR number)
curl -sL -X PUT \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/pulls/6/merge \
  -d '{
    "commit_title": "Add Refresh button to Hello World page",
    "merge_method": "squash"
  }'
```

## Step 7: Close the Issue

```bash
curl -sL -X PATCH \
  -H "Authorization: token ghp_yOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/issues/4 \
  -d '{"state":"closed"}'
```

## Step 8: Verify on Main

```bash
git checkout main
git pull origin main
.venv/bin/pytest  # 30 passed
```

Start the app and visit `http://localhost:5000/hello` — the Refresh button should appear and reload the page on click.

---

## Design Principles Demonstrated

| Principle | How it's applied |
|-----------|-----------------|
| **A-01** | Plan is created and approved before any code |
| **A-02** | Plan artifact is versioned (PR with labels) |
| **A-03** | Execution follows the approved plan |
| **A-05** | CI validates every PR before merge |
| **A-06** | Merge produces a durable commit on `main` |
| **V-08** | Branch-per-feature isolation |
| **F-11** | Operational checks run automatically |

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `workflow_dispatch` returns 422 | Ensure `name:` is the **first line** of the workflow YAML (comments after) |
| PR check `check-plan-approved` fails | Add `plan-approved` label to the Plan PR, not the Implementation PR |
| `ruff` lint fails on pre-existing code | Run `ruff check --fix` and commit; or set `pyproject.toml` line length to 120 |
