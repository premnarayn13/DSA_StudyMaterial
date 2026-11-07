import json
import re
from collections import Counter

# Exact GFG title -> Striver problem identifier (substring or exact title in Striver)
GFG_DUPLICATE_TARGETS = {
    # Arrays
    "Find the maximum and minimum element in an array": "Largest Element",
    "find duplicate in an array of N+1 Integers": "Find the duplicate in an array of N+1 integers",
    "Spiral traversal on a Matrix": "Print the matrix in spiral manner",
    
    # Strings
    "Write a program to find the longest Palindrome in a string.": "Longest Palindromic Substring",
    "Find Longest Recurring Subsequence in String": "Longest Repeating Subsequence",
    "Print all the permutations of the given string": "Print all Permutations",
    "Word break Problem": "Word Break",
    "Rabin Karp Algo": "Rabin Karp Algorithm",
    "KMP Algo": "KMP Algorithm or LPS array",
    "Count All Palindromic Subsequence in a given String.": "Longest palindromic subsequence",
    "Search a Word in a 2D Grid of characters.": "Word Search",
    "Find first and last positions of an element in a sorted array": "First and last occurrence",
    "Product array Puzzle": "Product of Array Except Self",
    
    # LinkedList
    "Write a Program to reverse the Linked List. (Both Iterative and recursive)": "Reverse a LL",
    "Reverse a Linked List in group of Given Size.": "Reverse LL in group of given size K",
    "Remove Duplicates in a sorted Linked List.": "Remove duplicates from sorted DLL",
    "Add “1” to a number represented as a Linked List.": "Add 1 to a number represented by LL",
    "Add two numbers represented by linked lists.": "Add two numbers represented by LL",
    "Intersection of two Sorted Linked List.": "Intersection of two Linked Lists",
    "Intersection Point of two Linked Lists.": "Intersection of two Linked Lists",
    "Merge Sort For Linked lists.": "Sort a LL",
    "Write a Program to check whether the Singly Linked list is a palindrome or not.": "Check if LL is palindrome or not",
    "Reverse a Doubly Linked list.": "Reverse a DLL",
    "Clone a linked list with next and random pointer": "Clone a LL with random and next pointer",
    "Merge K sorted Linked list": "Merge M sorted Lists",
    "Segregate even and odd nodes in a Linked List": "Segregate even and odd nodes in LL",
    "Program for n’th node from the end of a Linked List": "Remove Nth node from the back of the LL",
    "Find the first non-repeating character from a stream of characters": "First non-repeating character in a stream of characters",
    
    # Binary Trees
    "Reverse Level Order traversal": "Reverse Level Order Traversal",
    "Height of a tree": "Maximum Depth in BT",
    "Mirror of a tree": "Invert Binary Tree",
    "Left View of a tree": "Left/Right View of Binary Tree",
    "Right View of Tree": "Left/Right View of Binary Tree",
    "Zig-Zag traversal of a binary tree": "Zig Zag or Spiral Traversal",
    "Boundary traversal of a Binary tree": "Boundary Traversal",
    "Construct Binary tree from Inorder and preorder traversal": "Construct Binary Tree from Inorder and Preorder Traversal",
    "Check if 2 trees are mirror or not": "Check if two trees are identical or not",
    "Find LCA in a Binary tree": "LCA in BT",
    
    # BST
    "Fina a value in a BST": "Search in BST",
    "Find min and max value in a BST": "Find Min/Max in BST",
    "Find inorder successor and inorder predecessor in a BST": "Inorder Predecessor and Successor in BST",
    "Populate Inorder Successor for all nodes": "Populate Next Right Pointers of Tree",
    "Find LCA  of 2 nodes in a BST": "LCA in BST",
    "Construct BST from preorder traversal": "Construct BST from Preorder Traversal",
    "Convert a normal BST into a Balanced BST": "Balance a Binary Search Tree",
    "Find K-th largest element in BST": "Kth Smallest and Largest element in BST",
    "Find K-th smallest element in BST": "Kth Smallest and Largest element in BST",
    "Count pairs from 2 BST whose sum is equal to given value \"X\"": "Two Sum IV - Input is a BST",
    "Check whether BST contains Dead End": "Check whether BST contains Dead End",
    "Largest BST in a Binary Tree": "Maximum Sum BST in Binary Tree",
    
    # Greedy
    "activity selection problem": "N meetings in one room",
    "Fractional Knapsack Problem": "Fractional Knapsack",
    "Find maximum meetings in one room": "N meetings in one room",
    "Minimum Platforms Problem": "Minimum Platforms",
    "Buy Maximum Stocks if i stocks can be bought on i-th day": "Best Time to Buy and Sell Stock",
    
    # Backtracking
    "Rat in a Maze Problem": "Rat in a Maze",
    "Printing all solutions in N-Queen Problem": "N-Queen Problem",
    "Word Break Problem using Backtracking": "Word Break",
    "m Coloring Problem": "M-Coloring Problem",
    "Subset Sum Problem": "Subset Sum Equal to K",
    
    # Stacks & Queues
    "the celebrity problem": "Celebrity Problem",
    "evaluation of postfix expression": "Evaluation of Postfix Expression",
    "insert at the bottom of a stack": "Insert an Element at the Bottom of a Stack",
    "Reverse a Stack using recursion": "Reverse a Stack using Recursion",
    "Sort a Stack using recursion": "Sort a Stack using Recursion",
    "Merge Overlapping Intervals": "Merge Overlapping Subintervals",
    "Largest rectangular Area in Histogram": "Largest Rectangle in Histogram",
    "Next Greater Element": "Next Greater Element",
    "Next Smaller Element": "Next Smaller Element",
    "distance of nearest cell having 1": "Distance of nearest cell having one",
    "First negative integer in every window of size “k”": "Sliding Window Maximum",
    
    # Heaps
    "kth smallest and largest element in an unsorted array": "K-th Largest element in an array",
    "Merge “k” sorted arrays, [  merged_k ]": "Merge M sorted Lists",
    "Merge 2 binary Max Heaps": "Merge two binary Max heaps",
    "kth largest sum continuous subarrays": "K-th Largest element in an array",
    "Reorganize String": "Reorganize String",
    "Connect “n” ropes with minimum cost": "Minimum Cost to connect ropes",
    "convert min Heap to max heap": "Convert Min Heap to Max Heap",
    
    # Graph
    "Implement BFS algorithm": "Traversal Techniques",
    "Implement DFS Algo": "Traversal Techniques",
    "Detect cycle in directed graph using BFS/DFS Algo": "Detect a cycle in a directed graph",
    "Detect cycle in an undirected graph using BFS/DFS Algo": "Detect a cycle in an undirected graph",
    "Minimum Step by Knight": "Knight Walk",
    "Flood fill Algo": "Flood fill algorithm",
    "Clone a graph": "Clone Graph",
    "Making Wired Connections": "Number of operations to make network connected",
    "word ladder": "Word Ladder 'I'",
    "Dijkstra Algo": "Dijkstra's Algorithm",
    "Topological sort": "Topological sort or Kahn's algorithm",
    "Find the no. of Isalnds": "Number of islands",
    "Alien Dictionary": "Alien dictionary",
    "Implement Kruksal’sAlgorithm": "Minimum Spanning Tree (Kruskal's Algorithm)",
    "Implement Prim’s Algorithm": "Prim's Algorithm",
    "Implement Bellman Ford Algorithm": "Bellman Ford Algorithm",
    "Implement Floyd warshall Algorithm": "Floyd Warshall Algorithm",
    "Cheapest Flights Within K Stops": "Cheapest Flights Within K Stops",
    "Find bridge in a graph": "Bridges in Graph",
    "Check whether a graph is Bipartite or Not": "Bipartite graph",
    "Detect Negative cycle in a graph": "Bellman Ford Algorithm",
    
    # Dynamic Programming
    "0 - 1 Knapsack Problem": "0/1 Knapsack",
    "Longest Common Subsequence": "Longest Common Subsequence",
    "Longest Repeated Subsequence": "Longest Repeating Subsequence",
    "Egg Dropping Problem": "Egg Dropping Problem",
    "Maximum profit by buying and selling a share at most twice": "Best Time to Buy and Sell Stock III",
    "Palindrome PartitioningProblem": "Palindrome partitioning II",
    "Boolean Parenthesization Problem": "Boolean Parenthesization",
    "Maximum sum rectangle in a 2D matrix": "Maximal Rectangle",
    
    # Bit Manipulation
    "Count set bits in an integer": "Count total set bits",
    "Find the two non-repeating elements in an array of repeating elements": "Two numbers with odd occurrences",
    "count total set bits in all numbers from 1 to n": "Count total set bits",
    "Program to find whether a no is power of two": "Power of Two",
    "Find position of the only set bit": "Find position of only set bit",
    "Copy set bits in a range": "Check if the i-th bit is set or not",
    "divide two integers without using multiplication, division and mod operator": "Divide Two Integers",
    
    # Trie
    "Construct a trie from scratch": "Implement Trie : Insert, Search, StartsWith",
    "Word Break Problem | (Trie solution)": "Word Break",
    "Given a sequence of words, print all anagrams together": "Group Anagrams",
    "Implement a Phone Directory": "Implement Trie - II"
}

