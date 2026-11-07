import json
import re
from collections import Counter

def run_filter():
    with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    striver_core = [p for p in data['problems'] if not p['id'].startswith('gfg-450-')]
    gfg_added = [p for p in data['problems'] if p['id'].startswith('gfg-450-')]

    print(f"Total current problems: {len(data['problems'])}")
    print(f"Striver Core: {len(striver_core)}")
    print(f"GFG Added: {len(gfg_added)}")

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
        "construct bst from preorder traversal": "Construct BST from preorder traversal",
        "convert binary tree into bst": "Convert Binary tree to BST",
        "merge two bst": "Merge two BSTs",
        "find kth largest element in a bst": "Find K-th smallest/largest element in BST",
        "find kth smallest element in a bst": "Find K-th smallest/largest element in BST",
        "count pairs from 2 bst whose sum is equal to given value \"x\"": "Two Sum In BST | Check if there exists a pair with given sum",
        "count bst ndoes that lie in a given range": "Check whether BST contains Dead End",
        "check whether bst contains dead end": "Check whether BST contains Dead End",
        "largest bst in a binary tree": "Largest BST in Binary Tree",
        "huffman coding": "Huffman Coding",
        "water connection problem": "Water Connection Problem",
        "greedy algorithm to find minimum number of coins": "Find minimum number of coins",
        "find maximum meetings in one room": "N meetings in one room",
        "program for least recently used (lru) page replacement algorithm": "Page Faults in LRU",
        "chocolate distribution problem": "Assign Cookies",
        "minimum cost of ropes": "Connect Ropes",
        "rearrange characters in a string such that no two adjacent are same": "Reorganize String",
        "printing all solutions in n-queen problem": "N-Queen Problem",
        "word break problem using backtracking": "Word Break",
        "the knight’s tour problem": "Knight Tour",
        "implement \"n\" stacks in an array": "Implement Stack using Arrays",
        "design a stack that supports getmin() in o(1) time and o(1) extra space.": "Minimum element in stack in O(1) space",
        "the celebrity problem": "The Celebrity Problem",
        "arithmetic expression evaluation": "Prefix to Infix Conversion",
        "evaluation of postfix expression": "Postfix to Infix",
        "reverse a stack using recursion": "Reverse a stack using recursion",
        "sort a stack using recursion": "Sort a stack using recursion",
        "merge overlapping intervals": "Merge Intervals",
        "implement a circular queue": "Implement Queue using Arrays",
        "find the first circular tour that visits all petrol pumps": "Circular tour",
        "minimum time required to rot all oranges": "Rotten Oranges",
        "distance of nearest cell having 1 in a binary matrix": "0/1 Matrix (Bfs)",
        "queue based approach or first non-repeating character in a stream.": "First non-repeating character in a stream of characters",
        "next smaller element": "Next Smaller Element",
        "implement a maxheap/minheap using arrays and recursion.": "Build heap from a given Array",
        "“k” largest element in an array": "k largest elements in an array",
        "kth smallest and largest element in an unsorted array": "Kth smallest element",
        "merge “k” sorted arrays.": "Merge M sorted Lists",
        "merge 2 binary max heaps": "Merge 2 Binary Max Heaps",
        "kth largest sum continuous subarrays": "Kth largest sum continuous subarrays",
        "leetcode- reorganize strings": "Reorganize String",
        "merge “k” sorted linked lists": "Merge M sorted Lists",
        "median in a stream of integers": "Find Median from Data Stream",
        "connect “n” ropes with minimum cost": "Connect Ropes",
        "convert bst to min heap": "Convert Min Heap to Max Heap",
        "rearrange characters in a string such that no two adjacent are same.": "Reorganize String",
        "implement bfs algorithm": "BFS of graph",
        "implement dfs algo": "DFS of graph",
        "detect cycle in directed graph using bfs/dfs algo": "Detect cycle in a directed graph",
        "detect cycle in undirected graph using bfs/dfs algo": "Detect cycle in an undirected graph",
        "minimum step by knight": "Minimum Steps by Knight",
        "clone a graph": "Clone Graph",
        "find whether it is possible to finish all tasks or not from given dependencies": "Course Schedule - I",
        "implement kruksal’salgorithm": "Kruskal's Algorithm",
        "implement prim’s algorithm": "Prim's Algorithm",
        "implement bellman ford algorithm": "Bellman ford algorithm",
        "travelling salesman problem": "Travelling Salesman Problem",
        "snake and ladders problem": "Snake and Ladder Problem",
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
        "word break problem": "Word Break",
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

    striver_title_map = {p['title'].lower(): p for p in striver_core}

    # 1. Merge duplicates into Striver Core altUrls
    merged_alt_count = 0
    for p in gfg_added:
        t_clean = p['title'].strip().lower()
        t_no_brackets = re.sub(r'\[.*?\]', '', t_clean).strip()
        striver_title = GFG_TO_STRIVER_DUPLICATES.get(t_clean) or GFG_TO_STRIVER_DUPLICATES.get(t_no_brackets)
        if striver_title:
            sp = striver_title_map.get(striver_title.lower())
            if sp and p.get('url'):
                alt_urls = sp.setdefault('altUrls', [])
                all_existing = [sp['url']] + [a['url'] for a in alt_urls]
                if p['url'] not in all_existing:
                    alt_urls.append({'platform': 'gfg', 'url': p['url']})
                    merged_alt_count += 1

    # 2. Curated 34 High-Quality Standard DSA Template Questions to KEEP
    STANDARD_GFG_TITLES_TO_KEEP = {
        "minimum no. of jumps to reach end of an array",
        "find common elements in 3 sorted arrays",
        "rearrange the array in alternating positive and negative items with o(1) extra space",
        "given an array of size n and a number k, fin all elements that appear more than \" n/k \" times.",
        "smallest subarray with sum greater than a given value",
        "minimum swaps required bring elements less equal k together",
        "kth smallest element in a row-cpumn wise sorted matrix",
        "word wrap problem .",
        "boyer moore algorithm for pattern searching.",
        "write a program tofind the smallest window that contains all characters of string itself.",
        "minimum characters to be added at front to make string palindrome",
        "find the smallest window in a string containing all characters of another string",
        "string matching where one string contains wildcard characters",
        "minimum no. of swaps required to sort the array",
        "job scheduling algo",
        "sum of nodes on the longest path from root to leaf node",
        "maximum sum of nodes in binary tree such that no two are adjacent",
        "print all \"k\" sum paths in a binary tree",
        "minimum cost to cut a board into squares",
        "remove invalid parentheses",
        "print all palindromic partitions of a string",
        "find maximum number possible by doing at-most k swaps",
        "print all permutations of a string",
        "longest possible route in a matrix with hurdles",
        "partition of a set intok subsets with equal sum",
        "length of the longest valid substring",
        "sum of minimum and maximum elements of all subarrays of size “k”.",
        "smallest range in “k” lists",
        "longest path in a directed acyclic graph",
        "gold mine problem",
        "optimal strategy for a game",
        "optimal binary search tree",
        "largest area rectangular sub-matrix with equal number of 1’s and 0’s",
        "boolean parenthesization problem"
    }

    kept_gfg = []
    removed_count = 0

    for p in gfg_added:
        t_clean = p['title'].strip().lower()
        t_no_brackets = re.sub(r'\[.*?\]', '', t_clean).strip()
        if t_clean in STANDARD_GFG_TITLES_TO_KEEP or t_no_brackets in STANDARD_GFG_TITLES_TO_KEEP:
            kept_gfg.append(p)
        else:
            removed_count += 1

    print(f"GFG problems kept as standard additions: {len(kept_gfg)}")
    print(f"GFG problems filtered out (trivia/spoj/duplicates): {removed_count}")

    # Build final list
    final_problems = striver_core + kept_gfg

    # Re-index order sequentially
    for idx, p in enumerate(final_problems, 1):
        p['order'] = idx

    print(f"Final total problem count: {len(final_problems)}")

    # Update metadata
    data['problems'] = final_problems
    data['meta']['problemCount'] = len(final_problems)
    
    # Update step counts
    step_counts = Counter(p['step'] for p in final_problems)
    for s in data['meta'].get('steps', []):
        s['count'] = step_counts.get(s['n'], 0)

    # Save to data.json
    with open('d:/DSA/Problems_List/site/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved clean data.json successfully!")

if __name__ == '__main__':
    run_filter()
