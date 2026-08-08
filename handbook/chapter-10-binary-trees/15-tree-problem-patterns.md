# 15. Binary Tree & BST Problem Patterns, Decision Matrix & Code Templates

## 1. Introduction
Recognizing tree problem patterns instantly during a 45-minute technical coding interview is the key to solving binary tree and binary search tree problems bug-free. Tree problems can be categorized into **8 Core Pattern Families**. This section provides a master pattern decision matrix mapping problem requirements to optimal traversal strategies, along with copy-paste production Java templates.

> **Important:** Master the 3 primary tree recursion paradigms:
> 1. **Top-Down DFS (Pre-Order / Passing State Down)**: Used when parent state or path accumulation dictates subproblem logic (e.g. Path Sum II, Root-to-Leaf paths).
> 2. **Bottom-Up DFS (Post-Order / Synthesizing Results Up)**: Used when subproblems depend on left and right subtree results (e.g. Height, Balanced Check, LCA, Max Path Sum).
> 3. **Queue Snapshot BFS (Level-Order Horizontal Scanning)**: Used when depth levels or column view projections dictate logic (e.g. Level Order, Right Side View, Max Width).

---

## 2. Master Tree Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER TREE PROBLEM DECISION MATRIX                                                               |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Level-by-level traversal", "Rightmost view"      | Queue Snapshot BFS    | `int sz = q.size()`   |
| "Reconstruct tree from traversal arrays"          | Divide & Conquer Map  | `leftSize = inIdx-inSt`|
| "Validate BST", "K-th smallest in BST"            | In-Order Traversal    | `prev` node tracking  |
| "Find lowest ancestor common to P and Q"          | Post-Order Match DFS  | `left != null && right`|
| "Longest path between any two nodes"              | Post-Order Height Sum | `local = leftH+rightH`|
| "Any-to-Any Max Path Sum"                         | Post-Order Gain Prune | `max(0, maxGain)`     |
| "In-place tree modification / Flatten to List"    | Reversed Post-Order   | `right->left->root`   |
| "Prefix search / Autocomplete words"              | Trie (Prefix Tree)    | `TrieNode[26] + isEnd`|
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Queue Snapshot BFS Level-Order
* **Signal**: Level-by-level traversal, Right/Left views, Minimum depth.
* **Invariant**: Capture level size BEFORE entering the inner for loop (`int levelSize = queue.size()`).

```java
public static List<List<Integer>> bfsLevelOrderTemplate(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;

    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int levelSize = queue.size(); // SNAPSHOT LEVEL SIZE!
        List<Integer> currentLevel = new ArrayList<>(levelSize);

        for (int i = 0; i < levelSize; i++) {
            TreeNode curr = queue.poll();
            currentLevel.add(curr.val);

            if (curr.left != null)  queue.offer(curr.left);
            if (curr.right != null) queue.offer(curr.right);
        }
        result.add(currentLevel);
    }
    return result;
}
```

---

## 4. Pattern 2: Bottom-Up Post-Order Subtree Synthesis
* **Signal**: Tree height, Balanced check (110), LCA (236), Max Path Sum (124), Diameter (543).
* **Invariant**: Evaluate left and right subtrees completely BEFORE calculating parent state.

```java
public static int postOrderSynthesisTemplate(TreeNode root) {
    if (root == null) return 0; // Base Case

    int leftResult = postOrderSynthesisTemplate(root.left);
    int rightResult = postOrderSynthesisTemplate(root.right);

    // Synthesis & Global State Update
    int currentMetric = 1 + Math.max(leftResult, rightResult);

    return currentMetric;
}
```

---

## 5. Pattern 3: Top-Down DFS Backtracking (Root-to-Leaf Paths)
* **Signal**: Root-to-leaf path sums (113), Printing all paths.
* **Invariant**: Add node to path list $\to$ Recurse children $\to$ Remove node (Backtrack).

```java
public static void topDownPathDFSTemplate(TreeNode node, List<Integer> currentPath, List<List<Integer>> result) {
    if (node == null) return;

    currentPath.add(node.val); // 1. Choose

    if (node.left == null && node.right == null) {
        result.add(new ArrayList<>(currentPath)); // Leaf check
    } else {
        topDownPathDFSTemplate(node.left, currentPath, result);  // 2. Explore Left
        topDownPathDFSTemplate(node.right, currentPath, result); // 2. Explore Right
    }

    currentPath.remove(currentPath.size() - 1); // 3. Backtrack
}
```

---

## 6. Pattern 4: BST Valid Range & In-Order Traversal
* **Signal**: Validate BST (98), K-th smallest (230), In-order successor (285).
* **Invariant**: Range check `[lower, upper]` or In-Order strictly increasing `prev < curr`.

```java
public static boolean isValidBSTTemplate(TreeNode node, long lower, long upper) {
    if (node == null) return true;
    if (node.val <= lower || node.val >= upper) return false;

    return isValidBSTTemplate(node.left, lower, node.val) &&
           isValidBSTTemplate(node.right, node.val, upper);
}
```

---

