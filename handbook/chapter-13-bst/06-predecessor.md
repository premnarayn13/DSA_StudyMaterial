# 06. In-Order Predecessor Invariants, Ancestor Candidate Recording & $O(1)$ Space Search

## 1. Introduction
The **In-Order Predecessor** of a node $P$ in a Binary Search Tree (BST) is defined as the node with the **largest key strictly smaller than $P.val$** (the node visited immediately before $P$ during an In-Order traversal). Finding the In-Order Predecessor is the symmetric dual of the successor search, operating in **$O(H)$ logarithmic time** (where $H = \log N$ in a balanced BST) and **$O(1)$ Strict Constant Auxiliary Space**.

> **Important:** The 2 Structural Cases for Finding In-Order Predecessor:
> 1. **Case A: Left Subtree Exists (`P.left != null`)**: The predecessor is the **MAXIMUM NODE IN $P$'s LEFT SUBTREE** (`findMax(P.left)`).
> 2. **Case B: Left Subtree is NULL (`P.left == null`)**: The predecessor is the **LOWEST ANCESTOR** whose right child is also an ancestor of $P$!
>    - **$O(1)$ Space Search Rule**: Traverse down from root. Whenever `P.val > curr.val`, record `predecessor = curr` (candidate predecessor!) and move right (`curr = curr.right`). If `P.val <= curr.val`, move left! ⚡

```
In-Order Predecessor Case A vs Case B Topology:
Case A (Left Subtree Exists):               Case B (Left Subtree Null):
             (20)                                        [ 10 (Predecessor Candidate!) ]
            /    \                                      /  \
 [ 10 (Target P) ] (30)                               (5)  [ 20 ]
     /        \                                              /
   (5)       (15)                                  [ 12 (Target P, left=null) ]
               |
Max in Left = 15 (Predecessor!)              Ancestor recorded when turning RIGHT = 10! ⚡
```

---

## 2. Core Concepts & $O(1)$ Space Search Algorithm

### 2.1 The Ancestor Recording Algorithm for Predecessor
To find the In-Order Predecessor of node $P$ starting from `root` in $O(1)$ space:
1. Initialize `predecessor = null`, `curr = root`.
2. While `curr != null`:
   - If `p.val > curr.val`:
     - `predecessor = curr` (Record current node as candidate predecessor!).
     - `curr = curr.right` (Move right to search for a larger valid candidate).
   - Else (`p.val <= curr.val`):
     - `curr = curr.left` (Move left without updating predecessor candidate).
3. Return `predecessor`.

```
Predecessor Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Target P Condition    | Predecessor Loc   | Search Work       | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **`P.left != null`**  | `findMax(P.left)` | $O(H)$ Subtree    | **$O(1)$ Constant ⚡**|
| **`P.left == null`**  | Recorded Ancestor | $O(H)$ Binary Search| **$O(1)$ Constant ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Predecessor Search: If p.val > curr.val, record predecessor = curr and move right; else move left!"**

---

## 3. Characteristics & Property Proofs

### 3.1 Duality Between Successor and Predecessor Algorithms

```
Successor vs Predecessor Dual Syntax Comparison:
+-----------------------+-------------------+-------------------+
| Feature               | In-Order Successor| In-Order Predecessor|
+-----------------------+-------------------+-------------------+
| Subtree Search        | `findMin(P.right)`| `findMax(P.left)` |
| Candidate Record Check| `p.val < curr.val`| `p.val > curr.val`|
| Candidate Assignment  | `successor = curr`| `predecessor = curr`|
| Search Direction      | Move `curr.left`  | Move `curr.right` |
+-----------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Inorder Predecessor for $P = 12$ in BST `[20, 10, 30, 5, 12]`:

```
Init: P = 12 (P.left is null -> Case B!). predecessor = null, curr = root (20).

Step 1: curr = 20. P.val (12) <= 20:
  - Move curr = curr.left (Node 10). (predecessor remains null).

Step 2: curr = 10. P.val (12) > 10:
  - Record candidate: predecessor = Node 10.
  - Move curr = curr.right (Node 12).

Step 3: curr = 12. P.val (12) <= 12:
  - Move curr = curr.left (null).

Loop terminates!

Returns recorded predecessor = Node 10! ✅ (O(H) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Ancestor Predecessor Recording Path Topography:

```
                      (Root 20) (P=12 <= 20, Go Left)
                     /         \
   (Record: pred = 10) [ Node 10 ]      (Node 30) (P=12 > 10, Go Right)
             /          \
          (Node 5)    [ Target 12 ] (P=12 <= 12, Go Left -> Null!)
                          |
                Predecessor = 10! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing In-Order Predecessor in BST in $O(1)$ space and $O(H)$ time:

```java
import java.util.*;

public class BSTPredecessorMaster {

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

    // 1. In-Order Predecessor in BST O(H) Time, O(1) Auxiliary Space (Optimal!)
    public static TreeNode inorderPredecessor(TreeNode root, TreeNode p) {
        if (root == null || p == null) return null;

        // Case A: Left Subtree Exists
        if (p.left != null) {
            return findMax(p.left);
        }

        // Case B: Left Subtree is Null -> Ancestor Recording Search
        TreeNode predecessor = null;
        TreeNode curr = root;

        while (curr != null) {
            if (p.val > curr.val) {
                predecessor = curr; // Record candidate predecessor when turning RIGHT!
                curr = curr.right;
            } else {
                curr = curr.left;
            }
        }

        return predecessor;
    }

    // Helper: Find Maximum Node in Subtree
    public static TreeNode findMax(TreeNode node) {
        while (node.right != null) {
            node = node.right;
        }
        return node;
    }
}
```

