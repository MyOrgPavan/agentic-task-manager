import re
import sys

import yaml

filepath = sys.argv[1]
with open(filepath) as f:
    content = f.read()

match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
if match:
    data = yaml.safe_load(match.group(1))
    for k, v in data.items():
        print(f'{k}={v}')
else:
    print('ERROR: No YAML frontmatter found')
    sys.exit(1)
