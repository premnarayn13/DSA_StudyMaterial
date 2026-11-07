# 10. Floyd-Warshall Algorithm, All-Pairs DP & Intermediate Node Invariants

## 1. Introduction
The **Floyd-Warshall Algorithm** is an elegant All-Pairs Shortest Path dynamic programming algorithm that computes the shortest path distances between **EVERY PAIR OF VERTICES** $(i, j)$ in a weighted directed or undirected graph. Invented by Robert W. Floyd and Stephen Warshall in 1962, the algorithm uses a **Triply Nested Loop** over intermediate vertices $k$ to update path distances in **$O(V^3)$ Cubic Time** and **$O(V^2)$ Auxiliary Matrix Memory**. It serves as the primary engine for **Find the City With the Smallest Number of Neighbors at a Threshold Distance (LeetCode 1334)**.

> **Important:** The Intermediate Vertex Inclusion DP Invariant:
> 1. **DP State Representation**: `dist[i][j]` represents the shortest path distance from vertex $i$ to vertex $j$ considering intermediate vertices from subset $\{0, 1, \dots, k\}$.
> 2. **Triply Nested Loop Order**: The outer loop MUST iterate over intermediate vertex **$k$ FIRST**!
>    ```java
>    for (int k = 0; k < n; k++)
>        for (int i = 0; i < n; i++)
>            for (int j = 0; j < n; j++)
>                dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
>    ```
> 3. **Negative Cycle Signal**: If `dist[i][i] < 0` for any vertex $i$ after completion, a **NEGATIVE CYCLE IS DETECTED**! ⚡

```
Floyd-Warshall Intermediate Node Inclusion Topology:
Direct Path (i -> j):                     Path via Intermediate Node k:
        (i) --------------------------> (j)             (i) ----------> (k) ----------> (j)
                  dist[i][j]                                dist[i][k]      dist[k][j]

DP State Transition: dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) ⚡
```

---

## 2. Core Concepts & LeetCode 1334 All-Pairs Threshold City Architecture

### 2.1 LeetCode 1334 Strategy Matrix
Given $N$ cities, `edges`, and `distanceThreshold`:
1. Initialize 2D matrix `dist[N][N]` with `INF`, set `dist[i][i] = 0`.
2. Fill direct edge weights from `edges`.
3. Run Floyd-Warshall DP ($k, i, j$ loops).
4. For each city $i$, count cities $j$ with `dist[i][j] <= distanceThreshold`.
5. Return city with minimum reachable count (break ties by returning largest city index) in **$O(V^3)$ Time**.

```
All-Pairs Shortest Path Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm Variant     | Outer Loop        | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+
| **Floyd-Warshall**    | Intermediate $k$  | **$O(V^3)$ Cubic ⚡**| **$O(V^2)$ Matrix ⚡**|
| $V \times$ Dijkstra   | Source $s$        | $O(V \cdot (V + E) \log V)$| $O(V + E)$ Adjacency|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Floyd-Warshall: k loop MUST be outermost! dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])!"**

---

## 3. Characteristics & Outer Loop $k$ Ordering Proof

### 3.1 Mathematical Proof of Outermost Loop $k$ Invariant
* **Claim**: The intermediate vertex loop $k$ MUST be the outermost loop.
* **Proof**:
  - Floyd-Warshall builds shortest paths bottom-up by incrementally considering larger sets of allowed intermediate nodes $\{0 \dots k\}$.
  - To correctly compute `dist[i][j]` using intermediate node $k$, the paths `dist[i][k]` and `dist[k][j]` MUST ALREADY BE FINALIZED using intermediate nodes $\{0 \dots k-1\}$.
  - Putting $k$ as the outer loop guarantees subproblems for $\{0 \dots k-1\}$ are fully solved before evaluating node $k$! ⚡

---

## 4. Internal Working Mechanics
Tracing Floyd-Warshall DP step for Intermediate $k=2$ between Node $i=0$ and Node $j=1$:

```
Initial: dist[0][1] = 9 (Direct path).
Intermediate 2: dist[0][2] = 3, dist[2][1] = 4.

Check DP Transition for k = 2:
- dist[0][1] = min(dist[0][1] (9), dist[0][2] (3) + dist[2][1] (4))
- dist[0][1] = min(9, 7) = 7!

Shortest path 0 -> 1 updated to 7 via intermediate node 2! ✅ (O(V^3) Total Time!)
```

---

## 5. Visual Diagram
Floyd-Warshall Triply Nested DP Topography:

```
                  Intermediate Node k
                    /             \
       dist[i][k]  /               \  dist[k][j]
                  v                 v
            Start Node i -------> End Node j
                         dist[i][j]
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 1334 (Find the City With the Smallest Number of Neighbors at a Threshold Distance):

```java
import java.util.*;

// LeetCode 1334: Floyd-Warshall All-Pairs Shortest Path
public class FloydWarshallMaster {

    private static final int INF = 1000000000; // Large constant to prevent overflow

    // LeetCode 1334 Solution O(V^3) Time, O(V^2) Space
    public int findTheCity(int n, int[][] edges, int distanceThreshold) {
        int[][] dist = new int[n][n];

        // Step 1: Initialize Distance Matrix
        for (int i = 0; i < n; i++) {
            Arrays.fill(dist[i], INF);
            dist[i][i] = 0; // Distance to self is 0
        }

        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            int w = edge[2];
            dist[u][v] = w;
            dist[v][u] = w; // Undirected graph
        }

        // Step 2: Floyd-Warshall Triply Nested DP Loops (k MUST be outermost!)
        for (int k = 0; k < n; k++) {
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < n; j++) {
                    if (dist[i][k] != INF && dist[k][j] != INF) {
                        dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
                    }
                }
            }
        }

        // Step 3: Count reachable cities within distanceThreshold for each city
        int minReachableCount = n + 1;
        int bestCity = -1;

        for (int i = 0; i < n; i++) {
            int reachableCount = 0;
            for (int j = 0; j < n; j++) {
                if (i != j && dist[i][j] <= distanceThreshold) {
                    reachableCount++;
                }
            }

            // Select city with smallest reachable count (break ties by largest city index)
            if (reachableCount <= minReachableCount) {
                minReachableCount = reachableCount;
                bestCity = i;
            }
        }

        return bestCity;
    }
}
```

