# 08. Red-Black Trees, The 5 Color Invariants & Uncle Recoloring Engines

## 1. Introduction
A **Red-Black Tree** is a self-balancing binary search tree that maintains height balance using **Node Color Properties (RED or BLACK)** rather than strict height balance factors. Red-Black Trees power production runtime libraries—including Java's `java.util.TreeMap`, `java.util.TreeSet`, Java 8 `HashMap` treeified bins, C++ `std::map`, and Linux kernel `rbtree`. By guaranteeing that no path from root to leaf is more than **TWICE as long as any other path**, Red-Black Trees guarantee **$O(\log N)$ Strict Worst-Case Time Complexity** for search, insertion, and deletion with minimal rotation overhead.

> **Important:** The 5 Canonical Invariants of Red-Black Trees:
> 1. **Node Color Rule**: Every node is either **RED** or **BLACK**.
> 2. **Root Rule**: The **ROOT** node is ALWAYS **BLACK**.
> 3. **Leaf Rule**: Every **LEAF (NIL sentinel)** is ALWAYS **BLACK**.
> 4. **Red Parent-Child Rule (No Consecutive Reds)**: If a node is **RED**, both of its children MUST be **BLACK**! (A RED node cannot have a RED parent!).
> 5. **Black-Height Rule**: For every node $X$, all simple paths from $X$ down to descendant leaves contain the **EXACT SAME NUMBER OF BLACK NODES**! ⚡

```
Red-Black Tree Structural Topology:
                    [ Root: 10 (BLACK) ]
                     /                \
        [ Node 5 (RED) ]            [ Node 15 (RED) ]
         /           \               /            \
  [ N2 (BLACK) ] [ N7 (BLACK) ] [ N12 (BLACK) ] [ N20 (BLACK) ]

Black-Height from Root = 2 (Count of Black nodes down any path to NIL).
No consecutive RED nodes exist! Height H <= 2 log2(N+1)! ⚡
```

---

## 2. Core Concepts & Uncle Case Insertion Analysis

### 2.1 Insertion Strategy & The Uncle Node
When inserting a new key into a Red-Black Tree:
1. Always insert the new node $X$ as a **RED** node! (Inserting a RED node preserves Rule 5 Black-Height, but may violate Rule 4 No Consecutive Reds!).
2. If parent $P$ of $X$ is BLACK: Insertion is COMPLETE! No violation!
3. If parent $P$ of $X$ is **RED**: Violation of Rule 4! Inspect **Uncle Node $U$** (Sibling of parent $P$):

#### Case 1: Uncle $U$ is RED (Recoloring Case)
* **Action**:
  - Color Parent $P$ **BLACK**.
  - Color Uncle $U$ **BLACK**.
  - Color Grandparent $G$ **RED**.
  - Move current node pointer to Grandparent $G$ and repeat rebalancing up the tree!

#### Case 2: Uncle $U$ is BLACK (Rotation Case)
* **Sub-case 2A (Triangle / LR or RL)**: Rotate $X$ around $P$ to form a straight line (LL or RR).
* **Sub-case 2B (Line / LL or RR)**: Rotate $P$ around $G$, then swap colors of $P$ and $G$!

