import json
import re
import openpyxl
from collections import defaultdict, Counter
from difflib import SequenceMatcher

def clean_slug(url):
    if not url: return ''
    m = re.search(r'geeksforgeeks\.org/problems/([^/?#]+)', url)
    if m:
        slug = m.group(1)
        slug = re.sub(r'(-\d+|\d+)$', '', slug)
        return slug.lower().replace('-', '').replace('_', '')
    m = re.search(r'leetcode\.com/problems/([^/?#]+)', url)
    if m:
        slug = m.group(1)
        slug = re.sub(r'(-\d+|\d+)$', '', slug)
        return slug.lower().replace('-', '').replace('_', '')
    m = re.search(r'geeksforgeeks\.org/([^/?#]+)/?$', url)
    if m:
        slug = m.group(1)
        slug = re.sub(r'(-\d+|\d+)$', '', slug)
        return slug.lower().replace('-', '').replace('_', '')
    return ''

def normalize_title(t):
    if not t: return ''
    t = t.lower()
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'[^a-z0-9]', '', t)
    return t

def get_keywords(t):
    if not t: return set()
    t = t.lower()
    t = re.sub(r'\[.*?\]', '', t)
    t = re.sub(r'\(.*?\)', '', t)
    t = re.sub(r'\b(find|given|problem|check|program|write|print|determine|count|how|to|the|a|an|in|of|for|on|with|from|and|or|by|at|is|if|as|all|into|using|without|only|their|two|both|between|any)\b', ' ', t)
    t = re.sub(r'[^a-z0-9]', ' ', t)
    words = [w for w in t.split() if len(w) > 1]
    return set(words)

