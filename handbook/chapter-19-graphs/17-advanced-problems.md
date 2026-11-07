# 17. Advanced Graph Problems: Bitmask BFS, Minimum Height Trees & Path Reconstruction

## 1. Introduction
**Advanced Graph Problems** combine graph algorithms with **Bitmask State Tracking**, **BFS Level Distances**, **Backtracking Path Reconstruction**, and **Topological Leaf Trimming**. Hard-level problems like **Word Ladder II (LeetCode 126)**, **Minimum Height Trees (LeetCode 310)**, and **Shortest Path Visiting All Nodes (LeetCode 847)** require multi-stage graph pipelines. Using bitmasks $1 \ll u$ to represent visited node sets in BFS queues enables finding globally shortest paths across complex state spaces in **$O(N \cdot 2^N)$ Time**.

> **Important:** Core Invariants of Advanced Graph Algorithms:
> 1. **Bitmask BFS State (LeetCode 847)**:
>    - Queue stores state tuples `(node, visitedBitmask)`.
>    - Target state: `visitedBitmask == (1 << N) - 1` (All $N$ nodes visited!).
>    - Visited guard array: `boolean[N][1 << N]` prevents duplicate state exploration!
> 2. **Topological Leaf Trimming (LeetCode 310)**:
>    - Trim leaves (nodes with `degree == 1`) layer-by-layer using BFS until at most 2 centroid nodes remain!
> 3. **Word Ladder II (LeetCode 126)**:
>    - Stage 1: BFS from `beginWord` to record shortest level distance `map<String, Integer>`.
>    - Stage 2: Backtracking DFS from `endWord` back to `beginWord` to collect ALL shortest path sequences! ⚡

```
Bitmask BFS State Space Topology (LeetCode 847 Shortest Path Visiting All Nodes):
State Tuple: (currNode, bitmask)
Initial Queue: Push ALL nodes (i, 1 << i) for Multi-Source Initialization!

Target Check: bitmask == (1 << N) - 1 (All bits 1!).
State Guard: visited[next][mask | (1 << next)] prevents infinite state loops! ⚡
```

---

## 2. Core Concepts & Advanced Problem Pattern Strategy Matrix

### 2.1 Advanced Graph Strategy Matrix
```
Advanced Graph Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Pattern       | State Tracking    | Time Complexity   | Primary Target    |
+-----------------------+-------------------+-------------------+-------------------+
| **Bitmask BFS (847)** | `(node, mask)`    | **$O(N \cdot 2^N)$ ⚡**| Min steps visit all|
| **Leaf Trimming (310)**| `degree[] == 1`   | **$O(V + E)$ Linear ⚡**| Graph Centroid Nodes|
| **Path Reconstruct (126)**| BFS Dist + DFS| **$O(V + E)$ ⚡**  | All Shortest Paths|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LeetCode 847: Queue state = (node, mask)! Target check: mask == (1 << N) - 1!"**

---

## 3. Characteristics & $O(N \cdot 2^N)$ Bitmask Complexity Proof

### 3.1 Mathematical Proof of $O(N \cdot 2^N)$ Bitmask BFS Complexity
* Total unique states: $N$ possible current nodes $\times 2^N$ possible visited bitmasks.
* Total state space size: $N \cdot 2^N$.
* Each state transitions to at most $N$ neighbors.
* Total Time Complexity: $\mathbf{O(N \cdot 2^N) \text{ Time}}$ (Feasible for $N \le 12$)! ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 310 (Minimum Height Trees) on Tree $N=4$ with Edges `[[1,0],[1,2],[1,3]]`:

```
Degrees: Node 0: 1, Node 1: 3, Node 2: 1, Node 3: 1.

Step 1: Collect Initial Leaves (degree == 1): Queue = [0, 2, 3]. Remaining nodes = 4.

Step 2: Trim Layer 1 Leaves (size = 3):
- Pop 0: decrement degree[1] (becomes 2).
- Pop 2: decrement degree[1] (becomes 1).
- Pop 3: decrement degree[1] (becomes 0).
- Remaining nodes = 4 - 3 = 1 (<= 2!). Loop terminates!

