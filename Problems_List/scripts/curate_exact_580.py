import json
import re
from collections import Counter

# Exact verified duplicates from GFG 450 to Striver core problems
# (GFG Title -> Striver Exact Slug or exact title)
EXACT_DUPLICATE_MAP = {
    # Trees
    "Reverse level order traversal": "reverse-level-order-traversal",
    "Height of a tree": "height-of-a-binary-tree",
    "Left view of a tree": "left-view-of-binary-tree",
    "Right view of tree": "right-view-of-binary-tree",
    "Zig-zag traversal of a binary tree": "zigzag-level-order-traversal",
    "Boundary traversal of a binary tree": "boundary-traversal-of-binary-tree",
    "Convert binary tree into Doubly Linked List": "binary-tree-to-dll",
    "Construct Binary tree from Inorder and preorder traversal": "construct-binary-tree-from-preorder-and-inorder-traversal",
    "Find LCA in a Binary tree": "lowest-common-ancestor-of-a-binary-tree",
    "Find min and max value in a BST": "minimum-element-in-bst",
    "Find LCA  of 2 nodes in a BST": "lowest-common-ancestor-of-a-binary-search-tree",
    "Construct BST from preorder traversal": "construct-binary-search-tree-from-preorder-traversal",
    "Count BST ndoes that lie in a given range": "range-sum-of-bst",
    "Largest BST in a Binary Tree": "maximum-sum-bst-in-binary-tree",
    
    # Graphs
    "Implement BFS algorithm": "bfs-traversal-of-graph",
    "Implement DFS Algo": "dfs-traversal-of-graph",
    "Detect cycle in directed graph using BFS/DFS Algo": "detect-cycle-in-a-directed-graph",
    "Detect cycle in an undirected graph using BFS/DFS Algo": "detect-cycle-in-an-undirected-graph",
    "Rat in a Maze Problem": "rat-in-a-maze-problem",
    "Minimum Step by Knight": "knight-walk",
    "Flood fill Algo": "flood-fill",
    "Clone a graph": "clone-graph",
    "Making Wired Connections": "number-of-operations-to-make-network-connected",
    "word ladder": "word-ladder",
    "Dijkstra Algo": "dijkstras-algorithm",
    "Topological sort": "topological-sort",
    "Find the no. of Isalnds": "find-the-number-of-islands",
    "Alien Dictionary": "alien-dictionary",
    "Implement Kruksal’sAlgorithm": "minimum-spanning-tree-kruskals-algorithm",
    "Implement Prim’s Algorithm": "minimum-spanning-tree-prims-algorithm",
    "Implement Bellman Ford Algorithm": "bellman-ford-algorithm",
    "Implement Floyd warshall Algorithm": "floyd-warshall",
    "Cheapest Flights Within K Stops": "cheapest-flights-within-k-stops",
    "Find bridge in a graph": "critical-connections-in-a-network",
    "Check whether a graph is Bipartite or Not": "is-graph-bipartite",
    "Detect Negative cycle in a graph": "bellman-ford-algorithm",

    # Stacks & Queues
    "the celebrity problem": "the-celebrity-problem",
    "evaluation of postfix expression": "evaluation-of-postfix-expression",
    "insert at the bottom of a stack": "insert-an-element-at-the-bottom-of-a-stack",
    "reverse a stack using recursion": "reverse-a-stack",
    "sort a stack using recursion": "sort-a-stack",
    "merge overlapping intervals": "merge-overlapping-intervals",
    "largest rectangular area in histogram": "largest-rectangle-in-histogram",
    "find the next greater element": "next-greater-element",
    "expression contains redundant bracket or not": "redundant-brackets",
    "next smaller element": "next-smaller-element",
    "distance of nearest cell having 1": "01-matrix",

    # Greedy
    "activity selection problem": "n-meetings-in-one-room",
    "fractional knapsack problem": "fractional-knapsack",
    "find maximum meetings in one room": "n-meetings-in-one-room",
    "minimum platforms problem": "minimum-platforms",
    "buy maximum stocks if i stocks can be bought on i-th day": "best-time-to-buy-and-sell-stock",

    # Dynamic Programming
    "0 - 1 knapsack problem": "0-1-knapsack-problem",
    "longest common subsequence": "longest-common-subsequence",
    "longest repeated subsequence": "longest-repeating-subsequence",
    "egg dropping problem": "super-egg-drop",
    "maximum profit by buying and selling a share at most twice": "best-time-to-buy-and-sell-stock-iii",
    "palindrome partitioningproblem": "palindrome-partitioning-ii",
    
    # Linked List
    "write a program to reverse the linked list. (both iterative and recursive)": "reverse-linked-list",
    "reverse a linked list in group of given size.": "reverse-nodes-in-k-group",
    "remove duplicates in a sorted linked list.": "remove-duplicates-from-sorted-list",
    "remove duplicates in a un-sorted linked list.": "remove-duplicates-from-unsorted-linked-list",
    "add “1” to a number represented as a linked list.": "add-1-to-a-number-represented-as-linked-list",
    "add two numbers represented by linked lists.": "add-two-numbers",
    "intersection of two sorted linked list.": "intersection-of-two-sorted-linked-lists",
    "intersection point of two linked lists.": "intersection-of-two-linked-lists",
    "merge sort for linked lists.": "sort-list",
    "write a program to check whether the singly linked list is a palindrome or not.": "palindrome-linked-list",
    "reverse a doubly linked list.": "reverse-a-doubly-linked-list",
    "clone a linked list with next and random pointer": "copy-list-with-random-pointer",
    "merge k sorted linked list": "merge-k-sorted-lists",
    "segregate even and odd nodes in a linked list": "odd-even-linked-list",
    "program for n’th node from the end of a linked list": "remove-nth-node-from-end-of-list",

    # Strings
    "rabin karp algo": "rabin-karp-algorithm",
    "kmp algo": "kmp-algorithm-or-lps-array",
    "search a word in a 2d grid of characters.": "word-search",
    "split the binary string into two substring with equal 0’s and 1’s": "split-the-binary-string-into-substrings-with-equal-number-of-0s-and-1s",
    "convert a sentence into its equivalent mobile numeric keypad sequence.": "convert-sentence-equivalent-mobile-numeric-keypad-sequence",

    # Bit Manipulation
    "count set bits in an integer": "count-total-set-bits",
    "find the two non-repeating elements in an array of repeating elements": "two-numbers-with-odd-occurrences",
    "count total set bits in all numbers from 1 to n": "count-total-set-bits",
    "program to find whether a no is power of two": "power-of-two",
    "find position of the only set bit": "find-position-of-only-set-bit",
    "copy set bits in a range": "check-if-the-i-th-bit-is-set-or-not",
    "divide two integers without using multiplication, division and mod operator": "divide-two-integers",

    # Trie
    "construct a trie from scratch": "implement-trie-prefix-tree",
    "word break problem | (trie solution)": "word-break",
    "given a sequence of words, print all anagrams together": "group-anagrams",
    "implement a phone directory": "implement-trie-ii"
}

