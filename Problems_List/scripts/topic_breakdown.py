import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

gfg_added = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]
striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]

# Let's inspect known duplicates between GFG 450 and Striver
# and see which ones are 100% the exact same sum
print(f"Total problems currently: {len(d['problems'])}")
print(f"Striver problems: {len(striver)}")
print(f"GFG added: {len(gfg_added)}")

# Let's inspect topic by topic
from collections import Counter
counts = Counter(p['topic'] for p in gfg_added)
for topic, cnt in counts.most_common():
    print(f"{topic}: {cnt}")
