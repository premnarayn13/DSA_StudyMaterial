# 03. Path Compression Engine, Tree Flattening Invariants & Path Halving

## 1. Introduction
**Path Compression** is the single most powerful optimization for Disjoint Set Union (DSU). During a `find(x)` query, Path Compression **FLATTENS THE TREE TOPOLOGY** by re-pointing every node traversed along the search path directly to the root representative element. Re-pointing ancestors during `find(x)` reduces future lookup paths for all traversed elements to **$O(1)$ Direct Hop Links**, driving amortized operational query time down to **$O(\log N)$ Time** (standalone) and **$\alpha(N) \approx O(1)$ Time** (when combined with Union by Rank/Size).

> **Important:** The 2-Pass & 1-Pass Path Compression Invariants:
> 1. **Recursive 2-Pass Path Compression**: `parent[i] = find(parent[i])`.
>    - Pass 1: Traverses upward to find the root element.
>    - Pass 2: Unwinds call stack, updating `parent[i]` for every node along the path to point directly to root!
> 2. **Iterative 1-Pass Path Halving**: `parent[i] = parent[parent[i]]`.
>    - Updates parent pointers while traversing upward, cutting path lengths in half during a single pass without call stack recursion! ⚡

```
Recursive Path Compression Flattening Topology:
Before find(4):                             After find(4) (Tree Flattened!):
        (0) <--- Root                               (0) <--- Root
         |                                       / / | \
        (1)                                    (1)(2)(3)(4)
         |
        (2)                                 Every node now points directly to Root 0!
         |                                  Future find(4), find(3), find(2) take 1 hop! ⚡
        (3)
         |
        (4)
```

---

## 2. Core Concepts & Recursive vs Iterative Path Compression

### 2.1 Implementation Mechanics Comparison
```
Path Compression Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Path Compression Mode | Code Line         | Passes Required   | Call Stack Risk   |
+-----------------------+-------------------+-------------------+-------------------+
| **Recursive 2-Pass**  | `parent[i] = find(parent[i])` | 2 Passes (Down/Up)| Low ($H \le \log N$)|
| **Iterative Halving** | `parent[i] = parent[parent[i]]`| **1 Pass ⚡**   | **Zero Stack ⚡**  |
| Unoptimized DSU       | `return find(parent[i])` | 1 Pass (No Update)| High (Skewed $N$) |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Path Compression: parent[i] = find(parent[i]) flattens the tree during find(i)!"**

---

## 3. Characteristics & Amortized Cost Distribution

### 3.1 Amortized Complexity Property
* The first `find(x)` call on a deep tree of height $H$ takes $O(H)$ time to traverse.
* However, that single call **FLATTENS all $H$ nodes** directly to the root.
* The next $H - 1$ subsequent `find()` queries on those nodes execute in **$O(1)$ Instant Constant Time**!
* Total Amortized Complexity: **$O(\log N)$ Amortized Time** per operation.

---

## 4. Internal Working Mechanics
Tracing Recursive Path Compression `find(4)` on Tree `0 -> 1 -> 2 -> 3 -> 4`:

```
Call find(4):
1. parent[4] = 3 (!= 4) -> Call find(3).
2. parent[3] = 2 (!= 3) -> Call find(2).
3. parent[2] = 1 (!= 2) -> Call find(1).
4. parent[1] = 0 (!= 1) -> Call find(0).
5. parent[0] == 0 -> BASE CASE REACHED! Return Root 0.

Unwinding Call Stack (Path Compression Assignments):
- parent[1] = 0. Returns 0.
- parent[2] = 0. Returns 0. (Re-pointed 2 to 0!)
- parent[3] = 0. Returns 0. (Re-pointed 3 to 0!)
- parent[4] = 0. Returns 0. (Re-pointed 4 to 0!)

Tree flattened! parent array becomes [0, 0, 0, 0, 0]! ✅ (Instant O(1) future lookups!)
```

---

## 5. Visual Diagram
Tree Structure Before vs After Path Compression Topography:

```
Before find(4):                   After find(4):
      (0)                              (0)
       |                            / / | \
      (1)                         (1)(2)(3)(4)
       |
      (2)                        parent[] array:
       |                         [0, 0, 0, 0, 0]
      (3)
       |
      (4)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Recursive 2-Pass Path Compression and Iterative 1-Pass Path Halving DSU:

```java
import java.util.*;

public class PathCompressionMaster {

    // 1. Recursive 2-Pass Path Compression DSU
    public static class RecursivePathCompressionDSU {
        private final int[] parent;
        private int count;

        public RecursivePathCompressionDSU(int n) {
            this.count = n;
            this.parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        // Recursive Path Compression find(i) O(log N) Amortized
        public int find(int i) {
            if (i == parent[i]) {
                return i;
            }
            // Path Compression Assignment: Flattens tree on return path!
            return parent[i] = find(parent[i]);
        }

        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX != rootY) {
                parent[rootY] = rootX;
                count--;
            }
        }

        public boolean connected(int x, int y) { return find(x) == find(y); }
        public int getCount() { return count; }
    }

    // 2. Iterative 1-Pass Path Halving DSU (Zero Call Stack Memory)
    public static class IterativePathHalvingDSU {
        private final int[] parent;
        private int count;

        public IterativePathHalvingDSU(int n) {
            this.count = n;
            this.parent = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        // Iterative Path Halving find(i) O(log N) Amortized
        public int find(int i) {
            while (i != parent[i]) {
                parent[i] = parent[parent[i]]; // Make node point to its grandparent!
                i = parent[i];
            }
            return i;
        }

        public void union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);
            if (rootX != rootY) {
                parent[rootY] = rootX;
                count--;
            }
        }

        public boolean connected(int x, int y) { return find(x) == find(y); }
    }
}
```

> **Quick Syntax:**
```java
// Path Compression Line
public int find(int i) { if (i == parent[i]) return i; return parent[i] = find(parent[i]); }
```

---

## 7. Concrete Problem Examples
* **LeetCode 547 - Number of Provinces**: High-speed connected component counting.
* **LeetCode 684 - Redundant Connection**: Cycle detection with path compression.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Recursive Path Compression DSU:

```java
public class PathCompressionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Path Compression DSU Test ===");
        PathCompressionMaster.RecursivePathCompressionDSU dsu = 
            new PathCompressionMaster.RecursivePathCompressionDSU(5);

        dsu.union(0, 1);
        dsu.union(1, 2);
        dsu.union(2, 3);
        dsu.union(3, 4);

        System.out.println("Executing find(4) (Flattens tree)... Root = " + dsu.find(4)); // Output: 0

        System.out.println("Is 4 connected to 0? " + dsu.connected(4, 0)); // Output: true (Instant O(1))
        System.out.println("Total Connected Components: " + dsu.getCount()); // Output: 1 ✅
    }
}
```

---

## 9. Complexity Analysis

| DSU Variant | `find(x)` Time | `union(x, y)` Time | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Path Compression Only** | **$O(\log N)$ Amortized ⚡**| **$O(\log N)$ Amortized ⚡**| $O(N)$ Memory Array |
| **Path Compression + Rank**| **$\alpha(N) \approx O(1)$ ⚡** | **$\alpha(N) \approx O(1)$ ⚡** | $O(N)$ Memory Array |

---

## 10. Edge Cases & Boundary Handling
* **Finding Root Node (`i == parent[i]`)**: Recursion base case hits immediately, returning `i` in $O(1)$ time.
* **Fully Flattened Tree**: Subsequent `find()` calls return root in 1 hop.

---

## 11. Common Mistakes & Anti-Patterns
* **Writing `return find(parent[i])` Without Assignment**:
  - Forgetting the assignment (`parent[i] = find(...)`) traverses the tree WITHOUT saving parent shortcuts, completely disabling Path Compression!
  - **ALWAYS assign `return parent[i] = find(parent[i])`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `parent[i] = find(parent[i])` Flattens Trees:
> By assigning `parent[i]` to the return value of `find(parent[i])`, the return value propagates the root ID backwards down the call stack.
> Every single node along the search path has its `parent[node]` pointer updated to the root ID, converting a tall tree of height $H$ into a flat 1-level star graph! ⚡

> **Memory Trick:** **"One line flattens everything: return parent[i] = find(parent[i]);"**

---

## 13. System & Implementation Comparisons

| Feature | Recursive Path Compression | Iterative Path Halving |
| :--- | :--- | :--- |
| **Code Simplicity** | **1-Line Elegant Assignment ⚡**| Loop with grandparent step |
| **Pass Count** | 2 Passes (Down/Up) | **1 Pass (Upward only) ⚡** |
| **Call Stack Memory**| Uses Recursion Stack | **Zero Auxiliary Stack Memory ⚡**|

---

## 14. How to Recognize This in Questions
* **"Optimize Union-Find tree depth during set queries"** $\rightarrow$ Path Compression.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the time complexity of DSU with Path Compression alone (without Union by Rank)?**  
  *A:* $O(\log N)$ amortized time per operation.
* **Q: How does iterative Path Halving work?**  
  *A:* By executing `parent[i] = parent[parent[i]]` inside a `while (i != parent[i])` loop, re-pointing every node to its grandparent during a single upward pass.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PATH COMPRESSION MECHANICS                            |
+-----------------------------------------------------------------------+
| • One-Liner Rule : return parent[i] = find(parent[i]);                |
| • Tree Flattening: Re-points ALL nodes along search path to Root 0    |
| • Amortized Speed: O(log N) standalone | $\alpha(N) \approx O(1)$ with Rank|
| • Path Halving   : parent[i] = parent[parent[i]] (Iterative 1-pass)   |
| • Performance    : Eliminates deep tree traversals for all future queries!|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write 1-line Path Compression `find(i)` in Java.
- [ ] I can write 1-pass iterative Path Halving `find(i)`.
- [ ] I know why Path Compression flattens trees.
- [ ] I know the amortized time bounds with and without Union by Rank.
- [ ] I can trace tree flattening during `find(4)` step by step.
