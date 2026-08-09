# 05. BST Operations: Search, Insertion & 3-Case Node Deletion Mechanics

## 1. Introduction
Operations on a **Binary Search Tree (BST)**—specifically **Search (LeetCode 700)**, **Insertion (LeetCode 701)**, and **Deletion (LeetCode 450)**—leverage the BST structural ordering invariant ($L < Root < R$) to eliminate half of the remaining tree candidates at every step. This yields **$O(H)$ logarithmic time complexity** (where $H = \log N$ in a balanced BST). Deletion is the most complex operation, requiring handling **3 distinct structural node cases**.

> **Important:** The 3 Cases of BST Node Deletion (LeetCode 450):
> 1. **Case 1: Node is a LEAF (0 children)**: Remove node directly (`return null`).
> 2. **Case 2: Node has 1 CHILD**: Replace node with its single non-null child (`return child`).
> 3. **Case 3: Node has 2 CHILDREN**: Replace node's value with its **In-Order Successor** (Smallest node in Right Subtree) OR **In-Order Predecessor** (Largest node in Left Subtree), then recursively delete the successor from the right subtree! ⚡

```
BST 2-Child Deletion Substitution Topology:
Target Node to Delete : [ Val 10 ]  (Has 2 Children!)
In-Order Successor    : [ Val 12 ]  (Min node in Right Subtree)
Action                : 1. Overwrite Val 10 with Val 12!
                        2. Recursively delete Node 12 from Right Subtree! ⚡
```

---

## 2. Core Concepts & BST Search & Insertion Algorithms

### 2.1 Search in a Binary Search Tree (LeetCode 700)
Given the root of a BST and an integer `val`:
* If `root == null` OR `root.val == val`: Return `root`.
* If `val < root.val`: Recurse into **`searchBST(root.left, val)`**.
* Else (`val > root.val`): Recurse into **`searchBST(root.right, val)`**.
* Time Complexity: **$O(H)$ Logarithmic Time**, Space: **$O(1)$ Iterative** / **$O(H)$ Recursive**.

### 2.2 Insert into a Binary Search Tree (LeetCode 701)
Given the root of a BST and a value `val` to insert:
* If `root == null`: Return `new TreeNode(val)`.
* If `val < root.val`: `root.left = insertIntoBST(root.left, val)`.
* If `val > root.val`: `root.right = insertIntoBST(root.right, val)`.
* Return `root`.

```
BST Operations Complexity Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Operation Intent      | Best / Avg Time   | Worst Case Time   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| `searchBST(val)`      | **$O(\log N)$ ⚡**| $O(N)$ (Skewed)   | $O(1)$ Iterative  |
| `insertIntoBST(val)`  | **$O(\log N)$ ⚡**| $O(N)$ (Skewed)   | $O(H)$ Stack      |
| `deleteNode(key)`     | **$O(\log N)$ ⚡**| $O(N)$ (Skewed)   | $O(H)$ Stack      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Search & Insert follow simple binary search decisions! Insert attaches new nodes as LEAVES!"**

---

## 3. Characteristics & Deletion of a Node with 2 Children

### 3.1 Why In-Order Successor Substitution Works
When deleting a node $X$ that has BOTH left and right children:
* Deleting $X$ directly would sever two entire subtrees, breaking tree connectivity.
* **Solution**: Replace $X.val$ with a value $S.val$ such that $S.val$ is strictly greater than ALL elements in left subtree AND strictly smaller than ALL remaining elements in right subtree!
* The **In-Order Successor** $S = \text{findMin}(X.right)$ satisfies this condition perfectly!
* Since $S$ is the smallest node in the right subtree, $S$ has AT MOST ONE CHILD (Right Child), reducing the deletion of $S$ to Case 1 or Case 2!

---

## 4. Internal Working Mechanics
Tracing Delete Node in a BST (LeetCode 450) deleting key 5 from tree `[5, 3, 6, 2, 4, null, 7]`:

```
Target key 5 found at Root! (Has 2 children: Left=3, Right=6).

1. Find In-Order Successor in Right Subtree (root.right = 6):
   - Min node in right subtree of 6 is Node 6 itself (6.left is null).
   - In-Order Successor = Node 6.

2. Overwrite Target Node Value:
   - root.val = 6. Tree becomes [6, 3, 6, 2, 4, null, 7].

3. Recursively Delete Successor Key 6 from Right Subtree:
   - Call deleteNode(root.right, 6):
   - Key 6 matches node 6. Node 6 has 1 child (Right=7).
   - Case 2 applies: return node.right (Node 7).
   - root.right becomes 7.

Final Tree = [6, 3, 7, 2, 4] in Valid BST Order! ✅ (O(H) Time!)
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
Production-grade Java suite implementing Search (LeetCode 700), Insertion (LeetCode 701), and 3-Case Deletion (LeetCode 450):

```java
import java.util.*;

public class BSTOperationsMaster {

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

    // 1. Search in a BST (LeetCode 700) O(H) Time, O(1) Iterative Space
    public static TreeNode searchBST(TreeNode root, int val) {
        TreeNode curr = root;
        while (curr != null && curr.val != val) {
            if (val < curr.val) {
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }
        return curr;
    }

    // 2. Insert into a BST (LeetCode 701) O(H) Time, O(H) Recursion Space
    public static TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val);
        }

        if (val < root.val) {
            root.left = insertIntoBST(root.left, val);
        } else if (val > root.val) {
            root.right = insertIntoBST(root.right, val);
        }

        return root;
    }

    // 3. Delete Node in a BST (LeetCode 450) O(H) Time, O(H) Recursion Space
    public static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Target Key Found! Execute 3-Case Deletion:

            // Case 1 & 2: 0 or 1 Child
            if (root.left == null) {
                return root.right;
            } else if (root.right == null) {
                return root.left;
            }

            // Case 3: 2 Children
            // Find In-Order Successor (Smallest node in Right Subtree)
            TreeNode successor = findMin(root.right);

            // Overwrite value with successor's value
            root.val = successor.val;

            // Recursively delete successor from Right Subtree
            root.right = deleteNode(root.right, successor.val);
        }

        return root;
    }

    // Helper to find minimum node in a BST subtree
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
// 2-Child Deletion Handling
TreeNode successor = findMin(root.right);
root.val = successor.val;
root.right = deleteNode(root.right, successor.val);
```

