# Add a Refresh Button — Agentic SDLC Walkthrough

This guide walks through adding a **Refresh button** to the `/hello` page using a coding agent (opencode) that handles **planning, execution, and PR creation** automatically. The human only creates the issue and approves.

## Prerequisites

- GitHub token with `repo`, `issues:write`, `pull-requests:write`, `actions:write` scopes
- Write access to `MyOrgPavan/agentic-task-manager`
- opencode CLI installed

## Step 1: Create a GitHub Issue

Create an issue describing the feature. This is the only manual step.

```bash
curl -sL -X POST \
  -H "Authorization: token ghp_YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/issues \
  -d '{
    "title": "Add refresh button to Hello World page",
    "body": "Add a Refresh button to /hello that reloads the page."
  }'
```

Note the returned issue number (e.g., `#4`).

## Step 2: Tell the Coding Agent to Execute

The agent handles everything from here — planning, implementation, testing, and PRs.

```bash
opencode "Implement the refresh button described in issue #4.
Follow the full SDLC lifecycle:
1. Create a plan artifact in plans/plan-4.md
2. Create branch agent/frontend/4, commit the plan, push it, create a Plan PR with label 'plan'
3. Wait for plan approval (add 'plan-approved' label to the Plan PR)
4. Create branch impl/frontend/4, implement the button in backend/templates/hello.html, run tests, push, create an Implementation PR
5. Merge the Implementation PR to main
6. Close issue #4"
```

### What the agent does automatically:

| Phase | Agent action |
|-------|-------------|
| **Plan** | Runs `scripts/generate-plan.py`, customizes `plans/plan-4.md`, creates branch `agent/frontend/4`, commits plan, pushes, opens Plan PR with `plan` label |
| **Approve** | *(human adds `plan-approved` label to the Plan PR — see step 3)* |
| **Execute** | Creates branch `impl/frontend/4`, edits `backend/templates/hello.html`, runs `pytest`, commits, pushes, opens Implementation PR |
| **CI** | Waits for CI checks (test, lint, typecheck) to pass on the Implementation PR |
| **Merge** | Squash-merges the Implementation PR to `main` |
| **Close** | Closes issue #4 with a reference to the merge commit |

## Step 3: Approve the Plan

Once the agent creates the Plan PR, review it and add the `plan-approved` label:

```bash
curl -sL -X POST \
  -H "Authorization: token ghp_YOUR_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/MyOrgPavan/agentic-task-manager/issues/PLAN_PR_NUMBER/labels \
  -d '{"labels":["plan-approved"]}'
```

> **Principle A-01 enforced:** The agent does not write any code until the plan is approved.

## Step 4: Agent Executes & Opens Implementation PR

After detecting the `plan-approved` label, the agent:
1. Creates `impl/frontend/4` from `main`
2. Adds the Refresh button to `backend/templates/hello.html`
3. Runs `pytest` — verifies all 30 tests pass
4. Commits, pushes, creates an **Implementation PR** with body `Closes #4`
5. Monitors CI status

## Step 5: CI Validates

CI runs automatically on the Implementation PR (triggered by `pull_request` event in `ci.yml`):

| Check | Status |
|-------|--------|
| `test` | 30/30 passed ✅ |
| `lint` | `ruff check` passes ✅ |
| `typecheck` | `mypy` passes ✅ |

## Step 6: Agent Merges & Closes

Once CI passes, the agent squash-merges the PR to `main` and closes issue #4.

## Step 7: Verify

```bash
git checkout main && git pull
.venv/bin/pytest  # 30 passed
```

Browse to `http://localhost:5000/hello` — the Refresh button reloads the page on click.

---

## Design Principles Demonstrated

| Principle | How it's applied |
|-----------|-----------------|
| **A-01** | Plan gating — agent does not code until plan is approved |
| **A-02** | Plan is a durable artifact (committed to a branch, PR with labels) |
| **A-03** | Execution follows the approved plan scope |
| **A-05** | CI validates every PR before merge |
| **A-06** | Merge produces a permanent commit on `main` |
| **B-04** | Read-only plan phase (plan PR) gated from write phase (impl PR) |
| **V-08** | Branch-per-feature: `agent/frontend/N` for plan, `impl/frontend/N` for code |

## Single-Command Shortcut

Once the issue exists, run:

```bash
opencode "Implement issue #N following the full SDLC lifecycle: plan, plan PR, wait for approval, implement, implementation PR, merge, close."
```

The agent handles every step — planning, branching, coding, testing, PR creation, merging, and issue closure — with zero manual file edits.
