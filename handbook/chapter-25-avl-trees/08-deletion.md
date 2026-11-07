# 08. AVL Deletion Mechanics, 3-Case Relinking & $O(\log N)$ Rotation Propagation

## 1. Introduction
Deleting a key from an **AVL Tree** combines standard 3-case BST deletion with bottom-up height updates and 4-case rebalancing rotations. Unlike AVL insertion (which requires at most 1 rotation), deleting a node decreases subtree height, which can propagate height changes and balance factor violations all the way up the search path to the root node. Consequently, AVL deletion executes in **$O(\log N)$ Strict Worst-Case Time** and requires **Up to $O(\log N)$ Rotations**.

> **Important:** Why AVL Deletion May Require Up to $O(\log N)$ Rotations:
> When a rotation is performed to fix an imbalance caused by deletion:
> The rotation reduces the height of the rebalanced subtree by 1 level!
> Because the height of the subtree HAS DECREASED, the parent of that subtree may now become unbalanced!
> The height reduction can propagate up the tree, requiring up to $O(\log N)$ rotations along the path to the root! ⚡

```
AVL Deletion Rebalancing Propagation Topology:
Step 1: Standard 3-Case BST Deletion --------> Delete leaf, 1-child, or 2-child (Successor)
Step 2: Bottom-Up Path Traversal ------------> Traverse up towards Root Node
Step 3: Update Height & Evaluate BF ---------> BF = left.height - right.height
Step 4: Execute 4-Case Rebalancing ------------> Repeat rotations up to Root (Up to O(log N) rotations!) ⚡
```

---

## 2. Core Concepts & The 4-Case Deletion Rebalancing Engine

### 2.1 The Complete AVL Deletion Algorithm
To delete key `key` from an AVL tree rooted at `root`:
1. **Base Case**: If `root == null`, return `null`.
2. **BST Search & Deletion**:
   - If `key < root.val`: `root.left = deleteNode(root.left, key)`.
   - Else if `key > root.val`: `root.right = deleteNode(root.right, key)`.
   - Else: Target node matched! Handle 3 deletion cases:
     - Case 1 & 2 (0 or 1 Child): `TreeNode temp = (root.left != null) ? root.left : root.right;` If `temp == null`, `root = null`; else `root = temp`.
     - Case 3 (2 Children): `TreeNode temp = findMin(root.right); root.val = temp.val; root.right = deleteNode(root.right, temp.val);`.
3. If `root == null`, return `null`.
4. **Update Height**: `updateHeight(root)`.
5. **Evaluate Balance Factor**: `int balance = getBalanceFactor(root)`.
6. **Execute 4-Case Rebalancing Engine**:
   - **Case 1: LL Case**: `if (balance > 1 && getBalanceFactor(root.left) >= 0)` $\implies$ **`return rightRotate(root)`**!
   - **Case 2: LR Case**: `if (balance > 1 && getBalanceFactor(root.left) < 0)` $\implies$ **`root.left = leftRotate(root.left); return rightRotate(root)`**!
   - **Case 3: RR Case**: `if (balance < -1 && getBalanceFactor(root.right) <= 0)` $\implies$ **`return leftRotate(root)`**!
   - **Case 4: RL Case**: `if (balance < -1 && getBalanceFactor(root.right) > 0)` $\implies$ **`root.right = rightRotate(root.right); return leftRotate(root)`**!
7. Return `root`.

```
AVL 4-Case Deletion Rebalancing Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Imbalance Direction   | Root BF           | Child Subtree BF  | Rotation Action   |
+-----------------------+-------------------+-------------------+-------------------+
| **Left-Heavy**        | $\text{BF} > +1$  | `left.BF >= 0`    | **`rightRotate(root)` ⚡**|
| **Left-Heavy**        | $\text{BF} > +1$  | `left.BF < 0`     | **`rotateLR(root)` ⚡**   |
| **Right-Heavy**       | $\text{BF} < -1$  | `right.BF <= 0`   | **`leftRotate(root)` ⚡** |
| **Right-Heavy**       | $\text{BF} < -1$  | `right.BF > 0`    | **`rotateRL(root)` ⚡**   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"AVL Delete: Standard 3-case BST delete -> Check null -> Update height -> Execute rotations using child.BF!"**

---

## 3. Characteristics & Child Balance Factor Evaluation

### 3.1 Why Deletion Uses `child.BF >= 0` (Inclusive) Instead of `<` / `>`
In AVL Insertion, child balance factor is strictly non-zero (`val < node.left.val`).
In AVL Deletion, a child balance factor can equal **0** (e.g. `getBalanceFactor(root.left) == 0`).
* When `root.left.BF == 0`, a **Single Right Rotation (`rightRotate`)** is sufficient to restore balance!
* Therefore, deletion checks use inclusive comparisons: **`getBalanceFactor(root.left) >= 0`** for LL Case and **`<= 0`** for RR Case! ⚡

---

## 4. Internal Working Mechanics
Tracing AVL Deletion of key 10 from tree `[20, 10, 30, null, null, 25, 40]`:

```
Tree: Root 20 (left=10, right=30 [left=25, right=40]).

