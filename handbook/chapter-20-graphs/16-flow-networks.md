# 16. Flow Networks, Max-Flow Min-Cut Theorem & Edmonds-Karp BFS Engines

## 1. Introduction
A **Flow Network** is a directed graph $G = (V, E)$ where each edge $(u, v)$ has a non-negative **Capacity $c(u, v) \ge 0$** that bounds the amount of flow $f(u, v)$ passing through it. Featuring a designated **Source Node $s$** (producer) and **Sink Node $t$** (consumer), the **Maximum Flow Problem** seeks to route the maximum possible flow from $s$ to $t$ without violating capacity constraints or flow conservation. Computed via **Edmonds-Karp BFS Algorithm ($O(V \cdot E^2)$ Time)** or **Dinic's Algorithm ($O(V^2 \cdot E)$ Time)**, Max-Flow is tied to the fundamental **Max-Flow Min-Cut Theorem**.

> **Important:** The Core Invariants of Flow Networks & Residual Graphs:
> 1. **Capacity Constraint**: $0 \le f(u, v) \le c(u, v)$ for all edges $(u, v) \in E$.
> 2. **Flow Conservation Invariant**: For every vertex $u \ne s, t$, incoming flow equals outgoing flow:
>    $$\sum_{w \in V} f(w, u) = \sum_{v \in V} f(u, v)$$
> 3. **Residual Edge Invariants**:
>    - **Forward Residual Capacity**: $c_f(u, v) = c(u, v) - f(u, v)$ (Remaining available push capacity).
>    - **Backward Residual Capacity**: $c_f(v, u) = f(u, v)$ (Allows REDUCING flow pushed earlier!).
> 4. **Max-Flow Min-Cut Theorem**: In any flow network, the Maximum Flow from source $s$ to sink $t$ is STRICTLY EQUAL to the minimum capacity of a cut separating $s$ and $t$! ⚡

```
Residual Graph Edge Topology:
Forward Edge (u -> v): Capacity c = 10, Current Flow f = 7.
- Forward Residual Capacity c_f(u, v) = 10 - 7 = 3 (Can push +3 more flow!).
- Backward Residual Capacity c_f(v, u) = 7 (Can cancel up to 7 units of previous flow!). ⚡
```

---

## 2. Core Concepts & Edmonds-Karp vs Dinic's Max-Flow Algorithms

### 2.1 Max-Flow Algorithm Strategy Matrix
```
Maximum Flow Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Max-Flow Algorithm    | Augmenting Path Method| Operational Time  | Primary Structure |
+-----------------------+-------------------+-------------------+-------------------+
| **Edmonds-Karp**      | Shortest Path BFS | **$O(V \cdot E^2)$ Time ⚡**| Residual Graph + Queue|
| **Dinic's Algorithm**  | Level Graph + DFS | **$O(V^2 \cdot E)$ Time ⚡**| Level BFS + Blocking DFS|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Max-Flow: Push bottleneck flow along BFS path! Update residual capacities c_f(u,v) -= flow and c_f(v,u) += flow!"**

---

## 3. Characteristics & Max-Flow Min-Cut Proof

### 3.1 Mathematical Proof of Max-Flow Min-Cut Theorem
* Let $f$ be a flow in $G$ and $(S, T)$ be any cut partitioning $V$ such that $s \in S$ and $t \in T$.
* The net flow across cut $(S, T)$ equals total value $|f|$.
* Since flow across any edge cannot exceed capacity $c(u, v)$, net flow $|f| \le c(S, T)$.
* When no augmenting path exists in the residual graph $G_f$, defining $S$ as the set of nodes reachable from $s$ in $G_f$ creates a cut $(S, T)$ where net flow EXACTLY EQUALS capacity $c(S, T)$.
* Thus, **$\max |f| = \min c(S, T)$ (Max-Flow equals Min-Cut!)** ⚡

---

## 4. Internal Working Mechanics
Tracing Edmonds-Karp Max-Flow on Graph (Source=0, Sink=3) with Capacities `(0->1, 10)`, `(0->2, 10)`, `(1->2, 1)`, `(1->3, 10)`, `(2->3, 10)`:

```
Init maxFlow = 0. Residual Capacities initialized to edge capacities.

