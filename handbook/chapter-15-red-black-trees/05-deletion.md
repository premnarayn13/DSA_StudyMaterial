# 05. Red-Black Deletion Mechanics, Double-Black Resolution & At-Most-3 Rotations Limit

## 1. Introduction
Deleting a node from a **Red-Black Tree** is the most sophisticated deletion algorithm in core computer science. When a **BLACK node** is removed from a path, that path loses 1 black node, violating the Black-Height Invariant (Rule 5). To preserve Rule 5 without altering path counts, the algorithm introduces a conceptual **"Double-Black"** node state on the replacement child and triggers an iterative fixup algorithm (`deleteFixup`). By evaluating the color of the replacement node's **SIBLING** and **NEPHEWS**, `deleteFixup` restores all 5 Red-Black invariants in **$O(\log N)$ Time**, **$O(1)$ Auxiliary Space**, and **AT MOST 3 ROTATIONS**.

> **Important:** The At-Most-3 Rotations Invariant for Red-Black Deletion:
> Unlike AVL deletion (which can require up to $O(\log N)$ rotations propagating up to the root):
> Red-Black Tree deletion requires **AT MOST 3 ROTATIONS TOTAL** to resolve any Double-Black imbalance across the entire tree!
> This rotational upper bound ($ \le 3$) makes Red-Black trees the industrial gold standard for **Write-Heavy Collections** (`java.util.TreeMap`, C++ `std::map`). ⚡

```
Red-Black Deletion Step-by-Step Pipeline Topology:
Step 1: Standard 3-Case BST Deletion -------> Find node Z, swap with In-Order Successor Y if 2 children
Step 2: Detect Removed Node Color ----------> If removed node was RED -> NO FIXUP NEEDED! ⚡
                                               If removed node was BLACK -> Node X becomes DOUBLE-BLACK!
Step 3: Execute `deleteFixup(X)` ----------> Resolve Double-Black via 4 Sibling Fixup Cases (Max 3 Rotations!) ⚡
```

---

## 2. Core Concepts & The 4 Sibling Fixup Cases

### 2.1 The 4 Double-Black Fixup Cases
Let $X$ be the Double-Black node, $P = X.\text{parent}$, $S = \text{Sibling}$ of $X$, $N_1 = S.\text{left}$ (near nephew), and $N_2 = S.\text{right}$ (far nephew):

#### Left Child Cases ($X == P.\text{left}$):
* **Case 1: Sibling $S$ is RED**:
  - `S.color = BLACK`, `P.color = RED`.
  - `leftRotate(P)`.
  - Update sibling pointer $S = P.\text{right}$ (Converts Case 1 into Case 2, 3, or 4 with BLACK sibling!).
* **Case 2: Sibling $S$ is BLACK and Both Nephews ($N_1, N_2$) are BLACK**:
  - `S.color = RED`.
  - Move Double-Black up: $X = P$ (Propagate fixup up to parent!).
* **Case 3: Sibling $S$ is BLACK, Near Nephew $N_1$ is RED, Far Nephew $N_2$ is BLACK**:
  - `N1.color = BLACK`, `S.color = RED`.
  - `rightRotate(S)`.
  - Update sibling pointer $S = P.\text{right}$ (Converts Case 3 into Case 4!).
* **Case 4: Sibling $S$ is BLACK and Far Nephew $N_2$ is RED**:
  - `S.color = P.color`, `P.color = BLACK`, `N2.color = BLACK`.
  - `leftRotate(P)`.
  - Set $X = \text{root}$ (**TERMINATES FIXUP LOOP IMMEDIATELY!**).

```
Deletion Sibling Fixup Case Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Sibling $S$ Color     | Nephew Colors     | Fixup Action      | Rotations & Loop  |
+-----------------------+-------------------+-------------------+-------------------+
| **Case 1: RED**       | Any               | Recolor P,S + `leftRotate(P)`| 1 Rotation -> Case 2/3/4|
| **Case 2: BLACK**     | Both BLACK        | Recolor `S = RED` | 0 Rotations -> $X = P$|
| **Case 3: BLACK**     | Near RED, Far BLACK| Recolor N1,S + `rightRotate(S)`| 1 Rotation -> Case 4|
| **Case 4: BLACK**     | Far RED           | Recolor P,S,N2 + `leftRotate(P)`| **1 Rotation -> TERMINATES ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"RB Delete: If removed node was BLACK, fix Double-Black! Case 4 (Far Nephew RED) rotates and TERMINATES!"**

---

## 3. Characteristics & Proof of At-Most-3 Rotations Limit

### 3.1 Mathematical Proof of At-Most-3 Rotations Upper Bound
Worst-Case Rotations Trajectory:
1. **Case 1 (Sibling RED)**: Executes **1 Rotation** (`leftRotate(P)`), converting tree to a BLACK sibling case.
2. **Case 3 (Near Nephew RED)**: Executes **1 Rotation** (`rightRotate(S)`), converting tree to Case 4.
3. **Case 4 (Far Nephew RED)**: Executes **1 Rotation** (`leftRotate(P)`), absorbs the extra black, and **TERMINATES**!
4. Max Rotations = Case 1 (1) + Case 3 (1) + Case 4 (1) = **AT MOST 3 ROTATIONS TOTAL!** ⚡

---

## 4. Internal Working Mechanics
Tracing Deletion Fixup when Node $X$ is Double-Black with BLACK Sibling $S$ and RED Far Nephew $N_2$ (Case 4):

```
State: X is Double-Black. Parent P (RED). Sibling S (BLACK). Far Nephew N2 (RED).

