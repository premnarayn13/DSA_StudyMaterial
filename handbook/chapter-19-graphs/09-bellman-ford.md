# 09. Bellman-Ford Algorithm, Negative Weight Cycles & $K$-Hop Cheapest Flights

## 1. Introduction
The **Bellman-Ford Algorithm** is a single-source shortest path algorithm capable of handling graphs with **Negative Edge Weights** and detecting **Negative Weight Cycles**. Invented independently by Richard Bellman and Lester Ford Jr. in the 1950s, the algorithm operates by relaxing ALL edges in the graph $V - 1$ times. If an edge can STILL be relaxed on the $V$-th pass, a **Negative Cycle** exists! Modified variants of Bellman-Ford solve **Cheapest Flights Within K Stops (LeetCode 787)** in **$O(V \cdot E)$ Time** and **$O(V)$ Auxiliary Space**.

> **Important:** The $V-1$ Pass Invariant & Negative Cycle Detection:
> 1. **$V-1$ Pass Invariant**: A simple path without cycles in a graph with $V$ vertices contains at most $V - 1$ edges. Thus, relaxing all edges $V - 1$ times guarantees finding all shortest path distances!
> 2. **$V$-th Pass Negative Cycle Check**: If `dist[v] > dist[u] + w` STILL holds during a $V$-th relaxation pass across all edges, a **NEGATIVE WEIGHT CYCLE IS DETECTED**!
> 3. **$K$-Hop Shortest Path (LeetCode 787)**: Use a temporary clone `int[] temp = dist.clone()` during each pass to restrict path lengths to at most $K$ stops! ⚡

```
Bellman-Ford $V-1$ Edge Relaxation Topology:
Graph with 4 Vertices (Passes Required = V - 1 = 3 Passes):
Pass 1: Relaxes paths of length 1 edge.
Pass 2: Relaxes paths of length 2 edges.
Pass 3: Relaxes paths of length 3 edges (Guarantees Shortest Distance!).
Pass 4 (Check): If dist[v] > dist[u] + w holds -> NEGATIVE CYCLE DETECTED! ⚡
```

---

## 2. Core Concepts & LeetCode 787 Cheapest Flights Architecture

### 2.1 LeetCode 787 $K$-Hop Bellman-Ford Strategy
Given `flights` edges `[u, v, price]`, `src`, `dst`, and at most `k` stops:
1. `dist[]` initialized to `Integer.MAX_VALUE`, `dist[src] = 0`.
2. Execute loop $K + 1$ times (allowing at most $K+1$ edges / $K$ stops):
   - Clone distance array: `int[] temp = Arrays.copyOf(dist, n)`.
   - For each edge `[u, v, price]` in `flights`:
     - If `dist[u] != MAX_VALUE` AND `dist[u] + price < temp[v]`:
       - `temp[v] = dist[u] + price`.
   - Update `dist = temp`.
3. Return `dist[dst] == MAX_VALUE ? -1 : dist[dst]` in **$O(K \cdot E)$ Time**.

```
Bellman-Ford Operational Spectrum Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm Variant     | Pass Count        | Negative Edges?   | Primary Problem   |
+-----------------------+-------------------+-------------------+-------------------+
| **Standard Bellman**  | $V - 1$ Passes    | **Supported ⚡**  | Negative Weights  |
| **Negative Cycle Check**| $V$-th Pass Check | **Detects ⚡**    | Arbitrage Arbitrage|
| **$K$-Hop Bellman**   | $K + 1$ Passes    | Supported         | Cheapest Flights  |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Bellman-Ford: Relax all edges V-1 times! V-th pass check reveals negative cycles!"**

---

## 3. Characteristics & $O(V \cdot E)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(V \cdot E)$ Complexity
* Outer loop executes $V - 1$ passes.
* Inner loop iterates over all $E$ edges in the graph.
* Each relaxation check takes $O(1)$ constant time.
* Total Time Complexity: $(V - 1) \times O(E) = \mathbf{O(V \cdot E) \text{ Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 787 (Cheapest Flights Within $K=1$ Stop) on Edges `[[0,1,100], [1,2,100], [0,2,500]]`, `src=0`, `dst=2`:

```
Init: dist = [0, inf, inf], k = 1 stop (Allow k + 1 = 2 passes).

Pass 1 (1 edge): temp = [0, inf, inf].
- Edge (0, 1, 100): temp[1] = min(inf, 0 + 100) = 100.
- Edge (0, 2, 500): temp[2] = min(inf, 0 + 500) = 500.
- dist = [0, 100, 500].

Pass 2 (2 edges / 1 stop max): temp = [0, 100, 500].
- Edge (1, 2, 100): temp[2] = min(500, dist[1] (100) + 100) = 200!
- dist = [0, 100, 200].

Cheapest price within 1 stop = 200! ✅ (O(K * E) Time!)
```

---

## 5. Visual Diagram
Negative Cycle Detection Topography:

```
Pass 1 ... V-1: Distance array stabilizes.
Pass V Check:   Edge (0 -> 1, wt 2), (1 -> 2, wt 3), (2 -> 0, wt -6)  Sum = -1!
                dist[1] STILL DECREASES on Pass V! -> NEGATIVE CYCLE DETECTED! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Standard Bellman-Ford with Negative Cycle Detection and LeetCode 787 (Cheapest Flights Within K Stops):

