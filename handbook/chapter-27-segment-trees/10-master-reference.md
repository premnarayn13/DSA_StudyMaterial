# 10. Master Reference — Segment Trees

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, rotational mechanics, operational complexities, design patterns, and interview pitfalls for **Chapter 17: Segment Trees**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for dynamic range query algorithms and technical coding rounds.

> **Important:** Review this master reference 15 minutes before an interview to refresh the $4N$ Array Allocation Upper Bound, $O(N)$ Build Time, $O(\log N)$ Point Updates (LeetCode 307), 3 Overlap Query Cases (Total, None, Partial), Identity Base Elements (0, $\infty$, $-\infty$), Lazy Propagation `pushDown` Invariant, Dynamic Sparse Trees ($N=10^9$), and Coordinate Compression for LeetCode 315!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **$4N$ Array Allocation Formula**:
  - `tree = new int[4 * n];` strictly prevents index out-of-bounds errors for any input size $N$.
* **1D Heap-Style Child Index Formulas**:
  - `leftChild = 2 * treeIdx + 1;`
  - `rightChild = 2 * treeIdx + 2;`
  - `mid = l + (r - l) / 2;`
* **3 Overlap Query Cases Rules**:
  - **Case 1: Total Overlap ($qL \le L \text{ and } R \le qR$)**: `return tree[treeIdx];`
  - **Case 2: No Overlap ($R < qL \text{ or } L > qR$)**: `return Identity;`
  - **Case 3: Partial Overlap**: `return merge(query(left), query(right));`
* **Identity Elements by Query Function**:
  - Range Sum: $I = 0$. Range Minimum (RMQ): $I = \text{Integer.MAX\_VALUE}$. Range Maximum: $I = \text{Integer.MIN\_VALUE}$. Range GCD: $I = 0$.
* **Lazy Propagation PushDown Invariant**:
  - `if (lazy[i] != 0) { tree[i] += lazy[i] * (r - l + 1); if (l != r) { lazy[left] += lazy[i]; lazy[right] += lazy[i]; } lazy[i] = 0; }`

```
Segment Trees Master Formulas Summary:
+-----------------------------------+---------------------------------------------------+
| Structural Variant                | Invariant Rule / Formula                          |
+-----------------------------------+---------------------------------------------------+
| Memory Allocation Upper Bound     | new int[4 * n] (Strictly bounds 1D array size)    |
| Build Time Complexity             | O(N) Linear Time (Visits 2N - 1 nodes once) ⚡     |
| Point Update Time (LeetCode 307)  | O(log N) Time (Updates log2 N path ancestors) ⚡  |
| Range Query Time                  | O(log N) Time (Visits at most 4 * log2 N nodes) ⚡ |
| Lazy Range Update                 | O(log N) Time (Defers update via lazy[i] array) ⚡|
| Monoid Merge Requirement          | Associativity (A + B) + C = A + (B + C) & Identity|
+-----------------------------------+---------------------------------------------------+
```

---

## 3. Master Operations Complexity Table

| Operation / Problem | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`buildTree()`** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** | **$4N$ Array Space** | Post-order merge recursion |
| **Point Update (307)** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space | Path leaf update + ancestor merge |
| **Range Query ($qL, qR$)**| **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| $O(\log N)$ Call Stack Space | 3 Overlap case pruning |
| **Lazy Range Update** | **$O(1)$ Constant ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ Strict ⚡**| **$4N$ Lazy Array Space** | Deferred lazy[i] pushDown |
| **Range GCD Query** | **$O(1)$ Constant ⚡** | **$O(\log N \log V)$ ⚡** | **$O(\log N \log V)$ ⚡**| $O(\log N)$ Call Stack Space | Euclidean GCD monoid merge |
| **Dynamic Sparse Tree**| **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(\log N)$ ⚡** | **$O(Q \log N)$ Dynamic ⚡**| Dynamic node allocation ($10^9$) |
| **Smaller After (315)** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | **$O(N \log N)$ ⚡** | $O(N)$ Array Space | Compression + Backward SegTree |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Segment Trees                                                |
+-----------------------------------------------------------------------------------+
| Standard 1D `tree[]` Array           : 16 Bytes per $N$ elements ($4N \times 4$ Bytes)  |
| Lazy Propagation `lazy[]` Array      : 16 Bytes per $N$ elements ($4N \times 4$ Bytes)  |
| Total Memory for $N = 100,000$       : 3.2 MB Total Memory (Fits comfortably in L3 Cache)|
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Array Size Allocation Line
int[] tree = new int[4 * n];

