#!/usr/bin/env python3
# A-01, A-02
"""Generate a structured plan artifact for an agent task."""
import argparse
import os
from datetime import datetime

# Maps scope to suggested files for modification
SCOPE_FILES = {
    "frontend": [
        "backend/templates/",
        "backend/static/css/",
        "backend/static/js/",
    ],
    "backend": [
        "backend/app.py",
        "backend/models.py",
        "backend/routes/",
    ],
    "db": [
        "backend/models.py",
        "backend/migrations/",
    ],
    "docs": [
        "README.md",
        "docs/",
    ],
    "infra": [
        ".github/workflows/",
        "Dockerfile",
        "docker-compose.yml",
    ],
}

SCOPE_STEPS = {
    "frontend": [
        "Create/modify HTML template(s) with Bootstrap 5 components",
        "Add corresponding CSS styles in static/css/",
        "Add JavaScript behavior in static/js/ if needed",
        "Update route in appropriate blueprint if new page added",
        "Add/update tests in backend/tests/",
    ],
    "backend": [
        "Add/update model in backend/models.py",
        "Add/update route in backend/routes/",
        "Add/update form validation if needed",
        "Add/update tests in backend/tests/",
    ],
    "db": [
        "Update model definition in backend/models.py",
        "Create migration script if using alembic",
        "Update seed data if applicable",
        "Verify tests pass",
    ],
    "docs": [
        "Update relevant documentation files",
        "Verify markdown renders correctly",
    ],
    "infra": [
        "Update configuration file(s)",
        "Verify CI/CD pipeline still valid",
        "Test deployment process",
    ],
}


def generate_plan(scope: str, ticket: str, risk: str, description: str = "") -> str:
    files = SCOPE_FILES.get(scope, ["- (list files here)"])
    steps = SCOPE_STEPS.get(scope, ["1. (step 1)", "2. (step 2)", "3. (step 3)"])

    plan = f"""# Agent Plan

## Scope
{scope}

## Ticket / Issue
#{ticket}

## Risk Level
{risk}

## Description
{description}

## Success Criteria
- [ ] All changes are implemented per requirements
- [ ] All existing tests pass
- [ ] No regression in existing functionality
- [ ] Code follows project style guidelines
- [ ] New functionality covered by tests

## Files to Modify
"""
    for f in files:
        plan += f"- {f}\n"

    plan += """
## Implementation Steps
"""
    for i, step in enumerate(steps, 1):
        plan += f"{i}. {step}\n"

    plan += f"""
## Rollback Strategy
Revert the commit using `scripts/rollback.sh` if issues are detected.

## Escalation Path
If this plan cannot be executed as described, create an escalation issue with label `escalation`.

---

*Generated: {datetime.now().isoformat()}*
*Agent Scope: {scope}*
"""

    return plan


def main():
    parser = argparse.ArgumentParser(description="Generate a plan artifact")
    parser.add_argument("--scope", required=True, help="Agent scope (backend/frontend/db)")
    parser.add_argument("--ticket", required=True, help="Issue or ticket ID")
    parser.add_argument("--risk", default="medium", help="Risk level (low/medium/high/critical)")
    parser.add_argument("--output-dir", default="plans", help="Output directory for plan file")
    parser.add_argument("--description-file", help="Path to file containing issue description")
    args = parser.parse_args()

    description = ""
    if args.description_file and os.path.exists(args.description_file):
        with open(args.description_file) as f:
            description = f.read().strip()

    os.makedirs(args.output_dir, exist_ok=True)
    plan = generate_plan(args.scope, args.ticket, args.risk, description)
    filepath = os.path.join(args.output_dir, f"plan-{args.ticket}.md")
    with open(filepath, "w") as f:
        f.write(plan)
    print(f"Plan written to {filepath}")


if __name__ == "__main__":
    main()