Delete Key 10 (Leaf Node):
1. Node 10 deleted -> 20.left becomes null.
2. Update height of 20: Height left = 0, Height right = 2. Height 20 = 3.
3. Balance Factor of 20: BF = 0 - 2 = -2 (UNBALANCED!).
4. Inspect Right Child 30: Height left (25) = 1, Height right (40) = 1. BF(30) = 0 (<= 0!).
5. Triggers RR Single Left Rotation on Root 20!

Call leftRotate(20):
- Promotes Node 30 to root! Node 20 becomes left child of 30.
- Node 25 becomes right child of 20.

New Tree = [30, 20, 40, null, 25] (Height = 3, Perfect Balance)! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
AVL Deletion Rebalancing Propagation Topography:

```
Deletion at Left Subtree (Node 10 Deleted):       Balanced State After Single Left Rotate:
            (20) -2                                           (30) 0
           /       \          RR Left Rotate                 /      \
        null       (30) 0     ---------------->           (20)      (40)
                  /    \                                     \
               (25)    (40)                                  (25)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of complete AVL Tree Deletion with 3-case removal and automatic 4-case rebalancing:

```java
import java.util.*;

public class AVLDeletionMaster {

    public static class AVLNode {
        public int val;
        public int height;
        public AVLNode left;
        public AVLNode right;

        public AVLNode(int val) {
            this.val = val;
            this.height = 1;
        }
    }

    public static int getHeight(AVLNode node) {
        return (node == null) ? 0 : node.height;
    }

    public static int getBalanceFactor(AVLNode node) {
        return (node == null) ? 0 : getHeight(node.left) - getHeight(node.right);
    }

    public static void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
        }
    }

    public static AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;
        x.right = y;
        y.left = T2;
        updateHeight(y);
        updateHeight(x);
        return x;
    }

    public static AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;
        y.left = x;
        x.right = T2;
        updateHeight(x);
        updateHeight(y);
        return y;
    }

    public static AVLNode findMin(AVLNode node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // Full AVL Deletion Algorithm O(log N) Time, O(H) Space
    public static AVLNode deleteNode(AVLNode root, int key) {
        // Step 1: Standard BST Deletion
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Target Key Matched! Handle 3 Deletion Cases:
            if (root.left == null || root.right == null) {
                AVLNode temp = (root.left != null) ? root.left : root.right;
                if (temp == null) {
                    root = null; // Case 1: 0 Children
                } else {
                    root = temp; // Case 2: 1 Child
                }
            } else {
                // Case 3: 2 Children -> In-Order Successor Substitution
                AVLNode temp = findMin(root.right);
                root.val = temp.val;
                root.right = deleteNode(root.right, temp.val);
            }
        }

        if (root == null) return null; // Tree became empty after deletion

        // Step 2: Update Height of ancestor
        updateHeight(root);

        // Step 3: Evaluate Balance Factor
        int balance = getBalanceFactor(root);

        // Step 4: Execute 1 of 4 Rotation Cases if unbalanced

        // Case 1: LL Case (left.BF >= 0)
        if (balance > 1 && getBalanceFactor(root.left) >= 0) {
            return rightRotate(root);
        }

        // Case 2: LR Case (left.BF < 0)
        if (balance > 1 && getBalanceFactor(root.left) < 0) {
            root.left = leftRotate(root.left);
            return rightRotate(root);
        }

        // Case 3: RR Case (right.BF <= 0)
        if (balance < -1 && getBalanceFactor(root.right) <= 0) {
            return leftRotate(root);
        }

        // Case 4: RL Case (right.BF > 0)
        if (balance < -1 && getBalanceFactor(root.right) > 0) {
            root.right = rightRotate(root.right);
            return leftRotate(root);
        }

        return root;
    }
}
```

> **Quick Syntax:**
```java
// AVL Deletion Rebalancing Check Lines
if (balance > 1 && getBalanceFactor(root.left) >= 0) return rightRotate(root);
if (balance < -1 && getBalanceFactor(root.right) <= 0) return leftRotate(root);
```

---

## 7. Concrete Problem Examples
* **AVL Symbol Table Deletion**: Removing items from high-speed in-memory indexes.
* **Dynamic Set Eviction**: Continuous addition and deletion of boundary items.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing AVL Deletion:

```java
public class AVLDeletionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. AVL Deletion & Rebalancing Test ===");
        AVLDeletionMaster.AVLNode root = new AVLDeletionMaster.AVLNode(20);
        root.left = new AVLDeletionMaster.AVLNode(10);
        root.right = new AVLDeletionMaster.AVLNode(30, 
            new AVLDeletionMaster.AVLNode(25), new AVLDeletionMaster.AVLNode(40));

        System.out.println("Root Value BEFORE Deletion: " + root.val); // Output: 20

        // Delete Leaf Node 10 (Triggers RR rotation at root 20!)
        root = AVLDeletionMaster.deleteNode(root, 10);

        System.out.println("\nRoot Value AFTER Deleting 10: " + root.val);       // Output: 30
        System.out.println("Root Height AFTER Deletion:    " + AVLDeletionMaster.getHeight(root)); // Output: 3
        System.out.println("Root Left Value:              " + root.left.val);  // Output: 20 ✅
    }
}
```

---

## 9. Complexity Analysis

| AVL Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Rebalance Rotations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AVL Deletion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | **Up to $O(\log N)$ Rotations** |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Root of Single-Node Tree**: `root` becomes `null`, returns `null` safely.
* **Deleting In-Order Successor**: Recursively handled by 2-child deletion block `deleteNode(root.right, temp.val)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Null Check After Case 1/2 Deletion**:
  - If a leaf node is deleted (`root` becomes `null`), attempting `updateHeight(root)` or `getBalanceFactor(root)` causes `NullPointerException`.
  - **ALWAYS check `if (root == null) return null;` before updating height**.
