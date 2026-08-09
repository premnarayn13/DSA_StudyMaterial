# 11. BST Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly mapping problem statements to optimal Binary Search Tree design patterns during a technical coding interview enables solving BST searches, range queries, node deletions, and structural re-balancing in **$O(1)$ space and $O(\log N)$ logarithmic time**. BST problems resolve into **5 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal data structure strategies, along with copy-paste production Java templates.

> **Important:** Master the primary selection rules:
> 1. **Iterative Unidirectional Search `curr = (val < curr.val) ? left : right`**: Use for BST search, minimum, maximum, and insertion in $O(1)$ space.
> 2. **Range Bounds Recursion `(minBound, maxBound)`**: Use for BST validation (using `Long` bounds) and compact BST serialization.
> 3. **3-Case Node Deletion (`findMin(root.right)`)**: Use for BST node deletion and subtree pruning.
> 4. **Ancestor Candidate Recording (`if (p.val < curr.val) succ = curr`)**: Use for In-Order successor and predecessor search in $O(1)$ space.
> 5. **Reverse In-Order Traversal (`Right -> Root -> Left`)**: Use for Greater Tree transformation and cumulative sum updates.

---

## 2. Master BST Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER BST PROBLEM DECISION MATRIX                                                                |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Search for target value / insert new key"        | Iterative Search/Insert| `curr = (target<val)?L:R`|
| "Validate if binary tree is a valid BST"          | Range Bounds (`Long`) | `validateRange(min, max)`|
| "Delete a node from BST preserving BST order"     | 3-Case Node Deletion  | `findMin(root.right)` |
| "Find next / previous in-order node in BST"       | Ancestor Record Search| `if (p.val < val) succ=curr`|
| "Replace every key with sum of all larger keys"   | Reverse In-Order DFS  | `Right -> Root -> Left`|
| "Balance a skewed BST in O(N) linear time"        | In-Order + Midpoint   | `mid = (left + right) / 2`|
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Iterative BST Search & Insertion Template
* **Signal**: Search in BST, Insert into BST, Min, Max (700, 701).

```java
public static TreeNode iterativeBSTSearchTemplate(TreeNode root, int target) {
    TreeNode curr = root;
    while (curr != null && curr.val != target) {
        if (target < curr.val) curr = curr.left;
        else curr = curr.right;
    }
    return curr; // Returns matching node or null
}
```

---

## 4. Pattern 2: Range Bounds Validation Template
* **Signal**: Validate BST, Compact BST Codec (98, 449).

```java
public static boolean validateBSTTemplate(TreeNode root) {
    return validateRange(root, Long.MIN_VALUE, Long.MAX_VALUE);
}

private static boolean validateRange(TreeNode node, long minBound, long maxBound) {
    if (node == null) return true;
    if (node.val <= minBound || node.val >= maxBound) return false;
    return validateRange(node.left, minBound, node.val) &&
           validateRange(node.right, node.val, maxBound);
}
```

---

## 5. Pattern 3: 3-Case Structural Node Deletion Template
* **Signal**: Delete node in a BST (450).

```java
public static TreeNode deleteNodeTemplate(TreeNode root, int key) {
    if (root == null) return null;
    if (key < root.val) root.left = deleteNodeTemplate(root.left, key);
    else if (key > root.val) root.right = deleteNodeTemplate(root.right, key);
    else {
        if (root.left == null) return root.right;
        if (root.right == null) return root.left;
        TreeNode successor = findMin(root.right);
        root.val = successor.val;
        root.right = deleteNodeTemplate(root.right, successor.val);
    }
    return root;
}
private static TreeNode findMin(TreeNode n) {
    while (n.left != null) n = n.left;
    return n;
}
```

---

## 6. Pattern 4: In-Order Successor / Predecessor Search Template
* **Signal**: In-order successor, In-order predecessor, Floor, Ceiling (285).

```java
public static TreeNode successorTemplate(TreeNode root, TreeNode p) {
    if (p.right != null) return findMin(p.right); // Case A
    TreeNode successor = null, curr = root;
    while (curr != null) {
        if (p.val < curr.val) { successor = curr; curr = curr.left; }
        else curr = curr.right;
    }
    return successor; // Case B
}
```

---

## 7. Pattern 5: Reverse In-Order Traversal Template
* **Signal**: Convert BST to Greater Tree, cumulative sum updates (538, 1038).

```java
private static int runningSum = 0;

public static TreeNode convertBSTTemplate(TreeNode root) {
    runningSum = 0;
    reverseInorder(root);
    return root;
}

private static void reverseInorder(TreeNode node) {
    if (node == null) return;
    reverseInorder(node.right); // 1. Right
    runningSum += node.val;     // 2. Root
    node.val = runningSum;
    reverseInorder(node.left);  // 3. Left
}
```

---

## 8. Edge Case & Trap Checklist
* **`Integer.MIN_VALUE` Overflow**: Always use `Long.MIN_VALUE` and `Long.MAX_VALUE` for BST validation bounds.
* **Child Reference Re-assignment**: Always set `root.left = deleteNode(root.left, key)` during recursive deletion.
* **Successor Candidate Recording**: Record candidate successor ONLY when turning LEFT (`p.val < curr.val`).
* **Predecessor Candidate Recording**: Record candidate predecessor ONLY when turning RIGHT (`p.val > curr.val`).

---

## 9. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: BST PATTERN RECOGNITION                              |
+-----------------------------------------------------------------------+
| 1. Iterative Search: while (curr != null) curr = (target < val) ? L:R |
| 2. Validate BST   : Range bounds (Long.MIN_VALUE, Long.MAX_VALUE)      |
| 3. Delete Node    : 2-child case swaps val with findMin(root.right)   |
| 4. Successor      : If p.right != null findMin(p.right); else record left|
| 5. Predecessor    : If p.left != null findMax(p.left); else record right|
| 6. Greater Tree   : Reverse In-Order DFS (Right -> Root -> Left)       |
| 7. Balance BST    : In-order extract to array -> Build via midpoint mid|
+-----------------------------------------------------------------------+
```

---

## 10. Practice Checklist
- [ ] I can write all 5 production BST templates from memory in under 10 minutes.
- [ ] I can select the correct BST pattern within 30 seconds of reading a prompt.
- [ ] I know why `Long` range bounds are mandatory for validation.
- [ ] I know why candidate successors are recorded when turning left.
- [ ] I can derive Reverse In-Order traversal for Greater Trees.