// 2. Child Index Formulas
int mid = l + (r - l) / 2; int leftChild = 2 * treeIdx + 1; int rightChild = 2 * treeIdx + 2;

// 3. 3-Case Range Query Block
if (ql <= l && r <= qr) return tree[treeIdx]; // Case 1: Total Overlap
if (r < ql || l > qr) return Identity;       // Case 2: No Overlap
return merge(query(leftChild, l, mid, ql, qr), query(rightChild, mid + 1, r, ql, qr)); // Case 3: Partial

// 4. Point Update Directional Check Line
if (arrIdx <= mid) update(leftChild, l, mid, arrIdx, val);
else update(rightChild, mid + 1, r, arrIdx, val);
tree[treeIdx] = merge(tree[leftChild], tree[rightChild]);

// 5. Lazy PushDown Line
private void pushDown(int treeIdx, int l, int r) {
    if (lazy[treeIdx] != 0) {
        tree[treeIdx] += lazy[treeIdx] * (r - l + 1);
        if (l != r) { lazy[2*treeIdx+1] += lazy[treeIdx]; lazy[2*treeIdx+2] += lazy[treeIdx]; }
        lazy[treeIdx] = 0;
    }
}
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Allocating $2N$ Space Instead of $4N$**: Allocating $2N$ space causes out-of-bounds errors when $N$ is not a power of 2. Always allocate $4N$ array space (`new int[4 * n]`).
* **Pitfall 2: Returning `0` for Range Minimum Query (RMQ) No Overlap**: Returning `0` in RMQ masks positive and negative values. Always return `Integer.MAX_VALUE` for RMQ No Overlap!
* **Pitfall 3: Forgetting `pushDown` at Method Start**: Failing to call `pushDown(treeIdx, l, r)` at the first line of `queryRange` and `updateRange` reads stale values. Always call `pushDown` at method start!
* **Pitfall 4: Multiplying Lazy Value in Range Min/Max**: `lazyVal * (r - l + 1)` is used ONLY for Range Sum queries. For Range Min/Max queries, do not multiply by length.
* **Pitfall 5: Int Overflow for $N = 10^9$ Coordinate Math**: `(l + r) / 2` overflows 32-bit `int` when $r = 10^9$. Always use `long` coordinates (`l + (r - l) / 2`).

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 17 (SEGMENT TREES)               |
+-----------------------------------------------------------------------+
| 1. Space Allocation: ALWAYS allocate 4N space (new int[4 * n])        |
| 2. Build Complexity: O(N) Linear Time (Post-order merge of 2N-1 nodes)|
| 3. Point Update    : O(log N) Time (Updates log2 N path ancestors) ⚡  |
| 4. Range Query     : O(log N) Time (Total Overlap returns tree[i]) ⚡   |
| 5. Identities      : Sum = 0 | Min = Integer.MAX_VALUE | Max = MIN_VALUE|
| 6. Lazy Update     : O(log N) Time (Defers update via lazy[4N] array) ⚡|
| 7. Dynamic Sparse  : Allocate Node pointers dynamically for N = 10^9  |
| 8. LeetCode 315    : Compress ranks -> Backward traversal -> Query    |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write `buildTree` in Java in $O(N)$ time.
- [ ] I can write `update` (LeetCode 307) in Java in $O(\log N)$ time.
- [ ] I can write `query` with 3 overlap cases in $O(\log N)$ time.
- [ ] I can write a Segment Tree with Lazy Propagation in $O(\log N)$ time.
- [ ] I can write a Dynamic Sparse Segment Tree for $N = 10^9$.
- [ ] I can write LeetCode 315 (`Count of Smaller Numbers After Self`).
- [ ] I can write a Financial Stock Volatility Engine using dual Min/Max Segment Trees.
- [ ] I know why $4N$ space allocation is required.
