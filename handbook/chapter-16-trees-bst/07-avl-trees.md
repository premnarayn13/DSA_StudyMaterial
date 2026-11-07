# 07. AVL Trees, Strict Height Balancing & 4-Case Rotation Rebalancing Engines

## 1. Introduction
An **AVL Tree** (named after inventors **A**delson-**V**elsky and **L**andis) is the historically first self-balancing binary search tree. An AVL tree enforces a strict **Height-Balance Invariant**: for EVERY node in the tree, the height difference between its left and right subtrees is AT MOST 1 ($|\text{BF}| \le 1$). By performing single or double tree rotations during insertion and deletion, AVL trees guarantee a maximum height $H \le 1.44 \log_2 N$, providing **$O(\log N)$ Strict Worst-Case Time Complexity** for search, insertion, and deletion.

> **Important:** The 4 Rotation Cases in AVL Trees:
> 1. **LL Case (Left-Left)**: Insertion into left subtree of left child ($\text{BF} = +2$, child $\text{BF} \ge 0$) $\rightarrow$ **Single Right Rotation**!
> 2. **RR Case (Right-Right)**: Insertion into right subtree of right child ($\text{BF} = -2$, child $\text{BF} \le 0$) $\rightarrow$ **Single Left Rotation**!
> 3. **LR Case (Left-Right)**: Insertion into right subtree of left child ($\text{BF} = +2$, child $\text{BF} < 0$) $\rightarrow$ **Double Rotation: Left-Rotate Child, then Right-Rotate Node**!
> 4. **RL Case (Right-Left)**: Insertion into left subtree of right child ($\text{BF} = -2$, child $\text{BF} > 0$) $\rightarrow$ **Double Rotation: Right-Rotate Child, then Left-Rotate Node**! ⚡

```
AVL 4-Case Rotation Decision Topology:
+-----------------------+-------------------+-------------------+-------------------+
| Imbalance Case        | Node BF           | Child BF          | Rotation Required |
+-----------------------+-------------------+-------------------+-------------------+
| **LL (Left-Left)**    | $\text{BF} > +1$  | $\text{BF} \ge 0$ | **Single Right**  |
| **RR (Right-Right)**  | $\text{BF} < -1$  | $\text{BF} \le 0$ | **Single Left**   |
| **LR (Left-Right)**   | $\text{BF} > +1$  | $\text{BF} < 0$   | **Left-Right**    |
| **RL (Right-Left)**   | $\text{BF} < -1$  | $\text{BF} > 0$   | **Right-Left**    |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 2. Core Concepts & AVL Node Height Maintenance

### 2.1 The Height Equation
Unlike standard BST nodes, an `AVLNode` maintains an explicit `height` field:

$$\text{height}(X) = 1 + \max(\text{height}(X.\text{left}), \text{height}(X.\text{right}))$$

$$\text{Balance Factor } \text{BF}(X) = \text{height}(X.\text{left}) - \text{height}(X.\text{right})$$

* A `null` node has height **0**.
* A leaf node has height **1**.

```
Height Update Rule:
After every rotation or recursive child insertion/deletion:
node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
```

> **Memory Trick:** **"LL = Single Right! RR = Single Left! LR = Left-Right! RL = Right-Left!"**

---

## 3. Characteristics & Double Rotation Mechanics (LR and RL Cases)

### 3.1 Why Double Rotations Are Required for Zigzag Imbalances
* **LR Case (Left-Right)**: Node $Z$ has $\text{BF} = +2$, but its left child $Y$ has $\text{BF} = -1$ (right-heavy).
  - A single right rotation on $Z$ FAILS to balance the tree because the right-heavy subtree of $Y$ remains out of position!
  - **Solution**: First perform a **Left Rotation on Child $Y$** to convert the LR case into a straight LL case! Then perform a **Right Rotation on Node $Z$**!

```
LR Double Rotation Step-by-Step Topology:
      (Z) +2                (Z) +2                 (X) 0
     /                     /                      /   \
   (Y) -1    Left-Rot(Y) (X)      Right-Rot(Z)  (Y)   (Z)
     \       --------->  /        ----------->
     (X)               (Y)

LR Case resolved to 100% Height-Balanced State (BF = 0)! ⚡
```

---

## 4. Internal Working Mechanics
Tracing Insertion of key 3 into AVL Tree `[5, 4]` (LL Imbalance Case):

```
Initial Tree: Node 5 (left=4). Insert 3 into left subtree of 4.

Tree shape: 5 -> 4 -> 3 (Right-skewed line to the left).

1. Compute Heights and Balance Factors:
   - Node 3: Height 1, BF = 0.
   - Node 4: Height 2, BF = 1 - 0 = +1.
   - Node 5: Height 3, BF = 2 - 0 = +2! (UNBALANCED!).

2. Identify Case:
   - Node 5 has BF = +2.
   - Left Child 4 has BF = +1 (>= 0).
   - Case is LL (Left-Left)!

