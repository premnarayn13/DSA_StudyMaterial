# 07. AVL Insertion Mechanics, Bottom-Up Rebalancing & At-Most-One Rotation Invariant

## 1. Introduction
Inserting a key into an **AVL Tree** combines standard BST leaf insertion with bottom-up height updates and automatic 4-case rebalancing rotations. While standard BST insertion can cause tree height to degrade to $O(N)$, AVL insertion guarantees that after a new leaf is attached, propagating balance factor checks up the call stack identifies any imbalance and restores the strict height-balance invariant ($|\text{BF}| \le 1$) in **$O(\log N)$ Time and $O(H)$ Auxiliary Space**.

> **Important:** The At-Most-One Rotation Invariant for AVL Insertion:
> **An AVL Tree insertion requires AT MOST ONE single or double rotation to restore global height balance across the ENTIRE tree!**
> Once a single or double rotation is performed on the deepest unbalanced ancestor, the height of that subtree is restored to its exact pre-insertion height, preventing any further imbalance propagation above it! ⚡

```
AVL Insertion Step-by-Step Pipeline Topology:
Step 1: Standard BST Leaf Insertion --------> Attaches new node as LEAF at depth H
Step 2: Update Node Heights Bottom-Up ------> node.height = 1 + max(left.height, right.height)
Step 3: Evaluate Balance Factor -----------> BF = left.height - right.height
Step 4: Execute 1 of 4 Rotation Cases -------> LL, RR, LR, or RL Case (At most 1 rotation!) ⚡
```

---

## 2. Core Concepts & The 4-Case Rebalancing Decision Engine

### 2.1 The Complete AVL Insertion Algorithm
To insert key `val` into an AVL tree rooted at `node`:
1. **Base Case**: If `node == null`, return `new AVLNode(val)`.
2. **BST Search & Attachment**:
   - If `val < node.val`: `node.left = insert(node.left, val)`.
   - Else if `val > node.val`: `node.right = insert(node.right, val)`.
   - Else: Return `node` (Duplicate keys not allowed in standard AVL).
3. **Update Height**: `updateHeight(node)`.
4. **Evaluate Balance Factor**: `int balance = getBalanceFactor(node)`.
5. **Execute 4-Case Rebalancing Engine**:
   - **Case 1: LL (Left-Left)**: `if (balance > 1 && val < node.left.val)` $\implies$ **`return rightRotate(node)`**!
   - **Case 2: RR (Right-Right)**: `if (balance < -1 && val > node.right.val)` $\implies$ **`return leftRotate(node)`**!
   - **Case 3: LR (Left-Right)**: `if (balance > 1 && val > node.left.val)` $\implies$ **`node.left = leftRotate(node.left); return rightRotate(node)`**!
   - **Case 4: RL (Right-Left)**: `if (balance < -1 && val < node.right.val)` $\implies$ **`node.right = rightRotate(node.right); return leftRotate(node)`**!
6. Return `node`.

```
AVL 4-Case Insertion Rebalancing Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Insertion Subtree     | Node BF           | Value Comparison  | Rotation Action   |
+-----------------------+-------------------+-------------------+-------------------+
| **Left of Left Child**| $\text{BF} > +1$  | `val < left.val`  | **`rightRotate(node)` ⚡**|
| **Right of Right**    | $\text{BF} < -1$  | `val > right.val` | **`leftRotate(node)` ⚡** |
| **Right of Left Child**| $\text{BF} > +1$ | `val > left.val`  | **`rotateLR(node)` ⚡**   |
| **Left of Right Child**| $\text{BF} < -1$ | `val < right.val` | **`rotateRL(node)` ⚡**   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"AVL Insert: Standard BST insert -> Update Height -> Check BF -> Execute 1 of 4 Rotations!"**

---

## 3. Characteristics & The At-Most-One Rotation Theorem

### 3.1 Mathematical Proof of At-Most-One Rotation Limit
Let $Z$ be the deepest ancestor node that becomes unbalanced ($\text{BF}(Z) = +2$ or $-2$) following an insertion:
* Before insertion: Subtree $Z$ had height $H$.
* Insertion increases height of one branch, making subtree $Z$ height $H + 1$ and triggering imbalance.
* Applying the appropriate single or double rotation on $Z$ promotes a node that reduces the subtree height back to **$H$** (its exact pre-insertion height!).
* Because subtree $Z$'s height is restored to $H$, $Z$'s parent sees ZERO height change!
* Therefore, no higher ancestors experience imbalance $\implies \mathbf{\text{At Most 1 Rotation Per Insertion!}}$ ⚡

---

## 4. Internal Working Mechanics
Tracing AVL Insertion of keys `[10, 20, 30, 40, 50, 25]` step-by-step:

```
Insert 10, 20, 30:
- 10 -> 20 -> 30 triggers RR Case at 10 (BF = -2, 30 > 20).
- leftRotate(10) -> Root becomes 20 (left=10, right=30). (1 Rotation!).

