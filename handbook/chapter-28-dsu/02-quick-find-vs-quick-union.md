# 02. Quick Find vs Quick Union: Operational Trade-Offs & Complexity Benchmarks

## 1. Introduction
Before applying modern optimizations like Path Compression and Union by Rank, basic Disjoint Set Union (DSU) implementations fall into two classical operational categories: **Quick Find** and **Quick Union**. Quick Find prioritizes instant **$O(1)$ `find(x)` lookups** at the cost of slow **$O(N)$ `union(x, y)` scans**. Quick Union prioritizes fast **$O(1)$ tree root linking** during `union(x, y)` at the cost of **$O(H)$ tree path traversals** during `find(x)`.

> **Important:** The Classical DSU Architectural Trade-Off:
> 1. **Quick Find (`id[]` array)**: `id[i]` stores the exact Component ID of element $i$.
>    - `find(x)` $\to$ **$O(1)$ Constant Time**! (`return id[x]`).
>    - `union(x, y)` $\to$ **$O(N)$ Linear Time**! (Scans entire `id[]` array to change all instances of `id[rootX]` to `id[rootY]`).
> 2. **Quick Union (`parent[]` forest)**: `parent[i]` stores parent node index forming a tree forest.
>    - `find(x)` $\to$ **$O(H)$ Path Traversal Time** (Up to $O(N)$ for skewed trees).
>    - `union(x, y)` $\to$ **$O(H)$ Root Relinking Time** (`parent[rootX] = rootY`). ⚡

```
Quick Find vs Quick Union Internal Storage Topology:
Quick Find (Flat Array ID Mapping):          Quick Union (Parent Tree Forest):
id = [ 1, 1, 1, 3, 3 ]                       parent = [ 0, 0, 1, 3, 3 ]
       ^  ^  ^  ^  ^                                   (0)         (3)
Set 1: {0, 1, 2} | Set 3: {3, 4}                      /           /
                                                    (1)         (4)
find(x) takes 1 step!                             /
union(x,y) scans 5 elements!                    (2) -> find(2) takes 3 hops! ⚡
```

---

## 2. Core Concepts & Architectural Benchmarks

### 2.1 Trade-Off Comparison Matrix
```
Quick Find vs Quick Union Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| DSU Architecture      | `find(x)` Time    | `union(x, y)` Time| Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **Quick Find**        | **$O(1)$ Constant ⚡**| $O(N)$ Linear Scan| $O(N)$ Array      |
| **Quick Union**       | $O(H)$ Path Traversal| **$O(H)$ Root Link ⚡**| $O(N)$ Array |
| **Optimized DSU**     | **$\alpha(N) \approx O(1)$ ⚡**| **$\alpha(N) \approx O(1)$ ⚡**| $O(N)$ Array |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Quick Find = O(1) find, O(N) union! Quick Union = O(H) find, O(H) union!"**

---

## 3. Characteristics & $O(N^2)$ Sequence Degradation

### 3.1 Worst-Case Sequence Scenarios
* **Quick Find**: Executing $N$ `union()` operations takes $O(N \times N) = \mathbf{O(N^2) \text{ Quadratic Time}}$ regardless of tree geometry!
* **Quick Union**: Executing $N$ `union()` operations on pre-sorted elements (`union(0, 1)`, `union(1, 2)`) builds a linear tree of height $H = N$, degrading $N$ queries to $\mathbf{O(N^2) \text{ Quadratic Time}}$.

---

## 4. Internal Working Mechanics
Tracing `union(1, 4)` across Quick Find vs Quick Union on $N=5$:

```
Quick Find (id = [0, 0, 0, 3, 3]):
- rootX = id[1] = 0, rootY = id[4] = 3.
- Scan entire id[] array from 0 to 4:
  - Any element with id == 0 is changed to 3!
  - id becomes [3, 3, 3, 3, 3]. (Scanned 5 elements!).

Quick Union (parent = [0, 0, 0, 3, 3]):
- rootX = find(1) = 0, rootY = find(4) = 3.
- Set parent[0] = 3!
- parent becomes [3, 0, 0, 3, 3]. (Linked 1 pointer!).

Quick Union executed in 1 pointer write! ✅
```

---

## 5. Visual Diagram
Quick Find Flat Array vs Quick Union Tree Pointer Topography:

```
Quick Find Array Update:                       Quick Union Pointer Update:
id: [0, 0, 0, 3, 3]                            parent: [0, 0, 0, 3, 3]
     |  |  |  |  |  (Scan all 5 elements!)              |
id: [3, 3, 3, 3, 3]                            parent: [3, 0, 0, 3, 3] (Set parent[0] = 3)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Quick Find and Quick Union algorithms:

```java
import java.util.*;

public class QuickFindVsQuickUnionMaster {

    // 1. Quick Find Implementation (O(1) Find, O(N) Union)
    public static class QuickFindDSU {
        private final int[] id;
        private int count;

        public QuickFindDSU(int n) {
            this.count = n;
            this.id = new int[n];
            for (int i = 0; i < n; i++) id[i] = i;
        }

        // O(1) Instant Find
        public int find(int p) {
            return id[p];
        }

        // O(N) Linear Array Scan Union
        public void union(int p, int q) {
            int pID = find(p);
            int qID = find(q);
            if (pID == qID) return;

            // Scan entire array to update all instances of pID to qID
            for (int i = 0; i < id.length; i++) {
                if (id[i] == pID) {
                    id[i] = qID;
                }
            }
            count--;
        }

        public boolean connected(int p, int q) { return find(p) == find(q); }
    }

    // 2. Quick Union Implementation (O(H) Find, O(H) Union)
    public static class QuickUnionDSU {
        private final int[] parent;
        private int count;

        public QuickUnionDSU(int n) {
            this.count = n;
            this.parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        // O(H) Path Traversal Find
        public int find(int p) {
            while (p != parent[p]) {
                p = parent[p];
            }
            return p;
        }

        // O(H) Root Relinking Union
        public void union(int p, int q) {
            int rootP = find(p);
            int rootQ = find(q);
            if (rootP == rootQ) return;

            parent[rootP] = rootQ; // Single pointer update
            count--;
        }

        public boolean connected(int p, int q) { return find(p) == find(q); }
    }
}
```