3. Execute Single Right Rotation on Node 5:
   - Promotes Node 4 to root!
   - Node 4.right becomes 5.
   - Update heights: Node 5 Height 1, Node 3 Height 1, Node 4 Height 2.

New Tree = [4, 3, 5] (Perfect Balance, Height 2)! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
AVL Double Rotation (RL Case) Topography:

```
    (Z) -2               (Z) -2                (X) 0
      \                    \                  /   \
      (Y) +1  Right-Rot(Y) (X)   Left-Rot(Z) (Z)   (Y)
      /       ----------->   \   ---------->
    (X)                      (Y)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a complete self-balancing AVL Tree supporting Insertion, Deletion, and 4-Case Rotations:

```java
import java.util.*;

public class AVLTreesMaster {

    public static class AVLNode {
        public int val;
        public int height;
        public AVLNode left;
        public AVLNode right;

        public AVLNode(int val) {
            this.val = val;
            this.height = 1; // New leaf node height is 1
        }
    }

    // Helper: Get node height safely
    public static int getHeight(AVLNode node) {
        return (node == null) ? 0 : node.height;
    }

    // Helper: Get balance factor
    public static int getBalance(AVLNode node) {
        return (node == null) ? 0 : getHeight(node.left) - getHeight(node.right);
    }

    // Helper: Update height from children
    private static void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
        }
    }

    // 1. Right Rotation (Solves LL Case) O(1) Time
    public static AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;

        // Perform rotation
        x.right = y;
        y.left = T2;

        // Update heights
        updateHeight(y);
        updateHeight(x);

        return x; // New root
    }

    // 2. Left Rotation (Solves RR Case) O(1) Time
    public static AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;

        // Perform rotation
        y.left = x;
        x.right = T2;

        // Update heights
        updateHeight(x);
        updateHeight(y);

        return y; // New root
    }

    // 3. AVL Insert with Automatic 4-Case Rebalancing O(log N) Time
    public static AVLNode insert(AVLNode node, int val) {
        if (node == null) return new AVLNode(val);

        if (val < node.val) {
            node.left = insert(node.left, val);
        } else if (val > node.val) {
            node.right = insert(node.right, val);
        } else {
            return node; // Duplicate keys not allowed in standard AVL
        }

        // Update height of ancestor node
        updateHeight(node);

        // Check Balance Factor
        int balance = getBalance(node);

        // Case 1: LL (Left-Left) -> Single Right Rotate
        if (balance > 1 && getBalance(node.left) >= 0) {
            return rightRotate(node);
        }

        // Case 2: RR (Right-Right) -> Single Left Rotate
        if (balance < -1 && getBalance(node.right) <= 0) {
            return leftRotate(node);
        }

        // Case 3: LR (Left-Right) -> Double Rotate (Left then Right)
        if (balance > 1 && getBalance(node.left) < 0) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        // Case 4: RL (Right-Left) -> Double Rotate (Right then Left)
        if (balance < -1 && getBalance(node.right) > 0) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        return node;
    }

    // 4. AVL Delete with Automatic 4-Case Rebalancing O(log N) Time
    public static AVLNode deleteNode(AVLNode root, int key) {
        if (root == null) return null;

        if (key < root.val) {
            root.left = deleteNode(root.left, key);
        } else if (key > root.val) {
            root.right = deleteNode(root.right, key);
        } else {
            // Node found! Handle 3 deletion cases:
            if (root.left == null || root.right == null) {
                AVLNode temp = (root.left != null) ? root.left : root.right;
                if (temp == null) {
                    root = null; // 0 children
                } else {
                    root = temp; // 1 child
                }
            } else {
                // 2 Children: Get In-Order Successor (Min in Right Subtree)
                AVLNode temp = findMin(root.right);
                root.val = temp.val;
                root.right = deleteNode(root.right, temp.val);
            }
        }

        if (root == null) return null;

        // Update height and rebalance ancestor node
        updateHeight(root);
        int balance = getBalance(root);

        // LL Case
        if (balance > 1 && getBalance(root.left) >= 0) return rightRotate(root);
        // LR Case
        if (balance > 1 && getBalance(root.left) < 0) {
            root.left = leftRotate(root.left);
            return rightRotate(root);
        }
        // RR Case
        if (balance < -1 && getBalance(root.right) <= 0) return leftRotate(root);
        // RL Case
        if (balance < -1 && getBalance(root.right) > 0) {
            root.right = rightRotate(root.right);
            return leftRotate(root);
        }

        return root;
    }

    private static AVLNode findMin(AVLNode node) {
        while (node.left != null) node = node.left;
        return node;
    }
}
```

> **Quick Syntax:**
```java
// LR Double Rotation Code Line
if (balance > 1 && getBalance(node.left) < 0) {
    node.left = leftRotate(node.left);
    return rightRotate(node);
}
```

---

## 7. Concrete Problem Examples
* **High-Frequency Read-Heavy Search Engines**: AVL Trees ($H \le 1.44 \log_2 N$ guarantees fastest lookup times).
* **Database In-Memory Indexing**: Balanced BST range searches.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing AVL Tree insertion and automatic 4-case rebalancing:

```java
public class AVLTreesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. AVL Tree Auto-Rebalancing Test ===");
        AVLTreesMaster.AVLNode root = null;

        // Insert elements that trigger rotations: 10, 20, 30 (RR Case)
        root = AVLTreesMaster.insert(root, 10);
        root = AVLTreesMaster.insert(root, 20);
        root = AVLTreesMaster.insert(root, 30); // Triggers Left-Rotate on 10!

        System.out.println("Root after 10, 20, 30: " + root.val); // Output: 20 (Balanced!)

        // Insert 40, 50 (RR Case again)
        root = AVLTreesMaster.insert(root, 40);
        root = AVLTreesMaster.insert(root, 50);

        // Insert 25 (Triggers RL Double Rotation!)
        root = AVLTreesMaster.insert(root, 25);

        System.out.println("Root after 40, 50, 25: " + root.val); // Output: 30
        System.out.println("Root Height: " + AVLTreesMaster.getHeight(root)); // Height 3 (Strictly Balanced!) ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Action | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Search** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space |
