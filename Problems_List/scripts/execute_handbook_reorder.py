import os
import sys

handbook_dir = r'd:\DSA\handbook'

ORDER_MAPPING = [
    # --- Mapped Topics (Problem List Steps 1 to 19) ---
    ("chapter-01-introduction-to-dsa", "chapter-01-introduction-to-dsa"),
    ("chapter-23-sorting-algorithms", "chapter-02-sorting-algorithms"),
    ("chapter-04-arrays", "chapter-03-arrays"),
    ("chapter-10-hashing", "chapter-04-hashing"),
    ("chapter-22-searching-algorithms", "chapter-05-searching-algorithms"),
    ("chapter-21-recursion", "chapter-06-recursion"),
    ("chapter-27-backtracking", "chapter-07-backtracking"),
    ("chapter-06-linked-lists", "chapter-08-linked-lists"),
    ("chapter-29-bit-manipulation", "chapter-09-bit-manipulation"),
    ("chapter-25-greedy-algorithms", "chapter-10-greedy-algorithms"),
    ("chapter-07-two-pointers", "chapter-11-two-pointers"),
    ("chapter-08-sliding-window", "chapter-12-sliding-window"),
    ("chapter-09-stacks-queues", "chapter-13-stacks-queues"),
    ("chapter-11-trees-bst", "chapter-14-trees-bst"),
    ("chapter-13-bst", "chapter-15-bst"),
    ("chapter-12-heaps", "chapter-16-heaps"),
    ("chapter-20-graphs", "chapter-17-graphs"),
    ("chapter-26-dynamic-programming", "chapter-18-dynamic-programming"),
    ("chapter-16-tries", "chapter-19-tries"),
    ("chapter-05-strings", "chapter-20-strings"),
    ("chapter-24-string-algorithms", "chapter-21-string-algorithms"),
    ("chapter-30-mathematical-algorithms", "chapter-22-mathematical-algorithms"),

    # --- Remaining Topics (Placed after the mapped steps) ---
    ("chapter-02-complexity-analysis", "chapter-23-complexity-analysis"),
    ("chapter-03-java-for-dsa", "chapter-24-java-for-dsa"),
    ("chapter-14-avl-trees", "chapter-25-avl-trees"),
    ("chapter-15-red-black-trees", "chapter-26-red-black-trees"),
    ("chapter-17-segment-trees", "chapter-27-segment-trees"),
    ("chapter-18-dsu", "chapter-28-dsu"),
    ("chapter-19-fenwick-tree", "chapter-29-fenwick-tree"),
    ("chapter-28-branch-and-bound", "chapter-30-branch-and-bound")
]

# Step 1: Rename to intermediate temporary names
print("Step 1: Renaming to temporary names...")
temp_names = []
for idx, (old_name, new_name) in enumerate(ORDER_MAPPING):
    old_path = os.path.join(handbook_dir, old_name)
    temp_name = f"_temp_reorder_{idx:02d}"
    temp_path = os.path.join(handbook_dir, temp_name)
    os.rename(old_path, temp_path)
    temp_names.append((temp_path, os.path.join(handbook_dir, new_name)))

print("Step 1 completed successfully.")

# Step 2: Rename from temporary names to final names
print("Step 2: Renaming to final names...")
for temp_path, final_path in temp_names:
    os.rename(temp_path, final_path)

print("Step 2 completed successfully.")
print("\nFinal handbook directory listing:")
for f in sorted(os.listdir(handbook_dir)):
    if os.path.isdir(os.path.join(handbook_dir, f)):
        print(f"  {f}")
