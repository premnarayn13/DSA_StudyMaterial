import os

handbook_dir = r'd:\DSA\handbook'
existing_folders = sorted([f for f in os.listdir(handbook_dir) if os.path.isdir(os.path.join(handbook_dir, f))])

print(f"Total existing folders: {len(existing_folders)}")

# Mapping from current folder names to new folder names:
# User requested:
# "put strings, complexity analysis front before arrays..as2 & 3"
ORDER_MAPPING = [
    # 1. Introduction
    ("chapter-01-introduction-to-dsa", "chapter-01-introduction-to-dsa"),
    # 2. Strings
    ("chapter-20-strings", "chapter-02-strings"),
    # 3. Complexity Analysis
    ("chapter-23-complexity-analysis", "chapter-03-complexity-analysis"),
    # 4. Arrays (placed right after 2 & 3)
    ("chapter-03-arrays", "chapter-04-arrays"),
    # 5. Sorting
    ("chapter-02-sorting-algorithms", "chapter-05-sorting-algorithms"),
    # 6. Hashing
    ("chapter-04-hashing", "chapter-06-hashing"),
    # 7. Searching Algorithms (Binary Search)
    ("chapter-05-searching-algorithms", "chapter-07-searching-algorithms"),
    # 8. Recursion
    ("chapter-06-recursion", "chapter-08-recursion"),
    # 9. Backtracking
    ("chapter-07-backtracking", "chapter-09-backtracking"),
    # 10. Linked Lists
    ("chapter-08-linked-lists", "chapter-10-linked-lists"),
    # 11. Bit Manipulation
    ("chapter-09-bit-manipulation", "chapter-11-bit-manipulation"),
    # 12. Greedy Algorithms
    ("chapter-10-greedy-algorithms", "chapter-12-greedy-algorithms"),
    # 13. Two Pointers
    ("chapter-11-two-pointers", "chapter-13-two-pointers"),
    # 14. Sliding Window
    ("chapter-12-sliding-window", "chapter-14-sliding-window"),
    # 15. Stacks & Queues
    ("chapter-13-stacks-queues", "chapter-15-stacks-queues"),
    # 16. Binary Trees
    ("chapter-14-trees-bst", "chapter-16-trees-bst"),
    # 17. BST
    ("chapter-15-bst", "chapter-17-bst"),
    # 18. Heaps
    ("chapter-16-heaps", "chapter-18-heaps"),
    # 19. Graphs
    ("chapter-17-graphs", "chapter-19-graphs"),
    # 20. Dynamic Programming
    ("chapter-18-dynamic-programming", "chapter-20-dynamic-programming"),
    # 21. Tries
    ("chapter-19-tries", "chapter-21-tries"),
    # 22. String Algorithms (Advanced)
    ("chapter-21-string-algorithms", "chapter-22-string-algorithms"),
    # 23. Mathematical Algorithms
    ("chapter-22-mathematical-algorithms", "chapter-23-mathematical-algorithms"),

    # --- Remaining topics ---
    ("chapter-24-java-for-dsa", "chapter-24-java-for-dsa"),
    ("chapter-25-avl-trees", "chapter-25-avl-trees"),
    ("chapter-26-red-black-trees", "chapter-26-red-black-trees"),
    ("chapter-27-segment-trees", "chapter-27-segment-trees"),
    ("chapter-28-dsu", "chapter-28-dsu"),
    ("chapter-29-fenwick-tree", "chapter-29-fenwick-tree"),
    ("chapter-30-branch-and-bound", "chapter-30-branch-and-bound")
]

print(f"Total mapped: {len(ORDER_MAPPING)}")

old_names = [x[0] for x in ORDER_MAPPING]
new_names = [x[1] for x in ORDER_MAPPING]

missing_in_mapping = set(existing_folders) - set(old_names)
extra_in_mapping = set(old_names) - set(existing_folders)
duplicate_new = len(new_names) - len(set(new_names))

print(f"Missing in mapping: {missing_in_mapping}")
print(f"Extra in mapping: {extra_in_mapping}")
print(f"Duplicate new names: {duplicate_new}")

if not missing_in_mapping and not extra_in_mapping and duplicate_new == 0:
    print("\nExecuting safe two-step rename...")
    # Step 1: to temp
    temp_list = []
    for idx, (old_name, new_name) in enumerate(ORDER_MAPPING):
        old_path = os.path.join(handbook_dir, old_name)
        temp_path = os.path.join(handbook_dir, f"_temp_step_{idx:02d}")
        os.rename(old_path, temp_path)
        temp_list.append((temp_path, os.path.join(handbook_dir, new_name)))
    print("Step 1 (to temp) complete.")

    # Step 2: to final
    for temp_path, final_path in temp_list:
        os.rename(temp_path, final_path)
    print("Step 2 (to final) complete.")
    
    print("\nFinal handbook directory listing:")
    for f in sorted(os.listdir(handbook_dir)):
        if os.path.isdir(os.path.join(handbook_dir, f)):
            print(f"  {f}")
else:
    print("Validation failed, aborting rename!")
