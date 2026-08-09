# 12. Kruskal's Minimum Spanning Tree Algorithm, Edge Sorting & DSU Forest Merging

## 1. Introduction
**Kruskal's Algorithm** is an edge-centric greedy Minimum Spanning Tree (MST) algorithm that constructs a Minimum Spanning Tree by sorting all global edges in ascending order of weight and adding them one by one, provided they **DO NOT FORM A CYCLE**. Invented by Joseph Kruskal in 1956, the algorithm uses **Disjoint Set Union (DSU / Union-Find)** to detect cycles and merge forest components in **$O(E \log E)$ Time** and **$O(V + E)$ Auxiliary Memory**.

> **Important:** The Core Invariants of Kruskal's Algorithm:
> 1. **Global Edge Sorting**: Sort all $E$ edges in non-decreasing order of weight ($w_1 \le w_2 \le \dots \le w_E$) in $O(E \log E)$ time.
> 2. **DSU Cycle Avoidance Invariant**: Iterate through sorted edges. Call `dsu.union(u, v)`:
>    - If `dsu.union(u, v)` returns `true` (nodes were in disjoint sets): Add edge to MST and accumulate weight!
>    - If `dsu.union(u, v)` returns `false` (nodes were already connected): **SKIP EDGE to avoid forming a cycle**!
> 3. **Termination Condition**: Stop early as soon as $V - 1$ edges are added to the MST! ⚡

```
Kruskal's Forest Merging Pipeline Topology:
Edges Sorted by Weight: (0-1: wt 1), (1-2: wt 1), (0-2: wt 3), (1-3: wt 6)

Forest State: {0}, {1}, {2}, {3}
1. Edge (0-1, wt 1): union(0, 1) succeeds ---> MST: {(0-1)}, Forest: {0,1}, {2}, {3}
2. Edge (1-2, wt 1): union(1, 2) succeeds ---> MST: {(0-1), (1-2)}, Forest: {0,1,2}, {3}
3. Edge (0-2, wt 3): union(0, 2) FAILS (0 & 2 already in set {0,1,2}!) ---> SKIP CYCLE EDGE!
4. Edge (1-3, wt 6): union(1, 3) succeeds ---> MST Complete! Total Weight = 8! ⚡
```

---

## 2. Core Concepts & Kruskal's vs Prim's MST Algorithms

### 2.1 MST Algorithm Comparison Matrix
```
Kruskal's vs Prim's Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | Kruskal's Algorithm| Prim's Algorithm | Best Performance  |
+-----------------------+-------------------+-------------------+-------------------+
| **Primary Structure** | **DSU / Union-Find ⚡**| Min-Heap PriorityQueue| DSU for Kruskal   |
| **Traversal Focus**   | Global Edges      | Local Tree Expansion| Nodes vs Edges    |
| **Sparse Graphs ($E \approx V$)**| **$O(E \log E)$ Optimal ⚡**| $O(E \log V)$ | **Kruskal's ⚡**  |
| **Disconnected Graph**| Finds Minimum Forest| Fails / Needs Loop| Kruskal's         |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Kruskal's Algorithm: Sort edges by weight -> Add edge if dsu.union(u, v) succeeds in O(E log E) time!"**

---

## 3. Characteristics & $O(E \log E)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(E \log E)$ Complexity
* Edge Sorting: Sorting $E$ edges takes $O(E \log E)$ time.
* DSU Operations: Iterating through $E$ edges performs at most $E$ `union()` calls taking $O(E \cdot \alpha(V)) \approx O(E)$ time.
* Total Time Complexity: $O(E \log E) + O(E \cdot \alpha(V)) = \mathbf{O(E \log E) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Kruskal's MST on Graph $V=4$ with Edges `(0-1, wt 1)`, `(0-2, wt 3)`, `(1-2, wt 1)`, `(1-3, wt 6)`:

```
Sorted Edges: [(0,1,1), (1,2,1), (0,2,3), (1,3,6)]. Init DSU parent = [0, 1, 2, 3].

