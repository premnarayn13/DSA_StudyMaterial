# 11. Prim's Minimum Spanning Tree Algorithm, Greedy Cut Property & Min-Heap Expansion

## 1. Introduction
**Prim's Algorithm** is a greedy Minimum Spanning Tree (MST) algorithm designed to find a subset of edges in a weighted connected undirected graph that connects all $V$ vertices with the **MINIMUM TOTAL EDGE WEIGHT** without forming any cycles. Invented by Vojtěch Jarník in 1930 and rediscovered by Robert C. Prim in 1957, Prim's algorithm grows a single tree component one vertex at a time by repeatedly selecting the minimum weight edge connecting a visited vertex to an unvisited vertex using a **Min-Heap PriorityQueue (`PriorityQueue<Edge>`)** in **$O(E \log V)$ Time** and **$O(V + E)$ Auxiliary Memory**.

> **Important:** The Greedy Cut Property Invariant of Prim's Algorithm:
> 1. **Cut Property Theorem**: For any cut partitioning graph vertices into visited set $S$ and unvisited set $V \setminus S$, the minimum weight edge $e = (u, v)$ crossing the cut ($u \in S, v \in V \setminus S$) MUST belong to the Minimum Spanning Tree (MST)!
> 2. **Node-Centric MST Growth**: Unlike Kruskal's algorithm (which builds a forest by sorting all global edges), Prim's algorithm grows a SINGLE connected tree from an arbitrary starting root node $s$!
> 3. **Visited Array Guard**: Skip processing dequeued edge $(u, v, w)$ if `visited[v] == true`! ⚡

```
Prim's Greedy Cut Expansion Topology (Starting at Node 0):
Visited Set S = {0}                     Unvisited Set V \ S = {1, 2, 3}
        (0) ---- [2] ----> (1)
         |                  |
        [4]                [1]
         v                  v
        (2) ---- [3] ----> (3)

Min Crossing Edge = (0 -> 1, wt 2). Add Node 1 to Visited Set S = {0, 1}! ⚡
```

---

## 2. Core Concepts & Prim's vs Kruskal's MST Algorithms

### 2.1 MST Algorithm Strategy Matrix
```
Minimum Spanning Tree Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| MST Algorithm         | Primary Paradigm  | Primary Structure | Best Graph Density|
+-----------------------+-------------------+-------------------+-------------------+
| **Prim's Algorithm**  | Node-Centric Tree | **Min-Heap (PQ) ⚡**| **Dense Graphs ($E \approx V^2$) ⚡**|
| **Kruskal's Algorithm**| Edge-Centric Forest| **DSU / Union-Find ⚡**| Sparse Graphs ($E \approx V$) |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Prim's Algorithm grows 1 tree from node 0 using Min-Heap! Kruskal's grows a forest using DSU!"**

---

## 3. Characteristics & $O(E \log V)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(E \log V)$ Complexity
* Starting at root node 0, Prim's algorithm visits every vertex $v \in V$ exactly once.
* Outgoing edges from newly visited vertices are offered to the Min-Heap PriorityQueue.
* At most $E$ edges enter the PriorityQueue, taking $O(\log V)$ per `offer()` and `poll()`.
* Total Time Complexity: $\mathbf{O(E \log V) \text{ Time}}$ (or $O(V^2)$ for dense graphs without heap). ⚡

---

## 4. Internal Working Mechanics
Tracing Prim's Algorithm on Graph (Start = 0) with Edges `(0-1, wt 1)`, `(0-2, wt 3)`, `(1-2, wt 1)`, `(1-3, wt 6)`:

```
Init: visited = [F, F, F, F], PQ = [(0, wt 0)]. Total Weight = 0, Edges Count = 0.

Step 1: Pop (Node 0, wt 0). Mark visited[0] = true.
- Add outgoing edges from 0 to PQ: (0-1, wt 1), (0-2, wt 3).
- PQ = [(0-1, wt 1), (0-2, wt 3)].

Step 2: Pop (Node 1 via 0-1, wt 1). Mark visited[1] = true.
- Add MST weight += 1. Edges Count = 1.
- Add outgoing edges from 1 to PQ: (1-2, wt 1), (1-3, wt 6).
- PQ = [(1-2, wt 1), (0-2, wt 3), (1-3, wt 6)].

Step 3: Pop (Node 2 via 1-2, wt 1). Mark visited[2] = true.
- Add MST weight += 1 (Total = 2). Edges Count = 2.
- Outgoing edge from 2 already visited.
- PQ = [(0-2, wt 3), (1-3, wt 6)].

Step 4: Pop (0-2, wt 3). visited[2] is true -> SKIP (Stale edge!).
Step 5: Pop (Node 3 via 1-3, wt 6). Mark visited[3] = true. Total Weight = 8.

