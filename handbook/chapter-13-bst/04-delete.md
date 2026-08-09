# 04. BST Node Deletion Mechanics, 3-Case Structural Pointer Relinking & In-Order Successor Substitution

## 1. Introduction
Deleting a node from a **Binary Search Tree (BST)**—specifically **Delete Node in a BST (LeetCode 450)**—is the most structurally complex core BST operation. Deleting a key requires searching for the target node and executing structural pointer relinking across **3 distinct node cases** to maintain valid BST ordering ($L < Root < R$) in **$O(H)$ logarithmic time** (where $H = \log N$ in a balanced BST) and **$O(H)$ auxiliary space**.

> **Important:** The 3 Canonical Structural Cases of BST Node Deletion (LeetCode 450):
> 1. **Case 1: Target Node is a LEAF (0 Children)**: Remove the node directly (`return null`).
> 2. **Case 2: Target Node has 1 CHILD**: Replace the target node with its single non-null child (`return root.left != null ? root.left : root.right`).
> 3. **Case 3: Target Node has 2 CHILDREN**: Replace the target node's value with its **In-Order Successor** (Smallest key in Right Subtree) OR **In-Order Predecessor** (Largest key in Left Subtree), then recursively delete the successor from the right subtree! ⚡

```
BST 2-Child Deletion Substitution Topology:
Target Node to Delete : [ Val 10 ]  (Has 2 Children: Left=5, Right=15)
In-Order Successor    : [ Val 12 ]  (Min node in Right Subtree of 15)
Action Sequence       : 1. Overwrite Val 10 with Val 12!
                        2. Recursively delete Node 12 from Right Subtree! ⚡
```

---

## 2. Core Concepts & The 3 Deletion Cases

### 2.1 Case-by-Case Pointer Relinking Rules
When `root.val == key` is matched:

```
+-----------------------+-------------------+-------------------+-------------------+
| Structural Case       | Child Configuration| Action Taken      | Return Value      |
+-----------------------+-------------------+-------------------+-------------------+
| **Case 1: 0 Children**| Left=null, Right=null| Remove leaf node| **`return null` ⚡**|
| **Case 2: 1 Child**   | Left=null OR Right=null| Promote child   | **`return non-null child` ⚡**|
| **Case 3: 2 Children**| Left!=null & Right!=null| Successor swap  | **`root.val = successor.val`**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Delete 0 children: return null! Delete 1 child: return single child! Delete 2 children: swap value with findMin(root.right) and delete successor!"**

---

## 3. Characteristics & In-Order Successor Reduction Proof

### 3.1 Why Case 3 Reduction Always Succeeds
When deleting a target node $X$ that has 2 children:
1. $X$'s **In-Order Successor** $S = \text{findMin}(X.\text{right})$ is the minimum key in $X$'s right subtree.
2. Because $S$ is the MINIMUM key in $X$'s right subtree, $S$ **CANNOT HAVE A LEFT CHILD** (`S.left == null`).
3. Therefore, deleting $S$ from $X$'s right subtree is guaranteed to trigger **Case 1 (0 children)** or **Case 2 (1 child)**, simplifying complex 2-child deletion into a trivial single-child removal! ⚡

---

## 4. Internal Working Mechanics
Tracing Delete Node in a BST (LeetCode 450) deleting key 5 from tree `[5, 3, 6, 2, 4, null, 7]`:

```
Target key 5 matched at Root! (Has 2 children: Left=3, Right=6).

Step 1: Find In-Order Successor in Right Subtree (root.right = 6):
  - Min node in right subtree of 6 is Node 6 itself (6.left is null).
  - In-Order Successor = Node 6.

Step 2: Overwrite Target Node Value:
  - root.val = 6. Tree temporarily becomes [6, 3, 6, 2, 4, null, 7].

Step 3: Recursively Delete Successor Key 6 from Right Subtree:
  - Call deleteNode(root.right, 6):
  - Key 6 matches node 6. Node 6 has 1 child (Right=7).
  - Case 2 applies: return node.right (Node 7).
  - root.right becomes Node 7.

Final Rebalanced Tree = [6, 3, 7, 2, 4] in Valid BST Order! ✅ (O(H) Time!)
```

---

## 5. Visual Diagram
BST Node Deletion 3-Case Topography:

```
Case 1: Leaf Deletion          Case 2: Single Child Deletion    Case 3: Two Children Deletion
    (5)                            (5)                             [ 5 ] <- Replace with 6!
   /   \                          /   \                           /     \
 (3)   (7) <- Delete!           (3)   (7) <- Delete!            (3)     (6) <- Min in Right
  |                              |       \                        \
Return null                    Return    (8)                    Delete 6!
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Delete Node in a BST (LeetCode 450) using In-Order Successor (`findMin(root.right)`) and In-Order Predecessor (`findMax(root.left)`):

