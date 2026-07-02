# 02 — Agent Workflow Guide

How to trigger, monitor, and use each agent workflow in the SDLC.

## Workflow Overview

| Workflow | Purpose | Trigger | Scope |
|----------|---------|---------|-------|
| `agent-plan.yml` | Generate structured plan artifact | `issue_comment`, `workflow_dispatch` | All |
| `agent-execute.yml` | Execute approved plan | `pull_request` (label `plan-approved`) | All |
| `agent-backend.yml` | Backend code changes | `workflow_dispatch`, `workflow_run` (after DB) | `backend/` |
| `agent-frontend.yml` | Frontend/template changes | `workflow_dispatch` | `templates/`, `static/` |
| `agent-db.yml` | Schema/migrations | `workflow_dispatch` | `models.py`, migrations |
| `agent-integrator.yml` | Fan-in: merge backend+frontend | `workflow_run` (after backend+frontend) | Integration |
| `agent-audit.yml` | Read-only inspection | `workflow_dispatch` | All (read-only) |
| `agent-merger.yml` | Consume audit, merge PRs | `workflow_run` (after audit) | Merge |
| `conflict-detection.yml` | Detect merge conflicts | `pull_request` | All PRs |
| `drift-detection.yml` | Detect plan drift | `pull_request`, `workflow_dispatch` | All PRs |
| `resume-work.yml` | Resume from existing PR | `workflow_dispatch` | All |
| `failure-analysis.yml` | Analyze CI failures | `workflow_run` (CI failure) | CI |
| `memory-expiry.yml` | Prune old memory | `schedule` (weekly) | Memory |
| `governance-review.yml` | Monthly governance report | `schedule` (monthly) | Governance |

---

## Phase Workflows (Autonomy Levels)

| Workflow | Autonomy | Trigger |
|----------|----------|---------|
| `phase-1-pull-requests.yml` | Propose-only | `pull_request` |
| `phase-2-auto-merge.yml` | Auto-merge low risk | `pull_request` (label `low-risk`) |
| `phase-3-staging.yml` | Auto-deploy staging | `push` to `main` |
| `phase-4-production.yml` | Human-gated prod | `workflow_dispatch` |

---

## How to Trigger Workflows

### Via GitHub CLI

```bash
# Plan a new feature
gh workflow run "Agent - Plan" \
  --field scope=backend \
  --field ticket_id=123 \
  --field command="Add task filtering by status"

# Execute backend changes (after plan approved)
gh workflow run "Agent - Backend" \
  --field ticket_id=123 \
  --field command="Implement GET /tasks?status=filter"

# Trigger DB schema change
gh workflow run "Agent - Database" \
  --field ticket_id=123 \
  --field command="Add status index to tasks table"

# Resume work on existing PR
gh workflow run "Resume Work" \
  --field pr_number=456
```

### Via Issue Comments

Comment on any issue with `/plan backend 123 "Add feature"` to trigger `agent-plan.yml`:
```
@github-actions /plan backend 123 "Add task filtering by status"
```

(Requires GitHub App or Action that parses issue comments)

### Via GitHub Web UI

1. Go to **Actions** tab
2. Select workflow (e.g., "Agent - Plan")
3. Click **Run workflow**
4. Fill in inputs and click **Run workflow**

---

## Agent Plan Lifecycle (A-01, A-02, A-03)

```
1. TRIGGER: issue_comment or workflow_dispatch
   ↓
2. GENERATE PLAN: agent-plan.yml → generate-plan job (read-only)
   - Reads risk-classification.yml
   - Runs scripts/generate-plan.py
   - Uploads plan artifact
   ↓
3. PROPOSE PLAN: agent-plan.yml → propose-plan job (write)
   - Downloads plan artifact
   - Creates branch: agent/<scope>/<ticket-id>
   - Commits plan.md
   - Opens PR with label "plan"
   ↓
4. REVIEW: Human reviews plan PR
   - Request changes if needed
   - Add label "plan-approved" when satisfied
   ↓
5. EXECUTE: agent-execute.yml triggers on PR with "plan-approved"
   - Checks label exists
   - Runs implementation
   - Commits changes to same branch
   - CI runs (lint, typecheck, test)
   ↓
6. MERGE: Human merges PR after CI passes
   - All checks must pass
   - Required reviewers approve
```

---

## Monitoring Workflow Runs

```bash
# List recent runs for a workflow
gh run list --workflow "Agent - Backend" --limit 10

# View specific run details
gh run view <run-id> --log

# Watch live
gh run watch <run-id>
```

---

## Artifacts

Each workflow uploads artifacts. Download:

```bash
gh run download <run-id> --name <artifact-name>
```

Common artifacts:
- `plan-artifact` — generated plan markdown
- `backend-evidence` — backend execution logs
- `audit-report` — JSON audit report
- `drift-report` — drift detection results
- `failure-evidence` — CI failure logs

---

## MCP Allowlist

Agents can only use tools listed in `.github/mcp-allowlist.yml`:

```yaml
agent-backend:
  servers: [validate-schema-server, agent-memory-server]
  tools: [validate-schema, format-code, run-tests, read-memory, write-memory]

agent-frontend:
  servers: [agent-memory-server]
  tools: [format-code, read-memory]

agent-db:
  servers: [validate-schema-server, agent-memory-server]
  tools: [validate-schema, run-migrations, read-memory, write-memory]
```

To add a tool:
1. Add tool to MCP server
2. Update `.github/mcp-allowlist.yml`
3. Agent workflows automatically pick up changes