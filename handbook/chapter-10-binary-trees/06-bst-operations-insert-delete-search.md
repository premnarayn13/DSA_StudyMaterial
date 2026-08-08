# 06. BST Dynamic Mutation: Insertion, Deletion & Search Mechanics

## 1. Introduction
Dynamic mutation operations on a Binary Search Tree—**Search (LeetCode 700)**, **Insertion (LeetCode 701)**, and **Deletion (LeetCode 450)**—are fundamental operations in data structure design. In technical coding interviews, implementing BST deletion (known as **Hibbard Deletion**) is considered a classic test of pointer manipulation and recursive tree restructuring. Balanced BSTs execute search, insertion, and deletion in **$O(\log N)$ logarithmic time**, while un-balanced skewed BSTs degrade to $O(N)$ linear time.

> **Important:** Deleting a node with **TWO children** from a BST requires replacing the target node's value with either its **In-Order Successor** (minimum node in the right subtree) or its **In-Order Predecessor** (maximum node in the left subtree), and then recursively deleting that successor/predecessor node!

```
BST Mutation Operations Spectrum:
+-----------------------------------------------------------------------------------+
| Search Node    : Move Left if key < curr.val, Right if key > curr.val -> O(log N) |
| Insert Node    : Search for null insertion position, attach child     -> O(log N) |
| Delete Node    : 3 Cases (0 Children, 1 Child, 2 Children - Successor)-> O(log N) ⚡|
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Concepts & The 3 Cases of BST Deletion

### 2.1 Search Operation (`searchBST(key)`)
* Start at `root`.
* If `curr == null` or `curr.val == key`, return `curr`.
* If `key < curr.val`, recurse/move to `curr.left`.
* If `key > curr.val`, recurse/move to `curr.right`.

### 2.2 Insertion Operation (`insertIntoBST(val)`)
* Search for the location where `val` should exist.
* When reaching a `null` child pointer, instantiate `new TreeNode(val)` and return it to be linked to its parent.

### 2.3 Hibbard Deletion Operation (`deleteNode(key)`)
When deleting a target node $X$:

* **Case 1: Target Node is a Leaf Node (0 Children)**:
  - Simply disconnect/return `null` to the parent.
* **Case 2: Target Node has Exactly 1 Child**:
  - Bypass target node $X$ by returning its non-null child (`left != null ? left : right`) directly to $X$'s parent.
* **Case 3: Target Node has 2 Children (Complex Case)**:
  - Locate $X$'s **In-Order Successor** $S$ (the minimum node in $X$'s right subtree: `findMin(X.right)`).
  - Overwrite $X$'s value with $S$'s value: `X.val = S.val`.
  - Recursively delete the successor node $S$ from $X$'s right subtree: `X.right = deleteNode(X.right, S.val)`.

```
Hibbard Deletion (Case 3 - 2 Children):
Delete Node ( 5 ):
        ( 5 )                        ( 6 )  <- Replaced 5 with Successor (6)!
       /     \                      /     \
     ( 3 )   ( 7 )      ===>      ( 3 )   ( 7 )
            /     \                      /     \
          ( 6 )   ( 8 )                null   ( 8 ) <- Successor 6 deleted from Right Subtree!
```

> **Memory Trick:** **"Delete 2-Child Node: Swap value with In-Order Successor (Min of Right Subtree), then delete Successor!"**

---

## 3. Characteristics & In-Order Successor/Predecessor

### 3.1 In-Order Successor Definition
The **In-Order Successor** of a node $X$ is the node with the smallest key strictly greater than $X.\text{val}$.
* If $X$ has a **Right Subtree**: The successor is the **Left-Most (Minimum) Node in $X$'s Right Subtree**.
* If $X$ has NO Right Subtree: The successor is the **Lowest Ancestor whose Left Child is also an Ancestor of $X$**.

### 3.2 In-Order Predecessor Definition
The **In-Order Predecessor** of a node $X$ is the node with the largest key strictly smaller than $X.\text{val}$.
* If $X$ has a **Left Subtree**: The predecessor is the **Right-Most (Maximum) Node in $X$'s Left Subtree**.

```
In-Order Successor / Predecessor Search Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Target Reference      | Has Target Subtree| Search Path       | Key Invariant     |
+-----------------------+-------------------+-------------------+-------------------+
| In-Order Successor    | Has Right Subtree | Left-most node of Right Subtree | Minimum val > target |
| In-Order Predecessor  | Has Left Subtree  | Right-most node of Left Subtree | Maximum val < target |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 4. Internal Working Mechanics
Tracing Deletion of Node 5 (Case 3 - Two Children) in BST `[5, 3, 7, 2, 4, 6, 8]`:

```
Step 1: Search key 5 -> Found at Root Node 5.
Step 2: Check children: left != null (3) AND right != null (7) -> CASE 3!
Step 3: Find In-Order Successor S in Right Subtree (7):
        - Start at root.right (7). Move left: findMin(7) -> Node 6.
Step 4: Overwrite root.val with Successor val: root.val = 6.
Step 5: Delete Node 6 from Right Subtree:
        - Call root.right = deleteNode(7, 6).
        - Search 6 in subtree 7 -> Node 6 has 0 children (Case 1).
        - Disconnect Node 6 -> returns null to Node 7.left.

Resulting BST: [6, 3, 7, 2, 4, null, 8] ✅ (Valid BST in O(H) Time!)
```

---

## 5. Visual Diagram
Hibbard Deletion State Transitions for All 3 Cases:

```
[ CASE 1: DELETE LEAF NODE (0 Children) ]
  (3) ---> delete(4) ---> (3)
 /   \                   /
(2)  (4)               (2)

[ CASE 2: DELETE NODE WITH 1 CHILD ]
  (5) ---> delete(3) ---> (5)
 /                       /
(3)                    (2)
  \
  (2)

[ CASE 3: DELETE NODE WITH 2 CHILDREN ]
  (5)                     (6)  <- Replace 5 with In-Order Successor 6
 /   \                   /   \
(3)  (7)   ===>        (3)   (7)
    /   \                   /   \
  (6)   (8)               (null)(8) <- Delete duplicate Successor 6
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing BST Search (LeetCode 700), Insertion (LeetCode 701), Deletion (LeetCode 450), and In-Order Successor Search (LeetCode 285):

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
    }

    // 1. Search in a Binary Search Tree (LeetCode 700) O(H) Time, O(1) Space Iterative
    public static TreeNode searchBST(TreeNode root, int val) {
        TreeNode curr = root;
        while (curr != null) {
            if (curr.val == val) return curr;
            else if (val < curr.val) curr = curr.left;
            else curr = curr.right;
        }
        return null;
    }

    // 2. Insert into a Binary Search Tree (LeetCode 701) O(H) Time, O(H) Space Recursive
    public static TreeNode insertIntoBST(TreeNode root, int val) {
        if (root == null) {
            return new TreeNode(val); // Insert new node at null position
        }

        if (val < root.val) {
            root.left = insertIntoBST(root.left, val);
        } else if (val > root.val) {
            root.right = insertIntoBST(root.right, val);
        }

        return root;
    }

    // 3. Delete Node in a BST (LeetCode 450) O(H) Time, O(H) Space Recursive Hibbard Deletion
    public static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else { // Key matches root.val! Found target node to delete.

            // Case 1 & Case 2: Node has 0 or 1 child
            if (root.left == null)  return root.right;
            if (root.right == null) return root.left;

            // Case 3: Node has 2 children
            // Find In-Order Successor (Minimum node in Right Subtree)
            TreeNode minNode = findMin(root.right);

            // Copy Successor value to current node
            root.val = minNode.val;

            // Delete the duplicate Successor node from Right Subtree
            root.right = deleteNode(root.right, minNode.val);
        }

        return root;
    }

    private static TreeNode findMin(TreeNode node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }

    // 4. Inorder Successor in BST (LeetCode 285) O(H) Time, O(1) Space Iterative
    public static TreeNode inorderSuccessor(TreeNode root, TreeNode p) {
        TreeNode successor = null;
        TreeNode curr = root;

        while (curr != null) {
            if (p.val < curr.val) {
                successor = curr; // Potential successor!
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }

        return successor;
    }
}
```

> **Quick Syntax:**
```java
// Hibbard Deletion Case 3 Helper
TreeNode minNode = findMin(root.right);
root.val = minNode.val;
root.right = deleteNode(root.right, minNode.val);
```

---

## 7. Concrete Problem Examples
* **LeetCode 700 - Search in a Binary Search Tree**: Iterative BST search.
* **LeetCode 701 - Insert into a Binary Search Tree**: Recursive/Iterative BST node insertion.
* **LeetCode 450 - Delete Node in a BST**: Hibbard 3-Case deletion.
* **LeetCode 285 - Inorder Successor in BST**: $O(H)$ iterative successor search.

---

## 8. Java Code Demonstration & Dry Run
Demonstration executing search, insertion, and 3-case deletion on a BST:

```java
public class BSTOperationsDemo {

    public static void main(String[] args) {
        // Build BST: [5, 3, 6, 2, 4, null, 7]
        BSTOperationsMaster.TreeNode root = new BSTOperationsMaster.TreeNode(5);
        root.left = new BSTOperationsMaster.TreeNode(3);
        root.right = new BSTOperationsMaster.TreeNode(6);
        root.left.left = new BSTOperationsMaster.TreeNode(2);
        root.left.right = new BSTOperationsMaster.TreeNode(4);
        root.right.right = new BSTOperationsMaster.TreeNode(7);

        System.out.println("=== 1. Search in BST ===");
        BSTOperationsMaster.TreeNode found = BSTOperationsMaster.searchBST(root, 4);
        System.out.println("Search 4: Found Node Value = " + (found != null ? found.val : "null"));

        System.out.println("\n=== 2. Insert into BST (Val = 1) ===");
        root = BSTOperationsMaster.insertIntoBST(root, 1);
        System.out.println("Insert 1: Node 2 Left Child = " + root.left.left.left.val);

        System.out.println("\n=== 3. Delete Node in BST (Key = 5, Case 3 Two Children) ===");
        root = BSTOperationsMaster.deleteNode(root, 5);
        System.out.println("New Root Value after deleting 5: " + root.val + " (Expected Successor: 6)");
    }
}
```