---

## 7. Concrete Problem Examples
* **LeetCode 700 - Search in a Binary Search Tree**: Basic BST search.
* **LeetCode 701 - Insert into a Binary Search Tree**: Leaf insertion.
* **LeetCode 450 - Delete Node in a BST**: 3-case node deletion.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing BST Search, Insertion, and Deletion:

```java
public class BSTOperationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. BST Insertion & Search ===");
        BSTOperationsMaster.TreeNode root = null;
        root = BSTOperationsMaster.insertIntoBST(root, 5);
        root = BSTOperationsMaster.insertIntoBST(root, 3);
        root = BSTOperationsMaster.insertIntoBST(root, 6);
        root = BSTOperationsMaster.insertIntoBST(root, 2);
        root = BSTOperationsMaster.insertIntoBST(root, 4);

        System.out.println("Search Key 4: Found Val = " + 
            BSTOperationsMaster.searchBST(root, 4).val); // Output: 4

        System.out.println("\n=== 2. BST Deletion Test (Case 3: 2 Children) ===");
        System.out.println("Deleting Root Key 5 (Has 2 Children: Left=3, Right=6)...");
        root = BSTOperationsMaster.deleteNode(root, 5);

        System.out.println("New Root Value after Deletion: " + root.val); // Output: 6 (In-Order Successor!)
        System.out.println("Search Old Key 5: " + 
            (BSTOperationsMaster.searchBST(root, 5) == null ? "Not Found" : "Found")); // Not Found
    }
}
```

---

## 9. Complexity Analysis

| BST Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Search (700)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(1)$ Iterative |
| **Insert (701)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |
| **Delete (450)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Root of Single-Node Tree**: Returns `null`.
* **Inserting Duplicate Values**: Standard BSTs ignore duplicate insertions or increment a frequency count on existing nodes.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Re-assign Subtree References During Deletion**:
  - Writing `deleteNode(root.left, key)` without assigning `root.left = deleteNode(root.left, key)` fails to update parent-child pointer links!
  - **Always assign return values: `root.left = deleteNode(root.left, key)`**.
* **Searching for Min in Left Subtree Instead of Right Subtree for Successor**:
  - In-Order Successor is the minimum node in the **RIGHT subtree** (`findMin(root.right)`).
  - In-Order Predecessor is the maximum node in the **LEFT subtree** (`findMax(root.left)`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The 2 Equivalent Substitution Rules for Case 3 Deletion:
> To delete a node with 2 children:
> 1. Replace value with **In-Order Successor** (`findMin(root.right)`), then delete successor from `root.right`.
> 2. OR Replace value with **In-Order Predecessor** (`findMax(root.left)`), then delete predecessor from `root.left`.
> Both approaches maintain valid BST order!

> **Memory Trick:** **"Successor = Min in Right Subtree! Predecessor = Max in Left Subtree!"**

---

## 13. System & Implementation Comparisons

| Feature | Iterative BST Operations | Recursive BST Operations |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(H)$ Logarithmic ⚡** | **$O(H)$ Logarithmic ⚡** |
| **Auxiliary Memory** | **$O(1)$ Strict Constant ⚡**| $O(H)$ Call Stack Space |
| **Code Readability** | Moderate (Loop management) | High (Clean recursive links) |

---

## 14. How to Recognize This in Questions
* **"Search for a value in a Binary Search Tree"** $\rightarrow$ LeetCode 700 ($O(H)$ search).
* **"Delete a node from a BST while maintaining valid BST properties"** $\rightarrow$ LeetCode 450 (3-case node deletion).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does deletion of a node with 2 children reduce to deleting a node with 0 or 1 child?**  
  *A:* Because the In-Order Successor is the MINIMUM node in the right subtree, meaning it has NO left child (`successor.left == null`). Therefore, deleting the successor from the right subtree falls into Case 1 (0 children) or Case 2 (1 child), which is trivial.
* **Q: What causes BST operations to degrade from $O(\log N)$ down to $O(N)$ worst-case time?**  
  *A:* Inserting elements in already sorted order (e.g. `1, 2, 3, 4, 5`) creates a Degenerate (Skewed) Tree that acts as a linear linked list of height $H = N$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST OPERATIONS & DELETION MECHANICS                   |
+-----------------------------------------------------------------------+
| • Search/Insert: Compare target with root.val; go left or right       |
| • Insert Rule: New elements are ALWAYS inserted as LEAF nodes         |
| • Delete Case 1 (0 children): Return null                             |
| • Delete Case 2 (1 child)   : Return the single non-null child        |
| • Delete Case 3 (2 children): Replace val with findMin(root.right),   |
|                               then delete successor from root.right   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Search in a BST (LeetCode 700) iteratively in $O(1)$ space.
- [ ] I can write Insert into a BST (LeetCode 701).
- [ ] I can write Delete Node in a BST (LeetCode 450) handling all 3 cases.
- [ ] I know how to find the In-Order Successor (`findMin(root.right)`).
- [ ] I know why skewed BSTs degrade performance to $O(N)$ time.
