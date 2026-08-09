# 06. Double Right-Left Rotation (RL Case), Zigzag Resolution & Double Rotation Engines

## 1. Introduction
A **Double Right-Left Rotation** (also known as `rightLeftRotate`) is the symmetric dual of the LR double rotation, used to restore height balance in an AVL Tree when a **Right-Left (RL) Zigzag Imbalance** occurs. An RL imbalance occurs when an insertion or deletion causes a node $Z$ to have a **Balance Factor $\text{BF}(Z) = -2$** and its right child $Y$ to have a **Balance Factor $\text{BF}(Y) > 0$** (left-heavy). Because a single left rotation on $Z$ fails to balance the left-heavy child $Y$, the RL double rotation executes a **Single Right Rotation on Child $Y$** followed by a **Single Left Rotation on Node $Z$** in **$O(1)$ Strict Constant Time and Space**.

> **Important:** Triggering Conditions for Double Right-Left Rotation (RL Case):
> 1. **Node Imbalance Condition**: Node $Z$ has **$\text{BF}(Z) = -2$** (Right-Heavy Unbalanced).
> 2. **Child Heavy Condition**: Right Child $Y = Z.\text{right}$ has **$\text{BF}(Y) > 0$** (Left-Heavy Zigzag).
> 3. **Action**: Execute Double Rotation:
>    - Step 1: **`Z.right = rightRotate(Z.right)`** (Converts RL zigzag case into a straight RR case!).
>    - Step 2: **`return leftRotate(Z)`** (Resolves the straight RR case to perfect balance!). ⚡

```
Double Right-Left Rotation (RL Case) Two-Step Transformation Topology:
    (Z) -2               (Z) -2                (X) 0
      \                    \                  /   \
      (Y) +1  Right-Rot(Y) (X)   Left-Rot(Z) (Z)   (Y)
      /       ----------->   \   ---------->
    (X)                      (Y)

RL Zigzag converted to 100% Height-Balanced State (BF = 0)! ⚡
```

---

## 2. Core Concepts & Why Single Rotation Fails on RL Zigzag

### 2.1 Why Single Rotation Fails on RL Imbalance
Suppose node $Z$ has $\text{BF}(Z) = -2$ and right child $Y$ has $\text{BF}(Y) = +1$ (left-heavy child $X$):
* If we attempt a **Single Left Rotation on $Z$**:
  - $Y$ becomes the new root. But $X$ (which was the left child of $Y$) now becomes the right child of $Z$.
  - The tree remains unbalanced because the height of $X$ is simply shifted from right to left!
* **Solution**: Performing **`rightRotate(Y)`** FIRST promotes $X$ up to $Z$'s right child, aligning $Z, X, Y$ into a straight Right-Right (RR) line! Then **`leftRotate(Z)`** balances the tree completely! ⚡

```
RL Double Rotation Step-by-Step Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Rotation Step         | Target Node       | Resulting State   | Subtree Root      |
+-----------------------+-------------------+-------------------+-------------------+
| **Step 1: Right-Rotate**| Child $Y$        | Converts RL to RR | Child $X$         |
| **Step 2: Left-Rotate** | Node $Z$        | Restores Balance  | Node $X$ ⚡       |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"RL Case (BF=-2, childBF>0): First rightRotate(node.right), then leftRotate(node)!"**

---

## 3. Characteristics & Pointer Relinking Equations

### 3.1 Structural Pointer Assignments in RL Rotation
Let $Z$ be the unbalanced node, $Y = Z.\text{right}$, and $X = Y.\text{left}$ (with subtrees $T_1, T_2, T_3, T_4$):
1. **After `rightRotate(Y)`**: $X$ becomes right child of $Z$, $Y$ becomes right child of $X$.
2. **After `leftRotate(Z)`**: $X$ becomes the new root of the entire subtree!
   - $X.\text{left} = Z$, $X.\text{right} = Y$.
   - $Z.\text{right} = T_2$, $Y.\text{left} = T_3$.

$$\text{In-Order Key Sequence}: T_1 < Z < T_2 < X < T_3 < Y < T_4 \quad (\mathbf{100\% \text{ Preserved!}})$$

---

## 4. Internal Working Mechanics
Tracing RL Double Rotation on Unbalanced Tree `[10, 30, 20]` (RL Case):

```
Initial Tree: Node 10 (right=30). Node 30 (left=20).
- BF(10) = -2, BF(30) = +1. Trigger RL Case!

Step 1: Execute rightRotate(child Y = 30):
  - Promotes Node 20 to right child of 10. Node 30 becomes right child of 20.
  - Tree becomes straight RR line: 10 -> right 20 -> right 30.

Step 2: Execute leftRotate(node Z = 10):
  - Promotes Node 20 to root of subtree!
  - Node 10 becomes left child of 20; Node 30 becomes right child of 20.

New Subtree Root = Node 20 (left=10, right=30). Height = 2. Perfect Balance (BF=0)! ✅ (O(1) Time!)
```

---

## 5. Visual Diagram
RL Double Rotation Full Structural Topography:

```
    (10) -2 [Z]               (10) -2 [Z]               (20) 0 [X]
      \                         \                      /    \
      (30) +1 [Y] Right-Rot(30) (20) -1  Left-Rot(10) (10)    (30)
      /           ------------>   \  ------------->
    (20)                          (30)
    [X]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Double Right-Left Rotation (`rightLeftRotate` / `rotateRL`):

