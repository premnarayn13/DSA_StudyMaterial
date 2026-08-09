# 07. Segment Tree Variations: Dynamic Sparse Trees, 2D Grid Trees & Persistence

## 1. Introduction
**Segment Tree Variations** extend classical array-based segment trees to handle massive coordinate ranges ($N = 10^9$), multi-dimensional matrix queries (2D Segment Trees), and historical time-travel queries (Persistent Segment Trees). By replacing fixed $4N$ flat arrays with **Dynamic Pointer Nodes** or **Version Copying**, variations execute range queries and updates across $10^9$ coordinate spaces in **$O(\log N)$ Time** and **$O(Q \log N)$ Auxiliary Memory**.

> **Important:** Core Segment Tree Variations:
> 1. **Dynamic Sparse Segment Tree ($N = 10^9$)**: Allocates node pointers dynamically ONLY when visited (`left = new Node()`), supporting coordinate ranges up to $N = 10^9$ in **$O(Q \log N)$ Memory**!
> 2. **2D Grid Segment Tree**: Statically nests a 1D Segment Tree inside every node of another 1D Segment Tree, querying $M \times N$ submatrix sums in **$O(\log M \cdot \log N)$ Time**!
> 3. **Persistent Segment Tree**: Creates a new version root for each update while sharing unchanged child subtrees, preserving all past $V$ versions of the array in **$O(O(1) + \log N)$ Memory per update**! ⚡

```
Dynamic Sparse Segment Tree Pointer Allocation Topology (Range [0 ... 10^9]):
                     [ Node Range 0 ... 10^9 ]  <--- Root (Index 0)
                    /                          \
   (Dynamically Allocated!)                 (null - Unvisited!)
 [ Node 0 ... 5*10^8 ]
```

---

## 2. Core Concepts & Dynamic Sparse Segment Tree Architecture

### 2.1 Dynamic Pointer-Based Segment Tree ($N = 10^9$)
When array range is $N = 10^9$:
* Flat array allocation `new int[4 * 10^9]` crashes with `OutOfMemoryError`!
* **Dynamic Pointer Solution**: Each `Node` contains `long sum`, `Node left`, and `Node right`.
* Nodes are instantiated lazily on-the-fly inside `updateRange` and `queryRange`.

```
Segment Tree Variations Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Variation Type        | Range Size $N$    | Memory Overhead   | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+
| **Dynamic Sparse Tree**| **$N = 10^9$ ⚡** | **$O(Q \log N)$ ⚡**| Huge ranges ($10^9$)|
| **2D Grid Tree**      | $M \times N$ Grid | $O(4M \cdot 4N)$  | Submatrix queries |
| **Persistent Tree**   | $V$ Array Versions| **$O(V \log N)$ ⚡**| Version time-travel|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Dynamic Sparse Tree: Instantiate child pointers dynamically to handle ranges up to 10^9!"**

---

## 3. Characteristics & Persistent Segment Trees

### 3.1 Persistent Segment Tree (Path Copying)
When updating an element at version $v$:
* Create a new version root node.
* Copy ONLY the path of $\log_2 N$ nodes from root to leaf.
* Unchanged subtrees point directly to nodes in previous versions!
* Total space added per update: **$O(\log N)$ nodes**.

---

## 4. Internal Working Mechanics
Tracing Dynamic Sparse Segment Tree Point Update for Range $[0 \dots 10^9]$ at index $X = 500$:

```
Root Range [0 ... 1,000,000,000]. Call update(500, val=10):
1. Root exists. mid = 500,000,000. arrIdx (500) <= mid -> Go Left.
   - If root.left is null: Instantiate root.left = new Node()!
2. Node [0 ... 500,000,000]: mid = 250,000,000. arrIdx (500) <= mid -> Go Left.
   - Instantiate node.left = new Node()!
3. Repeat binary search down to Leaf [500 ... 500].
4. Set leaf.sum = 10. Re-merge parent sums on return!