# 16 Discarded items (theory, non-coding, dead contest links)
DISCARD_TITLES = [
    "why strings are immutable in java?",
    "write a program to check whether a string is a valid shuffle of two strings or not",
    "find pivot element in a sorted array",
    "function to find number of customers who could not get a computer",
    "bishu and soldiers",
    "rasta and kheshtak",
    "kth smallest number again",
    "ekospoj:",
    "defkin -defense of a kingdom",
    "diehard -die hard",
    "gergovia -wine trading in gergovia",
    "picking up chicks",
    "chocola",
    "arrange -arranging amplifiers",
    "oliver and the game",
    "can we reverse a linked list in less than o(n) ?",
    "why quicksort is preferred for. arrays and merge sort for linkedlists ?"
]

def norm(s):
    if not s: return ''
    s = s.lower()
    s = re.sub(r'\[.*?\]', '', s)
    s = s.replace('“', '"').replace('”', '"').replace('’', "'")
    s = re.sub(r'[^a-z0-9]', '', s)
    return s

def run_curation():
    # Load 693 dataset
    with open('site/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
    gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

    striver_by_norm = {norm(p['title']): p for p in striver_core}
    norm_dup_targets = {norm(k): norm(v) for k, v in GFG_DUPLICATE_TARGETS.items()}

    merged_duplicates = 0
    discarded = 0
    kept_gfg = []

    for g in gfg_added:
        t_raw = g['title'].strip()
        t_clean = re.sub(r'\[.*?\]', '', t_raw).strip().lower()
        k = norm(t_raw)

        # 1. Check if discarded
        if any(d in t_clean for d in DISCARD_TITLES):
            discarded += 1
            continue

        # 2. Check if duplicate of Striver core
        matched_striver = None
        if k in norm_dup_targets:
            target_norm = norm_dup_targets[k]
            matched_striver = striver_by_norm.get(target_norm)
            if not matched_striver:
                # Substring fallback
                for sp in striver_core:
                    if target_norm in norm(sp['title']) or norm(sp['title']) in target_norm:
                        matched_striver = sp
                        break
        elif k in striver_by_norm:
            matched_striver = striver_by_norm[k]

        if matched_striver:
            # Merge GFG link into Striver problem's altUrls
            g_url = g.get('url', '').strip()
            if g_url and 'geeksforgeeks.org' in g_url:
                alt_urls = matched_striver.setdefault('altUrls', [])
                all_existing = [matched_striver.get('url', '')] + [a.get('url', '') for a in alt_urls]
                if g_url not in all_existing:
                    alt_urls.append({'platform': 'gfg', 'url': g_url})
            merged_duplicates += 1
        else:
            # Clean character encoding in title
            t_cleaned = t_raw.replace(chr(65533), "'").strip()
            t_cleaned = re.sub(r'\[.*?\]', '', t_cleaned).strip()
            g['title'] = t_cleaned
            kept_gfg.append(g)

    final_problems = striver_core + kept_gfg

    # Re-order
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

    print("================ FINAL CURATION REPORT ================")
    print(f"Striver Core Problems: {len(striver_core)}")
    print(f"GFG Duplicates Merged into AltUrls: {merged_duplicates}")
    print(f"Trivia / Dead Contest Links Discarded: {discarded}")
    print(f"GFG Standard Practice Problems Kept: {len(kept_gfg)}")
    print(f"TOTAL PROBLEMS IN SHEET: {len(final_problems)}")
    print("=======================================================")

if __name__ == '__main__':
    run_curation()
