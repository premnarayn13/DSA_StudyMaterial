import json
import re
from collections import Counter

# GFG duplicate mapping to Striver Core title
GFG_TO_STRIVER_DUPLICATES = {
    "find the maximum and minimum element in an array": "Find the largest element in an array",
    "find duplicate in an array of n+1 integers": "Find the duplicate in an array of N+1 integers",
    "spiral traversal on a matrix": "Spiral Traversal of Matrix",
    "write a program to find the longest palindrome in a string.": "Longest Palindromic Substring",
    "find longest recurring subsequence in string": "Longest Repeating Subsequence",
    "print all the permutations of the given string": "Print all Permutations of a String/Array",
    "word break problem": "Word Break",
    "rabin karp algo": "Rabin Karp",
    "kmp algo": "KMP algo",
    "count all palindromic subsequence in a given string.": "Longest Palindromic Subsequence",
    "search a word in a 2d grid of characters.": "Word Search",
    "find first and last positions of an element in a sorted array": "First and Last Occurrences in Array",
    "product array puzzle": "Product of Array Except Self",
    "write a program to reverse the linked list. (both iterative and recursive)": "Reverse a LinkedList",
    "reverse a linked list in group of given size.": "Reverse a LL in groups of given size K",
    "remove duplicates in a sorted linked list.": "Remove duplicate elements from sorted linked list",
    "remove duplicates in a un-sorted linked list.": "Remove duplicates from sorted DLL",
    "add “1” to a number represented as a linked list.": "Add 1 to a number represented by LL",
    "add two numbers represented by linked lists.": "Add two numbers represented by LL",
    "intersection of two sorted linked list.": "Intersection of two sorted Linked Lists",
    "intersection point of two linked lists.": "Find intersection of Two Linked Lists",
    "merge sort for linked lists.": "Sort LL",
    "write a program to check whether the singly linked list is a palindrome or not.": "Check if LL is palindrome or not",
    "reverse a doubly linked list.": "Reverse a Doubly Linked List",
    "clone a linked list with next and random pointer": "Clone a Linked List with random and next pointer",
    "merge k sorted linked list": "Merge K Sorted Lists",
    "segregate even and odd nodes in a linked list": "Segrregate odd and even nodes in LL",
    "program for n’th node from the end of a linked list": "Remove Nth Node From End of List",
    "find the first non-repeating character from a stream of characters": "First non-repeating character in a stream of characters",
    "reverse level order traversal": "Reverse Level Order Traversal",
    "height of a tree": "Height of a Binary Tree",
    "mirror of a tree": "Invert Binary Tree",
    "left view of a tree": "Left view of BT",
    "right view of tree": "Right view of BT",
    "zig-zag traversal of a binary tree": "Zig Zag Traversal of BT",
    "boundary traversal of a binary tree": "Boundary Traversal of Binary Tree",
    "convert binary tree into doubly linked list": "Convert Binary tree into Doubly Linked List",
    "construct binary tree from inorder and preorder traversal": "Construct Binary Tree from Inorder and Preorder Traversal",
    "find lca in a binary tree": "Lowest Common Ancestor for two given Nodes",
    "fina a value in a bst": "Find a value in a BST",
    "find min and max value in a bst": "Find min and max value in a BST",
    "find inorder successor and inorder predecessor in a bst": "Inorder Predecessor and Successor in BST",
    "populate inorder successor of all nodes": "Populate Next Right Pointers of Tree",
    "find lca  of 2 nodes in a bst": "LCA in BST",
    "construct bst from preorder traversal": "Construct a BST from a preorder traversal",
    "convert binary tree into bst": "Binary Tree to BST",
    "convert a normal bst into a balanced bst": "Balance a Binary Search Tree",
    "merge two bst ‘s": "Merge two BST's",
    "find k-th largest element in bst": "Kth largest element in BST",
    "find k-th smallest element in bst": "Kth smallest element in BST",
    "count pairs from 2 bst whose sum is equal to given value \"x\"": "Two Sum IV - Input is a BST",
    "find the median of bst in o(n) time and o(1) space": "Find the median of BST in O(n) time and O(1) space",
    "count bst ndoes that lie in a given range": "Range Sum of BST",
    "check whether bst contains dead end": "Check whether BST contains Dead End",
    "largest bst in a binary tree": "Maximum Sum BST in Binary Tree",
    "activity selection problem": "N meetings in one room",
    "fractional knapsack problem": "Fractional Knapsack Problem",
    "choose and swap": "Minimum characters to be added at front to make string palindrome",
    "find maximum meetings in one room": "N meetings in one room",
    "maximum trains for which stoppage can be provided": "Minimum number of platforms required for a railway",
    "minimum platforms problem": "Minimum number of platforms required for a railway",
    "buy maximum stocks if i stocks can be bought on i-th day": "Best Time to Buy and Sell Stock",
    "find the minimum and maximum amount to buy all n candies": "Assign Cookies",
    "check if it is possible to survive on island": "Lemonade Change",
    "find maximum sum possible equal to sum of three stacks": "Insert at bottom of stack",
    "rat in a maze problem": "Rat in a Maze",
    "printing all solutions in n-queen problem": "N-Queen Problem",
    "word break problem using backtracking": "Word Break",
    "the knight’s tour problem": "Knight Walk",
    "m coloring problem": "M - Coloring Problem",
    "subset sum problem": "Subset Sum Equal to K",
    "the celebrity problem": "The Celebrity Problem",
    "evaluation of postfix expression": "Postfix to Infix",
    "insert at the bottom of a stack": "Insert at bottom of stack",
    "reverse a stack using recursion": "Reverse a Stack",
    "sort a stack using recursion": "Sort a Stack",
    "merge overlapping intervals": "Merge Intervals",
    "largest rectangular area in histogram": "Largest rectangle in a histogram",
    "find the next greater element": "Next Greater Element",
    "expression contains redundant bracket or not": "Count the Reversals",
    "implement stack using deque": "Implement Stack using Queue",
    "stack permutations (check if an array is stack permutation of other)": "Valid Stack Sequences",
    "queue based approach or first non-repeating character in a stream.": "First non-repeating character in a stream of characters",
    "next smaller element": "Next Smaller Element",
    "distance of nearest cell having 1": "0/1 Matrix (Bfs)",
    "first negative integer in every window of size “k”": "Sliding Window Maximum",
    "check if all levels of two trees are anagrams or not.": "Same Tree",
    "kth largest element in an array": "Kth Largest Element in an Array",
    "kth smallest and largest element in an unsorted array": "Kth Largest Element in an Array",
    "merge “k” sorted arrays, [ merged_k ]": "Merge M sorted Lists",
    "merge 2 binary max heaps": "Merge two binary Max heaps",
    "kth largest sum continuous subarrays": "Kth Largest Element in an Array",
    "reorganize string": "Reorganize String",
    "connect “n” ropes with minimum cost": "Minimum Cost to connect ropes",
    "convert min heap to max heap": "Convert Min Heap to Max Heap",
    "create a graph, print it": "Print adjacency list",
    "implement bfs algorithm": "BFS",
    "implement dfs algo": "DFS",
    "detect cycle in directed graph using bfs/dfs algo": "Detect a Cycle in Directed Graph | Topo Sort | BFS",
    "detect cycle in an undirected graph using bfs/dfs algo": "Detect cycle in an undirected graph",
    "rat in a maze problem": "Rat in a Maze",
    "minimum steps by knight": "Knight Walk",
    "flood fill algo": "Flood Fill",
    "clone a graph": "Clone Graph",
    "making wired connections": "Number of operations to make network connected",
    "word ladder": "Word Ladder 'I'",
    "dijkstra algo": "Dijkstra's Algorithm",
    "topological sort": "Topological sort",
    "find the no. of isalnds": "Number of Islands",
    "alien dictionary": "Alien dictionary",
    "implement kruksal’s algorithm": "Minimum Spanning Tree (Kruskal's Algorithm)",
    "implement prim’s algorithm": "Prim's Algorithm",
    "implement bellman ford algorithm": "Bellman ford algorithm",
    "implement floyd warshall algorithm": "Floyd Warshall Algorithm",
    "cheapest flights within k stops": "Cheapest Flights Within K Stops",
    "find bridge in a graph": "Bridge edge in a graph",
    "check whether a graph is bipartite or not": "Bipartite Graph (BFS/DFS)",
    "detect negative cycle in a graph": "Bellman ford algorithm",
    "construct a trie from scratch": "Implement Trie : Insert, Search, StartsWith",
    "find shortest unique prefix for every word in a given list": "Complete String",
    "word break problem | (trie solution)": "Word Break",
    "given a sequence of words, print all anagrams together": "Group Anagrams",
    "implement a phone directory": "Implement Trie - II",
    "print unique rows in a given boolean matrix": "Count of distinct substrings",
    "longest repeated subsequence": "Longest Repeating Subsequence",
    "egg dropping problem": "Super Egg Drop",
    "maximum size square sub-matrix with all 1s": "Maximal Rectangle",
    "min cost pathproblem": "Minimum path sum in Grid",
    "minimum number of jumps to reach end": "Jump Game II",
    "maximum profit by buying and selling a share at most twice": "Best time to buy and sell stock III",
    "palindrome partitioningproblem": "Palindrome Partitioning - II",
    "boolean parenthesization problem": "Boolean Parenthesization",
    "maximum sum rectangle in a 2d matrix": "Maximal Rectangle",
    "count set bits in an integer": "Count total set bits",
    "find the two non-repeating elements in an array of repeating elements": "Two numbers with odd occurrences",
    "count total set bits in all numbers from 1 to n": "Count total set bits",
    "program to find whether a no is power of two": "Power of Two",
    "find position of the only set bit": "Find position of only set bit",
    "copy set bits in a range": "Check if the i-th bit is set or not",
    "divide two integers without using multiplication, division and mod operator": "Divide Two Integers"
}

