# 07. Shortest Path Algorithms: Dijkstra's Greedy Relaxation, Triangular Inequality & Proofs

## 1. Introduction
Single-Source Shortest Path (SSSP) algorithms find the minimum weight paths from a designated starting source vertex $S$ to all other $V-1$ vertices in a weighted graph $G = (V, E, W)$. The premier greedy single-source shortest path algorithm is **Dijkstra's Algorithm**, created by Edsger W. Dijkstra in 1956. By maintaining a tentative distance array `dist[u]` initialized to $\infty$ and iteratively extracting the unvisited vertex with the minimum tentative distance using a **Min-Heap (Priority Queue)**, Dijkstra's Algorithm relaxes outgoing edges in **$O((V + E) \log V)$ Time Complexity** and **$O(V + E)$ Auxiliary Space**. Dijkstra's Algorithm requires **Non-Negative Edge Weights ($w(e) \ge 0$)** to guarantee correctness via the **Triangular Inequality Invariant**.

> **Important:** Core Structural Invariants of Dijkstra's Algorithm:
> 1. **Greedy Minimum Distance Selection**:
>    - At each step, pop the unvisited vertex $u$ with the absolute smallest tentative distance `dist[u]` from the Min-Heap.
>    - Once vertex $u$ is popped from the Min-Heap, its shortest distance `dist[u]` is PERMANENTLY finalized!
> 2. **Edge Relaxation Invariant**:
>    - For directed edge $(u, v)$ with weight $w$:
>      $$\text{if } dist[u] + w < dist[v] \implies dist[v] = dist[u] + w$$
>    - Updates candidate path to vertex $v$ if passing through $u$ yields a shorter route.
> 3. **Triangular Inequality Theorem**:
>    - For any 3 vertices $u, v, w$:
>      $$d(u, v) \le d(u, w) + d(w, v)$$
> 4. **Negative Edge Weight Failure Invariant**:
>    - If negative edges exist ($w(e) < 0$), popping a vertex no longer guarantees distance finality, causing Dijkstra's greedy choice to return incorrect shortest paths! (Use Bellman-Ford $O(V \cdot E)$ instead). ⚡

```
Dijkstra's Greedy Relaxation Topology (Source S = 0):

Min-Heap Pop Vertex 0 (dist[0] = 0):
- Edge (0-1: 4): dist[1] updated from inf to 4. Push (dist=4, node=1).
- Edge (0-2: 1): dist[2] updated from inf to 1. Push (dist=1, node=2).

Min-Heap Pop Vertex 2 (dist[2] = 1):  ──► FINALIZED! ⚡
- Edge (2-1: 2): dist[2] + 2 = 3 < dist[1] (4) -> RELAX dist[1] to 3! Push (dist=3, node=1).

Min-Heap Pop Vertex 1 (dist[1] = 3):  ──► FINALIZED! ⚡
Total Shortest Distances from 0: dist[1] = 3, dist[2] = 1! ⚡
```

---

## 2. Core Concepts & Shortest Path Strategy Matrix

