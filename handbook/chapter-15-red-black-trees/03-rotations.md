# 03. Parent-Pointer Tree Rotations, Relinking Equations & Color Maintenance

## 1. Introduction
Tree Rotations in a **Red-Black Tree**—specifically **Left Rotation (`leftRotate`)** and **Right Rotation (`rightRotate`)**—are local $O(1)$ structural re-linking operations that alter parent-child pointer topologies while strictly preserving the BST sorted key ordering ($L < Root < R$). Unlike standard BST rotations, Red-Black tree rotations maintain explicit 3-way parent pointer linkage (`node.parent`, `child.parent`, `grandparent.left/right`), executing in **$O(1)$ Strict Constant Time and Auxiliary Space**.

> **Important:** The 6 Explicit Pointer Assignments of a Red-Black Parent-Pointer Rotation:
> Standard recursive BST rotations only update child links (`root.left = ...`).
> In a Red-Black Tree, every node tracks a `parent` pointer. Rotating node $X$ with child $Y$ requires updating **6 explicit pointer links**:
> 1. `Y.left/right` $\to$ set to $X$.
> 2. `X.parent` $\to$ set to $Y$.
> 3. `T2.parent` (if $T_2 \ne \text{null}$) $\to$ set to $X$.
> 4. `X.left/right` $\to$ set to $T_2$.
> 5. `Y.parent` $\to$ set to $X.\text{parent}$.
> 6. `X.parent.left/right` (or `root`) $\to$ set to $Y$! ⚡

```
Red-Black Parent-Pointer Left Rotation Topology:
        Parent (P)                                  Parent (P)
            |                                           |
       Node X (BLACK)                                 Node Y (RED)
      /              \          Left Rotate(X)       /            \
    [T1]            Node Y    ---------------->    Node X         [T3]
                   /      \                       /      \
                 [T2]     [T3]                  [T1]     [T2]

All parent pointers (X.parent, Y.parent, T2.parent) updated in O(1) time! ⚡
```

---

## 2. Core Concepts & Parent-Pointer Pointer Relinking Algorithms

### 2.1 The `leftRotate(x)` Algorithm ($O(1)$ Space)
Given node $X$ and right child $Y = X.\text{right}$:
1. Identify $T_2 = Y.\text{left}$.
2. Link $T_2$ as $X$'s right child: `x.right = T2`. If `T2 != null`, `T2.parent = x`.
3. Link $X$'s parent to $Y$: `y.parent = x.parent`.
4. Update parent's child link:
   - If `x.parent == null`: `root = y`.
   - Else if `x == x.parent.left`: `x.parent.left = y`.
   - Else: `x.parent.right = y`.
5. Link $X$ as $Y$'s left child: `y.left = x`; `x.parent = y`.

```
Left Rotate vs Right Rotate Pointer Summary:
+-----------------------+-------------------+-------------------+
| Pointer Assignment    | `leftRotate(x)`   | `rightRotate(y)`  |
+-----------------------+-------------------+-------------------+
| Promoted Node         | $Y = X.\text{right}$| $X = Y.\text{left}$ |
| Orphaned Subtree      | $T_2 = Y.\text{left}$| $T_2 = X.\text{right}$|
| Re-attached Subtree   | `x.right = T2`    | `y.left = T2`     |
| Parent Relinking      | `y.parent = x.parent`| `x.parent = y.parent`|
+-----------------------+-------------------+-------------------+
```

> **Memory Trick:** **"RB Rotations: Always update 3 parent pointers (T2.parent, Y.parent, X.parent) in addition to child links!"**

---

## 3. Characteristics & Color Neutrality

### 3.1 Structural Rotations Are Color Neutral
* A rotation alters **ONLY POINTER TOPOLOGY**; it DOES NOT alter node colors!
* Node recoloring is performed separately before or after rotation to fix Rule 4 (Double-RED) or Rule 5 (Black-Height) violations.

---

## 4. Internal Working Mechanics
Tracing `leftRotate(X=10)` with $Y=20$ and parent $P=5$:

```
Initial Topology: 5.right = 10. 10.right = 20. 20.left = 15.

Step 1: Save T2 = 15.
Step 2: Set 10.right = 15. Set 15.parent = 10.
Step 3: Set 20.parent = 5.
Step 4: Set 5.right = 20 (Parent 5 now points to 20!).
Step 5: Set 20.left = 10. Set 10.parent = 20.

All 6 pointer links updated in O(1) time! New Subtree Root = 20! ✅
```

---

## 5. Visual Diagram
RB Parent-Pointer Relinking Topography:

```
BEFORE ROTATION:                            AFTER LEFT ROTATION:
       [ Parent P ]                                [ Parent P ]
           |                                           |
       [ Node X ]                                  [ Node Y ]
      /          \                                /          \
   [T1]        [ Node Y ]                    [ Node X ]      [T3]
              /          \                  /          \
           [T2]          [T3]            [T1]          [T2]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Red-Black Tree Parent-Pointer Rotations (`leftRotate` and `rightRotate`):

```java
import java.util.*;

public class RBRotationsMaster {

    public static final boolean RED = false;
    public static final boolean BLACK = true;

    public static class RBNode {
        public int val;
        public boolean color;
        public RBNode left;
        public RBNode right;
        public RBNode parent;

        public RBNode(int val) {
            this.val = val;
            this.color = RED;
        }
    }

    public static RBNode root = null;

    // 1. Left Rotate Node X O(1) Time, O(1) Space
    public static void leftRotate(RBNode x) {
        RBNode y = x.right;
        x.right = y.left; // Transfer T2 subtree

        if (y.left != null) {
            y.left.parent = x; // Update T2 parent link
        }

        y.parent = x.parent; // Link Y to X's parent

        if (x.parent == null) {
            root = y; // X was root, Y becomes new root
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }

        y.left = x; // Place X as Y's left child
        x.parent = y; // Update X's parent link
    }

