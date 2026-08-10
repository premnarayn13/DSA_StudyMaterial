# 06. Minimum Spanning Trees: Kruskal's, Prim's & Cut/Cycle Property Proofs

## 1. Introduction
A **Minimum Spanning Tree (MST)** is a fundamental graph optimization structure defined over a connected, undirected weighted graph $G = (V, E, W)$. An MST is a subset of edges $T \subseteq E$ that connects all $V$ vertices together without forming any cycles, while minimizing the total edge weight sum $W(T) = \sum_{e \in T} w(e)$. An MST over a graph with $V$ vertices contains exactly **$V - 1$ Edges**. Two primary greedy algorithms construct MSTs:
1. **Kruskal's Algorithm**: An **Edge-Centric Greedy Strategy** that sorts all $E$ edges in non-decreasing weight order and adds edges sequentially using **Disjoint-Set Union (DSU / Union-Find)** to prevent cycles in **$O(E \log E)$ Time Complexity**.
2. **Prim's Algorithm**: A **Vertex-Centric Greedy Strategy** that grows a single tree from an arbitrary root vertex, greedily adding the cheapest edge crossing the cut between visited and unvisited vertices using a **Min-Heap (Priority Queue)** in **$O(E \log V)$ Time Complexity**.

> **Important:** Core Structural Invariants of Minimum Spanning Trees:
> 1. **Cut Property (Greedy Choice Property)**:
>    - For ANY cut $(S, V \setminus S)$ dividing vertices into two disjoint sets, the **lightest (cheapest) edge crossing the cut** MUST belong to the Minimum Spanning Tree!
> 2. **Cycle Property**:
>    - For ANY cycle $C$ in graph $G$, the **heaviest (most expensive) edge in the cycle** CANNOT belong to any Minimum Spanning Tree!
> 3. **Spanning Tree Edge Invariant**:
>    - An MST over $V$ vertices contains EXACTLY $V - 1$ edges. Adding any edge creates a unique cycle; removing any edge disconnects the graph. ⚡

```
Kruskal's vs Prim's MST Greedy Strategies:

Kruskal's Edge-Centric Greedy:
1. Sort all edges by weight: e1(1), e2(2), e3(3)...
2. Pick lightest edge e1. If DSU find(u) != find(v) -> Add edge & Union!
3. Repeat until V - 1 edges are added. (Handles disconnected forests!) ⚡

Prim's Vertex-Centric Greedy:
1. Start at Vertex 0. Mark visited.
2. Push all outgoing edges of Vertex 0 to Min-Heap.
3. Pop cheapest edge (u, v, w). If v is unvisited: Mark v visited, add edge, push v's edges! ⚡
```

---

## 2. Core Concepts & MST Algorithm Strategy Matrix

### 2.1 Kruskal's vs Prim's Strategy Matrix
```
MST Algorithm Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| MST Algorithm         | Primary Invariant | Time Complexity   | Auxiliary Space   | Graph Suitability |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Kruskal's (DSU)**   | Edge Weight Sort  | **$O(E \log E)$ ⚡**| **$O(V + E)$ DSU ⚡**| **Sparse Graphs ($E \approx V$)⚡**|
| **Prim's (Min-Heap)** | Cut Crossing Edge | **$O(E \log V)$ ⚡**| **$O(V + E)$ Heap⚡**| **Dense Graphs ($E \approx V^2$)⚡**|
| **Prim's (Matrix)**   | Adjacency Matrix  | $O(V^2)$          | $O(V)$ Distance   | Complete Graphs   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Kruskal sorts edges and uses DSU (Best for Sparse graphs); Prim grows tree from root using Min-Heap (Best for Dense graphs)!"**

---

## 3. Characteristics & Cut Property Mathematical Proof

### 3.1 Mathematical Proof of Cut Property
* **Theorem**: Let $G = (V, E, W)$ be a weighted connected graph. Let $(S, V \setminus S)$ be any cut of $G$. Let $e = (u, v)$ be the lightest edge crossing the cut (i.e. $u \in S, v \in V \setminus S$). Then $e$ belongs to an MST of $G$.
* **Proof via Exchange Argument**:
  1. Assume there exists an MST $T$ that does NOT contain edge $e$.
  2. Adding edge $e = (u, v)$ to $T$ creates a unique cycle $C$.
  3. Since $u \in S$ and $v \in V \setminus S$, cycle $C$ MUST cross the cut $(S, V \setminus S)$ at least once more at another edge $e' = (u', v')$ where $u' \in S, v' \in V \setminus S$.
  4. Replace $e'$ with $e$ to form a new spanning tree $T' = T \cup \{e\} \setminus \{e'\}$.
  5. Compare edge weights: Since $e$ is the lightest edge crossing the cut, $w(e) \le w(e')$.
  6. Total Weight: $W(T') = W(T) - w(e') + w(e) \le W(T)$.
  7. Since $T$ was an MST, $W(T') = W(T)$, proving that $T'$ is also an MST containing edge $e$! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Kruskal vs Prim Execution

Tracing Kruskal's vs Prim's on Graph: Vertices {0, 1, 2, 3}, Edges: (0-1: 1), (1-2: 4), (0-2: 3), (2-3: 2), (1-3: 5):

```
Kruskal's Execution:
1. Sort Edges: (0-1: 1), (2-3: 2), (0-2: 3), (1-2: 4), (1-3: 5).
2. Edge (0-1: 1): find(0)!=find(1) -> ADD EDGE (0-1: 1), Union(0, 1). Edges = 1.
3. Edge (2-3: 2): find(2)!=find(3) -> ADD EDGE (2-3: 2), Union(2, 3). Edges = 2.
4. Edge (0-2: 3): find(0)!=find(2) -> ADD EDGE (0-2: 3), Union(0, 2). Edges = 3 = V-1!
Total Weight = 1 + 2 + 3 = 6! ✅