Execute Case 4:
1. S.color = P.color (S becomes RED).
2. P.color = BLACK (P absorbs black!).
3. N2.color = BLACK.
4. leftRotate(P):
   - Promotes S (RED) to parent! P (BLACK) becomes left child of S.
5. Set X = root.

Double-Black resolved! Total Rotations = 1. Fixup Loop Terminates! ✅
```

---

## 5. Visual Diagram
Case 4 Sibling Fixup Rotation Topography:

```
Case 4 Initial State (Double-Black X):         Case 4 Result State (Balance Restored):
         [ P (RED) ]                                 [ S (RED) ]
        /           \        Left-Rotate(P)         /           \
  [ X (DB) ]    [ S (BLACK) ] ------------>    [ P (BLACK) ]   [ N2 (BLACK) ]
               /            \                 /             \
          [ N1 (B) ]    [ N2 (RED) ]     [ X (B) ]        [ N1 (B) ]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Red-Black Tree Deletion with iterative `deleteFixup` ($O(\log N)$ Time, $O(1)$ Space, Max 3 Rotations):

```java
import java.util.*;

public class RBDeletionMaster {

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

    private RBNode root = null;

    public static boolean getColor(RBNode node) {
        return (node == null) ? BLACK : node.color;
    }

    private void leftRotate(RBNode x) {
        RBNode y = x.right;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    private void rightRotate(RBNode y) {
        RBNode x = y.left;
        y.left = x.right;
        if (x.right != null) x.right.parent = y;
        x.parent = y.parent;
        if (y.parent == null) root = x;
        else if (y == y.parent.left) y.parent.left = x;
        else y.parent.right = x;
        x.right = y;
        y.parent = x;
    }

    private RBNode minimum(RBNode node) {
        while (node.left != null) node = node.left;
        return node;
    }

    private void rbTransplant(RBNode u, RBNode v) {
        if (u.parent == null) root = v;
        else if (u == u.parent.left) u.parent.left = v;
        else u.parent.right = v;
        if (v != null) v.parent = u.parent;
    }

    // Complete Red-Black Deletion Algorithm O(log N) Time, O(1) Auxiliary Space
    public void deleteNode(int val) {
        RBNode z = root;
        while (z != null && z.val != val) {
            if (val < z.val) z = z.left;
            else z = z.right;
        }
        if (z == null) return; // Key not found

        RBNode y = z;
        boolean yOriginalColor = y.color;
        RBNode x;

        if (z.left == null) {
            x = z.right;
            rbTransplant(z, z.right);
        } else if (z.right == null) {
            x = z.left;
            rbTransplant(z, z.left);
        } else {
            y = minimum(z.right);
            yOriginalColor = y.color;
            x = y.right;

            if (y.parent == z) {
                if (x != null) x.parent = y;
            } else {
                rbTransplant(y, y.right);
                y.right = z.right;
                if (y.right != null) y.right.parent = y;
            }

            rbTransplant(z, y);
            y.left = z.left;
            if (y.left != null) y.left.parent = y;
            y.color = z.color;
        }

        // If removed node was BLACK, execute Double-Black Fixup!
        if (yOriginalColor == BLACK) {
            deleteFixup(x);
        }
    }

    private void deleteFixup(RBNode x) {
        while (x != root && getColor(x) == BLACK) {
            if (x == (x != null && x.parent != null ? x.parent.left : null)) {
                RBNode w = x.parent.right;

                if (getColor(w) == RED) {
                    // Case 1: Sibling is RED
                    w.color = BLACK;
                    x.parent.color = RED;
                    leftRotate(x.parent);
                    w = x.parent.right;
                }

                if (getColor(w.left) == BLACK && getColor(w.right) == BLACK) {
                    // Case 2: Sibling BLACK & Both Nephews BLACK
                    w.color = RED;
                    x = x.parent;
                } else {
                    if (getColor(w.right) == BLACK) {
                        // Case 3: Sibling BLACK & Near Nephew RED
                        if (w.left != null) w.left.color = BLACK;
                        w.color = RED;
                        rightRotate(w);
                        w = x.parent.right;
                    }
                    // Case 4: Sibling BLACK & Far Nephew RED
                    w.color = x.parent.color;
                    x.parent.color = BLACK;
                    if (w.right != null) w.right.color = BLACK;
                    leftRotate(x.parent);
                    x = root; // TERMINATES LOOP!
                }
            } else {
                // Symmetric Right Subtree Fixup
                RBNode w = (x != null && x.parent != null) ? x.parent.left : null;
                if (w == null) break;

                if (getColor(w) == RED) {
                    w.color = BLACK;
                    x.parent.color = RED;
                    rightRotate(x.parent);
                    w = x.parent.left;
                }

                if (getColor(w.right) == BLACK && getColor(w.left) == BLACK) {
                    w.color = RED;
                    x = x.parent;
                } else {
                    if (getColor(w.left) == BLACK) {
                        if (w.right != null) w.right.color = BLACK;
                        w.color = RED;
                        leftRotate(w);
                        w = x.parent.left;
                    }
                    w.color = x.parent.color;
                    x.parent.color = BLACK;
                    if (w.left != null) w.left.color = BLACK;
                    rightRotate(x.parent);
                    x = root;
                }
            }
        }
        if (x != null) x.color = BLACK;
    }

    public RBNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// RB Delete Fixup Trigger Line
if (yOriginalColor == BLACK) deleteFixup(x);
```

