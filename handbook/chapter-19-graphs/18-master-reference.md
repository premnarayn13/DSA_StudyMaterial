# 18. Master Reference — Graphs (Data Structures & Algorithms)

## 1. Introduction
This Master Reference consolidates all mathematical formulas, structural invariants, operational complexities, design patterns, and interview pitfalls for **Chapter 20: Graphs**. It serves as an ultra-dense, rapid-scanning interview cheat sheet for graph representations, traversals (BFS/DFS), shortest path algorithms (Dijkstra, Bellman-Ford, Floyd-Warshall), Minimum Spanning Trees (Prim, Kruskal), connectivity (Tarjan's Bridges, Kosaraju's SCCs), Eulerian paths (Hierholzer), Max-Flow Min-Cut (Edmonds-Karp), and Bitmask BFS.

> **Important:** Review this master reference 15 minutes before an interview to refresh Handshaking Lemma ($\sum \text{deg}(v) = 2|E|$), BFS Level-Order Queue Invariant, DFS Grid Flood-Fill in-place sinking (`grid[r][c] = '0'`), 3-Color Directed Cycle States (0 White, 1 Gray, 2 Black), Kahn's In-Degree BFS Algorithm (`inDegree[v] == 0`), 2-Coloring Bipartite Invariant (`color[v] = -color[u]`), Dijkstra's Min-Heap Relaxation (`dist[u] + w < dist[v]`), Bellman-Ford $V-1$ Edge Passes + $V$-th Pass Negative Cycle Check, Floyd-Warshall Triply Nested DP (`k` outermost!), Prim's Cut Property vs Kruskal's DSU Sorting, Tarjan's Bridge Condition (`low[v] > tin[u]`), Kosaraju's 2-Pass SCC Transposition, Hierholzer's Post-Order Edge Traversal (`addFirst(u)`), and Edmonds-Karp Residual Max-Flow!

---

## 2. Master Mathematical & Structural Formula Cheat Sheet
* **Handshaking Lemma**:
  - $\sum_{v \in V} \text{deg}(v) = 2 |E|$ (Undirected Graph).
* **BFS Unweighted Shortest Path Invariant**:
  - First time BFS reaches node $v$, `dist[v]` is strictly guaranteed to be the minimum shortest path distance!
* **Directed Cycle Detection (3-Color DFS)**:
  - If edge $(u \to v)$ encounters `state[v] == 1` (**GRAY - On Stack**), a directed cycle exists!
* **Bipartite Graph 2-Coloring Invariant**:
  - `color[v] = -color[u]`. Color conflict if `color[v] == color[u]`. (Bipartite $\iff$ No Odd-Length Cycles).
* **Dijkstra's Greedy Relaxation Invariant**:
  - `if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.offer(new Pair(v, dist[v])); }`
* **Bellman-Ford $V-1$ Pass & Negative Cycle Check**:
  - Pass $1 \dots V-1$: Relax all edges. Pass $V$: If `dist[u] + w < dist[v]` holds $\implies$ Negative Cycle!
* **Floyd-Warshall DP State Transition**:
  - `dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);` (Loop `k` MUST be outermost!).
* **Tarjan's Low-Link Bridge Condition**:
  - Edge $(u \to v)$ is a BRIDGE IF AND ONLY IF `low[v] > tin[u]`.
* **Max-Flow Min-Cut Theorem**:
  - $\max |f| = \min c(S, T)$. Residual updates: `residual[u][v] -= flow; residual[v][u] += flow;`

```
Graph Algorithms Master Decision Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Target Requirement    | Best Algorithm    | Time Complexity   | Key Data Structure|
+-----------------------+-------------------+-------------------+-------------------+
| Unweighted Shortest   | **BFS**           | **$O(V + E)$ ⚡** | FIFO Queue        |
| Non-Negative Weighted | **Dijkstra**      | **$O((V+E)\log V)$ ⚡**| Min-Heap (PQ)     |
| Negative Edge Weights | **Bellman-Ford**  | **$O(V \cdot E)$**| Edges List        |
| All-Pairs Shortest    | **Floyd-Warshall**| **$O(V^3)$**      | 2D DP Matrix      |
| Minimum Spanning Tree | **Kruskal / Prim**| **$O(E \log E)$ / $O(E \log V)$**| DSU / Min-Heap |
| Topological Ordering  | **Kahn's BFS**    | **$O(V + E)$ ⚡** | In-Degree Array   |
| Critical Network Link | **Tarjan Bridges**| **$O(V + E)$ ⚡** | `tin[]` / `low[]`  |
+-----------------------+-------------------+-------------------+-------------------+
```