> **Quick Syntax:**
```java
// Ancestor Predecessor Recording Line
if (p.val > curr.val) { predecessor = curr; curr = curr.right; }
else curr = curr.left;
```

---

## 7. Concrete Problem Examples
* **Inorder Predecessor in BST**: Core predecessor search.
* **Parent-Pointer Predecessor Search**: Parent pointer navigation.
* **BST Boundary Searches**: Floor element in BST.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing In-Order Predecessor across Case A and Case B:

```java
public class BSTPredecessorDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. In-Order Predecessor Test ===");
        // Build Tree:
        //       20
        //      /  \
        //     10   30
        //    /  \
        //   5   12
        BSTPredecessorMaster.TreeNode root = new BSTPredecessorMaster.TreeNode(20);
        root.left = new BSTPredecessorMaster.TreeNode(10, 
            new BSTPredecessorMaster.TreeNode(5), new BSTPredecessorMaster.TreeNode(12));
        root.right = new BSTPredecessorMaster.TreeNode(30);

        // Test Case A: Target 10 (Left subtree exists: 5)
        BSTPredecessorMaster.TreeNode pred10 = 
            BSTPredecessorMaster.inorderPredecessor(root, root.left);
        System.out.println("Predecessor of 10 (Case A): " + pred10.val); // Output: 5

        // Test Case B: Target 12 (Left subtree null -> Ancestor 10)
        BSTPredecessorMaster.TreeNode pred12 = 
            BSTPredecessorMaster.inorderPredecessor(root, root.left.right);
        System.out.println("Predecessor of 12 (Case B): " + pred12.val); // Output: 10 ✅
    }
}
```

---

## 9. Complexity Analysis

| Structural Case | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Case A (`P.left != null`)** | **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|
| **Case B (`P.left == null`)** | **$O(1)$ Constant ⚡** | **$O(H)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Strict Constant ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Target Node is Smallest in BST**: Predecessor is `null` (no node is smaller).
* **Target Node is Root Node**: Handled cleanly by Case A or Case B.

---

## 11. Common Mistakes & Anti-Patterns
* **Recording Candidates When Moving Left**:
  - Moving left means `p.val <= curr.val`. `curr` can NEVER be a predecessor because `curr.val` is larger than or equal to `p.val`!
  - **ONLY record candidate predecessor when turning RIGHT (`p.val > curr.val`)**.
* **Searching for Min in Left Subtree Instead of Max**:
  - Predecessor is the MAXIMUM node in the **LEFT subtree** (`findMax(p.left)`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Ancestors Are Recorded ONLY When Turning Right for Predecessor:
> In-Order Predecessor requires a key STRICTLY SMALLER than `P.val`.
> When `P.val > curr.val`, `curr` is smaller than `P`, making `curr` a valid candidate predecessor. We record `predecessor = curr` and move RIGHT to check if a larger valid candidate exists.
> When `P.val <= curr.val`, `curr` is larger than or equal to `P`, so it cannot be a predecessor. We move LEFT without updating `predecessor`.

> **Memory Trick:** **"Record predecessor candidate ONLY when turning RIGHT!"**

---

## 13. System & Implementation Comparisons

| Feature | Predecessor Ancestor Search | Successor Ancestor Search |
| :--- | :--- | :--- |
| **Candidate Record Trigger**| `p.val > curr.val` (Turn Right) | `p.val < curr.val` (Turn Left) |
| **Subtree Function** | `findMax(p.left)` | `findMin(p.right)` |
| **Space Complexity** | **$O(1)$ Strict Constant ⚡** | **$O(1)$ Strict Constant ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find previous in-order node in a Binary Search Tree"** $\rightarrow$ Predecessor search.
* **"Find Floor element in a Binary Search Tree"** $\rightarrow$ Predecessor search mechanics.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the In-Order Predecessor of the leftmost node in a BST?**  
  *A:* `null`, because it is the global minimum element in the tree.
* **Q: How does parent-pointer predecessor search work without `root`?**  
  *A:* If `P.left != null`, return `findMax(P.left)`. Else, move up `P = P.parent` while `P` is a left child of its parent; return `P.parent`!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: IN-ORDER PREDECESSOR IN BST                           |
+-----------------------------------------------------------------------+
| • Case A (P.left != null): Predecessor = findMax(P.left)              |
| • Case B (P.left == null): Predecessor = Recorded Ancestor when turning RIGHT|
| • Search Rule: If (p.val > curr.val) { predecessor = curr; curr = right; }|
|                else curr = left;                                      |
| • Space Bounds: O(1) Strict Constant Auxiliary Space ⚡                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write In-Order Predecessor in BST in $O(1)$ space.
- [ ] I can state the 2 structural cases for finding the predecessor.
- [ ] I know why candidates are recorded ONLY when turning right.
- [ ] I know why `findMax(P.left)` handles Case A.
- [ ] I can contrast successor and predecessor algorithms.
