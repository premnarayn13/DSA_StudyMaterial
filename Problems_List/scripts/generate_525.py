import json
import re
from collections import Counter

# 1. Restore clean 693 data
with open('site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Priority GFG problems to keep (top algorithmic questions from Love Babbar 450)
# We want ~120-125 of the highest quality standard problems to reach ~525 total.
HIGH_STANDARD_GFG_KEYWORDS = [
    # DP & Games
    "word wrap", "optimal strategy for a game", "boolean parenthesization", "optimal binary search tree",
    "gold mine", "longest path in a directed acyclic graph", "maximum profit by buying and selling",
    "longest alternating subsequence", "reach a given score", "count derangements", "maximum sum increasing subsequence",
    "bb counter", "matrix chain multiplication", "coin change", "edit distance", "subset sum",
    
    # Backtracking & Recursion
    "remove invalid parentheses", "partition of a set into", "longest possible route in a matrix with hurdles",
    "find maximum number possible by doing at-most k swaps", "print all palindromic partitions",
    "print all permutations", "m coloring", "rat in a maze", "sudoku solver", "knight", "word boggle",
    "tug of war", "k-th permutation sequence",
    
    # Arrays, Two Pointers, Sliding Window
    "minimum no. of jumps to reach end", "find common elements in 3 sorted arrays",
    "rearrange the array in alternating positive and negative", "appear more than \" n/k \" times",
    "smallest subarray with sum greater than a given value", "minimum swaps required bring elements less equal k together",
    "kth smallest element in a row", "chocolate distribution", "triplet sum in array", "trapping rain water",
    "maximum product subarray", "longest consecutive subsequence",
    
    # Strings
    "boyer moore algorithm for pattern searching", "smallest window that contains all characters of string itself",
    "minimum characters to be added at front to make string palindrome", "smallest window in a string containing all characters",
    "string matching where one string contains wildcard characters", "length of the longest valid substring",
    "count and say", "look-and-say", "permutations of a given string", "longest common prefix",
    "search a word in a 2d grid", "generate all possible valid ip",
    
    # Trees & BST
    "sum of nodes on the longest path from root to leaf", "maximum sum of nodes in binary tree such that no two are adjacent",
    "print all \"k\" sum paths in a binary tree", "diagnol traversal of a binary tree", "distance between 2 nodes in a binary tree",
    "kth ancestor of node in a binary tree", "find all duplicate subtrees in a binary tree", "tree isomorphism problem",
    "check if binary tree is sum tree", "check if all leaf nodes are at same level",
    "flatten bst to sorted list", "replace every element with the least greater element on its right",
    "count bst ndoes that lie in a given range", "check preorder is valid or not", "populate inorder successor",
    
    # Graphs
    "minimum cost to cut a board into squares", "job scheduling algo", "minimum steps by knight",
    "oliver and the game", "travelling salesman", "minimum time taken by each job to be completed",
    "find whether it is possible to finish all tasks", "steps by knight", "path of greater than equal to k length",
    "water jug problem", "word ladder", "journey to the moon", "cheapest flights",
    
    # Stacks, Queues, Heaps
    "smallest range in", "sum of minimum and maximum elements of all subarrays of size",
    "minimum sum of two numbers formed from digits of an array", "reorganize string",
    "k largest elements", "merge k sorted arrays", "sliding window maximum",
    "next smaller element", "the celebrity problem", "reverse a stack using recursion",
    "sort a stack using recursion", "interleave the first half of the queue",
    "reverse first k elements of queue", "distance of nearest cell having 1",
    
    # Linked List
    "split a circular linked list into two halves", "quicksort for linked lists",
    "sort a “k”sorted doubly linked list", "rotate doublylinked list by n nodes",
    "rotate a doubly linked list in group of given size", "flatten a multilevel linked list",
    "clone a linked list with next and random pointer", "merge sort for linked lists"
]

def clean_key(s):
    if not s: return ''
    s = s.lower()
    s = re.sub(r'\[.*?\]', '', s)
    s = s.replace('“', '"').replace('”', '"').replace('’', "'")
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def run():
    with open('site/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
    gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

    # Filter GFG to exactly high-standard problems to hit ~525 total
    target_total = 525
    gfg_target_count = target_total - len(striver_core) # 123

    # Score each GFG problem based on match with high standard keywords
    selected_gfg = []
    seen_titles = set()

    for g in gfg_added:
        t_clean = g['title'].lower()
        # Skip pure trivia/dead
        if any(bad in t_clean for bad in ['why strings are immutable', 'why quicksort is preferred', 'can we reverse a linked list in less']):
            continue
        
        # Check if matches any keyword
        for kw in HIGH_STANDARD_GFG_KEYWORDS:
            if kw in t_clean and g['id'] not in seen_titles:
                seen_titles.add(g['id'])
                selected_gfg.append(g)
                break

    # If count is slightly off target, trim or top-up cleanly
    if len(selected_gfg) > gfg_target_count:
        selected_gfg = selected_gfg[:gfg_target_count]
    elif len(selected_gfg) < gfg_target_count:
        for g in gfg_added:
            if g['id'] not in seen_titles and len(selected_gfg) < gfg_target_count:
                t_clean = g['title'].lower()
                if not any(bad in t_clean for bad in ['why strings are immutable', 'why quicksort is preferred', 'can we reverse']):
                    selected_gfg.append(g)
                    seen_titles.add(g['id'])

    # Clean titles
    for g in selected_gfg:
        t = g['title'].replace(chr(65533), "'").strip()
        t = re.sub(r'\[.*?\]', '', t).strip()
        g['title'] = t

    final_problems = striver_core + selected_gfg

    # Re-order 1 to N
    for idx, p in enumerate(final_problems, start=1):
        p['order'] = idx

    data['problems'] = final_problems
    data['meta']['problemCount'] = len(final_problems)

    # Step counts
    step_counts = Counter(p['step'] for p in final_problems)
    for s in data['meta'].get('steps', []):
        s['count'] = step_counts.get(s['n'], 0)

    with open('site/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("================ FINAL LIST GENERATED ================")
    print(f"Striver Core Problems: {len(striver_core)}")
    print(f"Standard GFG Practice Problems: {len(selected_gfg)}")
    print(f"TOTAL PROBLEMS: {len(final_problems)}")
    print("======================================================")

if __name__ == '__main__':
    run()
