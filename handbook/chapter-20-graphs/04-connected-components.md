# 04. Connected Components, Subgraph Isolation & Component Counting Algorithms

## 1. Introduction
A **Connected Component** in an undirected graph $G = (V, E)$ is a maximal subgraph in which any two vertices are connected to each other by at least one valid path, and which is connected to no additional vertices in the rest of the graph. Identifying connected components, counting total components, and extracting the largest component size are foundational graph tasks executed via **Depth-First Search (DFS)**, **Breadth-First Search (BFS)**, or **Disjoint Set Union (DSU)** in **$O(V + E)$ Linear Time**.

> **Important:** The Connected Component Partition Invariant:
> 1. **Component Partitioning**: The vertex set $V$ is partitioned into disjoint non-overlapping subsets $C_1, C_2, \dots, C_K$:
>    $$\bigcup_{i=1}^{K} C_i = V \quad \text{and} \quad C_i \cap C_j = \emptyset \quad (\forall i \ne j)$$
> 2. **Component Traversal Outer Loop**: Iterate $i = 0 \dots V-1$. If `!visited[i]`, increment `componentCount++` and launch DFS/BFS from node $i$ to mark all reachable nodes in component $C_i$ as visited in $O(V + E)$ time! ⚡

```
Graph Connected Components Partition Topology:
Component 1 (Nodes {0, 1, 2}):        Component 2 (Nodes {3, 4}):        Component 3 (Node {5}):
      (0) --- (1)                           (3) --- (4)                        (5)
       |
      (2)

Total Connected Components = 3! Component 1 Size = 3, Component 2 Size = 2, Component 3 Size = 1. ⚡
```

---

## 2. Core Concepts & DFS vs BFS vs DSU Component Counting

### 2.1 Algorithm Strategy Matrix
```
Connected Component Counting Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Component Strategy    | Primary Mechanism | Time Complexity   | Best Use Case     |
+-----------------------+-------------------+-------------------+-------------------+
| **DFS Component Scan**| Outer Loop + DFS  | **$O(V + E)$ Linear ⚡**| Static Graph      |
| **BFS Component Scan**| Outer Loop + BFS  | **$O(V + E)$ Linear ⚡**| Static Graph      |
| **DSU Dynamic Tracker**| `dsu.union(u, v)`| **$O(E \cdot \alpha(V))$ ⚡**| Dynamic Edge Stream|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Component Count: Outer loop i=0..V-1; if !visited[i], count++ and run DFS/BFS!"**

---

## 3. Characteristics & Component Extraction Invariants

### 3.1 Extracting Component Details
Beyond counting components, real-world systems require returning:
* **All Nodes per Component**: `List<List<Integer>> components`.
* **Largest Component Size**: `max(component.size())`.
* **Component ID Map**: `int[] componentId` mapping node $v \to C_i$.

---

## 4. Internal Working Mechanics
Tracing Component Counting on Graph $V=6$ with Edges `(0,1)`, `(0,2)`, `(3,4)`:

```
Init: visited = [false, false, false, false, false, false], count = 0.

Outer Loop i = 0:
- visited[0] is false! Increment count = 1. Launch dfs(0).
- dfs(0) visits 0, 1, 2. Sets visited[0]=true, visited[1]=true, visited[2]=true.
- Component 1 = {0, 1, 2}.

Outer Loop i = 1, 2:
- visited[1] and visited[2] are true -> Skip!

Outer Loop i = 3:
- visited[3] is false! Increment count = 2. Launch dfs(3).
- dfs(3) visits 3, 4. Sets visited[3]=true, visited[4]=true.
- Component 2 = {3, 4}.

Outer Loop i = 4: visited[4] is true -> Skip.

Outer Loop i = 5:
- visited[5] is false! Increment count = 3. Launch dfs(5).
- dfs(5) visits 5. Sets visited[5]=true.
- Component 3 = {5}.

Total Connected Components = 3! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
Component Partition Outer Loop Topography:

```
Nodes: [0, 1, 2, 3, 4, 5]
Visited: [F, F, F, F, F, F]

i=0 (!visited) ---> DFS(0) ---> Marks [0, 1, 2] Visited ---> Component 1 {0,1,2}
i=3 (!visited) ---> DFS(3) ---> Marks [3, 4] Visited    ---> Component 2 {3,4}
i=5 (!visited) ---> DFS(5) ---> Marks [5] Visited       ---> Component 3 {5}
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Connected Component Counting, Component Extraction, and Largest Component Size:

```java
import java.util.*;

public class ConnectedComponentsMaster {

