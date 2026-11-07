import os

handbook_dir = r'd:\DSA\handbook'
existing_folders = sorted([f for f in os.listdir(handbook_dir) if os.path.isdir(os.path.join(handbook_dir, f))])

print(f"Total existing folders: {len(existing_folders)}")

# Mapping definition:
# Old folder name -> (Order index, new folder name)
ORDER_MAPPING = [
    # --- Mapped Topics (Problem List Steps 1 to 19) ---
    # Step 01: Beginner Problems
    ("chapter-01-introduction-to-dsa", "chapter-01-introduction-to-dsa"),
    # Step 02: Sorting
    ("chapter-23-sorting-algorithms", "chapter-02-sorting-algorithms"),
    # Step 03: Arrays
    ("chapter-04-arrays", "chapter-03-arrays"),
    # Step 04: Hashing
    ("chapter-10-hashing", "chapter-04-hashing"),
    # Step 05: Binary Search
    ("chapter-22-searching-algorithms", "chapter-05-searching-algorithms"),
    # Step 06: Recursion (& Backtracking)
    ("chapter-21-recursion", "chapter-06-recursion"),
    ("chapter-27-backtracking", "chapter-07-backtracking"),
    # Step 07: Linked-List
    ("chapter-06-linked-lists", "chapter-08-linked-lists"),
    # Step 08: Bit Manipulation
    ("chapter-29-bit-manipulation", "chapter-09-bit-manipulation"),
    # Step 09: Greedy Algorithms
    ("chapter-25-greedy-algorithms", "chapter-10-greedy-algorithms"),
    # Step 10: Sliding Window / 2 Pointer
    ("chapter-07-two-pointers", "chapter-11-two-pointers"),
    ("chapter-08-sliding-window", "chapter-12-sliding-window"),
    # Step 11: Stack / Queues
    ("chapter-09-stacks-queues", "chapter-13-stacks-queues"),
    # Step 12: Binary Trees
    ("chapter-11-trees-bst", "chapter-14-trees-bst"),
    # Step 13: Binary Search Trees
    ("chapter-13-bst", "chapter-15-bst"),
    # Step 14: Heaps
    ("chapter-12-heaps", "chapter-16-heaps"),
    # Step 15: Graphs
    ("chapter-20-graphs", "chapter-17-graphs"),
    # Step 16: Dynamic Programming
    ("chapter-26-dynamic-programming", "chapter-18-dynamic-programming"),
    # Step 17: Tries
    ("chapter-16-tries", "chapter-19-tries"),
    # Step 18: Strings (Advanced Algo)
    ("chapter-05-strings", "chapter-20-strings"),
    ("chapter-24-string-algorithms", "chapter-21-string-algorithms"),
    # Step 19: Maths
    ("chapter-30-mathematical-algorithms", "chapter-22-mathematical-algorithms"),

    # --- Remaining Topics (Not directly in Problem List steps) ---
    ("chapter-02-complexity-analysis", "chapter-23-complexity-analysis"),
    ("chapter-03-java-for-dsa", "chapter-24-java-for-dsa"),
    ("chapter-14-avl-trees", "chapter-25-avl-trees"),
    ("chapter-15-red-black-trees", "chapter-26-red-black-trees"),
    ("chapter-17-segment-trees", "chapter-27-segment-trees"),
    ("chapter-18-dsu", "chapter-28-dsu"),
    ("chapter-19-fenwick-tree", "chapter-29-fenwick-tree"),
    ("chapter-28-branch-and-bound", "chapter-30-branch-and-bound")
]

print(f"Total mapped folders: {len(ORDER_MAPPING)}")

old_names = [x[0] for x in ORDER_MAPPING]
new_names = [x[1] for x in ORDER_MAPPING]

# Validation
missing_in_mapping = set(existing_folders) - set(old_names)
extra_in_mapping = set(old_names) - set(existing_folders)
duplicate_new = len(new_names) - len(set(new_names))

print(f"Missing in mapping: {missing_in_mapping}")
print(f"Extra in mapping: {extra_in_mapping}")
print(f"Duplicate new names: {duplicate_new}")