def norm_key(t):
    if not t: return ''
    t = t.lower()
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

def main():
    with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
    gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

    striver_by_norm = {norm_key(p['title']): p for p in striver_core}
    striver_by_clean_title = {re.sub(r'\[.*?\]', '', p['title']).strip().lower(): p for p in striver_core}

    norm_dup_map = {norm_key(k): v for k, v in GFG_TO_STRIVER_DUPLICATES.items()}

    NON_CODING_OR_DEAD = [
        "why strings are immutable in java?",
        "write a program to check whether a string is a valid shuffle of two strings or not",
        "find pivot element in a sorted array"
    ]

    merged_duplicates = 0
    final_problems = list(striver_core)
    kept_gfg = []

    for g in gfg_added:
        t_raw = g['title'].strip()
        t_clean = re.sub(r'\[.*?\]', '', t_raw).strip().lower()
        k = norm_key(t_raw)

        # 1. Skip non-coding / dead blog questions
        if any(nc in t_clean for nc in NON_CODING_OR_DEAD):
            continue

        # 2. Check if it matches an existing Striver problem
        matched_striver = None
        if k in norm_dup_map:
            target_title = norm_dup_map[k]
            matched_striver = striver_by_clean_title.get(target_title.lower()) or striver_by_norm.get(norm_key(target_title))
        elif k in striver_by_norm:
            matched_striver = striver_by_norm[k]

        if matched_striver:
            # Attach GFG practice link to Striver problem's altUrls so it's not lost
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
            final_problems.append(g)

    # Re-order 1 to N
    for idx, p in enumerate(final_problems, start=1):
        p['order'] = idx

    data['problems'] = final_problems
    data['meta']['problemCount'] = len(final_problems)

    # Update meta step counts
    step_counts = Counter(p['step'] for p in final_problems)
    for s in data['meta'].get('steps', []):
        s['count'] = step_counts.get(s['n'], 0)

    with open('d:/DSA/Problems_List/site/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("================ FINAL SHEET SUMMARY ================")
    print(f"Striver Core Problems: {len(striver_core)}")
    print(f"GFG Duplicates Merged into AltUrls: {merged_duplicates}")
    print(f"GFG Unique Practice Questions Kept: {len(kept_gfg)}")
    print(f"TOTAL FINAL PROBLEMS IN SHEET: {len(final_problems)}")
    print("=====================================================")

if __name__ == '__main__':
    main()
