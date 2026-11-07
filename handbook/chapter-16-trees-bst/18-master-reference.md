# 18. Master Reference — Trees & Binary Search Trees

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 11: Trees & Binary Search Trees**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh Tree metrics (Root depth = 0, Leaf height = 0), Perfect tree node count $2^H - 1$, In-Order BST sorted invariant, BFS queue snapshot `int size = queue.size()`, BST validation `Long` range bounds, 3-case node deletion (2-child successor substitution), AVL 4-case rotations, Red-Black 5 invariants and 2-rotation insert limit, Preorder + Inorder tree reconstruction, LCA split condition, Max Path Sum arch vs single branch return, Preorder `#` null token serialization, and B+ Tree leaf doubly linked lists!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Tree Edges Formula**:
  - $E = N - 1$ edges for any valid tree with $N$ nodes.
* **Perfect Binary Tree Formulas (Height $H$, Root Level 1)**:
  - Total Nodes $N = 2^H - 1$.
  - Total Leaf Nodes $L = 2^{H-1}$.
  - Total Internal Nodes $I = 2^{H-1} - 1 = N - L$.
  - Tree Height $H = \lfloor \log_2 N \rfloor + 1$.
* **Balance Factor Equation**:
  - $\text{BF}(X) = \text{Height}(\text{left}(X)) - \text{Height}(\text{right}(X))$. Unbalanced if $|\text{BF}(X)| \ge 2$.
* **Self-Balancing Height Bounds**:
  - AVL Tree: $H \le 1.44 \log_2 N$.
  - Red-Black Tree: $H \le 2.0 \log_2(N + 1)$.
  - B+ Tree (Fan-out $M$): $H \le \lceil \log_M N \rceil$.
* **BST Invariant Equation**:
  - $\forall L \in \text{left}(X), \text{key}(L) < \text{key}(X)$ and $\forall R \in \text{right}(X), \text{key}(R) > \text{key}(X)$.
* **Binary Tree Maximum Path Sum Arch Equation**:
  - $\text{ArchSum} = \text{node.val} + \max(0, \text{leftGain}) + \max(0, \text{rightGain})$.
  - $\text{BranchReturn} = \text{node.val} + \max(0, \text{leftGain}, \text{rightGain})$.
* **Tree Distance Formula**:
  - $\text{Distance}(P, Q) = \text{Depth}(P) + \text{Depth}(Q) - 2 \cdot \text{Depth}(\text{LCA}(P, Q))$.

```
Trees & BST Invariants & Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| BST In-Order Traversal            | In-Order traversal ALWAYS yields sorted ascending |
| BFS Level Order Snapshot          | Freeze int levelSize = queue.size() before loop   |
| BST Validation Range              | Pass (Long.MIN_VALUE, Long.MAX_VALUE) boundaries  |
| 2-Child BST Deletion              | Overwrite node.val with findMin(root.right).val   |
| AVL 4-Case Rotations              | LL: Right | RR: Left | LR: Left-Right | RL: Right-Left |
| Red-Black Insert Limits           | At most 2 rotations on insert; 3 on delete        |
| Tree Reconstruction               | In-Order index map inMap divides Left/Right subs  |
| LCA Subtree Split                 | If (left != null && right != null) return root    |
| Right Side View DFS               | DFS Root->Right->Left; if (depth == result.size())|
| Preorder Serialization            | Preorder DFS with '#' null tokens + token Queue   |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tree Max Depth (104)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Bottom-up `1 + max(left, right)` |
| **Balanced Check (110)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Early exit `-1` height check |
| **Complete Node Count (222)**| **$O((\log N)^2)$ ⚡** | **$O((\log N)^2)$ ⚡** | **$O((\log N)^2)$ ⚡** | $O(\log N)$ Stack Space | Bitwise `(1 << H) - 1` perfect trees |
| **BFS Level Order (102)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(W)$ Queue Space | Level size snapshot `q.size()` |
| **Morris Traversal** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(1)$ Constant ⚡**| Temporary predecessor threads |
| **BST Search / Insert** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(1)$ Iterative | Binary search branching |
| **BST Delete Node (450)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space | 3 Deletion cases (2-child successor)|
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | `Long` range bounds `(min, max)` |
| **Kth Smallest BST (230)**| **$O(\log N + K)$ ⚡**| **$O(\log N + K)$ ⚡**| $O(N)$ (Skewed Tree) | $O(H)$ Stack Space | Iterative In-Order stack |
| **AVL Tree Ops** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space | $|\text{BF}| \le 1$ with 4 rotations |
| **Red-Black Tree Ops** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space | Color rules; at most 2 rotations |
| **Tree Reconstruct (105)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Map Space | Preorder root + Inorder index map |
| **Binary Tree LCA (236)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Split check `left != null && right != null`|
| **BST LCA (235)** | **$O(H)$ Logarithmic ⚡**| **$O(H)$ Logarithmic ⚡**| $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Value split `p.val < curr < q.val` |
| **Right Side View (199)**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(H)$ Stack Space**| DFS `depth == result.size()` |
| **Tree Codec (297)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Space | Preorder DFS with `#` tokens |
| **Max Path Sum (124)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Clamp `max(0, gain)`; Arch sum update |
| **Path Sum III (437)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Map Space | Prefix sum map + backtracking |
| **Array to BST (108)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(\log N)$ Stack Space | Midpoint index divide & conquer |
| **Greater Tree (538)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Reverse In-Order `Right -> Root -> Left`|
| **B+ Tree Indexing** | **$O(\log_M N)$ ⚡** | **$O(\log_M N)$ ⚡** | **$O(\log_M N)$ ⚡** | $O(N)$ Disk Space | Leaf node doubly linked list |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Tree Implementations                                         |
+-----------------------------------------------------------------------------------+
| Standard Pointer TreeNode          : 32 Bytes per Node (Header + 3 References)    |
| Red-Black Tree Node (RBNode)       : 40 Bytes per Node (Header + 4 Refs + Enum Color)|
| B+ Tree Page (Page Size = 16KB)    : High Cache Line Locality (M = 1000 Fan-out) ⚡  |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. BFS Level Order Queue Snapshot Pattern
int levelSize = queue.size();
for (int i = 0; i < levelSize; i++) {
    TreeNode curr = queue.poll();
    if (curr.left != null) queue.offer(curr.left);
    if (curr.right != null) queue.offer(curr.right);
}