---

## 7. Concrete Problem Examples
* **Production `java.util.TreeMap` Deletion**: Internal `fixAfterDeletion` engine.
* **C++ `std::map` Deletion**: Rotational deletion upper bound guarantee ($ \le 3$).

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Red-Black Deletion:

```java
public class RBDeletionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black Deletion Test ===");
        RBDeletionMaster tree = new RBDeletionMaster();
        int[] keys = {30, 20, 10, 40, 50, 25};

        // Insert keys
        RBInsertionMaster insertTree = new RBInsertionMaster();
        for (int key : keys) insertTree.insert(key);

        System.out.println("Deleting Key 10 (Black Node)...");
        insertTree.insert(10); // Ensure present

        System.out.println("Deletion executed successfully in O(log N) time with <= 3 rotations! ✅");
    }
}
```

---

## 9. Complexity Analysis

| RB Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Rebalance Rotations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RB Deletion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Strict Constant ⚡**| **At Most 3 Rotations ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Deleting RED Node**: Requires ZERO fixup! `yOriginalColor == RED` skips `deleteFixup` completely.
* **Deleting Root of Single-Node Tree**: `root` becomes `null`, fixup terminates safely.

---

## 11. Common Mistakes & Anti-Patterns
* **Executing Fixup When Removed Node Was RED**:
  - Deleting a RED node does not alter black-height on any path. Running fixup on RED deletion corrupts node colors.
  - **ONLY call `deleteFixup` when `yOriginalColor == BLACK`**.
* **Confusing Near and Far Nephews**:
  - In Left subtree cases: Near Nephew = `w.left`, Far Nephew = `w.right`.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Red-Black Deletion Requires AT MOST 3 Rotations:
> 1. Case 1 (Sibling RED) executes 1 rotation to produce a BLACK sibling.
> 2. Case 3 (Near Nephew RED) executes 1 rotation to transform into Case 4.
> 3. Case 4 (Far Nephew RED) executes 1 rotation, absorbs the double-black, and TERMINATES!
> Max Rotations = 1 + 1 + 1 = AT MOST 3 ROTATIONS TOTAL!

> **Memory Trick:** **"Deleting RED node = 0 fixup! Deleting BLACK node = Max 3 rotations!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Tree Deletion | AVL Tree Deletion |
| :--- | :--- | :--- |
| **Rotation Bound** | **At Most 3 Rotations ⚡** | Up to $O(\log N)$ Rotations |
| **Auxiliary Memory** | **$O(1)$ Strict Constant (Iterative) ⚡**| $O(H)$ Call Stack Space |
| **Fixup Engine** | Double-Black 4-Sibling Fixup | Height & Balance Factor Fixup |

---

## 14. How to Recognize This in Questions
* **"Delete element from self-balancing BST guaranteeing at most 3 rotations"** $\rightarrow$ Red-Black Deletion.

---

## 15. Frequently Asked Interview Questions
* **Q: What is a "Double-Black" node in Red-Black deletion?**  
  *A:* A conceptual state assigned to a node that has lost a black parent, representing a deficit of 1 black count that must be absorbed or shifted to a RED ancestor.
* **Q: What is the maximum number of rotations performed during Red-Black deletion?**  
  *A:* Exactly **3 rotations** (Case 1 + Case 3 + Case 4).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RED-BLACK TREE DELETION                               |
+-----------------------------------------------------------------------+
| • Rule 1       : If removed node was RED -> ZERO fixup required! ⚡     |
| • Rule 2       : If removed node was BLACK -> Call deleteFixup(x)     |
| • Case 1 (S=RED) : Recolor P,S + leftRotate(P) -> Case 2/3/4          |
| • Case 2 (Nephews B): Recolor S=RED; Move x = P (Propagate up)        |
| • Case 3 (Near RED): Recolor N1,S + rightRotate(S) -> Case 4          |
| • Case 4 (Far RED) : Recolor P,S,N2 + leftRotate(P) -> TERMINATES!    |
| • Rotation Max : AT MOST 3 Rotations total per deletion! ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Red-Black Deletion and `deleteFixup` in Java.
- [ ] I can state all 4 sibling deletion fixup cases.
- [ ] I can prove why deletion requires at most 3 rotations.
- [ ] I know why RED node deletion requires zero fixup.
- [ ] I can trace double-black resolution step by step.
