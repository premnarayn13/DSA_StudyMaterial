import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

print(f"Striver Core: {len(striver_core)}")
print(f"GFG Added: {len(gfg_added)}")
print(f"Total: {len(data['problems'])}")

# Known exact duplicates where GFG problem is literally the same question as Striver
# Let's map GFG ID or clean title to Striver ID or URL
from scripts.filter_standard_problems import GFG_TO_STRIVER_DUPLICATES

print(f"Duplicate mapping count: {len(GFG_TO_STRIVER_DUPLICATES)}")