> **Quick Syntax:**
```java
// Floyd-Warshall Core DP Line
for (int k=0; k<n; k++) for (int i=0; i<n; i++) for (int j=0; j<n; j++)
    if (dist[i][k] != INF && dist[k][j] != INF) dist[i][j] = Math.min(dist[i][j], dist[i][k] + dist[k][j]);
```

---

## 7. Concrete Problem Examples
* **LeetCode 1334 - Find the City With Smallest Neighbors**: Primary problem.
* **All-Pairs Distance Matrix Pre-computation**: Network routing matrices.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 1334 `findTheCity`:

```java
public class FloydWarshallDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 1334 Floyd-Warshall Test ===");
        FloydWarshallMaster solver = new FloydWarshallMaster();

        int n = 4;
        int[][] edges = {{0,1,3}, {1,2,1}, {1,3,4}, {2,3,1}};
        int distanceThreshold = 4;

        int city = solver.findTheCity(n, edges, distanceThreshold);
        System.out.println("Best City Index: " + city); // Output: 3 ✅
    }
}
```

---

## 9. Complexity Analysis

| All-Pairs Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Floyd-Warshall DP** | **$O(V^3)$ Cubic ⚡** | **$O(V^2)$ Matrix Space**| Triply nested loop ($k, i, j$) |
| **$V \times$ Dijkstra** | $O(V \cdot (V + E) \log V)$| $O(V + E)$ Space | Run Dijkstra from all $V$ sources |

---

## 10. Edge Cases & Boundary Handling
* **Self-Distance `dist[i][i]`**: Initialized to 0. If `dist[i][i] < 0` at end $\implies$ Negative Cycle.
* **Disconnected Pair $(i, j)$**: Remains `INF` ($10^9$).

---

## 11. Common Mistakes & Anti-Patterns
* **Putting Intermediate Node $k$ as the Inner Loop**:
  - Placing $k$ as the innermost loop (`for i, for j, for k`) calculates incorrect distances because intermediate subproblems are not solved in topological DP order.
  - **ALWAYS put intermediate node loop $k$ as the VERY FIRST OUTERMOST loop**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Floyd-Warshall Uses `INF = 1000000000` Instead of `Integer.MAX_VALUE`:
> If `dist[i][k] = Integer.MAX_VALUE` and `dist[k][j] = 5`, adding `dist[i][k] + dist[k][j]` causes **32-Bit Integer Overflow** into negative values (`-2147483643`), corrupting `Math.min` calculations!
> Always use a large sentinel constant like `1000000000` (`10^9`) or check `dist[i][k] != INF` explicitly before adding! ⚡

> **Memory Trick:** **"Use INF = 10^9 to prevent integer overflow in dist[i][k] + dist[k][j]!"**

---

## 13. System & Implementation Comparisons

| Feature | Floyd-Warshall Algorithm | $V \times$ Dijkstra's Algorithm |
| :--- | :--- | :--- |
| **Implementation** | **5 Lines Triply Nested Loop ⚡**| Complex PriorityQueue Loop |
| **Graph Density** | **Optimal for Dense Graphs ($E \approx V^2$) ⚡**| Optimal for Sparse Graphs |
| **Negative Edges** | **Supported (No negative cycles) ⚡**| Not Supported |

---

## 14. How to Recognize This in Questions
* **"Find all-pairs shortest paths or smallest reachable neighbors threshold on V <= 400"** $\rightarrow$ Floyd-Warshall.

---

## 15. Frequently Asked Interview Questions
* **Q: Why must the intermediate node loop $k$ be the outermost loop?**  
  *A:* To guarantee that all shortest paths using intermediate nodes $\{0 \dots k-1\}$ are fully computed before evaluating paths through node $k$.
* **Q: How does Floyd-Warshall detect negative weight cycles?**  
  *A:* By checking if `dist[i][i] < 0` for any vertex $i$ on the matrix diagonal.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: FLOYD-WARSHALL ALGORITHM (LEETCODE 1334)              |
+-----------------------------------------------------------------------+
| • Triply Loop    : k MUST be outermost! (for k; for i; for j)         |
| • DP Transition  : dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])|
| • Integer Guard  : Use INF = 10^9 to prevent 32-bit integer overflow!  |
| • Negative Cycle : dist[i][i] < 0 on matrix diagonal signals cycle!   |
| • Time Bounds    : O(V^3) Cubic Time | O(V^2) Matrix Auxiliary Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Floyd-Warshall in Java in 5 lines of code.
- [ ] I can write LeetCode 1334 (`Find the City With Smallest Neighbors`).
- [ ] I know why $k$ MUST be the outermost loop.
- [ ] I know why `INF = 10^9` is used instead of `Integer.MAX_VALUE`.
- [ ] I can trace DP matrix transitions step by step.
