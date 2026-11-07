# 04. Binary Search Tree (BST) Properties, Validation Bounds & K-th Smallest Invariants

## 1. Introduction
A **Binary Search Tree (BST)** is a node-based binary tree data structure defined by a strict structural order invariant: for EVERY node $X$ in the tree, **all keys in the left subtree are strictly LESS than $X.val$**, and **all keys in the right subtree are strictly GREATER than $X.val$**:

$$\forall \text{ node } L \in \text{left}(X), \text{key}(L) < \text{key}(X) \quad \text{and} \quad \forall \text{ node } R \in \text{right}(X), \text{key}(R) > \text{key}(X)$$

Understanding BST invariants enables solving fundamental search, range, and order statistic problems—such as **Validate Binary Search Tree (LeetCode 98)** and **Kth Smallest Element in a BST (LeetCode 230)**—in **$O(H)$ time** (where $H = \log N$ in a balanced BST).

> **Important:** The single most fundamental property of a Binary Search Tree:
> **An In-Order Traversal (`Left -> Root -> Right`) of a valid BST yields values in STRICTLY ASCENDING SORTED ORDER!**
> Any violation of strictly increasing order (e.g. `prev >= curr.val`) proves the tree is NOT a valid BST! ⚡

```
Binary Search Tree Invariant Topology:
                       [ 10 ]  <--- Root
                      /      \
             [ 5 ]            [ 15 ]
            /     \          /      \
        [ 2 ]    [ 7 ]    [ 12 ]    [ 20 ]

In-Order Traversal Sequence: 2 -> 5 -> 7 -> 10 -> 12 -> 15 -> 20 (Strictly Sorted!) ⚡
```

---

## 2. Core Concepts & BST Validation Algorithms (LeetCode 98)

### 2.1 Why Local Parent-Child Validation FAILS for BST Validation
A common novice mistake when validating a BST is checking only immediate parent-child relationships (`node.left.val < node.val && node.right.val > node.val`).
* **Why it Fails**: A node in a right subtree could be smaller than a higher ancestor node!

```
Invalid BST Example (Local check passes, but tree is INVALID!):
         10
        /  \
       5   15
          /  \
        (6)   20   <--- 6 is < 15 (Local pass), BUT 6 is in RIGHT subtree of 10! INVALID! ❌
```

### 2.2 Correct Validation Strategy 1: Min / Max Range Boundary Passing
Pass a valid value range `(minBound, maxBound)` down recursively:
* Initial Call: `validate(root, Long.MIN_VALUE, Long.MAX_VALUE)`.
* Left Child Recursive Call: Range becomes **`(minBound, node.val)`**. (Upper bound restricted to `node.val`).
* Right Child Recursive Call: Range becomes **`(node.val, maxBound)`**. (Lower bound restricted to `node.val`).
* Base Condition: If `node.val <= minBound || node.val >= maxBound`, return `false`!

### 2.3 Correct Validation Strategy 2: In-Order Prev Pointer Tracking
Perform an In-Order traversal while maintaining a `prev` reference to the previously visited value.
* If `prev != null && node.val <= prev`, return `false`!

```
BST Validation Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Validation Strategy   | Time Complexity   | Auxiliary Space   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| **Min/Max Range**     | **$O(N)$ Linear ⚡**| $O(H)$ Stack Space | Range shrinking `(min, max)`|
| **In-Order Prev**     | **$O(N)$ Linear ⚡**| $O(H)$ Stack Space | Check `prev >= node.val`|
| Local Parent-Child    | WRONG ($O(N)$)    | WRONG             | Fails on grand-ancestors!|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Validate BST: Pass (min, max) bounds recursively! Left child updates max bound; Right child updates min bound!"**

---

## 3. Characteristics & K-th Smallest Element in BST (LeetCode 230)

### 3.1 K-th Smallest Element Algorithm (LeetCode 230)
Given the root of a binary search tree and integer $K$, return the $K$-th smallest value (1-indexed):

#### Algorithmic Strategy ($O(H + K)$ Time, $O(H)$ Space):
* Because BST In-Order traversal processes nodes in sorted ascending order:
  1. Perform an **Iterative In-Order Traversal** using an explicit stack.
  2. Maintain a counter `count = 0`.
  3. On every popped node, increment `count++`.
  4. When `count == K`, return `curr.val` immediately!

```
K-th Smallest In-Order Traversal Step:
Stack Pops Order: 1st Smallest -> 2nd Smallest -> ... -> K-th Smallest!
Stop traversal IMMEDIATELY when count == K to achieve optimal O(H + K) time! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Validate Binary Search Tree (LeetCode 98) on Invalid Tree `[10, 5, 15, null, null, 6, 20]`:

```
Call validate(10, MIN_VAL, MAX_VAL):
  - Left Call : validate(5, MIN_VAL, 10)  -> Valid (5 in range).
  - Right Call: validate(15, 10, MAX_VAL) -> Valid so far.
      - Left Child 6 Call: validate(6, 10, 15):
          - Check: 6 <= 10 (minBound) -> FAILS RANGE CHECK!
          - Returns FALSE!

Validation terminates early with FALSE! Tree is INVALID! ✅ (O(N) Time!)
```

---

## 5. Visual Diagram
BST Min/Max Range Boundary Inheritance Topography:

```
                      Root 10  (Range: -inf ... +inf)
                     /       \
         (Range: -inf ... 10) (Range: 10 ... +inf)
                 /                 \
            Node 5               Node 15
                                 /      \
                    (Range: 10 ... 15)  (Range: 15 ... +inf)
                           /                  \
                       Node 6 (FAIL!)       Node 20
                       (6 is NOT > 10!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Validate BST (LeetCode 98), Kth Smallest Element in BST (LeetCode 230), and In-Order Successor in BST (LeetCode 285):

```java
import java.util.*;

public class BSTPropertiesMaster {

    public static class TreeNode {
        public int val;
        public TreeNode left;
        public TreeNode right;

        public TreeNode(int val) {
            this.val = val;
        }

        public TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    // 1. Validate Binary Search Tree (LeetCode 98) Min/Max Range Strategy O(N) Time, O(H) Space
    public static boolean isValidBST(TreeNode root) {
        return validateRange(root, Long.MIN_VALUE, Long.MAX_VALUE);
    }

    private static boolean validateRange(TreeNode node, long minBound, long maxBound) {
        if (node == null) return true;

        if (node.val <= minBound || node.val >= maxBound) {
            return false; // Out of valid BST range!
        }

        // Left subtree must be < node.val; Right subtree must be > node.val
        return validateRange(node.left, minBound, node.val) &&
               validateRange(node.right, node.val, maxBound);
    }

    // 2. Validate BST In-Order Prev Pointer Strategy O(N) Time, O(H) Space
    private static TreeNode prevNode = null;

    public static boolean isValidBSTInorder(TreeNode root) {
        prevNode = null; // Reset static state
        return inorderCheck(root);
    }

    private static boolean inorderCheck(TreeNode node) {
        if (node == null) return true;

        if (!inorderCheck(node.left)) return false;

        if (prevNode != null && node.val <= prevNode.val) {
            return false; // Violation of strictly ascending order!
        }
        prevNode = node;

        return inorderCheck(node.right);
    }

    // 3. Kth Smallest Element in a BST (LeetCode 230) O(H + K) Time, O(H) Space
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
                return curr.val; // Found K-th smallest element!
            }

            curr = curr.right;
        }

        return -1;
    }

    // 4. Inorder Successor in BST (LeetCode 285) O(H) Time, O(1) Auxiliary Space
    public static TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        TreeNode successor = null;
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val) {
                successor = curr; // Candidate successor found! Move left to find smaller
                curr = curr.left;
            } else {
                curr = curr.right; // Target p is >= curr.val; move right
            }
        }

        return successor;
    }
}
```

> **Quick Syntax:**
```java
// Validate BST Range Call
return validateRange(node.left, minBound, node.val) && validateRange(node.right, node.val, maxBound);
```

---

## 7. Concrete Problem Examples
* **LeetCode 98 - Validate Binary Search Tree**: Min/max range recursion.
* **LeetCode 230 - Kth Smallest Element in a BST**: Iterative in-order traversal.
* **LeetCode 285 - Inorder Successor in BST**: $O(H)$ BST search traversal.
* **LeetCode 501 - Find Mode in Binary Search Tree**: In-order frequency tracking.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `isValidBST` and `kthSmallest`:

```java
public class BSTPropertiesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Valid BST Test ===");
        // Build Valid BST:
        //       5
        //     /   \
        //    3     7
        //   / \
        //  2   4
        BSTPropertiesMaster.TreeNode validRoot = new BSTPropertiesMaster.TreeNode(5);
        validRoot.left = new BSTPropertiesMaster.TreeNode(3, 
            new BSTPropertiesMaster.TreeNode(2), new BSTPropertiesMaster.TreeNode(4));
        validRoot.right = new BSTPropertiesMaster.TreeNode(7);

        System.out.println("Is Valid BST? " + BSTPropertiesMaster.isValidBST(validRoot)); // true

        System.out.println("\n=== 2. K-th Smallest Element Test ===");
        int k3 = BSTPropertiesMaster.kthSmallest(validRoot, 3);
        System.out.println("3rd Smallest Element: " + k3); // Output: 4 (Sorted order: 2, 3, 4)

        System.out.println("\n=== 3. Invalid BST Test ===");
        // Build Invalid Tree: [5, 1, 4, null, null, 3, 6]
        BSTPropertiesMaster.TreeNode invalidRoot = new BSTPropertiesMaster.TreeNode(5);
        invalidRoot.left = new BSTPropertiesMaster.TreeNode(1);
        invalidRoot.right = new BSTPropertiesMaster.TreeNode(4, 
            new BSTPropertiesMaster.TreeNode(3), new BSTPropertiesMaster.TreeNode(6));

        System.out.println("Is Invalid Tree Valid BST? " + BSTPropertiesMaster.isValidBST(invalidRoot)); // false
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space |
| **Kth Smallest (230)**| **$O(\log N + K)$ ⚡**| **$O(\log N + K)$ ⚡**| $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |
| **BST Successor (285)**| **$O(1)$ Constant ⚡**| **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Integer Bounds (`Integer.MIN_VALUE` / `Integer.MAX_VALUE`)**: Using `int` range bounds causes overflow errors when node values equal `Integer.MIN_VALUE`. Always use **`Long.MIN_VALUE` and `Long.MAX_VALUE`** as initial boundaries!
* **Duplicate Node Values in BST**: Standard BSTs do NOT allow duplicate values (`<` and `>` strictly enforced).

