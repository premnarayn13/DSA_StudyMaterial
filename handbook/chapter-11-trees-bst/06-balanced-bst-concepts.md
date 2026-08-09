# 06. Balanced BST Concepts, Balance Factor Invariants & Degeneracy Prevention

## 1. Introduction
The efficiency of all operations on a Binary Search Tree (BST) depends directly on its **Tree Height ($H$)**. When keys are inserted in sorted order into a naive BST, the tree degenerates into a linear **Skewed Linked List** of height $H = N$, causing search, insertion, and deletion times to degrade from $O(\log N)$ logarithmic time down to **$O(N)$ Worst-Case Linear Time**. **Self-Balancing Binary Search Trees** (such as AVL Trees and Red-Black Trees) maintain a strict **Height-Balance Invariant** via tree rotations, guaranteeing **$O(\log N)$ Strict Worst-Case Operations**.

> **Important:** Why does a Self-Balancing BST enforce $H = O(\log_2 N)$?
> By maintaining balance invariants (e.g. Balance Factor $|H_{\text{left}} - H_{\text{right}}| \le 1$ in AVL Trees), every level doubling doubles the node capacity $N = 2^H - 1$.
> Taking the base-2 logarithm proves $H \approx \log_2 N$, guaranteeing that search paths NEVER exceed logarithmic length! ⚡

```
Skewed vs Balanced BST Topology (N = 7 Nodes):
Skewed BST (Height H = 7, O(N) Search)   Balanced BST (Height H = 3, O(log N) Search)
        (1)                                             (4)
         \                                            /     \
         (2)                                        (2)     (6)
          \                                        /   \   /   \
          (3)...                                 (1)  (3) (5)  (7)
```

---

## 2. Core Concepts & The Balance Factor Metric

### 2.1 Balance Factor Definition ($\text{BF}$)
For any node $X$ in a Binary Search Tree, the **Balance Factor ($\text{BF}(X)$)** is the difference between the height of its left subtree and right subtree:

$$\text{BF}(X) = \text{Height}(\text{left}(X)) - \text{Height}(\text{right}(X))$$

#### Balance Factor Classifications:
* **$\text{BF}(X) = 0$**: Left and Right subtrees have identical heights (Perfect local balance).
* **$\text{BF}(X) = +1$**: Left subtree is 1 level taller than Right subtree (Left-Heavy).
* **$\text{BF}(X) = -1$**: Right subtree is 1 level taller than Left subtree (Right-Heavy).
* **$|\text{BF}(X)| \ge 2$**: Node $X$ is **UNBALANCED**! Requires immediate structural re-balancing (Rotations)!

```
Balanced BST Family Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Self-Balancing Tree   | Balance Invariant | Height Bound      | Primary Use Case  |
+-----------------------+-------------------+-------------------+-------------------+
| **AVL Tree**          | $|\text{BF}| \le 1$| $H \le 1.44 \log_2 N$| Read-Heavy Search |
| **Red-Black Tree**    | Red/Black Rules   | $H \le 2 \log_2 N$| Write-Heavy Maps  |
| **Treap**             | Random Heap Priority| $H = O(\log N)$ Avg| Randomized Search|
| **B-Tree / B+ Tree**  | Multi-way M-ary   | Low Height $H$    | Disk & DB Indexing|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Balance Factor BF = Height(Left) - Height(Right)! If |BF| >= 2, the node is unbalanced!"**

---

## 3. Characteristics & The Need for Tree Rotations

### 3.1 Why Tree Rotations Restore Balance Without Violating BST Properties
When an insertion or deletion causes $|\text{BF}(X)| \ge 2$, tree balance is restored using **Tree Rotations**:
* **Rotations** rearrange pointers between a parent, child, and subtrees.
* **BST Invariant Preservation**: Rotations change tree height while **STRICTLY PRESERVING IN-ORDER SORTED KEY ORDER**!

```
Left and Right Rotation Equations:
Right Rotation on Node Y:        Left Rotation on Node X:
        (Y)                            (X)
       /   \                          /   \
     (X)   [T3]    Right-Rotate     [T1]   (Y)
    /   \        -------------->          /   \
  [T1]  [T2]     <--------------        [T2]  [T3]
                   Left-Rotate