Prim's Execution (Start Root = 0):
1. Visited = {0}. Heap = [ (0-1: 1), (0-2: 3) ].
2. Pop (0-1: 1): Vertex 1 unvisited -> Add Edge (0-1: 1), Visited = {0, 1}. Heap = [ (0-2: 3), (1-2: 4), (1-3: 5) ].
3. Pop (0-2: 3): Vertex 2 unvisited -> Add Edge (0-2: 3), Visited = {0, 1, 2}. Heap = [ (2-3: 2), (1-2: 4), (1-3: 5) ].
4. Pop (2-3: 2): Vertex 3 unvisited -> Add Edge (2-3: 2), Visited = {0, 1, 2, 3} (ALL VISITED!).
Total Weight = 1 + 3 + 2 = 6! ✅
```

---

## 5. Visual Diagram: Disjoint-Set Union (DSU) vs Cut Crossing Selection

```
Kruskal's DSU Forest Merging:
Initial: (0) (1) (2) (3)  ──► Component Forests
Add (0-1: 1): [0 - 1] (2) (3)
Add (2-3: 2): [0 - 1] [2 - 3]
Add (0-2: 3): [0 - 1 - 2 - 3] ──► Unified MST! ⚡

Prim's Cut Expansion:
[ Visited Set S: {0, 1} ] ◄────── Cut Crossing Edge (0-2: 3) ──────► [ Unvisited Set V\S: {2, 3} ]
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Kruskal's Algorithm with DSU Path Compression & Rank, and Prim's Algorithm with Min-Heap Priority Queue.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Minimum Spanning Trees (MST),
 * Kruskal's Algorithm with DSU, and Prim's Algorithm with Min-Heap.
 */
public class MinimumSpanningTreeMaster {

    public static class Edge implements Comparable<Edge> {
        public final int src;
        public final int dest;
        public final int weight;

        public Edge(int src, int dest, int weight) {
            this.src = src;
            this.dest = dest;
            this.weight = weight;
        }

        @Override
        public int compareTo(Edge o) {
            return Integer.compare(this.weight, o.weight);
        }

        @Override
        public String toString() {
            return String.format("(%d-%d: %d)", src, dest, weight);
        }
    }

    public static class MSTResult {
        public final int totalWeight;
        public final List<Edge> mstEdges;

        public MSTResult(int totalWeight, List<Edge> mstEdges) {
            this.totalWeight = totalWeight;
            this.mstEdges = mstEdges;
        }
    }

    // =========================================================================
    // 1. KRUSKAL'S ALGORITHM WITH DSU (O(E log E) Time, O(V + E) Space)
    // =========================================================================
    public static class DSU {
        private final int[] parent;
        private final int[] rank;

        public DSU(int n) {
            this.parent = new int[n];
            this.rank = new int[n];
            for (int i = 0; i < n; i++) {
                parent[i] = i;
                rank[i] = 0;
            }
        }

        public int find(int i) {
            if (parent[i] == i) return i;
            return parent[i] = find(parent[i]); // Path Compression! ⚡
        }

