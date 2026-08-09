# 02. Breadth-First Search (BFS), Level-Order Traversal & Unweighted Shortest Path

## 1. Introduction
**Breadth-First Search (BFS)** is a fundamental graph traversal algorithm that explores vertices in strict **Level-by-Level (Order of Radius / Distance)** order from a starting source node. Powered by a **FIFO Queue (`Queue<Integer>`)** and a **`boolean[] visited` array**, BFS guarantees finding the **SHORTEST PATH (Minimum Number of Edges)** between the source node and any reachable vertex in an unweighted graph in **$O(V + E)$ Linear Time** and **$O(V)$ Auxiliary Memory**.

> **Important:** Core Invariants of Graph BFS:
> 1. **Shortest Path Guarantee**: In unweighted graphs, the first time BFS visits a node $v$, the recorded path distance is STRICTLY GUARANTEED to be the absolute minimum shortest path from source $s$ to $v$!
> 2. **Visited Guard Placement**: Mark a node as `visited[v] = true` IMMEDIATELY UPON ENQUEUING it into the Queue (NOT when popping/dequeuing!), preventing duplicate nodes from entering the Queue!
> 3. **Level-Order Queue Loop**: Process queue level by level using snapshot size `int levelSize = queue.size()`. ⚡

```
Graph BFS Level-Order Traversal Topology (Source = Node 0):
Level 0:                             [ Node 0 ]
                                    /          \
Level 1:                     [ Node 1 ]      [ Node 2 ]
                            /          \          \
Level 2:             [ Node 3 ]      [ Node 4 ]  [ Node 5 ]

Traversal Order: 0 -> 1 -> 2 -> 3 -> 4 -> 5! Guarantees Shortest Path in Unweighted Graphs! ⚡
```

---

## 2. Core Concepts & Single-Source vs Multi-Source BFS

### 2.1 BFS Operational Patterns Matrix
```
BFS Operational Patterns Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| BFS Variant           | Initial Queue State| Level Counter     | Target Problem    |
+-----------------------+-------------------+-------------------+-------------------+
| **Single-Source BFS** | Enqueue Source `s`| Distance Array    | Shortest Path     |
| **Multi-Source BFS**  | Enqueue ALL Sources| Level Steps      | Rotting Oranges   |
| **Word Ladder BFS**   | Enqueue Start Word| Transformation Hops| LeetCode 127      |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Graph BFS: Mark visited IMMEDIATELY on push to queue! Guarantees shortest path in unweighted graphs!"**

---

## 3. Characteristics & $O(V + E)$ Time Complexity Proof

### 3.1 Mathematical Proof of $O(V + E)$ BFS Complexity
* Every vertex $v \in V$ is marked `visited` and pushed into the Queue at most ONCE $\implies \mathbf{O(V)}$ Queue operations.
* When dequeuing vertex $u$, BFS iterates over all outgoing edges $(u, v)$. Across the entire traversal, every edge $e \in E$ is examined at most once (directed) or twice (undirected) $\implies \mathbf{O(E)}$ edge lookups.
* Total Time Complexity: $\mathbf{O(V + E) \text{ Strict Linear Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing BFS Shortest Path on Graph with Edges `(0, 1)`, `(0, 2)`, `(1, 3)`, `(2, 3)` (Source = 0):

```
Init: queue = [0], visited[0] = true, dist = [0, inf, inf, inf].

Step 1: Pop Node 0. Neighbors: 1 and 2.
- Node 1: visited[1] = true, dist[1] = 1, push 1.
- Node 2: visited[2] = true, dist[2] = 1, push 2.
- Queue = [1, 2].

Step 2: Pop Node 1. Neighbors: 0 (visited), 3.
- Node 3: visited[3] = true, dist[3] = dist[1] + 1 = 2, push 3.
- Queue = [2, 3].

Step 3: Pop Node 2. Neighbors: 0 (visited), 3 (visited!). Skip.
- Queue = [3].

Step 4: Pop Node 3. No unvisited neighbors. Loop ends.

Shortest distance from 0 to 3 is dist[3] = 2! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
BFS Wavefront Expansion Topography:

```
                  [ Source Node 0 ] (Dist = 0)
                 /                 \
         [ Node 1 ]               [ Node 2 ] (Wavefront 1: Dist = 1)
        /          \                  /
    [ Node 3 ]    [ Node 4 ]     [ Node 5 ]  (Wavefront 2: Dist = 2)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Single-Source BFS Shortest Path and Multi-Source BFS (LeetCode 994 Rotting Oranges):

```java
import java.util.*;

public class GraphBFSMaster {

    // 1. Single-Source BFS Shortest Path O(V + E) Time
    public int[] shortestPathUnweighted(List<List<Integer>> adj, int numVertices, int source) {
        int[] dist = new int[numVertices];
        Arrays.fill(dist, -1); // -1 represents unvisited / unreachable

        Queue<Integer> queue = new LinkedList<>();

        // Enqueue Source and Mark Visited IMMEDIATELY
        queue.offer(source);
        dist[source] = 0;

        while (!queue.isEmpty()) {
            int u = queue.poll();

            for (int v : adj.get(u)) {
                if (dist[v] == -1) { // Unvisited neighbor check
                    dist[v] = dist[u] + 1; // Record shortest path distance
                    queue.offer(v);        // Enqueue neighbor
                }
            }
        }

        return dist;
    }