```java
import java.util.*;

public class RLRotationMaster {

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

    // Double Right-Left Rotation (Solves RL Case) O(1) Time, O(1) Auxiliary Space
    public static AVLNode rotateRL(AVLNode z) {
        // Step 1: Right rotate child Y to convert RL to straight RR case
        z.right = rightRotate(z.right);

        // Step 2: Left rotate node Z to restore perfect height balance
        return leftRotate(z);
    }
}
```

> **Quick Syntax:**
```java
// Double Right-Left Rotation Engine
z.right = rightRotate(z.right);
return leftRotate(z);
```

---

## 7. Concrete Problem Examples
* **AVL Insertion (RL Case)**: Inserting into left subtree of right child.
* **AVL Deletion (LR Deletion Effect)**: Deleting from left subtree causes right-heavy RL zigzag imbalance.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Double Right-Left Rotation:

```java
public class RLRotationDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Double Right-Left Rotation (RL Case) Test ===");
        // Build RL Unbalanced Tree: 10 -> 30 -> 20
        RLRotationMaster.AVLNode z = new RLRotationMaster.AVLNode(10);
        z.right = new RLRotationMaster.AVLNode(30, 
            new RLRotationMaster.AVLNode(20), null);
        RLRotationMaster.updateHeight(z);

        System.out.println("Root Value BEFORE Rotation: " + z.val); // Output: 10
        System.out.println("Root Height BEFORE Rotation: " + RLRotationMaster.getHeight(z)); // Output: 3

        RLRotationMaster.AVLNode newRoot = RLRotationMaster.rotateRL(z);

        System.out.println("\nRoot Value AFTER Rotation:  " + newRoot.val);       // Output: 20
        System.out.println("Root Height AFTER Rotation: " + RLRotationMaster.getHeight(newRoot)); // Output: 2
        System.out.println("New Root Left:  " + newRoot.left.val);                // Output: 10
        System.out.println("New Root Right: " + newRoot.right.val);               // Output: 30 ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Time Complexity | Auxiliary Space | Memory Access |
| :--- | :--- | :--- | :--- |
| **`rotateRL(z)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 8 Pointer assignments (2 single rotations) |
| **Height Updates** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 4 Height calculations |

---

## 10. Edge Cases & Boundary Handling
* **Subtrees $T_2, T_3$ Empty**: Handled cleanly by pointer relinking logic inside `rightRotate` and `leftRotate`.
* **Root Subtree Assignment**: Caller MUST capture return value: `node = rotateRL(node)`.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting Single Left Rotation on RL Case**:
  - Applying `leftRotate(Z)` directly on an RL case shifts the left-heavy child $X$ from right to left, leaving the tree unbalanced!
  - **ALWAYS execute `rightRotate(z.right)` FIRST, then `leftRotate(z)` SECOND**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Duality Between LR and RL Double Rotations:
> * **`rotateLR(Z)`**: $\text{BF}(Z) = +2, \text{childBF} < 0 \implies Z.\text{left} = \text{leftRotate}(Z.\text{left})$; return $\text{rightRotate}(Z)$.
> * **`rotateRL(Z)`**: $\text{BF}(Z) = -2, \text{childBF} > 0 \implies Z.\text{right} = \text{rightRotate}(Z.\text{right})$; return $\text{leftRotate}(Z)$.
> Both double rotations execute in **$O(1)$ constant time** and promote the grandchild node $X$ to the root of the subtree!

> **Memory Trick:** **"Opposite BF signs (-2 and +1) signal RL Zigzag requiring Double Rotation!"**

---

## 13. System & Implementation Comparisons

| Feature | Double Right-Left Rotation (`rotateRL`) | Double Left-Right Rotation (`rotateLR`) |
| :--- | :--- | :--- |
| **Imbalance Case** | **RL Case ($\text{BF} = -2, \text{childBF} > 0$)**| LR Case ($\text{BF} = +2, \text{childBF} < 0$) |
| **Rotation Steps** | 2 Single Rotations (`rightRotate` then `leftRotate`)| 2 Single Rotations (`leftRotate` then `rightRotate`) |
| **Promoted Node** | Grandchild $X = Z.\text{right}.\text{left}$ | Grandchild $X = Z.\text{left}.\text{right}$ |

---

## 14. How to Recognize This in Questions
* **"Node has BF = -2 and right child has BF > 0"** $\rightarrow$ Execute Double Right-Left Rotation (`rotateRL`).
* **"Insertion into left subtree of right child causes imbalance"** $\rightarrow$ RL Case.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is RL rotation called a "Double Rotation"?**  
  *A:* Because it executes 2 single rotations sequentially: first `rightRotate(child)`, then `leftRotate(parent)`.
* **Q: Which node becomes the new subtree root after an RL double rotation?**  
  *A:* The grandchild node $X = Z.\text{right}.\text{left}$ is promoted to become the new root of the subtree!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DOUBLE RIGHT-LEFT ROTATION (RL CASE)                  |
+-----------------------------------------------------------------------+
| • Trigger Condition : Node BF = -2 AND Right Child BF > 0 (RL Case)   |
| • Execution Code    : z.right = rightRotate(z.right); return leftRotate(z);|
| • Promoted Node     : Grandchild X = Z.right.left becomes NEW ROOT    |
| • Order Invariant   : In-Order key sequence T1 < Z < T2 < X < T3 < Y < T4 |
| • Complexity        : O(1) Constant Time | O(1) Auxiliary Space ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `rotateRL` from memory in 3 lines.
- [ ] I can state the RL imbalance conditions ($\text{BF} = -2, \text{childBF} > 0$).
- [ ] I know why single rotation fails on zigzag imbalances.
- [ ] I know which node becomes the new root after an RL rotation.
- [ ] I can trace a double RL rotation step by step.
