# 04. Single Left Rotation (RR Case), Pointer Relinking & Order Preservation Proof

## 1. Introduction
A **Single Left Rotation** (also known as `leftRotate`) is the symmetric dual of the right rotation, used to restore height balance in an AVL Tree when a **Right-Right (RR) Imbalance** occurs. An RR imbalance occurs when an insertion or deletion causes a node $X$ to have a **Balance Factor $\text{BF}(X) = -2$** and its right child $Y$ to have a **Balance Factor $\text{BF}(Y) \le 0$**. Executing a Single Left Rotation promotes right child $Y$ to the root of the subtree and demotes $X$ to $Y$'s left child in **$O(1)$ Strict Constant Time and Space**, while strictly preserving the BST sorted key order ($L < Root < R$).

> **Important:** Triggering Conditions for Single Left Rotation (RR Case):
> 1. **Node Imbalance Condition**: Node $X$ has **$\text{BF}(X) = -2$** (Right-Heavy Unbalanced).
> 2. **Child Heavy Condition**: Right Child $Y = X.\text{right}$ has **$\text{BF}(Y) \le 0$** (Right-Heavy or Balanced).
> 3. **Action**: Execute **`leftRotate(X)`**! Right child $Y$ becomes the new subtree root, $X$ becomes $Y$'s left child, and $Y$'s former left subtree $T_2$ attaches as $X$'s right child! ⚡

```
Single Left Rotation (RR Case) Structural Transformation Topology:
        Unbalanced Node (X) [BF = -2]                       Balanced New Root (Y) [BF = 0]
               /           \        Left Rotation                  /           \
             [T1]     Right Child (Y) [BF = -1] ------------->  Node (X) [BF = 0] [T3]
                       /           \        <-------------       /       \
                     [T2]          [T3]     Right Rotation     [T1]      [T2]

In-Order Key Order BEFORE Rotation: T1 < X < T2 < Y < T3
In-Order Key Order AFTER Rotation : T1 < X < T2 < Y < T3 (STRICTLY IDENTICAL!) ⚡
```

---

## 2. Core Concepts & Pointer Relinking Equations

### 2.1 The `leftRotate(X)` Step-by-Step Algorithm
Given unbalanced node $X$:
1. Identify right child: **`Y = X.right`**.
2. Save $Y$'s left subtree: **`T2 = Y.left`**.
3. **Perform Rotation**:
   - Make $X$ the left child of $Y$: **`Y.left = X`**.
   - Attach $T_2$ as the right child of $X$: **`X.right = T2`**.
4. **Update Heights** (MUST update child $X$ FIRST, then parent $Y$!):
   - `updateHeight(X)`.
   - `updateHeight(Y)`.
5. Return **`Y`** (New root of the subtree!).

```
Single Left Rotation Pointer Relinking Equations:
+-----------------------+-------------------+-------------------+
| Pointer Field         | Before Rotation   | After Rotation    |
+-----------------------+-------------------+-------------------+
| `Y.left`              | Points to $T_2$   | Points to $X$ ⚡   |
| `X.right`             | Points to $Y$     | Points to $T_2$ ⚡ |
| Subtree Root          | Node $X$          | Node $Y$ ⚡       |
+-----------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Left Rotate X: Y = X.right; T2 = Y.left; Y.left = X; X.right = T2; Return Y!"**

---

## 3. Mathematical Proof of BST Sorted Order Preservation

### 3.1 Algebraic Proof of In-Order Key Sequence Invariance
Let $K(N)$ denote the key of node $N$, and $K(T)$ denote all keys in subtree $T$:
* **Before Rotation**:
  1. $T_1$ is in left subtree of $X \implies K(T_1) < K(X)$.
  2. $T_2$ is in left subtree of $Y$ and right subtree of $X \implies K(X) < K(T_2) < K(Y)$.
  3. $T_3$ is in right subtree of $Y \implies K(Y) < K(T_3)$.
  - **In-Order Key Sequence**: $K(T_1) < K(X) < K(T_2) < K(Y) < K(T_3)$.

* **After Rotation**:
  1. $T_1$ remains left child of $X \implies K(T_1) < K(X)$.
  2. $X$ is left child of $Y$, and $T_2$ is right child of $X \implies K(X) < K(T_2) < K(Y)$.
  3. $T_3$ remains right child of $Y \implies K(Y) < K(T_3)$.
  - **In-Order Key Sequence**: $K(T_1) < K(X) < K(T_2) < K(Y) < K(T_3)$.

$$\text{Sequence BEFORE} \equiv \text{Sequence AFTER} \implies \mathbf{100\% \text{ BST Order Preserved!}}$$

---

## 4. Internal Working Mechanics
Tracing Single Left Rotation on Unbalanced Tree `[10, 20, 30]` (RR Case):

```
Initial Tree: Node 10 (left=null, right=20). Node 20 (left=null, right=30).
- Height 30 = 1, Height 20 = 2, Height 10 = 3.
- BF(10) = 0 - 2 = -2 (UNBALANCED!). BF(20) = 0 - 1 = -1 (<= 0). RR Case!

