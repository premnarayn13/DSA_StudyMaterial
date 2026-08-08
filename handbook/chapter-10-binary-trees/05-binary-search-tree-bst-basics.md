# 05. Binary Search Tree (BST) Fundamentals, Validation & Range Mechanics

## 1. Introduction
A **Binary Search Tree (BST)** is a specialized binary tree that satisfies the **Binary Search Property** at every node. In computer science and technical software engineering interviews, BSTs serve as the core data structure behind dynamic dictionary lookups, range query engines, spatial partitioning trees (k-d Trees), and self-balancing BST sets/maps (Java's `TreeSet` and `TreeMap` implemented via Red-Black Trees). A balanced BST achieves **$O(\log N)$ logarithmic time complexity** for search, insertion, deletion, minimum, maximum, predecessor, and successor queries.

> **Important:** The fundamental invariant of a BST is that for ANY node $X$:
> * Every node in the **Left Subtree** has a value **strictly smaller** than $X.\text{val}$ ($\text{left}.\text{val} < X.\text{val}$).
> * Every node in the **Right Subtree** has a value **strictly larger** than $X.\text{val}$ ($\text{right}.\text{val} > X.\text{val}$).
> * An **In-Order Traversal** of a valid BST produces a **strictly non-decreasing sorted sequence**!

```
BST Invariant Topology:
+-----------------------------------------------------------------------------------+
| Left Subtree Values  : STRICTLY SMALLER than Current Node (< X.val)              |
| Right Subtree Values : STRICTLY GREATER than Current Node (> X.val)              |
| In-Order Traversal   : Yields Sorted Order (e.g. [1, 2, 3, 4, 5]) ⚡             |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & Mathematical Validation

### 2.1 The BST Property Invariant
For a node $X$ in a Binary Search Tree:

$$\forall L \in \text{LeftSubtree}(X), \quad L.\text{val} < X.\text{val}$$
$$\forall R \in \text{RightSubtree}(X), \quad R.\text{val} > X.\text{val}$$

* **Common Pitfall**: Checking ONLY immediate children (`node.left.val < node.val` and `node.right.val > node.val`) is INSUFFICIENT to validate a BST! A node in a right subtree could violate the BST property relative to an ancestor higher up the tree.

### 2.2 Technique 1: Valid Range Recursion (`[lowerBound, upperBound]`)
To validate a BST correctly in $O(N)$ time:
* Pass a valid value range `[lowerBound, upperBound]` down the recursive call stack.
* Initially for the root: `isValidBST(root, Long.MIN_VALUE, Long.MAX_VALUE)`.
* When moving **Left**: The upper bound shrinks to `node.val` $\implies$ `[lowerBound, node.val]`.
* When moving **Right**: The lower bound grows to `node.val` $\implies$ `[node.val, upperBound]`.
* If at any node `curr.val <= lowerBound || curr.val >= upperBound`, the tree is INVALID!

### 2.3 Technique 2: In-Order Traversal State Memory
Since an In-Order traversal of a BST visits nodes in strictly increasing sorted order, we can track the `prev` visited node value:
* Maintain a variable `long prev = Long.MIN_VALUE`.
* Perform In-Order traversal (Left $\to$ Node $\to$ Right).
* At each visited node: If `curr.val <= prev`, return `false`! Update `prev = curr.val`.

```
Valid vs Invalid BST Example:
VALID BST:             ( 5 )                INVALID BST:           ( 5 )
                      /     \                                     /     \
                    ( 3 )   ( 7 )                               ( 3 )   ( 7 )
                   /     \                                     /     \
                 ( 1 )   ( 4 )                               ( 1 )   ( 4 )  <- INVALID! (4 < 5 OK, but...)
                                                                      \
                                                                      ( 6 ) <- 6 is in Left Subtree of 5! (6 > 5 Violation!)
```

> **Memory Trick:** **"Validate BST: Pass valid range [min, max] down recursion! Moving Left updates max; Moving Right updates min!"**

---

## 3. Characteristics & Problem Variations

### 3.1 K-th Smallest Element in a BST (LeetCode 230)
* Perform an **In-Order Traversal** (Iterative Stack or Recursive).
* Maintain a counter `count`. Each time a node is visited in-order, increment `count++`.
* When `count == k`, the current node is the **$K$-th Smallest Element** in $O(H + K)$ time!

### 3.2 Lowest Common Ancestor (LCA) in a BST (LeetCode 235)
Due to the BST search property, finding the LCA of two nodes $P$ and $Q$ ($P.\text{val} < Q.\text{val}$) is drastically simpler than in a general Binary Tree:
* Start at `root`.
* If BOTH $P$ and $Q$ have values $< \text{curr.val}$: Move to `curr.left`.
* If BOTH $P$ and $Q$ have values $> \text{curr.val}$: Move to `curr.right`.
* Else: The paths to $P$ and $Q$ split at `curr`! `curr` is the **Lowest Common Ancestor** in $O(H)$ time!

```
BST Problem Complexity Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| BST Query             | Time Complexity   | Space Complexity  | Strategy          |
+-----------------------+-------------------+-------------------+-------------------+
| Validate BST (98)     | O(N) Linear ⚡    | O(H) Call Stack   | Valid Range `[min, max]`|
| K-th Smallest (230)   | O(H + K) ⚡       | O(H) Call Stack   | In-Order Counter  |
| LCA in BST (235)      | O(H) Logarithmic⚡| O(1) Iterative ⚡ | Value Range Split |
| Range Sum BST (938)   | O(N) Pruned ⚡    | O(H) Call Stack   | Range Pruning DFS |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Validate Binary Search Tree (LeetCode 98) using Valid Range Check:

```
Tree: [5, 1, 4, null, null, 3, 6]

Node 5: Range (-inf, +inf) -> 5 OK.
- Recurse Left  (Node 1): Range (-inf, 5).
- Recurse Right (Node 4): Range (5, +inf).

Left Child (Node 1): Range (-inf, 5) -> 1 OK.
- Recurse Left/Right: Null -> Return true.

Right Child (Node 4): Range (5, +inf) -> Check: 4 > 5? NO! (4 <= 5 Violation!)
                     Returns FALSE immediately!

Result: isValidBST = FALSE ❌ (Short-circuit $O(N)$ Time!)
```

---

## 5. Visual Diagram
LCA Search Splitting Mechanics in a BST:

```
Target Nodes: P = 2, Q = 4 in BST:

                        ( 6 )   <- P < 6 AND Q < 6 -> Move LEFT to 2!
                       /     \
                     ( 2 )   ( 8 )   <- P == 2 AND Q > 2 -> SPLIT OCCURS AT 2!
                    /     \
                  ( 0 )   ( 4 )

LCA(2, 4) = Node 2! (Found in O(H) time without exploring right subtree at 8!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Validate BST (LeetCode 98), K-th Smallest (LeetCode 230), LCA in BST (LeetCode 235), and Range Sum BST (LeetCode 938):

```java
import java.util.*;

public class BSTBasicsMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }
    }

    // 1. Validate Binary Search Tree (LeetCode 98) O(N) Time, O(H) Space
    public static boolean isValidBST(TreeNode root) {
        return validateRange(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean validateRange(TreeNode node, long lower, long upper) {
        if (node == null) return true;

        if (node.val <= lower || node.val >= upper) {
            return false; // Bounds violation!
        }

        // Left child bounded by node.val upper limit; Right child bounded by node.val lower limit
        return validateRange(node.left, lower, node.val) &&
               validateRange(node.right, node.val, upper);
    }

    // 2. Validate BST via In-Order Traversal Tracking O(N) Time, O(H) Space
    public static class InorderBSTValidator {
        private Long prev = null;

        public boolean isValidBSTInorder(TreeNode root) {
            prev = null;
            return inorderCheck(root);
        }

        private boolean inorderCheck(TreeNode node) {
            if (node == null) return true;

            if (!inorderCheck(node.left)) return false;

            if (prev != null && node.val <= prev) {
                return false; // In-Order sequence must be strictly increasing!
            }
            prev = (long) node.val;

            return inorderCheck(node.right);
        }
    }

    // 3. K-th Smallest Element in a BST (LeetCode 230) O(H + K) Time, O(H) Space
    public static int kthSmallest(TreeNode root, int k) {
        Deque<TreeNode> stack = new ArrayDeque<>();
        TreeNode curr = root;
        int count = 0;

        while (curr != null || !stack.isEmpty()) {
            while (curr != null) {
                stack.push(curr);
                curr = curr.left;
            }

            curr = stack.pop();
            count++;
            if (count == k) {
                return curr.val; // K-th smallest found!
            }

            curr = curr.right;
        }

        return -1;
    }

    // 4. Lowest Common Ancestor of a BST (LeetCode 235) O(H) Time, O(1) Auxiliary Space
    public static TreeNode lowestCommonAncestorBST(TreeNode root, TreeNode p, TreeNode q) {
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val && q.val < curr.val) {
                curr = curr.left; // Both targets in left subtree
            } else if (p.val > curr.val && q.val > curr.val) {
                curr = curr.right; // Both targets in right subtree
            } else {
                return curr; // Split point or matching node is LCA!
            }
        }

        return null;
    }

    // 5. Range Sum of BST (LeetCode 938) O(N) Pruned Time, O(H) Space
    public static int rangeSumBST(TreeNode root, int low, int high) {
        if (root == null) return 0;

        if (root.val < low) {
            return rangeSumBST(root.right, low, high); // Prune left subtree!
        }
        if (root.val > high) {
            return rangeSumBST(root.left, low, high); // Prune right subtree!
        }

        return root.val + rangeSumBST(root.left, low, high) + rangeSumBST(root.right, low, high);
    }
}
```

> **Quick Syntax:**
```java
// LCA in BST Iterative Loop
if (p.val < curr.val && q.val < curr.val) curr = curr.left;
else if (p.val > curr.val && q.val > curr.val) curr = curr.right;
else return curr; // LCA found!
```

---

## 7. Concrete Problem Examples
* **LeetCode 98 - Validate Binary Search Tree**: Valid range recursion `[min, max]`.
* **LeetCode 230 - Kth Smallest Element in a BST**: Iterative In-Order traversal counting.
* **LeetCode 235 - Lowest Common Ancestor of a BST**: Range split LCA search.
* **LeetCode 938 - Range Sum of BST**: Range pruning DFS.

---

## 8. Java Code Demonstration & Dry Run
Demonstration validating BSTs, searching LCA, and computing range sums:

```java
public class BSTBasicsDemo {