> **Quick Syntax:**
```java
// Quick Find Union Scan Line
for (int i = 0; i < id.length; i++) if (id[i] == pID) id[i] = qID;
```

---

## 7. Concrete Problem Examples
* **Read-Heavy Static Query Systems**: Quick Find where `find()` queries vastly outnumber `union()`.
* **Dynamic Connection Streams**: Quick Union where `union()` requests arrive continuously.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Quick Find vs Quick Union:

```java
public class QuickFindVsQuickUnionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Quick Find vs Quick Union Benchmark Test ===");
        QuickFindVsQuickUnionMaster.QuickFindDSU qf = 
            new QuickFindVsQuickUnionMaster.QuickFindDSU(5);
        QuickFindVsQuickUnionMaster.QuickUnionDSU qu = 
            new QuickFindVsQuickUnionMaster.QuickUnionDSU(5);

        qf.union(0, 1); qf.union(1, 2);
        qu.union(0, 1); qu.union(1, 2);

        System.out.println("Quick Find find(2):  Component ID = " + qf.find(2)); // Output: 2 (O(1))
        System.out.println("Quick Union find(2): Root Node   = " + qu.find(2)); // Output: 2 (O(H))

        System.out.println("Are 0 and 2 connected in Quick Find?  " + qf.connected(0, 2)); // true
        System.out.println("Are 0 and 2 connected in Quick Union? " + qu.connected(0, 2)); // true ✅
    }
}
```

---

## 9. Complexity Analysis

| Architecture | `find(p)` Time | `union(p, q)` Time | `connected(p, q)` Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Quick Find** | **$O(1)$ Constant ⚡** | $O(N)$ Linear Scan | **$O(1)$ Constant ⚡** | $O(N)$ Memory Array |
| **Quick Union**| $O(H)$ Path Traversal | **$O(H)$ Root Link ⚡** | $O(H)$ Path Traversal | $O(N)$ Memory Array |

---

## 10. Edge Cases & Boundary Handling
* **$N = 100,000$ Elements**: Quick Find `union()` executes $100,000$ operations per call ($O(N^2)$ TLE!). Quick Union serves as the foundation for modern optimizations.

---

## 11. Common Mistakes & Anti-Patterns
* **Using Quick Find for Dynamic Edge Addition Problems**:
  - Scanning $N$ array elements on every `union()` call takes $O(N^2)$ time on large graphs.
  - **Never use unoptimized Quick Find for dynamic graph algorithms**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Quick Union Formed the Foundation for Modern DSU:
> Quick Find cannot be optimized beyond $O(N)$ union time because array scanning is fundamentally linear.
> Quick Union uses tree structures (`parent[]`), allowing Path Compression and Union by Rank to compress tree height $H$ down to $\alpha(N) \approx O(1)$!

> **Memory Trick:** **"Quick Union trees enable Path Compression to achieve O(1) time for BOTH find and union!"**

---

## 13. System & Implementation Comparisons

| Feature | Quick Find | Quick Union |
| :--- | :--- | :--- |
| **Data Structure** | Flat Array `id[]` | Parent Tree Forest `parent[]` |
| **`find(x)` Cost** | **Instant $O(1)$ ⚡** | Tree Path Traversal $O(H)$ |
| **`union(x, y)` Cost** | $O(N)$ Full Array Scan | **Single Pointer Write $O(H)$ ⚡**|

---

## 14. How to Recognize This in Questions
* **"Compare basic DSU architectures prior to path compression optimizations"** $\rightarrow$ Quick Find vs Quick Union.

---

## 15. Frequently Asked Interview Questions
* **Q: Why is Quick Find `union()` $O(N)$ linear time?**  
  *A:* Because it must iterate through every element $0 \dots N-1$ in the `id[]` array to overwrite all occurrences of `pID` with `qID`.
* **Q: Can Quick Union degrade to $O(N)$ time?**  
  *A:* Yes, if elements are linked sequentially (`0 -> 1 -> 2 -> 3`), creating a linear tree of height $H = N$.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: QUICK FIND VS QUICK UNION                             |
+-----------------------------------------------------------------------+
| • Quick Find : id[x] stores component ID; find O(1), union O(N) scan  |
| • Quick Union: parent[x] stores parent node; find O(H), union O(H)    |
| • Flaw       : Quick Find union is strictly O(N); cannot be optimized |
| • Solution   : Quick Union tree structure enables Path Compression! ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Quick Find in Java in $O(1)$ find / $O(N)$ union.
- [ ] I can write Quick Union in Java in $O(H)$ find / $O(H)$ union.
- [ ] I know why Quick Find `union()` takes $O(N)$ time.
- [ ] I know why Quick Union formed the foundation for Path Compression.
- [ ] I can trace `union()` step by step for Quick Find vs Quick Union.
