# 10. Master Reference — AVL Trees

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 14: AVL Trees**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for self-balancing tree technical rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh the Height-Balance Invariant ($|\text{BF}| \le 1$), Strict Height Limit ($H \le 1.44 \log_2 N$), 4 Rotation Cases (LL, RR, LR, RL), Pointer Relinking Formulas, At-Most-One Rotation Limit for Insertions, Up to $O(\log N)$ Rotations for Deletions, and Read-Heavy System Benchmarks!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **AVL Height-Balance Invariant**:
  - $\forall \text{ node } X, |\text{BF}(X)| = |\text{Height}(\text{left}(X)) - \text{Height}(\text{right}(X))| \le 1$.
* **Node Height Calculation Formula**:
  - $\text{Height}(X) = 1 + \max(\text{Height}(\text{left}(X)), \text{Height}(\text{right}(X)))$. (Leaf height = 1, Null height = 0).
* **Strict Height Limit Bound**:
  - $H < 1.44 \log_2(N + 2)$, derived from the Fibonacci minimum node recurrence $N(H) = 1 + N(H-1) + N(H-2)$.
* **Balance Factor Classification & Rebalancing Matrix**:
  - $\text{BF}(X) = +2, \text{child.BF} \ge 0 \implies$ **LL Case** $\to$ `rightRotate(X)`.
  - $\text{BF}(X) = -2, \text{child.BF} \le 0 \implies$ **RR Case** $\to$ `leftRotate(X)`.
  - $\text{BF}(X) = +2, \text{child.BF} < 0 \implies$ **LR Case** $\to$ `X.left = leftRotate(X.left); return rightRotate(X)`.
  - $\text{BF}(X) = -2, \text{child.BF} > 0 \implies$ **RL Case** $\to$ `X.right = rightRotate(X.right); return leftRotate(X)`.

```
AVL Trees Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Height-Balance Invariant          | |Balance Factor| <= 1 for EVERY node              |
| Balance Factor Formula            | BF = Height(Left) - Height(Right)                 |
| Maximum Height Bound              | H <= 1.44 log2 N (Tighter than Red-Black)         |
| Single Right Rotation (LL)        | X = Y.left; T2 = X.right; X.right = Y; Y.left = T2|
| Single Left Rotation (RR)         | Y = X.right; T2 = Y.left; Y.left = X; X.right = T2|
| Double Left-Right Rotation (LR)   | node.left = leftRotate(node.left); return rightRotate(node)|
| Double Right-Left Rotation (RL)   | node.right = rightRotate(node.right); return leftRotate(node)|
| Insertion Rotation Upper Bound    | AT MOST 1 single or double rotation per insert ⚡  |
| Deletion Rotation Upper Bound     | Up to O(log N) rotations propagating to root ⚡    |
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Search Lookup** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | Tighter height $H \le 1.44 \log_2 N$ |
| **`rightRotate(y)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 4 Pointer relinks (LL Case) |
| **`leftRotate(x)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 4 Pointer relinks (RR Case) |
| **`rotateLR(z)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 2 Single rotations (LR Case) |
| **`rotateRL(z)`** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡** | **$O(1)$ Constant ⚡**| 2 Single rotations (RL Case) |
| **AVL Insertion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | At most 1 rotation total ⚡ |
| **AVL Deletion** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(H)$ Call Stack Space | Up to $O(\log N)$ rotations ⚡ |
| **Find Min / Max** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$O(1)$ Constant ⚡**| Leftmost / Rightmost link follow |
| **Range Query** | **$O(K + \log N)$ ⚡** | **$O(K + \log N)$ ⚡** | **$O(K + \log N)$ ⚡** | $O(H)$ Call Stack Space | Range-pruned tree traversal |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for AVL Nodes                                                    |
+-----------------------------------------------------------------------------------+
| Standard `AVLNode` Object           : 32 Bytes per Node (Header + 3 Refs + Int Height)|
| CPU Cache Line Alignment            : Fits 2 nodes per 64-byte L1 cache line        |
| Search Lookup Efficiency            : ~30% fewer cache misses than Red-Black trees   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Balance Factor Calculation Line
int bf = (node == null) ? 0 : getHeight(node.left) - getHeight(node.right);