    // 2. Right Rotate Node Y O(1) Time, O(1) Space
    public static void rightRotate(RBNode y) {
        RBNode x = y.left;
        y.left = x.right; // Transfer T2 subtree

        if (x.right != null) {
            x.right.parent = y; // Update T2 parent link
        }

        x.parent = y.parent; // Link X to Y's parent

        if (y.parent == null) {
            root = x; // Y was root, X becomes new root
        } else if (y == y.parent.left) {
            y.parent.left = x;
        } else {
            y.parent.right = x;
        }

        x.right = y; // Place Y as X's right child
        y.parent = x; // Update Y's parent link
    }
}
```

> **Quick Syntax:**
```java
// RB Left Rotate Core Line
RBNode y = x.right; x.right = y.left; if (y.left != null) y.left.parent = x;
y.parent = x.parent; if (x.parent == null) root = y; else if (x == x.parent.left) x.parent.left = y; else x.parent.right = y;
y.left = x; x.parent = y;
```

---

## 7. Concrete Problem Examples
* **Red-Black Insertion Balancing**: Rotations during double-RED resolution.
* **Red-Black Deletion Balancing**: Rotations during double-BLACK resolution.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Left Rotate and Right Rotate with explicit parent checking:

```java
public class RBRotationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black Parent-Pointer Left Rotate Test ===");
        // Build 10 -> 20 (right) with parent 5
        RBRotationsMaster.RBNode p = new RBRotationsMaster.RBNode(5);
        RBRotationsMaster.RBNode x = new RBRotationsMaster.RBNode(10);
        RBRotationsMaster.RBNode y = new RBRotationsMaster.RBNode(20);

        p.right = x; x.parent = p;
        x.right = y; y.parent = x;
        RBRotationsMaster.root = p;

        System.out.println("Parent's Right BEFORE Rotate: " + p.right.val); // Output: 10

        RBRotationsMaster.leftRotate(x);

        System.out.println("Parent's Right AFTER Rotate:  " + p.right.val); // Output: 20
        System.out.println("Y's Left Child:              " + y.left.val);  // Output: 10
        System.out.println("X's New Parent:              " + x.parent.val); // Output: 20 ✅
    }
}
```

---

## 9. Complexity Analysis

| Rotation Operation | Time Complexity | Auxiliary Space | Memory Access |
| :--- | :--- | :--- | :--- |
| **`leftRotate(x)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 6 Pointer assignments |
| **`rightRotate(y)`**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | 6 Pointer assignments |

---

## 10. Edge Cases & Boundary Handling
* **Rotating Root Node (`x.parent == null`)**: Handled by setting `root = y`.
* **Orphaned Subtree $T_2$ is Null**: Guarded by `if (y.left != null) y.left.parent = x`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Update `T2.parent`**:
  - Re-linking `x.right = y.left` without updating `y.left.parent = x` leaves $T_2$ pointing to old parent $Y$, corrupting bottom-up tree traversals!
  - **ALWAYS check `if (y.left != null) y.left.parent = x`**.
* **Forgetting to Update Parent's Child Link**:
  - Updating `y.parent = x.parent` without updating `x.parent.left = y` or `x.parent.right = y` leaves parent $P$ pointing to old child $X$.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Parent Pointers are Mandatory in Red-Black Trees:
> Standard BST rotations return the new root to be captured recursively down call stacks.
> Production Red-Black trees (e.g. `java.util.TreeMap`) use **ITERATIVE REBALANCING** to achieve $O(1)$ auxiliary space.
> Explicit `parent` pointers allow iterative code to walk up the tree without call stack frames!

> **Memory Trick:** **"Check 3 null guards: y.left != null, x.parent == null, x == x.parent.left!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Parent-Pointer Rotation | Standard Recursive Rotation |
| :--- | :--- | :--- |
| **Pointer Updates** | **6 Explicit Pointer Links ⚡** | 2 Pointer Links |
| **Auxiliary Memory** | **$O(1)$ Strict Constant ⚡** | $O(H)$ Call Stack Space |
| **Parent Field** | `node.parent` Reference | No Parent Field |

---

## 14. How to Recognize This in Questions
* **"Perform O(1) rotation in parent-pointer augmented BST"** $\rightarrow$ RB Left / Right Rotate.

---

## 15. Frequently Asked Interview Questions
* **Q: How many pointer assignments are performed in a parent-pointer Red-Black rotation?**  
  *A:* Exactly **6 pointer assignments** (`x.right`, `T2.parent`, `y.parent`, `x.parent.left/right`, `y.left`, `x.parent`).
* **Q: Does a rotation change the color of any node?**  
  *A:* No! Rotations alter only structural pointers. Colors are modified separately during recoloring phases.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RED-BLACK PARENT-POINTER ROTATIONS                    |
+-----------------------------------------------------------------------+
| • Left Rotate X : y = x.right; x.right = y.left; if (y.left) y.left.parent = x;|
|                   y.parent = x.parent; relink x.parent to y; y.left = x; x.parent = y|
| • Right Rotate Y: x = y.left; y.left = x.right; if (x.right) x.right.parent = y;|
|                   x.parent = y.parent; relink y.parent to x; x.right = y; y.parent = x|
| • Space Bounds  : O(1) Constant Time | O(1) Auxiliary Space ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `leftRotate` with parent pointers from memory.
- [ ] I can write `rightRotate` with parent pointers from memory.
- [ ] I know all 6 pointer assignments required for parent-pointer rotations.
- [ ] I know why $T_2$ null checking is mandatory.
- [ ] I can trace parent link updates step by step.