    // 1. Count Total Connected Components O(V + E) Time
    public int countComponents(int n, int[][] edges) {
        List<List<Integer>> adj = buildAdjacencyList(n, edges);
        boolean[] visited = new boolean[n];
        int count = 0;

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                count++;
                dfsMarkComponent(adj, visited, i);
            }
        }

        return count;
    }

    private void dfsMarkComponent(List<List<Integer>> adj, boolean[] visited, int u) {
        visited[u] = true;
        for (int v : adj.get(u)) {
            if (!visited[v]) {
                dfsMarkComponent(adj, visited, v);
            }
        }
    }

    // 2. Extract All Connected Components List O(V + E) Time
    public List<List<Integer>> getComponentList(int n, int[][] edges) {
        List<List<Integer>> adj = buildAdjacencyList(n, edges);
        boolean[] visited = new boolean[n];
        List<List<Integer>> components = new ArrayList<>();

        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                List<Integer> currentComponent = new ArrayList<>();
                dfsCollectComponent(adj, visited, i, currentComponent);
                components.add(currentComponent);
            }
        }

        return components;
    }

    private void dfsCollectComponent(List<List<Integer>> adj, boolean[] visited, int u, List<Integer> currentComponent) {
        visited[u] = true;
        currentComponent.add(u);
        for (int v : adj.get(u)) {
            if (!visited[v]) {
                dfsCollectComponent(adj, visited, v, currentComponent);
            }
        }
    }

    // Helper: Build Undirected Adjacency List O(V + E) Time
    private List<List<Integer>> buildAdjacencyList(int n, int[][] edges) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        for (int[] edge : edges) {
            adj.get(edge[0]).add(edge[1]);
            adj.get(edge[1]).add(edge[0]);
        }
        return adj;
    }
}
```

> **Quick Syntax:**
```java
// Component Counting Outer Loop Line
for (int i = 0; i < n; i++) if (!visited[i]) { count++; dfs(adj, visited, i); }
```

---

## 7. Concrete Problem Examples
* **LeetCode 323 - Number of Connected Components in an Undirected Graph**: Primary problem.
* **LeetCode 547 - Number of Provinces**: Matrix component counting.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing `getComponentList` and `countComponents`:

```java
public class ConnectedComponentsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Graph Connected Components Test ===");
        ConnectedComponentsMaster solver = new ConnectedComponentsMaster();

        int n = 6;
        int[][] edges = {{0, 1}, {0, 2}, {3, 4}};

        int count = solver.countComponents(n, edges);
        System.out.println("Total Connected Components: " + count); // Output: 3

        List<List<Integer>> components = solver.getComponentList(n, edges);
        System.out.println("Extracted Components: " + components);
        // Output: [[0, 1, 2], [3, 4], [5]] ✅
    }
}
```

---

## 9. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **`countComponents()`** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Visited & Stack**| Outer loop + DFS traversal |
| **`getComponentList()`**| **$O(V + E)$ Linear ⚡** | **$O(V)$ Components List**| Component node collection |

---

## 10. Edge Cases & Boundary Handling
* **Graph with 0 Edges ($E = 0$)**: Every vertex forms an isolated component of size 1 $\implies$ returns $V$ components.
* **Fully Connected Graph**: Single connected component containing all $V$ nodes $\implies$ returns $1$.

---

## 11. Common Mistakes & Anti-Patterns
* **Omitting the Outer Loop `for (int i = 0; i < V; i++)`**:
  - Running DFS only from node 0 fails to visit nodes in disconnected components.
  - **ALWAYS use an outer loop over all vertices $0 \dots V-1$**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Outer Loop Over All Vertices Is Mandatory:
> Graph traversal algorithms (BFS/DFS) started from a single node $s$ can ONLY visit nodes reachable from $s$.
> To guarantee visiting every node in a disconnected graph, we MUST use an outer loop `for (int i = 0; i < V; i++)` that launches traversal whenever `!visited[i]`.

> **Memory Trick:** **"Outer loop visits all disconnected components; single DFS visits only 1 component!"**

---

## 13. System & Implementation Comparisons

| Feature | DFS/BFS Component Counting | DSU Component Counting |
| :--- | :--- | :--- |
| **Graph Input Type** | **Static Graph $O(V + E)$ ⚡**| Dynamic Edge Stream $O(\alpha(V))$ |
| **Code Length** | ~15 Lines Clean Code | ~30 Lines DSU Class |
| **Space Footprint** | $O(V)$ Visited Array | $O(V)$ Parent Array |

---

## 14. How to Recognize This in Questions
* **"Find total number of disconnected subgraphs or isolated groups in undirected graph"** $\rightarrow$ Connected Components.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the time complexity of finding all connected components in an undirected graph?**  
  *A:* $O(V + E)$ linear time using DFS or BFS with an outer loop over all vertices.
* **Q: How does DSU compare with DFS for static component counting?**  
  *A:* Both run in near-linear time ($O(V + E)$ for DFS, $O(E \cdot \alpha(V))$ for DSU). DFS is slightly simpler for static graphs; DSU is superior for dynamic edge additions.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: CONNECTED COMPONENTS                                  |
+-----------------------------------------------------------------------+
| • Invariant Rule : Outer loop for (i = 0...V-1) checks if (!visited[i])|
| • Count Increment: Increment count++ on each unvisited node in outer loop|
| • DFS Traversal  : Recurse from node i to mark all component nodes visited|
| • Component Size : Accumulate node count per component during DFS    |
| • Time Bounds    : O(V + E) Linear Time | O(V) Auxiliary Memory Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write `countComponents` in Java in $O(V + E)$ time.
- [ ] I can write `getComponentList` to extract node components.
- [ ] I know why the outer loop over all vertices is mandatory.
- [ ] I can contrast static DFS component counting with DSU.
- [ ] I can trace component partitioning step by step.