# Known semantic mappings between GFG 450 titles/slugs and Striver titles
KNOWN_MATCHES = {
    # Arrays & Hashing
    "reverse the array": "Reverse an array",
    "find the maximum and minimum element in an array": "Find the largest element in an array",
    "find the \"kth\" max and min element of an array": "Kth Largest Element in an Array",
    "given an array which consists of only 0, 1 and 2. sort the array without using any sorting algo": "Sort an array of 0's 1's and 2's",
    "move all the negative elements to one side of the array": "Move Zeros to End",
    "find the union and intersection of the two sorted arrays.": "Union of two sorted arrays",
    "write a program to cyclically rotate an array by one.": "Left Rotate Array by One",
    "find largest sum contiguous subarray [v. imp]": "Kadane's Algorithm",
    "kadane's algo [v.v.v.v.v imp]": "Kadane's Algorithm",
    "minimise the maximum difference between heights [v.imp]": "Minimize Max Distance to Gas Station",
    "find duplicate in an array of n+1 integers": "Find the duplicate in an array of N+1 integers",
    "merge 2 sorted arrays without using extra space.": "Merge two sorted arrays without extra space",
    "merge intervals": "Merge Intervals",
    "next permutation": "Next Permutation",
    "count inversion": "Count Inversions",
    "best time to buy and sell stock": "Best time to buy and sell stock",
    "find all pairs on integer array whose sum is equal to given number": "Two Sum",
    "find if there is any subarray with sum equal to 0": "Largest Subarray with Sum 0",
    "find factorial of a large number": "Factorial of a given number",
    "find maximum product subarray": "Maximum Product Subarray in an Array",
    "find longest coinsecutive subsequence": "Longest Consecutive Sequence in an Array",
    "given an array of size n and a number k, fin all elements that appear more than \" n/k \" times.": "Majority Element ( > n/3 times )",
    "maximum profit by buying and selling a share atmost twice": "Best time to buy and sell stock III",
    "find the triplet that sum to a given value": "3 Sum",
    "trapping rain water problem": "Trapping Rainwater",
    "chocolate distribution problem": "Chocolate Distribution Problem",
    "three way partitioning of an array around a given value": "Sort an array of 0's 1's and 2's",
    "minimum no. of operations required to make an array palindrome": "Valid Palindrome",
    "median of 2 sorted arrays of equal size": "Median of 2 sorted arrays",
    "median of 2 sorted arrays of different size": "Median of 2 sorted arrays",

    # Matrix
    "spirally traversing a matrix": "Spiral Traversal of Matrix",
    "search an element in a matriix": "Search in a 2D Matrix",
    "find median in a row wise sorted matrix": "Matrix Median",
    "find row with maximum no. of 1's": "Find row with maximum 1's",
    "print elements in sorted order using row-column wise sorted matrix": "Matrix Median",
    "maximum size rectangle": "Maximum Rectangles",
    "rotate matrix by 90 degrees": "Rotate matrix by 90 degrees",

    # String
    "reverse a string": "Reverse a String I",
    "check whether a string is palindrome or not": "Check if String is Palindrome or Not",
    "find duplicate characters in a string": "Check if String is Palindrome or Not",
    "write a code to check whether one string is a rotation of another": "Rotate String",
    "write a program to find the longest palindrome in a string.[ longest palindromic substring]": "Longest Palindromic Substring",
    "find longest recurring subsequence in string": "Longest Repeating Subsequence",
    "print all subsequences of a string.": "Print all subsequences",
    "print all permutations of a given string": "Print all Permutations of a String/Array",
    "word break problem[ very imp]": "Word Break",
    "rabin karp algo": "Rabin Karp",
    "kmp algo": "KMP algo",
    "count and say problem": "Count and say",
    "edit distance [very imp]": "Edit distance",
    "balanced parenthesis problem.[imp]": "Balanced Paranthesis",

    # Search & Sort
    "find first and last positions of an element in a sorted array": "First and Last Occurrences in Array",
    "find a fixed point (value equal to index) in a given array": "Search in Rotated Sorted Array",
    "search in rotated sorted array": "Search in rotated sorted array-I",
    "square root of an integer": "Find square root of a number",
    "maximum and minimum of an array using minimum number of comparisons": "Find the largest element in an array",
    "optimum location of point to minimize total distance": "Minimize Max Distance to Gas Station",
    "find the repeating and the missing": "Find the repeating and missing number",
    "find majority element": "Majority Element",
    "searching in an array where adjacent differ by at most k": "Linear Search",
    "find a pair with a given difference": "Two Sum",
    "find four elements that sum to a given value": "4 Sum",
    "maximum sum such that no 2 elements are adjacent": "Maximum sum of non-adjacent elements",
    "count triplet with sum smaller than a given value": "3 Sum",
    "merge 2 sorted arrays": "Merge two sorted arrays without extra space",
    "print all subarrays with 0 sum": "Largest Subarray with Sum 0",
    "product array puzzle": "Product of Array Except Self",
    "sort array according to count of set bits": "Sort Characters by Frequency",
    "k-th element of two sorted arrays": "Kth element of 2 sorted arrays",
    "allocate minimum number of pages": "Book Allocation Problem",
    "painters partition problem:": "Painter's Partition",
    "roti-prata spoj": "Aggressive Cows",
    "doublehelix spoj": "Merge two sorted arrays without extra space",
    "subset sums": "Subsets I",
    "find the inversion count": "Count Inversions",

    # LinkedList
    "write a program to reverse the linked list. (both iterative and recursive)": "Reverse a LinkedList",
    "reverse a linked list in group of given size. [very imp]": "Reverse a LL in groups of given size K",
    "write a program to detect loop in a linked list.": "Detect a loop in LL",
    "write a program to delete loop in a linked list.": "Find the starting point in LL",
    "find the starting point of the loop.": "Find the starting point in LL",
    "remove duplicate element from sorted linked list": "Remove duplicate elements from sorted linked list",
    "remove duplicates from an unsorted linked list": "Remove duplicates from sorted DLL",
    "write a program to find the middle of the linked list.": "Middle of a LinkedList",
    "check if linked list is palindrome": "Check if LL is palindrome or not",
    "deletion from a circular linked list": "Delete Kth Element of LL",
    "reverse a doubly linked list.": "Reverse a Doubly Linked List",
    "find pairs with a given sum in a dll.": "Find Pairs with Given Sum in Doubly Linked List",
    "rotate doublylinked list by n nodes.": "Rotate a LinkedList",
    "intersection of two sorted linked list": "Intersection of two sorted Linked Lists",
    "intersection point of two linked lists.": "Find intersection of Two Linked Lists",
    "merge two sorted linked lists": "Merge two Sorted Lists",
    "merge k sorted linked list": "Merge K Sorted Lists",
    "flatten a linked list": "Flattening of LL",
    "sort a ll of 0's, 1's and 2's": "Sort a Linked List of 0's 1's and 2's",
    "clone a linked list with next and random pointer": "Clone a Linked List with random and next pointer",
    "delete nodes which have a greater value on right side": "Delete all occurrences of a key in DLL",

    # Binary Trees
    "level order traversal": "Level order Traversal",
    "reverse level order traversal": "Reverse Level Order Traversal",
    "height of a tree": "Height of a Binary Tree",
    "diameter of a tree": "Diameter of Binary Tree",
    "create a mirror tree from the given binary tree": "Invert Binary Tree",
    "inorder traversal of a tree both using recursion and iteration": "Inorder Traversal",
    "preorder traversal of a tree both using recursion and iteration": "Preorder Traversal",
    "postorder traversal of a tree both using recursion and iteration": "Postorder Traversal",
    "left view of a tree": "Left view of BT",
    "right view of tree": "Right view of BT",
    "top view of a tree": "Top View of BT",
    "bottom view of a tree": "Bottom view of BT",
    "zig-zag traversal of a binary tree": "Zig Zag Traversal of BT",
    "check if a tree is balanced or not": "Check for Balanced Binary Tree",
    "diagonal traversal of a binary tree": "Diagonal Traversal of Binary Tree",
    "boundary traversal of binary tree": "Boundary Traversal of Binary Tree",
    "construct tree from inorder & preorder": "Construct Binary Tree from Inorder and Preorder Traversal",
    "check for children sum property": "Children Sum Property in Binary Tree",
    "lowest common ancestor in a binary tree": "Lowest Common Ancestor for two given Nodes",
    "check if 2 trees are mirror or not": "Symmetric Binary Tree",
    "check if two trees are identical": "Check if two Trees are Identical or Not",

    # Binary Search Trees
    "fina a value in a bst": "Find a value in a BST",
    "deletion of a node in a bst": "Deletion of a node in BST",
    "find min and max value in a bst": "Find min and max value in a BST",
    "find inorder predecessor and successor for a given key in bst.": "Inorder Predecessor and Successor in BST",
    "check if a tree is a bst or not": "Check if a tree is a BST or BT",
    "populate inorder successor for all nodes": "Inorder Successor in BST",
    "find lca of 2 nodes in a bst": "LCA in BST",
    "construct bst from preorder traversal": "Construct BST from preorder traversal",
    "convert binary tree into bst": "Convert Binary tree to BST",
    "find kth smallest element in a bst": "Find K-th smallest/largest element in BST",
    "find kth largest element in a bst": "Find K-th smallest/largest element in BST",
    "count pairs from 2 bst whose sum is equal to given value \"x\"": "Two Sum In BST | Check if there exists a pair with given sum",
    "check whether bst contains dead end": "Check whether BST contains Dead End",
    "find the largest bst subtree in a given binary tree": "Largest BST in Binary Tree",

    # Greedy
    "activity selection problem": "N meetings in one room",
    "job sequencingproblem": "Job sequencing Problem",
    "fractional knapsack problem": "Fractional Knapsack",
    "water connection problem": "Water Connection Problem",
    "huffman coding": "Huffman Coding",
    "n meetings in one room": "N meetings in one room",
    "minimum platforms problem": "Minimum number of platforms required for a railway",
    "buy maximum stocks if i stocks can be bought on i-th day": "Best time to buy and sell stock",
    "find the minimum and maximum amount to buy all n candies": "Assign Cookies",
    "page faults in lru": "Page Faults in LRU",

    # Backtracking
    "rat in a maze problem": "Rat in a Maze",
    "printing all solutions in n-queen problem": "N-Queen Problem",
    "word break problem using backtracking": "Word Break",
    "m coloring problem": "M Coloring Problem",
    "sudoku solver": "Sudoku Solver",
    "the knight’s tour problem": "Knight Tour",
    "partition equal subset sum": "Partition equal subset sum",
    "find if there is a path of more than k length from a source": "Rat in a Maze",

    # Stack & Queue
    "implement stack from scratch": "Implement Stack using Arrays",
    "implement queue from scratch": "Implement Queue using Arrays",
    "implement 2 stack in an array": "Implement Stack using Arrays",
    "find the middle element of a stack": "Implement Stack using Arrays",
    "implement \"k\" stacks in an array": "Implement Stack using Arrays",
    "check the expression has valid or balanced parenthesis or not.": "Balanced Paranthesis",
    "reverse a string using stack": "Reverse a String I",
    "design a stack that supports getmin() in o(1) time and o(1) extra space.": "Minimum element in stack in O(1) space",
    "find the next greater element": "Next Greater Element",
    "the celebrity problem": "The Celebrity Problem",
    "arithmetic expression evaluation": "Prefix to Infix Conversion",
    "evaluation of postfix expression": "Postfix to Infix",
    "insert at the bottom of stack": "Insert at the bottom of stack",
    "reverse a stack using recursion": "Reverse a stack using recursion",
    "sort a stack using recursion": "Sort a stack using recursion",
    "largest rectangular area in histogram": "Largest rectangle in a histogram",
    "lru cache implementation": "LRU Cache",
    "lfu cache implementation": "LFU Cache",
    "rotten oranges": "Rotten Oranges",
    "distance of nearest cell having 1 in a binary matrix.": "0/1 Matrix (Bfs)",
    "first negative integer in every window of size “k”": "Sliding Window Maximum",
    "first non-repeating character in a stream": "First non-repeating character in a stream of characters",
    "next smaller element": "Next Smaller Element",

    # Heap
    "building heap from array": "Build heap from a given Array",
    "heap sort": "Heap Sort",
    "maximum of all subarrays of size k.": "Sliding Window Maximum",
    "“k” largest element in an array": "k largest elements in an array",
    "kth smallest and largest element in an unsorted array": "Kth smallest element",
    "merge “k” sorted arrays. [ imp ]": "Merge M sorted Lists",
    "merge 2 binary max heaps": "Merge 2 Binary Max Heaps",
    "kth largest sum continuous subarrays": "Kth largest sum continuous subarrays",
    "reorganize string": "Reorganize String",
    "connect “n” ropes with minimum cost": "Connect Ropes",
    "convert min heap to max heap": "Convert Min Heap to Max Heap",

    # Graph
    "create a graph, print it": "Connected Components",
    "implement bfs algorithm": "BFS of graph",
    "implement dfs algo": "DFS of graph",
    "detect cycle in directed graph using bfs/dfs algo": "Detect cycle in a directed graph",
    "detect cycle in undirected graph using bfs/dfs algo": "Detect cycle in an undirected graph",
    "rat in a maze problem": "Rat in a Maze",
    "minimum step by knight": "Minimum Steps by Knight",
    "flood fill algo": "Flood fill",
    "clone a graph": "Clone Graph",
    "making wired connections": "Number of Operations to Make Network Connected",
    "word ladder": "Word Ladder - I",
    "dijkstra algo": "Dijkstra's algorithm",
    "topological sort": "Topological sort or Kahn's algorithm",
    "alien dictionary": "Alien dictionary",
    "implement kruksal’salgorithm": "Kruskal's Algorithm",
    "implement prim’s algorithm": "Prim's Algorithm",
    "find the no. of isalnds": "Number of islands",
    "check whether a given graph is bipartite or not": "Bipartite Graph (BFS/DFS)",
    "bridge in a graph": "Bridge edge in a graph",
    "count strongly connected components(kosaraju algo)": "Kosaraju's Algorithm",
    "bellman ford algorithm": "Bellman ford algorithm",
    "floyd warshall algorithm": "Floyd warshall algorithm",
    "travelling salesman problem": "Travelling Salesman Problem",
    "graph colouringproblem": "M Coloring Problem",
    "snake and ladder problem": "Snake and Ladder Problem",

    # Dynamic Programming
    "0 - 1 knapsack problem": "0 and 1 Knapsack",
    "binomial coefficientproblem": "Pascal's Triangle II",
    "permutation coefficientproblem": "Permutations of Array/String",
    "program for nth catalan number": "Count Unique BSTs",
    "matrix chain multiplication": "Matrix chain multiplication",
    "edit distance": "Edit distance",
    "subset sum problem": "Subset sum equals to target",
    "equal sum partition problem": "Partition equal subset sum",
    "friends pairing problem": "Count Subsets with Sum K",
    "gold mine problem": "Minimum path sum in Triangular Grid",
    "assembly line schedulingproblem": "Ninja's training",
    "painting the fenceproblem": "Ninja's training",
    "maximize the cut segments": "Rod cutting problem",
    "longest common subsequence": "Longest common subsequence",
    "longest repeated subsequence": "Longest Repeating Subsequence",
    "longest increasing subsequence": "Longest increasing subsequence",
    "space optimized solution of lcs": "Longest common subsequence",
    "lcs (longest common subsequence) of three strings": "Longest common subsequence",
    "maximum sum increasing subsequence": "Longest increasing subsequence",
    "count all subsequences having product less than k": "Count subsets with sum K",
    "longest subsequence such that difference between adjacent is one": "Longest increasing subsequence",
    "maximum subsequence sum such that no three are consecutive": "House Robber",
    "egg dropping problem": "Super Egg Drop",
    "maximum length chain of pairs": "Longest increasing subsequence",
    "maximum size square sub-matrix with all 1s": "Maximal Rectangle",
    "maximum sum of pairs with specific difference": "Partition equal subset sum",
    "min cost pathproblem": "Minimum path sum in Grid",
    "maximum path sum in matrix": "Maximum path sum in matrix",
    "coin changeproblem": "Coin Change",
    "rod cutting problem": "Rod cutting problem",
    "longest common substring": "Longest common substring",
    "count palindromic subsequences": "Longest Palindromic Subsequence",
    "longest palindromic subsequence": "Longest Palindromic Subsequence",
    "count all palindromic subsequence in a given string": "Longest Palindromic Subsequence",
    "longest palindromic substring": "Longest Palindromic Subsequence",
    "longest alternating subsequence": "Longest Bitonic Subsequence",
    "weighted job scheduling": "Job sequencing Problem",
    "coin game winner where every player has three choices": "Coin Change",
    "count derangements (permutation such that no element appears in its original position) [ leetcode ]": "Permutations of Array/String",
    "maximum profit by buying and selling a share at most k times": "Best time to buy and sell stock IV",
    "find if a string is interleaved of two other strings": "Distinct Subsequences",
    "maximum length of pair chain": "Longest increasing subsequence",

    # Bit Manipulation
    "count set bits in an integer": "Count total set bits",
    "find the two non-repeating elements in an array of repeating elements": "Two numbers with odd occurrences",
    "count number of bits to be flipped to convert a to b": "Minimum Bit Flips to Convert Number",
    "count total set bits in all numbers from 1 to n": "Count total set bits",
    "program to find whether a no is power of two": "Power of Two",
    "find position of the only set bit": "Find position of only set bit",
    "copy set bits in a range": "Check if the i-th bit is set or not",
    "divide two integers without using multiplication, division and mod operator": "Divide Two Integers",
    "calculate square of a number without using *, / and pow()": "Find square root of a number",
    "power set": "Power Set",

    # Trie
    "construct a trie from scratch": "Implement Trie : Insert, Search, StartsWith",
    "find shortest unique prefix for every word in a given list": "Complete String",
    "word break problem | (trie solution)": "Word Break",
    "given a sequence of words, print all anagrams together": "Group Anagrams",
    "implement a phone directory": "Implement Trie - II",
    "print unique rows in a given boolean matrix": "Count of distinct substrings"
}