Call leftRotate(X=10):
1. Y = X.right = Node 20.
2. T2 = Y.left = null.
3. Y.left = X (20.left becomes 10).
4. X.right = T2 (10.right becomes null).
5. Update heights: Height 10 = 1, Height 20 = 2.
6. Return Y (Node 20).

New Subtree Root = Node 20 (left=10, right=30). Height = 2. Perfect Balance (BF=0)! ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
RR Case Single Left Rotation Step-by-Step Topography:

```
Step 1: Identify X (10) & Y (20)             Step 2: Relink Y.left = X, X.right = T2
        (10) -2 [X]                                   (20) 0 [Y]
       /   \                                         /    \
  null [T1] (20) -1 [Y]  Left Rotate(10)          (10) 0    (30)
           /   \        --------------->        /  \     /   \
        null   (30)                          null  null null null [T3]
        [T2]   [T3]                          [T1]  [T2]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Single Left Rotation (`leftRotate`) with height updating:

```java
import java.util.*;

public class RRRotationMaster {

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

    // Single Left Rotation (Solves RR Case) O(1) Time, O(1) Auxiliary Space
    public static AVLNode leftRotate(AVLNode x) {
        AVLNode y = x.right;
        AVLNode T2 = y.left;

        // Perform Rotation
        y.left = x;
        x.right = T2;

        // Update heights (Child x MUST be updated before new root y!)
        updateHeight(x);
        updateHeight(y);

        return y; // Return new root of subtree
    }
}
```

> **Quick Syntax:**
```java
// Single Left Rotation Engine
AVLNode y = x.right; AVLNode T2 = y.left;
y.left = x; x.right = T2;
updateHeight(x); updateHeight(y); return y;
```

---

## 7. Concrete Problem Examples
* **AVL Insertion (RR Case)**: Inserting into right subtree of right child.
* **AVL Deletion (LL Deletion Effect)**: Deleting from left subtree causes right-heavy RR imbalance.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Single Left Rotation:

```java
public class RRRotationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Single Left Rotation (RR Case) Test ===");
        // Build RR Unbalanced Tree: 10 -> 20 -> 30
        RRRotationMaster.AVLNode x = new RRRotationMaster.AVLNode(10);
        x.right = new RRRotationMaster.AVLNode(20, 
            null, new RRRotationMaster.AVLNode(30));
        RRRotationMaster.updateHeight(x);

        System.out.println("Root Value BEFORE Rotation: " + x.val); // Output: 10
        System.out.println("Root Height BEFORE Rotation: " + RRRotationMaster.getHeight(x)); // Output: 3

        RRRotationMaster.AVLNode newRoot = RRRotationMaster.leftRotate(x);

        System.out.println("\nRoot Value AFTER Rotation:  " + newRoot.val);       // Output: 20
        System.out.println("Root Height AFTER Rotation: " + RRRotationMaster.getHeight(newRoot)); // Output: 2
        System.out.println("New Root Left:  " + newRoot.left.val);                // Output: 10
        System.out.println("New Root Right: " + newRoot.right.val);               // Output: 30 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Time Complexity | Auxiliary Space | Memory Access |
