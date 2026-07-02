# Instructions for Agentic Task Manager SDLC

This folder contains step-by-step guides for using the Agentic Task Manager implementation in a real SDLC workflow.

## Available Guides

| File | Description | Audience |
|------|-------------|----------|
| [01-repository-setup.md](01-repository-setup.md) | Configure GitHub repository settings (rulesets, environments, branch protection) | Repository Admin |
| [02-agent-workflow-guide.md](02-agent-workflow-guide.md) | How to trigger and use each agent workflow | Developers, DevOps |
| [03-end-to-end-scenarios.md](03-end-to-end-scenarios.md) | Run the 7 validation scenarios (S-01 through S-07) | QA, Developers |
| [04-risk-classification.md](04-risk-classification.md) | Customize risk levels and autonomy behaviors | Security, Architecture |
| [05-mcp-server-usage.md](05-mcp-server-usage.md) | Use and extend MCP servers for agent tooling | Platform Engineers |
| [06-memory-management.md](06-memory-management.md) | Manage AGENTS_MEMORY.md and memory expiry | Project Leads |
| [07-local-development.md](07-local-development.md) | Run the web app locally with Docker | Developers |
| [08-troubleshooting.md](08-troubleshooting.md) | Common issues and resolutions | All |

## Quick Start

```bash
# 1. Clone and configure repository
git clone <your-repo>
cd agentic-task-manager

# 2. Set up GitHub settings (see 01-repository-setup.md)
# - Create rulesets for main branch
# - Create production environment with required reviewers
# - Enable branch protection

# 3. Run locally
docker-compose up

# 4. Trigger first agent workflow
gh workflow run "Agent - Plan" --field scope=backend --field ticket_id=001 --field command="Add user dashboard"
```

## Architecture Overview

```
Issue → agent-plan.yml (generates plan) → PR with plan label → Review → plan-approved label
  → agent-execute.yml (executes) → CI passes → Merge → phase-3-staging.yml (deploys)
```

The system implements **Plan → Act → Evaluate** lifecycle with GitHub as the control plane.