---

## 9. Complexity Analysis

| BST Operation | Balanced Tree Time | Degenerate (Skewed) Tree Time | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Search (`searchBST`)** | **$O(\log N)$ ⚡** | $O(N)$ Linear | **$O(1)$ Iterative ⚡** |
| **Insert (`insertIntoBST`)** | **$O(\log N)$ ⚡** | $O(N)$ Linear | $O(H)$ Recursive Call Stack |
| **Delete (`deleteNode`)** | **$O(\log N)$ ⚡** | $O(N)$ Linear | $O(H)$ Recursive Call Stack |
| **In-Order Successor (285)** | **$O(\log N)$ ⚡** | $O(N)$ Linear | **$O(1)$ Iterative ⚡** |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Root Node**: When `root.val == key`, returning `deleteNode` result correctly updates the root reference.
* **Deleting Non-Existent Key**: Algorithm searches to `null` and returns unchanged tree.
* **Inserting Duplicate Values**: Standard implementations ignore duplicates or append to right subtree.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Re-assign Returned Child References in Recursion**:
  - Writing `deleteNode(root.left, key)` without assigning `root.left = deleteNode(root.left, key)`.
  - In Java, primitives and references are passed by value. Re-assigning `root.left` is MANDATORY to update parent-child pointer connections!
* **Searching Entire Tree for Minimum Node in Case 3**:
  - Scanning the ENTIRE tree for minimum node instead of searching strictly in `root.right` (`findMin(root.right)`).

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Pointer Re-assignment (`root.left = deleteNode(...)`) is Mandatory:
> In recursive tree mutation, returning the updated child node and assigning `root.left = deleteNode(root.left, key)` ensures that:
> 1. Unlinked children (Case 1 & 2) disconnect cleanly.
> 2. Parent-child pointer references remain intact without explicit parent pointers.

> **Memory Trick:** **"Always assign root.left = deleteNode(root.left, key) and root.right = deleteNode(root.right, key)!"**

---

## 13. System & Implementation Comparisons

| Feature | Hibbard Deletion (Successor) | Hibbard Deletion (Predecessor) |
| :--- | :--- | :--- |
| **Replacement Target** | Min Node of Right Subtree (`findMin(right)`) | Max Node of Left Subtree (`findMax(left)`) |
| **Subtree Search Path**| Go Right once, then Left until `null` | Go Left once, then Right until `null` |
| **Equivalence** | Equally Valid | Equally Valid |

---

## 14. How to Recognize This in Questions
* **"Delete a node from a BST while maintaining BST properties"** $\rightarrow$ LeetCode 450 (Hibbard Deletion).
* **"Find in-order successor of a node in a BST"** $\rightarrow$ LeetCode 285 ($O(H)$ iterative successor search).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Hibbard Deletion replace a 2-child node with its In-Order Successor?**  
  *A:* Because the In-Order Successor $S$ (minimum node of the right subtree) is strictly greater than all nodes in the left subtree and strictly smaller than all other nodes in the right subtree. Placing $S$ at the target node's position preserves the BST invariant perfectly.
* **Q: Why can the In-Order Successor node $S$ never have a left child?**  
  *A:* Because $S$ is defined as the left-most node in the right subtree (`while (node.left != null) node = node.left`). If $S$ had a left child, that left child would be smaller than $S$, contradicting $S$'s status as the minimum node!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BST MUTATION (INSERT, DELETE, SEARCH)                 |
+-----------------------------------------------------------------------+
| • Search: Move Left if key < val, Right if key > val (O(log N))       |
| • Insert: Search until null, create new TreeNode(val) at leaf position |
| • Delete Case 1 (0 Children): Return null to parent                   |
| • Delete Case 2 (1 Child): Return non-null child directly to parent   |
| • Delete Case 3 (2 Children): Replace root.val with min(root.right).val|
|   Then recursive call: root.right = deleteNode(root.right, minVal)    |
| • Pointer Rule: ALWAYS reassign root.left/right = deleteNode(...)     |
| • In-Order Successor: Min node of right subtree (has ZERO left child!)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write iterative BST search in $O(1)$ auxiliary space.
- [ ] I can write recursive BST insertion.
- [ ] I can implement Hibbard Deletion handling all 3 cases (LeetCode 450).
- [ ] I know why the In-Order Successor has no left child.
- [ ] I can write iterative In-Order Successor search (LeetCode 285).
- [ ] I know why `root.left = deleteNode(root.left, key)` re-assignment is mandatory.