| :--- | :--- | :--- | :--- |
| **`leftRotate(x)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 4 Pointer assignments |
| **Height Updates**  | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 2 Height calculations |

---

## 10. Edge Cases & Boundary Handling
* **Null Subtree $T_2$ (`y.left == null`)**: Handled cleanly by assignment `x.right = null`.
* **Root Subtree Assignment**: Caller MUST update parent link: `parent.left = leftRotate(x)` or `parent.right = leftRotate(x)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Updating Parent $Y$ Height BEFORE Child $X$ Height**:
  - `y.height` depends on `x.height`. Calling `updateHeight(y)` before `updateHeight(x)` computes $Y$'s height using stale $X$ height!
  - **ALWAYS call `updateHeight(x)` FIRST, then `updateHeight(y)` SECOND**.
* **Forgetting to Capture Return Value of Rotation**:
  - `leftRotate(x)` returns the new root $Y$. Discarding the return value leaves the parent pointing to old node $X$.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Duality Between Single Left and Right Rotations:
> * **`rightRotate(Y)`**: Promotes left child $X$, demotes $Y$ to right child, transfers $X.right \to Y.left$.
> * **`leftRotate(X)`**: Promotes right child $Y$, demotes $X$ to left child, transfers $Y.left \to X.right$.
> Both operations execute in **$O(1)$ constant time** and preserve BST sorted key order 100%!

> **Memory Trick:** **"Update child x height FIRST, parent y height SECOND in leftRotate!"**

---

## 13. System & Implementation Comparisons

| Feature | Single Left Rotation (`leftRotate`) | Single Right Rotation (`rightRotate`) |
| :--- | :--- | :--- |
| **Imbalance Case** | **RR Case ($\text{BF} = -2, \text{childBF} \le 0$)**| LL Case ($\text{BF} = +2, \text{childBF} \ge 0$) |
| **Promoted Node** | Right Child $Y = X.\text{right}$ | Left Child $X = Y.\text{left}$ |
| **Demoted Node** | Old Root $X$ becomes Left Child | Old Root $Y$ becomes Right Child |

---

## 14. How to Recognize This in Questions
* **"Node has BF = -2 and right child has BF <= 0"** $\rightarrow$ Execute Single Left Rotation (`leftRotate`).
* **"Insertion into right subtree of right child causes imbalance"** $\rightarrow$ RR Case.

---

## 15. Frequently Asked Interview Questions
* **Q: How many pointer assignments are performed during a Single Left Rotation?**  
  *A:* Exactly **4 pointer assignments**: `Y = X.right`, `T2 = Y.left`, `Y.left = X`, `X.right = T2`.
* **Q: Why does Single Left Rotation decrease overall subtree height by 1?**  
  *A:* Because the right-heavy subtree of height $H$ becomes a child of $Y$, balancing both left and right subtrees to height $H-1$, resulting in total new root height $H$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SINGLE LEFT ROTATION (RR CASE)                        |
+-----------------------------------------------------------------------+
| • Trigger Condition : Node BF = -2 AND Right Child BF <= 0 (RR Case)  |
| • Pointer Formulas  : Y = X.right; T2 = Y.left; Y.left = X; X.right = T2|
| • Height Rule       : MUST update child X height FIRST, parent Y SECOND|
| • Order Invariant   : In-Order key sequence T1 < X < T2 < Y < T3 preserved|
| • Complexity        : O(1) Constant Time | O(1) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `leftRotate` from memory in 6 lines.
- [ ] I can state the RR imbalance conditions ($\text{BF} = -2, \text{childBF} \le 0$).
- [ ] I know why `updateHeight(x)` must be called before `updateHeight(y)`.
- [ ] I can prove why in-order sorted key order is preserved.
- [ ] I can trace a single left rotation step by step.
