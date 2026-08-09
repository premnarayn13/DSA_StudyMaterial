# 04. Red-Black Insertion Mechanics, 3 Fixup Cases & At-Most-2 Rotations Limit

## 1. Introduction
Inserting a node into a **Red-Black Tree** combines standard BST leaf insertion (with the new node ALWAYS colored **RED**) with an iterative fixup algorithm (`insertFixup`) to resolve Double-RED (Rule 4) violations. By analyzing the color of the new node's **UNCLE** (parent's sibling), the insertion fixup algorithm restores all 5 Red-Black invariants in **$O(\log N)$ Time**, **$O(1)$ Auxiliary Space**, and **AT MOST 2 ROTATIONS**.

> **Important:** The At-Most-2 Rotations Invariant for Red-Black Insertion:
> While recoloring (Case 1) can propagate up the tree up to $O(\log N)$ times:
> Once an Uncle BLACK case (Case 2 or Case 3) is encountered, performing **AT MOST 2 ROTATIONS** restores global Red-Black invariants and IMMEDIATELY TERMINATES the insertion algorithm!
> Thus, Red-Black insertion executes **At Most 2 Rotations** total! ⚡

```
Red-Black Insertion Fixup 3-Case Decision Matrix:
Case 1: Uncle is RED              Case 2: Uncle is BLACK (Zigzag)   Case 3: Uncle is BLACK (Straight Line)
Recolor Parent & Uncle to BLACK   Rotate Parent (convert to Case 3) Rotate Grandparent & Swap Colors!
Recolor Grandparent to RED        --------------------------------> Immediately Restores All Rules!
Push violation up to Grandparent                                    TERMINATES FIXUP LOOP! ⚡
```

---

## 2. Core Concepts & The 3 Insertion Fixup Cases

### 2.1 The Complete Insertion Fixup Algorithm
New node $K$ is inserted as **RED**. While $K \ne \text{root}$ and $K.\text{parent}.\text{color} == \text{RED}$ (Double-RED violation!):

Let $P = K.\text{parent}$, $G = P.\text{parent}$, and $U = \text{Uncle}$ (sibling of $P$):

#### Left Subtree Cases ($P == G.\text{left}$):
* **Case 1: Uncle $U$ is RED**:
  - `P.color = BLACK`, `U.color = BLACK`, `G.color = RED`.
  - Move $K = G$ (Propagate check up to Grandparent!).
* **Case 2: Uncle $U$ is BLACK and $K$ is Right Child ($K == P.\text{right}$ - Zigzag)**:
  - Move $K = P$.
  - `leftRotate(K)` (Converts Case 2 into Case 3 straight line!).
* **Case 3: Uncle $U$ is BLACK and $K$ is Left Child ($K == P.\text{left}$ - Straight Line)**:
  - `P.color = BLACK`, `G.color = RED`.
  - `rightRotate(G)` (Restores balance completely!).
  - **Loop Terminates!**

(Right Subtree Cases $P == G.\text{right}$ are symmetric duals!).
Finally, enforce Rule 2: **`root.color = BLACK`**!

```
Insertion Fixup Case Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Uncle Color           | Node Configuration| Fixup Action      | Loop Continuance  |
+-----------------------+-------------------+-------------------+-------------------+
| **Uncle is RED**      | Any               | Recolor P, U, G   | Propagate $K = G$ |
| **Uncle is BLACK**    | Zigzag ($K=P.\text{right}$)| `leftRotate(P)`   | Fallthrough Case 3|
| **Uncle is BLACK**    | Line ($K=P.\text{left}$)| Recolor + `rightRotate(G)`| **TERMINATES ⚡**  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Uncle RED: Recolor P, U, G and propagate up! Uncle BLACK: Rotate and TERMINATE in at most 2 rotations!"**

---

## 3. Characteristics & Proof of At-Most-2 Rotations Limit

### 3.1 Mathematical Proof of At-Most-2 Rotations Upper Bound
* **Case 1 (Uncle RED)**: Performs ZERO rotations. Only recolors $P, U, G$ and propagates $K = G$ up 2 levels.
* **Case 2 (Uncle BLACK Zigzag)**: Performs **1 Rotation** (`leftRotate(P)`), transforming the zigzag into Case 3.
* **Case 3 (Uncle BLACK Line)**: Performs **1 Rotation** (`rightRotate(G)`), restores all rules, and terminates the loop.
* Max Rotations = Case 2 (1 rotation) + Case 3 (1 rotation) = **AT MOST 2 ROTATIONS TOTAL!** ⚡

---

## 4. Internal Working Mechanics
Tracing Insertion of key 10 into Red-Black Tree `[30 (B), 20 (R)]`:

```
Insert 10 as RED under 20 (RED). Double-RED conflict between 10 and 20!