---

## 11. Common Mistakes & Anti-Patterns
* **Using `Integer.MIN_VALUE` as Initial Range Bound**:
  - If a single node in the tree has value `Integer.MIN_VALUE`, `node.val <= minBound` returns `false` incorrectly!
  - **Use `Long.MIN_VALUE` and `Long.MAX_VALUE` or `null` Wrapper Objects**.
* **Checking Only Local Parent-Child Bounds**:
  - `node.left.val < node.val` misses grand-ancestor constraint violations.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `Integer.MIN_VALUE` Breaks LeetCode 98:
> LeetCode 98 test cases include trees containing `[Integer.MIN_VALUE]`.
> If you write `validate(root, Integer.MIN_VALUE, Integer.MAX_VALUE)`:
> The check `node.val <= minBound` evaluates `-2147483648 <= -2147483648` to `true`, returning `false` incorrectly!
> **Always use 64-bit `Long.MIN_VALUE` and `Long.MAX_VALUE` boundaries!**

> **Memory Trick:** **"Use Long.MIN_VALUE and Long.MAX_VALUE for BST range bounds to prevent Integer overflow!"**

---

## 13. System & Implementation Comparisons

| Feature | Min/Max Range Boundaries | In-Order Prev Pointer |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Auxiliary Memory** | $O(H)$ Stack Space | $O(H)$ Stack Space |
| **State Management**| Pure Functional Parameters | Requires State Management |

---

## 14. How to Recognize This in Questions
* **"Determine if a binary tree is a valid Binary Search Tree"** $\rightarrow$ LeetCode 98 (Min/max range recursion using `Long` bounds).
* **"Find K-th smallest element in a BST"** $\rightarrow$ LeetCode 230 (Iterative in-order traversal stopping at count $K$).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does an In-Order traversal of a BST produce a sorted array?**  
  *A:* Because In-Order traversal visits `Left Subtree` (smaller elements) $\to$ `Root Node` (middle element) $\to$ `Right Subtree` (larger elements). Recursive application across all subtrees guarantees strictly ascending order.
* **Q: How does `inorderSuccessor` (LeetCode 285) achieve $O(1)$ auxiliary space?**  
  *A:* By navigating down the BST like a binary search. Whenever `p.val < curr.val`, `curr` is a potential candidate successor, so we record `successor = curr` and move left. If `p.val >= curr.val`, we move right. When `curr == null`, the recorded `successor` is the exact In-Order successor!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST PROPERTIES & VALIDATION                           |
+-----------------------------------------------------------------------+
| • BST Invariant: ALL left nodes < Root < ALL right nodes              |
| • BST In-Order Invariant: In-Order traversal yields SORTED ASCENDING! |
| • Validation Bounds: Pass (Long.MIN_VALUE, Long.MAX_VALUE) range      |
| • Overflow Trap: ALWAYS use Long bounds to handle Integer.MIN_VALUE   |
| • K-th Smallest (230): Iterative In-Order stack; stop when count == K |
| • BST Successor (285): Record candidate successor when moving LEFT    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Validate BST (LeetCode 98) using `Long` range bounds.
- [ ] I can write Kth Smallest Element in BST (LeetCode 230) in $O(H + K)$ time.
- [ ] I can write Inorder Successor in BST (LeetCode 285) in $O(1)$ space.
- [ ] I know why local parent-child validation fails.
- [ ] I know why `Integer.MIN_VALUE` causes overflow bugs in BST validation.
