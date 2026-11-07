import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

gfg_added = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]
striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]

def norm(t):
    return re.sub(r'[^a-z0-9]', '', t.lower())

def clean_slug(url):
    if not url: return ''
    m = re.search(r'geeksforgeeks\.org/problems/([^/?#]+)', url)
    if m: return re.sub(r'(-\d+|\d+)$', '', m.group(1)).lower().replace('-', '').replace('_', '')
    m = re.search(r'leetcode\.com/problems/([^/?#]+)', url)
    if m: return re.sub(r'(-\d+|\d+)$', '', m.group(1)).lower().replace('-', '').replace('_', '')
    m = re.search(r'geeksforgeeks\.org/([^/?#]+)/?$', url)
    if m: return re.sub(r'(-\d+|\d+)$', '', m.group(1)).lower().replace('-', '').replace('_', '')
    return ''

# Let's map Striver problems by slug and norm
striver_by_slug = {}
for p in striver:
    for u in [p.get('url', '')] + [a.get('url', '') for a in p.get('altUrls', [])]:
        s = clean_slug(u)
        if s: striver_by_slug[s] = p

exact_duplicates = []
for g in gfg_added:
    s = clean_slug(g['url'])
    if s and s in striver_by_slug:
        exact_duplicates.append((g, striver_by_slug[s], f"slug match: {s}"))

print(f"Exact duplicates by slug with Striver: {len(exact_duplicates)}")
for g, s, r in exact_duplicates:
    print(f"GFG: {g['title']} <==> STRIVER: {s['title']} ({r})")
