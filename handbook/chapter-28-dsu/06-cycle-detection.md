# 06. Graph Cycle Detection, Redundant Connections & Kruskal MST Foundations

## 1. Introduction
Detecting cycles in undirected graphs is one of the premier algorithmic applications of **Disjoint Set Union (DSU)**. When processing a sequence of graph edges $(u, v)$ dynamically, if both vertices $u$ and $v$ **ALREADY BELONG TO THE SAME CONNECTED COMPONENT** (`find(u) == find(v)`), adding edge $(u, v)$ creates a **CLOSED CYCLE**! This invariant forms the backbone of **Redundant Connection (LeetCode 684)** and **Kruskal's Minimum Spanning Tree (MST)** algorithm, executing cycle checks in **$O(E \cdot \alpha(V)) \approx O(E)$ Near-Linear Time**.

> **Important:** The Cycle Detection Invariant of DSU:
> For any edge $(u, v)$ in an undirected graph:
> 1. Call `rootU = find(u)` and `rootV = find(v)`.
> 2. **If `rootU == rootV`**: Vertices $u$ and $v$ are already connected via a path. Edge $(u, v)$ completes a **CYCLE**! (Redundant Edge!).
> 3. **If `rootU != rootV`**: Vertices belong to disjoint components. Perform `union(u, v)` to merge components safely without forming a cycle! ⚡

```
DSU Cycle Detection Pipeline Topology:
Edges: (0, 1), (1, 2), (2, 0)
Step 1: Edge (0, 1) ---> find(0)=0, find(1)=1 (Disjoint!) ---> union(0, 1) [Set: {0, 1}]
Step 2: Edge (1, 2) ---> find(1)=0, find(2)=2 (Disjoint!) ---> union(1, 2) [Set: {0, 1, 2}]
Step 3: Edge (2, 0) ---> find(2)=0, find(0)=0 (MATCH! ALREADY CONNECTED!)
                         CYCLE DETECTED! Edge (2, 0) is the REDUNDANT EDGE! ⚡
```

---

## 2. Core Concepts & LeetCode 684 Redundant Connection Engine

### 2.1 LeetCode 684 Redundant Connection Algorithm
Given a 2D array of `edges` representing a connected graph that started as a tree with 1 additional edge creating 1 cycle:
1. Initialize DSU for $N$ vertices ($1 \dots N$).
2. Iterate through each edge `[u, v]` in `edges`:
   - If `!dsu.union(u, v)` (i.e. `find(u) == find(v)`):
     - Return edge `[u, v]` as the redundant edge!
3. Total Time: **$O(E \cdot \alpha(V))$ Time**, Space: **$O(V)$ Space**.

```
Cycle Detection Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Graph Problem         | Core Condition    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Redundant Edge (684)**| `!union(u, v)`   | **$O(E \cdot \alpha(V))$ ⚡**| $O(V)$ DSU Array  |
| **Kruskal's MST**     | Sort + Skip Cycle | **$O(E \log E)$ ⚡** | $O(V)$ DSU Array  |
| Directed Cycle        | DFS Colors        | $O(V + E)$        | $O(V)$ DFS Stack  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Cycle Detection: If find(u) == find(v), edge (u, v) creates a cycle!"**

---

## 3. Characteristics & Kruskal's MST Cycle Avoidance

### 3.1 Kruskal's Algorithm Minimum Spanning Tree
To build a Minimum Spanning Tree connecting $V$ vertices with minimum total edge weight:
1. Sort all $E$ edges by weight ascending ($O(E \log E)$).
2. Initialize DSU with $V$ vertices.
3. For each sorted edge $(u, v, \text{weight})$:
   - If `dsu.union(u, v)` succeeds (no cycle formed): Add edge to MST!
   - If `dsu.union(u, v)` fails (cycle formed): Skip edge!
4. Stop when MST contains $V - 1$ edges in **$O(E \log E)$ Time**.

---

## 4. Internal Working Mechanics
Tracing Redundant Connection (LeetCode 684) for Edges `[[1,2], [1,3], [2,3]]`:

```
Graph with 3 vertices. Initialize DSU parent = [0, 1, 2, 3].

Processing Edge [1, 2]:
- find(1) = 1, find(2) = 2. Disjoint! union(1, 2) -> parent[2] = 1.

Processing Edge [1, 3]:
- find(1) = 1, find(3) = 3. Disjoint! union(1, 3) -> parent[3] = 1.

Processing Edge [2, 3]:
- find(2) = 1, find(3) = 1. EQUAL ROOTS!
- union(2, 3) returns FALSE -> CYCLE DETECTED!

Edge [2, 3] is the Redundant Connection! ✅ (O(E * alpha(V)) Time!)
```

---

## 5. Visual Diagram
DSU Cycle Detection Topography:

```
Before Edge (2, 3):                     Adding Edge (2, 3):
       (1) <--- Root                            (1) <--- Root
      /   \                                    /   \
    (2)   (3)                                (2)---(3)  <--- CYCLE COMPLETED!
                                 Edge (2, 3) connects nodes in same component! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 684 (Redundant Connection) and Kruskal's Minimum Spanning Tree using DSU cycle detection:

```java
import java.util.*;

// LeetCode 684: Redundant Connection & Kruskal MST Master
public class DSUCycleDetectionMaster {

    private static class DSU {
        private final int[] parent;
        private final int[] rank;

        public DSU(int n) {
            this.parent = new int[n + 1];
            this.rank = new int[n + 1];
            for (int i = 0; i <= n; i++) parent[i] = i;
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        public boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) {
                return false; // Cycle detected! Nodes already connected.
            }

            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
            return true; // Successfully merged without cycle
        }
    }

    // LeetCode 684 Solution: Find Redundant Connection O(E * alpha(V)) Time
    public int[] findRedundantConnection(int[][] edges) {
        int n = edges.length;
        DSU dsu = new DSU(n);

        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];

            // If union fails, edge (u, v) forms a cycle!
            if (!dsu.union(u, v)) {
                return edge; // Return redundant cycle edge
            }
        }

        return new int[0];
    }

    // Kruskal's MST Algorithm using DSU O(E log E) Time
    public static class Edge implements Comparable<Edge> {
        public int u, v, weight;
        public Edge(int u, int v, int weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }

    public int minSpanningTreeWeight(int n, List<Edge> edges) {
        Collections.sort(edges); // Sort edges by weight ascending
        DSU dsu = new DSU(n);

        int totalWeight = 0;
        int edgesAdded = 0;

        for (Edge edge : edges) {
            // Add edge IF AND ONLY IF it does NOT form a cycle!
            if (dsu.union(edge.u, edge.v)) {
                totalWeight += edge.weight;
                edgesAdded++;
                if (edgesAdded == n - 1) break; // MST complete
            }
        }

        return (edgesAdded == n - 1) ? totalWeight : -1;
    }
}
```

> **Quick Syntax:**
```java
// DSU Cycle Detection Check Line
if (!dsu.union(u, v)) return edge; // Cycle detected!
```

---

## 7. Concrete Problem Examples
* **LeetCode 684 - Redundant Connection**: Primary cycle detection problem.
* **LeetCode 1584 - Min Cost to Connect All Points**: Kruskal MST with DSU.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 684 `findRedundantConnection`:

```java
public class DSUCycleDetectionDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 684 Redundant Connection Test ===");
        DSUCycleDetectionMaster solver = new DSUCycleDetectionMaster();

        int[][] edges = {{1, 2}, {1, 3}, {2, 3}};
        int[] redundantEdge = solver.findRedundantConnection(edges);

        System.out.println("Redundant Connection Edge: " + 
            Arrays.toString(redundantEdge)); // Output: [2, 3] ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Redundant Connection (684)**| **$O(E \cdot \alpha(V)) \approx O(E)$ ⚡**| **$O(V)$ DSU Space**| DSU `!union(u, v)` cycle check |
| **Kruskal's MST** | **$O(E \log E)$ Sorting ⚡**| **$O(V)$ DSU Space**| Sort edges + DSU cycle check |

---

## 10. Edge Cases & Boundary Handling
* **Self-Loops (`u == v`)**: `find(u) == find(v)` triggers cycle detection immediately on the self-loop edge.
* **Disconnected Graphs**: Kruskal MST checks `edgesAdded == n - 1` to confirm full spanning tree connectivity.

---

## 11. Common Mistakes & Anti-Patterns
* **Using DSU for Directed Graph Cycle Detection**:
  - DSU assumes undirected connectivity ($u \to v$ implies $v \to u$).
  - **Do NOT use standard DSU for directed graph cycle detection (use Tarjan's or Kahn's Topological Sort instead)**!

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** DSU Cycle Detection Applicability Limit:
> DSU cycle detection works EXCLUSIVELY on **UNDIRECTED GRAPHS**.
> In undirected graphs, if two nodes are already connected in DSU, any additional edge between them MUST close a cycle loop.
> For directed graphs, cycles require directional path tracing via **DFS Colors (White/Gray/Black)** or **Kahn's In-Degree Topological Sort**! ⚡

> **Memory Trick:** **"DSU cycle detection is ONLY for undirected graphs! Use Topological Sort for directed graphs!"**

---

## 13. System & Implementation Comparisons

| Feature | DSU Cycle Detection | DFS Cycle Detection |
| :--- | :--- | :--- |
| **Graph Type** | **Undirected Graphs Only** | Undirected & Directed Graphs |
| **Edge Stream** | **Dynamic Edge Stream $O(\alpha(V))$ ⚡**| Static Graph Only $O(V + E)$ |
| **Kruskal Integration**| **Native 1-Line Check (`!union`) ⚡**| Requires full DFS traversal |

---

## 14. How to Recognize This in Questions
* **"Find redundant edge creating a cycle in undirected graph"** $\rightarrow$ LeetCode 684 (DSU Cycle Detection).

---

## 15. Frequently Asked Interview Questions
* **Q: How does DSU detect cycles in an undirected graph?**  
  *A:* By checking if `find(u) == find(v)` prior to inserting edge $(u, v)$. If roots match, nodes $u$ and $v$ are already connected, so edge $(u, v)$ closes a cycle.
* **Q: Why is DSU cycle detection preferred for Kruskal's MST?**  
  *A:* Because DSU evaluates cycle creation in near-constant $O(\alpha(V))$ time per edge, allowing Kruskal MST to run in $O(E \log E)$ time.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRAPH CYCLE DETECTION & KRUSKAL MST                   |
+-----------------------------------------------------------------------+
| • Cycle Rule     : Edge (u, v) forms a cycle IF AND ONLY IF find(u) == find(v)|
| • Union Check    : If (!dsu.union(u, v)) -> CYCLE DETECTED!           |
| • LeetCode 684   : Iterate edges; first failed union is redundant edge|
| • Kruskal MST    : Sort edges by weight; add edge IF dsu.union succeeds|
| • Limit          : DSU cycle detection applies ONLY to UNDIRECTED graphs!|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 684 (`Redundant Connection`) in Java.
- [ ] I can write Kruskal's MST using DSU.
- [ ] I know why DSU cycle detection applies ONLY to undirected graphs.
- [ ] I know why `!dsu.union(u, v)` signals a cycle.
- [ ] I can trace cycle detection step by step.
