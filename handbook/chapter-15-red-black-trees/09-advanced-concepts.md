# 09. Advanced Red-Black Concepts: Left-Leaning LLRB, OS-Trees & Interval Trees

## 1. Introduction
Advanced Red-Black Tree extensions—specifically **Left-Leaning Red-Black Trees (LLRB)** invented by Robert Sedgewick in 2008, **Order-Statistic Trees (OS-Trees)**, and **Interval Trees**—extend basic Red-Black mechanics to dramatically simplify code complexity or solve specialized geometric range query problems. LLRB trees restrict RED links to lean exclusively to the **LEFT**, creating a 1-to-1 direct isometry with **2-3 B-Trees** and reducing insertion/deletion fixup code from 300+ lines down to ~30 lines!

> **Important:** Advanced Red-Black Variants:
> 1. **Left-Leaning Red-Black (LLRB) Trees**: Enforces that ALL RED links lean LEFT! Eliminates right-leaning RED links using a simple `isRed(node.right) && !isRed(node.left) \implies rotateLeft(node)` fixup rule.
> 2. **Order-Statistic Trees (OS-Trees)**: Augments each node with a `size` field (`node.size = 1 + left.size + right.size`), enabling `select(k)` ($K$-th smallest key) and `rank(key)` queries in **$O(\log N)$ Time**!
> 3. **Interval Trees**: Augments each node with `[low, high]` intervals and a `maxHigh` attribute, enabling overlapping interval searches in **$O(\log N)$ Time**! ⚡

```
Left-Leaning Red-Black (LLRB) Invariant vs Standard RB-Tree:
LLRB Invariant (Red Links Lean LEFT ONLY):          Standard RB-Tree (Red Links Lean Left OR Right):
             (30 BLACK)                                          (30 BLACK)
            /          \                                        /          \
     (20 RED)          (40 BLACK)                        (20 BLACK)        (40 RED) <--- Right-leaning RED!
```

---

## 2. Core Concepts & LLRB 2-3 Tree Isometry

### 2.1 LLRB Insertion Mechanics (3 Universal Post-Order Lines)
In an LLRB tree, after standard BST recursive insertion, balance is restored using **3 concise post-order statements**:
1. **Right-leaning RED link**: `if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h);`
2. **Double-left RED links**: `if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h);`
3. **Both children RED**: `if (isRed(h.left) && isRed(h.right)) flipColors(h);`

```
LLRB 3-Rule Fixup Pipeline:
1. Is right child RED & left child BLACK? -------------> rotateLeft(h)!
2. Are left child AND left-grandchild RED? ----------> rotateRight(h)!
3. Are BOTH left child AND right child RED? ---------> flipColors(h)! ⚡
```

> **Memory Trick:** **"LLRB 3 lines: rotateLeft if right is RED; rotateRight if double-left RED; flipColors if both RED!"**

---

## 3. Characteristics & Order-Statistic Trees (OS-Trees)

### 3.1 Order-Statistic Tree `select(k)` Algorithm
Given an OS-Tree, find the $K$-th smallest key (1-indexed):
1. Compute `leftSize = (node.left == null) ? 0 : node.left.size`.
2. `rank = leftSize + 1`.
3. If `k == rank`: Return `node.val`! (Target matched).
4. If `k < rank`: Recurse into `node.left` with target `k`.
5. Else (`k > rank`): Recurse into `node.right` with target `k - rank`.

---

## 4. Internal Working Mechanics
Tracing LLRB 3-Rule Post-Order Fixup on inserting key 30 into tree `[10 (B), 20 (R)]`:

```
Insertion path: 10 -> 20 -> 30.
- Node 10 has left=null, right=20 (RED). Node 20 has right=30 (RED).

Post-Order Fixup at Node 10:
- Rule 1 Check: isRed(right=20) && !isRed(left=null) -> TRUE!
  - Execute rotateLeft(10) -> Promotes 20 to root (left=10 RED, right=30 RED).
- Rule 3 Check: isRed(left=10) && isRed(right=30) -> TRUE!
  - Execute flipColors(20) -> 20 becomes RED, 10 and 30 become BLACK!

Enforce Root Rule: root.color = BLACK (20 becomes BLACK).

Resulting Tree = 20 (B, left=10 B, right=30 B). 100% Valid LLRB Tree! ✅ (O(log N) Time!)
```

---

## 5. Visual Diagram
LLRB 3-Rule Transformation Topography:

```
Step 1: Right-Leaning RED Link              Step 2: Color Flip (Both RED)
       (10 BLACK)                                  (20 RED)
      /          \         rotateLeft(10)         /        \
  null        (20 RED)    -------------->   (10 BLACK)    (30 BLACK)
                 \
              (30 RED)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a Left-Leaning Red-Black (LLRB) Tree:

```java
import java.util.*;

public class AdvancedRBConceptsMaster {

    public static final boolean RED = true;
    public static final boolean BLACK = false;

    public static class LLRBNode {
        public int val;
        public boolean color;
        public LLRBNode left;
        public LLRBNode right;

        public LLRBNode(int val) {
            this.val = val;
            this.color = RED; // New nodes inserted as RED
        }
    }

    private LLRBNode root = null;

    public static boolean isRed(LLRBNode h) {
        return (h != null) && (h.color == RED);
    }

    private LLRBNode rotateLeft(LLRBNode h) {
        LLRBNode x = h.right;
        h.right = x.left;
        x.left = h;
        x.color = h.color;
        h.color = RED;
        return x;
    }

