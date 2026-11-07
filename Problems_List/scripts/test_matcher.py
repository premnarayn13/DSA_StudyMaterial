import json
import difflib
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

import sys
sys.path.append('scripts')
from curate_target_580 import GFG_TO_STRIVER_MAP, clean_str

striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]
striver_titles = {clean_str(p['title']): p for p in striver}
title_list = [p['title'] for p in striver]

matches = {}
for gfg_t, target_t in GFG_TO_STRIVER_MAP.items():
    k = clean_str(target_t)
    if k in striver_titles:
        matches[clean_str(gfg_t)] = striver_titles[k]
    else:
        close = difflib.get_close_matches(target_t, title_list, n=1, cutoff=0.55)
        if close:
            matches[clean_str(gfg_t)] = striver_titles[clean_str(close[0])]

print(f"Total resolved matches: {len(matches)} out of {len(GFG_TO_STRIVER_MAP)}")
for gfg_t in list(GFG_TO_STRIVER_MAP.keys())[:15]:
    k = clean_str(gfg_t)
    if k in matches:
        print(f"  {gfg_t}  ==>  {matches[k]['title']}")
    else:
        print(f"  {gfg_t}  ==>  [UNMATCHED]")