- Node K = 10 (RED). Parent P = 20 (RED). Grandparent G = 30 (BLACK).
- Uncle U = G.right = null (NIL is BLACK!).
- Uncle U is BLACK! K = 10 is Left Child of P = 20 (Straight Line -> Case 3!).

Execute Case 3:
1. Recolor P (20) to BLACK.
2. Recolor G (30) to RED.
3. rightRotate(G=30):
   - Promotes 20 to Root (BLACK)! 20.left = 10 (RED), 20.right = 30 (RED).

Loop terminates! 1 Rotation performed! Total Black-Height = 2. All 5 Rules Satisfied! ✅
```

---

## 5. Visual Diagram
Case 1 Recoloring vs Case 3 Rotation Topography:

```
Case 1 (Uncle RED -> Recolor):               Case 3 (Uncle BLACK -> Rotate & Recolor):
        [ G (BLACK) ]                                [ G (BLACK) ]
       /             \                              /             \
  [ P (RED) ]     [ U (RED) ]                  [ P (RED) ]     [ U (BLACK) ]
     /                                            /
[ K (RED) ]                                  [ K (RED) ]
    |                                             |
Recolor P, U to BLACK; G to RED!             P to BLACK, G to RED; rightRotate(G)! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Red-Black Tree Insertion with iterative `insertFixup` ($O(\log N)$ Time, $O(1)$ Space):

```java
import java.util.*;

public class RBInsertionMaster {

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

    // Complete Red-Black Insertion O(log N) Time, O(1) Auxiliary Space
    public void insert(int val) {
        RBNode z = new RBNode(val);
        RBNode y = null;
        RBNode x = root;

        // Step 1: Standard Iterative BST Leaf Insertion
        while (x != null) {
            y = x;
            if (z.val < x.val) x = x.left;
            else if (z.val > x.val) x = x.right;
            else return; // Duplicate ignored
        }

        z.parent = y;
        if (y == null) root = z;
        else if (z.val < y.val) y.left = z;
        else y.right = z;

        // Step 2: Fixup Red-Black Invariant Violations
        insertFixup(z);
    }

    private void insertFixup(RBNode k) {
        while (k.parent != null && k.parent.color == RED) {
            if (k.parent == k.parent.parent.left) {
                RBNode uncle = k.parent.parent.right;

                if (getColor(uncle) == RED) {
                    // Case 1: Uncle is RED -> Recolor and propagate up
                    k.parent.color = BLACK;
                    uncle.color = BLACK;
                    k.parent.parent.color = RED;
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.right) {
                        // Case 2: Uncle BLACK & Zigzag -> Left rotate parent
                        k = k.parent;
                        leftRotate(k);
                    }
                    // Case 3: Uncle BLACK & Line -> Right rotate grandparent
                    k.parent.color = BLACK;
                    k.parent.parent.color = RED;
                    rightRotate(k.parent.parent);
                }
            } else {
                // Symmetric Right Subtree Cases
                RBNode uncle = k.parent.parent.left;

                if (getColor(uncle) == RED) {
                    k.parent.color = BLACK;
                    uncle.color = BLACK;
                    k.parent.parent.color = RED;
                    k = k.parent.parent;
                } else {
                    if (k == k.parent.left) {
                        k = k.parent;
                        rightRotate(k);
                    }
                    k.parent.color = BLACK;
                    k.parent.parent.color = RED;
                    leftRotate(k.parent.parent);
                }
            }
        }
        root.color = BLACK; // Rule 2: Root is ALWAYS BLACK!
    }

    public RBNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// RB Insert Fixup Case 1 Block
k.parent.color = BLACK; uncle.color = BLACK; k.parent.parent.color = RED; k = k.parent.parent;
```

---

## 7. Concrete Problem Examples
* **Production `java.util.TreeMap` Insertion**: Internal `fixAfterInsertion` engine.
* **Linux Kernel CFS Scheduler**: Inserting executable tasks into `rbtree`.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Red-Black Insertion:

