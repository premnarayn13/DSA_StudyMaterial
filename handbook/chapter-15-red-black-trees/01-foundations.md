# 01. Red-Black Tree Foundations, Structural Invariants & Black-Height Topology

## 1. Introduction
A **Red-Black Tree** is a self-balancing Binary Search Tree augmented with an extra 1-bit color attribute (`RED` or `BLACK`) on every node. Invented by Rudolf Bayer in 1972 (originally named "Symmetric Binary B-Trees") and refined by Leo J. Guibas and Robert Sedgewick in 1978, Red-Black Trees enforce a set of 5 strict color invariant rules. These rules bound the maximum path length from root to any leaf to at most **$2 \log_2(N + 1)$**, guaranteeing **$O(\log N)$ Worst-Case Operations** for search, insertion, and deletion while requiring **AT MOST 2-3 rotations per write operation**.

> **Important:** The Core Invariant & Mathematical Guarantee of Red-Black Trees:
> 1. **Looser Height Bound**: Maximum height $H \le 2 \log_2(N + 1)$, allowing slightly looser height balance than AVL trees ($H \le 1.44 \log_2 N$).
> 2. **Rotation Superiority for Writes**: While AVL deletion can trigger up to $O(\log N)$ rotations, Red-Black insertion requires **AT MOST 2 rotations** and Red-Black deletion requires **AT MOST 3 rotations**! This makes Red-Black trees the undisputed industrial standard for **Write-Heavy Collections** (`java.util.TreeMap`, `java.util.TreeSet`, C++ `std::map`, Linux kernel `rbtree`). ⚡

```
Red-Black Tree Structural Topology:
                      [ 30 (BLACK) ]  <--- Root Node (Rule 2: Root is always BLACK!)
                     /              \
         [ 20 (RED) ]                [ 40 (RED) ]  (Rule 3: No two consecutive RED nodes!)
        /            \              /            \
 [ 10 (BLACK) ]  [ 25 (BLACK) ] [ 35 (BLACK) ] [ 50 (BLACK) ]

Black-Height Invariant: Every path from Root to Null Leaf contains EXACTLY 2 BLACK nodes! ⚡
```

---

## 2. Core Concepts & `RBNode` Structural Definition

### 2.1 The `RBNode` Structure
Each node in a Red-Black Tree contains a boolean `color` flag (`RED = false`, `BLACK = true`):

```java
public class RBNode {
    public static final boolean RED = false;
    public static final boolean BLACK = true;

    public int val;
    public boolean color; // Node color flag
    public RBNode left;
    public RBNode right;
    public RBNode parent; // Explicit Parent pointer required for recoloring & rotations

    public RBNode(int val) {
        this.val = val;
        this.color = RED; // New nodes are ALWAYS inserted as RED!
        this.left = null;
        this.right = null;
        this.parent = null;
    }
}
```

```
Red-Black Tree Structural Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Structural Attribute  | Red-Black Tree    | AVL Tree          | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+
| **Maximum Height**    | $H \le 2.0 \log_2 N$| $H \le 1.44 \log_2 N$| Looser balance    |
| **Insert Rotations**  | **At Most 2 ⚡**  | At Most 1         | Fewer write edits |
| **Delete Rotations**  | **At Most 3 ⚡**  | Up to $O(\log N)$ | **Fastest Writes ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Red-Black Trees: New nodes are inserted RED! Delete requires AT MOST 3 rotations!"**

---

## 3. Characteristics & 2-3-4 Tree Equivalence

### 3.1 Equivalence to 2-3-4 B-Trees
A Red-Black Tree is an isometry of a **2-3-4 B-Tree**:
* A **BLACK node** combined with its **RED children** forms a single 2-3-4 tree node:
  - 2-Node: 1 Black node with 0 Red children.
  - 3-Node: 1 Black node with 1 Red child.
  - 4-Node: 1 Black node with 2 Red children.
* Color recoloring operations correspond directly to **B-Tree node splits and merges**!

---

## 4. Internal Working Mechanics
Tracing Black-Height evaluation across a Red-Black Tree:

```
Tree Topology: Root 30 (BLACK). Left 20 (RED, children 10 BLACK, 25 BLACK). Right 40 (BLACK).

Black-Height Paths from Root 30:
1. Path 30 -> 20 -> 10 -> NIL : Nodes (30 B, 10 B, NIL B) -> Black-Height = 3.
2. Path 30 -> 20 -> 25 -> NIL : Nodes (30 B, 25 B, NIL B) -> Black-Height = 3.
3. Path 30 -> 40 -> NIL        : Nodes (30 B, 40 B, NIL B) -> Black-Height = 3.

All paths contain identical Black-Height = 3! Black-Height Invariant Satisfied! ✅
```

---

## 5. Visual Diagram
2-3-4 Tree to Red-Black Tree Isometry Topography:

```
2-3-4 Tree 4-Node [10 | 20 | 30]:           Equivalent Red-Black Subtree:
     +-----------------+                               (20 BLACK)
     |  10 | 20 | 30   |                              /          \
     +-----------------+                     (10 RED)            (30 RED)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Red-Black Node definition, Black-Height calculation, and Invariant verification:

```java
import java.util.*;

public class RBFoundationsMaster {

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

        public RBNode(int val, boolean color) {
            this.val = val;
            this.color = color;
        }
    }

    // Safely get color of node (Null NIL leaf is always BLACK)
    public static boolean getColor(RBNode node) {
        return (node == null) ? BLACK : node.color;
    }

    // Calculate Black-Height along leftmost path O(log N) Time
    public static int getBlackHeight(RBNode root) {
        int blackCount = 0;
        RBNode curr = root;
        while (curr != null) {
            if (getColor(curr) == BLACK) {
                blackCount++;
            }
            curr = curr.left;
        }
        return blackCount;
    }

    // Verify Black-Height Uniformity Invariant O(N) Time
    public static boolean verifyBlackHeightInvariant(RBNode root) {
        return checkBlackHeight(root) != -1;
    }

    private static int checkBlackHeight(RBNode node) {
        if (node == null) return 1; // NIL leaf is BLACK (count = 1)

        int leftBH = checkBlackHeight(node.left);
        if (leftBH == -1) return -1;

        int rightBH = checkBlackHeight(node.right);
        if (rightBH == -1) return -1;

        // Verify black-heights match across left and right subtrees
        if (leftBH != rightBH) {
            return -1; // Black-Height Invariant Violation!
        }

        return leftBH + (node.color == BLACK ? 1 : 0);
    }
}
```

> **Quick Syntax:**
```java
// Color Helper Line (NIL is BLACK)
public static boolean getColor(RBNode node) { return (node == null) ? BLACK : node.color; }
```

---

## 7. Concrete Problem Examples
* **`java.util.TreeMap` / `TreeSet`**: Red-Black Tree production collections.
* **Linux Kernel Completely Fair Scheduler (CFS)**: `rbtree` task scheduling.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Red-Black Node color inspection and Black-Height verification:

```java
public class RBFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black Tree Foundations Test ===");
        // Build Valid Red-Black Subtree:
        //       30 (BLACK)
        //      /          \
        //   20 (RED)     40 (BLACK)
        //   /      \
        // 10 (B)  25 (B)
        RBFoundationsMaster.RBNode root = 
            new RBFoundationsMaster.RBNode(30, RBFoundationsMaster.BLACK);
        root.left = new RBFoundationsMaster.RBNode(20, RBFoundationsMaster.RED);
        root.right = new RBFoundationsMaster.RBNode(40, RBFoundationsMaster.BLACK);

        root.left.left = new RBFoundationsMaster.RBNode(10, RBFoundationsMaster.BLACK);
        root.left.right = new RBFoundationsMaster.RBNode(25, RBFoundationsMaster.BLACK);

        System.out.println("Root Color: " + 
            (RBFoundationsMaster.getColor(root) == RBFoundationsMaster.BLACK ? "BLACK" : "RED"));

        System.out.println("Is Black-Height Invariant Valid? " + 
            RBFoundationsMaster.verifyBlackHeightInvariant(root)); // Output: true ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Property | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Search Lookup** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space |
| **Color Check `getColor`**| **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | $O(1)$ Auxiliary Space |
| **Black-Height Verify**| **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Null Node (NIL Leaf)**: Defined as BLACK by convention.
* **Root Node**: Must ALWAYS be BLACK.

---

## 11. Common Mistakes & Anti-Patterns
* **Treating Null Pointers as RED**:
  - Null pointers represent sentinel NIL leaves and are strictly defined as **BLACK**.
  - **Always return `BLACK` for null nodes in `getColor(node)`**.
* **Inserting New Nodes as BLACK**:
  - Inserting a new BLACK node immediately violates Rule 5 (Black-Height invariant) for that path.
  - **New nodes are ALWAYS inserted as RED**!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Red-Black Trees are Preferred for Production Collections:
> Red-Black trees trade slightly looser height bounds ($2.0 \log_2 N$) for **DRASTICALLY FASTER WRITE OPERATIONS**.
> AVL tree deletion requires up to $O(\log N)$ rotations, while Red-Black tree deletion requires **AT MOST 3 ROTATIONS**.
> This rotational upper bound makes Red-Black trees the standard implementation for Java `TreeMap`, C++ `std::map`, and Linux CFS!

> **Memory Trick:** **"Red-Black Tree: Max 2 rotations on insert, Max 3 rotations on delete!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Tree | AVL Tree |
| :--- | :--- | :--- |
| **Height Bound** | $H \le 2.0 \log_2 N$ (Looser) | **$H \le 1.44 \log_2 N$ (Tighter) ⚡**|
| **Insert Rotations** | **At Most 2 ⚡** | **At Most 1 ⚡** |
| **Delete Rotations** | **At Most 3 ⚡** | Up to $O(\log N)$ |
| **Production Standard**| **`java.util.TreeMap`, C++ `map` ⚡**| Read-heavy spatial indexes |

---

## 14. How to Recognize This in Questions
* **"Self-balancing BST with at most 3 rotations per deletion for write-heavy maps"** $\rightarrow$ Red-Black Tree.
* **"Analyze color invariants and black-height properties"** $\rightarrow$ Red-Black Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: Who invented the Red-Black Tree?**  
  *A:* Rudolf Bayer in 1972 (originally named "Symmetric Binary B-Trees"), named "Red-Black Trees" by Guibas & Sedgewick in 1978.
* **Q: Why are sentinel NIL leaves always BLACK?**  
  *A:* To satisfy the Black-Height invariant uniformly across all paths that terminate at external null links.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RED-BLACK TREE FOUNDATIONS                            |
+-----------------------------------------------------------------------+
| • Color Flag    : Node stores 1-bit boolean color (RED/BLACK)          |
| • Height Bound  : H <= 2.0 log2(N + 1)                                |
| • Write Bounds  : At most 2 rotations on insert; At most 3 on delete!  |
| • New Nodes     : ALWAYS inserted as RED!                             |
| • NIL Leaves    : Null pointers are ALWAYS treated as BLACK           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can state the 5 core structural properties of Red-Black trees.
- [ ] I can write the `getColor` helper returning BLACK for null nodes.
- [ ] I can verify the Black-Height invariant across a tree in $O(N)$ time.
- [ ] I know why Red-Black trees require at most 3 rotations per deletion.
- [ ] I know the 2-3-4 tree isometry to Red-Black trees.