Remaining Node = [1]! Centroid Root = Node 1! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
Topological Leaf Trimming (LeetCode 310) Topography:

```
Initial Tree:   (0) --- (1) --- (2)
                         |
                        (3)
Leaves Layer 1: Nodes 0, 2, 3 (degree 1) ---> Trim Leaves!
Remaining Centroid Node: Node 1 (Root of Minimum Height Tree!) ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 847 (Shortest Path Visiting All Nodes) and LeetCode 310 (Minimum Height Trees):

```java
import java.util.*;

// LeetCode 847 & 310: Advanced Graph Algorithms
public class AdvancedGraphMaster {

    // 1. LeetCode 847: Shortest Path Visiting All Nodes (Bitmask BFS) O(N * 2^N) Time
    public int shortestPathLength(int[][] graph) {
        if (graph == null || graph.length == 0) return 0;
        int n = graph.length;

        int finalState = (1 << n) - 1; // Target mask: all n bits set to 1
        Queue<int[]> queue = new LinkedList<>(); // State: [currNode, visitedMask]
        boolean[][] visited = new boolean[n][1 << n];

        // Multi-source BFS initialization: Start from ALL nodes simultaneously at step 0
        for (int i = 0; i < n; i++) {
            int mask = (1 << i);
            queue.offer(new int[]{i, mask});
            visited[i][mask] = true;
        }

        int steps = 0;

        while (!queue.isEmpty()) {
            int levelSize = queue.size();

            for (int i = 0; i < levelSize; i++) {
                int[] curr = queue.poll();
                int u = curr[0];
                int mask = curr[1];

                if (mask == finalState) {
                    return steps; // Reached all nodes!
                }

                for (int v : graph[u]) {
                    int nextMask = mask | (1 << v); // Set bit for neighbor v

                    if (!visited[v][nextMask]) {
                        visited[v][nextMask] = true;
                        queue.offer(new int[]{v, nextMask});
                    }
                }
            }

            steps++;
        }

        return -1;
    }

    // 2. LeetCode 310: Minimum Height Trees (Topological Leaf Trimming) O(V + E) Time
    public List<Integer> findMinHeightTrees(int n, int[][] edges) {
        List<Integer> result = new ArrayList<>();
        if (n <= 0) return result;
        if (n == 1) {
            result.add(0);
            return result;
        }

        List<Set<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new HashSet<>());

        int[] degree = new int[n];
        for (int[] edge : edges) {
            int u = edge[0];
            int v = edge[1];
            adj.get(u).add(v);
            adj.get(v).add(u);
            degree[u]++;
            degree[v]++;
        }

        // Collect initial leaf nodes (degree == 1)
        Queue<Integer> leaves = new LinkedList<>();
        for (int i = 0; i < n; i++) {
            if (degree[i] == 1) {
                leaves.offer(i);
            }
        }

        int remainingNodes = n;

        // Trim leaves layer-by-layer until at most 2 centroid nodes remain
        while (remainingNodes > 2) {
            int leafCount = leaves.size();
            remainingNodes -= leafCount;

            for (int i = 0; i < leafCount; i++) {
                int leaf = leaves.poll();

                for (int neighbor : adj.get(leaf)) {
                    adj.get(neighbor).remove(leaf);
                    degree[neighbor]--;

                    if (degree[neighbor] == 1) {
                        leaves.offer(neighbor); // Enqueue new leaf
                    }
                }
            }
        }