| **Insert** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space |
| **Delete** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Deleting Root Node in AVL**: Successfully rebalances the new root along the deletion search path up to $O(\log N)$ height.
* **Inserting Duplicates**: Ignored or tracked via node frequency counter.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting Single Rotation on LR or RL Imbalance**:
  - Applying single right-rotate on LR case fails to restore balance because the right-heavy child remains out of position.
  - **Always perform double rotation (left-rotate child, then right-rotate node)**.
* **Forgetting to Update Node Heights After Rotation**:
  - Rotations change child-parent relationships. Failing to call `updateHeight()` leaves stale heights, corrupting future balance factor queries.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** AVL Tree vs Red-Black Tree Architectural Decision:
> * **AVL Trees** are strictly balanced ($H \le 1.44 \log_2 N$). They provide **Faster Search Lookups** because tree height is strictly minimal.
> * **Red-Black Trees** are loosely balanced ($H \le 2.0 \log_2 N$). They provide **Faster Insertions/Deletions** because write operations require fewer rebalancing rotations.
> * **Rule of Thumb**: Use **AVL Trees** for Read-Heavy workloads; use **Red-Black Trees** for Write-Heavy / Frequent Mutation workloads!

> **Memory Trick:** **"AVL Trees = Faster Search (Strict Balance)! Red-Black Trees = Faster Writes (Fewer Rotations)!"**

---

## 13. System & Implementation Comparisons

| Feature | AVL Tree | Red-Black Tree |
| :--- | :--- | :--- |
| **Maximum Height Bound**| **$H \le 1.44 \log_2 N$ (Tighter) ⚡**| $H \le 2.0 \log_2 N$ (Looser) |
| **Lookup Speed** | **Faster Lookups ⚡** | Slightly Slower Lookups |
| **Rebalance Rotations** | Up to $O(\log N)$ per delete | **At most 2-3 Rotations per write ⚡**|

---

## 14. How to Recognize This in Questions
* **"Maintain strict height balance |BF| <= 1 for optimal search performance"** $\rightarrow$ AVL Tree.
* **"Execute double rotations for zigzag tree imbalances"** $\rightarrow$ LR and RL Cases in AVL Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does an AVL Tree guarantee $H \le 1.44 \log_2 N$?**  
  *A:* The minimum number of nodes $N(H)$ in an AVL tree of height $H$ follows a Fibonacci recurrence: $N(H) = N(H-1) + N(H-2) + 1$. Solving this recurrence relation yields $H \approx 1.44 \log_2 N$, proving strict logarithmic height.
* **Q: How many rotations are required during AVL insertion vs deletion?**  
  *A:* Insertion requires AT MOST 1 single or double rotation to restore global balance. Deletion may require up to $O(\log N)$ rotations propagating up to the root.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: AVL TREES & 4-CASE REBALANCING                        |
+-----------------------------------------------------------------------+
| • Invariant: Balance Factor |BF| <= 1 for EVERY node                  |
| • Height Formula: height = 1 + max(height(left), height(right))       |
| • LL Case (BF > 1, childBF >= 0) : Single Right Rotation              |
| • RR Case (BF < -1, childBF <= 0): Single Left Rotation               |
| • LR Case (BF > 1, childBF < 0)  : Left-Rotate Child -> Right-Rotate  |
| • RL Case (BF < -1, childBF > 0) : Right-Rotate Child -> Left-Rotate  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write an AVL Tree with insert, delete, and 4-case rotations.
- [ ] I can state the rotation required for each of the 4 imbalance cases.
- [ ] I know why LR and RL cases require double rotations.
- [ ] I know why AVL Trees provide faster lookups than Red-Black Trees.
- [ ] I know the difference between AVL insertion and deletion rotation propagation.
