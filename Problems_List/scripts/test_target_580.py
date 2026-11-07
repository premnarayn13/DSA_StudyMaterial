import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

print(f"Striver core: {len(striver_core)}")
print(f"GFG added: {len(gfg_added)}")

# Let's inspect the duplicate map from audit_filter.py
from audit_filter import GFG_TO_STRIVER_DUPLICATES

print(f"Total duplicates mapped in audit_filter: {len(GFG_TO_STRIVER_DUPLICATES)}")

# Let's check how many match currently in gfg_added
matched_count = 0
unmatched_gfg = []

# Map Striver title lower clean to striver problem
striver_by_title = {re.sub(r'[^a-z0-9]', '', p['title'].lower()): p for p in striver_core}

for g in gfg_added:
    t_clean = re.sub(r'\[.*?\]', '', g['title']).strip().lower()
    t_key = re.sub(r'[^a-z0-9]', '', t_clean)
    
    # Check manual map
    if t_clean in GFG_TO_STRIVER_DUPLICATES:
        matched_count += 1
    elif t_key in striver_by_title:
        matched_count += 1
    else:
        unmatched_gfg.append(g)

print(f"Matched duplicates: {matched_count}")
print(f"Remaining distinct GFG problems: {len(unmatched_gfg)}")
print(f"Resulting total: {len(striver_core) + len(unmatched_gfg)}")