        result.addAll(leaves);
        return result;
    }
}
```

> **Quick Syntax:**
```java
// Bitmask BFS Target Check Line
if (mask == (1 << n) - 1) return steps;
```

---

## 7. Concrete Problem Examples
* **LeetCode 847 - Shortest Path Visiting All Nodes**: Bitmask state BFS.
* **LeetCode 310 - Minimum Height Trees**: Topological leaf trimming.
* **LeetCode 126 - Word Ladder II**: Dual-stage BFS + DFS path reconstruction.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 847 `shortestPathLength`:

```java
public class AdvancedGraphDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 847 Bitmask BFS Test ===");
        AdvancedGraphMaster solver = new AdvancedGraphMaster();

        int[][] graph = {{1,2,3}, {0}, {0}, {0}};
        int steps = solver.shortestPathLength(graph);

        System.out.println("Shortest Steps to Visit All Nodes: " + steps); // Output: 4 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem / Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Bitmask BFS (847)**| **$O(N \cdot 2^N)$ Exponential ⚡**| **$O(N \cdot 2^N)$ Visited State**| Multi-source BFS with state `(node, mask)` |
| **Leaf Trimming (310)**| **$O(V + E)$ Linear ⚡**| **$O(V + E)$ Adjacency**| Layer-by-layer leaf queue reduction |

---

## 10. Edge Cases & Boundary Handling
* **$N = 1$ Single Node**: Handled in $O(1)$ time, returning `0` steps or `[0]` root.
* **Complete Graph (All-to-All Edges)**: Bitmask BFS visits all nodes in $N-1$ steps.

---

## 11. Common Mistakes & Anti-Patterns
* **Using a 1D `visited[node]` Array for Bitmask BFS (LeetCode 847)**:
  - Bitmask BFS permits re-visiting nodes provided the visited set bitmask is DIFFERENT!
  - Using 1D `visited[node]` prevents valid back-tracking paths across different set masks.
  - **ALWAYS use 2D `visited[node][mask]` for Bitmask BFS**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Leaf Trimming (LeetCode 310) Leaves At Most 2 Nodes:
> In any tree, the tree centroids (nodes that minimize max depth) can number AT MOST 1 OR 2!
> Trimming leaves layer-by-layer shrinks the tree inward while preserving tree centroids until `remainingNodes <= 2`! ⚡

> **Memory Trick:** **"Tree centroids = At most 2 nodes remaining after layer-by-layer leaf trimming!"**

---

## 13. System & Implementation Comparisons

| Feature | Bitmask BFS (LeetCode 847) | Standard BFS |
| :--- | :--- | :--- |
| **State Key** | **`(node, mask)` Tuple ⚡**| `node` Single Value |
| **Re-visiting Nodes**| Allowed with different mask | Strictly forbidden |
| **Target State** | `mask == (1 << n) - 1` | `node == target` |

---

## 14. How to Recognize This in Questions
* **"Find shortest path visiting every node at least once on N <= 12"** $\rightarrow$ LeetCode 847 (Bitmask BFS).

---

## 15. Frequently Asked Interview Questions
* **Q: Why are all nodes pushed to the queue initially in LeetCode 847?**  
  *A:* Because the shortest path visiting all nodes can start from ANY node as the initial origin.
* **Q: Why does LeetCode 310 trim leaves until `remainingNodes <= 2`?**  
  *A:* Because a tree can have at most 1 or 2 centroid nodes that minimize the tree's maximum height.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ADVANCED GRAPH ALGORITHMS                             |
+-----------------------------------------------------------------------+
| • Bitmask BFS    : Queue state = (node, mask); Target = (1 << n) - 1  |
| • State Guard    : boolean[N][1 << N] visited array                   |
| • Leaf Trimming  : Degree == 1 queue reduction while (remaining > 2)  |
| • Centroid Bounds: At most 2 nodes remain in tree centroid set! ⚡    |
| • Performance    : Bitmask O(N * 2^N) | Leaf Trimming O(V + E) ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 847 (`Shortest Path Visiting All Nodes`) using Bitmask BFS.
- [ ] I can write LeetCode 310 (`Minimum Height Trees`) using leaf trimming.
- [ ] I know why 2D `visited[node][mask]` is required for Bitmask BFS.
- [ ] I know why at most 2 centroids remain in a tree.
- [ ] I can trace Bitmask BFS transitions step by step.