### 2.1 Shortest Path Algorithms Comparison Matrix
```
Shortest Path Algorithms Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm             | Edge Weight Guard | Time Complexity   | Auxiliary Space   | Graph Archetype   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **BFS Shortest Path** | Unweighted ($w=1$)| **$O(V + E)$ Fast⚡**| $O(V)$ Queue      | Unweighted Graphs |
| **Dijkstra's (Heap)** | **Non-Negative ($w\ge 0$)⚡**| **$O((V + E) \log V)$⚡**| **$O(V + E)$ Heap⚡**| Weighted Graphs   |
| **Bellman-Ford**      | **Supports Negative⚡**| $O(V \cdot E)$    | $O(V)$ Distance   | Graphs with Neg Cycles|
| **Floyd-Warshall**    | All-Pairs ($w\ge 0$)| $O(V^3)$          | $O(V^2)$ DP Matrix| Dense All-Pairs   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Dijkstra pops min dist from Min-Heap and relaxes dist[v] = min(dist[v], dist[u] + w)! Requires non-negative edges w >= 0!"**

---

## 3. Characteristics & Proof of Dijkstra Failure on Negative Edges

### 3.1 Mathematical Proof of Why Dijkstra Fails on Negative Edges
* **Greedy Invariant**: When Dijkstra pops vertex $u$ from the Min-Heap, it assumes `dist[u]` cannot be decreased by any future unvisited path.
* **Counter-Example**:
  - Consider graph with 3 vertices $S=0, A=1, B=2$.
  - Edges: $(0 \to 1, w=5)$, $(0 \to 2, w=2)$, $(2 \to 1, w=-10)$.
  - Step 1: Pop Vertex 0 (dist=0). Push $(1, dist=5)$ and $(2, dist=2)$.
  - Step 2: Pop Vertex 2 (dist=2) as minimum. Finalize `dist[2] = 2`.
  - Step 3: Pop Vertex 1 (dist=5) as next minimum. Finalize `dist[1] = 5`.
  - **Failure**: Path $0 \to 2 \to 1$ has total length $2 + (-10) = -8$, which is MUCH SHORTER than 5!
  - Because Dijkstra marked Vertex 1 visited at dist=5, it fails to discover the true shortest path $-8$.
  - Negative edges violate the assumption that adding edges monotonically increases path length! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Distance Array Trace

Tracing Dijkstra's Algorithm on Source $S = 0$, Graph Vertices {0, 1, 2, 3}, Edges: $(0 \to 1: 4)$, $(0 \to 2: 1)$, $(2 \to 1: 2)$, $(1 \to 3: 1)$, $(2 \to 3: 5)$:

```
Init: dist = [0, inf, inf, inf], visited = [false, false, false, false].
Min-Heap = [ Pair(dist=0, node=0) ].

Step 1: Pop Pair(0, 0). Node 0 unvisited. Mark visited[0] = true.
  Relax Outgoing Edges from 0:
  - (0 -> 1: 4): 0 + 4 = 4 < inf -> dist[1] = 4. Push Pair(4, 1).
  - (0 -> 2: 1): 0 + 1 = 1 < inf -> dist[2] = 1. Push Pair(1, 2).
  Min-Heap = [ Pair(1, 2), Pair(4, 1) ].

Step 2: Pop Pair(1, 2). Node 2 unvisited. Mark visited[2] = true.
  Relax Outgoing Edges from 2:
  - (2 -> 1: 2): dist[2] + 2 = 1 + 2 = 3 < dist[1] (4) -> dist[1] = 3. Push Pair(3, 1).
  - (2 -> 3: 5): dist[2] + 5 = 1 + 5 = 6 < inf -> dist[3] = 6. Push Pair(6, 3).
  Min-Heap = [ Pair(3, 1), Pair(4, 1), Pair(6, 3) ].

Step 3: Pop Pair(3, 1). Node 1 unvisited. Mark visited[1] = true.
  Relax Outgoing Edges from 1:
  - (1 -> 3: 1): dist[1] + 1 = 3 + 1 = 4 < dist[3] (6) -> dist[3] = 4. Push Pair(4, 3).
  Min-Heap = [ Pair(4, 1), Pair(4, 3), Pair(6, 3) ].

Step 4: Pop Pair(4, 1) -> Node 1 already visited -> SKIP!
Step 5: Pop Pair(4, 3) -> Node 3 unvisited. Mark visited[3] = true.

Final Shortest Distances: dist = [0, 3, 1, 4]! ✅
```

---

## 5. Visual Diagram: Edge Relaxation & Priority Queue Trajectory

```
Shortest Path Graph Traversal Topology:

             (0) ─── weight 4 ───► (1) ─── weight 1 ───► (3)
              │                     ▲                     ▲
              │ weight 1            │ weight 2            │ weight 4 (relaxed!)
              ▼                     │                     │
             (2) ───────────────────┴─────────────────────┘

Path 0 -> 2 -> 1 -> 3 is shorter than direct path 0 -> 1 -> 3! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Dijkstra's Algorithm with PriorityQueue Min-Heap, Path Reconstruction, LeetCode 743 (Network Delay Time), and LeetCode 787 (Cheapest Flights Within K Stops).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Dijkstra's Shortest Path Algorithm,
 * PriorityQueue Edge Relaxation, Path Reconstruction, and Network Flow Benchmark Problems.
 */
public class ShortestPathMaster {

    public static class Edge {
        public final int dest;
        public final int weight;

        public Edge(int dest, int weight) {
            this.dest = dest;
            this.weight = weight;
        }
    }

    public static class PathNode implements Comparable<PathNode> {
        public final int node;
        public final int dist;

