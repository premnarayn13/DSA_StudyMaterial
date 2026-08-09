# 17. Tree Pattern Recognition, Decision Matrix & Production Templates

## 1. Introduction
Instantly matching problem statements to optimal Tree design patterns during a technical coding interview enables solving complex tree traversals, BST range searches, and path optimization problems in **$O(\log N)$ or $O(N)$ linear time**. Tree problems resolve into **6 Core Pattern Families**. This section provides a master pattern decision matrix mapping verbal problem signals to optimal data structure strategies, along with copy-paste production Java templates.

> **Important:** Master the primary selection rules:
> 1. **Bottom-Up DFS Subtree Return**: Use for tree height, balance, subtree sum, and LCA problems.
> 2. **Queue BFS Level-Order Snapshot**: Use for level-by-level processing, level averages, and right-side views.
> 3. **BST Range Partitioning `(min, max)`**: Use for BST validation, BST insertion/deletion, and BST range construction.
> 4. **Preorder DFS String Codec**: Use for binary tree serialization and deserialization with `#` markers.

---

## 2. Master Tree Problem Decision Matrix

```
+---------------------------------------------------------------------------------------------------+
| MASTER TREE PROBLEM DECISION MATRIX                                                               |
+---------------------------------------------------+-----------------------+-----------------------+
| Problem Verbal Signal                             | Recommended Pattern   | Key Mechanism / Code  |
+---------------------------------------------------+-----------------------+-----------------------+
| "Determine if tree is height-balanced / count nodes"| Bottom-Up DFS Return| `1 + max(left, right)`|
| "Traverse tree level by level / find level average"| BFS Queue Snapshot   | `int size = q.size()` |
| "Validate Binary Search Tree / find Kth smallest" | BST Bounds / Inorder  | Range `(min, max)`    |
| "Find lowest common ancestor of 2 nodes"          | LCA Subtree Split     | `if (L!=null && R!=null)`|
| "Find maximum path sum across any 2 nodes"        | Global Max DFS Arch   | Clamp `max(0, gain)`  |
| "Serialize and deserialize a binary tree"         | Preorder DFS Codec    | `#` null sentinel Queue|
+---------------------------------------------------+-----------------------+-----------------------+
```

---

## 3. Pattern 1: Bottom-Up DFS Subtree Return Template
* **Signal**: Tree height, height balance check, subtree node counts (104, 110, 222).

```java
public static int bottomUpDFSTemplate(TreeNode root) {
    if (root == null) return 0;
    int leftVal = bottomUpDFSTemplate(root.left);
    if (leftVal == -1) return -1; // Early exit on unbalanced
    int rightVal = bottomUpDFSTemplate(root.right);
    if (rightVal == -1) return -1;

    if (Math.abs(leftVal - rightVal) > 1) return -1; // Violation check
    return 1 + Math.max(leftVal, rightVal);
}
```

---

## 4. Pattern 2: BFS Queue Level Snapshot Template
* **Signal**: Level-by-level traversal, level averages, zigzag level order (102, 103, 199).

```java
public static List<List<Integer>> levelOrderTemplate(TreeNode root) {
    List<List<Integer>> result = new ArrayList<>();
    if (root == null) return result;
    Queue<TreeNode> queue = new ArrayDeque<>();
    queue.offer(root);

    while (!queue.isEmpty()) {
        int levelSize = queue.size(); // Level Snapshot!
        List<Integer> level = new ArrayList<>(levelSize);
        for (int i = 0; i < levelSize; i++) {
            TreeNode curr = queue.poll();
            level.add(curr.val);
            if (curr.left != null) queue.offer(curr.left);
            if (curr.right != null) queue.offer(curr.right);
        }
        result.add(level);
    }
    return result;
}
```

---

## 5. Pattern 3: BST Range Partitioning `(min, max)` Template
* **Signal**: Validate BST, BST range construction, BST search (98, 108, 449).

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

## 6. Pattern 4: Lowest Common Ancestor (LCA) Template
* **Signal**: Finding lowest common ancestor of two nodes in binary tree (236, 235).

```java
public static TreeNode lcaTemplate(TreeNode root, TreeNode p, TreeNode q) {
    if (root == null || root == p || root == q) return root;
    TreeNode left = lcaTemplate(root.left, p, q);
    TreeNode right = lcaTemplate(root.right, p, q);

    if (left != null && right != null) return root; // Split point!
    return (left != null) ? left : right;
}
```

---

## 7. Pattern 5: Global Max DFS Path Sum Arch Template
* **Signal**: Max path sum, diameter of binary tree (124, 543).

```java
private static int globalMaxSum = Integer.MIN_VALUE;

