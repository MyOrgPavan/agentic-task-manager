import re

with open(".github/AGENTS_MEMORY.md") as f:
    content = f.read()

entries = re.findall(r"## (.*?)\n.*?\((.*?)\)", content, re.DOTALL)
print("Found entries:", len(entries))
