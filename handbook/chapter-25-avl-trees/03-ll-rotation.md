# 03. Single Right Rotation (LL Case), Pointer Relinking & Order Preservation Proof

## 1. Introduction
A **Single Right Rotation** (also known as `rightRotate`) is the fundamental structural transformation used to restore height balance in an AVL Tree when a **Left-Left (LL) Imbalance** occurs. An LL imbalance occurs when an insertion or deletion causes a node $Y$ to have a **Balance Factor $\text{BF}(Y) = +2$** and its left child $X$ to have a **Balance Factor $\text{BF}(X) \ge 0$**. Executing a Single Right Rotation promotes left child $X$ to the root of the subtree and demotes $Y$ to $X$'s right child in **$O(1)$ Strict Constant Time and Space**, while strictly preserving the BST sorted key order ($L < Root < R$).

> **Important:** Triggering Conditions for Single Right Rotation (LL Case):
> 1. **Node Imbalance Condition**: Node $Y$ has **$\text{BF}(Y) = +2$** (Left-Heavy Unbalanced).
> 2. **Child Heavy Condition**: Left Child $X = Y.\text{left}$ has **$\text{BF}(X) \ge 0$** (Left-Heavy or Balanced).
> 3. **Action**: Execute **`rightRotate(Y)`**! Left child $X$ becomes the new subtree root, $Y$ becomes $X$'s right child, and $X$'s former right subtree $T_2$ attaches as $Y$'s left child! ⚡

```
Single Right Rotation (LL Case) Structural Transformation Topology:
        Unbalanced Node (Y) [BF = +2]                       Balanced New Root (X) [BF = 0]
               /           \        Right Rotation                 /           \
      Left Child (X) [BF = +1] [T3]  --------------->             [T1]        Node (Y) [BF = 0]
       /           \                 <---------------                         /       \
     [T1]          [T2]              Left Rotation                          [T2]      [T3]

In-Order Key Order BEFORE Rotation: T1 < X < T2 < Y < T3
In-Order Key Order AFTER Rotation : T1 < X < T2 < Y < T3 (STRICTLY IDENTICAL!) ⚡
```

---

## 2. Core Concepts & Pointer Relinking Equations

### 2.1 The `rightRotate(Y)` Step-by-Step Algorithm
Given unbalanced node $Y$:
1. Identify left child: **`X = Y.left`**.
2. Save $X$'s right subtree: **`T2 = X.right`**.
3. **Perform Rotation**:
   - Make $Y$ the right child of $X$: **`X.right = Y`**.
   - Attach $T_2$ as the left child of $Y$: **`Y.left = T2`**.
4. **Update Heights** (MUST update child $Y$ FIRST, then parent $X$!):
   - `updateHeight(Y)`.
   - `updateHeight(X)`.
5. Return **`X`** (New root of the subtree!).

```
Single Right Rotation Pointer Relinking Equations:
+-----------------------+-------------------+-------------------+
| Pointer Field         | Before Rotation   | After Rotation    |
+-----------------------+-------------------+-------------------+
| `X.right`             | Points to $T_2$   | Points to $Y$ ⚡   |
| `Y.left`              | Points to $X$     | Points to $T_2$ ⚡ |
| Subtree Root          | Node $Y$          | Node $X$ ⚡       |
+-----------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Right Rotate Y: X = Y.left; T2 = X.right; X.right = Y; Y.left = T2; Return X!"**

---

## 3. Mathematical Proof of BST Sorted Order Preservation

### 3.1 Algebraic Proof of In-Order Key Sequence Invariance
Let $K(N)$ denote the key of node $N$, and $K(T)$ denote all keys in subtree $T$:
* **Before Rotation**:
  1. $T_1$ is in left subtree of $X \implies K(T_1) < K(X)$.
  2. $T_2$ is in right subtree of $X$ and left subtree of $Y \implies K(X) < K(T_2) < K(Y)$.
  3. $T_3$ is in right subtree of $Y \implies K(Y) < K(T_3)$.
  - **In-Order Key Sequence**: $K(T_1) < K(X) < K(T_2) < K(Y) < K(T_3)$.

* **After Rotation**:
  1. $T_1$ remains left child of $X \implies K(T_1) < K(X)$.
  2. $Y$ is right child of $X$, and $T_2$ is left child of $Y \implies K(X) < K(T_2) < K(Y)$.
  3. $T_3$ remains right child of $Y \implies K(Y) < K(T_3)$.
  - **In-Order Key Sequence**: $K(T_1) < K(X) < K(T_2) < K(Y) < K(T_3)$.

$$\text{Sequence BEFORE} \equiv \text{Sequence AFTER} \implies \mathbf{100\% \text{ BST Order Preserved!}}$$

---

## 4. Internal Working Mechanics
Tracing Single Right Rotation on Unbalanced Tree `[30, 20, 10]` (LL Case):

```
Initial Tree: Node 30 (left=20, right=null). Node 20 (left=10, right=null).
- Height 10 = 1, Height 20 = 2, Height 30 = 3.
- BF(30) = 2 - 0 = +2 (UNBALANCED!). BF(20) = 1 - 0 = +1 (>= 0). LL Case!