In-Order Key Sequence BEFORE & AFTER Rotation: T1 < X < T2 < Y < T3 (IDENTICAL!) ⚡
```

---

## 4. Internal Working Mechanics
Tracing Balance Factor Calculation and Degeneracy Detection:

```
Insert sequence [1, 2, 3] into naive BST:

Insert 1: Node 1 (Height 1, BF = 0)
Insert 2: Node 1 -> Right 2 (Node 1 Height 2, BF = -1)
Insert 3: Node 1 -> Right 2 -> Right 3 (Node 1 Height 3, BF = -2!)

Node 1 has BF = -2! Node 1 is UNBALANCED!
Applying a Single Left-Rotate on Node 1 converts [1, 2, 3] into Balanced Tree with Root 2! ✅
```

---

## 5. Visual Diagram
Tree Rotation Pointer Manipulation Topography:

```
     Unbalanced Node Y (BF = +2)                   Balanced Node X (BF = 0)
            (Y)                                           (X)
           /   \         Right Rotation                  /   \
         (X)   [T3]    ----------------->             [T1]   (Y)
        /   \                                               /   \
      [T1]  [T2]                                          [T2]  [T3]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite demonstrating Balance Factor computation, Degeneracy Detection, and Height-Balanced Tree Verification:

```java
import java.util.*;

public class BalancedBSTConceptsMaster {

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

    // 1. Calculate Balance Factor of a Node O(H) Time
    public static int getBalanceFactor(TreeNode node) {
        if (node == null) return 0;
        return getHeight(node.left) - getHeight(node.right);
    }

    // 2. Get Height of a Node O(H) Time
    public static int getHeight(TreeNode node) {
        if (node == null) return 0;
        return 1 + Math.max(getHeight(node.left), getHeight(node.right));
    }

    // 3. Verify Full Tree Balance (LeetCode 110) O(N) Time, O(H) Space
    public static boolean isTreeBalanced(TreeNode root) {
        return checkBalance(root) != -1;
    }

    private static int checkBalance(TreeNode node) {
        if (node == null) return 0;

        int leftH = checkBalance(node.left);
        if (leftH == -1) return -1;

        int rightH = checkBalance(node.right);
        if (rightH == -1) return -1;

        // Check Balance Factor Invariant |leftH - rightH| <= 1
        if (Math.abs(leftH - rightH) > 1) {
            return -1; // Unbalanced subtree found!
        }

        return 1 + Math.max(leftH, rightH);
    }

    // 4. Basic Left Rotation Implementation O(1) Time, O(1) Space
    public static TreeNode leftRotate(TreeNode x) {
        TreeNode y = x.right;
        TreeNode T2 = y.left;

        // Perform Rotation
        y.left = x;
        x.right = T2;

        return y; // New root of subtree
    }

    // 5. Basic Right Rotation Implementation O(1) Time, O(1) Space
    public static TreeNode rightRotate(TreeNode y) {
        TreeNode x = y.left;
        TreeNode T2 = x.right;

        // Perform Rotation
        x.right = y;
        y.left = T2;

        return x; // New root of subtree
    }
}
```

> **Quick Syntax:**
```java
// Balance Factor Formula
int bf = getHeight(node.left) - getHeight(node.right);
```

---

## 7. Concrete Problem Examples
* **LeetCode 110 - Balanced Binary Tree**: Height-balance property verification.
* **LeetCode 108 - Convert Sorted Array to Binary Search Tree**: Divide-and-conquer balanced BST construction.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Balance Factor computation and Rotations:

