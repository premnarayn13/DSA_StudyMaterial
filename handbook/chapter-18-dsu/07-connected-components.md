# 07. Dynamic Connected Components, Island Merging (LeetCode 305) & Grid Partitioning

## 1. Introduction
Dynamic **Connected Component Tracking** is one of DSU's most frequent real-world design requirements. Unlike static BFS/DFS graph scans ($O(V + E)$ time per query), DSU maintains total active connected components and component sizes dynamically in **$O(1)$ Constant Time** as new land cells or edges are dynamically added. Problems like **Number of Islands II (LeetCode 305 - Dynamic Grid Merging)** and **Number of Provinces (LeetCode 547)** execute in **$O(K \cdot \alpha(M \cdot N))$ Near-Linear Time**.

> **Important:** Dynamic Grid DSU Mapping & Island Merging Rules (LeetCode 305):
> 1. **2D Grid to 1D ID Conversion**: Map 2D grid cell $(r, c)$ in an $M \times N$ grid to 1D DSU ID:
>    $$\text{id} = r \times N + c$$
> 2. **Land Addition Invariant**: When adding new land at $(r, c)$:
>    - Mark cell as land, initialize `parent[id] = id`, increment `count++`.
>    - Check 4 orthogonal neighbors (Up, Down, Left, Right).
>    - For each neighbor $(nr, nc)$ that IS LAND: call `dsu.union(id, neighborId)`.
>    - Each successful union automatically decrements `count--`! ⚡

```
Dynamic Island Merging Topology (Adding land at (0, 1) between (0, 0) and (0, 2)):
Initial State: Land at (0,0) [ID 0] and (0,2) [ID 2] ----> count = 2 islands.
Grid: [ (0)  water  (2) ]

Add Land at (0, 1) [ID 1]:
1. Add Land at ID 1 -----------------------------------> count = 3 islands!
2. Check Left Neighbor (0,0) [ID 0]: union(1, 0) -------> count = 2 islands!
3. Check Right Neighbor (0,2) [ID 2]: union(1, 2) ------> count = 1 merged island! ⚡
```

---

## 2. Core Concepts & LeetCode 305 Number of Islands II Architecture

### 2.1 LeetCode 305 Dynamic Island Merging Engine
Given grid dimensions $M \times N$ and a list of land positions `positions`:
1. Initialize DSU array of size $M \times N$.
2. Maintain boolean `grid[M][N]` initialized to `false` (water).
3. For each land coordinate `[r, c]` in `positions`:
   - If `grid[r][c]` is ALREADY land, add current island count to result.
   - Set `grid[r][c] = true`.
   - Increment `count++` (New isolated island created).
   - Check 4 directions `(r+1,c), (r-1,c), (r,c+1), (r,c-1)`:
     - If neighbor is inside grid AND `grid[nr][nc] == true`:
       - `dsu.union(r * N + c, nr * N + nc)` (If union succeeds, `count--`).
   - Add current `count` to `result` list!

```
Connected Component Problem Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Islands II (305)**  | Dynamic 2D DSU    | **$O(K \cdot \alpha(M \cdot N))$ ⚡**| $O(M \cdot N)$ DSU|
| **Provinces (547)**   | Adjacency Matrix  | **$O(N^2 \cdot \alpha(N))$ ⚡**| $O(N)$ DSU Array  |
| **Largest Island (827)**| Size Aggregation| **$O(M \cdot N \cdot \alpha(M \cdot N))$ ⚡**| $O(M \cdot N)$ DSU|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Grid DSU Formula: id = r * N + c! Add land -> count++ -> Check 4 neighbors -> union decrements count!"**

---

## 3. Characteristics & 2D Grid Offset Mapping

### 3.1 2D to 1D Coordinate Flattening Invariants
* 2D Cell Coordinates: Row $r \in [0 \dots M-1]$, Column $c \in [0 \dots N-1]$.
* Flattened 1D Index Formula: $\mathbf{\text{id} = r \times N + c}$.
* Reconstructing 2D Coordinates from 1D ID: $r = \text{id} / N$, $c = \text{id} \% N$.

---

## 4. Internal Working Mechanics
Tracing LeetCode 305 on $3 \times 3$ Grid with positions `[[0,0], [0,1], [1,2], [2,1]]`:

```
Grid Size 3x3 (N = 3). ID formula: id = r * 3 + c.