    // 2. Multi-Source BFS: LeetCode 994 Rotting Oranges O(M * N) Time
    public int orangesRotting(int[][] grid) {
        if (grid == null || grid.length == 0) return 0;

        int rows = grid.length;
        int cols = grid[0].length;

        Queue<int[]> queue = new LinkedList<>();
        int freshCount = 0;

        // Step 1: Add ALL initial rotten oranges (Multi-Sources) to Queue
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                if (grid[r][c] == 2) {
                    queue.offer(new int[]{r, c});
                } else if (grid[r][c] == 1) {
                    freshCount++;
                }
            }
        }

        if (freshCount == 0) return 0; // No fresh oranges to rot

        int minutes = 0;
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        // Step 2: Level-Order Multi-Source BFS
        while (!queue.isEmpty() && freshCount > 0) {
            int levelSize = queue.size();
            minutes++;

            for (int i = 0; i < levelSize; i++) {
                int[] curr = queue.poll();
                int r = curr[0];
                int c = curr[1];

                for (int[] d : dirs) {
                    int nr = r + d[0];
                    int nc = c + d[1];

                    if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && grid[nr][nc] == 1) {
                        grid[nr][nc] = 2; // Mark rotten (visited)
                        freshCount--;
                        queue.offer(new int[]{nr, nc});
                    }
                }
            }
        }

        return (freshCount == 0) ? minutes : -1;
    }
}
```

> **Quick Syntax:**
```java
// BFS Queue Push & Mark Line
if (dist[v] == -1) { dist[v] = dist[u] + 1; queue.offer(v); }
```

---

## 7. Concrete Problem Examples
* **LeetCode 994 - Rotting Oranges**: Multi-Source BFS.
* **LeetCode 127 - Word Ladder**: Word transformation BFS shortest path.
* **LeetCode 1091 - Shortest Path in Binary Matrix**: Grid BFS shortest path.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Multi-Source BFS Rotting Oranges (LeetCode 994):

```java
public class GraphBFSDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 994 Rotting Oranges Multi-Source BFS Test ===");
        GraphBFSMaster solver = new GraphBFSMaster();

        int[][] grid = {
            {2, 1, 1},
            {1, 1, 0},
            {0, 1, 1}
        };

        int minutes = solver.orangesRotting(grid);
        System.out.println("Minutes until all oranges rot: " + minutes); // Output: 4 ✅
    }
}
```

---

## 9. Complexity Analysis

| BFS Pattern | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Single-Source BFS** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Queue Memory** | Level-order queue traversal |
| **Multi-Source BFS (994)**| **$O(M \cdot N)$ Linear ⚡**| **$O(M \cdot N)$ Queue** | Initial queue load of all sources |

---

## 10. Edge Cases & Boundary Handling
* **Unreachable Vertices**: Distance remains `-1`.
* **Graph with Disconnected Components**: BFS visits only the component containing `source`.

---

## 11. Common Mistakes & Anti-Patterns
* **Marking Nodes as `visited` When Dequeuing (Polling) Instead of Enqueuing**:
  - Delaying the `visited` mark until dequeuing allows duplicate copies of the same node to enter the Queue thousands of times, causing severe memory spikes (`OutOfMemoryError`)!
  - **ALWAYS set `visited[v] = true` IMMEDIATELY when enqueuing (`queue.offer(v)`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why BFS Guarantees Shortest Path ONLY on Unweighted Graphs:
> BFS explores graph nodes in strictly increasing distance order ($d = 0, 1, 2, \dots$).
> On weighted graphs with varying edge costs (e.g. edge weights 1, 5, 10), a node visited at hop-distance 2 might have a higher cost than a path of 4 small edges.
> For weighted graphs, **Dijkstra's Algorithm (PriorityQueue)** MUST be used instead of BFS! ⚡

> **Memory Trick:** **"Unweighted Shortest Path = BFS! Weighted Shortest Path = Dijkstra!"**

---

## 13. System & Implementation Comparisons

| Feature | Breadth-First Search (BFS) | Depth-First Search (DFS) |
| :--- | :--- | :--- |
| **Data Structure** | **FIFO Queue (`LinkedList`)** | LIFO Stack / Recursion |
| **Shortest Path** | **Guaranteed on Unweighted Graphs ⚡**| No Shortest Path Guarantee |
| **Traversal Strategy**| Level-Order Wavefront Expansion | Deep Branch Exploration |

---

## 14. How to Recognize This in Questions
* **"Find minimum number of steps/hops/edges to reach target in unweighted graph"** $\rightarrow$ BFS.

---

## 15. Frequently Asked Interview Questions
* **Q: Why must nodes be marked `visited` immediately upon enqueuing?**  
  *A:* To prevent the same unvisited node from being pushed into the queue multiple times by adjacent neighboring nodes before it gets dequeued.
* **Q: How does Multi-Source BFS work?**  
  *A:* By enqueuing ALL starting source nodes into the Queue during initialization at time level $T = 0$, then executing standard BFS level-order expansion.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BREADTH-FIRST SEARCH (BFS)                            |
+-----------------------------------------------------------------------+
| • Data Structure : FIFO Queue (`Queue<Integer> queue = new LinkedList<>()`)|
| • Visited Rule   : Mark visited IMMEDIATELY upon enqueuing (offer)!   |
| • Shortest Path  : Guarantees shortest path ONLY on UNWEIGHTED graphs ⚡|
| • Multi-Source   : Enqueue ALL initial sources to Queue at level T=0  |
| • Time Bounds    : O(V + E) Linear Time | O(V) Queue Memory Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write single-source BFS shortest path in Java.
- [ ] I can write LeetCode 994 (`Rotting Oranges`) using Multi-Source BFS.
- [ ] I know why `visited` MUST be marked upon enqueuing.
- [ ] I know why BFS guarantees shortest paths ONLY on unweighted graphs.
- [ ] I can trace BFS wavefront expansion level by level.