```java
import java.util.*;

public class BSTDeleteMaster {

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

    // 1. Delete Node in a BST (LeetCode 450) O(H) Time, O(H) Call Stack Space
    public static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Target Key Matched! Execute 3-Case Structural Deletion:

            // Case 1 & Case 2: 0 or 1 Child
            if (root.left == null) {
                return root.right; // If left is null, return right (covers 0 and 1 child)
            } else if (root.right == null) {
                return root.left;  // If right is null, return left
            }

            // Case 3: 2 Children
            // Step 1: Find In-Order Successor (Smallest node in Right Subtree)
            TreeNode successor = findMin(root.right);

            // Step 2: Overwrite target node value with successor value
            root.val = successor.val;

            // Step 3: Recursively delete successor from Right Subtree
            root.right = deleteNode(root.right, successor.val);
        }

        return root;
    }

    // Helper: Find Minimum Node in a Subtree
    public static TreeNode findMin(TreeNode node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }

    // Helper: Find Maximum Node in a Subtree
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
// Case 3 Deletion Block
TreeNode successor = findMin(root.right);
root.val = successor.val;
root.right = deleteNode(root.right, successor.val);
```

---

## 7. Concrete Problem Examples
* **LeetCode 450 - Delete Node in a BST**: Primary 3-case deletion problem.
* **BST Re-balancing & Node Pruning**: Deleting keys out of target ranges.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing BST Node Deletion across 0, 1, and 2-child cases:

```java
public class BSTDeleteDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. BST Node Deletion Test (LeetCode 450) ===");
        // Build Tree:
        //       5
        //     /   \
        //    3     6
        //   / \     \
        //  2   4     7
        BSTDeleteMaster.TreeNode root = new BSTDeleteMaster.TreeNode(5);
        root.left = new BSTDeleteMaster.TreeNode(3, 
            new BSTDeleteMaster.TreeNode(2), new BSTDeleteMaster.TreeNode(4));
        root.right = new BSTDeleteMaster.TreeNode(6, null, new BSTDeleteMaster.TreeNode(7));

        System.out.println("Deleting Key 5 (Has 2 Children)...");
        root = BSTDeleteMaster.deleteNode(root, 5);

        System.out.println("New Root Value: " + root.val); // Output: 6 (In-Order Successor!)
        System.out.println("New Root Right Child Value: " + root.right.val); // Output: 7 ✅
    }
}
```

---

## 9. Complexity Analysis

| Deletion Case | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Case 1 (0 Children)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |
| **Case 2 (1 Child)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |
| **Case 3 (2 Children)** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Root of Single-Node Tree**: Returns `null` safely.
* **Key Not Present in Tree**: Returns original tree structure unmodified.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Re-assign Child References During Search**:
  - Writing `deleteNode(root.left, key)` without assigning `root.left = deleteNode(root.left, key)` breaks parent-child pointer linkage!
  - **Always write: `root.left = deleteNode(root.left, key)`**.
* **Searching for Min in Left Subtree Instead of Right Subtree for Successor**:
  - In-Order Successor is the MINIMUM node in the **RIGHT subtree** (`findMin(root.right)`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Successor Deletion in Case 3 Never Infinite Loops:
> The In-Order Successor `S = findMin(root.right)` is guaranteed to have NO LEFT CHILD (`S.left == null`).
> Therefore, calling `deleteNode(root.right, S.val)` falls immediately into Case 1 or Case 2 and terminates in **$O(H)$ total steps**!

> **Memory Trick:** **"Successor = findMin(root.right)! Predecessor = findMax(root.left)!"**

---

## 13. System & Implementation Comparisons

| Feature | Successor Substitution | Predecessor Substitution |
| :--- | :--- | :--- |
| **Substitution Key** | Min in Right Subtree (`findMin(root.right)`) | Max in Left Subtree (`findMax(root.left)`) |
| **Recursive Call** | `root.right = deleteNode(root.right, S.val)` | `root.left = deleteNode(root.left, P.val)` |
| **Order Validity** | **100% Valid BST Order ⚡** | **100% Valid BST Order ⚡** |

---

## 14. How to Recognize This in Questions
* **"Delete a key from a Binary Search Tree while preserving BST properties"** $\rightarrow$ LeetCode 450 (3-case node deletion).

---

## 15. Frequently Asked Interview Questions
* **Q: How does deleting a node with 2 children maintain valid BST order?**  
  *A:* Replacing node $X$ with its In-Order Successor $S$ (smallest value in $X$'s right subtree) guarantees $S$ is larger than all elements in $X$'s left subtree and smaller than all remaining elements in $X$'s right subtree, preserving the BST invariant globally.
* **Q: Can Case 1 and Case 2 be combined into concise Java code?**  
  *A:* Yes! `if (root.left == null) return root.right; else if (root.right == null) return root.left;` handles 0 children (returns null) and 1 child (returns non-null child) simultaneously!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST NODE DELETION (LEETCODE 450)                      |
+-----------------------------------------------------------------------+
| • Case 1 (0 Children): Return null                                    |
| • Case 2 (1 Child)   : Return single non-null child                     |
| • Case 3 (2 Children): Successor S = findMin(root.right);             |
|                        root.val = S.val;                              |
|                        root.right = deleteNode(root.right, S.val);    |
| • Pointer Assignment : ALWAYS set root.left = deleteNode(root.left, k)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Delete Node in a BST (LeetCode 450) handling all 3 cases.
- [ ] I can write `findMin` and `findMax` helper functions.
- [ ] I know why the In-Order Successor has no left child.
- [ ] I know how 0 and 1 child cases are combined in concise Java code.
- [ ] I can trace 2-child deletion step by step.
