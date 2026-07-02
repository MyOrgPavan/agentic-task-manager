#!/usr/bin/env python3
"""Create an implementation PR from an approved plan."""
import argparse
import os
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Create implementation PR from plan")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--ticket", required=True)
    parser.add_argument("--plan-file", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.plan_file):
        print(f"Plan file not found: {args.plan_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.plan_file) as f:
        plan_content = f.read()

    branch = f"impl/{args.scope}/{args.ticket}"

    subprocess.run(["git", "config", "user.name", "agent-execute"], check=True)
    subprocess.run(["git", "config", "user.email", "agent-execute@github.local"], check=True)

    result = subprocess.run(
        ["git", "checkout", "-b", branch],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        # Branch may already exist
        subprocess.run(["git", "checkout", branch], check=True)

    # Run tests
    test_result = subprocess.run(["pytest", "backend/tests/", "-v"], capture_output=True, text=True)
    print(test_result.stdout)
    if test_result.returncode != 0:
        print("Tests failed, continuing anyway", file=sys.stderr)
        print(test_result.stderr)

    result = subprocess.run(["git", "add", "-A"], capture_output=True, text=True)
    result = subprocess.run(
        ["git", "commit", "-m", f"Implement: {args.scope} / #{args.ticket}"],
        capture_output=True, text=True
    )
    if result.returncode != 0 and "nothing to commit" not in result.stderr:
        print(f"Commit result: {result.stdout} {result.stderr}")

    result = subprocess.run(
        ["git", "push", "origin", branch],
        capture_output=True, text=True
    )
    print(f"Push result: {result.stdout} {result.stderr}")

    print(f"Branch: {branch}")
    print("PR body:")
    print(plan_content)

if __name__ == "__main__":
    main()
