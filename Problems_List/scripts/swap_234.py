import os

handbook_dir = r'd:\DSA\handbook'

# Target changes:
# 2: complexity analysis
# 3: arrays
# 4: strings
reorder_map = [
    ("chapter-03-complexity-analysis", "chapter-02-complexity-analysis"),
    ("chapter-04-arrays", "chapter-03-arrays"),
    ("chapter-02-strings", "chapter-04-strings"),
]

print("Step 1: Renaming 2, 3, 4 to temporary names...")
temp_list = []
for idx, (old_name, new_name) in enumerate(reorder_map):
    old_p = os.path.join(handbook_dir, old_name)
    temp_p = os.path.join(handbook_dir, f"_temp_swap_{idx}")
    os.rename(old_p, temp_p)
    temp_list.append((temp_p, os.path.join(handbook_dir, new_name)))

print("Step 2: Renaming to final target names...")
for temp_p, final_p in temp_list:
    os.rename(temp_p, final_p)

print("\nVerification - First 8 chapters:")
for f in sorted(os.listdir(handbook_dir))[:8]:
    if os.path.isdir(os.path.join(handbook_dir, f)):
        print(f"  {f}")
