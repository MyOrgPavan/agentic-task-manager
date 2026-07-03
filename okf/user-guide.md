---
type: Architecture
title: User Guide — Issue to Merge via opencode
description: Step-by-step instructions for triggering the full Plan-Act-Process lifecycle by creating a GitHub Issue.
tags: [guide, workflow, issue, opencode]
timestamp: "2026-07-03T09:45:00Z"
---

# User Guide — From Issue to Merged Code

This guide walks through the complete lifecycle: create a GitHub Issue → opencode plans → you approve → opencode implements → merge → deploy to Docker on localhost:8080.

## Step 1: Create a GitHub Issue

Go to your repository's **Issues** tab and click **New Issue**.

**Title:** Clear description of what you want
  ```
  Add a footer with copyright to base.html
  ```

**Body:** Describe the change in plain English
  ```
  Add a sticky footer to the bottom of every page that says:
  "© 2026 Task Manager. All rights reserved."
  ```

**Labels:** Add exactly one scope label. This determines which agent handles the work:

  | Label | Agent Scope | Example |
  |-------|-------------|---------|
  | `frontend` | HTML templates, CSS | Add a footer, change nav bar |
  | `backend` | Flask routes, app logic | New API endpoint |
  | `db` | Database models, migrations | Add a column to a table |
  | `docs` | Documentation | Update README |
  | `infra` | CI/CD, configs | Update Dockerfile |
  | `deploy` | Docker, deployment | Deploy main to production |

Click **Submit new issue**.

## Step 2: Wait for the Plan PR

Within ~1–2 minutes, the `Agent - Plan` workflow will:
1. Detect the new issue with a scope label
2. Run opencode (read-only) to study the codebase
3. Generate `plans/plan-<issue-number>.md`
4. Open a **Plan PR** — title starts with `Plan:`

**Example Plan PR:** `Plan: scope=frontend ticket=19`

## Step 3: Review the Plan

Open the Plan PR. The PR body contains the full plan:

```
## Scope
frontend

## Ticket / Issue
#19

## Risk Level
low

## Description
Add a sticky footer with copyright text to all pages.

## Success Criteria
- [ ] Footer appears on every page
- [ ] Footer sticks to bottom (not floating)
- [ ] Copyright text matches the description

## Files to Modify
- `backend/templates/base.html` — add footer HTML
- `backend/static/style.css` — add sticky footer CSS

## Implementation Steps
1. Add `<footer>` block before closing `</body>` in base.html
2. Add CSS for sticky footer layout
```

**Verify:** Does the plan look correct? Are the right files listed? Is the approach sound?

## Step 4: Approve the Plan

If the plan looks good, add the **`plan-approved`** label to the Plan PR:

```
gh pr edit <plan-pr-number> --add-label plan-approved
```

Or via the GitHub UI: Labels → `plan-approved`.

This triggers the `Agent - Execute` workflow.

## Step 5: Wait for the Implementation PR

The Execute workflow will:
1. Checkout the plan branch
2. Install opencode
3. Run opencode to implement every step in the plan
4. Run `pytest` to verify tests pass
5. Push changes to `impl/<scope>/<issue-number>`
6. Open an **Implementation PR**

**Example Impl PR:** `Implement: backend / #19`

## Step 6: Review & Merge the Implementation PR

Open the Implementation PR. Verify:
- The changes match the plan
- All CI checks pass (lint, typecheck, test)
- The diff looks clean

If everything looks good, **merge the PR** into `main`.

## Step 7: Automatic Staging Deploy

Once merged to `main`, the **Phase 3 - Auto-Deploy to Staging** workflow runs automatically:

1. Runs lint, typecheck, and tests
2. Builds the Docker image for the `staging` service
3. Stops any existing `task-manager-staging` container
4. Starts the new container on **port 8080**
5. Runs a health check against `http://localhost:8080/`

The staging URL is: `http://localhost:8080`

## Step 8: Deploy to Production

When you're ready to release to production:

### Option A: Create a Deployment Issue

Create a GitHub Issue with label `deploy`:

**Title:**
  ```
  Deploy main to production
  ```

**Labels:** `deploy`

The router will trigger **Phase 4 - Production (Environment Gate)**.

### Option B: Manual Workflow Dispatch

Go to **Actions** → **Phase 4 - Production (Environment Gate)** → **Run workflow** → select `main` as the ref.

### Approval Gate

The production environment requires **1 human reviewer**. The deployment will pause and wait for approval:

1. A reviewer is notified (GitHub Environment protection rule)
2. Reviewer inspects the changes (all merged PRs since last deploy)
3. Reviewer **approves** the deployment in the GitHub UI
4. The workflow resumes and deploys:

```
docker compose build production
docker compose up -d production    → container on :8080
curl http://localhost:8080/         → health check
```

The production URL is: `http://localhost:8080`

**Note:** Since staging and production run on the same machine on the same port, only one can run at a time. The deploy workflow stops the previous container before starting the new one.

## Troubleshooting

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| No Plan PR after 5 min | Missing or wrong label | Add a valid scope label to the issue |
| Plan PR has `plan-approved` but no Impl PR | Workflow failed | Check Actions tab for `Agent - Execute` logs |
| Impl PR CI fails | Plan was incomplete | Fix manually or create a new issue |
| opencode didn't modify all files | Plan steps unclear | Be more specific in the issue description |
| Staging deploy not running | Phase 3 only triggers on push to main | Merge the Impl PR first |
| Production deploy hangs at "waiting for approval" | Environment requires reviewer | Check your GitHub notifications and approve |
| Container fails to start on :8080 | Port already in use | Stop the old container first (handled automatically) |
| Health check fails after deploy | App didn't start in time | Check docker logs: `docker logs task-manager-prod` |

## Alternative Entry Point: Intent Files

Instead of an Issue, you can push an intent file:

```bash
cat > agent-intents/42-add-footer.md << 'EOF'
---
scope: backend
ticket: "42"
risk: low
command: "Add a health check endpoint at /health"
---
EOF

git add agent-intents/42-add-footer.md
git commit -m "intent: add health check endpoint"
git push origin main
```

The router processes intent files the same way as Issues.

## See Also

- [okf/workflows/agentic-router](../workflows/agentic-router.md)
- [okf/workflows/agent-plan](../workflows/agent-plan.md)
- [okf/workflows/agent-execute](../workflows/agent-execute.md)
- [okf/workflows/phases](../workflows/phases.md)
- [okf/patterns/lifecycle](../patterns/lifecycle.md)
- [okf/agents/overview](../agents/overview.md)
- [.github/workflows/phase-4-production.yml](../../.github/workflows/phase-4-production.yml)
- [.github/workflows/phase-3-staging.yml](../../.github/workflows/phase-3-staging.yml)
