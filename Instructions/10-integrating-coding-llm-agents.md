# Integrating Coding LLM Agents into the SDLC Workflow

## Design Document

Based on the 6-module "Developing in Agentic AI Systems" curriculum at `docs/` and the existing `agentic-task-manager` implementation.

---

## 1. Current State Analysis

### What exists today

| Component | Purpose | Status |
|-----------|---------|--------|
| 21 GitHub Actions workflows | Plan → Act → Evaluate lifecycle, multi-agent orchestration, phase gating | Deployed but workflows with `name:` after comments fail to parse |
| `agentic-workflow-processor.yml` | GitHub Agentic Workflow — parses markdown frontmatter, creates lock file, dispatches agent workflows | Working |
| `scripts/generate-plan.py` | Generates structured plan artifacts | Working |
| `AGENTS_MEMORY.md` | Long-term memory scoped by regex section | Working |
| `mcp-servers/` | MCP servers for memory and schema validation | Working |
| `Instructions/` | 9 markdown guides for SDLC procedures | Working |

### What's missing

| Gap | Impact |
|-----|--------|
| No direct LLM agent invocation from workflows | `agent-frontend.yml` has placeholder `echo` steps — no actual code generation |
| No agent affinity / routing | Workflows use static scope mapping, no dynamic LLM routing |
| No agent output evaluation | Plans are generated but no LLM-based quality check on agent output |
| No tool registry for agents | MCP allowlist exists but disconnected from agent workflow execution |
| No ephemeral agent state | Memory is only long-term (`AGENTS_MEMORY.md`); no per-task short-term memory |
| No agent feedback loop | Failed checks don't feed back to the agent for self-correction |

---

## 2. Architectural Model

```
┌──────────────────────────────────────────────────────────┐
│                    GitHub (Control Plane)                  │
│                                                          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐            │
│  │  Issues  │──▶│  Plans   │──▶│    PRs   │            │
│  └──────────┘   └──────────┘   └──────────┘            │
│       │              │              │                    │
│       ▼              ▼              ▼                    │
│  ┌─────────────────────────────────────────────┐        │
│  │         GitHub Actions (Orchestrator)        │        │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐    │        │
│  │  │  Plan    │ │ Execute  │ │ Evaluate │    │        │
│  │  │ Workflow │ │ Workflow │ │ Workflow │    │        │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘    │        │
│  └───────┼────────────┼────────────┼──────────┘        │
│          │            │            │                    │
└──────────┼────────────┼────────────┼────────────────────┘
           │            │            │
           ▼            ▼            ▼
     ┌─────────────────────────────────────┐
     │       Coding LLM Agent Layer        │
     │                                     │
     │  ┌─────────────────────────────┐   │
     │  │     opencode / Copilot      │   │
     │  │  (Plan, Code, Test, Fix)    │   │
     │  └────────────┬────────────────┘   │
     │               │                    │
     │  ┌────────────┴────────────────┐   │
     │  │      MCP Server Layer       │   │
     │  │  ┌──────┐ ┌──────┐ ┌────┐  │   │
     │  │  │Memory│ │Schema│ │Git │  │   │
     │  │  │ MCP  │ │ MCP  │ │ MCP│  │   │
     │  │  └──────┘ └──────┘ └────┘  │   │
     │  └─────────────────────────────┘   │
     └─────────────────────────────────────┘
```

### Key Design Decisions

1. **GitHub is the control plane** — all agent actions are triggered by and recorded in GitHub. No external infra.
2. **Workflows orchestrate; agents execute** — workflows handle sequencing, permissions, gates. Agents handle generation.
3. **MCP servers provide tools** — agents access memory, validation, and git operations through MCP.
4. **PRs are the audit trail** — every plan and every change goes through a PR for review and traceability.

---

## 3. Integration Points

### 3.1 Issue → Agent Trigger

**When:** Issue is created or labeled `agent-ready`

