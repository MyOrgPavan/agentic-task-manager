# V-08, V-09, V-11, Deliverable 3
# Repository Settings — Rulesets, Environments, Branch Protection

This document describes the required GitHub repository settings for the Agentic Task Manager project. These settings must be configured in the GitHub UI (Settings > Rules > Rulesets, Settings > Environments, Settings > Branches).

---

## 1. Rulesets (V-08, F-04, F-05)

### Main Branch Ruleset

**Name:** `main-branch-protection`
**Target branches:** `main`
**Enforcement status:** Active

**Rules:**
- Restrict creations: ✅
- Restrict updates: ✅
- Restrict deletions: ✅
- Require a pull request before merging: ✅
  - Required approvals: 1
  - Dismiss stale pull request approvals when new commits are pushed: ✅
  - Require review from Code Owners: ✅
- Require status checks: ✅
  - Required checks: `lint`, `typecheck`, `test`
- Block force pushes: ✅

### GitHub Infrastructure Ruleset

**Name:** `github-infrastructure-protection`
**Target branches:** `main`
**Target paths:** `.github/**/*`
**Enforcement status:** Active

**Rules:**
- Require a pull request before merging: ✅
  - Required approvals: 2
  - Require review from Code Owners: ✅
- Restrict deletions: ✅

---

## 2. Environments (V-09, F-08, F-09)

### Production Environment

**Name:** `production`
**Required reviewers:** 1
**Deployment branch:** `main`
**Secret name:** `DATABASE_URL`

### Staging Environment

**Name:** `staging`
**Required reviewers:** 0
**Deployment branch:** `main`

---

## 3. Branch Protection (V-08, V-11, E-09)

- Default branch: `main`
- Require status checks before merging: ✅
  - `lint` (from ci.yml)
  - `typecheck` (from ci.yml)
  - `test` (from ci.yml)
- Require branches to be up to date: ✅
- Require conversation resolution: ✅

---

## 4. CODEOWNERS Enforcement (F-10, B-02)

See `.github/CODEOWNERS` for path-based ownership rules. The ruleset for `main` MUST require review from Code Owners for all protected paths.

---

## 5. Environment Protection Rules

### Production
- Required reviewers: 1 (at minimum)
- Wait timer: 0 minutes
- Deployment branches: `main`
- Secret: `DATABASE_URL` (production PostgreSQL connection string)
- Concurrency group: `phase4-production` (prevents overlapping deployments)

### Staging
- No required reviewers
- Deployment branches: `main`
