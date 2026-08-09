# 05. Double Left-Right Rotation (LR Case), Zigzag Resolution & Double Rotation Engines

## 1. Introduction
A **Double Left-Right Rotation** (also known as `leftRightRotate`) is the double-rotation structural transformation used to restore height balance in an AVL Tree when a **Left-Right (LR) Zigzag Imbalance** occurs. An LR imbalance occurs when an insertion or deletion causes a node $Z$ to have a **Balance Factor $\text{BF}(Z) = +2$** and its left child $Y$ to have a **Balance Factor $\text{BF}(Y) < 0$** (right-heavy). Because a single right rotation on $Z$ fails to balance the right-heavy child $Y$, the LR double rotation executes a **Single Left Rotation on Child $Y$** followed by a **Single Right Rotation on Node $Z$** in **$O(1)$ Strict Constant Time and Space**.

> **Important:** Triggering Conditions for Double Left-Right Rotation (LR Case):
> 1. **Node Imbalance Condition**: Node $Z$ has **$\text{BF}(Z) = +2$** (Left-Heavy Unbalanced).
> 2. **Child Heavy Condition**: Left Child $Y = Z.\text{left}$ has **$\text{BF}(Y) < 0$** (Right-Heavy Zigzag).
> 3. **Action**: Execute Double Rotation:
>    - Step 1: **`Z.left = leftRotate(Z.left)`** (Converts LR zigzag case into a straight LL case!).
>    - Step 2: **`return rightRotate(Z)`** (Resolves the straight LL case to perfect balance!). ⚡

```
Double Left-Right Rotation (LR Case) Two-Step Transformation Topology:
   (Z) +2                (Z) +2                 (X) 0
  /                     /                      /   \
(Y) -1    Left-Rot(Y) (X)      Right-Rot(Z)  (Y)   (Z)
  \       --------->  /        ----------->
  (X)               (Y)

LR Zigzag converted to 100% Height-Balanced State (BF = 0)! ⚡
```

---

## 2. Core Concepts & Why Single Rotation Fails on LR Zigzag

### 2.1 Why Single Rotation Fails on LR Imbalance
Suppose node $Z$ has $\text{BF}(Z) = +2$ and left child $Y$ has $\text{BF}(Y) = -1$ (right-heavy child $X$):
* If we attempt a **Single Right Rotation on $Z$**:
  - $Y$ becomes the new root. But $X$ (which was the right child of $Y$) now becomes the left child of $Z$.
  - The tree remains unbalanced because the height of $X$ is simply shifted from left to right!
* **Solution**: Performing **`leftRotate(Y)`** FIRST promotes $X$ up to $Z$'s left child, aligning $Y, X, Z$ into a straight Left-Left (LL) line! Then **`rightRotate(Z)`** balances the tree completely! ⚡

```
LR Double Rotation Step-by-Step Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Rotation Step         | Target Node       | Resulting State   | Subtree Root      |
+-----------------------+-------------------+-------------------+-------------------+
| **Step 1: Left-Rotate**| Child $Y$         | Converts LR to LL | Child $X$         |
| **Step 2: Right-Rotate**| Node $Z$        | Restores Balance  | Node $X$ ⚡       |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LR Case (BF=+2, childBF<0): First leftRotate(node.left), then rightRotate(node)!"**

---

## 3. Characteristics & Pointer Relinking Equations

### 3.1 Structural Pointer Assignments in LR Rotation
Let $Z$ be the unbalanced node, $Y = Z.\text{left}$, and $X = Y.\text{right}$ (with subtrees $T_1, T_2, T_3, T_4$):
1. **After `leftRotate(Y)`**: $X$ becomes left child of $Z$, $Y$ becomes left child of $X$.
2. **After `rightRotate(Z)`**: $X$ becomes the new root of the entire subtree!
   - $X.\text{left} = Y$, $X.\text{right} = Z$.
   - $Y.\text{right} = T_2$, $Z.\text{left} = T_3$.

$$\text{In-Order Key Sequence}: T_1 < Y < T_2 < X < T_3 < Z < T_4 \quad (\mathbf{100\% \text{ Preserved!}})$$

---

## 4. Internal Working Mechanics
Tracing LR Double Rotation on Unbalanced Tree `[30, 10, 20]` (LR Case):

```
Initial Tree: Node 30 (left=10). Node 10 (right=20).
- BF(30) = +2, BF(10) = -1. Trigger LR Case!

Step 1: Execute leftRotate(child Y = 10):
  - Promotes Node 20 to left child of 30. Node 10 becomes left child of 20.
  - Tree becomes straight LL line: 30 -> left 20 -> left 10.

Step 2: Execute rightRotate(node Z = 30):
  - Promotes Node 20 to root of subtree!
  - Node 10 becomes left child of 20; Node 30 becomes right child of 20.

New Subtree Root = Node 20 (left=10, right=30). Height = 2. Perfect Balance (BF=0)! ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
LR Double Rotation Full Structural Topography:

```
    (30) +2 [Z]               (30) +2 [Z]               (20) 0 [X]
   /                         /                         /    \
(10) -1 [Y]   Left-Rot(10) (20) +1      Right-Rot(30) (10)    (30)
   \          -----------> /            ------------>
   (20)                  (10)
   [X]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Double Left-Right Rotation (`leftRightRotate` / `rotateLR`):

```java
import java.util.*;

public class LRRotationMaster {

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

