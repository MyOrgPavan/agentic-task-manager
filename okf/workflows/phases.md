---
type: Workflow
title: Progressive Autonomy Phases
description: Four deployment phases with increasing autonomy levels for risk-based change management.
tags: [workflow, phases, autonomy, deployment]
timestamp: "2026-07-03T09:45:00Z"
---

# Progressive Autonomy Phases

## Phase 1 — Pull Requests Only

**Trigger:** PR opened

Behavior: All changes require a pull request. No auto-merge. Human must review and merge.

## Phase 2 — Auto-Merge Low Risk

**Trigger:** PR labeled `low-risk`

Behavior: After CI passes, the PR is auto-merged without human review. Risk classification determines eligibility.

## Phase 3 — Staging Deploy

**Trigger:** Push to main

Behavior: On every merge to main, the staging environment is automatically deployed. No manual approval needed.

## Phase 4 — Production Deploy

**Trigger:** `workflow_dispatch`

Behavior: Production deployment requires manual workflow dispatch and environment approval. Gated by GitHub Environments.

## Autonomy Mapping

| Risk Level | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|-----------|---------|---------|---------|---------|
| Critical | Required | — | — | Human-gated |
| High | Required | — | Auto | Human-gated |
| Medium | Required | — | Auto | Human-gated |
| Low | — | Auto | Auto | Human-gated |

## See Also

- [/governance/risk-classification](/governance/risk-classification.md)
- [/patterns/phase-gating](/patterns/phase-gating.md)
- [/governance/repository-settings](/governance/repository-settings.md)