Call rightRotate(Y=30):
1. X = Y.left = Node 20.
2. T2 = X.right = null.
3. X.right = Y (20.right becomes 30).
4. Y.left = T2 (30.left becomes null).
5. Update heights: Height 30 = 1, Height 20 = 2.
6. Return X (Node 20).

New Subtree Root = Node 20 (left=10, right=30). Height = 2. Perfect Balance (BF=0)! ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
LL Case Single Right Rotation Step-by-Step Topography:

```
Step 1: Identify Y (30) & X (20)             Step 2: Relink X.right = Y, Y.left = T2
        (30) +2 [Y]                                   (20) 0 [X]
       /   \                                         /    \
   (20) +1  null [T3]   Right Rotate(30)         (10)     (30) 0 [Y]
   /   \               ---------------->        /  \     /   \
(10)   null [T2]                              null null null null [T3]
 [T1]                                          [T1]      [T2]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Single Right Rotation (`rightRotate`) with height updating:

```java
import java.util.*;

public class LLRotationMaster {

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

    public static int getHeight(AVLNode node) {
        return (node == null) ? 0 : node.height;
    }

    public static void updateHeight(AVLNode node) {
        if (node != null) {
            node.height = 1 + Math.max(getHeight(node.left), getHeight(node.right));
        }
    }

    // Single Right Rotation (Solves LL Case) O(1) Time, O(1) Auxiliary Space
    public static AVLNode rightRotate(AVLNode y) {
        AVLNode x = y.left;
        AVLNode T2 = x.right;

        // Perform Rotation
        x.right = y;
        y.left = T2;

        // Update heights (Child y MUST be updated before new root x!)
        updateHeight(y);
        updateHeight(x);

        return x; // Return new root of subtree
    }
}
```

> **Quick Syntax:**
```java
// Single Right Rotation Engine
AVLNode x = y.left; AVLNode T2 = x.right;
x.right = y; y.left = T2;
updateHeight(y); updateHeight(x); return x;
```

---

## 7. Concrete Problem Examples
* **AVL Insertion (LL Case)**: Inserting into left subtree of left child.
* **AVL Deletion (RR Deletion Effect)**: Deleting from right subtree causes left-heavy LL imbalance.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Single Right Rotation:

```java
public class LLRotationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Single Right Rotation (LL Case) Test ===");
        // Build LL Unbalanced Tree: 30 -> 20 -> 10
        LLRotationMaster.AVLNode y = new LLRotationMaster.AVLNode(30);
        y.left = new LLRotationMaster.AVLNode(20, 
            new LLRotationMaster.AVLNode(10), null);
        LLRotationMaster.updateHeight(y);

        System.out.println("Root Value BEFORE Rotation: " + y.val); // Output: 30
        System.out.println("Root Height BEFORE Rotation: " + LLRotationMaster.getHeight(y)); // Output: 3

        LLRotationMaster.AVLNode newRoot = LLRotationMaster.rightRotate(y);

        System.out.println("\nRoot Value AFTER Rotation:  " + newRoot.val);       // Output: 20
        System.out.println("Root Height AFTER Rotation: " + LLRotationMaster.getHeight(newRoot)); // Output: 2
        System.out.println("New Root Left:  " + newRoot.left.val);                // Output: 10
        System.out.println("New Root Right: " + newRoot.right.val);               // Output: 30 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Time Complexity | Auxiliary Space | Memory Access |