---

## 3. Master Operations Complexity Table

| Algorithm / Problem | Time Complexity | Auxiliary Space | Key Factor / Mechanism |
| :--- | :--- | :--- | :--- |
| **Adjacency List Build**| **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Memory ⚡**| Array of ArrayLists |
| **Breadth-First Search**| **$O(V + E)$ Linear ⚡** | **$O(V)$ Queue Space**| Level-order FIFO queue |
| **Depth-First Search**  | **$O(V + E)$ Linear ⚡** | **$O(V)$ Stack Space**| Recursion / Call Stack |
| **Connected Components**| **$O(V + E)$ Linear ⚡** | **$O(V)$ Visited Array**| Outer loop + DFS |
| **Cycle Detection (207)**| **$O(V + E)$ Linear ⚡** | **$O(V)$ State Array**| 3-Color DFS States (0, 1, 2) |
| **Topological Sort (210)**| **$O(V + E)$ Linear ⚡**| **$O(V)$ In-Degree Array**| Kahn's In-Degree BFS |
| **Is Graph Bipartite (785)**| **$O(V + E)$ Linear ⚡**| **$O(V)$ Color Array**| 2-Coloring BFS (`color[v] = -color[u]`) |
| **Dijkstra's Shortest Path**| **$O((V + E) \log V)$ ⚡**| **$O(V + E)$ Memory** | PriorityQueue Min-Heap |
| **Bellman-Ford (787)** | **$O(V \cdot E)$ Time** | **$O(V)$ Distance Array**| $V-1$ edge relaxation passes |
| **Floyd-Warshall (1334)**| **$O(V^3)$ Cubic** | **$O(V^2)$ Matrix Space**| Triply nested DP (`k` outermost!) |
| **Prim's MST (1584)**  | **$O(E \log V)$ ⚡** | **$O(V + E)$ Memory** | Min-Heap priority queue |
| **Kruskal's MST**      | **$O(E \log E)$ ⚡** | **$O(V + E)$ Memory** | Edge sorting + DSU union |
| **Tarjan's Bridges (1192)**| **$O(V + E)$ Linear ⚡**| **$O(V + E)$ Memory** | Low-link `low[v] > tin[u]` check |
| **Kosaraju's SCCs**    | **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Memory** | Pass 1 Stack + Transposed DFS |
| **Hierholzer Eulerian (332)**| **$O(E \log E)$ ⚡**| **$O(E)$ Memory**    | Post-order `addFirst(u)` prepend |
| **Edmonds-Karp Max-Flow**| **$O(V \cdot E^2)$** | **$O(V^2)$ Residual Matrix**| Shortest BFS augmenting paths |
| **Bitmask BFS (847)**  | **$O(N \cdot 2^N)$** | **$O(N \cdot 2^N)$ Memory**| Queue state `(node, mask)` |

---

## 4. Hardware & Memory Footprint Audit
```
+-----------------------------------------------------------------------------------+
| Memory Breakdown for Graph Storage Representations                                |
+-----------------------------------------------------------------------------------+
| Adjacency List for $V = 100,000$, $E = 200,000$ : ~5 MB Memory Footprint (Minimal!)|
| Adjacency Matrix for $V = 100,000$               : ~40 GB Memory (Crashes OutOfMemory!)|
| Rule of Thumb                                    : DEFAULT TO ADJACENCY LISTS! ⚡ |
+-----------------------------------------------------------------------------------+
```

---

## 5. Java Code Syntax Cheat Sheet

