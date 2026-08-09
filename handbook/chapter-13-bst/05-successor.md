# 05. In-Order Successor Invariants, Ancestor Candidate Recording & $O(1)$ Space Search

## 1. Introduction
The **In-Order Successor** of a node $P$ in a Binary Search Tree (BST) is defined as the node with the **smallest key strictly greater than $P.val$** (the node visited immediately after $P$ during an In-Order traversal). Finding the In-Order Successor—specifically **Inorder Successor in BST (LeetCode 285)**—is essential for BST iterators, BST node deletion, and range queries in **$O(H)$ logarithmic time** (where $H = \log N$ in a balanced BST) and **$O(1)$ Strict Constant Auxiliary Space**.

> **Important:** The 2 Structural Cases for Finding In-Order Successor:
> 1. **Case A: Right Subtree Exists (`P.right != null`)**: The successor is the **MINIMUM NODE IN $P$'s RIGHT SUBTREE** (`findMin(P.right)`).
> 2. **Case B: Right Subtree is NULL (`P.right == null`)**: The successor is the **LOWEST ANCESTOR** whose left child is also an ancestor of $P$!
>    - **$O(1)$ Space Search Rule**: Traverse down from root. Whenever `P.val < curr.val`, record `successor = curr` (candidate successor!) and move left (`curr = curr.left`). If `P.val >= curr.val`, move right! ⚡

```
In-Order Successor Case A vs Case B Topology:
Case A (Right Subtree Exists):              Case B (Right Subtree Null):
             (10)                                        [ 20 (Successor Candidate!) ]
            /    \                                      /
          (5)    [ 15 (Target P) ]                  (10)
                 /          \                      /    \
            (12)            (20)                 (5)    [ 12 (Target P, right=null) ]
             |
Min in Right = 12 (Successor!)               Ancestor recorded when turning LEFT = 20! ⚡
```

---

## 2. Core Concepts & $O(1)$ Space Search Algorithm

### 2.1 The Ancestor Recording Algorithm (LeetCode 285)
To find the In-Order Successor of node $P$ starting from `root` in $O(1)$ space:
1. Initialize `successor = null`, `curr = root`.
2. While `curr != null`:
   - If `p.val < curr.val`:
     - `successor = curr` (Record current node as candidate successor!).
     - `curr = curr.left` (Move left to search for a smaller valid candidate).
   - Else (`p.val >= curr.val`):
     - `curr = curr.right` (Move right without updating successor candidate).
3. Return `successor`.

```
Successor Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Target P Condition    | Successor Location| Search Work       | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **`P.right != null`** | `findMin(P.right)`| $O(H)$ Subtree    | **$O(1)$ Constant ⚡**|
| **`P.right == null`** | Recorded Ancestor | $O(H)$ Binary Search| **$O(1)$ Constant ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Successor Search: If p.val < curr.val, record successor = curr and move left; else move right!"**

---

## 3. Characteristics & Property Proofs

### 3.1 Mathematical Proof of $O(H)$ Time & $O(1)$ Space
* **Binary Search Traversal**: The algorithm follows a single top-down path from `root` down to a leaf or $P$.
* At most $H = \log N$ node comparisons are performed.
* No recursion stack or dynamic memory allocations are used $\implies \mathbf{O(H) \text{ Time, } O(1) \text{ Space}}$.

---

## 4. Internal Working Mechanics
Tracing Inorder Successor (LeetCode 285) for $P = 12$ in BST `[20, 10, 30, 5, 12]`:

```
Init: P = 12 (P.right is null -> Case B!). successor = null, curr = root (20).

Step 1: curr = 20. P.val (12) < 20:
  - Record candidate: successor = Node 20.
  - Move curr = curr.left (Node 10).

Step 2: curr = 10. P.val (12) > 10:
  - Move curr = curr.right (Node 12). (successor remains Node 20).

Step 3: curr = 12. P.val (12) >= 12:
  - Move curr = curr.right (null).

Loop terminates!

