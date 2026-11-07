import json
import re

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

gfg_added = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]
print(f"Total GFG added: {len(gfg_added)}")

# Let's inspect potential removal candidates:
# 1. Non-coding theory/trivia (e.g. "Why strings are immutable in Java?")
# 2. Dead/external links not on practice platform (e.g. spoj, hackerearth, programiz, theoryofprogramming)
# 3. Exact duplicates of existing Striver questions where the title in GFG is just slightly worded differently, so the user won't practice the exact same question twice

# Let's categorize every added problem
theory_questions = []
external_broken = []
duplicate_of_striver = []

# Striver normalized titles
striver_titles = {re.sub(r'[^a-z0-9]', '', p['title'].lower()): p['title'] for p in d['problems'] if not p['id'].startswith('gfg-450-')}

for p in gfg_added:
    t = p['title'].strip()
    u = p['url'].strip()
    
    # Theory questions
    if any(q in t.lower() for q in ['why strings are immutable', 'function to find number of customers who could not get a computer']):
        theory_questions.append((p['id'], t, u))
    # External non-practice / dead links
    elif any(host in u.lower() for host in ['spoj.com', 'hackerearth.com', 'theoryofprogramming.com', 'programiz.com']):
        external_broken.append((p['id'], t, u))

print(f"Theory questions: {len(theory_questions)}")
print(f"External/SPOJ/HackerEarth links: {len(external_broken)}")
