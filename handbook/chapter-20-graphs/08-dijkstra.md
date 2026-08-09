# 08. Dijkstra's Algorithm, Greedy Edge Relaxation & Min-Heap PriorityQueue

## 1. Introduction
**Dijkstra's Algorithm** is the foundational single-source shortest path algorithm for non-negatively weighted graphs. Invented by Edsger W. Dijkstra in 1956, it greedily selects the unvisited node with the absolute smallest tentative distance, relaxing all its outgoing edges. Powered by a **Min-Heap PriorityQueue (`PriorityQueue<Pair>`)**, Dijkstra's algorithm finds shortest path distances from a source node $s$ to all other reachable vertices in **$O((V + E) \log V)$ Time** and **$O(V + E)$ Auxiliary Memory**.

> **Important:** The Greedy Relaxation Invariant & Non-Negative Edge Weight Limitation:
> 1. **Greedy Relaxation Invariant**: For edge $(u \to v, w)$:
>    $$\text{If } \text{dist}[v] > \text{dist}[u] + w \implies \text{Update } \text{dist}[v] = \text{dist}[u] + w \quad \text{and offer } (v, \text{dist}[v]) \text{ to Min-Heap!}$$
> 2. **Stale Node Skipping**: If dequeued `currDist > dist[u]`, skip processing immediately (Node $u$ was already relaxed via a shorter path!).
> 3. **Non-Negative Weight Constraint**: Dijkstra's algorithm FAILS on graphs with negative edge weights! Use **Bellman-Ford Algorithm** for negative edges! ⚡

```
Dijkstra's Greedy Edge Relaxation Topology (Edge 0 -> 1 with weight 2):
Initial State: dist[0] = 0, dist[1] = infinity

Relaxation Step:
Check condition: dist[1] (inf) > dist[0] (0) + weight (2) = 2.
Condition holds! Update dist[1] = 2, Push (1, dist=2) into PriorityQueue! ⚡
```

---

## 2. Core Concepts & Min-Heap PriorityQueue Architecture

### 2.1 Dijkstra's Operational Strategy Matrix
```
Dijkstra's Algorithm Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Component             | Implementation    | Operational Time  | Purpose           |
+-----------------------+-------------------+-------------------+-------------------+
| **Distance Array**    | `int[] dist`      | $O(V)$ Init       | Stores min cost   |
| **Min-Heap Queue**    | `PriorityQueue`   | **$O(\log V)$ ⚡** | Extracts min node |
| **Edge Relaxation**   | `dist[u] + w`     | **$O(1)$ Check ⚡**| Updates shorter   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Dijkstra: Min-Heap pops smallest distance node! Relax edge if dist[u] + w < dist[v]!"**

---

## 3. Characteristics & $O((V + E) \log V)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O((V + E) \log V)$ Complexity
* Total nodes pushed/popped from PriorityQueue $\le E$ (each edge can trigger 1 relaxation push).
* Min-Heap size is at most $V$, so each `offer()` and `poll()` operation takes $O(\log V)$ time.
* Total Min-Heap operations $\implies O(E \log V)$.
* Distance array initialization and vertex processing $\implies O(V \log V)$.
* Total Time Complexity: $\mathbf{O((V + E) \log V) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Dijkstra on Graph (Source = 0) with Edges `(0->1, wt 4)`, `(0->2, wt 1)`, `(2->1, wt 2)`, `(1->3, wt 1)`:

```
Init: dist = [0, inf, inf, inf], PQ = [(0, 0)].

Step 1: Pop (0, dist 0). Relax outgoing edges:
- Edge (0->1, 4): dist[1] > 0 + 4 -> dist[1] = 4. PQ.add(1, 4).
- Edge (0->2, 1): dist[2] > 0 + 1 -> dist[2] = 1. PQ.add(2, 1).
- PQ = [(2, 1), (1, 4)].

Step 2: Pop (2, dist 1). Relax outgoing edge (2->1, 2):
- dist[1] (4) > 1 + 2 = 3 -> Update dist[1] = 3! PQ.add(1, 3).
- PQ = [(1, 3), (1, 4)].

Step 3: Pop (1, dist 3). Relax outgoing edge (1->3, 1):
- dist[3] (inf) > 3 + 1 = 4 -> dist[3] = 4. PQ.add(3, 4).
- PQ = [(1, 4), (3, 4)].

Step 4: Pop (1, dist 4). Stale! currDist (4) > dist[1] (3) -> Skip!
Step 5: Pop (3, dist 4). Terminal. Loop ends.

