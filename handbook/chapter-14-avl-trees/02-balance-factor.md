# 02. Balance Factor Calculation, 5-State Classifications & Imbalance Triggers

## 1. Introduction
The **Balance Factor ($\text{BF}$)** is the fundamental metric that drives self-balancing operations in an AVL Tree. Computed for every node as the height difference between its left and right subtrees, the Balance Factor quantitatively monitors tree geometry. When an insertion or deletion causes $|\text{BF}(X)| \ge 2$, the node is flagged as **UNBALANCED**, triggering targeted single or double tree rotations to restore global height balance in **$O(1)$ constant time**.

> **Important:** The 5 Canonical Balance Factor States of an AVL Node:
> 1. **$\text{BF}(X) = 0$ (Perfect Balance)**: Left and Right subtrees have identical heights ($H_{\text{left}} = H_{\text{right}}$).
> 2. **$\text{BF}(X) = +1$ (Left-Heavy Balanced)**: Left subtree is 1 level taller than Right subtree.
> 3. **$\text{BF}(X) = -1$ (Right-Heavy Balanced)**: Right subtree is 1 level taller than Left subtree.
> 4. **$\text{BF}(X) = +2$ (Left-Heavy UNBALANCED - Rotation Required!)**: Left subtree is 2 levels taller!
> 5. **$\text{BF}(X) = -2$ (Right-Heavy UNBALANCED - Rotation Required!)**: Right subtree is 2 levels taller! ⚡

```
The 5 Balance Factor State Spectrum Topology:
  BF = 0 (Balanced)       BF = +1 (Left-Heavy)      BF = +2 (UNBALANCED - ROTATE!)
        (50)                      (50)                      (50) +2
       /    \                    /    \                    /
    (30)    (70)              (30)    (70)              (30) +1
                             /                         /
                          (20)                      (20)
```

---

## 2. Core Concepts & Balance Factor Mathematical Equation

### 2.1 Balance Factor Formula & Height Update Invariants
For any node $X$ in an AVL tree:

$$\text{Height}(X) = 1 + \max(\text{Height}(\text{left}(X)), \text{Height}(\text{right}(X)))$$

$$\mathbf{\text{Balance Factor } \text{BF}(X) = \text{Height}(\text{left}(X)) - \text{Height}(\text{right}(X))}$$

* Null node height $= 0$.
* Leaf node height $= 1 \implies \text{BF}(\text{leaf}) = 1 - 1 = 0$.

```
Balance Factor Imbalance Case Classification Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Node BF               | Child Node        | Child BF          | Rebalancing Case  |
+-----------------------+-------------------+-------------------+-------------------+
| **$\text{BF} = +2$**  | `node.left`       | **$\text{BF} \ge 0$**| **LL Case (Single Right Rotate)**|
| **$\text{BF} = +2$**  | `node.left`       | **$\text{BF} < 0$** | **LR Case (Double Left-Right)**  |
| **$\text{BF} = -2$**  | `node.right`      | **$\text{BF} \le 0$**| **RR Case (Single Left Rotate)** |
| **$\text{BF} = -2$**  | `node.right`      | **$\text{BF} > 0$** | **RL Case (Double Right-Left)**  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"BF = Height(Left) - Height(Right)! |BF| <= 1 is valid; |BF| >= 2 triggers rotations!"**

---

## 3. Characteristics & Propagation of Height Changes

### 3.1 Bottom-Up Height Update Propagation
* **Insertion**: An insertion increases the height of ancestor nodes along the search path. Balance factors are re-calculated bottom-up. Re-balancing AT MOST ONE node restores global balance for insertion!
* **Deletion**: A deletion decreases subtree height, which can propagate balance factor changes all the way up to the root, requiring up to $O(\log N)$ rotations.

---

## 4. Internal Working Mechanics
Tracing Balance Factor Updates during Insertion of 10 into AVL Tree `[50, 30]`:

```
Initial Tree: Node 50 (left=30). Height 50 = 2, Height 30 = 1. BF(50) = 1 - 0 = +1.

