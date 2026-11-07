import json

with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for p in d['problems']:
    p['title'] = p['title'].replace(chr(65533), "'").strip()

with open('site/data.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("Title encoding successfully fixed!")