Shortest Distances from 0: dist = [0, 3, 1, 4]! ✅ (O((V + E) log V) Time!)
```

---

## 5. Visual Diagram
Dijkstra PriorityQueue Relaxation Topography:

```
Direct Path (0 -> 1, wt 4):  Dist = 4
Alternative Path via Node 2: (0 -> 2, wt 1) + (2 -> 1, wt 2) = Dist 3!
Dijkstra relaxes dist[1] from 4 down to 3 via PriorityQueue! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 743 (Network Delay Time using Dijkstra's Algorithm):

```java
import java.util.*;

// LeetCode 743: Network Delay Time (Dijkstra's Algorithm)
public class DijkstraMaster {

    public static class Pair implements Comparable<Pair> {
        public int node;
        public int dist;

        public Pair(int node, int dist) {
            this.node = node;
            this.dist = dist;
        }

        @Override
        public int compareTo(Pair other) {
            return Integer.compare(this.dist, other.dist); // Min-Heap based on distance
        }
    }

    // LeetCode 743 Solution O((V + E) log V) Time, O(V + E) Space
    public int networkDelayTime(int[][] times, int n, int k) {
        // Step 1: Build Weighted Adjacency List
        List<List<Pair>> adj = new ArrayList<>();
        for (int i = 0; i <= n; i++) adj.add(new ArrayList<>());

        for (int[] time : times) {
            int u = time[0];
            int v = time[1];
            int w = time[2];
            adj.get(u).add(new Pair(v, w));
        }

        // Step 2: Initialize Distance Array
        int[] dist = new int[n + 1];
        Arrays.fill(dist, Integer.MAX_VALUE);

        // Step 3: PriorityQueue Min-Heap for Dijkstra
        PriorityQueue<Pair> pq = new PriorityQueue<>();

        // Enqueue Source Node K (1-based indexing)
        dist[k] = 0;
        pq.offer(new Pair(k, 0));

        while (!pq.isEmpty()) {
            Pair curr = pq.poll();
            int u = curr.node;
            int d = curr.dist;

            // Stale Node Guard: Skip if we already found a shorter path to u!
            if (d > dist[u]) continue;

            for (Pair neighbor : adj.get(u)) {
                int v = neighbor.node;
                int weight = neighbor.dist;

                // Greedy Edge Relaxation Condition
                if (dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    pq.offer(new Pair(v, dist[v]));
                }
            }
        }

        // Step 4: Find maximum signal arrival time across all nodes
        int maxDelay = 0;
        for (int i = 1; i <= n; i++) {
            if (dist[i] == Integer.MAX_VALUE) {
                return -1; // Unreachable node exists!
            }
            maxDelay = Math.max(maxDelay, dist[i]);
        }

        return maxDelay;
    }
}
```

> **Quick Syntax:**
```java
// Dijkstra Relaxation Line
if (dist[u] + weight < dist[v]) { dist[v] = dist[u] + weight; pq.offer(new Pair(v, dist[v])); }
```

---

## 7. Concrete Problem Examples
* **LeetCode 743 - Network Delay Time**: Core Dijkstra problem.
* **LeetCode 1514 - Path with Maximum Probability**: Probability-maximized Dijkstra.
* **GPS Navigation Systems**: Shortest driving routes (Google Maps).

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 743 `networkDelayTime`:

```java
public class DijkstraDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 743 Network Delay Time Test ===");
        DijkstraMaster solver = new DijkstraMaster();

        int[][] times = {{2,1,1}, {2,3,1}, {3,4,1}};
        int n = 4, k = 2;

        int delay = solver.networkDelayTime(times, n, k);
        System.out.println("Network Delay Time from Source 2: " + delay); // Output: 2 ✅
    }
}
```

---

## 9. Complexity Analysis

| Dijkstra Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Binary Min-Heap PQ** | **$O((V + E) \log V)$ Optimal ⚡**| **$O(V + E)$ Memory** | PriorityQueue Min-Heap |
| **Fibonacci Heap** | **$O(E + V \log V)$ Theoretical**| $O(V + E)$ Memory | Theoretical optimization |

---

## 10. Edge Cases & Boundary Handling
* **Unreachable Nodes**: Distance remains `Integer.MAX_VALUE`, returning `-1`.
* **Negative Edge Weights**: Causes infinite loops! Use **Bellman-Ford** instead.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting the Stale Node Check (`if (d > dist[u]) continue;`)**:
  - Without this check, stale nodes dequeued from the Min-Heap re-examine outgoing edges needlessly, degrading performance to exponential time!
  - **ALWAYS include `if (d > dist[u]) continue;` after polling from PriorityQueue**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Dijkstra Fails on Negative Edge Weights:
> Dijkstra greedily assumes that once a node is dequeued from the Min-Heap, its shortest distance is FINALized and can never decrease.
> A negative edge weight later in the graph can reduce path costs, violating Dijkstra's greedy assumption!
> Use **Bellman-Ford** when graphs contain negative edge weights! ⚡

> **Memory Trick:** **"Non-negative edges = Dijkstra! Negative edges = Bellman-Ford!"**

---

## 13. System & Implementation Comparisons

| Feature | Dijkstra's Algorithm | Bellman-Ford Algorithm |
| :--- | :--- | :--- |
| **Edge Weight Support** | **Non-Negative Edges Only ($\ge 0$)** | **Negative Edges Supported** |
| **Time Complexity** | **$O((V + E) \log V)$ Fast ⚡** | $O(V \cdot E)$ Slower |
| **Negative Cycle Detection**| No | **Detects Negative Cycles ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find shortest path in non-negatively weighted graph"** $\rightarrow$ LeetCode 743 (Dijkstra's Algorithm).

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Dijkstra use a Min-Heap PriorityQueue?**  
  *A:* To extract the unvisited vertex with the minimum tentative distance in $O(\log V)$ time instead of scanning all $V$ vertices ($O(V)$).
* **Q: What is the purpose of `if (d > dist[u]) continue;`?**  
  *A:* It discards stale entries in the PriorityQueue that were superseded by shorter paths discovered earlier.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DIJKSTRA'S ALGORITHM                                  |
+-----------------------------------------------------------------------+
| • Data Structure : Min-Heap (`PriorityQueue<Pair> pq = new PriorityQueue<>()`)|
| • Stale Check    : if (d > dist[u]) continue;                         |
| • Relaxation Rule: if (dist[u] + w < dist[v]) { dist[v] = dist[u] + w; pq.offer(...); }|
| • Requirement    : Non-negative edge weights ONLY (>= 0)!             |
| • Time Bounds    : O((V + E) log V) Time | O(V + E) Auxiliary Space ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Dijkstra's algorithm using PriorityQueue in Java.
- [ ] I can write LeetCode 743 (`Network Delay Time`).
- [ ] I know why `if (d > dist[u]) continue;` is mandatory.
- [ ] I know why Dijkstra fails on negative edge weights.
- [ ] I can trace edge relaxation step by step.
