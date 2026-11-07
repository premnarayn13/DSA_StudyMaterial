import json

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for s in d['meta']['steps']:
    probs = [p for p in d['problems'] if p['step'] == s['n']]
    topics = sorted(list(set(p['topic'] for p in probs)))
    print(f"Step {s['n']:02d}: {s['title']:<25} ({len(probs):3d} problems) -> {topics}")
