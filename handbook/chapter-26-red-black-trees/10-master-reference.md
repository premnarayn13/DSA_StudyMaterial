# 10. Master Reference — Red-Black Trees

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 15: Red-Black Trees**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for advanced data structures and operating systems technical rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh the 5 Red-Black Invariants, Maximum Height Bound ($H \le 2.0 \log_2(N + 1)$), 6-Pointer Relinking Equations, 3 Insertion Fixup Cases (At Most 2 Rotations), 4 Deletion Fixup Cases (At Most 3 Rotations), Left-Leaning LLRB 3-Line Post-Order Rules, and Production Adoption (`java.util.TreeMap`, Linux CFS Scheduler)!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **The 5 Red-Black Structural Rules**:
  1. Every node is RED or BLACK.
  2. Root is ALWAYS BLACK.
  3. NIL leaves are ALWAYS BLACK.
  4. RED nodes MUST have BLACK children (No Double RED!).
  5. Every path from a node to descendant NIL leaves has the EXACT SAME Black-Height ($bh$).
* **Strict Maximum Height Bound Formula**:
  - $H \le 2 \log_2(N + 1)$, derived from shortest path $bh$ vs longest path $2 \cdot bh$.
* **Rotational Upper Bounds**:
  - **Insertion**: At Most **2 Rotations** total.
  - **Deletion**: At Most **3 Rotations** total.
* **Left-Leaning Red-Black (LLRB) 3 Post-Order Rules**:
  - `if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h);`
  - `if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h);`
  - `if (isRed(h.left) && isRed(h.right)) flipColors(h);`

```
Red-Black Trees Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Maximum Height Bound              | H <= 2 log2(N + 1) (Longest path <= 2 * shortest) |
| Insertion Fixup (Case 1)          | Uncle RED -> Recolor P, U to BLACK; G to RED; k=G |
| Insertion Fixup (Case 2)          | Uncle BLACK (Zigzag) -> k=P; leftRotate(k)        |
| Insertion Fixup (Case 3)          | Uncle BLACK (Line) -> Recolor P, G; rightRotate(G)|
| Deletion Fixup (Case 4)           | Sibling BLACK, Far Nephew RED -> Rotate & TERMINATE|
| Insertion Rotation Upper Bound    | AT MOST 2 Rotations total per insertion ⚡         |
| Deletion Rotation Upper Bound     | AT MOST 3 Rotations total per deletion ⚡          |
| LLRB Fixup Engine                 | 3 lines: rotateLeft, rotateRight, flipColors      |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Search Lookup** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(1)$ Auxiliary Space | Binary search tree traversal |
| **`leftRotate(x)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 6 Parent-pointer links |
| **`rightRotate(y)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 6 Parent-pointer links |
| **Red-Black Insertion**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Constant ⚡**| **At Most 2 Rotations ⚡**|
| **Red-Black Deletion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Constant ⚡**| **At Most 3 Rotations ⚡**|
| **LLRB Insertion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | 3 Post-order fixup lines |
| **OS-Tree `select(k)`**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | Node size field traversal |
| **Find Min / Max** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Constant ⚡**| Leftmost / Rightmost link follow |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Red-Black Nodes                                              |
+-----------------------------------------------------------------------------------+
| Standard `RBNode` Object            : 32 Bytes per Node (Header + 3 Refs + 1 Bit Color)|
| Pointer Alignment Optimization      : Boolean color packed into 64-bit reference padding|
| Production Standard                 : `java.util.TreeMap`, C++ `std::map`, Linux `rbtree`|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Color Helper Line (NIL is BLACK)
public static boolean getColor(RBNode node) { return (node == null) ? BLACK : node.color; }

// 2. RB Parent-Pointer Left Rotate Core
RBNode y = x.right; x.right = y.left; if (y.left != null) y.left.parent = x;
y.parent = x.parent; if (x.parent == null) root = y; else if (x == x.parent.left) x.parent.left = y; else x.parent.right = y;
y.left = x; x.parent = y;

// 3. RB Insertion Fixup Case 1 (Uncle RED)
k.parent.color = BLACK; uncle.color = BLACK; k.parent.parent.color = RED; k = k.parent.parent;

// 4. LLRB 3 Post-Order Fixup Lines
if (isRed(h.right) && !isRed(h.left)) h = rotateLeft(h);
if (isRed(h.left) && isRed(h.left.left)) h = rotateRight(h);
if (isRed(h.left) && isRed(h.right)) flipColors(h);

// 5. Enforce Root Rule
root.color = BLACK;
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Treating Null Pointers as RED**: Null pointers represent sentinel NIL leaves and are strictly defined as **BLACK**. Returning RED for null corrupts black-height math.
* **Pitfall 2: Forgetting `T2.parent` Link Update in Rotations**: Re-linking `x.right = y.left` without updating `y.left.parent = x` leaves $T_2$ pointing to old parent $Y$, corrupting bottom-up tree traversals.
* **Pitfall 3: Forgetting `root.color = BLACK` at End of Fixup**: Insertion fixup recoloring can color the root RED. Always enforce `root.color = BLACK` at the end of `insertFixup`.
* **Pitfall 4: Running Deletion Fixup on RED Node Deletion**: Deleting a RED node does not alter black-height on any path. Running fixup on RED deletion corrupts node colors. Only run `deleteFixup` when `yOriginalColor == BLACK`.
* **Pitfall 5: Reversing LLRB Post-Order Statement Order**: The 3 LLRB statements MUST be executed in exact order: `rotateLeft` $\to$ `rotateRight` $\to$ `flipColors`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 15 (RED-BLACK TREES)             |
+-----------------------------------------------------------------------+
| 1. Height Bound   : H <= 2.0 log2(N + 1) (Longest <= 2 * Shortest)     |
| 2. Insert Rotations: AT MOST 2 Rotations total per insertion ⚡        |
| 3. Delete Rotations: AT MOST 3 Rotations total per deletion ⚡         |
| 4. Uncle RED Case  : Recolor P, U to BLACK, G to RED; propagate up    |
| 5. Uncle BLACK Case: Rotate & TERMINATE immediately                   |
| 6. Delete Fixup    : Sibling BLACK & Far Nephew RED rotates & TERMINATES|
| 7. LLRB Engine     : 3 lines: rotateLeft, rotateRight, flipColors     |
| 8. OS-Trees        : Augments size field for O(log N) select(k)       |
| 9. Production Std  : Powers Java TreeMap, C++ map, Linux CFS scheduler|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can list all 5 Red-Black tree coloring rules from memory.
- [ ] I can write `leftRotate` and `rightRotate` with parent pointers in Java.
- [ ] I can write full Red-Black Insertion and `insertFixup` in Java.
- [ ] I can write full Red-Black Deletion and `deleteFixup` in Java.
- [ ] I can write LLRB Tree Insertion with 3 post-order fixup lines in Java.
- [ ] I can prove why insertion requires at most 2 rotations.
- [ ] I can prove why deletion requires at most 3 rotations.
- [ ] I know why Java `TreeMap` and Linux CFS use Red-Black trees.
