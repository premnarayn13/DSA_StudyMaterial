# 12. Master Reference — Binary Search Trees (BST)

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 13: Binary Search Trees (BST)**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh BST Ordering Invariant ($L < Root < R$), In-Order Sorted Traversal Invariant, Iterative $O(1)$ Space Search, 3-Case Node Deletion (`findMin(root.right)`), In-Order Successor / Predecessor Candidate Recording, Range Validation Bounds `(Long.MIN_VALUE, Long.MAX_VALUE)`, Reverse In-Order `Right -> Root -> Left` Greater Trees, Catalan Number Counting $C_N$, and In-Order + Midpoint Partition Re-balancing!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **BST Invariant Formula**:
  - $\forall L \in \text{left}(X), \text{key}(L) < \text{key}(X) \quad \text{and} \quad \forall R \in \text{right}(X), \text{key}(R) > \text{key}(X)$.
* **In-Order Traversal Invariant**:
  - In-Order Traversal (`Left -> Root -> Right`) of a valid BST yields values in **STRICTLY ASCENDING SORTED ORDER**!
* **Height Bounds**:
  - Balanced BST: Height $H = \lfloor \log_2 N \rfloor$. Operations run in $O(\log N)$ time.
  - Skewed BST: Height $H = N$. Operations degrade to $O(N)$ linear time.
* **$N$-th Catalan Number Formula (Unique BST Count)**:
  - $C_N = \frac{1}{N + 1} \binom{2N}{N} = \sum_{i=0}^{N-1} C_i \cdot C_{N-1-i}$.
* **Optimal BST DP Recurrence Equation**:
  - $dp[i][j] = w(i, j) + \min_{i \le k \le j} \left( dp[i][k-1] + dp[k+1][j] \right)$.
* **BST Range Search Pruning Rules**:
  - If `curr.val > low`: Recurse into `curr.left`.
  - If `curr.val < high`: Recurse into `curr.right`.

