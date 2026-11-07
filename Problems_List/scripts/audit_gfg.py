import json

with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

gfg_new = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

with open('d:/DSA/Problems_List/scripts/gfg_new_list.txt', 'w', encoding='utf-8') as out:
    for idx, p in enumerate(gfg_new, 1):
        out.write(f"{idx:3d}. [{p['topic']}] {p['title']} --> {p['url']}\n")

print(f"Written {len(gfg_new)} problems to gfg_new_list.txt")