// 2. Single Right Rotation Engine (LL Case)
AVLNode x = y.left; AVLNode T2 = x.right;
x.right = y; y.left = T2;
updateHeight(y); updateHeight(x); return x;

// 3. Single Left Rotation Engine (RR Case)
AVLNode y = x.right; AVLNode T2 = y.left;
y.left = x; x.right = T2;
updateHeight(x); updateHeight(y); return y;

// 4. Double Rotation Engines (LR & RL Cases)
// LR: node.left = leftRotate(node.left); return rightRotate(node);
// RL: node.right = rightRotate(node.right); return leftRotate(node);

// 5. Complete AVL Rebalancing Block (Insertion)
if (balance > 1 && val < node.left.val) return rightRotate(node);
if (balance < -1 && val > node.right.val) return leftRotate(node);
if (balance > 1 && val > node.left.val) { node.left = leftRotate(node.left); return rightRotate(node); }
if (balance < -1 && val < node.right.val) { node.right = rightRotate(node.right); return leftRotate(node); }
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Incorrect Height Update Order in Rotations**: Updating parent node height before child node height computes height using stale values. Always call `updateHeight(child)` FIRST, then `updateHeight(parent)` SECOND.
* **Pitfall 2: Strict `<` / `>` Checks in Deletion**: In deletion, child balance factor can equal 0. Using strict `<` skips single rotation when `child.BF == 0`. Always use inclusive `>= 0` and `<= 0` checks in deletion!
* **Pitfall 3: Missing Null Check After Deletion**: Deleting a leaf node leaves `root == null`. Calling `updateHeight(root)` causes `NullPointerException`. Always check `if (root == null) return null;` before rebalancing.
* **Pitfall 4: Discarding Rotation Return Values**: Rotations return the NEW root of the subtree. Discarding the return value leaves parent pointers pointing to old nodes.
* **Pitfall 5: Choosing Red-Black Trees for Read-Heavy Workloads**: Using Red-Black trees for 99% read workloads wastes performance because Red-Black height is up to $2.0 \log_2 N$. Always use AVL Trees ($1.44 \log_2 N$) for Read-Heavy workloads!

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 14 (AVL TREES)                   |
+-----------------------------------------------------------------------+
| 1. Height-Balance: |Balance Factor| <= 1 for EVERY node               |
| 2. Balance Factor : BF = Height(Left) - Height(Right)                 |
| 3. Height Bound   : H <= 1.44 log2 N (Strictly tighter search paths)   |
| 4. LL Case        : BF = +2, child.BF >= 0 -> rightRotate(node)       |
| 5. RR Case        : BF = -2, child.BF <= 0 -> leftRotate(node)        |
| 6. LR Case        : BF = +2, child.BF < 0  -> leftRotate(left) + rightRotate|
| 7. RL Case        : BF = -2, child.BF > 0  -> rightRotate(right) + leftRotate|
| 8. AVL Insertion  : Requires AT MOST 1 single or double rotation ⚡   |
| 9. AVL Deletion   : Requires Up to O(log N) rotations to root ⚡       |
| 10. System Choice : Best for Read-Heavy Workloads (Order Books, Caches)|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write the AVL height-balance invariant $|\text{BF}| \le 1$.
- [ ] I can write `getHeight`, `getBalanceFactor`, and `updateHeight`.
- [ ] I can write `rightRotate` (LL Case) in 6 lines.
- [ ] I can write `leftRotate` (RR Case) in 6 lines.
- [ ] I can write `rotateLR` and `rotateRL` double rotations.
- [ ] I can write full AVL Insertion with 4-case rebalancing in Java.
- [ ] I can write full AVL Deletion with 3-case removal and rebalancing in Java.
- [ ] I can state the rotation upper bounds for insertion (at most 1) vs deletion (up to $O(\log N)$).
- [ ] I can prove why AVL trees provide faster lookups than Red-Black trees.
- [ ] I can design an AVL Order Book Price Index for high-frequency trading.