MST Complete! Total Minimum Weight = 8! ✅ (O(E log V) Time!)
```

---

## 5. Visual Diagram
Prim's Cut Property Expansion Topography:

```
Step 1: Set S = {0}       ---> Min Cut Edge (0-1, wt 1) ---> S = {0, 1}
Step 2: Set S = {0, 1}    ---> Min Cut Edge (1-2, wt 1) ---> S = {0, 1, 2}
Step 3: Set S = {0, 1, 2} ---> Min Cut Edge (1-3, wt 6) ---> S = {0, 1, 2, 3} (MST Done!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 1584 (Min Cost to Connect All Points using Prim's MST Algorithm):

```java
import java.util.*;

// LeetCode 1584: Min Cost to Connect All Points (Prim's Algorithm)
public class PrimsAlgorithmMaster {

    private static class Edge implements Comparable<Edge> {
        private final int to;
        private final int weight;

        public Edge(int to, int weight) {
            this.to = to;
            this.weight = weight;
        }

        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight); // Min-Heap based on weight
        }
    }

    // LeetCode 1584 Solution O(E log V) Time, O(V + E) Space
    public int minCostConnectPoints(int[][] points) {
        if (points == null || points.length == 0) return 0;

        int numVertices = points.length;
        boolean[] visited = new boolean[numVertices];
        PriorityQueue<Edge> pq = new PriorityQueue<>();

        // Start Prim's algorithm from Node 0
        pq.offer(new Edge(0, 0));

        int totalMinCost = 0;
        int nodesVisitedCount = 0;

        while (!pq.isEmpty() && nodesVisitedCount < numVertices) {
            Edge curr = pq.poll();
            int u = curr.to;
            int weight = curr.weight;

            // Stale Node Check: Skip if node u is already in MST!
            if (visited[u]) continue;

            visited[u] = true;
            totalMinCost += weight;
            nodesVisitedCount++;

            // Explore all implicit edges from node u to all unvisited nodes
            for (int v = 0; v < numVertices; v++) {
                if (!visited[v]) {
                    int dist = Math.abs(points[u][0] - points[v][0]) + 
                               Math.abs(points[u][1] - points[v][1]); // Manhattan distance
                    pq.offer(new Edge(v, dist));
                }
            }
        }

        return totalMinCost;
    }
}
```

> **Quick Syntax:**
```java
// Prim's Stale Edge Guard Line
if (visited[u]) continue; visited[u] = true; totalMinCost += weight;
```

---

## 7. Concrete Problem Examples
* **LeetCode 1584 - Min Cost to Connect All Points**: Complete graph Prim's MST.
* **Fiber Optic Network Cable Deployment**: Minimum cost network backbone design.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 1584 `minCostConnectPoints`:

```java
public class PrimsAlgorithmDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 1584 Prim's MST Test ===");
        PrimsAlgorithmMaster solver = new PrimsAlgorithmMaster();

        int[][] points = {{0,0}, {2,2}, {3,10}, {5,2}, {7,0}};
        int minCost = solver.minCostConnectPoints(points);

        System.out.println("Minimum Total Cost to Connect All Points: " + minCost); 
        // Output: 20 ✅
    }
}
```

---

## 9. Complexity Analysis

| MST Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Prim's Min-Heap PQ** | **$O(E \log V)$ Optimal ⚡** | **$O(V + E)$ Memory** | PriorityQueue Min-Heap |
| **Prim's Dense $O(V^2)$**| **$O(V^2)$ Optimal ⚡** | **$O(V)$ Distance Array**| Un-heaped array scan for $E \approx V^2$ |

---

## 10. Edge Cases & Boundary Handling
* **$N = 1$ Single Point**: Returns cost `0` immediately.
* **Disconnected Graph**: `nodesVisitedCount < numVertices` after loop signals incomplete MST.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting `if (visited[u]) continue;` Check**:
  - Failing to skip already-visited nodes allows stale edges to add duplicate weight costs and form invalid cycle paths!
  - **ALWAYS check `if (visited[u]) continue;` immediately after polling from PriorityQueue**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Prim's Outperforms Kruskal's on Dense Graphs ($E \approx V^2$):
> Kruskal's algorithm must sort all $E$ global edges ($O(E \log E) = O(V^2 \log V)$).
> Prim's algorithm using an un-heaped array distance scan (`minDist[V]`) finds the minimum crossing edge in $O(V)$ time per vertex, achieving **$O(V^2)$ time** and beating Kruskal's by a logarithmic factor! ⚡

> **Memory Trick:** **"Dense Complete Graph = Prim's O(V^2)! Sparse Edge Graph = Kruskal's O(E log E)!"**

---

## 13. System & Implementation Comparisons

| Feature | Prim's Algorithm | Kruskal's Algorithm |
| :--- | :--- | :--- |
| **Core Concept** | Grows 1 Tree Component | Merges Forest of Trees |
| **Primary Structure** | **Min-Heap PriorityQueue ⚡** | **DSU / Union-Find ⚡** |
| **Dense Graph $O(V^2)$**| **Native $O(V^2)$ Array Scan ⚡**| Requires sorting all $V^2$ edges |

---

## 14. How to Recognize This in Questions
* **"Connect all 2D points or cities with minimum total edge weight"** $\rightarrow$ LeetCode 1584 (Prim's / Kruskal's MST).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Greedy Cut Property in Prim's algorithm?**  
  *A:* The theorem stating that the minimum weight edge crossing any cut between visited and unvisited node sets MUST belong to the Minimum Spanning Tree.
* **Q: How does Prim's algorithm prevent cycles?**  
  *A:* By maintaining a `visited[]` boolean array and ignoring any edge pointing to an already visited vertex.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRIM'S ALGORITHM                                      |
+-----------------------------------------------------------------------+
| • Paradigm       : Grows 1 single tree from node 0 using Min-Heap (PQ) |
| • Stale Check    : if (visited[u]) continue; visited[u] = true;       |
| • Cut Expansion  : Offer all outgoing edges from newly visited node   |
| • Performance    : O(E log V) with PriorityQueue | O(V^2) for Dense Graphs⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Prim's algorithm using PriorityQueue in Java.
- [ ] I can write LeetCode 1584 (`Min Cost to Connect All Points`).
- [ ] I know why `if (visited[u]) continue;` is mandatory.
- [ ] I can explain the Greedy Cut Property Theorem.
- [ ] I can trace Prim's cut expansion step by step.