**Flow:**
1. `issue_comment` or `issues` event triggers `agent-plan.yml`
2. Workflow reads issue body, extracts scope/command
3. Workflow invokes the coding agent via `opencode` CLI or Copilot API
4. Agent generates plan artifact and pushes Plan PR

**YAML snippet:**
```yaml
on:
  issues:
    types: [opened, labeled]
jobs:
  trigger-agent:
    if: contains(github.event.issue.labels.*.name, 'agent-ready')
    steps:
      - run: |
          opencode "Implement issue #${{ github.event.issue.number }}"
```

### 3.2 Plan Phase → Agent Generates Plan

**When:** `agent-plan.yml` dispatches or agent is invoked directly

**Flow:**
1. Agent receives issue, scope, and risk level
2. Agent reads repository context (codebase, existing plans, AGENTS_MEMORY.md)
3. Agent generates `plans/plan-<ticket>.md` with:
   - Success criteria
   - Files to modify with line-level detail
   - Implementation steps
   - Rollback strategy
4. Agent commits plan to branch `agent/<scope>/<ticket>`
5. Agent opens Plan PR with `plan` label
6. Agent adds traceability comments to the plan referencing issue and requirements

**Agent prompt template:**
```
You are a coding agent following the Plan → Act → Evaluate lifecycle.
Your current phase is PLAN (read-only). You may NOT write any code.

Issue: #{ticket}
Scope: {scope}
Risk: {risk}

Read the repository context, then generate a plan at plans/plan-{ticket}.md
with: success criteria, files to modify, implementation steps, rollback strategy.
```

### 3.3 Plan Approval → Agent Detects Gate

**When:** `plan-approved` label added to Plan PR

**Flow:**
1. `pull_request` event with `labeled` triggers agent execution
2. Workflow checks label is `plan-approved`
3. Workflow invokes agent with execution command
4. Agent reads the approved plan, creates implementation branch

**YAML snippet:**
```yaml
on:
  pull_request:
    types: [labeled]
jobs:
  check-and-execute:
    if: contains(github.event.pull_request.labels.*.name, 'plan-approved')
    steps:
      - run: |
          opencode "Execute the approved plan at plans/plan-$TICKET.md"
```

### 3.4 Execution Phase → Agent Implements

**When:** Plan is approved, execution branch is created

**Flow:**
1. Agent checks out `impl/<scope>/<ticket>` from `main`
2. Agent reads the approved plan artifact
3. Agent makes changes per plan (files, tests, templates)
4. Agent runs `pytest` to verify
5. Agent runs `ruff check` to lint
6. If failures, agent self-corrects and retries (up to 3 attempts)
7. Agent commits and pushes
8. Agent opens Implementation PR referencing the plan PR and issue

**Self-correction loop:**
```
┌────────────┐    ┌────────────┐    ┌────────────┐
│  Implement │───▶│  Test &    │───▶│   Pass?    │
│  Changes   │    │  Validate  │    │            │
└────────────┘    └────────────┘    └─────┬──────┘
         ▲                                │
         │  ┌────────────┐               │
         └──│  Fix &     │◀──────────────┘
            │  Retry (3x)│  No
            └────────────┘
                          │ Yes
                          ▼
                   ┌────────────┐
                   │  Open PR   │
                   └────────────┘
```

### 3.5 CI Evaluation → Agent Responds

**When:** CI checks complete on Implementation PR

**Flow:**
1. `check_run` or `workflow_run` event fires with CI results
2. If any check fails, agent is re-invoked to fix
3. Agent reads failure logs, identifies root cause, pushes fix
4. CI re-runs automatically
5. After max retries, agent escalates (adds `needs-human` label)

**YAML snippet:**
```yaml
on:
  workflow_run:
    workflows: [CI]
    types: [completed]
jobs:
  evaluate-and-fix:
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - run: |
          opencode "Fix CI failures in PR #$PR_NUMBER"
```

