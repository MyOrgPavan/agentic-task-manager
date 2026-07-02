# 03 — End-to-End Scenarios (S-01 through S-07)

Step-by-step instructions to run each validation scenario from the requirements.

---

## S-01: Full Lifecycle

**Scenario:** Issue → Plan PR → Plan Approved → Execute → CI Pass → Merge → Deploy Staging

### Prerequisites
- Repository configured per [01-repository-setup.md](01-repository-setup.md)
- At least one reviewer for main branch

### Steps

1. **Create Issue**
   ```bash
   gh issue create --title "Feature: Add task priority filter" \
     --body "Add GET /tasks?priority=high to filter tasks by priority"
   ```
   Note the issue number (e.g., `#42`)

2. **Trigger Plan Workflow**
   ```bash
   gh workflow run "Agent - Plan" \
     --field scope=backend \
     --field ticket_id=42 \
     --field command="Add priority filter to tasks endpoint"
   ```

3. **Review Plan PR**
   - Go to PRs, find "Plan: backend / 42"
   - Review the generated `plans/plan-42.md`
   - Add label: `plan-approved`

4. **Execute**
   ```bash
   gh workflow run "Agent - Backend" \
     --field ticket_id=42 \
     --field command="Implement GET /tasks?priority=filter"
   ```
   OR wait for `agent-execute.yml` to auto-trigger on the plan PR.

5. **Verify CI Passes**
   ```bash
   gh run list --workflow "CI" --branch "agent/backend/42"
   ```

6. **Merge**
   - Approve the execution PR
   - Merge to `main`

7. **Verify Staging Deploy**
   ```bash
   gh run list --workflow "Phase 3 - Auto-Deploy to Staging" --limit 1
   ```

### Expected Artifacts
- Plan PR with `plans/plan-42.md`
- Execution PR with code changes
- CI run logs (lint, typecheck, test)
- Staging deployment artifact

---

## S-02: Plan Rejection

**Scenario:** Plan PR → Reviewer Requests Changes → Agent Amends → Re-review → Approve

### Steps

1. **Create Plan PR** (same as S-01 steps 1-3)
2. **Request Changes**
   - On Plan PR, click **Files changed** → **Review changes**
   - Select **Request changes**
   - Comment: "Priority filter should also support comma-separated values"
3. **Agent Amends Plan**
   - Re-run `agent-plan.yml` with updated command:
   ```bash
   gh workflow run "Agent - Plan" \
     --field scope=backend \
     --field ticket_id=42 \
     --field command="Add priority filter (support comma-separated: priority=high,low)"
   ```
   - This updates the same branch and Plan PR
4. **Re-review & Approve**
   - Verify changes address feedback
   - Add `plan-approved` label

### Verification
- No code was written until plan was approved
- Plan PR shows revision history with amendments

---

## S-03: Conflict Resolution

**Scenario:** Two agents open overlapping PRs → Conflict detected → Escalation → Human resolves

### Steps

1. **Trigger Two Conflicting Agents**
   ```bash
   # Terminal 1 - Backend agent modifies routes/tasks.py
   gh workflow run "Agent - Backend" \
     --field ticket_id=100 \
     --field command="Add due_date filter to tasks"

   # Terminal 2 - Frontend agent modifies same file (unlikely but possible)
   gh workflow run "Agent - Frontend" \
     --field ticket_id=101 \
     --field command="Update task template for due dates"
   ```

2. **Conflict Detection Runs Automatically**
   - `conflict-detection.yml` triggers on both PRs
   - Runs `git merge --dry-run` to detect conflicts
   - If conflicts found, adds comment to PR

3. **Escalation After 3 Attempts**
   ```bash
   # Check for escalation issue
   gh issue list --label escalation
   ```

4. **Human Resolves**
   - Checkout conflicting branches locally
   - Resolve merge conflicts manually
   - Push resolution
   - Re-trigger agents if needed

### Verification
- Escalation issue created with context
- Conflict not silently overwritten

---

## S-04: Context Drift

**Scenario:** Agent starts → New requirement added → Drift detected → Agent adjusts

### Steps