| :--- | :--- | :--- | :--- |
| **`rightRotate(y)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 4 Pointer assignments |
| **Height Updates**   | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 2 Height calculations |

---

## 10. Edge Cases & Boundary Handling
* **Null Subtree $T_2$ (`x.right == null`)**: Handled cleanly by assignment `y.left = null`.
* **Root Subtree Assignment**: Caller MUST update parent link: `parent.left = rightRotate(y)` or `parent.right = rightRotate(y)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Updating Parent $X$ Height BEFORE Child $Y$ Height**:
  - `x.height` depends on `y.height`. Calling `updateHeight(x)` before `updateHeight(y)` computes $X$'s height using stale $Y$ height!
  - **ALWAYS call `updateHeight(y)` FIRST, then `updateHeight(x)` SECOND**.
* **Forgetting to Capture Return Value of Rotation**:
  - `rightRotate(y)` returns the new root $X$. Discarding the return value leaves the parent pointing to old node $Y$.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Single Right Rotation Decreases Subtree Height by 1:
> Before rotation: Height of left subtree $X$ was $H$, right subtree $T_3$ was $H-2$. Total height of $Y$ was $H + 1$.
> After rotation: Left subtree $T_1$ has height $H-1$, right subtree $Y$ has height $H-1$. Total height of new root $X$ becomes $H$.
> This reduces overall subtree height by 1 level, absorbing the new insertion!

> **Memory Trick:** **"Update child y height FIRST, parent x height SECOND!"**

---

## 13. System & Implementation Comparisons

| Feature | Single Right Rotation (`rightRotate`) | Single Left Rotation (`leftRotate`) |
| :--- | :--- | :--- |
| **Imbalance Case** | **LL Case ($\text{BF} = +2, \text{childBF} \ge 0$)**| RR Case ($\text{BF} = -2, \text{childBF} \le 0$) |
| **Promoted Node** | Left Child $X = Y.\text{left}$ | Right Child $X = Y.\text{right}$ |
| **Demoted Node** | Old Root $Y$ becomes Right Child | Old Root $Y$ becomes Left Child |

---

## 14. How to Recognize This in Questions
* **"Node has BF = +2 and left child has BF >= 0"** $\rightarrow$ Execute Single Right Rotation (`rightRotate`).
* **"Insertion into left subtree of left child causes imbalance"** $\rightarrow$ LL Case.

---

## 15. Frequently Asked Interview Questions
* **Q: How many pointer assignments are performed during a Single Right Rotation?**  
  *A:* Exactly **4 pointer assignments**: `X = Y.left`, `T2 = X.right`, `X.right = Y`, `Y.left = T2`.
* **Q: Why does Single Right Rotation preserve in-order sorted key order?**  
  *A:* Because $X < Y$, $T_1 < X$, $X < T_2 < Y$, and $Y < T_3$. The rotated structure maintains $T_1 < X < T_2 < Y < T_3$ identically.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SINGLE RIGHT ROTATION (LL CASE)                       |
+-----------------------------------------------------------------------+
| • Trigger Condition : Node BF = +2 AND Left Child BF >= 0 (LL Case)   |
| • Pointer Formulas  : X = Y.left; T2 = X.right; X.right = Y; Y.left = T2|
| • Height Rule       : MUST update child Y height FIRST, parent X SECOND|
| • Order Invariant   : In-Order key sequence T1 < X < T2 < Y < T3 preserved|
| • Complexity        : O(1) Constant Time | O(1) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `rightRotate` from memory in 6 lines.
- [ ] I can state the LL imbalance conditions ($\text{BF} = +2, \text{childBF} \ge 0$).
- [ ] I know why `updateHeight(y)` must be called before `updateHeight(x)`.
- [ ] I can prove why in-order sorted key order is preserved.
- [ ] I can trace a single right rotation step by step.