public static int maxPathSumTemplate(TreeNode root) {
    globalMaxSum = Integer.MIN_VALUE;
    dfsMaxGain(root);
    return globalMaxSum;
}

private static int dfsMaxGain(TreeNode node) {
    if (node == null) return 0;
    int leftGain = Math.max(0, dfsMaxGain(node.left));
    int rightGain = Math.max(0, dfsMaxGain(node.right));

    globalMaxSum = Math.max(globalMaxSum, node.val + leftGain + rightGain); // Arch update
    return node.val + Math.max(leftGain, rightGain); // Single branch return
}
```

---

## 8. Pattern 6: Preorder DFS String Codec Template
* **Signal**: Binary tree serialization and deserialization (297).

```java
public static class TreeCodecTemplate {
    public String serialize(TreeNode root) {
        StringBuilder sb = new StringBuilder();
        buildStr(root, sb);
        return sb.toString();
    }
    private void buildStr(TreeNode n, StringBuilder sb) {
        if (n == null) { sb.append("#,"); return; }
        sb.append(n.val).append(",");
        buildStr(n.left, sb); buildStr(n.right, sb);
    }

    public TreeNode deserialize(String data) {
        Queue<String> q = new LinkedList<>(Arrays.asList(data.split(",")));
        return buildTree(q);
    }
    private TreeNode buildTree(Queue<String> q) {
        String val = q.poll();
        if (val.equals("#")) return null;
        TreeNode root = new TreeNode(Integer.parseInt(val));
        root.left = buildTree(q); root.right = buildTree(q);
        return root;
    }
}
```

---

## 9. Edge Case & Trap Checklist
* **Level Snapshot Freeze**: Always set `int levelSize = queue.size()` before level loop.
* **BST Range Overflow**: Always use `Long.MIN_VALUE` and `Long.MAX_VALUE` for BST bounds.
* **Max Path Branch Return**: Helper MUST return single branch `node.val + max(left, right)` (NOT arch sum).
* **Prefix Sum Backtracking**: Always decrement prefix map frequency when exiting subtree in Path Sum III.

---

## 10. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION: TREE PATTERN RECOGNITION                             |
+-----------------------------------------------------------------------+
| 1. Height Balance (110): Return -1 on unbalanced subtree              |
| 2. Level Order (102)  : Freeze int levelSize = queue.size()           |
| 3. Validate BST (98)  : Pass Long range bounds (minBound, maxBound)   |
| 4. LCA (236)          : If (left != null && right != null) return root|
| 5. Max Path Sum (124) : Update global with arch; Return single branch |
| 6. Serializer (297)   : Preorder DFS with '#' markers + token Queue   |
| 7. BST Codec (449)    : Zero null markers! Deserializes via (min, max)|
| 8. Tree Views (199)   : Right view DFS root->right->left if (d == size)|
+-----------------------------------------------------------------------+
```

---

## 11. Practice Checklist
- [ ] I can write all 6 production templates from memory in under 10 minutes.
- [ ] I can select the correct pattern within 30 seconds of reading a prompt.
- [ ] I know why arch sum cannot be returned to parent in 124.
- [ ] I know why `Long` bounds are required in BST validation.
- [ ] I can write level order snapshot BFS without dynamic queue size bugs.