Insert 40, 50:
- 30 -> 40 -> 50 triggers RR Case at 30 (BF = -2).
- leftRotate(30) -> Subtree 30 becomes 40 (left=30, right=50). (1 Rotation!).

Insert 25:
- Path: 20 -> 40 -> 30 -> 25.
- Node 40 has left=30 (left=25). Node 40 BF = 2 - 1 = +1 (Balanced).
- Node 20 has left=10 (h=1), right=40 (h=3). Node 20 BF = 1 - 3 = -2!
- Right Child 40 has BF = +1 (Left-heavy!).
- Triggers RL Double Rotation at Root 20!
- Step 1: rightRotate(40) -> 40 becomes 30 (right=40).
- Step 2: leftRotate(20) -> Root becomes 30 (left=20, right=40).

All 6 keys inserted into perfectly balanced AVL tree in O(N log N) total time! ✅
```

---

## 5. Visual Diagram
AVL Insertion Pipeline Topography:

```
Unbalanced State After Insertion:                  Balanced State After Rotation:
             (20) -2                                           (30) 0
            /       \         RL Double Rotation              /      \
         (10)       (40) +1   ----------------->           (20)      (40)
                    /                                      /   \        \
                 (30)                                   (10)   (25)     (50)
                 /
              (25)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of complete AVL Tree Insertion with automatic 4-case rebalancing:

```java
import java.util.*;

public class AVLInsertionMaster {

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

    // Full AVL Insertion Algorithm O(log N) Time, O(H) Space
    public static AVLNode insert(AVLNode node, int val) {
        // Step 1: Standard BST Insertion
        if (node == null) return new AVLNode(val);

        if (val < node.val) {
            node.left = insert(node.left, val);
        } else if (val > node.val) {
            node.right = insert(node.right, val);
        } else {
            return node; // Duplicate keys ignored
        }

        // Step 2: Update height of ancestor node
        updateHeight(node);

        // Step 3: Evaluate Balance Factor
        int balance = getBalanceFactor(node);

        // Step 4: Execute 1 of 4 Rotation Cases if unbalanced

        // Case 1: LL (Left-Left) -> Single Right Rotate
        if (balance > 1 && val < node.left.val) {
            return rightRotate(node);
        }

        // Case 2: RR (Right-Right) -> Single Left Rotate
        if (balance < -1 && val > node.right.val) {
            return leftRotate(node);
        }

        // Case 3: LR (Left-Right) -> Double Rotate (Left then Right)
        if (balance > 1 && val > node.left.val) {
            node.left = leftRotate(node.left);
            return rightRotate(node);
        }

        // Case 4: RL (Right-Left) -> Double Rotate (Right then Left)
        if (balance < -1 && val < node.right.val) {
            node.right = rightRotate(node.right);
            return leftRotate(node);
        }

        return node; // Return unmodified or rebalanced node pointer
    }
}
```

> **Quick Syntax:**
```java
// AVL Insertion Complete Rebalancing Block
if (balance > 1 && val < node.left.val) return rightRotate(node);
if (balance < -1 && val > node.right.val) return leftRotate(node);
if (balance > 1 && val > node.left.val) { node.left = leftRotate(node.left); return rightRotate(node); }
if (balance < -1 && val < node.right.val) { node.right = rightRotate(node.right); return leftRotate(node); }
```