        public boolean union(int u, int v) {
            int rootU = find(u);
            int rootV = find(v);

            if (rootU == rootV) return false; // Cycle detected!

            // Union by Rank
            if (rank[rootU] < rank[rootV]) {
                parent[rootU] = rootV;
            } else if (rank[rootU] > rank[rootV]) {
                parent[rootV] = rootU;
            } else {
                parent[rootV] = rootU;
                rank[rootU]++;
            }

            return true;
        }
    }

    /**
     * Solves MST using Kruskal's Edge-Centric Greedy Algorithm in O(E log E) time.
     *
     * @param v number of vertices
     * @param edges list of all graph edges
     * @return MSTResult containing total weight and MST edges
     */
    public MSTResult kruskalMST(int v, List<Edge> edges) {
        if (edges == null || edges.isEmpty() || v <= 0) {
            return new MSTResult(0, new ArrayList<>());
        }

        // Step 1: Sort all edges in non-decreasing order of weight
        List<Edge> sortedEdges = new ArrayList<>(edges);
        Collections.sort(sortedEdges);

        DSU dsu = new DSU(v);
        List<Edge> mstEdges = new ArrayList<>();
        int totalWeight = 0;

        // Step 2: Greedily pick lightest non-cycling edges
        for (Edge edge : sortedEdges) {
            if (dsu.union(edge.src, edge.dest)) {
                mstEdges.add(edge);
                totalWeight += edge.weight;

                if (mstEdges.size() == v - 1) break; // MST complete! ⚡
            }
        }

        return new MSTResult(totalWeight, mstEdges);
    }

    // =========================================================================
    // 2. PRIM'S ALGORITHM WITH MIN-HEAP (O(E log V) Time, O(V + E) Space)
    // =========================================================================
    /**
     * Solves MST using Prim's Vertex-Centric Greedy Algorithm in O(E log V) time.
     */
    public MSTResult primMST(int v, List<Edge> edges) {
        if (edges == null || edges.isEmpty() || v <= 0) {
            return new MSTResult(0, new ArrayList<>());
        }

        // Build Adjacency List Graph
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());

        for (Edge edge : edges) {
            adj.get(edge.src).add(new Edge(edge.src, edge.dest, edge.weight));
            adj.get(edge.dest).add(new Edge(edge.dest, edge.src, edge.weight)); // Undirected
        }

        boolean[] visited = new boolean[v];
        PriorityQueue<Edge> minHeap = new PriorityQueue<>();
        List<Edge> mstEdges = new ArrayList<>();
        int totalWeight = 0;

        // Start from Root Vertex 0
        visited[0] = true;
        for (Edge edge : adj.get(0)) {
            minHeap.add(edge);
        }

        while (!minHeap.isEmpty() && mstEdges.size() < v - 1) {
            Edge edge = minHeap.poll();

            if (visited[edge.dest]) continue; // Skip visited vertex

            visited[edge.dest] = true;
            mstEdges.add(edge);
            totalWeight += edge.weight;

            // Push outgoing edges from new vertex dest
            for (Edge nextEdge : adj.get(edge.dest)) {
                if (!visited[nextEdge.dest]) {
                    minHeap.add(nextEdge);
                }
            }
        }

        return new MSTResult(totalWeight, mstEdges);
    }
}
```

> **Quick Syntax:**
```java
// Kruskal DSU Union Loop Line
if (dsu.union(edge.src, edge.dest)) { mstEdges.add(edge); totalWeight += edge.weight; }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1584 - Min Cost to Connect All Points**:
   - Equivalent to Minimum Spanning Tree over Manhattan distance graph solved using Prim's or Kruskal's algorithm ($O(V^2)$ or $O(E \log V)$).

2. **Telecommunication & Fiber Optic Cable Layout**:
   - Laying fiber optic cable between cities to minimize infrastructure cost while keeping all cities connected.

