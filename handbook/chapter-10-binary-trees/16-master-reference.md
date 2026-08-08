# 16. Master Reference — Binary Trees & Binary Search Trees

## 1. Introduction
This Master Reference consolidates all mathematical proofs, tree invariants, traversal algorithms, search tree operations, self-balancing mechanics, and problem recognition patterns for **Chapter 10: Binary Trees & Binary Search Trees**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Handshaking Lemma ($L = I_2 + 1$), Morris Traversal $O(1)$ space threads, `inMap` $O(N)$ tree reconstruction, Hibbard deletion 3 cases, LeetCode 124 arch path updates, and AVL/Red-Black Tree balance invariants!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Tree Edges Invariant**: For any tree with $N$ nodes, total edges $E = N - 1$.
* **Max Nodes at Depth $D$**: $n(D) = 2^D$ (where $\text{Depth}(\text{Root}) = 0$).
* **Max Total Nodes in Tree of Height $H$**: $N_{\text{max}} = 2^{H+1} - 1$.
* **Min Height for $N$ Nodes**: $H_{\text{min}} = \lceil \log_2(N + 1) \rceil - 1 = \mathbf{O(\log N)}$.
* **Max Height for $N$ Nodes (Skewed)**: $H_{\text{max}} = N - 1 = \mathbf{O(N)}$.
* **Handshaking Lemma for Trees**: Leaf Nodes $L = I_2 + 1$ (where $I_2$ is number of nodes with 2 children).
* **Full Binary Tree Relation**: $N = 2I + 1$ (where $I$ is total internal nodes).
* **AVL Balance Factor**: $\text{BF}(X) = \text{Height}(\text{left}) - \text{Height}(\text{right}) \in \{-1, 0, 1\}$.
* **Red-Black Tree Height Bound**: $\text{Height} \le 2 \log_2(N + 1) = O(\log N)$.
* **Binary Heap Index Position**: Left child = $2 \cdot \text{idx} + 1$, Right child = $2 \cdot \text{idx} + 2$.
* **Tree Reconstruction Subtree Size**: `leftSubtreeSize = inIndex - inStart`.