---

## 7. Concrete Problem Examples
* **AVL Auto-Balancing Symbol Tables**: Compiler symbol lookup tables.
* **LeetCode 108 Adaptation**: Dynamically building height-balanced BSTs.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing AVL Insertion across multiple elements:

```java
public class AVLInsertionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. AVL Insertion & Auto-Rebalancing Test ===");
        AVLInsertionMaster.AVLNode root = null;
        int[] keys = {10, 20, 30, 40, 50, 25};

        for (int key : keys) {
            root = AVLInsertionMaster.insert(root, key);
        }

        System.out.println("Root Value:  " + root.val);                          // Output: 30
        System.out.println("Root Height: " + AVLInsertionMaster.getHeight(root)); // Output: 3
        System.out.println("Root Left:   " + root.left.val);                     // Output: 20
        System.out.println("Root Right:  " + root.right.val);                    // Output: 40 ✅
    }
}
```

---

## 9. Complexity Analysis

| AVL Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Rebalance Rotations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AVL Insertion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | **At Most 1 Rotation ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Inserting First Node into Empty Tree**: Returns `new AVLNode(val)` height 1.
* **Inserting Pre-Sorted Array (`1, 2, 3, 4, 5`)**: Rebalances continuously into height-balanced tree of height $\lfloor \log_2 N \rfloor + 1$.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Re-assign Subtree Return Pointers**:
  - Writing `insert(node.left, val)` without assigning `node.left = insert(node.left, val)` breaks tree connectivity after rotations.
  - **Always write: `node.left = insert(node.left, val)`**.
* **Checking `val < node.left.val` When `node.left` is Null**:
  - In `insert()`, `val < node.left.val` is only evaluated when `balance > 1`, which guarantees `node.left` is non-null!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Insertion Requires AT MOST 1 Rotation:
> A single rotation on the deepest unbalanced node $Z$ restores the height of subtree $Z$ to its EXACT height prior to the insertion.
> Because the height of subtree $Z$ does not change globally, parent ancestors of $Z$ experience zero height delta, halting all further rotation checks!

> **Memory Trick:** **"AVL Insert requires AT MOST 1 single or double rotation per insert!"**

---

## 13. System & Implementation Comparisons

| Feature | AVL Tree Insertion | Red-Black Tree Insertion |
| :--- | :--- | :--- |
| **Rotation Upper Bound** | **At Most 1 Rotation ⚡** | **At Most 2 Rotations ⚡** |
| **Strict Height Limit** | **$H \le 1.44 \log_2 N$ (Tighter) ⚡**| $H \le 2.0 \log_2 N$ (Looser) |
| **Rebalance Protocol** | Balance Factor $|\text{BF}| \le 1$ | Color Rules (Red/Black) |

---

## 14. How to Recognize This in Questions
* **"Dynamically insert elements into BST while maintaining strict height balance H = O(log N)"** $\rightarrow$ AVL Tree Insertion.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the maximum number of rotations performed during a single AVL insertion?**  
  *A:* At most **1 rotation** (either 1 single rotation or 1 double rotation).
* **Q: Why are duplicate keys ignored in standard AVL trees?**  
  *A:* Storing duplicate keys in separate nodes complicates height balance definitions. Duplicates are typically handled by storing a `count` frequency attribute inside nodes.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: AVL TREE INSERTION MECHANICS                          |
+-----------------------------------------------------------------------+
| • Step 1: Standard BST Leaf Insertion (node.left = insert(...))       |
| • Step 2: Update height (node.height = 1 + max(left, right))          |
| • Step 3: Evaluate Balance Factor (BF = left.height - right.height)   |
| • Step 4: Execute 1 of 4 Rotation Cases if |BF| >= 2                  |
| • Rotation Bound: AT MOST 1 rotation per insertion! ⚡                 |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write full AVL Insertion with 4-case rebalancing in Java.
- [ ] I can state the At-Most-One Rotation theorem for insertion.
- [ ] I know how `val < node.left.val` selects between LL and LR cases.
- [ ] I know why subtree height restoration halts higher rotations.
- [ ] I can trace multi-element AVL insertions step by step.