Insert 10 under Node 30:
1. Node 10 (Leaf): Height = 1, BF = 0.
2. Node 30: Height = 1 + max(1, 0) = 2. BF(30) = 1 - 0 = +1.
3. Node 50: Height = 1 + max(2, 0) = 3. BF(50) = 2 - 0 = +2!

Node 50 has BF = +2 (UNBALANCED!). Left Child 30 has BF = +1 (>= 0).
Triggers LL Case -> Single Right Rotation on Node 50! ✅
```

---

## 5. Visual Diagram
Imbalance Triggers & Balance Factor Spectrum Topography:

```
          Node Y (BF = +2) <--- Imbalance Triggered!
         /                \
   Node X (BF = +1)       [T3] (Height h)
   /              \
 [T1] (Height h+1) [T2] (Height h)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite demonstrating Balance Factor computation, State Classification, and Bottom-Up Height Maintenance:

```java
import java.util.*;

public class BalanceFactorMaster {

    public static class AVLNode {
        public int val;
        public int height;
        public AVLNode left;
        public AVLNode right;

        public AVLNode(int val) {
            this.val = val;
            this.height = 1;
        }

        public AVLNode(int val, AVLNode left, AVLNode right) {
            this.val = val;
            this.height = 1 + Math.max(getHeight(left), getHeight(right));
            this.left = left;
            this.right = right;
        }
    }

    // Safely compute Height of any node O(1) Time
    public static int getHeight(AVLNode node) {
        return (node == null) ? 0 : node.height;
    }

    // Safely compute Balance Factor O(1) Time
    public static int getBalanceFactor(AVLNode node) {
        return (node == null) ? 0 : getHeight(node.left) - getHeight(node.right);
    }

    // Re-calculate node height from children O(1) Time
    public static void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
        }
    }

    // Classify Balance Factor State into String Descriptor
    public static String classifyBalanceState(AVLNode node) {
        int bf = getBalanceFactor(node);
        switch (bf) {
            case 0:  return "PERFECTLY_BALANCED (BF=0)";
            case 1:  return "LEFT_HEAVY_BALANCED (BF=+1)";
            case -1: return "RIGHT_HEAVY_BALANCED (BF=-1)";
            case 2:  return "UNBALANCED_LEFT_HEAVY (BF=+2)";
            case -2: return "UNBALANCED_RIGHT_HEAVY (BF=-2)";
            default: return "CRITICAL_IMBALANCE (BF=" + bf + ")";
        }
    }
}
```

> **Quick Syntax:**
```java
// Balance Factor Line
int bf = (node == null) ? 0 : getHeight(node.left) - getHeight(node.right);
```

---

## 7. Concrete Problem Examples
* **AVL Auto-Rebalancing Engines**: Monitoring balance factors after every insertion/deletion.
* **LeetCode 110 - Balanced Binary Tree**: Bottom-up height balance verification.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `getBalanceFactor` and `classifyBalanceState`:

```java
public class BalanceFactorDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Balance Factor State Classification Test ===");
        // Build Left-Unbalanced Subtree: 50 -> 30 -> 10
        BalanceFactorMaster.AVLNode root = new BalanceFactorMaster.AVLNode(50);
        root.left = new BalanceFactorMaster.AVLNode(30, 
            new BalanceFactorMaster.AVLNode(10), null);

        // Update heights bottom-up
        BalanceFactorMaster.updateHeight(root.left);
        BalanceFactorMaster.updateHeight(root);

        System.out.println("Node 10 State: " + 
            BalanceFactorMaster.classifyBalanceState(root.left.left)); // PERFECTLY_BALANCED (BF=0)

        System.out.println("Node 30 State: " + 
            BalanceFactorMaster.classifyBalanceState(root.left));      // LEFT_HEAVY_BALANCED (BF=+1)

        System.out.println("Node 50 State: " + 
            BalanceFactorMaster.classifyBalanceState(root));           // UNBALANCED_LEFT_HEAVY (BF=+2) ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`getHeight(node)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | Direct field access |
