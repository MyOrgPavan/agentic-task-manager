#!/usr/bin/env python3
# A-01, A-02
"""Generate a structured plan artifact for an agent task."""
import argparse
import os
from datetime import datetime


def generate_plan(scope: str, ticket: str, risk: str) -> str:
    return f"""# Agent Plan

## Scope
{scope}

## Ticket / Issue
#{ticket}

## Risk Level
{risk}

## Success Criteria
- [ ] All changes are implemented per requirements
- [ ] All tests pass
- [ ] No regression in existing functionality
- [ ] Code follows project style guidelines

## Files to Modify
- (list files here)

## Plan
1. (step 1)
2. (step 2)
3. (step 3)

## Rollback Strategy
Revert the commit using `scripts/rollback.sh` if issues are detected.

## Escalation Path
If this plan cannot be executed as described, create an escalation issue with label `escalation`.

---

*Generated: {datetime.now().isoformat()}*
*Agent Scope: {scope}*
"""


def main():
    parser = argparse.ArgumentParser(description="Generate a plan artifact")
    parser.add_argument("--scope", required=True, help="Agent scope (backend/frontend/db)")
    parser.add_argument("--ticket", required=True, help="Issue or ticket ID")
    parser.add_argument("--risk", default="medium", help="Risk level (low/medium/high/critical)")
    parser.add_argument("--output-dir", default="plans", help="Output directory for plan file")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    plan = generate_plan(args.scope, args.ticket, args.risk)
    filepath = os.path.join(args.output_dir, f"plan-{args.ticket}.md")
    with open(filepath, "w") as f:
        f.write(plan)
    print(f"Plan written to {filepath}")


if __name__ == "__main__":
    main()
