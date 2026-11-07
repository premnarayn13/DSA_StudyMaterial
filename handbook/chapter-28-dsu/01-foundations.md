# 01. Disjoint Set Union (DSU) Foundations, Equivalence Relations & Partitioning Invariants

## 1. Introduction
A **Disjoint Set Union (DSU)**—also known as a **Union-Find** data structure—manages a partition of a set of $N$ elements into non-overlapping (disjoint) dynamic subsets. Introduced by Bernard A. Galler and Michael J. Fischer in 1964, DSU efficiently supports two fundamental operations: **`find(x)`** (identifying the representative representative element/root of the set containing $x$) and **`union(x, y)`** (merging the sets containing elements $x$ and $y$). Equipped with path compression and union by rank/size, DSU executes both operations in **$\alpha(N) \approx O(1)$ Amortized Near-Constant Time** (where $\alpha$ is the Inverse Ackermann Function).

> **Important:** The Core Invariant & Mathematical Model of DSU:
> 1. **Partitioning Invariant**: The universe of $N$ elements is partitioned into disjoint subsets $S_1, S_2, \dots, S_K$ such that:
>    $$\bigcup_{i=1}^{K} S_i = \{0, 1, \dots, N-1\} \quad \text{and} \quad S_i \cap S_j = \emptyset \quad (\forall i \ne j)$$
> 2. **Canonical Representative (Root)**: Each set $S_i$ has a unique designated representative root element `find(x)`. Two elements $x$ and $y$ belong to the SAME set IF AND ONLY IF `find(x) == find(y)`! ⚡

```
DSU Disjoint Sets Partition Topology:
Universe = {0, 1, 2, 3, 4, 5, 6, 7}

Set S1 (Root 0):       Set S2 (Root 3):       Set S3 (Root 6):
      (0)                    (3)                    (6)
     /   \                  /                      /
   (1)   (2)              (4)                    (7)
                          /
                        (5)

find(1) = 0, find(2) = 0 -> 1 and 2 are CONNECTED!
find(1) = 0, find(5) = 3 -> 1 and 5 belong to DISJOINT sets! ⚡
```

---

## 2. Core Concepts & Equivalence Relations

### 2.1 Equivalence Relation Foundations
DSU models an **Equivalence Relation** ($\sim$) over elements:
* **Reflexivity**: $x \sim x$ (Every element is connected to itself).
* **Symmetry**: $x \sim y \iff y \sim x$ (Connection is undirected).
* **Transitivity**: $x \sim y \text{ and } y \sim z \implies x \sim z$ (Indirect connectivity propagation).

```
DSU Operational Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| DSU Operation         | Primary Goal      | Time Complexity   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| **`find(x)`**         | Return Root ID    | **$\alpha(N) \approx O(1)$ ⚡**| Path Compression  |
| **`union(x, y)`**     | Merge 2 Subsets   | **$\alpha(N) \approx O(1)$ ⚡**| Link roots by rank|
| **`connected(x, y)`** | Check set equality| **$\alpha(N) \approx O(1)$ ⚡**| `find(x) == find(y)`|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"DSU: find(x) returns set root ID; union(x, y) merges sets if find(x) != find(y)!"**

---

## 3. Characteristics & The Inverse Ackermann Function $\alpha(N)$

### 3.1 Extremely Slow Growth of $\alpha(N)$
The **Inverse Ackermann Function $\alpha(N)$** measures the operational complexity of DSU optimized with both Path Compression and Union by Rank:
* For all physical universe sizes up to $N = 10^{80}$ (estimated total atoms in the observable universe!):
  $$\alpha(N) \le 4$$
* For all practical engineering purposes, $\alpha(N)$ is **STRICTLY CONSTANT $O(1)$ TIME**! ⚡

---

## 4. Internal Working Mechanics
Tracing DSU set partition updates across `union(1, 2)` and `union(3, 4)`:

```
Init N = 5 elements: parent = [0, 1, 2, 3, 4]. Every element is its own root!

Call union(1, 2):
- root1 = find(1) = 1, root2 = find(2) = 2.
- Set parent[2] = 1. parent becomes [0, 1, 1, 3, 4].

Call union(2, 3):
- root1 = find(2) = 1, root2 = find(3) = 3.
- Set parent[3] = 1. parent becomes [0, 1, 1, 1, 4].

Check connected(1, 3): find(1) = 1, find(3) = 1 -> Connected (true)! ✅
```

---

## 5. Visual Diagram
DSU Parent Pointer Forest Topography:

```
Initial State (5 Disjoint Trees):          After union(1, 2), union(3, 4), union(1, 3):
(0)  (1)  (2)  (3)  (4)                                (1) <--- Component Root
                                                      /   \
                                                    (2)   (3)
                                                           |
                                                          (4)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing basic DSU foundations:

```java
import java.util.*;

public class DSUFoundationsMaster {

    private final int[] parent;
    private int count; // Number of connected components

    // Initialize DSU with N disjoint sets O(N) Time
    public DSUFoundationsMaster(int n) {
        this.count = n;
        this.parent = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i; // Every node is initially its own parent root
        }
    }

    // Basic Find (Unoptimized) O(H) Time
    public int find(int i) {
        while (i != parent[i]) {
            i = parent[i];
        }
        return i;
    }

    // Basic Union O(H) Time
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX != rootY) {
            parent[rootY] = rootX; // Link rootY to rootX
            count--; // Decrement total connected components
        }
    }

    // Check if x and y belong to the same set O(H) Time
    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }

    public int getCount() { return count; }
}
```

> **Quick Syntax:**
```java
// DSU Basic Find Loop Line
while (i != parent[i]) i = parent[i]; return i;
```

---

## 7. Concrete Problem Examples
* **Kruskal's Minimum Spanning Tree (MST)**: Cycle detection during edge selection.
* **LeetCode 547 - Number of Provinces**: Graph connected component counting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing DSU initialization, union, and connected component counting:

```java
public class DSUFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. DSU Foundations Test ===");
        DSUFoundationsMaster dsu = new DSUFoundationsMaster(5);

        System.out.println("Initial Component Count: " + dsu.getCount()); // Output: 5

        dsu.union(0, 1);
        dsu.union(1, 2);
        dsu.union(3, 4);

        System.out.println("Component Count AFTER Unions: " + dsu.getCount()); // Output: 2 (Set {0,1,2} and Set {3,4})
        System.out.println("Is 0 connected to 2? " + dsu.connected(0, 2)); // Output: true
        System.out.println("Is 0 connected to 4? " + dsu.connected(0, 4)); // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation (Basic DSU) | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **`find(x)`** | **$O(1)$ Constant ⚡** | $O(H)$ Tree Height | $O(N)$ (Skewed Line) | $O(1)$ Auxiliary Space |
| **`union(x, y)`** | **$O(1)$ Constant ⚡** | $O(H)$ Tree Height | $O(N)$ (Skewed Line) | $O(1)$ Auxiliary Space |
| **`connected(x, y)`**| **$O(1)$ Constant ⚡** | $O(H)$ Tree Height | $O(N)$ (Skewed Line) | $O(1)$ Auxiliary Space |

---

## 10. Edge Cases & Boundary Handling
* **`union(x, x)` (Same Element Union)**: `rootX == rootY`, operation returns immediately without mutating state.
* **`n = 1` Single Element DSU**: `count = 1`, `find(0) = 0`.

---

## 11. Common Mistakes & Anti-Patterns
* **Linking Uncompressed Pointers Directly**:
  - Writing `parent[y] = x` instead of `parent[rootY] = rootX` links child nodes instead of roots, corrupting DSU set structures!
  - **ALWAYS find roots first (`rootX = find(x)`, `rootY = find(y)`) before setting parent pointers**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why DSU Unoptimized Degrades to $O(N)$ Worst-Case:
> Without Path Compression or Union by Rank, performing sequential unions (`union(0, 1)`, `union(1, 2)`, `union(2, 3)`) constructs a linear linked list tree of height $H = N$.
> Future `find()` queries must traverse all $N$ links in **$O(N)$ linear time**. Optimization optimizations (Path Compression + Rank) are mandatory!

> **Memory Trick:** **"Always link roots (parent[rootY] = rootX), NEVER link non-root child nodes!"**

---

## 13. System & Implementation Comparisons

| Feature | Disjoint Set Union (DSU) | Adjacency List BFS/DFS |
| :--- | :--- | :--- |
| **Dynamic Edge Additions**| **Near-Instant $\alpha(N) \approx O(1)$ ⚡**| Requires Re-running BFS ($O(V + E)$) |
| **Connected Component Count**| **Maintained in $O(1)$ Constant Time ⚡**| Requires $O(V + E)$ Full Graph Scan |
| **Memory Footprint** | **Compact $O(N)$ `parent[]` Array ⚡**| $O(V + E)$ Adjacency Lists |

---

## 14. How to Recognize This in Questions
* **"Check dynamic graph connectivity or merge sets in near-constant time"** $\rightarrow$ DSU / Union-Find.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Inverse Ackermann Function $\alpha(N)$ value for $N = 10^{80}$?**  
  *A:* $\alpha(N) \le 4$, making operations effectively $O(1)$ constant time in practice.
* **Q: How does DSU maintain connected component count in $O(1)$ time?**  
  *A:* By initializing `count = N` and decrementing `count--` whenever `find(x) != find(y)` during a union operation.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DSU FOUNDATIONS                                       |
+-----------------------------------------------------------------------+
| • Representation : Array parent[N] where parent[i] points to parent   |
| • Root Node      : Node i is root IF AND ONLY IF parent[i] == i       |
| • Set Equality   : x and y in SAME set IF find(x) == find(y)          |
| • Union Action   : rootX = find(x); rootY = find(y); parent[rootY] = rootX|
| • Component Count: Track count; decrement on successful unions        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write basic DSU `find` and `union` in Java.
- [ ] I can state the DSU partitioning invariant.
- [ ] I know why parent pointers must link roots (`parent[rootY] = rootX`).
- [ ] I can state the value of Inverse Ackermann $\alpha(N)$ for practical $N$.
- [ ] I can track connected component count in $O(1)$ time.