Augmenting Path 1 via BFS: 0 -> 1 -> 3.
- Bottleneck Capacity = min(c_f(0,1)=10, c_f(1,3)=10) = 10.
- Push flow = 10. Update residual:
  - c_f(0,1) -= 10 (0), c_f(1,0) += 10
  - c_f(1,3) -= 10 (0), c_f(3,1) += 10
- maxFlow += 10 (Total = 10).

Augmenting Path 2 via BFS: 0 -> 2 -> 3.
- Bottleneck Capacity = min(c_f(0,2)=10, c_f(2,3)=10) = 10.
- Push flow = 10. Update residual:
  - c_f(0,2) -= 10 (0), c_f(2,0) += 10
  - c_f(2,3) -= 10 (0), c_f(3,2) += 10
- maxFlow += 10 (Total = 20).

BFS finds no more paths from 0 to 3!
Maximum Flow = 20! ✅ (O(V * E^2) Time!)
```

---

## 5. Visual Diagram
Edmonds-Karp Residual Graph Updating Topography:

```
Forward Edge (u -> v):   c_f(u, v) = c(u, v) - bottleneckFlow  (Decreases!)
Backward Edge (v -> u):  c_f(v, u) = c_f(v, u) + bottleneckFlow (Increases!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Edmonds-Karp Maximum Flow algorithm using BFS residual capacity augmentation:

```java
import java.util.*;

// Edmonds-Karp Maximum Flow Algorithm Master Class
public class FlowNetworksMaster {

    // Edmonds-Karp Max-Flow O(V * E^2) Time, O(V^2) Auxiliary Space
    public int edmondsKarpMaxFlow(int n, int[][] capacity, int source, int sink) {
        int[][] residual = new int[n][n];

        // Step 1: Initialize Residual Graph with Original Edge Capacities
        for (int i = 0; i < n; i++) {
            System.arraycopy(capacity[i], 0, residual[i], 0, n);
        }

        int[] parent = new int[n];
        int maxFlow = 0;

        // Step 2: Loop while BFS finds an augmenting path from source to sink in residual graph
        while (bfsAugmentingPath(residual, parent, n, source, sink)) {
            // Step 3: Find bottleneck residual capacity along BFS path
            int bottleneckFlow = Integer.MAX_VALUE;

            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                bottleneckFlow = Math.min(bottleneckFlow, residual[u][v]);
            }

            // Step 4: Augment flow and update residual capacities
            for (int v = sink; v != source; v = parent[v]) {
                int u = parent[v];
                residual[u][v] -= bottleneckFlow; // Reduce forward residual capacity
                residual[v][u] += bottleneckFlow; // Increase backward residual capacity (Allow flow cancellation!)
            }

            maxFlow += bottleneckFlow;
        }

        return maxFlow;
    }

    // Helper BFS to find shortest augmenting path in residual graph
    private boolean bfsAugmentingPath(int[][] residual, int[] parent, int n, int source, int sink) {
        boolean[] visited = new boolean[n];
        Queue<Integer> queue = new LinkedList<>();

        queue.offer(source);
        visited[source] = true;
        parent[source] = -1;

        while (!queue.isEmpty()) {
            int u = queue.poll();

            for (int v = 0; v < n; v++) {
                // Traverse edge ONLY IF it has positive residual capacity!
                if (!visited[v] && residual[u][v] > 0) {
                    visited[v] = true;
                    parent[v] = u;
                    queue.offer(v);

                    if (v == sink) {
                        return true; // Found path to sink!
                    }
                }
            }
        }

        return false; // No path to sink exists in residual graph
    }
}
```

> **Quick Syntax:**
```java
// Edmonds-Karp Residual Update Line
residual[u][v] -= bottleneckFlow; residual[v][u] += bottleneckFlow;
```

---

## 7. Concrete Problem Examples
* **Bipartite Matching Problem**: Converting Maximum Bipartite Matching to Max-Flow.
* **Network Bandwidth Optimization**: Maximizing data packet throughput.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `edmondsKarpMaxFlow`:

```java
public class FlowNetworksDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Edmonds-Karp Maximum Flow Test ===");
        FlowNetworksMaster solver = new FlowNetworksMaster();

        int n = 4;
        int[][] capacity = new int[n][n];

        // Source = 0, Sink = 3
        capacity[0][1] = 10;
        capacity[0][2] = 10;
        capacity[1][2] = 1;
        capacity[1][3] = 10;
        capacity[2][3] = 10;

        int maxFlow = solver.edmondsKarpMaxFlow(n, capacity, 0, 3);
        System.out.println("Maximum Flow from Source 0 to Sink 3: " + maxFlow); 
        // Output: 20 ✅
    }
}
```

---

## 9. Complexity Analysis

| Max-Flow Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Edmonds-Karp BFS**| **$O(V \cdot E^2)$ Polynomial ⚡**| **$O(V^2)$ Residual Matrix**| BFS shortest augmenting paths |
| **Dinic's Algorithm** | **$O(V^2 \cdot E)$ Polynomial ⚡**| **$O(V + E)$ Adjacency**    | Level graph BFS + Blocking DFS |

---

## 10. Edge Cases & Boundary Handling
* **Source Equals Sink ($s = t$)**: Flow is infinite / zero, handled by guards.
* **No Path from Source to Sink**: Returns `maxFlow = 0`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Backward Residual Capacity Update (`residual[v][u] += bottleneckFlow`)**:
  - Failing to add backward residual capacity prevents the algorithm from canceling inefficient greedy choices, leading to suboptimal flow values!
  - **ALWAYS update both forward (`-= flow`) and backward (`+= flow`) residual capacities**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Backward Edges Are Essential in Max-Flow:
> If an early greedy BFS path routes flow along a sub-optimal edge, later paths may need to "undo" some of that flow.
> Adding $+ \text{flow}$ to backward edge $c_f(v, u)$ allows subsequent augmenting paths to route flow in reverse, cancelling previous flow and achieving the global maximum! ⚡

> **Memory Trick:** **"Backward edges (c_f(v,u) += flow) allow algorithms to cancel bad greedy choices!"**

---

## 13. System & Implementation Comparisons

| Feature | Edmonds-Karp Algorithm | Dinic's Algorithm |
| :--- | :--- | :--- |
| **Augmenting Strategy** | Single BFS Path per Pass | Blocking Flow per Level Graph Pass |
| **Time Complexity** | $O(V \cdot E^2)$ | **$O(V^2 \cdot E)$ (Fastest in Practice) ⚡** |
| **Code Length** | **~25 Lines Clean Code ⚡** | ~60 Lines |

---

## 14. How to Recognize This in Questions
* **"Find maximum throughput from source to sink or minimum capacity cut separating source and sink"** $\rightarrow$ Max-Flow Min-Cut.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Max-Flow Min-Cut Theorem?**  
  *A:* The fundamental theorem stating that the maximum flow passing from source $s$ to sink $t$ equals the minimum sum of capacities of edges in a cut separating $s$ and $t$.
* **Q: Why does Edmonds-Karp use BFS instead of DFS?**  
  *A:* Using BFS guarantees finding the shortest augmenting path (minimum number of edges), bounding the time complexity to $O(V \cdot E^2)$ instead of exponential iterations.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLOW NETWORKS & EDMONDS-KARP MAX-FLOW                 |
+-----------------------------------------------------------------------+
| • Flow Theorem   : Max-Flow equals Min-Cut capacity!                  |
| • Residual Rule  : c_f(u,v) = capacity - flow; c_f(v,u) = flow        |
| • Edmonds-Karp   : BFS finds shortest path -> find bottleneck flow -> |
|                    residual[u][v] -= flow; residual[v][u] += flow;    |
| • Time Bounds    : O(V * E^2) Polynomial Time | O(V^2) Matrix Memory ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Edmonds-Karp Maximum Flow algorithm in Java.
- [ ] I can state the Max-Flow Min-Cut Theorem.
- [ ] I know why backward residual capacity `residual[v][u] += flow` is required.
- [ ] I know why BFS is used instead of DFS in Edmonds-Karp.
- [ ] I can trace residual capacity updates step by step.
