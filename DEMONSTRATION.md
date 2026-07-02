# Demonstration Guide — Agentic Task Manager

This document provides step-by-step instructions to run each end-to-end scenario (S-01 through S-07).

---

## S-01: Full Lifecycle

**Scenario:** Issue created -> agent drafts plan PR -> plan approved -> agent executes -> CI passes -> PR merged -> deployed to staging.

### Steps:
1. Create a GitHub Issue describing a new feature (e.g., "Add task filtering by status").
2. Run `agent-plan.yml` workflow via `workflow_dispatch` with scope and ticket ID.
3. Agent creates a branch `agent/<scope>/<ticket-id>` and opens a Plan PR.
4. Review the Plan PR, add label `plan-approved`.
5. Run `agent-execute.yml` with the PR number.
6. Execution workflow runs CI checks automatically via `ci.yml`.
7. Once CI passes, merge the execution PR.
8. Push to `main` triggers `phase-3-staging.yml`, deploying to staging.

**Expected:** Every step leaves a durable artifact in GitHub (PRs, workflow logs, artifacts).

---

## S-02: Plan Rejection

**Scenario:** Agent creates plan PR -> reviewer requests changes -> agent amends plan -> re-review -> approved -> execution proceeds.

### Steps:
1. Run `agent-plan.yml` to create a Plan PR.
2. Review and request changes via PR review comments.
3. Agent amends the plan and pushes updates to the same branch.
4. Re-review and approve.
5. Add `plan-approved` label.
6. Run `agent-execute.yml`.

**Expected:** No code is written until the plan is approved.

---

## S-03: Conflict Resolution

**Scenario:** Two agents open overlapping PRs -> conflict detection identifies -> escalation issue created -> human resolves.

### Steps:
1. Run `agent-backend.yml` and `agent-frontend.yml` targeting overlapping files.
2. Both create separate PRs.
3. `conflict-detection.yml` runs on each PR, detecting merge conflicts.
4. After 3 failed merge attempts, an escalation issue is created.
5. Human reviews and resolves the conflict.

**Expected:** Conflict is detected and escalated, not silently overwritten.

---

## S-04: Context Drift

**Scenario:** Agent starts work -> new requirement added to issue -> drift detection catches divergence -> agent adjusts.

### Steps:
1. Run an agent workflow to start work on a feature.
2. Add new requirements to the original issue.
3. `drift-detection.yml` runs on the PR, comparing changes against the plan.
4. Drift report is added as a PR comment.
5. Agent updates the PR description and re-runs checks.

**Expected:** Drift is detected and corrected with evidence in the PR.

---

## S-05: Autonomy Levels

**Scenario:** Same change requested at different risk levels -> agent behavior differs.

### Steps:
1. Create a low-risk change (e.g., template change) -> `phase-2-auto-merge.yml` auto-merges after CI.
2. Create a medium-risk change (e.g., route change) -> agent proposes via PR, human merges.
3. Create a high-risk change (e.g., schema change) -> `phase-4-production.yml` requires environment approval.
4. Run `agent-audit.yml` with `contents: read` only -> read-only inspection.

**Expected:** Risk classification drives autonomy level.

---

## S-06: Governance Enforcement

**Scenario:** Agent attempts to modify `.github/workflows/` without CODEOWNERS approval -> PR is blocked.

### Steps:
1. Run `agent-backend.yml` targeting a file in `.github/workflows/`.
2. Agent creates a PR.
3. Rulesets enforce CODEOWNERS review for `.github/` paths.
4. PR cannot be merged without approval from `@core-maintainers`.

**Expected:** Rulesets prevent the merge regardless of agent's permissions.

---

## S-07: Failure -> Recovery

**Scenario:** Agent's change introduces test failure -> CI fails -> failure analysis creates Issue -> retried -> escalation.

### Steps:
1. Run an agent that introduces a code change.
2. `ci.yml` fails with test errors.
3. `failure-analysis.yml` detects the CI failure and creates a GitHub Issue.
4. Agent is retried (up to 3 times) via bounded retries.
5. If still failing, `conflict-detection.yml` creates an escalation issue.

**Expected:** Failures are analyzed, artifacted, and escalated — not lost.

---

## Running the Web App Locally

### Prerequisites
- Python 3.11+
- Docker and Docker Compose (optional)

### Using Docker
```bash
cp .env.example .env
docker-compose up
```

Open http://localhost:5000

### Without Docker
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask run
```

Open http://localhost:5000

### Running Tests
```bash
pip install -r requirements.txt
pytest backend/tests/ -v
```