> **Quick Syntax:**
```java
// 1. Adjacency List Initialization
List<List<Integer>> adj = new ArrayList<>();
for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

// 2. BFS Queue & Visited Guard Line
if (dist[v] == -1) { dist[v] = dist[u] + 1; queue.offer(v); }

// 3. Grid DFS Flood-Fill Sinking Line
if (r < 0 || r >= rows || c < 0 || c >= cols || grid[r][c] == '0') return;
grid[r][c] = '0'; // Sink land cell in-place

// 4. Directed Graph 3-Color Cycle Check
if (state[v] == 1) return true; // GRAY node on call stack = Cycle!

// 5. Kahn's Topological BFS In-Degree Processing
inDegree[v]--; if (inDegree[v] == 0) queue.offer(v);

// 6. Dijkstra Greedy Relaxation
if (dist[u] + weight < dist[v]) { dist[v] = dist[u] + weight; pq.offer(new Pair(v, dist[v])); }

// 7. Floyd-Warshall Outermost k Loop
for (int k=0; k<n; k++) for (int i=0; i<n; i++) for (int j=0; j<n; j++)
    if (dist[i][k] != INF && dist[k][j] != INF) dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);

// 8. Tarjan Bridge Check Line
if (low[v] > tin[u]) bridges.add(Arrays.asList(u, v));
```

---

## 6. Critical Trap & Pitfall Audit
* **Pitfall 1: Delaying `visited` Marking in BFS Until Polling**: Delaying `visited` allows duplicate copies of the same node to enter the Queue thousands of times, causing `OutOfMemoryError`. Always mark `visited` IMMEDIATELY when enqueuing (`queue.offer(v)`).
* **Pitfall 2: Running Dijkstra on Graphs with Negative Edge Weights**: Dijkstra assumes dequeued node distances are final. Negative edges violate this greedy assumption. Use **Bellman-Ford** for negative edges!
* **Pitfall 3: Putting Intermediate Loop $k$ Inside Inner Loops in Floyd-Warshall**: Placing $k$ inside calculates incorrect distances because subproblems are not solved in topological DP order. Always put $k$ as the VERY FIRST OUTERMOST loop.
* **Pitfall 4: Forgetting `temp` Array Copy in $K$-Hop Bellman-Ford (LeetCode 787)**: Modifying distance array directly allows 1 pass to traverse multiple edges, violating $K$-stop bounds. Always use `temp = Arrays.copyOf(dist, n)`.
* **Pitfall 5: Using 1D `visited[node]` for Bitmask BFS (LeetCode 847)**: Bitmask BFS permits re-visiting nodes provided the visited bitmask is different. Always use 2D `visited[node][mask]`.

---

## 7. Quick Revision Box
```
+-----------------------------------------------------------------------+
| MASTER REVISION CHEAT SHEET: CHAPTER 20 (GRAPHS)                      |
+-----------------------------------------------------------------------+
| 1. Unweighted Shortest Path : BFS Queue (Mark visited on push!)      |
| 2. Directed Cycle Detection : 3-Color DFS (state[v] == 1 GRAY = Cycle)|
| 3. Topological Sort (210)   : Kahn's In-Degree BFS (inDegree[v] == 0) |
| 4. Weighted Shortest Path   : Dijkstra's Algorithm (Min-Heap PQ)       |
| 5. Negative Edge Weights    : Bellman-Ford (V-1 passes + V-th check)  |
| 6. All-Pairs Shortest Path  : Floyd-Warshall (k loop MUST be outermost!)|
| 7. Minimum Spanning Tree    : Kruskal's (Sort edges + DSU union)      |
| 8. Critical Network Bridges : Tarjan's DFS (low[v] > tin[u])          |
+-----------------------------------------------------------------------+
```

---

## 8. Final Practice Checklist
- [ ] I can write single-source BFS shortest path in Java.
- [ ] I can write LeetCode 200 (`Number of Islands`) using DFS flood-fill.
- [ ] I can write LeetCode 207 (`Course Schedule`) using 3-Color DFS.
- [ ] I can write LeetCode 210 (`Course Schedule II`) using Kahn's BFS.
- [ ] I can write LeetCode 785 (`Is Graph Bipartite?`) using 2-Coloring.
- [ ] I can write Dijkstra's algorithm using PriorityQueue in Java.
- [ ] I can write LeetCode 787 (`Cheapest Flights Within K Stops`).
- [ ] I can write Floyd-Warshall in 5 lines of code.
- [ ] I can write Kruskal's algorithm using DSU in Java.
- [ ] I can write LeetCode 1192 (`Critical Connections in a Network`).
- [ ] I can write Kosaraju's 2-Pass SCC algorithm.
- [ ] I can write LeetCode 332 (`Reconstruct Itinerary`) using Hierholzer.
- [ ] I can write Edmonds-Karp Max-Flow algorithm.
- [ ] I can write LeetCode 847 (`Shortest Path Visiting All Nodes`) using Bitmask BFS.