### 3.6 Merge → Agent or Human Closes

**When:** All CI checks pass and review is approved

**Flow:**
1. `agent-merger.yml` detects passing checks + required approvals
2. Workflow squash-merges the Implementation PR
3. Agent closes the issue with reference to merge commit
4. Agent updates `AGENTS_MEMORY.md` with outcome

---

## 4. Multi-Agent Coordination

### Agent Routing

| Trigger | Agent | Scope | Autonomy |
|---------|-------|-------|----------|
| Issue labeled `backend` | opencode (backend) | `backend/` | After plan approval |
| Issue labeled `frontend` | opencode (frontend) | `backend/templates/`, `backend/static/` | After plan approval |
| Issue labeled `db` | opencode (db) | `backend/models.py`, `migrations/` | After plan approval |
| Issue labeled `docs` | opencode (docs) | `Instructions/`, `*.md` | Low — auto-approve |
| Issue labeled `infra` | opencode (infra) | `.github/`, `Dockerfile` | High — requires human merge |

### Conflict Prevention

```yaml
# File: .github/workflows/conflict-detection.yml
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - run: opencode "Check if PR #${{ github.event.pull_request.number }} conflicts with open PRs #$(gh pr list --state open --json number --jq '.[].number' | tr '\n' ',')"
```

### Fan-Out / Fan-In Pattern

```
         ┌──────────┐
         │  Issue   │
         │  #42     │
         └────┬─────┘
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
 ┌────────┐┌────────┐┌────────┐
 │ Agent  ││ Agent  ││ Agent  │
 │ Backend││Frontend││   DB   │
 └───┬────┘└───┬────┘└───┬────┘
     │        │        │
     └────────┼────────┘
              ▼
     ┌────────────────┐
     │   Integrator   │
     │  (merge plans  │
     │   & PRs)       │
     └────────────────┘
```

---

## 5. Tool Access via MCP Servers

| MCP Server | Tool | Access Level | Used By |
|------------|------|-------------|---------|
| `agent-memory-server.py` | `read_memory`, `write_memory`, `search_memory` | Read/Write | All agents |
| `validate-schema-server.py` | `validate_schema`, `format_lint` | Read | Plan phase |
| `git-mcp` (future) | `create_branch`, `commit`, `push`, `create_pr` | Write | Execute phase |
| `test-mcp` (future) | `run_tests`, `run_lint` | Read | Execute phase |
| `github-mcp` (future) | `read_issue`, `read_pr`, `list_workflows`, `trigger_workflow` | Read/Write | Orchestrator |

**Tool gating by phase:**

```
         PLAN PHASE          EXECUTION PHASE         EVALUATION PHASE
    ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
    │ read_memory     │  │ create_branch   │  │ run_tests       │
    │ search_files    │  │ write_files     │  │ read_ci_logs    │
    │ validate_schema │  │ commit          │  │ read_memory     │
    │ read_issue      │  │ push            │  │ write_memory    │
    │ NO WRITE TOOLS  │  │ create_pr       │  │ escalate        │
    └─────────────────┘  └─────────────────┘  └─────────────────┘
```

**MCP allowlist (`mcp-allowlist.yml`):**
```yaml
# Phase-based tool gating
plan:
  tools:
    - read_file, search_files, read_memory, validate_schema
  allow_write: false
execute:
  tools:
    - write_file, create_branch, commit, push, create_pr, run_tests
  allow_write: true
  retry_limit: 3
evaluate:
  tools:
    - read_ci_logs, read_memory, write_memory, add_label
  allow_write: true
  allowed_labels:
    - needs-human
    - agent-escalated
```

---

## 6. Memory Architecture

```yaml
# Memory scoping per agent interaction
memory:
  short_term:
    storage: workflow artifacts (plan-<ticket>.md)
    scope: single agent execution
    ttl: until merge
  long_term:
    storage: AGENTS_MEMORY.md (section-scoped by regex)
    scope: project-wide
    ttl: permanent
  external:
    storage: MCP memory server (agent-memory-server.py)
    scope: cross-session agent context
    ttl: configurable (default 30 days)
```

