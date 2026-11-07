import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]
gfg = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]

# Let's inspect all 291 gfg problems
print(f"Total GFG problems: {len(gfg)}")

# Let's write out all 291 titles to a clean review file
with open('scripts/gfg_titles_review.txt', 'w', encoding='utf-8') as out:
    for idx, p in enumerate(gfg, start=1):
        out.write(f"{idx:3d}. [{p['topic']}] {p['title']}  |  {p['url']}\n")

print("Wrote gfg_titles_review.txt")