1. **Start Agent Work**
   ```bash
   gh workflow run "Agent - Backend" \
     --field ticket_id=200 \
     --field command="Add task sorting by created_date"
   ```

2. **Add New Requirement to Issue**
   ```bash
   gh issue comment 200 --body "Also need sorting by updated_date"
   ```

3. **Drift Detection Triggers**
   - `drift-detection.yml` runs on PR
   - `scripts/drift-check.sh` compares PR changes vs plan
   - Detects: `updated_date` sorting not in original plan

4. **Agent Adjusts**
   - Drift report posted as PR comment
   - Re-run agent with updated command:
   ```bash
   gh workflow run "Agent - Backend" \
     --field ticket_id=200 \
     --field command="Add task sorting by created_date AND updated_date"
   ```

### Verification
- Drift report in PR comments
- Updated PR description reflects new scope
- CI re-runs after adjustment

---

## S-05: Autonomy Levels

**Scenario:** Same change at different risk levels → Different agent behavior

### Test Each Level

| Risk Level | File Pattern | Expected Behavior |
|------------|--------------|-------------------|
| Low | `backend/templates/*.html` | Auto-merge after CI (Phase 2) |
| Medium | `backend/routes/tasks.py` | Propose PR, human merges |
| High | `backend/models.py` | Requires CODEOWNERS + environment gate |
| Critical | `.github/workflows/*.yml` | Requires 2 approvals + env gate |

### Run Test

```bash
# Low risk - template change
gh workflow run "Agent - Frontend" \
  --field ticket_id=300 \
  --field command="Update task card styling"

# Medium risk - route change
gh workflow run "Agent - Backend" \
  --field ticket_id=301 \
  --field command="Add pagination to tasks list"

# High risk - schema change
gh workflow run "Agent - Database" \
  --field ticket_id=302 \
  --field command="Add priority enum to tasks"

# Critical risk - workflow change (manual PR required)
```

### Verify Behavior

- Low: PR gets `low-risk` label → Phase 2 auto-merges
- Medium: PR waits for human approval
- High: PR requires CODEOWNERS review
- Critical: Infrastructure ruleset blocks without 2 approvals

---

## S-06: Governance Enforcement

**Scenario:** Agent modifies `.github/workflows/` → Blocked by ruleset

### Steps

1. **Attempt Workflow Change**
   ```bash
   gh workflow run "Agent - Backend" \
     --field ticket_id=400 \
     --field command="Modify CI workflow to add new check"
   ```

2. **Observe Block**
   - Agent creates PR modifying `.github/workflows/ci.yml`
   - Ruleset `github-infrastructure-protection` triggers
   - Requires 2 approvals from `@core-maintainers`
   - Even if agent has write permissions, ruleset enforces review

3. **Verify Block**
   ```bash
   gh pr view <pr-number> --json mergeable,mergeStateStatus
   ```

### Expected
- PR cannot be merged without required reviews
- Ruleset enforcement is independent of agent permissions

---

## S-07: Failure → Recovery

**Scenario:** Agent introduces test failure → CI fails → Failure analysis → Retry → Escalation

### Steps

1. **Introduce Failure** (modify test to fail)
   ```bash
   # Temporarily break a test
   gh workflow run "Agent - Backend" \
     --field ticket_id=500 \
     --field command="Introduce bug: remove validation"
   ```

2. **CI Fails**
   - `ci.yml` runs on PR
   - `test` job fails
   - `failure-analysis.yml` triggers on CI failure

3. **Failure Analysis Creates Issue**
   ```bash
   gh issue list --label failure
   ```
   - Issue contains: run URL, branch, failure logs

4. **Bounded Retries (Max 3)**
   - Agent retries automatically up to 3 times
   - Each retry creates new workflow run

5. **Escalation After 3 Failures**
   ```bash
   gh issue list --label escalation
   ```
   - Escalation issue with context and resolution options

### Verify
- Failure issue created with artifacts
- Retry count tracked (max 3)
- Escalation with full context if still failing

---

## Running All Scenarios Sequentially

```bash
# Run all scenarios in order
./scripts/run-all-scenarios.sh
```

(Script not included - run each scenario manually per above)