Allocated exactly 30 nodes for range 1,000,000,000! ✅ (O(log N) Time & Space!)
```

---

## 5. Visual Diagram
Dynamic Pointer Node Allocation Topography:

```
                  [ Root 0...10^9: Sum=10 ]
                 /                         \
  [ Node 0...5*10^8: Sum=10 ]             null (Unallocated!)
 /                           \
[ Node 0...2.5*10^8: Sum=10 ] null (Unallocated!)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of a Dynamic Sparse Segment Tree for ranges up to $N = 10^9$:

```java
import java.util.*;

// Dynamic Sparse Segment Tree for Large Coordinate Ranges [0 ... 10^9]
public class DynamicSegmentTreeMaster {

    public static class Node {
        public long sum;
        public long lazy;
        public Node left;
        public Node right;

        public Node() {
            this.sum = 0;
            this.lazy = 0;
            this.left = null;
            this.right = null;
        }
    }

    private final Node root;
    private final long N = 1000000000L; // Coordinate range [0 ... 10^9]

    public DynamicSegmentTreeMaster() {
        this.root = new Node();
    }

    private void pushDown(Node node, long l, long r) {
        if (node.lazy != 0) {
            long mid = l + (r - l) / 2;

            // Instantiate child pointer nodes dynamically on demand!
            if (node.left == null) node.left = new Node();
            if (node.right == null) node.right = new Node();

            node.left.sum += node.lazy * (mid - l + 1);
            node.left.lazy += node.lazy;

            node.right.sum += node.lazy * (r - mid);
            node.right.lazy += node.lazy;

            node.lazy = 0; // Clear lazy flag
        }
    }

    // Dynamic Range Update O(log N) Time, O(log N) Space per update
    public void updateRange(long ql, long qr, long val) {
        updateHelper(root, 0, N, ql, qr, val);
    }

    private void updateHelper(Node node, long l, long r, long ql, long qr, long val) {
        if (ql <= l && r <= qr) {
            node.sum += val * (r - l + 1);
            node.lazy += val;
            return;
        }

        pushDown(node, l, r);
        long mid = l + (r - l) / 2;

        if (ql <= mid) {
            if (node.left == null) node.left = new Node();
            updateHelper(node.left, l, mid, ql, qr, val);
        }

        if (qr > mid) {
            if (node.right == null) node.right = new Node();
            updateHelper(node.right, mid + 1, r, ql, qr, val);
        }

        long leftSum = (node.left != null) ? node.left.sum : 0;
        long rightSum = (node.right != null) ? node.right.sum : 0;
        node.sum = leftSum + rightSum;
    }

    // Dynamic Range Query O(log N) Time
    public long queryRange(long ql, long qr) {
        return queryHelper(root, 0, N, ql, qr);
    }

    private long queryHelper(Node node, long l, long r, long ql, long qr) {
        if (node == null || r < ql || l > qr) return 0;
        if (ql <= l && r <= qr) return node.sum;

        pushDown(node, l, r);
        long mid = l + (r - l) / 2;

        return queryHelper(node.left, l, mid, ql, qr) + 
               queryHelper(node.right, mid + 1, r, ql, qr);
    }
}
```

> **Quick Syntax:**
```java
// Dynamic Child Allocation Line
if (node.left == null) node.left = new Node();
```

---

## 7. Concrete Problem Examples
* **LeetCode 715 - Range Module**: Dynamic Segment Tree range tracking.
* **LeetCode 308 - Range Sum Query 2D - Mutable**: 2D Segment Tree matrix queries.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Dynamic Sparse Segment Tree over range $[0 \dots 10^9]$:

```java
public class DynamicSegmentTreeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Dynamic Sparse Segment Tree Test (N = 10^9) ===");
        DynamicSegmentTreeMaster segTree = new DynamicSegmentTreeMaster();

        System.out.println("Updating range [100 ... 500] by +5...");
        segTree.updateRange(100, 500, 5);

        System.out.println("Updating range [400 ... 1000] by +2...");
        segTree.updateRange(400, 1000, 2);

        System.out.println("Query Sum [100 ... 500]: " + 
            segTree.queryRange(100, 500)); // Output: 5*401 + 2*101 = 2207

        System.out.println("Query Sum [0 ... 1000000000]: " + 
            segTree.queryRange(0, 1000000000L)); // Output: 3227 ✅
    }
}
```

---

## 9. Complexity Analysis

| Variation Type | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Dynamic Sparse Tree** | **$O(\log N)$ Logarithmic ⚡**| **$O(Q \log N)$ Dynamic ⚡**| Allocates nodes lazily on demand |
| **2D Grid Tree** | **$O(\log M \log N)$ ⚡** | $O(4M \cdot 4N)$ Array Space| Nested 1D Segment Trees |
| **Persistent Tree** | **$O(\log N)$ Logarithmic ⚡**| **$O(V \log N)$ Version Space**| Path copying per update |

---

## 10. Edge Cases & Boundary Handling
* **Coordinates Near $10^9$**: Use 64-bit `long` indices to prevent 32-bit `int` overflow during `mid` calculation.
* **Unvisited Range Query**: Returns `0` immediately when `node == null`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using `int` for $N = 10^9$ Coordinate Math**:
  - `(l + r) / 2` overflows 32-bit `int` when $r = 10^9$.
  - **Use `long` for coordinate ranges ($l + (r - l) / 2$)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Dynamic Pointer Allocation Outperforms Coordinate Compression:
> Coordinate Compression requires pre-collecting all query coordinates upfront ($O(Q \log Q)$ offline processing).
> Dynamic Sparse Segment Trees operate **ONLINE in real time**, handling dynamic range queries up to $10^9$ without pre-sorting coordinates!

> **Memory Trick:** **"Dynamic Sparse Trees handle online queries up to 10^9 range without coordinate pre-sorting!"**

---

## 13. System & Implementation Comparisons

| Feature | Dynamic Sparse Segment Tree | Coordinate Compression + Array Tree |
| :--- | :--- | :--- |
| **Online / Offline** | **100% Online Processing ⚡** | Offline Only (Pre-collected points) |
| **Max Coordinate Range**| **$10^9 \dots 10^{18}$ ⚡** | Mapped to $2Q$ |
| **Memory Structure** | Dynamic Pointer Nodes | $4N$ Heap Array |

---

## 14. How to Recognize This in Questions
* **"Range query/update on sparse coordinates up to 10^9"** $\rightarrow$ Dynamic Sparse Segment Tree.

---

## 15. Frequently Asked Interview Questions
* **Q: How does a Persistent Segment Tree achieve $O(\log N)$ space per version update?**  
  *A:* By copying ONLY the $\log_2 N$ nodes along the update path while sharing unchanged child subtrees with previous versions.
* **Q: What is the maximum number of nodes allocated by a Dynamic Sparse Segment Tree for $Q$ queries on range $10^9$?**  
  *A:* At most $Q \times \lceil \log_2(10^9) \rceil \approx 30 Q$ nodes.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: SEGMENT TREE VARIATIONS (DYNAMIC SPARSE & PERSISTENT)  |
+-----------------------------------------------------------------------+
| • Dynamic Sparse : Allocate Node pointers dynamically for ranges 10^9  |
| • 2D Grid Tree   : Nested Segment Trees for O(log M * log N) submatrix |
| • Persistent Tree: Path copying creates array versions in O(log N) space|
| • Long Bounds    : Always use long for ranges near 10^9 (mid calculation)|
| • Performance    : O(log N) Time per query | O(Q log N) Memory Space ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write a Dynamic Sparse Segment Tree in Java for $N = 10^9$.
- [ ] I can write `pushDown` with dynamic pointer node allocation.
- [ ] I know why `long` coordinates are required for $N = 10^9$.
- [ ] I can explain Persistent Segment Tree path copying.
- [ ] I can trace dynamic node allocation for range updates.