```
Binary Search Trees Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| BST In-Order Traversal            | In-Order traversal ALWAYS yields sorted ascending |
| Iterative Search                  | while (curr != null && curr.val != target)        |
| BST Validation Range              | Pass (Long.MIN_VALUE, Long.MAX_VALUE) boundaries  |
| 2-Child BST Deletion              | Overwrite node.val with findMin(root.right).val   |
| In-Order Successor                | Record candidate when turning LEFT (p.val < val)  |
| In-Order Predecessor              | Record candidate when turning RIGHT (p.val > val) |
| Minimum Key                       | Leftmost node: while (curr.left != null) curr=left|
| Maximum Key                       | Rightmost node: while (curr.right != null) curr=right|
| Greater Tree Conversion           | Reverse In-Order DFS (Right -> Root -> Left)      |
| Balance Skewed BST                | In-order extract to array -> Build via mid = (l+r)/2|
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Iterative Search (700)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Unidirectional `while` loop |
| **Iterative Insert (701)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Parent pointer leaf attachment |
| **Delete Node (450)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | $O(H)$ Stack Space | 3 Structural cases (findMin right)|
| **Inorder Successor (285)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Candidate record when turning LEFT |
| **Inorder Predecessor**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Candidate record when turning RIGHT|
| **Find Min / Max** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Leftmost / Rightmost link follow |
| **Find Floor / Ceiling**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | $O(N)$ (Skewed Tree) | **$O(1)$ Constant ⚡**| Candidate record on range match |
| **Validate BST (98)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | `Long` range bounds `(min, max)` |
| **Recover BST (99)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | In-Order swapped nodes recovery |
| **Optimal BST (OBST)**| **$O(N^3)$ Cubic ⚡** | **$O(N^3)$ Cubic ⚡** | **$O(N^3)$ Cubic ⚡** | $O(N^2)$ DP Table | Min expected search cost DP |
| **Unique BSTs I (96)** | **$O(N^2)$ Quadratic ⚡**| **$O(N^2)$ Quadratic ⚡**| **$O(N^2)$ Quadratic ⚡**| $O(N)$ DP Array | Catalan DP $C_N$ counting |
| **Balance BST (1382)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(N)$ Array Space | In-order extract + midpoint build |
| **Greater Tree (538)** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | $O(H)$ Stack Space | Reverse In-Order `Right -> Root -> Left`|

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for BST Nodes                                                    |
+-----------------------------------------------------------------------------------+
| Standard `TreeNode` Object          : 32 Bytes per Node (Header + 3 References)    |
| Augmented `BSTNode` (Count / Size) : 36 Bytes per Node (Header + 3 Refs + Int Count)|
| CPU Cache Performance               : Poor Cache Line Locality (Heap Pointer Chasing)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Iterative BST Search Loop
while (curr != null && curr.val != target) curr = (target < curr.val) ? curr.left : curr.right;

// 2. Validate BST Range Call Pattern
validateRange(node.left, minBound, node.val) && validateRange(node.right, node.val, maxBound);

// 3. 2-Child BST Deletion Line
TreeNode successor = findMin(root.right);
root.val = successor.val;
root.right = deleteNode(root.right, successor.val);

// 4. In-Order Successor Ancestor Record Line
if (p.val < curr.val) { successor = curr; curr = curr.left; } else curr = curr.right;

// 5. Balance BST Midpoint Build Line
int mid = left + (right - left) / 2;
TreeNode node = list.get(mid);
node.left = build(list, left, mid - 1); node.right = build(list, mid + 1, right);
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Local Parent-Child BST Validation**: Checking only `node.left.val < node.val` misses grand-ancestor violations. Always use `Long` range boundaries.
* **Pitfall 2: Integer.MIN_VALUE Validation Overflow**: Using `int` range bounds causes overflow when `node.val == Integer.MIN_VALUE`. Always use `Long.MIN_VALUE` and `Long.MAX_VALUE`.
* **Pitfall 3: Child Reference Re-assignment in Deletion**: Writing `deleteNode(root.left, key)` without assigning `root.left = deleteNode(root.left, key)` breaks parent-child linkage. Always assign return values.
* **Pitfall 4: Successor Candidate Recording**: Recording candidate successor when moving right is WRONG. Always record candidate successor ONLY when turning LEFT (`p.val < curr.val`).
* **Pitfall 5: Reverse In-Order for Greater Trees**: Standard In-Order (`Left -> Root -> Right`) visits ascending keys. Always use Reverse In-Order (`Right -> Root -> Left`) for $O(N)$ single-pass Greater Tree conversion.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 13 (BINARY SEARCH TREES)         |
+-----------------------------------------------------------------------+
| 1. BST Invariant   : Left Subtree < Root < Right Subtree (Global!)      |
| 2. In-Order Traversal: ALWAYS yields strictly ascending sorted array   |
| 3. Iterative Search: Runs in O(1) Auxiliary Space ⚡                    |
| 4. Validate BST (98): Pass Long range bounds (minBound, maxBound)     |
| 5. BST 2-Child Delete: Overwrite val with findMin(root.right).val     |
| 6. Successor (285) : Record candidate when turning LEFT (p.val < val) |
| 7. Predecessor     : Record candidate when turning RIGHT (p.val > val)|
| 8. Greater Tree    : Reverse In-Order DFS (Right -> Root -> Left)       |
| 9. Balance BST     : In-order extract to array -> Build via mid = (l+r)/2|
| 10. Unique BSTs (96): N-th Catalan Number C_N = (1/(N+1)) * (2N choose N)|
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can define the BST structural ordering invariant.
- [ ] I can write Iterative BST Search (LeetCode 700) in $O(1)$ space.
- [ ] I can write Iterative BST Insertion (LeetCode 701) in $O(1)$ space.
- [ ] I can write Delete Node in a BST (LeetCode 450) handling all 3 cases.
- [ ] I can write Inorder Successor in BST (LeetCode 285) in $O(1)$ space.
- [ ] I can write Inorder Predecessor in BST in $O(1)$ space.
- [ ] I can write Minimum, Maximum, Floor, and Ceiling operations in $O(1)$ space.
- [ ] I can write Validate BST (LeetCode 98) using `Long` range bounds.
- [ ] I can write Optimal BST (OBST) DP recurrence.
- [ ] I can write Unique BSTs Count (LeetCode 96) using Catalan DP.
- [ ] I can write Balance a Binary Search Tree (LeetCode 1382) in $O(N)$ time.