```
Red-Black Insertion Case Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Insertion State       | Parent Color      | Uncle Color       | Action Taken      |
+-----------------------+-------------------+-------------------+-------------------+
| Base Case             | **BLACK**         | Any               | Done! No Violation|
| **Case 1: Red Uncle** | **RED**           | **RED**           | **Recolor P,U,G** |
| **Case 2A: Triangle** | **RED**           | **BLACK**         | **Rotate P -> Line**|
| **Case 2B: Line**     | **RED**           | **BLACK**         | **Rotate G + Swap Color**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Red Uncle = Recolor P, U, G! Black Uncle = Rotate and Swap Colors of P and G!"**

---

## 3. Characteristics & Black-Height Invariant Proof

### 3.1 Mathematical Proof of $H \le 2 \log_2(N + 1)$ Height Bound
Let $bh(X)$ be the **Black-Height** of node $X$ (number of black nodes on any path from $X$ down to leaf, excluding $X$):
* By Rule 4 (No Consecutive Reds), at least half of the nodes on any path from root to leaf must be BLACK.
* Therefore, total tree height $H \le 2 \cdot bh(\text{root})$.
* A Red-Black tree with black-height $bh$ has at least $2^{bh} - 1$ internal nodes:

$$N \ge 2^{bh} - 1 \implies bh \le \log_2(N + 1) \implies \mathbf{H \le 2 \log_2(N + 1)}$$

---

## 4. Internal Working Mechanics
Tracing Insertion of Key into Red-Black Tree (Case 1: Red Uncle):

```
Initial Tree: Grandparent G(10, BLACK), Parent P(5, RED), Uncle U(15, RED).
Insert New Node X(2, RED) under P(5).

Violation Detected: X(2, RED) has RED Parent P(5)!
Inspect Uncle U(15): Uncle is RED! -> Trigger Case 1 (Recoloring):

1. Color P(5) -> BLACK.
2. Color U(15) -> BLACK.
3. Color G(10) -> RED.
4. Set current node = G(10).
5. G(10) is Root -> Enforce Root Rule: Color G(10) BACK TO BLACK!

All 5 Invariants Restored in O(1) Time without ANY tree rotations! ✅
```

---

## 5. Visual Diagram
Red-Black Case 1 (Red Uncle) vs Case 2B (Black Uncle Line) Topography:

```
Case 1: Red Uncle (Recolor Only)        Case 2B: Black Uncle (Rotate & Swap Color)
        G (BLACK)                              G (BLACK)
       /         \                            /         \
    P (RED)    U (RED)                     P (RED)    U (BLACK)
    /                                      /
 X (RED)                                X (RED)
   |                                       |
Recolor P & U -> BLACK                  Rotate G Right! Swap colors of P & G!
Recolor G     -> RED                    P (BLACK) root, G (RED) child! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing a complete self-balancing Red-Black Tree supporting Insertion, Uncle Recoloring, and Rotations:

```java
import java.util.*;

public class RedBlackTreesMaster {

    public enum Color { RED, BLACK }

    public static class RBNode {
        public int val;
        public Color color;
        public RBNode left;
        public RBNode right;
        public RBNode parent;

        public RBNode(int val) {
            this.val = val;
            this.color = Color.RED; // New nodes inserted as RED by default!
            this.left = null;
            this.right = null;
            this.parent = null;
        }
    }

    private RBNode root;

    public RedBlackTreesMaster() {
        this.root = null;
    }

    // 1. Insertion into Red-Black Tree O(log N) Time
    public void insert(int val) {
        RBNode node = new RBNode(val);
        root = bstInsert(root, node);
        fixViolation(node); // Restore 5 Color Invariants
    }

    private RBNode bstInsert(RBNode root, RBNode node) {
        if (root == null) return node;

        if (node.val < root.val) {
            root.left = bstInsert(root.left, node);
            root.left.parent = root;
        } else if (node.val > root.val) {
            root.right = bstInsert(root.right, node);
            root.right.parent = root;
        }

        return root;
    }

    // Restore Red-Black Tree Invariants after Insertion
    private void fixViolation(RBNode node) {
        RBNode parent = null;
        RBNode grandparent = null;

        while (node != root && node.color == Color.RED && node.parent.color == Color.RED) {
            parent = node.parent;
            grandparent = parent.parent;

            // Parent is LEFT child of Grandparent
            if (parent == grandparent.left) {
                RBNode uncle = grandparent.right;

                // Case 1: Uncle is RED -> Recolor P, U, G
                if (uncle != null && uncle.color == Color.RED) {
                    grandparent.color = Color.RED;
                    parent.color = Color.BLACK;
                    uncle.color = Color.BLACK;
                    node = grandparent; // Propagate up
                } else {
                    // Case 2A: Triangle (Left-Right) -> Rotate Parent Left
                    if (node == parent.right) {
                        rotateLeft(parent);
                        node = parent;
                        parent = node.parent;
                    }

                    // Case 2B: Line (Left-Left) -> Rotate Grandparent Right & Swap Colors
                    rotateRight(grandparent);
                    Color temp = parent.color;
                    parent.color = grandparent.color;
                    grandparent.color = temp;
                    node = parent;
                }
            } else {
                // Parent is RIGHT child of Grandparent (Symmetric Cases)
                RBNode uncle = grandparent.left;

                // Case 1: Uncle is RED
                if (uncle != null && uncle.color == Color.RED) {
                    grandparent.color = Color.RED;
                    parent.color = Color.BLACK;
                    uncle.color = Color.BLACK;
                    node = grandparent;
                } else {
                    // Case 2A: Triangle (Right-Left)
                    if (node == parent.left) {
                        rotateRight(parent);
                        node = parent;
                        parent = node.parent;
                    }

                    // Case 2B: Line (Right-Right)
                    rotateLeft(grandparent);
                    Color temp = parent.color;
                    parent.color = grandparent.color;
                    grandparent.color = temp;
                    node = parent;
                }
            }
        }

        root.color = Color.BLACK; // Always enforce Root Rule!
    }

    private void rotateLeft(RBNode node) {
        RBNode rightChild = node.right;
        node.right = rightChild.left;
        if (node.right != null) node.right.parent = node;

        rightChild.parent = node.parent;
        if (node.parent == null) root = rightChild;
        else if (node == node.parent.left) node.parent.left = rightChild;
        else node.parent.right = rightChild;

        rightChild.left = node;
        node.parent = rightChild;
    }

    private void rotateRight(RBNode node) {
        RBNode leftChild = node.left;
        node.left = leftChild.right;
        if (node.left != null) node.left.parent = node;

        leftChild.parent = node.parent;
        if (node.parent == null) root = leftChild;
        else if (node == node.parent.left) node.parent.left = leftChild;
        else node.parent.right = leftChild;

        leftChild.right = node;
        node.parent = leftChild;
    }

    public RBNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// Case 1 Red Uncle Recoloring Lines
grandparent.color = Color.RED;
parent.color = Color.BLACK;
uncle.color = Color.BLACK;
```

---

## 7. Concrete Problem Examples
* **Java 8 `java.util.HashMap`**: Treeification of bucket bins to Red-Black Trees.
* **Java `java.util.TreeMap` / `TreeSet`**: Standard JDK sorted map implementation.
* **Linux Kernel CPU Scheduler (`CFS`)**: Red-Black tree tracking runnable tasks.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Red-Black Tree insertion and color fixing:

```java
public class RedBlackTreesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Red-Black Tree Insertion & Color Fixing Test ===");
        RedBlackTreesMaster rbTree = new RedBlackTreesMaster();

        // Insert elements: 10, 20, 30, 15
        rbTree.insert(10);
        rbTree.insert(20);
        rbTree.insert(30);
        rbTree.insert(15);

        RedBlackTreesMaster.RBNode root = rbTree.getRoot();
        System.out.println("Root Value: " + root.val + " (Color: " + root.color + ")"); 
        // Output: 20 (BLACK)

        System.out.println("Root Left Value:  " + root.left.val + " (Color: " + root.left.color + ")"); 
        // Output: 10 (BLACK)

        System.out.println("Root Right Value: " + root.right.val + " (Color: " + root.right.color + ")"); 
        // Output: 30 (BLACK)

        System.out.println("Root Right Left:  " + root.right.left.val + " (Color: " + root.right.left.color + ")"); 
        // Output: 15 (RED) -> All 5 Invariants Restored! ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation / Action | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Rebalance Rotations |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Search** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space | 0 Rotations |
| **Insert** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space | **At most 2 Rotations ⚡**|
| **Delete** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Stack Space | **At most 3 Rotations ⚡**|

---

## 10. Edge Cases & Boundary Handling
* **Root Node Re-coloring**: Always enforce `root.color = Color.BLACK` at the end of every fixup operation.
* **Null Sentinel Leaves**: NIL leaves are treated as BLACK nodes for Black-Height calculations.

---

## 11. Common Mistakes & Anti-Patterns
* **Inserting New Nodes as BLACK**:
  - Inserting a BLACK node immediately violates Rule 5 (Black-Height equality) across subtrees, requiring complex multi-level rebalancing.
  - **ALWAYS insert new nodes as RED**.
* **Forgetting to Enforce Black Root Rule**:
  - Case 1 recoloring can change the Root to RED. Always explicitly set `root.color = Color.BLACK` before returning.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Red-Black Trees are Preferred over AVL Trees for Production Maps:
> * **AVL Trees** enforce strict height balance ($|\text{BF}| \le 1$), requiring up to $O(\log N)$ rotations on deletions.
> * **Red-Black Trees** allow looser balance ($H \le 2 \log_2 N$), guaranteeing **AT MOST 2 ROTATIONS on Insertion and AT MOST 3 ROTATIONS on Deletion**!
> * Fewer rotations make Red-Black Trees significantly faster for write-heavy maps (`TreeMap`, Linux `rbtree`)!

> **Memory Trick:** **"Red-Black Trees guarantee AT MOST 2 rotations on insert and 3 rotations on delete!"**

---

## 13. System & Implementation Comparisons

| Feature | Red-Black Tree | AVL Tree |
| :--- | :--- | :--- |
| **Max Rotation Count (Write)**| **At most 2-3 Rotations ⚡** | Up to $O(\log N)$ Rotations |
| **Maximum Height Bound** | $H \le 2.0 \log_2 N$ | **$H \le 1.44 \log_2 N$ ⚡** |
| **Industry Adoption** | **Java TreeMap / HashMap, Linux Kernel**| High-Speed Read-Only Databases |

---

## 14. How to Recognize This in Questions
* **"Explain the 5 invariants of Red-Black Trees"** $\rightarrow$ Root Black, No Consecutive Reds, Equal Black-Height.
* **"Why does Java 8 HashMap treeify bins to Red-Black Trees instead of AVL Trees?"** $\rightarrow$ Red-Black trees require fewer rotations on writes.

---

## 15. Frequently Asked Interview Questions
* **Q: Why are new nodes inserted as RED by default?**  
  *A:* Inserting a RED node preserves Rule 5 (equal black-height across all paths). While it may violate Rule 4 (no consecutive REDs), fixing a red-red violation locally via recoloring or 1-2 rotations is far easier than re-balancing black-heights across the entire tree.
* **Q: What is the maximum number of rotations performed during a Red-Black tree insertion?**  
  *A:* At most **2 rotations**! Case 1 (Red Uncle) performs only recoloring. Case 2A (Triangle) performs 1 rotation to convert to a line. Case 2B (Line) performs 1 rotation, restoring all color invariants completely.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: RED-BLACK TREES & THE 5 INVARIANTS                    |
+-----------------------------------------------------------------------+
| 1. Color Rule : Nodes are RED or BLACK                                |
| 2. Root Rule  : Root is ALWAYS BLACK                                  |
| 3. Leaf Rule  : NIL leaves are ALWAYS BLACK                           |
| 4. Red Rule   : RED node MUST have BLACK children (No consecutive REDs)|
| 5. Black-Height: ALL paths to leaves contain SAME number of BLACK nodes|
| • Red Uncle (Case 1)  : Recolor Parent, Uncle, Grandparent            |
| • Black Uncle (Case 2): Rotate & Swap Colors of Parent and Grandparent|
| • Rotation Limit: AT MOST 2 rotations on insert, 3 on delete ⚡       |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can list all 5 Red-Black Tree color invariants.
- [ ] I know why new nodes are inserted as RED.
- [ ] I can handle Case 1 (Red Uncle) recoloring.
- [ ] I can handle Case 2 (Black Uncle) rotations and color swaps.
- [ ] I know why Red-Black trees are preferred for `TreeMap` and `HashMap`.
