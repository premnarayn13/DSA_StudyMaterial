import json
import re
import openpyxl
from collections import defaultdict
from difflib import SequenceMatcher

# 1. Load Striver data
with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
    striver_data = json.load(f)

striver_probs = striver_data['problems']

# 2. Load GFG-450
wb = openpyxl.load_workbook('d:/DSA/MY_GFG-450.xlsx')
sheet = wb.active

gfg_rows = []
for r in range(5, sheet.max_row + 1):
    topic = sheet.cell(r, 1).value
    title = sheet.cell(r, 2).value
    link = sheet.cell(r, 2).hyperlink.target if sheet.cell(r, 2).hyperlink else ''
    done = sheet.cell(r, 3).value
    if title and title.strip():
        gfg_rows.append({
            'row': r,
            'topic': str(topic).strip() if topic else 'General',
            'title': title.strip(),
            'url': link.strip() if link else '',
            'done': done
        })

print(f"Loaded {len(striver_probs)} Striver problems and {len(gfg_rows)} GFG problems.")

def clean_slug(url):
    if not url: return ''
    m = re.search(r'geeksforgeeks\.org/problems/([^/]+)', url)
    if m:
        slug = m.group(1)
        # remove trailing numbers e.g. -1587115620 or 4636
        slug = re.sub(r'(-\d+|\d+)$', '', slug)
        return slug.lower().replace('-', '').replace('_', '')
    m2 = re.search(r'geeksforgeeks\.org/([^/]+)/?', url)
    if m2:
        slug = m2.group(1)
        slug = re.sub(r'(-\d+|\d+)$', '', slug)
        return slug.lower().replace('-', '').replace('_', '')
    m3 = re.search(r'leetcode\.com/problems/([^/]+)', url)
    if m3:
        slug = m3.group(1)
        return slug.lower().replace('-', '').replace('_', '')
    return ''

def normalize_title(t):
    if not t: return ''
    t = t.lower()
    t = re.sub(r'\[.*?\]', '', t) # remove [V. IMP], etc.
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

def token_set(t):
    if not t: return set()
    t = t.lower()
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'\b(find|given|problem|check|program|write|print|determine|count|how|to|the|a|an|in|of|for|on|with|from|and|or|by|at|is|if|as|all|into|using|without|only|their|two|both|between|any)\b', ' ', t)
    t = re.sub(r'[^a-z0-9]', ' ', t)
    return set(w for w in t.split() if len(w) > 1)

# Build index of Striver problems
by_exact_url = {}
by_clean_slug = defaultdict(list)
by_norm_title = {}
by_tokens = []

for p in striver_probs:
    all_urls = [p['url']] + [a['url'] for a in p.get('altUrls', [])]
    for u in all_urls:
        if u:
            by_exact_url[u.strip()] = p
            cslug = clean_slug(u)
            if cslug:
                by_clean_slug[cslug].append(p)
    
    if p.get('slug'):
        by_clean_slug[clean_slug(p['slug'])].append(p)
    if p.get('lcSlug'):
        by_clean_slug[clean_slug(p['lcSlug'])].append(p)
        
    nt = normalize_title(p['title'])
    if nt:
        by_norm_title[nt] = p
    
    by_tokens.append((p, token_set(p['title']), normalize_title(p['title'])))

# Try matching
duplicates = []
new_problems = []

for g in gfg_rows:
    g_title = g['title']
    g_url = g['url']
    g_slug = clean_slug(g_url)
    g_norm = normalize_title(g_title)
    g_tok = token_set(g_title)
    
    matched_p = None
    match_type = ''
    
    # 1. Exact URL
    if g_url and g_url in by_exact_url:
        matched_p = by_exact_url[g_url]
        match_type = 'exact_url'
    
    # 2. Slug match
    if not matched_p and g_slug and g_slug in by_clean_slug:
        matched_p = by_clean_slug[g_slug][0]
        match_type = 'slug'
        
    # 3. Normalized Title exact match
    if not matched_p and g_norm in by_norm_title:
        matched_p = by_norm_title[g_norm]
        match_type = 'norm_title'
        
    # 4. Token & similarity match
    if not matched_p:
        best_score = 0
        best_cand = None
        for sp, s_tok, s_norm in by_tokens:
            if not g_tok or not s_tok: continue
            jaccard = len(g_tok & s_tok) / len(g_tok | s_tok)
            seq = SequenceMatcher(None, g_norm, s_norm).ratio()
            score = max(jaccard, seq)
            if score > best_score:
                best_score = score
                best_cand = sp
        if best_score >= 0.75: # high confidence
            matched_p = best_cand
            match_type = f'similarity_{best_score:.2f}'

    if matched_p:
        duplicates.append({
            'gfg': g,
            'striver': matched_p,
            'match_type': match_type
        })
    else:
        new_problems.append(g)

print(f"Matched Duplicates: {len(duplicates)}")
print(f"New Problems to Add: {len(new_problems)}")

# Check duplicate details
print("\nSample Duplicates (first 25):")
for d in duplicates[:25]:
    print(f"[{d['match_type']}] GFG: {d['gfg']['title'][:40]} ===> Striver: {d['striver']['title'][:40]}")

# Check sample new problems
print("\nSample New Problems (first 20):")
for np in new_problems[:20]:
    print(f"[{np['topic']}] {np['title']}")