    private LLRBNode rotateRight(LLRBNode h) {
        LLRBNode x = h.left;
        h.left = x.right;
        x.right = h;
        x.color = h.color;
        h.color = RED;
        return x;
    }

    private void flipColors(LLRBNode h) {
        h.color = !h.color;
        if (h.left != null) h.left.color = !h.left.color;
        if (h.right != null) h.right.color = !h.right.color;
    }

    // LLRB Insertion with 3 Post-Order Fixup Rules O(log N) Time, O(H) Space
    public void insert(int val) {
        root = insertHelper(root, val);
        root.color = BLACK; // Enforce root BLACK rule
    }

    private LLRBNode insertHelper(LLRBNode h, int val) {
        if (h == null) return new LLRBNode(val);

        if (val < h.val) h.left = insertHelper(h.left, val);
        else if (val > h.val) h.right = insertHelper(h.right, val);
        else return h;

        // The 3 Universal LLRB Post-Order Fixup Statements:
        if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h);
        if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h);
        if (isRed(h.left) && isRed(h.right)) flipColors(h);

        return h;
    }

    public LLRBNode getRoot() { return root; }
}
```

> **Quick Syntax:**
```java
// The 3 LLRB Post-Order Fixup Lines
if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h);
if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h);
if (isRed(h.left) && isRed(h.right)) flipColors(h);
```

---

## 7. Concrete Problem Examples
* **Sedgewick's LLRB Trees**: Concise production Red-Black tree implementation.
* **Interval Trees**: Overlapping calendar event scheduling.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LLRB Tree Insertion:

```java
public class AdvancedRBConceptsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Left-Leaning Red-Black (LLRB) Tree Test ===");
        AdvancedRBConceptsMaster llrb = new AdvancedRBConceptsMaster();
        int[] keys = {10, 20, 30, 40, 50};

        for (int key : keys) {
            llrb.insert(key);
        }

        AdvancedRBConceptsMaster.LLRBNode root = llrb.getRoot();
        System.out.println("LLRB Root Value: " + root.val); // Output: 20
        System.out.println("LLRB Root Color: " + 
            (root.color == AdvancedRBConceptsMaster.BLACK ? "BLACK" : "RED")); // BLACK
        System.out.println("Root Left Value: " + root.left.val); // Output: 10
        System.out.println("Root Right Value: " + root.right.val); // Output: 40 ✅
    }
}
```

---

## 9. Complexity Analysis

| LLRB Operation | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **LLRB Insertion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space |
| **OS-Tree `select(k)`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space |

---

## 10. Edge Cases & Boundary Handling
* **Inserting into Empty LLRB Tree**: Returns `new LLRBNode(val)` and sets color to BLACK.
* **Duplicate Keys**: Ignored in standard LLRB implementation.

---

## 11. Common Mistakes & Anti-Patterns
* **Reversing Order of the 3 LLRB Post-Order Fixup Statements**:
  - The 3 statements MUST be executed in exact order: `rotateLeft` $\to$ `rotateRight` $\to$ `flipColors`. Reversing statement order leaves right-leaning RED links in the tree!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Sedgewick Invented Left-Leaning Red-Black (LLRB) Trees:
> Standard Red-Black tree insertion/deletion requires complex parent-pointer tracking and ~300 lines of code.
> By restricting RED links to lean exclusively LEFT, LLRB trees achieve exact 1-to-1 equivalence with 2-3 trees, allowing insertion to be implemented recursively in **under 30 lines of code**!

> **Memory Trick:** **"LLRB 3 lines: rotateLeft, rotateRight, flipColors! Under 30 lines total code!"**

---

## 13. System & Implementation Comparisons

| Feature | Left-Leaning Red-Black (LLRB) | Standard Red-Black Tree |
| :--- | :--- | :--- |
| **Red Link Direction** | **Left ONLY ⚡** | Left OR Right |
| **Code Length** | **~30 Lines (Concise) ⚡** | ~300 Lines (Complex) |
| **B-Tree Isometry** | **2-3 Tree ⚡** | 2-3-4 Tree |

---

## 14. How to Recognize This in Questions
* **"Implement Red-Black tree recursively in under 30 lines of code"** $\rightarrow$ Left-Leaning Red-Black (LLRB) Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: What is a Left-Leaning Red-Black (LLRB) tree?**  
  *A:* A variant of Red-Black trees where all RED links are restricted to lean LEFT, making the structure 1-to-1 equivalent with 2-3 B-Trees.
* **Q: How does an Order-Statistic Tree find the $K$-th smallest key in $O(\log N)$ time?**  
  *A:* By storing `size` in every node, allowing binary search navigation based on `leftSize + 1`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED RED-BLACK CONCEPTS (LLRB & OS-TREES)         |
+-----------------------------------------------------------------------+
| • LLRB Invariant : RED links MUST lean LEFT ONLY                      |
| • Fixup Rule 1   : if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h)|
| • Fixup Rule 2   : if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h)|
| • Fixup Rule 3   : if (isRed(h.left) && isRed(h.right)) flipColors(h);|
| • OS-Tree        : Augments nodes with size; select(k) runs in O(log N)|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LLRB Tree Insertion with 3 post-order fixup lines in Java.
- [ ] I can state the 3 LLRB fixup rules in exact order.
- [ ] I know why LLRB trees map 1-to-1 to 2-3 B-Trees.
- [ ] I can write `select(k)` on an Order-Statistic Tree in $O(\log N)$ time.
- [ ] I can trace LLRB insertion step by step.
