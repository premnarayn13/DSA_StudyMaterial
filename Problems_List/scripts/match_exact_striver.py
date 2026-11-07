import json
import re

# Load data.json
with open('site/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

striver = [p for p in d['problems'] if not p['id'].startswith('gfg-450-')]
gfg = [p for p in d['problems'] if p['id'].startswith('gfg-450-')]

# Let's inspect gfg problems and their intended striver matches
MAP = {
    # Trees
    "Reverse level order traversal": "Reverse Level Order Traversal", # GFG slug or title
    "Height of a tree": "Maximum Depth in BT",
    "Left view of a tree": "Left/Right View of Binary Tree",
    "Right view of tree": "Left/Right View of Binary Tree",
    "Zig-zag traversal of a binary tree": "Zig Zag Traversal of BT",
    "Boundary traversal of a binary tree": "Boundary Traversal of Binary Tree",
    "Convert binary tree into Doubly Linked List": None, # Striver doesn't have BT to DLL! Keep GFG!
    "Construct Binary tree from Inorder and preorder traversal": "Construct Binary Tree from Inorder and Preorder Traversal",
    "Find LCA in a Binary tree": "LCA in BT",
    "Find min and max value in a BST": "Find Min/Max in BST",
    "Find LCA  of 2 nodes in a BST": "LCA in BST",
    "Construct BST from preorder traversal": "Construct BST from Preorder Traversal",
    "Count BST ndoes that lie in a given range": None, # Good problem to keep!
    "Largest BST in a Binary Tree": "Maximum Sum BST in Binary Tree",
    
    # Graphs
    "Implement BFS algorithm": "BFS",
    "Implement DFS Algo": "DFS",
    "Detect cycle in directed graph using BFS/DFS Algo": "Detect cycle in a directed graph",
    "Detect cycle in an undirected graph using BFS/DFS Algo": "Detect cycle in an undirected graph",
    "Rat in a Maze Problem": "Rat in a Maze",
    "Minimum Step by Knight": "Knight Walk",
    "Flood fill Algo": "Flood Fill",
    "Clone a graph": "Clone Graph",
    "Making Wired Connections": "Number of Operations to Make Network Connected",
    "word ladder": "Word Ladder I",
    "Dijkstra Algo": "Dijkstra's Algorithm",
    "Topological sort": "Topological Sort",
    "Find the no. of Isalnds": "Number of Islands",
    "Alien Dictionary": "Alien Dictionary",
    "Implement Kruksal’sAlgorithm": "Kruskal's Algorithm",
    "Implement Prim’s Algorithm": "Prim's Algorithm",
    "Implement Bellman Ford Algorithm": "Bellman Ford Algorithm",
    "Implement Floyd warshall Algorithm": "Floyd Warshall Algorithm",
    "Cheapest Flights Within K Stops": "Cheapest Flights Within K Stops",
    "Find bridge in a graph": "Bridges in Graph",
    "Check whether a graph is Bipartite or Not": "Bipartite Graph",
    "Detect Negative cycle in a graph": "Bellman Ford Algorithm",

    # Stacks & Queues
    "the celebrity problem": "Celebrity Problem",
    "evaluation of postfix expression": "Evaluation of Postfix Expression",
    "insert at the bottom of a stack": "Insert an Element at the Bottom of a Stack",
    "reverse a stack using recursion": "Reverse a Stack using Recursion",
    "sort a stack using recursion": "Sort a Stack using Recursion",
    "merge overlapping intervals": "Merge Overlapping Subintervals",
    "largest rectangular area in histogram": "Largest Rectangle in Histogram",
    "find the next greater element": "Next Greater Element",
    "next smaller element": "Next Smaller Element",
    "distance of nearest cell having 1": "Distance of nearest cell having 1",

    # Linked List
    "write a program to reverse the linked list. (both iterative and recursive)": "Reverse a LL",
    "reverse a linked list in group of given size.": "Reverse LL in group of given size K",
    "remove duplicates in a sorted linked list.": "Remove duplicates from sorted DLL",
    "add “1” to a number represented as a linked list.": "Add 1 to a number represented by LL",
    "add two numbers represented by linked lists.": "Add two numbers represented by LL",
    "intersection point of two linked lists.": "Intersection of two Linked Lists",
    "merge sort for linked lists.": "Sort a LL",
    "write a program to check whether the singly linked list is a palindrome or not.": "Check if LL is palindrome or not",
    "reverse a doubly linked list.": "Reverse a DLL",
    "clone a linked list with next and random pointer": "Clone a LL with random and next pointer",
    "merge k sorted linked list": "Merge K Sorted Lists",
    "segregate even and odd nodes in a linked list": "Segregate even and odd nodes in LL",
    "program for n’th node from the end of a linked list": "Remove Nth node from the back of the LL",

    # Strings
    "rabin karp algo": "Rabin Karp Algorithm",
    "kmp algo": "KMP Algorithm or LPS array",
    "search a word in a 2d grid of characters.": "Word Search",
    
    # DP
    "0 - 1 knapsack problem": "0/1 Knapsack",
    "longest common subsequence": "Longest Common Subsequence",
    "longest repeated subsequence": "Longest Repeating Subsequence",
    "egg dropping problem": "Egg Dropping Problem",
    "maximum profit by buying and selling a share at most twice": "Best Time to Buy and Sell Stock III",
    "palindrome partitioningproblem": "Palindrome Partitioning - II"
}

# Let's test how many Striver titles match
striver_titles_lower = {p['title'].lower(): p for p in striver}
resolved = {}
for gfg_t, str_t in MAP.items():
    if str_t:
        # Search in striver
        found = None
        for p in striver:
            if p['title'].lower() == str_t.lower() or str_t.lower() in p['title'].lower():
                found = p
                break
        if found:
            resolved[gfg_t.lower()] = found
        else:
            print(f"FAILED to match Striver: {str_t}")

print(f"\nTotal resolved mappings: {len(resolved)} out of {len(MAP)}")