### Memory enrichment flow:
1. **Before execution:** Agent reads `AGENTS_MEMORY.md` + issue comments + plan
2. **During execution:** Agent writes decisions to short-term artifact
3. **After merge:** Agent summarizes outcome → appends to `AGENTS_MEMORY.md`
4. **Periodic:** `memory-expiry.yml` prunes stale entries

---

## 7. Agent Prompt Hierarchy

Each agent invocation includes layered context:

```
SYSTEM: You are a {role} agent. Follow Plan→Act→Evaluate lifecycle.
        Current phase: {phase}. {restrictions}

REPOSITORY: {key architectural decisions from AGENTS_MEMORY.md}
            {file tree overview}
            {coding conventions}

TASK: Issue #{number}: {title}
      Scope: {scope} | Risk: {risk}
      Plan artifact: plans/plan-{ticket}.md

TOOLS: Available: {mcp_tools}
       Blocked: {blocked_tools}

CONSTRAINTS: {phase-specific rules, e.g., "read-only during plan"}
```

---

## 8. Governance & Guardrails

| Control | Mechanism | Enforced At |
|---------|-----------|-------------|
| No direct-to-main writes | Branch protection + rulesets | Repository level |
| Plan required before code | `check-plan-approved` job in agent workflows | Workflow level |
| Risk-based autonomy | `risk-classification.yml` gates merge method | Workflow level |
| Least-privilege tokens | `permissions:` block per job | Workflow level |
| Max retries | Loop counter, escalation at 3 failures | Agent level |
| Observable artifacts | Every step produces PR, artifact, or commit | Architecture level |
| Agent attribution | PR labels (`agent: {name}`), branch naming | Convention level |
| Audit trail | `agent-audit.yml` periodic review | Schedule level |

---

## 9. Implementation Roadmap

| Phase | What | Depends On |
|-------|------|------------|
| **P1** | Fix workflow YAML parsing (name first) | None |
| **P2** | Add `opencode` CLI invocation to agent workflows | opencode installed on runner |
| **P3** | Replace placeholder echo steps with real agent prompts | P2 |
| **P4** | Implement self-correction loop (CI failure → agent re-invoke) | P3 |
| **P5** | Connect MCP servers to agent runtime | P3 |
| **P6** | Dynamic agent routing from issue labels | P2 |
| **P7** | Fan-out/fan-in for multi-file changes | P6 |
| **P8** | Memory enrichment flow (auto-update AGENTS_MEMORY.md) | P5 |

---

## 10. Quick-Start: Add opencode to a Workflow

To integrate `opencode` into any existing agent workflow:

```yaml
steps:
  - name: Install opencode
    run: npm install -g @opencode/cli
  - name: Invoke coding agent
    env:
      OPENCODE_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    run: |
      opencode "Issue #${{ github.event.inputs.ticket_id }}: ${{ github.event.inputs.command }}
      Scope: ${{ github.event.inputs.scope }}
      Risk: low
      Phase: execute"
```

This single step replaces all manual `echo` + `git commit` + `gh pr create` steps in the existing agent workflows.

---

## References

- `docs/module-01-foundations-of-agentic-ai/` — Plan → Act → Evaluate lifecycle
- `docs/module-02-designing-agent-architecture/` — PR-based governance, separation of planning/execution
- `docs/module-03-tooling-mcp-execution-environments/` — MCP servers, execution boundaries, GitHub Agentic Workflows
- `docs/module-04-multi-agent-orchestration/` — Sequential/parallel orchestration, conflict detection
- `docs/module-05-memory-state-evaluation/` — Short/long-term memory, evaluation signals
- `docs/module-06-governance-guardrails-operations/` — Risk-based autonomy, least-privilege, audit