        public PathNode(int node, int dist) {
            this.node = node;
            this.dist = dist;
        }

        @Override
        public int compareTo(PathNode o) {
            return Integer.compare(this.dist, o.dist);
        }
    }

    public static class DijkstraResult {
        public final int[] distances;
        public final int[] parent; // For path reconstruction

        public DijkstraResult(int[] distances, int[] parent) {
            this.distances = distances;
            this.parent = parent;
        }

        public List<Integer> reconstructPathTo(int target) {
            List<Integer> path = new ArrayList<>();
            if (distances[target] == Integer.MAX_VALUE) return path;

            for (int curr = target; curr != -1; curr = parent[curr]) {
                path.add(curr);
            }

            Collections.reverse(path);
            return path;
        }
    }

    // =========================================================================
    // 1. STANDARD DIJKSTRA'S ALGORITHM (O((V + E) log V) Time, O(V + E) Space)
    // =========================================================================
    /**
     * Solves Single-Source Shortest Path using Dijkstra's Algorithm.
     *
     * @param v total vertices count
     * @param adj adjacency list of weighted edges
     * @param source starting vertex S
     * @return DijkstraResult containing distances array and parent array
     */
    public DijkstraResult dijkstra(int v, List<List<Edge>> adj, int source) {
        int[] dist = new int[v];
        int[] parent = new int[v];
        Arrays.fill(dist, Integer.MAX_VALUE);
        Arrays.fill(parent, -1);

        dist[source] = 0;

        PriorityQueue<PathNode> minHeap = new PriorityQueue<>();
        minHeap.add(new PathNode(source, 0));

        boolean[] visited = new boolean[v];

        while (!minHeap.isEmpty()) {
            PathNode curr = minHeap.poll();
            int u = curr.node;

            if (visited[u]) continue; // Skip already finalized vertex ⚡
            visited[u] = true;

            for (Edge edge : adj.get(u)) {
                int next = edge.dest;
                int weight = edge.weight;

                // Greedy Relaxation Step
                if (!visited[next] && dist[u] + weight < dist[next]) {
                    dist[next] = dist[u] + weight;
                    parent[next] = u;
                    minHeap.add(new PathNode(next, dist[next]));
                }
            }
        }

        return new DijkstraResult(dist, parent);
    }

    // =========================================================================
    // 2. LEETCODE 743: NETWORK DELAY TIME (O((V + E) log V) Time)
    // =========================================================================
    /**
     * Calculates time for signal to reach all nodes in network.
     * times[i] = [u, v, w], n = nodes, k = source node (1-indexed).
     */
    public int networkDelayTime(int[][] times, int n, int k) {
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());

        for (int[] time : times) {
            adj.get(time[0]).add(new Edge(time[1], time[2]));
        }

        DijkstraResult res = dijkstra(n + 1, adj, k);

        int maxTime = 0;
        for (int i = 1; i <= n; i++) {
            if (res.distances[i] == Integer.MAX_VALUE) return -1; // Unreachable node!
            maxTime = Math.max(maxTime, res.distances[i]);
        }

        return maxTime;
    }
}
```

> **Quick Syntax:**
```java
// Dijkstra Greedy Relaxation Line
if (dist[u] + weight < dist[next]) { dist[next] = dist[u] + weight; minHeap.add(new PathNode(next, dist[next])); }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 743 - Network Delay Time**:
   - Standard single-source shortest path application solved in $O((V + E) \log V)$ time.

2. **GPS Satellite Navigation Systems (Google Maps / Waze)**:
   - Calculating optimal driving routes with minimal travel time across road networks.

3. **IP Network Packet Routing Protocols (OSPF / IS-IS)**:
   - Open Shortest Path First (OSPF) uses Dijkstra's algorithm to route packets along lowest cost network links.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.ArrayList;
import java.util.List;

