import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

from audit_filter import GFG_TO_STRIVER_DUPLICATES
striver_by_title = {re.sub(r'[^a-z0-9]', '', p['title'].lower()): p for p in striver_core}

unmatched_gfg = []
for g in gfg_added:
    t_clean = re.sub(r'\[.*?\]', '', g['title']).strip().lower()
    t_key = re.sub(r'[^a-z0-9]', '', t_clean)
    if t_clean in GFG_TO_STRIVER_DUPLICATES or t_key in striver_by_title:
        continue
    unmatched_gfg.append(g)

print(f"Total distinct GFG problems: {len(unmatched_gfg)}")

# Check external links and trivia in these 160
trivia_and_external = []
standard_gfg = []

for g in unmatched_gfg:
    t = g['title'].strip()
    u = g['url'].strip()
    
    is_trivia = "why strings are immutable" in t.lower()
    is_external = any(h in u.lower() for h in ['spoj.com', 'hackerearth.com', 'theoryofprogramming.com', 'programiz.com'])
    
    if is_trivia or is_external:
        trivia_and_external.append((t, u))
    else:
        standard_gfg.append(g)

print(f"\nTrivia/External links: {len(trivia_and_external)}")
for t, u in trivia_and_external:
    print(f"  - {t} ({u})")

print(f"\nRemaining Standard GFG problems: {len(standard_gfg)}")
print(f"Total problems if removing trivia/external: {len(striver_core) + len(standard_gfg)}")