    public static void main(String[] args) {
        // Build Valid BST: [5, 3, 7, 1, 4, 6, 8]
        BSTBasicsMaster.TreeNode root = new BSTBasicsMaster.TreeNode(5);
        root.left = new BSTBasicsMaster.TreeNode(3);
        root.right = new BSTBasicsMaster.TreeNode(7);
        root.left.left = new BSTBasicsMaster.TreeNode(1);
        root.left.right = new BSTBasicsMaster.TreeNode(4);
        root.right.left = new BSTBasicsMaster.TreeNode(6);
        root.right.right = new BSTBasicsMaster.TreeNode(8);

        System.out.println("=== 1. Testing BST Validation ===");
        System.out.println("Is Valid BST? " + BSTBasicsMaster.isValidBST(root)); // true

        System.out.println("\n=== 2. K-th Smallest Element (K=3) ===");
        System.out.println("3rd Smallest: " + BSTBasicsMaster.kthSmallest(root, 3)); // Output: 4 (Sorted: 1,3,4,5,6,7,8)

        System.out.println("\n=== 3. Lowest Common Ancestor (P=1, Q=4) ===");
        BSTBasicsMaster.TreeNode lca = BSTBasicsMaster.lowestCommonAncestorBST(root, root.left.left, root.left.right);
        System.out.println("LCA(1, 4): " + lca.val); // Output: 3

        System.out.println("\n=== 4. Range Sum BST (low=4, high=7) ===");
        System.out.println("Range Sum [4..7]: " + BSTBasicsMaster.rangeSumBST(root, 4, 7)); // Output: 4 + 5 + 6 + 7 = 22
    }
}
```

---

## 9. Complexity Analysis

| BST Operation | Balanced Tree Complexity | Degenerate (Skewed) Tree Complexity | Key Advantage |
| :--- | :--- | :--- | :--- |
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | $O(N)$ Linear | Valid range check `[lower, upper]` |
| **LCA in BST (235)** | **$O(\log N)$ Time ⚡**| $O(N)$ Linear | Zero stack space ($O(1)$ Iterative) |
| **K-th Smallest (230)** | **$O(\log N + K)$ ⚡** | $O(N + K)$ Linear | Early exit on $K$-th count |
| **Range Sum (938)** | **$O(\log N + M)$ ⚡** | $O(N)$ Linear | Prunes subtrees outside range |

---

## 10. Edge Cases & Boundary Handling
* **`Integer.MIN_VALUE` and `Integer.MAX_VALUE` Node Values**: If a BST contains `Integer.MIN_VALUE` as a valid node value, initializing range bounds with `Integer.MIN_VALUE` causes false validation failures (`node.val <= lower`). **Always use `Long.MIN_VALUE` and `Long.MAX_VALUE`** for range bounds!
* **Duplicate Node Values**: Standard strict BST definitions require strictly smaller left nodes (`<`) and strictly greater right nodes (`>`). Duplicates are forbidden unless explicitly specified.

---

## 11. Common Mistakes & Anti-Patterns
* **Checking Only Immediate Children**:
  - `node.left.val < node.val && node.right.val > node.val` (Fails to catch invalid grand-ancestor violations!).
  - Always pass bounding range `[lowerBound, upperBound]` down the recursive call stack.
* **Using General Binary Tree LCA Algorithm for BST**:
  - Calling General Tree LCA (LeetCode 236) takes $O(N)$ space and time, ignoring the BST property.
  - BST LCA (LeetCode 235) uses value comparisons to run in $O(\log N)$ time and $O(1)$ space!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `Long.MIN_VALUE` / `Long.MAX_VALUE` is Mandatory in BST Validation:
> If input tree contains `node.val = Integer.MIN_VALUE`, `node.val <= Integer.MIN_VALUE` evaluates `true`, falsely failing validation!
> Using `Long.MIN_VALUE` and `Long.MAX_VALUE` handles full 32-bit integer ranges cleanly.

> **Memory Trick:** **"BST LCA: If P and Q are smaller, go Left! If larger, go Right! First split point is the LCA!"**

---

## 13. System & Implementation Comparisons

| Feature | General Binary Tree LCA (236) | BST LCA (235) |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ Full Tree Traversal | **$O(\log N)$ Path Traversal ⚡** |
| **Auxiliary Space** | $O(H)$ Call Stack Space | **$O(1)$ Iterative Loop ⚡** |
| **Node Comparison** | Post-Order Subtree Match | Value Comparisons (`p.val < curr.val`) |

---

## 14. How to Recognize This in Questions
* **"Validate if a binary tree is a valid Binary Search Tree"** $\rightarrow$ Valid Range Recursion (`validate(node, min, max)`).
* **"Find lowest common ancestor of two nodes in a BST"** $\rightarrow$ BST LCA Iterative Split (`p.val` & `q.val` comparison).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does In-Order traversal of a BST yield nodes in sorted order?**  
  *A:* In-Order visits Left Subtree ($< X$), then Node ($X$), then Right Subtree ($> X$). By induction across all subtrees, every element is visited after all smaller elements and before all larger elements.
* **Q: How does Range Sum BST (LeetCode 938) prune unnecessary subtrees?**  
  *A:* If `curr.val < low`, all nodes in `curr`'s left subtree are also $< \text{low}$, so we completely skip exploring the left subtree. If `curr.val > high`, we skip the right subtree.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BINARY SEARCH TREE (BST) BASICS                       |
+-----------------------------------------------------------------------+
| • BST Invariant: Left < Node < Right (Strictly no duplicates)         |
| • Validate BST: validate(node, Long.MIN_VALUE, Long.MAX_VALUE)        |
| • Moving Left: Upper bound becomes node.val [lower, node.val]         |
| • Moving Right: Lower bound becomes node.val [node.val, upper]        |
| • In-Order BST Traversal: Yields strictly non-decreasing sorted order  |
| • BST LCA (235): If P & Q < curr -> Left; If P & Q > curr -> Right; Else LCA|
| • K-th Smallest (230): In-order traversal counter k                   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `isValidBST` using valid range recursion `[lower, upper]`.
- [ ] I know why `Long.MIN_VALUE` is used instead of `Integer.MIN_VALUE`.
- [ ] I can write BST LCA (LeetCode 235) in $O(1)$ space iteratively.
- [ ] I can find the $K$-th smallest element in a BST using iterative In-Order.
- [ ] I can implement Range Sum BST (LeetCode 938) with subtree pruning.