```java
public class BalancedBSTConceptsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Balance Factor & Rotation Test ===");
        // Build Right-Skewed Unbalanced Tree: 1 -> 2 -> 3
        BalancedBSTConceptsMaster.TreeNode root = new BalancedBSTConceptsMaster.TreeNode(1);
        root.right = new BalancedBSTConceptsMaster.TreeNode(2);
        root.right.right = new BalancedBSTConceptsMaster.TreeNode(3);

        System.out.println("Root 1 Balance Factor: " + 
            BalancedBSTConceptsMaster.getBalanceFactor(root)); // Output: -2 (Unbalanced!)
        System.out.println("Is Tree Balanced? " + 
            BalancedBSTConceptsMaster.isTreeBalanced(root)); // Output: false

        System.out.println("\nExecuting Left Rotation on Root 1...");
        root = BalancedBSTConceptsMaster.leftRotate(root); // New root is 2

        System.out.println("New Root Value: " + root.val); // Output: 2
        System.out.println("New Root Balance Factor: " + 
            BalancedBSTConceptsMaster.getBalanceFactor(root)); // Output: 0 (Balanced!)
        System.out.println("Is Tree Balanced Now? " + 
            BalancedBSTConceptsMaster.isTreeBalanced(root)); // Output: true ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Concept | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Balance Factor Computation**| **$O(H)$ Linear ⚡** | $O(H)$ Stack Space | Height difference calculation |
| **Left / Right Rotation** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | Pointer re-assignment |
| **Full Tree Balance Check** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Bottom-up early exit `-1` |

---

## 10. Edge Cases & Boundary Handling
* **Null Subtrees (`node.left == null`)**: Subtree height is 0.
* **Single Node Subtree**: Balance factor is 0.

---

## 11. Common Mistakes & Anti-Patterns
* **Assuming Balance Means Left and Right Subtrees Have Equal Node Counts**:
  - Balance factor is defined by SUBTREE HEIGHT ($H_{\text{left}} - H_{\text{right}}$), NOT total node counts!
* **Executing Rotations Without Updating Parent Links**:
  - Rotations return a new subtree root. Always update the parent pointer: `parent.left = rotate(child)`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Tree Rotations Preserve BST Sorted Order:
> For any node $X$ and $Y$ involved in a rotation, the relative In-Order sequence `T1 < X < T2 < Y < T3` remains unchanged!
> Because In-Order key order is strictly preserved, tree rotations can be applied freely to adjust tree height without breaking BST search validity!

> **Memory Trick:** **"Tree rotations change tree height while preserving in-order sorted key order 100%!"**

---

## 13. System & Implementation Comparisons

| Feature | Unbalanced Naive BST | Self-Balancing BST (AVL / Red-Black) |
| :--- | :--- | :--- |
| **Worst-Case Search Time**| $O(N)$ Linear (Skewed) | **$O(\log N)$ Guaranteed Logarithmic ⚡** |
| **Tree Height $H$** | $1 \le H \le N$ | **$H = O(\log_2 N)$ ⚡** |
| **Rotation Overhead** | None | Low ($O(1)$ per insert/delete) |

---

## 14. How to Recognize This in Questions
* **"Explain why naive BST operations can degrade to O(N) time"** $\rightarrow$ Sorted insertion creates skewed tree of height $N$.
* **"Restore O(log N) worst-case bounds without violating BST order"** $\rightarrow$ Tree Rotations (Balance Factor $|\text{BF}| \le 1$).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the difference between AVL Tree and Red-Black Tree balance invariants?**  
  *A:* AVL Trees enforce strict height balance ($|\text{BF}| \le 1$), providing faster lookups but requiring more frequent rotations on insertion/deletion. Red-Black Trees enforce color properties allowing height difference up to $2 \log N$, requiring fewer rotations on write operations.
* **Q: Why does a Left Rotation on node $X$ make $X$'s right child $Y$ the new root?**  
  *A:* In a left-heavy right subtree, $Y = X.\text{right}$ is larger than $X$. Promoting $Y$ to the root and attaching $X$ as $Y$'s left child reduces the height of the right subtree while maintaining $X < Y$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BALANCED BST CONCEPTS & ROTATIONS                     |
+-----------------------------------------------------------------------+
| • Balance Factor Formula: BF = Height(Left) - Height(Right)           |
| • Unbalanced Condition: |BF| >= 2 requires immediate rotation!        |
| • Rotation Invariant: Rotations adjust height while preserving order  |
| • Left Rotation: Promotes right child Y to root; X becomes left child |
| • Right Rotation: Promotes left child X to root; Y becomes right child|
| • Height Bound: Balanced BST guarantees H = O(log N) -> O(log N) Ops ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can calculate the Balance Factor of any node.
- [ ] I can write `leftRotate` and `rightRotate` from memory.
- [ ] I can explain why tree rotations preserve BST sorted key order.
- [ ] I know why naive BST operations degrade to $O(N)$ time.
- [ ] I know the difference between AVL and Red-Black tree balance rules.