| **`getBalanceFactor(node)`**| **$O(1)$ Constant ⚡**| **$O(1)$ Constant ⚡** | Single subtraction |
| **`updateHeight(node)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | `1 + max(left, right)` |

---

## 10. Edge Cases & Boundary Handling
* **Null Pointer**: `getHeight(null)` returns 0, `getBalanceFactor(null)` returns 0.
* **Leaf Node**: Height is 1, Balance Factor is $1 - 0 = 0$.

---

## 11. Common Mistakes & Anti-Patterns
* **Re-calculating Heights Recursively ($O(N)$ Penalty)**:
  - Calling a full tree height function `computeHeight(node)` to get child heights inside `getBalanceFactor` turns $O(1)$ operations into $O(N)$ operations!
  - **Always store and access the explicit `node.height` field in $O(1)$ time**.
* **Reversing Balance Factor Sign Formula**:
  - Writing `Height(Right) - Height(Left)` reverses positive and negative balance factor interpretations.
  - **Standard Convention: $\text{BF} = \text{Height}(\text{Left}) - \text{Height}(\text{Right})$**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `node.height` MUST Be Updated AFTER Rotations:
> Tree rotations alter parent-child relationships between nodes.
> Failing to call `updateHeight(child)` and `updateHeight(parent)` immediately after rotating leaves stale height values in memory, corrupting future balance factor queries!

> **Memory Trick:** **"BF = Height(Left) - Height(Right)! Always update node heights after rotations!"**

---

## 13. System & Implementation Comparisons

| Feature | Stored Explicit Height Attribute | On-the-Fly Recursive Height Calculation |
| :--- | :--- | :--- |
| **BF Access Time** | **$O(1)$ Constant Time ⚡** | $O(N)$ Linear Scan ❌ |
| **Memory Overhead** | 4 Bytes `int height` per Node | Zero Extra Bytes |
| **Performance Impact**| **100x Faster Rebalancing ⚡**| Horribly Slow |

---

## 14. How to Recognize This in Questions
* **"Determine if node requires rotation based on subtree height difference"** $\rightarrow$ Check $|\text{BF}| \ge 2$.
* **"Identify which of the 4 AVL rotation cases applies"** $\rightarrow$ Inspect `node.BF` and `child.BF`.

---

## 15. Frequently Asked Interview Questions
* **Q: What balance factor values trigger an AVL tree rotation?**  
  *A:* $\text{BF} = +2$ (Left-Unbalanced) or $\text{BF} = -2$ (Right-Unbalanced).
* **Q: How does `child.BF` distinguish between Single and Double Rotations?**  
  *A:* If `node.BF = +2`: `child.BF >= 0` indicates LL Case (Single Right Rotate); `child.BF < 0` indicates LR Case (Double Left-Right Rotate).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BALANCE FACTOR METRICS & CLASSIFICATIONS              |
+-----------------------------------------------------------------------+
| • Formula       : Balance Factor = Height(Left) - Height(Right)       |
| • Valid Range   : -1, 0, +1 (Height-Balanced State)                   |
| • Imbalance State: |BF| >= 2 requires immediate rotation!              |
| • Height Formula : height = 1 + max(height(left), height(right))      |
| • Performance   : Stored node.height field enables O(1) BF access ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write the Balance Factor formula $\text{BF} = H_{\text{left}} - H_{\text{right}}$.
- [ ] I can write `getHeight`, `getBalanceFactor`, and `updateHeight`.
- [ ] I know all 5 Balance Factor states ($0, +1, -1, +2, -2$).
- [ ] I know why explicit `node.height` storage is required for $O(1)$ performance.
- [ ] I know how `node.BF` and `child.BF` select the correct rotation case.
