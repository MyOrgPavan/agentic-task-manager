# 04 — Risk Classification & Autonomy Customization

How to customize risk levels, file patterns, and autonomy behaviors.

## Risk Classification Model

The `.github/risk-classification.yml` file defines which file patterns map to which risk levels, and which autonomy levels are allowed for each risk level.

### Current Configuration

```yaml
default_risk: medium

rules:
  - pattern: "backend/models.py"
    risk: high
    reason: "Database schema changes can break existing data"

  - pattern: "backend/routes/*.py"
    risk: medium
    reason: "API route changes may affect frontend contract"

  - pattern: "backend/templates/*.html"
    risk: low
    reason: "Presentation-only, easily reversible"

  - pattern: ".github/workflows/*.yml"
    risk: critical
    reason: "Affects entire agentic infrastructure"

  - pattern: "requirements.txt"
    risk: high
    reason: "Dependency changes can introduce security issues"
```

### Adding a New Pattern

```yaml
rules:
  - pattern: "backend/services/*.py"
    risk: medium
    reason: "Business logic changes require careful review"

  - pattern: "docs/**/*.md"
    risk: low
    reason: "Documentation only"
```

**Pattern syntax:** Uses GitHub's glob patterns (`*`, `**`, `?`)

### Autonomy Levels per Risk

```yaml
autonomy_levels:
  critical:
    - read_only
    - propose_only
  high:
    - propose_only
    - execute_with_guardrails
  medium:
    - propose_only
    - execute_with_guardrails
  low:
    - execute_with_guardrails
    - auto_merge
```

### Risk Level Definitions

| Risk Level | Description | Autonomy |
|------------|-------------|----------|
| **Critical** | Infrastructure, security, CI/CD | Read-only or propose only |
| **High** | Schema, dependencies, auth | Propose or execute with guardrails |
| **Medium** | Business logic, API routes | Propose or execute with guardrails |
| **Low** | Templates, styles, docs | Auto-merge after CI |

---

## Customizing for Your Project

### 1. Add Project-Specific Patterns

```yaml
rules:
  - pattern: "src/api/v1/**/*.py"
    risk: medium
    reason: "Public API surface"

  - pattern: "src/internal/**/*.py"
    risk: low
    reason: "Internal utilities"

  - pattern: "terraform/**/*.tf"
    risk: critical
    reason: "Infrastructure as code"
```

### 2. Adjust Autonomy Levels

To be more conservative:
```yaml
autonomy_levels:
  high:
    - propose_only  # Remove execute_with_guardrails
```

To be more aggressive:
```yaml
autonomy_levels:
  medium:
    - auto_merge  # Allow auto-merge for medium risk
```

### 3. Change Default Risk

```yaml
default_risk: low  # More permissive by default
```

---

## How Agents Use Risk Classification

1. **agent-plan.yml** reads risk level:
   ```yaml
   - name: Read risk classification
     run: |
       python -c "
       import yaml
       with open('.github/risk-classification.yml') as f:
           data = yaml.safe_load(f)
       print(f'risk_level={data.get(\"default_risk\", \"medium\")}')
       "
   ```

2. **phase-2-auto-merge.yml** checks for `low-risk` label:
   ```yaml
   if: contains(github.event.pull_request.labels.*.name, 'low-risk')
   ```

3. **agent-execute.yml** gates on plan approval regardless of risk

---

## Phase Workflows Mapping

| Phase | Autonomy Level | Risk Levels Allowed |
|-------|----------------|---------------------|
| Phase 1 | Propose-only | All |
| Phase 2 | Auto-merge | Low only |
| Phase 3 | Staging deploy | Low + Medium (after merge) |
| Phase 4 | Prod deploy | Human-authorized only |

---

## Validation

Test risk classification:
```bash
python -c "
import yaml, fnmatch
with open('.github/risk-classification.yml') as f:
    config = yaml.safe_load(f)

test_files = [
    'backend/models.py',
    'backend/routes/tasks.py',
    'backend/templates/task_detail.html',
    '.github/workflows/ci.yml',
    'requirements.txt',
]

for f in test_files:
    risk = config.get('default_risk', 'medium')
    for rule in config.get('rules', []):
        if fnmatch.fnmatch(f, rule['pattern']):
            risk = rule['risk']
            break
    print(f'{f:40s} → {risk}')
"
```

---

## Best Practices

1. **Start conservative** — default to `high` for new patterns
2. **Document reasons** — each rule needs a `reason` field
3. **Test changes** — run validation script after edits
4. **Review quarterly** — governance review should assess risk model accuracy
5. **Track overrides** — log when human overrides agent autonomy