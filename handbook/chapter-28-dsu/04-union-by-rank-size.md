# 04. Union by Rank & Union by Size: Height Bounding & $\alpha(N)$ Proofs

## 1. Introduction
**Union by Rank** and **Union by Size** are height-balancing heuristics for Disjoint Set Union (DSU) that prevent tree depth from growing out of control during `union(x, y)` operations. By attaching the root of the **shorter tree (smaller rank)** or **smaller component (smaller size)** under the root of the **taller/larger tree**, these heuristics guarantee that tree height $H$ NEVER exceeds $\mathbf{O(\log N)}$. When combined with **Path Compression**, DSU operations execute in **$\alpha(N) \approx O(1)$ Amortized Near-Constant Time**.

> **Important:** Union by Rank vs Union by Size Rules:
> 1. **Union by Rank (Height Upper Bound)**: `rank[i]` represents an upper bound on tree height.
>    - If `rank[rootX] < rank[rootY]`: Set `parent[rootX] = rootY`. (Height unchanged!).
>    - If `rank[rootX] > rank[rootY]`: Set `parent[rootY] = rootX`. (Height unchanged!).
>    - If `rank[rootX] == rank[rootY]`: Set `parent[rootY] = rootX` AND increment `rank[rootX]++`!
> 2. **Union by Size (Element Count)**: `size[i]` stores the exact number of elements in set $i$.
>    - Always attach smaller size set under larger size set (`parent[smaller] = larger`), and update `size[larger] += size[smaller]`! ⚡

```
Union by Rank Balancing Topology (Merging Tree X (rank 1) into Tree Y (rank 2)):
Tree X (rank 1):       Tree Y (rank 2):              Merged Result (Attach X under Y!):
      (1)                    (4)                                   (4) (rank 2 preserved!)
       |                    /   \                                 / | \
      (2)                 (5)   (6)                             (5)(6) (1)
                                                                        |
                                                                       (2)
Tree Y height remains 2! Tree height NEVER grows unnecessarily! ⚡
```

---

## 2. Core Concepts & Rank vs Size Heuristics Comparison

### 2.1 Architectural Comparison Matrix
```
Union Heuristics Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Heuristic Variant     | Metadata Array    | Merge Rule        | Height Bound $H$  |
+-----------------------+-------------------+-------------------+-------------------+
| **Union by Rank**     | `int[] rank`      | Attach lower rank | **$H \le \log_2 N$ ⚡**|
| **Union by Size**     | `int[] size`      | Attach lower size | **$H \le \log_2 N$ ⚡**|
| Naive Union           | None              | Arbitrary link    | $H = N$ (Skewed)  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Union by Rank/Size: Attach smaller tree under larger tree! Height H <= log2 N strictly guaranteed!"**

---

## 3. Characteristics & Mathematical Proof of $H \le \log_2 N$ Height Bound

### 3.1 Mathematical Proof of $O(\log N)$ Tree Height Bound
* **Claim**: A DSU tree of rank $R$ contains at least $2^R$ nodes.
* **Proof by Induction**:
  - Base Case $R = 0$: A tree of rank 0 has $2^0 = 1$ node.
  - Inductive Step: A tree's rank increases from $R$ to $R + 1$ IF AND ONLY IF two trees of equal rank $R$ are merged together.
  - Total nodes in merged tree $= \text{Nodes}(T_1) + \text{Nodes}(T_2) \ge 2^R + 2^R = 2 \cdot 2^R = 2^{R+1}$.
* Since total nodes $N \ge 2^R$, taking $\log_2$ on both sides yields:
  $$R \le \log_2 N \implies H \le \mathbf{O(\log N) \text{ Strict Height Bound!}}$$ ⚡

---

## 4. Internal Working Mechanics
Tracing Union by Rank on sets `{0, 1}` (rank 1) and `{2, 3, 4}` (rank 2):

```
Set 1: root 0, rank[0] = 1.
Set 2: root 2, rank[2] = 2.

Call union(1, 4):
- rootX = find(1) = 0 (rank 1).
- rootY = find(4) = 2 (rank 2).

Check Ranks:
- rank[0] (1) < rank[2] (2).
- Attach smaller rank root 0 under larger rank root 2: Set parent[0] = 2!
- rank[2] stays 2!

Tree height remains 2! Search time stays fast! ✅
```

---

## 5. Visual Diagram
Union by Size Component Tracking Topography:

```
Set A (size = 2):              Set B (size = 3):
      (0)                            (2)
       |                            /   \
      (1)                         (3)   (4)
               \               /
            Attach A under B!
                     (2) (size = 5)
                   /  |  \
                 (3) (4) (0)
                          |
                         (1)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Union by Rank and Union by Size DSU:

```java
import java.util.*;

public class UnionByRankSizeMaster {

    // 1. Union by Rank DSU Implementation
    public static class UnionByRankDSU {
        private final int[] parent;
        private final int[] rank;
        private int count;

        public UnionByRankDSU(int n) {
            this.count = n;
            this.parent = new int[n];
            this.rank = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0; // Initial rank is 0 for single node trees
            }
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        // Union by Rank O(alpha(N)) Time
        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX != rootY) {
                // Attach shorter tree under taller tree
                if (rank[rootX] < rank[rootY]) {
                    parent[rootX] = rootY;
                } else if (rank[rootX] > rank[rootY]) {
                    parent[rootY] = rootX;
                } else {
                    parent[rootY] = rootX;
                    rank[rootX]++; // Increment rank ONLY when equal rank trees merge!
                }
                count--;
            }
        }

        public boolean connected(int x, int y) { return find(x) == find(y); }
    }

    // 2. Union by Size DSU Implementation (Tracks Exact Component Sizes)
    public static class UnionBySizeDSU {
        private final int[] parent;
        private final int[] size;
        private int count;

        public UnionBySizeDSU(int n) {
            this.count = n;
            this.parent = new int[n];
            this.size = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                size[i] = 1; // Initial component size is 1
            }
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        // Union by Size O(alpha(N)) Time
        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX != rootY) {
                // Attach smaller component under larger component
                if (size[rootX] < size[rootY]) {
                    parent[rootX] = rootY;
                    size[rootY] += size[rootX]; // Accumulate component size
                } else {
                    parent[rootY] = rootX;
                    size[rootX] += size[rootY]; // Accumulate component size
                }
                count--;
            }
        }

        // Get size of component containing node i O(alpha(N)) Time
        public int getComponentSize(int i) {
            return size[find(i)];
        }

        public boolean connected(int x, int y) { return find(x) == find(y); }
    }
}
```

> **Quick Syntax:**
```java
// Union by Rank Equal Rank Case
if (rank[rootX] == rank[rootY]) { parent[rootY] = rootX; rank[rootX]++; }
```

---

## 7. Concrete Problem Examples
* **LeetCode 990 - Satisfiability of Equality Equations**: DSU with Union by Rank.
* **LeetCode 1568 - Minimum Number of Days to Disconnect Island**: Union by Size for island areas.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `UnionBySizeDSU` component size tracking:

```java
public class UnionByRankSizeDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Union by Size DSU Test ===");
        UnionByRankSizeMaster.UnionBySizeDSU dsu = 
            new UnionByRankSizeMaster.UnionBySizeDSU(5);

        dsu.union(0, 1);
        dsu.union(1, 2);

        System.out.println("Size of Component containing 0: " + 
            dsu.getComponentSize(0)); // Output: 3 (Set {0, 1, 2})

        System.out.println("Size of Component containing 3: " + 
            dsu.getComponentSize(3)); // Output: 1 (Set {3}) ✅
    }
}
```

---

## 9. Complexity Analysis

| DSU Implementation | `find(x)` Time | `union(x, y)` Time | Component Size Query | Auxiliary Space |
| :--- | :--- | :--- | :--- | :--- |
| **Union by Rank / Size Only**| $O(\log N)$ Logarithmic | $O(\log N)$ Logarithmic | **$O(1)$ Constant (Size)** | $O(N)$ Memory Arrays |
| **Path Compression + Rank**  | **$\alpha(N) \approx O(1)$ ⚡**| **$\alpha(N) \approx O(1)$ ⚡**| **$O(1)$ Constant (Size)** | $O(N)$ Memory Arrays |

---

## 10. Edge Cases & Boundary Handling
* **Merging Components of Equal Rank**: Rank of new root increases by $+1$.
* **Merging Components of Equal Size**: Arbitrarily attach one under the other and sum sizes.

---

## 11. Common Mistakes & Anti-Patterns
* **Incrementing Rank When Ranks Are Unequal**:
  - Incrementing `rank` when attaching a shorter tree under a taller tree artificially inflates rank values.
  - **ONLY increment `rank[rootX]++` when `rank[rootX] == rank[rootY]`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Union by Size is Preferred in Coding Interviews:
> Union by Size achieves the exact same $H \le \log_2 N$ height bound as Union by Rank, BUT also provides the size of any connected component (`size[find(x)]`) in **$O(1)$ constant time**!
> Many interview questions (e.g. "Find the size of the largest connected component") require component sizes, making **Union by Size** superior in practice! ⚡

> **Memory Trick:** **"Union by Size gives you component sizes for free in O(1) time!"**

---

## 13. System & Implementation Comparisons

| Feature | Union by Rank | Union by Size |
| :--- | :--- | :--- |
| **Metadata Array** | `int[] rank` (Height upper bound) | `int[] size` (Element count) |
| **Rank/Size Update** | Increments $+1$ ONLY on ties | Sums sizes: `size[A] += size[B]` |
| **Bonus Capability**| Height bounding | **Instant Component Size Queries $O(1)$ ⚡**|

---

## 14. How to Recognize This in Questions
* **"Find size of largest connected component in dynamic graph"** $\rightarrow$ DSU with Union by Size.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does a tree of rank $R$ contain at least $2^R$ nodes?**  
  *A:* Because rank increases by 1 IF AND ONLY IF two trees of equal rank $R$ are merged together, doubling the total number of nodes.
* **Q: How does `getComponentSize(x)` execute in $O(1)$ time in Union by Size?**  
  *A:* By looking up `size[find(x)]` where `size[root]` maintains the accumulated element count of the set.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: UNION BY RANK & UNION BY SIZE                         |
+-----------------------------------------------------------------------+
| • Height Bound : Strict H <= log2 N height bound guaranteed           |
| • Union Rank   : Attach shorter tree under taller tree                |
|                  Increment rank[rootX]++ ONLY if rank[X] == rank[Y]   |
| • Union Size   : Attach smaller size set under larger size set        |
|                  size[larger] += size[smaller]                        |
| • Combination  : Path Compression + Rank/Size = $\alpha(N) \approx O(1)$ ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Union by Rank in Java.
- [ ] I can write Union by Size with $O(1)$ component size lookup.
- [ ] I can prove why tree height $H \le \log_2 N$ under Union by Rank.
- [ ] I know why rank increases ONLY when equal ranks merge.
- [ ] I can trace Union by Size updates step by step.
