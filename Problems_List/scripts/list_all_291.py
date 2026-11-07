import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

gfg_added = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]
striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]

# Let's inspect gfg_added titles and URLs
for idx, p in enumerate(gfg_added, start=1):
    print(f"{idx:3d}. [{p['topic']}] {p['title']} --> {p['url']}")