def run_merge():
    with open('d:/DSA/Problems_List/site/data.json', 'r', encoding='utf-8') as f:
        striver_data = json.load(f)

    striver_probs = striver_data['problems']
    
    wb = openpyxl.load_workbook('d:/DSA/MY_GFG-450.xlsx')
    sheet = wb.active

    gfg_rows = []
    for r in range(5, sheet.max_row + 1):
        topic = sheet.cell(r, 1).value
        title = sheet.cell(r, 2).value
        link = sheet.cell(r, 2).hyperlink.target if sheet.cell(r, 2).hyperlink else ''
        done = sheet.cell(r, 3).value
        if title and title.strip():
            gfg_rows.append({
                'row': r,
                'topic': str(topic).strip() if topic else 'General',
                'title': title.strip(),
                'url': link.strip() if link else '',
                'done': done
            })

    # Build multi-index on Striver
    striver_by_norm = {}
    striver_by_slug = {}
    striver_by_url = {}

    for p in striver_probs:
        striver_by_norm[normalize_title(p['title'])] = p
        
        all_urls = [p['url']] + [a['url'] for a in p.get('altUrls', [])]
        for u in all_urls:
            if u:
                striver_by_url[u.strip()] = p
                s = clean_slug(u)
                if s: striver_by_slug[s] = p
        
        if p.get('slug'):
            s = clean_slug(p['slug'])
            if s: striver_by_slug[s] = p
        if p.get('lcSlug'):
            s = clean_slug(p['lcSlug'])
            if s: striver_by_slug[s] = p

    # Map GFG topics to Striver module steps
    TOPIC_TO_STEP = {
        'Array': (3, 'Arrays'),
        'Matrix': (3, 'Arrays'),
        'String': (18, 'Strings (Advanced Algo)'),
        'Searching & Sorting': (5, 'Binary Search'),
        'LinkedList': (7, 'Linked-List'),
        'Binary Trees': (12, 'Binary Trees'),
        'Binary Search Trees': (13, 'Binary Search Trees'),
        'Greedy': (9, 'Greedy Algorithms'),
        'BackTracking': (6, 'Recursion'),
        'Stacks & Queues': (11, 'Stack / Queues'),
        'Heap': (14, 'Heaps'),
        'Graph': (15, 'Graphs'),
        'Dynamic Programming': (16, 'Dynamic Programming'),
        'Bit Manipulation': (8, 'Bit Manipulation'),
        'Trie': (17, 'Tries')
    }

    duplicates_topic_wise = Counter()
    new_topic_wise = Counter()
    duplicates_list = []
    new_list = []

    for g in gfg_rows:
        g_title = g['title']
        g_url = g['url']
        g_slug = clean_slug(g_url)
        g_norm = normalize_title(g_title)
        g_topic = g['topic']

        matched_p = None
        match_reason = ''

        # 1. Exact manual mapping
        clean_key = g_title.strip().lower()
        clean_key_no_brackets = re.sub(r'\[.*?\]', '', clean_key).strip()
        if clean_key in KNOWN_MATCHES:
            target_title = KNOWN_MATCHES[clean_key]
            matched_p = striver_by_norm.get(normalize_title(target_title))
            match_reason = 'known_alias'
        elif clean_key_no_brackets in KNOWN_MATCHES:
            target_title = KNOWN_MATCHES[clean_key_no_brackets]
            matched_p = striver_by_norm.get(normalize_title(target_title))
            match_reason = 'known_alias'

        # 2. Exact URL
        if not matched_p and g_url and g_url in striver_by_url:
            matched_p = striver_by_url[g_url]
            match_reason = 'exact_url'

        # 3. Slug match
        if not matched_p and g_slug and g_slug in striver_by_slug:
            matched_p = striver_by_slug[g_slug]
            match_reason = 'slug'

        # 4. Normalized title match
        if not matched_p and g_norm in striver_by_norm:
            matched_p = striver_by_norm[g_norm]
            match_reason = 'norm_title'

        # Process outcome
        if matched_p:
            duplicates_topic_wise[g_topic] += 1
            duplicates_list.append((g, matched_p, match_reason))
            
            # If the duplicate problem has a GFG URL from this sheet, add it to altUrls!
            if g_url:
                alt_urls = matched_p.setdefault('altUrls', [])
                existing_urls = [matched_p['url']] + [a['url'] for a in alt_urls]
                if g_url not in existing_urls:
                    alt_urls.append({
                        'platform': 'gfg',
                        'url': g_url
                    })
        else:
            new_topic_wise[g_topic] += 1
            new_list.append(g)

    total_gfg = len(gfg_rows)
    total_dups = len(duplicates_list)
    total_new = len(new_list)
    initial_striver = len(striver_probs)
    final_total = initial_striver + total_new

    print("================ CALCULATION REPORT ================")
    print(f"Total problems in GFG-450 Sheet: {total_gfg}")
    print(f"Initial problems in Striver Sheet: {initial_striver}")
    print(f"Duplicates found & merged into existing problems: {total_dups}")
    print(f"New good problems to add: {total_new}")
    print(f"Final total problems in sheet: {final_total}")
    print("\n----------- Topic-wise Breakdown -----------")
    print(f"{'Topic':<25} | {'GFG Total':<10} | {'Duplicates':<12} | {'New Added':<10}")
    print("-" * 65)
    
    all_topics = sorted(set(g['topic'] for g in gfg_rows))
    for t in all_topics:
        tot = sum(1 for g in gfg_rows if g['topic'] == t)
        dup = duplicates_topic_wise[t]
        nw = new_topic_wise[t]
        print(f"{t:<25} | {tot:<10} | {dup:<12} | {nw:<10}")
    print("-" * 65)
    print(f"{'TOTAL':<25} | {total_gfg:<10} | {total_dups:<12} | {total_new:<10}")

    # Now create new problem entries and add them to striver_probs
    cur_order = max(p['order'] for p in striver_probs) + 1
    new_prob_entries = []

    for idx, g in enumerate(new_list, start=1):
        step_num, step_name = TOPIC_TO_STEP.get(g['topic'], (19, 'General'))
        pid = f"gfg-450-{idx:04d}"
        
        # Clean title
        title = g['title']
        title = re.sub(r'\[.*?\]', '', title).strip() # clean [V. IMP]
        
        new_p = {
            "id": pid,
            "order": cur_order,
            "title": title,
            "step": step_num,
            "stepTitle": step_name,
            "topic": f"GFG 450 - {g['topic']}",
            "tier": "basic",
            "difficulty": "Medium", # Default good problem difficulty
            "difficultySource": "gfg",
            "platform": "gfg",
            "url": g['url'] if g['url'] else "https://www.geeksforgeeks.org/",
            "altUrls": [],
            "article": g['url'] if 'geeksforgeeks.org/' in g['url'] else None,
            "video": None,
            "premium": False,
            "duration": "15 min",
            "slug": re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-'),
            "lcSlug": ""
        }
        new_prob_entries.append(new_p)
        cur_order += 1

    # Merge into data.json
    striver_data['problems'].extend(new_prob_entries)
    striver_data['meta']['problemCount'] = len(striver_data['problems'])
    
    # Update step counts in meta
    step_counts = Counter(p['step'] for p in striver_data['problems'])
    for s in striver_data['meta'].get('steps', []):
        s['count'] = step_counts.get(s['n'], 0)
    
    # Save back to data.json
    with open('d:/DSA/Problems_List/site/data.json', 'w', encoding='utf-8') as f:
        json.dump(striver_data, f, indent=2, ensure_ascii=False)

    print(f"\nSuccessfully updated data.json! Final count: {len(striver_data['problems'])}")

if __name__ == '__main__':
    run_merge()
