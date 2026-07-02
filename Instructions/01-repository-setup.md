# 01 — Repository Setup

Configure the GitHub repository to enforce all governance rules. These settings must be applied via the GitHub UI (Settings > Rules > Rulesets, Settings > Environments, Settings > Branches).

## Prerequisites

- Repository admin access
- GitHub CLI (`gh`) installed and authenticated

---

## 1. Branch Protection & Rulesets

### Main Branch Ruleset

1. Go to **Settings > Rules > Rulesets** → **New ruleset**
2. Name: `main-branch-protection`
3. Target: `main` branch
4. Enable:
   - ✅ Restrict creations
   - ✅ Restrict updates
   - ✅ Restrict deletions
   - ✅ Require a pull request before merging
     - Required approvals: **1**
     - Dismiss stale approvals on new commits: ✅
     - Require review from Code Owners: ✅
   - ✅ Require status checks
     - Required checks: `lint`, `typecheck`, `test`
   - ✅ Block force pushes

### GitHub Infrastructure Ruleset (Critical)

1. Go to **Settings > Rules > Rulesets** → **New ruleset**
2. Name: `github-infrastructure-protection`
3. Target: `main` branch + **paths: `.github/**`**
4. Enable:
   - ✅ Require a pull request before merging
     - Required approvals: **2**
     - Require review from Code Owners: ✅
   - ✅ Restrict deletions

---

## 2. Environments

### Production Environment

1. Go to **Settings > Environments** → **New environment**
2. Name: `production`
3. Required reviewers: **1** (add team or users)
4. Deployment branch: `main`
5. Add secret: `DATABASE_URL` (production PostgreSQL connection string)
5. Concurrency group: `phase4-production`

### Staging Environment

1. Go to **Settings > Environments** → **New environment**
2. Name: `staging`
3. Required reviewers: **0**
4. Deployment branch: `main`

---

## 3. CODEOWNERS Enforcement

The `.github/CODEOWNERS` file is already in the repo. It defines:
- `@core-maintainers` for `.github/`, `backend/models.py`, `requirements.txt`
- `@agent-backend` for `backend/`
- `@agent-frontend` for `backend/templates/`, `backend/static/`

Ensure the **@core-maintainers team exists** in your GitHub organization.

---

## 4. Branch Protection (Legacy)

If not using rulesets, also configure at **Settings > Branches**:
- Require status checks: `lint`, `typecheck`, `test`
- Require branches to be up to date
- Require conversation resolution

---

## 5. Verification

After setup, verify:

```bash
# Check branch protection
gh api repos/{owner}/{repo}/branches/main/protection

# Check environments
gh api repos/{owner}/{repo}/environments

# Check rulesets
gh api repos/{owner}/{repo}/rulesets
```

---

## 6. Required GitHub Actions Permissions

Ensure the default `GITHUB_TOKEN` has:
- `contents: read`
- `pull-requests: write`
- `issues: read` (for memory expiry workflow)
- `deployments: write` (for staging/production workflows)

These are configured per-workflow in the YAML files.