Returns recorded successor = Node 20! ✅ (O(H) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Ancestor Successor Recording Path Topography:

```
                      [ Root 20 ] (Recorded: successor = 20, Go Left)
                     /         \
              [ Node 10 ]      (Node 30) (P=12 > 10, Go Right)
             /          \
          (Node 5)    [ Target 12 ] (P=12 >= 12, Go Right -> Null!)
                          |
                 Successor = 20! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing In-Order Successor in BST (LeetCode 285) in $O(1)$ space and $O(H)$ time:

```java
import java.util.*;

public class BSTSuccessorMaster {

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

    // 1. In-Order Successor in BST (LeetCode 285) O(H) Time, O(1) Auxiliary Space (Optimal!)
    public static TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        if (root == null || p == null) return null;

        // Case A: Right Subtree Exists
        if (p.right != null) {
            return findMin(p.right);
        }

        // Case B: Right Subtree is Null -> Ancestor Recording Search
        TreeNode successor = null;
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val) {
                successor = curr; // Record candidate successor when turning LEFT!
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }

        return successor;
    }

    // Helper: Find Minimum Node in Subtree
    public static TreeNode findMin(TreeNode node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }
}
```

> **Quick Syntax:**
```java
// Ancestor Successor Recording Line
if (p.val < curr.val) { successor = curr; curr = curr.left; }
else curr = curr.right;
```

---

## 7. Concrete Problem Examples
* **LeetCode 285 - Inorder Successor in BST**: Core successor search.
* **LeetCode 510 - Inorder Successor in BST II**: Parent-pointer successor search.
* **BST Iterators (LeetCode 173)**: Next element extraction.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing In-Order Successor across Case A and Case B:

```java
public class BSTSuccessorDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. In-Order Successor Test (LeetCode 285) ===");
        // Build Tree:
        //       20
        //      /  \
        //     10   30
        //    /  \
        //   5   12
        BSTSuccessorMaster.TreeNode root = new BSTSuccessorMaster.TreeNode(20);
        root.left = new BSTSuccessorMaster.TreeNode(10, 
            new BSTSuccessorMaster.TreeNode(5), new BSTSuccessorMaster.TreeNode(12));
        root.right = new BSTSuccessorMaster.TreeNode(30);

        // Test Case A: Target 10 (Right subtree exists: 12)
        BSTSuccessorMaster.TreeNode succ10 = 
            BSTSuccessorMaster.inorderSuccessor(root, root.left);
        System.out.println("Successor of 10 (Case A): " + succ10.val); // Output: 12

        // Test Case B: Target 12 (Right subtree null -> Ancestor 20)
        BSTSuccessorMaster.TreeNode succ12 = 
            BSTSuccessorMaster.inorderSuccessor(root, root.left.right);
        System.out.println("Successor of 12 (Case B): " + succ12.val); // Output: 20 ✅
    }
}
```

---

## 9. Complexity Analysis

| Structural Case | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Case A (`P.right != null`)**| **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|
| **Case B (`P.right == null`)**| **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Target Node is Largest in BST**: Successor is `null` (no node is greater).
* **Target Node is Root Node**: Handled cleanly by Case A or Case B.

---

## 11. Common Mistakes & Anti-Patterns
* **Using In-Order Traversal Array ($O(N)$ Space Penalty)**:
  - Performing a full In-Order traversal into an array to find `seq[idx + 1]` wastes $O(N)$ space and time.
  - **Use top-down ancestor recording for $O(H)$ time and $O(1)$ space**.
* **Recording Candidates When Moving Right**:
  - Moving right means `p.val >= curr.val`. `curr` can NEVER be a successor because `curr.val` is smaller than or equal to `p.val`!
  - **ONLY record candidate successor when turning LEFT (`p.val < curr.val`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Ancestors Are Recorded ONLY When Turning Left:
> In-Order Successor requires a key STRICTLY GREATER than `P.val`.
> When `P.val < curr.val`, `curr` is greater than `P`, making `curr` a valid candidate successor. We record `successor = curr` and move LEFT to check if a smaller valid candidate exists.
> When `P.val >= curr.val`, `curr` is smaller than or equal to `P`, so it cannot be a successor. We move RIGHT without updating `successor`.

> **Memory Trick:** **"Record successor candidate ONLY when turning LEFT!"**

---

## 13. System & Implementation Comparisons

| Feature | Ancestor Recording Search | In-Order Traversal Array |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(H)$ Logarithmic ⚡** | $O(N)$ Full Tree Scan |
| **Auxiliary Memory** | **$O(1)$ Strict Constant ⚡** | $O(N)$ Array Memory |
| **Tree Modification**| Zero Modification | Zero Modification |

---

## 14. How to Recognize This in Questions
* **"Find next in-order node in a Binary Search Tree"** $\rightarrow$ LeetCode 285 (Successor search).
* **"Implement BST Iterator `hasNext()` and `next()`"** $\rightarrow$ In-Order Successor mechanics.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the In-Order Successor of the rightmost node in a BST?**  
  *A:* `null`, because it is the global maximum element in the tree.
* **Q: How does parent-pointer successor search (LeetCode 510) work without `root`?**  
  *A:* If `P.right != null`, return `findMin(P.right)`. Else, move up `P = P.parent` while `P` is a right child of its parent; return `P.parent`!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: IN-ORDER SUCCESSOR IN BST (LEETCODE 285)              |
+-----------------------------------------------------------------------+
| • Case A (P.right != null): Successor = findMin(P.right)              |
| • Case B (P.right == null): Successor = Recorded Ancestor when turning LEFT|
| • Search Rule: If (p.val < curr.val) { successor = curr; curr = left; }|
|                else curr = right;                                     |
| • Space Bounds: O(1) Strict Constant Auxiliary Space ⚡                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Inorder Successor in BST (LeetCode 285) in $O(1)$ space.
- [ ] I can state the 2 structural cases for finding the successor.
- [ ] I know why candidates are recorded ONLY when turning left.
- [ ] I can handle parent-pointer successor search (LeetCode 510).
- [ ] I can trace successor search for leaf vs internal nodes.