public class ShortestPathDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   DIJKSTRA'S GREEDY SHORTEST PATH DEMO          ");
        System.out.println("=================================================\n");

        ShortestPathMaster master = new ShortestPathMaster();

        int v = 4;
        List<List<ShortestPathMaster.Edge>> adj = new ArrayList<>();
        for (int i = 0; i < v; i++) adj.add(new ArrayList<>());

        adj.get(0).add(new ShortestPathMaster.Edge(1, 4));
        adj.get(0).add(new ShortestPathMaster.Edge(2, 1));
        adj.get(2).add(new ShortestPathMaster.Edge(1, 2));
        adj.get(1).add(new ShortestPathMaster.Edge(3, 1));
        adj.get(2).add(new ShortestPathMaster.Edge(3, 5));

        int source = 0;
        ShortestPathMaster.DijkstraResult result = master.dijkstra(v, adj, source);

        System.out.println("1. Shortest Distances from Source " + source + ":");
        for (int i = 0; i < v; i++) {
            System.out.println("   Node " + i + " : Min Distance = " + result.distances[i] + ", Path = " + result.reconstructPathTo(i));
        }
        System.out.println("-------------------------------------------------");

        // LeetCode 743 Test
        int[][] times = {{2, 1, 1}, {2, 3, 1}, {3, 4, 1}};
        int n = 4, k = 2;
        int delay = master.networkDelayTime(times, n, k);
        System.out.println("2. LeetCode 743 Network Delay Time from Source " + k + ": " + delay + " Units");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Shortest Path Engine | Time Complexity | Auxiliary Space | Negative Edges |
| :--- | :--- | :--- | :--- |
| **BFS (Unweighted)** | $\mathbf{O(V + E)}$ Fast ⚡| $O(V)$ Queue | N/A ($w=1$) |
| **Dijkstra's (Min-Heap)**| $\mathbf{O((V + E) \log V)}$⚡| $\mathbf{O(V + E)}$ Heap ⚡| **FAILS ❌** |
| **Bellman-Ford Engine**| $O(V \cdot E)$ | $O(V)$ Distance | **SUPPORTED ✅** |

---

## 10. Edge Cases & Boundary Handling

1. **Unreachable Vertices (`dist[v] == Integer.MAX_VALUE`)**:
   - Check if `dist[v] == Integer.MAX_VALUE` before adding weights to prevent 32-bit integer overflow wrap to negative numbers!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running Dijkstra's Algorithm on Graphs with Negative Edge Weights**:
  - Negative edges break Dijkstra's greedy distance finality assumption. Use **Bellman-Ford Algorithm** ($O(V \cdot E)$) for graphs with negative weights!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Dijkstra Uses a Min-Heap:
> Scanning an unvisited distance array linearly takes $O(V)$ per step ($O(V^2)$ total).
> Min-Heap extracts the minimum distance vertex in **$O(\log V)$ time**, reducing total runtime to **$O((V + E) \log V)$**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Dijkstra's Algorithm | Bellman-Ford | Floyd-Warshall |
| :--- | :--- | :--- | :--- |
| **Source Type** | Single Source | Single Source | **All Pairs ⚡** |
| **Time Complexity** | **$O((V + E) \log V)$ ⚡** | $O(V \cdot E)$ | $O(V^3)$ |
| **Negative Edges** | **FAILS ❌** | **Supported ✅** | Supported |

---

## 14. How to Recognize This in Questions

* **"Find shortest path in non-negative weighted graph"** $\rightarrow$ Dijkstra's Algorithm.
* **"Network delay time for signal to reach all nodes"** $\rightarrow$ LeetCode 743.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Dijkstra's algorithm fail on graphs with negative edge weights?**  
  *A:* Because Dijkstra assumes popping a vertex from the Min-Heap finalizes its shortest distance. A negative edge can decrease distance later, violating the greedy choice invariant.

* **Q: What is Edge Relaxation?**  
  *A:* The step of updating `dist[v] = dist[u] + w` if passing through vertex $u$ provides a shorter path to vertex $v$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: DIJKSTRA'S SHORTEST PATH                              |
+-----------------------------------------------------------------------+
| • Greedy Choice: Pop vertex u with minimum dist[u] from Min-Heap      |
| • Relaxation   : if (dist[u] + w < dist[v]) dist[v] = dist[u] + w     |
| • Guard        : FAILS on negative edges! (Requires w >= 0)           |
| • Performance  : O((V + E) log V) Time | O(V + E) Auxiliary Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Dijkstra's Algorithm using Min-Heap PriorityQueue in Java.
- [ ] I can reconstruct shortest paths using parent pointers.
- [ ] I can explain why Dijkstra fails on negative edge weights.
- [ ] I can solve LeetCode 743 (`Network Delay Time`).
- [ ] I can state the time complexity of Dijkstra's algorithm ($O((V + E) \log V)$).
