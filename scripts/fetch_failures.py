import json
import sys

data = json.load(sys.stdin)
for job in data.get("jobs", []):
    if job.get("conclusion") == "failure":
        print(f"Job: {job['name']} failed")
        for step in job.get("steps", []):
            if step.get("conclusion") == "failure":
                print(f"  Step: {step['name']}")
        print()