Pos [0, 0] (id 0): grid[0][0]=true. count = 1. 0 neighbors land. ans = [1].
Pos [0, 1] (id 1): grid[0][1]=true. count = 2.
  - Neighbor (0, 0) [id 0] is land -> union(1, 0) -> count = 1. ans = [1, 1].

Pos [1, 2] (id 5): grid[1][2]=true. count = 2. 0 neighbors land. ans = [1, 1, 2].
Pos [2, 1] (id 7): grid[2][1]=true. count = 3. 0 neighbors land. ans = [1, 1, 2, 3].

Final Output: [1, 1, 2, 3]! Executed in O(K) time! ✅
```

---

## 5. Visual Diagram
Dynamic Grid Land Union & Offset Direction Topography:

```
Direction Offsets: { {-1,0}, {1,0}, {0,-1}, {0,1} }

              (r-1, c) [Up]
                 |
(r, c-1) <--- (r, c) ---> (r, c+1) [Right]
  [Left]         |
              (r+1, c) [Down]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 305 (Number of Islands II) and LeetCode 547 (Number of Provinces):

```java
import java.util.*;

// LeetCode 305: Number of Islands II (Dynamic Grid DSU)
public class ConnectedComponentsMaster {

    private static class GridDSU {
        private final int[] parent;
        private final int[] rank;
        private int count;

        public GridDSU(int n) {
            this.parent = new int[n];
            this.rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
            this.count = 0;
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        public boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) return false;

            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
            count--; // Decrement island count on successful merge
            return true;
        }

        public void addLand() {
            count++; // Increment count when new land cell is added
        }

        public int getCount() { return count; }
    }

    // LeetCode 305 Solution O(K * alpha(M * N)) Time
    public List<Integer> numIslands2(int m, int n, int[][] positions) {
        List<Integer> result = new ArrayList<>();
        if (m <= 0 || n <= 0 || positions == null) return result;

        boolean[][] isLand = new boolean[m][n];
        GridDSU dsu = new GridDSU(m * n);

        int[][] directions = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        for (int[] pos : positions) {
            int r = pos[0];
            int c = pos[1];

            // If cell is already land, keep current count
            if (isLand[r][c]) {
                result.add(dsu.getCount());
                continue;
            }

            isLand[r][c] = true;
            dsu.addLand(); // New land cell added

            int currentId = r * n + c;

            // Check 4 orthogonal neighbors
            for (int[] dir : directions) {
                int nr = r + dir[0];
                int nc = c + dir[1];

                if (nr >= 0 && nr < m && nc >= 0 && nc < n && isLand[nr][nc]) {
                    int neighborId = nr * n + nc;
                    dsu.union(currentId, neighborId); // Merges land components
                }
            }

            result.add(dsu.getCount());
        }

        return result;
    }
}
```

> **Quick Syntax:**
```java
// 2D to 1D Grid Index Line
int id = r * n + c;
```

---

## 7. Concrete Problem Examples
* **LeetCode 305 - Number of Islands II**: Dynamic island merging.
* **LeetCode 547 - Number of Provinces**: Graph matrix connectivity.
* **LeetCode 827 - Making A Large Island**: Grid size aggregation with DSU.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 305 `numIslands2`:

```java
public class ConnectedComponentsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 305 Number of Islands II Test ===");
        ConnectedComponentsMaster solver = new ConnectedComponentsMaster();

        int m = 3, n = 3;
        int[][] positions = {{0,0}, {0,1}, {1,2}, {2,1}};

        List<Integer> islandCounts = solver.numIslands2(m, n, positions);
        System.out.println("Island Counts After Each Addition: " + islandCounts);
        // Output: [1, 1, 2, 3] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Islands II (305)**  | **$O(K \cdot \alpha(M \cdot N)) \approx O(K)$ ⚡**| **$O(M \cdot N)$ DSU Space**| Dynamic 2D DSU + neighbor union |
| **Provinces (547)**   | **$O(N^2 \cdot \alpha(N)) \approx O(N^2)$ ⚡**| **$O(N)$ DSU Space** | Matrix edge iteration |

---

## 10. Edge Cases & Boundary Handling
* **Duplicate Land Position in Inputs**: Handled safely by `if (isLand[r][c]) continue;` check.
* **Grid Cell Out of Bounds**: Handled by boundary guards `nr >= 0 && nr < m && nc >= 0 && nc < n`.

---

## 11. Common Mistakes & Anti-Patterns
* **Using 2D Arrays for Parent Pointer Storage**:
  - Allocating `int[][] parent = new int[M][N]` complicates Path Compression.
  - **ALWAYS convert 2D coordinates $(r, c)$ to 1D index `r * N + c` and use 1D arrays (`int[] parent`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why DSU is Mandatory for LeetCode 305 (Dynamic Islands):
> Standard BFS/DFS calculates island counts on a static grid in $O(M \cdot N)$ time.
> For $K$ sequential land additions, running BFS/DFS on every step takes $O(K \cdot M \cdot N)$ time (TLE penalty!).
> DSU processes each land addition dynamically in **$\alpha(M \cdot N) \approx O(1)$ time**, reducing total time to **$O(K)$ time**! ⚡

> **Memory Trick:** **"Static grid = BFS/DFS! Dynamic land additions = 2D DSU!"**

---

## 13. System & Implementation Comparisons

| Feature | Dynamic 2D DSU (LeetCode 305) | Static BFS/DFS Re-computation |
| :--- | :--- | :--- |
| **Query Mode** | **Dynamic Real-Time Stream ⚡**| Static Snapshot Only |
| **Time per Land Addition**| **$\alpha(M \cdot N) \approx O(1)$ Instant ⚡**| $O(M \cdot N)$ Full Grid Scan ❌ |
| **Overall Time** | **$O(K)$ Linear ⚡** | $O(K \cdot M \cdot N)$ (TLE) |

---

## 14. How to Recognize This in Questions
* **"Add land cells dynamically to a grid and query island count after each addition"** $\rightarrow$ LeetCode 305 (2D DSU).

---

## 15. Frequently Asked Interview Questions
* **Q: How are 2D grid coordinates $(r, c)$ mapped to a 1D DSU array index?**  
  *A:* Using the formula $\text{id} = r \times N + c$ (where $N$ is total number of columns).
* **Q: Why does adding a land cell initially increment `count++`?**  
  *A:* Because a new land cell forms an isolated island of size 1 before checking neighbor connections. Each successful union with adjacent land decrements `count--`.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DYNAMIC CONNECTED COMPONENTS (LEETCODE 305)           |
+-----------------------------------------------------------------------+
| • 2D to 1D Mapping: id = r * n + c                                    |
| • Land Addition   : grid[r][c] = true; dsu.addLand(); (count++)       |
| • Check 4 Directions: For each adjacent land cell, call dsu.union()   |
| • Auto Decrement  : Each successful union automatically does count--  |
| • Time Bounds     : O(K * alpha(M * N)) approx O(K) Total Time! ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 305 (`Number of Islands II`) in Java.
- [ ] I can convert 2D coordinates $(r, c)$ to 1D index `r * N + c`.
- [ ] I know why BFS/DFS TLEs on dynamic land addition streams.
- [ ] I can track component counts dynamically in $O(1)$ time.
- [ ] I can trace dynamic island merging step by step.