```
Tree Types Classification Summary:
+-----------------------------------+---------------------------------------------------+
| Tree Type Name                    | Structural Invariant Rule                         |
+-----------------------------------+---------------------------------------------------+
| Full Binary Tree                  | Every node has 0 or 2 children (No 1-child nodes!)|
| Complete Binary Tree              | All levels full except last (filled left-aligned) |
| Perfect Binary Tree               | All internal nodes have 2 children, all leaves at H|
| Balanced Tree (AVL)               | |Height(left) - Height(right)| <= 1 at every node |
| Binary Search Tree (BST)          | Left.val < Node.val < Right.val (In-Order Sorted) |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Tree Algorithm Complexity Table

| Operation / Algorithm | Time Complexity (Balanced) | Time Complexity (Skewed) | Auxiliary Space | Key Mechanism / Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **Recursive DFS (Pre/In/Post)**| **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | JVM Call Stack Recursion |
| **Iterative DFS (Stack)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Stack | Explicit `ArrayDeque` Stack |
| **Morris In-Order Traversal** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | **$O(1)$ Constant ⚡**| Temporary Thread `pred.right = curr` |
| **BFS Level Order (102)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(W)$ Queue | Queue Snapshot `levelSize = q.size()` |
| **Tree Construction (105)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(N)$ Map Space | `inMap.put(val, idx)` for $O(1)$ root lookup |
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | Range Recursion `[lower, upper]` |
| **BST Search / Insert (700)** | **$O(\log N)$ Logarithmic⚡**| $O(N)$ Linear | **$O(1)$ Iterative ⚡**| Move Left if key < val, else Right |
| **BST Delete (450)** | **$O(\log N)$ Logarithmic⚡**| $O(N)$ Linear | $O(H)$ Call Stack | Hibbard 3 Cases (Successor Swap) |
| **BST LCA (235)** | **$O(\log N)$ Logarithmic⚡**| $O(N)$ Linear | **$O(1)$ Iterative ⚡**| Value Split `p.val < curr && q.val < curr` |
| **General Tree LCA (236)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | Post-Order `left != null && right != null` |
| **Parent Pointer LCA (1650)**| **$O(H)$ Logarithmic⚡**| $O(N)$ Linear | **$O(1)$ Constant ⚡**| Two Pointers Linked List Intersection |
| **Max Path Sum (124)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | `val + leftGain + rightGain` Arch Update |
| **Tree Diameter (543)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | Post-Order Height Sum `leftH + rightH` |
| **Max Level Width (662)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(W)$ Queue | Heap Indexing `(lastIdx - firstIdx + 1)` |
| **Boundary Traversal (545)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | $O(H)$ Call Stack | 4-Stage Anti-Clockwise Shell |
| **Flatten Tree to List (114)**| **$O(N)$ Linear ⚡** | $O(N)$ Linear | **$O(1)$ Morris ⚡** | Reversed DFS / Morris `pred.right=right` |
| **Trie Insert / Search (208)**| **$O(L)$ String Length ⚡**| **$O(L)$ Linear ⚡** | $O(N \cdot L \cdot 26)$ | Array `TrieNode[26]` Prefix Graph |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Tree Nodes on 64-Bit JVM (Compressed OOPs)                    |
+-----------------------------------------------------------------------------------+
| Standard TreeNode Object  : 24 Bytes (Header 12B + int val 4B + left 4B + right 4B)|
| Parent Node (Node with Parent): 28 Bytes (Adds parent reference 4B)               |
| TreeMap.Entry<K,V>        : 32 Bytes (Header + K + V + left + right + parent + color)|
| TrieNode (Array[26])      : 120 Bytes per node (Array object + 26 null references)|
| Memory Optimization       : Use Map<Character, TrieNode> for sparse character tries|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Queue Snapshot Level-Order BFS Pattern
int levelSize = queue.size();
for (int i = 0; i < levelSize; i++) {
    TreeNode curr = queue.poll();
    if (i == levelSize - 1) rightView.add(curr.val);
    if (curr.left != null)  queue.offer(curr.left);
    if (curr.right != null) queue.offer(curr.right);
}

// 2. Bottom-Up Height-Balanced Check O(N) Time
private static int checkHeight(TreeNode node) {
    if (node == null) return 0;
    int leftH = checkHeight(node.left);
    if (leftH == -1) return -1;
    int rightH = checkHeight(node.right);
    if (rightH == -1) return -1;
    if (Math.abs(leftH - rightH) > 1) return -1; // Unbalanced!
    return 1 + Math.max(leftH, rightH);
}

// 3. Tree Reconstruction Left Subtree Boundary Offset
int inIndex = inMap.get(rootVal);
int leftSubtreeSize = inIndex - inStart;

// 4. Hibbard BST Deletion Case 3 Helper
TreeNode minNode = findMin(root.right);
root.val = minNode.val;
root.right = deleteNode(root.right, minNode.val);

// 5. General Tree LCA Post-Order Synthesis
TreeNode left = LCA(root.left, p, q), right = LCA(root.right, p, q);
if (left != null && right != null) return root;
return left != null ? left : right;

// 6. Max Path Sum Subtree Gain Pruning & Return
int leftGain = Math.max(0, maxGain(node.left));
int rightGain = Math.max(0, maxGain(node.right));
maxSum = Math.max(maxSum, node.val + leftGain + rightGain);
return node.val + Math.max(leftGain, rightGain);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Dynamic `queue.size()` in BFS Loop**: Evaluating `i < queue.size()` directly inside the loop causes children added during the loop to be processed in the current level! Always snapshot `int levelSize = queue.size()`.
* **Pitfall 2: Top-Down $O(N^2)$ Balanced Check**: Calling `getHeight()` at every node repeatedly causes quadratic slowdown. Always use **Bottom-Up Post-Order Check** returning `-1` on balance failure.
* **Pitfall 3: Validating BST by Checking Immediate Children Only**: Checking `left < node && right > node` fails on deep ancestor violations. Always pass bounding range `[lowerBound, upperBound]`.
* **Pitfall 4: Linear Inorder Scan in Tree Reconstruction**: Scanning `inorder` array linearly on every recursion causes $O(N^2)$ time. Always pre-build `inMap = new HashMap<>()`.
* **Pitfall 5: Returning Arch Path Sum to Parent in LeetCode 124**: Returning `val + left + right` creates invalid branching paths. Return ONLY single branch gain `val + max(left, right)`.
* **Pitfall 6: Duplicating Leaves in Boundary Traversal**: Boundary edge functions MUST explicitly skip leaf nodes (`if (!isLeaf(node))`).

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 10 (TREES & BSTs)                |
+-----------------------------------------------------------------------+
| 1. Edges Invariant: Total Edges E = N - 1                              |
| 2. Handshaking Theorem: Leaf Nodes L = I_2 + 1                        |
| 3. BFS Level Order: Snapshot levelSize = queue.size() BEFORE loop     |
| 4. Morris In-Order: Uses pred.right = curr thread pointers for O(1) space|
| 5. Tree Construction: Pre-build inMap in O(N); leftSize = inIdx - inSt|
| 6. Validate BST: validateRange(node, Long.MIN_VALUE, Long.MAX_VALUE)  |
| 7. Hibbard Deletion: Replace 2-child node with min(right); delete min |
| 8. General LCA: Return root if leftMatch != null && rightMatch != null|
| 9. Parent Pointer LCA: Two Pointers Linked List Intersection          |
| 10. Max Path Sum: Prune negative gain Math.max(0, gain); return branch|
| 11. Max Width: Heap index 2*idx+1, 2*idx+2 with normalize (idx-firstIdx)|
| 12. Flatten Tree: Reversed DFS (Right -> Left -> Root) with prev      |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can prove why total edges $E = N - 1$ and $L = I_2 + 1$.
- [ ] I can write Morris In-Order Traversal in $O(1)$ constant auxiliary space.
- [ ] I can write the queue snapshot level-order template in under 60 seconds.
- [ ] I can write LeetCode 105 (Pre + In reconstruction) using `inMap`.
- [ ] I can write `isValidBST` using valid range recursion `[lower, upper]`.
- [ ] I can implement Hibbard Deletion handling all 3 cases (LeetCode 450).
- [ ] I can write General Tree LCA (LeetCode 236) and Parent Pointer LCA (LeetCode 1650).
- [ ] I can write Binary Tree Maximum Path Sum (LeetCode 124).
- [ ] I can write Maximum Width of Binary Tree (LeetCode 662) with position normalization.
- [ ] I can write Boundary Traversal (LeetCode 545) in 4 distinct steps.
- [ ] I can write In-Place Tree Flattening (LeetCode 114) using Reversed DFS.
- [ ] I can implement a Trie (LeetCode 208) with `insert`, `search`, and `startsWith`.