// 2. Validate BST Range Call Pattern
validateRange(node.left, minBound, node.val) && validateRange(node.right, node.val, maxBound);

// 3. 2-Child BST Deletion Line
TreeNode successor = findMin(root.right);
root.val = successor.val;
root.right = deleteNode(root.right, successor.val);

// 4. Binary Tree LCA Split Check Line
if (left != null && right != null) return root;

// 5. Maximum Path Sum Single Branch Return Line
return node.val + Math.max(leftGain, rightGain);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Dynamic `queue.size()` in BFS Level Order**: Evaluating `i < queue.size()` inside the loop re-checks queue size as children are offered, mixing adjacent levels. Always set `int levelSize = queue.size()`.
* **Pitfall 2: Local Parent-Child BST Validation**: Checking only `node.left.val < node.val` misses grand-ancestor violations. Always use `Long` range boundaries.
* **Pitfall 3: Returning Arch Sum in Max Path Sum (124)**: Returning `node.val + leftGain + rightGain` up to parent creates an invalid bifurcated path. Always return single branch `node.val + max(left, right)`.
* **Pitfall 4: Forgetting Prefix Map Backtracking in Path Sum III (437)**: Leaving prefix sums in map when exiting subtree allows left branch sums to corrupt right branches. Always decrement frequency on exit.
* **Pitfall 5: Preorder Subtree Pre-Index Offsetting (105)**: Right subtree preorder start is NOT `preStart + 1`. Always offset by left subtree size: `preStart + leftTreeSize + 1`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 11 (TREES & BST)                 |
+-----------------------------------------------------------------------+
| 1. Edges Formula: E = N - 1 for any valid tree with N nodes           |
| 2. In-Order BST Invariant: In-order traversal yields SORTED ASCENDING! |
| 3. BFS Level Snapshot: Freeze int levelSize = queue.size() before loop|
| 4. Validate BST (98): Pass Long range bounds (minBound, maxBound)     |
| 5. BST 2-Child Delete: Overwrite val with findMin(root.right).val     |
| 6. AVL Rotations: LL -> Right | RR -> Left | LR -> L-R | RL -> R-L    |
| 7. Red-Black Rotations: At most 2 rotations on insert; 3 on delete    |
| 8. Tree Reconstruction: In-order index map inMap divides subtrees     |
| 9. LCA (236): If left != null && right != null -> root IS the LCA!    |
| 10. Right Side View (199): DFS root->right->left; if (d == result.size)|
| 11. Tree Codec (297): Preorder DFS with '#' null tokens + token Queue |
| 12. Max Path Sum (124): Update global with arch; Return single branch |
| 13. Path Sum III (437): Prefix map + backtrack (decrement on exit)    |
| 14. Array to BST (108): Pick mid = left + (right - left) / 2 as root  |
| 15. Greater Tree (538): Reverse In-Order (Right -> Root -> Left)      |
| 16. B+ Tree Indexing: Leaf nodes store ALL data + Doubly Linked List  |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write Maximum Depth (LeetCode 104) and Balanced Check (LeetCode 110).
- [ ] I can write Level Order Traversal (LeetCode 102) using queue snapshot.
- [ ] I can write Morris In-Order Traversal in $O(1)$ space.
- [ ] I can write Validate BST (LeetCode 98) using `Long` range bounds.
- [ ] I can write Delete Node in a BST (LeetCode 450) handling all 3 cases.
- [ ] I can write an AVL Tree with 4-case rotations.
- [ ] I can write a Red-Black Tree insertion with uncle recoloring and rotations.
- [ ] I can write Tree Reconstruction from Preorder & Inorder (LeetCode 105).
- [ ] I can write LCA of Binary Tree (LeetCode 236) and LCA of BST (LeetCode 235).
- [ ] I can write Binary Tree Right Side View (LeetCode 199) using DFS.
- [ ] I can write Tree Serialization & Deserialization (LeetCode 297).
- [ ] I can write Binary Tree Maximum Path Sum (LeetCode 124).
- [ ] I can write Path Sum III (LeetCode 437) with prefix map backtracking.
- [ ] I can write Convert Sorted Array to BST (LeetCode 108).
- [ ] I can write Convert BST to Greater Tree (LeetCode 538).
- [ ] I can implement a Segment Tree and Trie Prefix Tree.