# Obsolete / Non-coding / Dead external items
DISCARD_ITEMS = [
    "why strings are immutable in java?",
    "write a program to check whether a string is a valid shuffle of two strings or not",
    "find pivot element in a sorted array",
    "function to find number of customers who could not get a computer",
    "dishu and soldiers",
    "rasta and kheshtak",
    "kth smallest number again",
    "ekospoj:",
    "defkin -defense of a kingdom",
    "diehard -die hard",
    "gergovia -wine trading in gergovia",
    "picking up chicks",
    "chocola",
    "arrange -arranging amplifiers",
    "oliver and the game"
]

def clean_key(s):
    if not s: return ''
    s = s.lower()
    s = re.sub(r'\[.*?\]', '', s)
    s = s.replace('“', '"').replace('”', '"').replace('’', "'")
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def run():
    # 1. Restore clean 693 data
    with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
    gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

    striver_by_slug = {p.get('slug', ''): p for p in striver_core}
    striver_by_lc_slug = {p.get('lcSlug', ''): p for p in striver_core}
    striver_by_key = {clean_key(p['title']): p for p in striver_core}

    norm_dup_map = {clean_key(k): v for k, v in EXACT_DUPLICATE_MAP.items()}

    merged_duplicates = 0
    discarded = 0
    kept_gfg = []

    for g in gfg_added:
        t_raw = g['title'].strip()
        t_clean = re.sub(r'\[.*?\]', '', t_raw).strip().lower()
        k = clean_key(t_raw)

        # 1. Check if discarded
        if any(d in t_clean for d in DISCARD_ITEMS):
            discarded += 1
            continue

        # 2. Check if verified duplicate of Striver
        matched_striver = None
        if k in norm_dup_map:
            target_slug = norm_dup_map[k]
            matched_striver = striver_by_slug.get(target_slug) or striver_by_lc_slug.get(target_slug) or striver_by_key.get(clean_key(target_slug))
        elif k in striver_by_key:
            matched_striver = striver_by_key[k]

        if matched_striver:
            # Merge GFG link into Striver altUrls
            g_url = g.get('url', '').strip()
            if g_url and 'geeksforgeeks.org' in g_url:
                alt_urls = matched_striver.setdefault('altUrls', [])
                all_existing = [matched_striver.get('url', '')] + [a.get('url', '') for a in alt_urls]
                if g_url not in all_existing:
                    alt_urls.append({'platform': 'gfg', 'url': g_url})
            merged_duplicates += 1
        else:
            # Keep as distinct high-standard problem
            t_cleaned = t_raw.replace(chr(65533), "'").strip()
            t_cleaned = re.sub(r'\[.*?\]', '', t_cleaned).strip()
            g['title'] = t_cleaned
            kept_gfg.append(g)

    final_problems = striver_core + kept_gfg

    # Re-order 1 to N
    for idx, p in enumerate(final_problems, start=1):
        p['order'] = idx

    data['problems'] = final_problems
    data['meta']['problemCount'] = len(final_problems)

    # Step counts
    step_counts = Counter(p['step'] for p in final_problems)
    for s in data['meta'].get('steps', []):
        s['count'] = step_counts.get(s['n'], 0)

    with open('d:/DSA/Problems_List/site/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("================ CURATION COMPLETED ================")
    print(f"Striver Core Problems: {len(striver_core)}")
    print(f"GFG Duplicates Merged into AltUrls: {merged_duplicates}")
    print(f"Trivia / Dead Links Discarded: {discarded}")
    print(f"GFG Standard Practice Questions Kept: {len(kept_gfg)}")
    print(f"TOTAL FINAL PROBLEMS IN SHEET: {len(final_problems)}")
    print("====================================================")

if __name__ == '__main__':
    run()