    // Double Left-Right Rotation (Solves LR Case) O(1) Time, O(1) Auxiliary Space
    public static AVLNode rotateLR(AVLNode z) {
        // Step 1: Left rotate child Y to convert LR to straight LL case
        z.left = leftRotate(z.left);

        // Step 2: Right rotate node Z to restore perfect height balance
        return rightRotate(z);
    }
}
```

> **Quick Syntax:**
```java
// Double Left-Right Rotation Engine
z.left = leftRotate(z.left);
return rightRotate(z);
```

---

## 7. Concrete Problem Examples
* **AVL Insertion (LR Case)**: Inserting into right subtree of left child.
* **AVL Deletion (RL Deletion Effect)**: Deleting from right subtree causes left-heavy LR zigzag imbalance.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Double Left-Right Rotation:

```java
public class LRRotationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Double Left-Right Rotation (LR Case) Test ===");
        // Build LR Unbalanced Tree: 30 -> 10 -> 20
        LRRotationMaster.AVLNode z = new LRRotationMaster.AVLNode(30);
        z.left = new LRRotationMaster.AVLNode(10, 
            null, new LRRotationMaster.AVLNode(20));
        LRRotationMaster.updateHeight(z);

        System.out.println("Root Value BEFORE Rotation: " + z.val); // Output: 30
        System.out.println("Root Height BEFORE Rotation: " + LRRotationMaster.getHeight(z)); // Output: 3

        LRRotationMaster.AVLNode newRoot = LRRotationMaster.rotateLR(z);

        System.out.println("\nRoot Value AFTER Rotation:  " + newRoot.val);       // Output: 20
        System.out.println("Root Height AFTER Rotation: " + LRRotationMaster.getHeight(newRoot)); // Output: 2
        System.out.println("New Root Left:  " + newRoot.left.val);                // Output: 10
        System.out.println("New Root Right: " + newRoot.right.val);               // Output: 30 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Time Complexity | Auxiliary Space | Memory Access |
| :--- | :--- | :--- | :--- |
| **`rotateLR(z)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 8 Pointer assignments (2 single rotations) |
| **Height Updates** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 4 Height calculations |

---

## 10. Edge Cases & Boundary Handling
* **Subtrees $T_2, T_3$ Empty**: Handled cleanly by pointer relinking logic inside `leftRotate` and `rightRotate`.
* **Root Subtree Assignment**: Caller MUST capture return value: `node = rotateLR(node)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting Single Right Rotation on LR Case**:
  - Applying `rightRotate(Z)` directly on an LR case shifts the right-heavy child $X$ from left to right, leaving the tree unbalanced!
  - **ALWAYS execute `leftRotate(z.left)` FIRST, then `rightRotate(z)` SECOND**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** How to Instantly Identify the LR Double Rotation Case:
> 1. Check parent node balance factor: **$\text{BF}(Z) = +2$** (Left-Heavy).
> 2. Check left child balance factor: **$\text{BF}(Z.\text{left}) < 0$** (Right-Heavy).
> Opposite balance factor signs ($+2$ vs $-1$) signal a **Zigzag Shape**, demanding a **Double Rotation**!

> **Memory Trick:** **"Opposite BF signs (+2 and -1) signal a Zigzag case requiring Double Rotation!"**

---

## 13. System & Implementation Comparisons

| Feature | Double Left-Right Rotation (`rotateLR`) | Single Right Rotation (`rightRotate`) |
| :--- | :--- | :--- |
| **Imbalance Case** | **LR Case ($\text{BF} = +2, \text{childBF} < 0$)**| LL Case ($\text{BF} = +2, \text{childBF} \ge 0$) |
| **Rotation Steps** | 2 Single Rotations (`leftRotate` then `rightRotate`) | 1 Single Rotation (`rightRotate`) |
| **Promoted Node** | Grandchild $X = Z.\text{left}.\text{right}$ | Left Child $X = Z.\text{left}$ |

---

## 14. How to Recognize This in Questions
* **"Node has BF = +2 and left child has BF < 0"** $\rightarrow$ Execute Double Left-Right Rotation (`rotateLR`).
* **"Insertion into right subtree of left child causes imbalance"** $\rightarrow$ LR Case.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is LR rotation called a "Double Rotation"?**  
  *A:* Because it executes 2 single rotations sequentially: first `leftRotate(child)`, then `rightRotate(parent)`.
* **Q: Which node becomes the new subtree root after an LR double rotation?**  
  *A:* The grandchild node $X = Z.\text{left}.\text{right}$ is promoted to become the new root of the subtree!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DOUBLE LEFT-RIGHT ROTATION (LR CASE)                  |
+-----------------------------------------------------------------------+
| • Trigger Condition : Node BF = +2 AND Left Child BF < 0 (LR Case)    |
| • Execution Code    : z.left = leftRotate(z.left); return rightRotate(z);|
| • Promoted Node     : Grandchild X = Z.left.right becomes NEW ROOT    |
| • Order Invariant   : In-Order key sequence T1 < Y < T2 < X < T3 < Z < T4 |
| • Complexity        : O(1) Constant Time | O(1) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `rotateLR` from memory in 3 lines.
- [ ] I can state the LR imbalance conditions ($\text{BF} = +2, \text{childBF} < 0$).
- [ ] I know why single rotation fails on zigzag imbalances.
- [ ] I know which node becomes the new root after an LR rotation.
- [ ] I can trace a double LR rotation step by step.