Processing Edge (0, 1, wt 1):
- dsu.union(0, 1) returns true -> Add (0,1) to MST. totalWeight = 1. edgesAdded = 1.

Processing Edge (1, 2, wt 1):
- dsu.union(1, 2) returns true -> Add (1,2) to MST. totalWeight = 2. edgesAdded = 2.

Processing Edge (0, 2, wt 3):
- find(0) = 0, find(2) = 0 (Same root!). dsu.union(0, 2) returns false -> SKIP CYCLE!

Processing Edge (1, 3, wt 6):
- dsu.union(1, 3) returns true -> Add (1,3) to MST. totalWeight = 8. edgesAdded = 3 (V - 1!).

MST Complete! Total Minimum Weight = 8! ✅ (O(E log E) Time!)
```

---

## 5. Visual Diagram
Kruskal's Forest Component Merging Topography:

```
Step 1: Edge (0,1, wt 1) ---> Merge Component {0} and {1} -> {0, 1}
Step 2: Edge (1,2, wt 1) ---> Merge Component {0, 1} and {2} -> {0, 1, 2}
Step 3: Edge (0,2, wt 3) ---> SKIP! Both 0 and 2 belong to {0, 1, 2}
Step 4: Edge (1,3, wt 6) ---> Merge Component {0, 1, 2} and {3} -> {0, 1, 2, 3} ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Kruskal's Minimum Spanning Tree algorithm using DSU:

```java
import java.util.*;

// Kruskal's Minimum Spanning Tree Algorithm Master Class
public class KruskalsAlgorithmMaster {

    // Edge Representation
    public static class Edge implements Comparable<Edge> {
        public int u, v, weight;

        public Edge(int u, int v, int weight) {
            this.u = u;
            this.v = v;
            this.weight = weight;
        }

        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight); // Sort ascending by weight
        }
    }

    // Disjoint Set Union (DSU) with Path Compression & Union by Rank
    private static class DSU {
        private final int[] parent;
        private final int[] rank;

        public DSU(int n) {
            this.parent = new int[n];
            this.rank = new int[n];
            for (int i = 0; i < n; i++) parent[i] = i;
        }

        public int find(int i) {
            if (i == parent[i]) return i;
            return parent[i] = find(parent[i]); // Path Compression
        }

        public boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) return false; // Cycle detected!

            if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else {
                parent[rootY] = rootX;
                rank[rootX]++;
            }
            return true;
        }
    }

    // Kruskal's MST Algorithm O(E log E) Time, O(V + E) Space
    public int minSpanningTree(int numVertices, List<Edge> edges) {
        if (numVertices <= 0 || edges == null) return 0;

        // Step 1: Sort all global edges in ascending order of weight O(E log E)
        Collections.sort(edges);

        DSU dsu = new DSU(numVertices);

        int totalWeight = 0;
        int edgesAdded = 0;

        // Step 2: Process sorted edges using DSU cycle avoidance
        for (Edge edge : edges) {
            // Add edge IF AND ONLY IF dsu.union succeeds (no cycle formed!)
            if (dsu.union(edge.u, edge.v)) {
                totalWeight += edge.weight;
                edgesAdded++;

                // Step 3: Early termination when V - 1 edges are added
                if (edgesAdded == numVertices - 1) {
                    break;
                }
            }
        }

        // Verify if graph is fully connected
        return (edgesAdded == numVertices - 1) ? totalWeight : -1;
    }
}
```

> **Quick Syntax:**
```java
// Kruskal's Edge Loop Line
Collections.sort(edges);
if (dsu.union(edge.u, edge.v)) { totalWeight += edge.weight; edgesAdded++; }
```

---

## 7. Concrete Problem Examples
* **LeetCode 1584 - Min Cost to Connect All Points**: Kruskal's MST algorithm.
* **Network Infrastructure Cable Routing**: Connecting servers at minimum cost.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `minSpanningTree`:

```java
public class KruskalsAlgorithmDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Kruskal's MST Algorithm Test ===");
        KruskalsAlgorithmMaster solver = new KruskalsAlgorithmMaster();

        int n = 4;
        List<KruskalsAlgorithmMaster.Edge> edges = Arrays.asList(
            new KruskalsAlgorithmMaster.Edge(0, 1, 1),
            new KruskalsAlgorithmMaster.Edge(0, 2, 3),
            new KruskalsAlgorithmMaster.Edge(1, 2, 1),
            new KruskalsAlgorithmMaster.Edge(1, 3, 6)
        );

        int mstWeight = solver.minSpanningTree(n, edges);
        System.out.println("Minimum Spanning Tree Weight: " + mstWeight); // Output: 8 ✅
    }
}
```

---

## 9. Complexity Analysis

| MST Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Kruskal's Algorithm** | **$O(E \log E)$ Optimal ⚡**| **$O(V + E)$ Memory** | Edge sorting + DSU cycle check |
| **Prim's Algorithm** | $O(E \log V)$ | $O(V + E)$ Memory | Min-Heap priority queue |

---

## 10. Edge Cases & Boundary Handling
* **Disconnected Graph**: `edgesAdded < numVertices - 1` after loop returns `-1`.
* **$N = 1$ Single Vertex**: Returns weight `0` immediately.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting Edge Sorting Before Calling DSU `union()`**:
  - Processing edges in arbitrary un-sorted order builds a random spanning tree, NOT the Minimum Spanning Tree!
  - **ALWAYS sort edges ascending by weight (`Collections.sort(edges)`) BEFORE processing**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Kruskal's Algorithm Is Superior for Sparse Graphs:
> On sparse graphs where $E \approx V$, $O(E \log E) = O(V \log V)$ time.
> Kruskal's algorithm uses 10 lines of clean code (Sort edges + DSU union loop), making it the most popular MST choice in competitive programming! ⚡

> **Memory Trick:** **"Sort edges ascending -> add edge if dsu.union succeeds -> stop at V-1 edges!"**

---

## 13. System & Implementation Comparisons

| Feature | Kruskal's Algorithm | Prim's Algorithm |
| :--- | :--- | :--- |
| **Data Structure** | **Disjoint Set Union (DSU) ⚡**| Min-Heap PriorityQueue |
| **Edge Sorting** | **Global Pre-sorting $O(E \log E)$**| Local Heap Insertion |
| **Code Simplicity** | **High (Clean DSU Loop) ⚡** | Moderate |

---

## 14. How to Recognize This in Questions
* **"Find minimum weight connecting all graph vertices given list of weighted edges"** $\rightarrow$ Kruskal's MST.

---

## 15. Frequently Asked Interview Questions
* **Q: How does Kruskal's algorithm detect cycles?**  
  *A:* By attempting `dsu.union(u, v)`. If both nodes $u$ and $v$ already share the same DSU root, `union()` returns `false`, signaling a cycle.
* **Q: Why does Kruskal's algorithm stop when $V - 1$ edges are added?**  
  *A:* Because any tree connecting $V$ vertices contains exactly $V - 1$ edges.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: KRUSKAL'S ALGORITHM                                   |
+-----------------------------------------------------------------------+
| • Step 1: Sort all global edges ascending by weight (Collections.sort)|
| • Step 2: Initialize DSU with V vertices                              |
| • Step 3: For each edge (u, v, w): if (dsu.union(u, v)) add to MST!   |
| • Step 4: Early termination when edgesAdded == V - 1                  |
| • Performance: $O(E \log E)$ Time | $O(V + E)$ Space ⚡               |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Kruskal's algorithm in Java using DSU.
- [ ] I know why `Collections.sort(edges)` is mandatory.
- [ ] I know why $V-1$ edges complete a Minimum Spanning Tree.
- [ ] I can state the time complexity $O(E \log E)$.
- [ ] I can trace Kruskal's forest merging step by step.