3. **Electric Power Grid Distribution Networks**:
   - Connecting high-voltage electrical towers with minimum wire material cost.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class MinimumSpanningTreeDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MINIMUM SPANNING TREE (MST) DEMO              ");
        System.out.println("=================================================\n");

        MinimumSpanningTreeMaster master = new MinimumSpanningTreeMaster();

        int v = 4;
        List<MinimumSpanningTreeMaster.Edge> edges = List.of(
            new MinimumSpanningTreeMaster.Edge(0, 1, 1),
            new MinimumSpanningTreeMaster.Edge(1, 2, 4),
            new MinimumSpanningTreeMaster.Edge(0, 2, 3),
            new MinimumSpanningTreeMaster.Edge(2, 3, 2),
            new MinimumSpanningTreeMaster.Edge(1, 3, 5)
        );

        System.out.println("1. Graph Vertices = " + v + ", Edges List: " + edges);

        // Kruskal's Test
        MinimumSpanningTreeMaster.MSTResult kruskalRes = master.kruskalMST(v, edges);
        System.out.println("\n2. Kruskal's MST Result (Edge-Centric O(E log E)):");
        System.out.println("   Total Weight: " + kruskalRes.totalWeight);
        System.out.println("   MST Edges   : " + kruskalRes.mstEdges);

        // Prim's Test
        MinimumSpanningTreeMaster.MSTResult primRes = master.primMST(v, edges);
        System.out.println("\n3. Prim's MST Result (Vertex-Centric O(E log V)):");
        System.out.println("   Total Weight: " + primRes.totalWeight);
        System.out.println("   MST Edges   : " + primRes.mstEdges);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| MST Algorithm | Time Complexity | Auxiliary Space | Graph Suitability |
| :--- | :--- | :--- | :--- |
| **Kruskal's Algorithm** | $\mathbf{O(E \log E)}$ ⚡| $\mathbf{O(V + E)}$ DSU ⚡| Sparse Graphs ($E \approx V$) |
| **Prim's Algorithm (Min-Heap)**| $\mathbf{O(E \log V)}$ ⚡| $\mathbf{O(V + E)}$ Heap ⚡| Dense Graphs ($E \approx V^2$) |
| **Prim's Algorithm (Adjacency Matrix)**| $O(V^2)$ | $O(V)$ Distance | Dense Complete Graphs |

---

## 10. Edge Cases & Boundary Handling

1. **Disconnected Graph (Forest)**:
   - Kruskal's algorithm outputs a **Minimum Spanning Forest**. Check if `mstEdges.size() == v - 1` to verify complete connectivity.

2. **Negative Edge Weights**:
   - Both Kruskal's and Prim's algorithms handle negative edge weights correctly! (Unlike Dijkstra's algorithm).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Confusing MST Algorithms with Dijkstra's Shortest Path**:
  - MST minimizes the **TOTAL sum of all edge weights** connecting all vertices. Dijkstra minimizes the **path distance from a single source root**.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Pick Kruskal's vs Prim's:
> * **Kruskal's Algorithm**: Pick when edges are already sorted or graph is **sparse** ($E \ll V^2$).
> * **Prim's Algorithm**: Pick when graph is **dense** ($E \approx V^2$) or represented as an adjacency matrix! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Kruskal's Algorithm | Prim's Algorithm | Dijkstra's Shortest Path |
| :--- | :--- | :--- | :--- |
| **Core Paradigm** | Edge Sorting + DSU | Vertex Cut Growing | Single Source Relaxation |
| **Target Goal** | Min Total Tree Weight | Min Total Tree Weight | Min Path Distance |
| **Negative Edges** | **Supported ⚡** | **Supported ⚡** | NOT Supported |

---

## 14. How to Recognize This in Questions

* **"Connect all cities/points with minimum total cable length"** $\rightarrow$ Minimum Spanning Tree (LeetCode 1584).

---

## 15. Frequently Asked Interview Questions

* **Q: What is the Cut Property in MST?**  
  *A:* The property stating that for any cut of the graph, the lightest edge crossing the cut belongs to the Minimum Spanning Tree.

* **Q: Does an MST always have unique edge weights?**  
  *A:* If all edge weights in a graph are distinct, the Minimum Spanning Tree is strictly unique. If edge weights are identical, multiple valid MSTs may exist.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MINIMUM SPANNING TREES (MST)                         |
+-----------------------------------------------------------------------+
| • Cut Property: Lightest edge crossing ANY cut belongs to MST ⚡       |
| • Kruskal     : Sort edges by weight -> Add if DSU find(u) != find(v) |
| • Prim        : Grow tree from root -> Pop cheapest edge from Min-Heap|
| • Edge Count  : An MST over V vertices contains EXACTLY V - 1 edges   |
| • Performance : Kruskal O(E log E) Sparse | Prim O(E log V) Dense ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the Cut Property and Cycle Property proofs.
- [ ] I can write Kruskal's Algorithm with DSU Path Compression in Java.
- [ ] I can write Prim's Algorithm using Min-Heap Priority Queue.
- [ ] I can solve LeetCode 1584 (`Min Cost to Connect All Points`).
- [ ] I can state when to use Kruskal's vs Prim's algorithm.