```java
import java.util.*;

// LeetCode 787: Cheapest Flights Within K Stops (Bellman-Ford Algorithm)
public class BellmanFordMaster {

    // 1. LeetCode 787 Solution O(K * E) Time, O(V) Space
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // Execute K + 1 passes to allow at most K stops
        for (int i = 0; i <= k; i++) {
            int[] temp = Arrays.copyOf(dist, n); // Clone to prevent chain updates in same pass!

            for (int[] flight : flights) {
                int u = flight[0];
                int v = flight[1];
                int price = flight[2];

                if (dist[u] != Integer.MAX_VALUE && dist[u] + price < temp[v]) {
                    temp[v] = dist[u] + price;
                }
            }

            dist = temp; // Update distance array after pass completes
        }

        return dist[dst] == Integer.MAX_VALUE ? -1 : dist[dst];
    }

    // 2. Standard Bellman-Ford with Negative Cycle Detection O(V * E) Time
    public boolean bellmanFord(int n, int[][] edges, int src, int[] dist) {
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;

        // Step 1: Relax all edges V - 1 times
        for (int i = 1; i <= n - 1; i++) {
            for (int[] edge : edges) {
                int u = edge[0];
                int v = edge[1];
                int w = edge[2];

                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }

        // Step 2: V-th Pass Check for Negative Weight Cycles
        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int w = edge[2];

            if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                return false; // Negative Cycle Detected!
            }
        }

        return true; // No negative cycles, valid shortest distances!
    }
}
```

> **Quick Syntax:**
```java
// Bellman-Ford Relaxation Check Line
if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) dist[v] = dist[u] + w;
```

---

## 7. Concrete Problem Examples
* **LeetCode 787 - Cheapest Flights Within K Stops**: $K$-hop bounded Bellman-Ford.
* **Financial Currency Arbitrage Detection**: Negative log weight cycle detection.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 787 `findCheapestPrice`:

```java
public class BellmanFordDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 787 Cheapest Flights Test ===");
        BellmanFordMaster solver = new BellmanFordMaster();

        int n = 4;
        int[][] flights = {{0,1,100}, {1,2,100}, {2,0,100}, {1,3,600}, {2,3,200}};
        int src = 0, dst = 3, k = 1;

        int cheapestPrice = solver.findCheapestPrice(n, flights, src, dst, k);
        System.out.println("Cheapest Price from 0 to 3 within 1 stop: " + 
            cheapestPrice); // Output: 700 (0 -> 1 -> 3) ✅
    }
}
```

---

## 9. Complexity Analysis

| Bellman-Ford Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Standard Bellman-Ford**| **$O(V \cdot E)$ Time** | **$O(V)$ Distance Array** | $V-1$ edge relaxation passes |
| **$K$-Hop Bounded (787)**| **$O(K \cdot E)$ Time ⚡**| **$O(V)$ Distance Array** | $K+1$ passes with `temp` array |

---

## 10. Edge Cases & Boundary Handling
* **Unreachable Destination Node**: `dist[dst]` remains `Integer.MAX_VALUE`, returning `-1`.
* **Graph Contains Negative Cycle**: $V$-th pass detects `dist[v] > dist[u] + w`, returning `false`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting the `temp` Copy Array in $K$-Hop Bellman-Ford (LeetCode 787)**:
  - Without cloning `temp = Arrays.copyOf(dist, n)`, a single pass can chain updates through multiple edges ($0 \to 1 \to 2 \to 3$), exceeding the $K$-stop bound!
  - **ALWAYS use a temporary array `temp` during each pass for $K$-hop bounded updates**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why `temp` Array Is Mandatory for LeetCode 787:
> When updating distances in pass $p$, if we modify `dist[]` directly, an edge $(u \to v)$ updated in pass $p$ can immediately be used by another edge $(v \to w)$ in the SAME pass $p$.
> This causes 1 pass to traverse 2 edges!
> Using `temp = Arrays.copyOf(dist, n)` forces pass $p$ to evaluate edge relaxation strictly using distances from pass $p-1$, enforcing the exact $K$-stop constraint! ⚡

> **Memory Trick:** **"LeetCode 787: Clone dist to temp array before each pass to enforce exact K-stop bounds!"**

---

## 13. System & Implementation Comparisons

| Feature | Bellman-Ford Algorithm | Dijkstra's Algorithm |
| :--- | :--- | :--- |
| **Negative Edges** | **Supported ⚡** | Not Supported |
| **Negative Cycles** | **Detects Negative Cycles ⚡** | Infinite Loops |
| **Time Complexity** | $O(V \cdot E)$ Slower | **$O((V + E) \log V)$ Faster ⚡**|

---

## 14. How to Recognize This in Questions
* **"Find cheapest flight path within at most K stops or handle negative edge weights"** $\rightarrow$ Bellman-Ford.

---

## 15. Frequently Asked Interview Questions
* **Q: Why does Bellman-Ford relax edges $V - 1$ times?**  
  *A:* Because the longest simple path without cycles in a graph of $V$ vertices contains at most $V - 1$ edges.
* **Q: How does Bellman-Ford detect negative weight cycles?**  
  *A:* By attempting a $V$-th relaxation pass. If any edge can still be relaxed, a negative weight cycle exists.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BELLMAN-FORD ALGORITHM                                |
+-----------------------------------------------------------------------+
| • Standard Setup : Relax all edges V-1 times; dist[u] + w < dist[v]   |
| • Negative Cycle : V-th pass check: if (dist[u] + w < dist[v]) -> Cycle!|
| • LeetCode 787   : K+1 passes using temp = Arrays.copyOf(dist, n)     |
| • Time Bounds    : O(V * E) Standard | O(K * E) Bounded ⚡              |
| • Advantage      : Handles negative edge weights & detects cycles! ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write standard Bellman-Ford with negative cycle detection in Java.
- [ ] I can write LeetCode 787 (`Cheapest Flights Within K Stops`).
- [ ] I know why `temp` array copy is mandatory for $K$-hop bounds.
- [ ] I know why $V-1$ passes are required.
- [ ] I can trace edge relaxation step by step.