## 7. Pattern 5: Divide & Conquer Tree Reconstruction
* **Signal**: Preorder + Inorder (105), Inorder + Postorder (106).
* **Invariant**: Locate root in `inMap` in $O(1)$ time, calculate `leftSubtreeSize = inIndex - inStart`.

```java
public static TreeNode buildTreeTemplate(int[] preorder, int preStart, int preEnd,
                                         int[] inorder, int inStart, int inEnd,
                                         Map<Integer, Integer> inMap) {
    if (preStart > preEnd || inStart > inEnd) return null;

    int rootVal = preorder[preStart];
    TreeNode root = new TreeNode(rootVal);

    int inIndex = inMap.get(rootVal);
    int leftSubtreeSize = inIndex - inStart;

    root.left = buildTreeTemplate(preorder, preStart + 1, preStart + leftSubtreeSize,
                                  inorder, inStart, inIndex - 1, inMap);

    root.right = buildTreeTemplate(preorder, preStart + leftSubtreeSize + 1, preEnd,
                                   inorder, inIndex + 1, inEnd, inMap);

    return root;
}
```

---

## 8. Pattern 6: Reversed Post-Order In-Place Flattening
* **Signal**: Flatten tree to linked list in-place (114).
* **Invariant**: Explore Right $\to$ Left $\to$ Root; set `node.right = prev; node.left = null; prev = node;`.

```java
private static TreeNode prevNode = null;

public static void flattenTemplate(TreeNode node) {
    if (node == null) return;

    flattenTemplate(node.right); // Right FIRST!
    flattenTemplate(node.left);  // Left SECOND!

    node.right = prevNode;
    node.left = null;
    prevNode = node;
}
```

---

## 9. Pattern 7: Trie (Prefix Tree) Implementation
* **Signal**: Prefix search, Autocomplete, Wildcard string matching.
* **Invariant**: `TrieNode[26] children` + `boolean isEnd`.

```java
public static class TrieTemplate {
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd = false;
    }

    private final TrieNode root = new TrieNode();

    public void insert(String word) {
        TrieNode curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new TrieNode();
            curr = curr.children[idx];
        }
        curr.isEnd = true;
    }
}
```

---

## 10. Pattern 8: Binary Heap Position Indexing
* **Signal**: Maximum Width of Binary Tree including null gaps (662).
* **Invariant**: Assign indices `2*idx+1` and `2*idx+2`; normalize by subtracting `firstIdx`.

```java
public static int maxWidthTemplate(TreeNode root) {
    if (root == null) return 0;
    Deque<PairNode> q = new ArrayDeque<>();
    q.offer(new PairNode(root, 0L));
    int maxW = 0;

    while (!q.isEmpty()) {
        int sz = q.size();
        long firstIdx = q.peek().idx;
        long lastIdx = q.peekLast().idx;
        maxW = Math.max(maxW, (int)(lastIdx - firstIdx + 1));

        for (int i = 0; i < sz; i++) {
            PairNode curr = q.poll();
            long normIdx = curr.idx - firstIdx;
            if (curr.node.left != null)  q.offer(new PairNode(curr.node.left, 2 * normIdx + 1));
            if (curr.node.right != null) q.offer(new PairNode(curr.node.right, 2 * normIdx + 2));
        }
    }
    return maxW;
}
```

---

## 11. Edge Case Checklist for Tree Problems
* **Null Root**: Always check `if (root == null)` at the start of recursion or BFS.
* **Single Node Tree**: Verify leaf check conditions (`left == null && right == null`).
* **Skewed Tree ($H = N$)**: StackOverflow risk in recursive DFS when $N > 10,000$.
* **Negative Node Values**: Use `Math.max(0, gain)` in path sum algorithms; initialize global max with `Integer.MIN_VALUE`.
* **Duplicate Values in Tree Construction**: Tree reconstruction requires unique node values.

---

## 12. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: BINARY TREE & BST PROBLEM PATTERNS                   |
+-----------------------------------------------------------------------+
| 1. BFS Level Order: Snapshot levelSize = queue.size() BEFORE loop     |
| 2. Post-Order DFS: Evaluate left & right subtrees BEFORE parent state |
| 3. Top-Down DFS: Add to path -> Recurse -> Backtrack remove           |
| 4. Validate BST: validateRange(node, Long.MIN_VALUE, Long.MAX_VALUE)  |
| 5. Tree Construction: Pre-build inMap in O(N); leftSize = inIdx-inSt  |
| 6. Flatten Tree: Reversed DFS (Right -> Left -> Root) with prev       |
| 7. Trie: TrieNode[26] children + boolean isEnd                        |
| 8. Max Width: Heap index 2*idx+1, 2*idx+2 with normalize (idx-firstIdx)|
+-----------------------------------------------------------------------+
```

---

## 13. Practice Checklist
- [ ] I can write all 8 tree code templates from memory.
- [ ] I can select the correct pattern within 30 seconds of reading a problem prompt.
- [ ] I know why `int levelSize = queue.size()` must be captured before BFS loops.
- [ ] I know why `leftSubtreeSize = inIndex - inStart` computes exact preorder bounds.
- [ ] I know why `Math.max(0, gain)` prunes negative subtrees in LeetCode 124.
