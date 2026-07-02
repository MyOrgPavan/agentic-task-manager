# 08 — Troubleshooting

Common issues and their solutions for the Agentic Task Manager.

---

## CI Failures

### "pip install -r requirements.txt" fails

**Symptom:**
```
ERROR: Could not find a version that satisfies the requirement Flask==3.1.0
```

**Solution:**
1. Update `requirements.txt` to compatible versions (e.g., use Flask 3.0.3)
2. Use virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install with `--upgrade`: `pip install --upgrade -r requirements.txt`

---

### "ruff check" fails

**Symptom:** Style or linting errors

**Solution:**
```bash
# Auto-fix
git diff --cached | head -20
ruff check --fix backend/
git add backend/
```

Check fixed issues: `ruff check backend/`

---

### "mypy" shows many errors

**Solution:**
1. Ignore specific modules: `mypy backend/ --ignore-missing-imports`
2. Check `pyproject.toml` and adjust type-check settings
3. Run mypy on individual files: `mypy backend/app.py`

---

## Agent Workflows

### "agent-plan.yml" doesn't trigger

**Check:**
- Workflow trigger is `issue_comment` or `workflow_dispatch`
- GitHub token has `pull-requests: write` permissions
- Repository has secret named `GH_TOKEN`

**Fix:**
```yaml
# In agent-plan.yml
permissions:
  contents: read
  pull-requests: write
  issues: read
```

### "Plan not approved" error

**Check:** PR has label `plan-approved`

**Fix:** On Plan PR, add the label:
```bash
gh pr edit <pr-number> --add-label plan-approved
```

### MCP server tools not available

**Check:**
1. MCP allowlist `.github/mcp-allowlist.yml` is correctly configured
2. MCP server files are in `mcp-servers/`
3. Agent workflows call the tools correctly

**Fix:**
```bash
# Update allowlist
python3 mcp-servers/validate-schema-server.py <<< '{"action": "validate-schema"}'
```

---

## Memory Issues

### Memory file not updated
**Check:** Scripts overwrite the file correctly
**Solution:** Ensure `.github/AGENTS_MEMORY.md` has proper write permissions

### Memory search slow
**Solution:** 
1. Use scopes: `echo '{"action": "read", "scope": "backend"}'`
2. Consider caching memory content in workflows

---

## Docker Issues

### "docker-compose up" fails
```bash
docker-compose down -v
docker-compose up --build
```

### Port conflicts
```bash
# Use different ports or check if:
lsof -i:5000
kill -9 <PID>
```

### Python type mismatches
```bash
# Clear any cached Python files
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete -type d
```

---

## Version Compatibility

### Flask version issues
If using Flask 3.x:
```python
# Some imports changed
# from flask import render_template
# Flask-Login works same in 3.x
```

### SQLAlchemy version issues
```python
# Use flask_sqlalchemy instead of sqlalchemy directly
from flask_sqlalchemy import SQLAlchemy
```

### Werkzeug version issues
```python
# Some deprecation warnings, update import:
# from werkzeug.security import generate_password_hash
```

---

## GitHub API Rate Limits

### "API rate limit exceeded" errors
**Solution:** Use token:
```bash
gh auth login
# Then use: gh workflow run <workflow-name>
```

### Workflow runner stuck
**Solution:**
1. Check workflow logs
2. Cancel with `gh run cancel <run-id>`
3. Kill long-running jobs: `gh run delete <run-id>`

---

## File Permissions

### Permission denied
```bash
# Ensure scripts are executable
chmod +x scripts/*.sh
chmod +x mcp-servers/*.py
```

---

## Debugging Tips

### Enable debug output
```bash
# In workflows
set -x
# In Python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Monitor resource usage
```bash
# See running containers
docker ps

# Check logs
docker-compose logs -f
```

### Check system resources
```bash
# Memory
free -h

# Disk space
 df -h .
```

---

## Getting Help

### GitHub Issues
- File issue in repository
- Include: workflow name, logs, steps to reproduce

### Debug with SSH
```bash
docker-compose exec web bash
vim backend/app.py
```

### Check Workflow Permissions
```bash
gh api repos/{owner}/{repo}/actions/permissions
```

---

## Common Fixes Script

Create `quick-fixes.sh`:
```bash
#!/bin/bash

# Fix permissions
chmod +x scripts/*.sh
chmod +x mcp-servers/*.py

# Update requirements
pip install --upgrade -r requirements.txt

# Clean up
ruff check --fix backend/
git add backend/
```

---

## Recovery

### Repository State
If something breaks:
```bash
# Backup important files
git status --porcelain | grep -v "^??" | xargs git checkout --

# Restore from backup
cp .github/AGENTS_MEMORY.md .github/AGENTS_MEMORY.md.backup
```

### Clean Slate
```bash
docker-compose down -v
rm -f app.db
rm -f docker-compose.local.yml
```

### Previous State Recovery
```bash
# Use rollback
./scripts/rollback.sh main <previous-commit>
```

---

## Monitoring

### Logs
All agent workflows log to GitHub Actions logs.

### Artifact Monitor
```bash
gh artifact list --workflow "CI" --limit 5
```

### Performance Monitor
```bash
# Check workflow run times
gh api repos/{owner}/{repo}/actions/runs --paginate | jq '.workflow_runs[] | {name, created_at, conclusion, run_duration}'
```

---

## Maintenance

### Monthly Tasks
1. Review `AGENTS_MEMORY.md` (see memory expiry)
2. Update risk classification if new patterns emerge
3. Archive old artifacts

### Quarterly Tasks
1. Review and update MCP servers
2. Check workflow performance
3. Update documentation

### Yearly Tasks
1. Review all 85 design principles
2. Assess if any requirements are obsolete
3. Plan major architecture changes