* **Using Strict `<` / `>` Instead of `>=` / `<=` for Child Balance Factors**:
  - In deletion, a child balance factor can equal 0. Using strict `<` skips single rotation when `child.BF == 0`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Deletion Can Trigger Up to $O(\log N)$ Rotations:
> Unlike insertion (where a rotation restores the subtree to its pre-insertion height), deletion-induced rotations REDUCE subtree height by 1 level.
> This height reduction can propagate up to higher ancestors, requiring rotations at multiple levels along the path to the root!

> **Memory Trick:** **"AVL Insert = At most 1 rotation; AVL Delete = Up to O(log N) rotations!"**

---

## 13. System & Implementation Comparisons

| Feature | AVL Tree Deletion | Red-Black Tree Deletion |
| :--- | :--- | :--- |
| **Rotation Bound** | **Up to $O(\log N)$ Rotations** | **At Most 3 Rotations ⚡** |
| **Lookup Speed After Delete**| **Faster Lookups ($H \le 1.44 \log_2 N$) ⚡**| Slightly Slower Lookups |
| **Delete Code Complexity** | Moderate (3 BST cases + 4 Rotations)| High (Complex double-black rules) |

---

## 14. How to Recognize This in Questions
* **"Delete element from self-balancing BST maintaining strict height balance H = O(log N)"** $\rightarrow$ AVL Deletion.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does deletion check `getBalanceFactor(root.left) >= 0` instead of `> 0`?**  
  *A:* Because when a child balance factor equals 0, executing a Single Right Rotation is completely valid and restores height balance.
* **Q: What is the maximum height of an AVL tree after $N$ deletions?**  
  *A:* Still strictly bounded by $H \le 1.44 \log_2 N$, guaranteeing logarithmic operational bounds.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: AVL TREE DELETION MECHANICS                           |
+-----------------------------------------------------------------------+
| • Step 1: Standard 3-Case BST Deletion (Leaf, 1-child, 2-child)       |
| • Step 2: Null Check: if (root == null) return null;                  |
| • Step 3: Update height & compute Balance Factor (BF)                 |
| • Step 4: Execute rotations using INCLUSIVE child BF checks (>= 0 / <= 0)|
| • Rotation Limit: Up to O(log N) rotations propagating to root! ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write full AVL Deletion in Java.
- [ ] I know why `if (root == null) return null;` is required after step 1.
- [ ] I know why child balance factor checks use `>= 0` and `<= 0`.
- [ ] I can explain why deletion can require up to $O(\log N)$ rotations.
- [ ] I can trace multi-node AVL deletions step by step.