```java
public class RBInsertionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black Insertion Test ===");
        RBInsertionMaster tree = new RBInsertionMaster();
        int[] keys = {30, 20, 10, 40, 50, 25};

        for (int key : keys) {
            tree.insert(key);
        }

        RBInsertionMaster.RBNode root = tree.getRoot();
        System.out.println("Root Value: " + root.val); // Output: 20 (Balanced Root!)
        System.out.println("Root Color: " + (root.color == RBInsertionMaster.BLACK ? "BLACK" : "RED"));
        System.out.println("Root Left:  " + root.left.val + " (Color: " + 
            (root.left.color == RBInsertionMaster.BLACK ? "BLACK" : "RED") + ")"); // 10 (BLACK)
        System.out.println("Root Right: " + root.right.val + " (Color: " + 
            (root.right.color == RBInsertionMaster.BLACK ? "BLACK" : "RED") + ")"); // 40 (RED) ✅
    }
}
```

---

## 9. Complexity Analysis

| RB Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Rebalance Rotations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **RB Insertion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Strict Constant ⚡**| **At Most 2 Rotations ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Inserting First Node into Empty Tree**: Set to BLACK immediately by `root.color = BLACK`.
* **Uncle is Null (NIL Leaf)**: `getColor(null)` returns BLACK, directing execution cleanly into Case 2 / Case 3.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `root.color = BLACK` at End of Fixup**:
  - Case 1 recoloring can color the root RED.
  - **ALWAYS execute `root.color = BLACK` at the end of `insertFixup`**.
* **Re-assigning $K = K.\text{parent}$ BEFORE Rotation in Case 2**:
  - Forgetting `k = k.parent` before calling `leftRotate(k)` rotates the wrong node.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** The At-Most-2 Rotations Guarantee:
> 1. Case 1 (Uncle RED) recolors nodes and moves up, performing 0 rotations.
> 2. Case 2 (Uncle BLACK Zigzag) performs 1 rotation to convert into Case 3.
> 3. Case 3 (Uncle BLACK Line) performs 1 rotation, restores all rules, and terminates!
> Total Rotations = At Most 2 Rotations per Insertion!

> **Memory Trick:** **"Uncle RED = Recolor & propagate up! Uncle BLACK = Rotate & TERMINATE!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Tree Insertion | AVL Tree Insertion |
| :--- | :--- | :--- |
| **Auxiliary Memory** | **$O(1)$ Strict Constant (Iterative) ⚡**| $O(H)$ Call Stack Space |
| **Rotation Bound** | **At Most 2 Rotations ⚡** | **At Most 1 Rotation ⚡** |
| **Fixup Mechanism**| Uncle color check (Recolor / Rotate) | Height & Balance Factor check |

---

## 14. How to Recognize This in Questions
* **"Insert element into self-balancing BST with O(1) space and at most 2 rotations"** $\rightarrow$ Red-Black Insertion.

---

## 15. Frequently Asked Interview Questions
* **Q: Why are new nodes inserted as RED?**  
  *A:* Inserting RED nodes satisfies Rule 5 (equal black height across all paths) automatically, risking only Rule 4 (double-RED conflict), which is fast to resolve.
* **Q: What is the maximum number of rotations during Red-Black insertion?**  
  *A:* Exactly **2 rotations** (Case 2 single rotation + Case 3 single rotation).

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RED-BLACK TREE INSERTION                              |
+-----------------------------------------------------------------------+
| • New Nodes   : Always inserted as RED                                |
| • Case 1      : Uncle is RED -> Recolor P, U to BLACK; G to RED; k = G|
| • Case 2      : Uncle BLACK (Zigzag) -> k = P; leftRotate(k) -> Case 3|
| • Case 3      : Uncle BLACK (Line) -> P to BLACK, G to RED; rightRotate(G)|
| • Final Step  : ALWAYS enforce root.color = BLACK                     |
| • Rotation Max: AT MOST 2 Rotations total per insertion! ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Red-Black Insertion and `insertFixup` in Java.
- [ ] I can state all 3 insertion fixup cases.
- [ ] I can prove why insertion requires at most 2 rotations.
- [ ] I know why `root.color = BLACK` is required at the end.
- [ ] I can trace multi-element Red-Black insertions step by step.
