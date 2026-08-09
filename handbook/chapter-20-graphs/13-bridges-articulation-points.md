# 13. Tarjan's Bridge & Articulation Point Engine: `tin[]`, `low[]` & Critical Connections

## 1. Introduction
A **Bridge (Critical Edge)** in a connected graph is an edge whose removal increases the number of connected components (disconnects the graph!). An **Articulation Point (Cut Vertex)** is a vertex whose removal (along with its incident edges) disconnects the graph. Discovered by Robert Tarjan, **Tarjan's Low-Link DFS Algorithm** identifies all bridges and articulation points in an undirected graph in **$O(V + E)$ Linear Time** using discovery timestamps `tin[]` and lowest reachable discovery times `low[]`. It serves as the primary engine for **Critical Connections in a Network (LeetCode 1192)**.

> **Important:** Tarjan's Low-Link Invariants:
> 1. **Discovery Timestamp (`tin[u]`)**: The exact DFS entry time counter when node $u$ is first visited.
> 2. **Lowest Reachable Timestamp (`low[u]`)**: The smallest discovery timestamp reachable from node $u$ using DFS tree edges and at most ONE back-edge!
> 3. **Bridge Condition (Critical Edge)**: Edge $(u \to v)$ is a BRIDGE IF AND ONLY IF:
>    $$\text{low}[v] > \text{tin}[u]$$
>    (Meaning neighbor $v$ has NO back-edge back to $u$ or any ancestor of $u$!).
> 4. **Articulation Point Condition (Cut Vertex)**: Non-root vertex $u$ is a CUT VERTEX IF:
>    $$\text{low}[v] \ge \text{tin}[u]$$
>    (For root vertex $u$, it is a cut vertex IF AND ONLY IF it has $\ge 2$ DFS tree children!). ⚡

```
Tarjan's Low-Link Bridge Topology (LeetCode 1192):
Nodes 0 - 1 - 2 form a Cycle (tin[0]=1, tin[1]=2, tin[2]=3, low[2]=1).
Edge (1 -> 3): tin[1]=2, tin[3]=4, low[3]=4.

Check Edge (1 -> 3): low[3] (4) > tin[1] (2) ---> EDGE (1, 3) IS A CRITICAL BRIDGE! ⚡
```

---

## 2. Core Concepts & Bridges vs Articulation Points Comparison

### 2.1 Low-Link Condition Comparison Matrix
```
Low-Link Condition Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Structural Criticality| Mathematical Rule | Special Root Case | Primary Problem   |
+-----------------------+-------------------+-------------------+-------------------+
| **Bridge (Critical Edge)**| **`low[v] > tin[u]` ⚡**| Standard Rule     | LeetCode 1192     |
| **Articulation Point**| **`low[v] >= tin[u]` ⚡**| Root children $\ge 2$| Network Vulnerability|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Bridge condition: low[v] > tin[u] strictly! Cut Vertex condition: low[v] >= tin[u]!"**

---

## 3. Characteristics & $O(V + E)$ Linear Time Proof

### 3.1 Mathematical Proof of $O(V + E)$ Low-Link DFS Complexity
* Tarjan's algorithm executes a single DFS traversal across the graph.
* Every vertex $u$ is visited once, initializing `tin[u]` and `low[u]` $\implies O(V)$.
* Every edge $(u, v)$ is traversed at most twice to compute `low[u] = min(low[u], low[v])` or `low[u] = min(low[u], tin[v])` $\implies O(E)$.
* Total Time Complexity: $\mathbf{O(V + E) \text{ Strict Linear Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Tarjan's Bridge Search (LeetCode 1192) on Graph with Edges `(0-1)`, `(1-2)`, `(2-0)`, `(1-3)`:

```
Init timer = 1, tin = [0,0,0,0], low = [0,0,0,0].

DFS(0, parent=-1): tin[0]=1, low[0]=1. Recurse 1.
- DFS(1, parent=0): tin[1]=2, low[1]=2. Recurse 2 and 3.
  - DFS(2, parent=1): tin[2]=3, low[2]=3. Neighbor 0 is visited (not parent)!
    - Back-edge (2->0): low[2] = min(low[2], tin[0]) = min(3, 1) = 1.
    - Return to 1: low[1] = min(low[1], low[2]) = min(2, 1) = 1.
  - DFS(3, parent=1): tin[3]=4, low[3]=4. No neighbors.
    - Check Bridge Condition for (1 -> 3): low[3] (4) > tin[1] (2) ---> BRIDGE FOUND: [1, 3]!

Resulting Critical Connections: [[1, 3]]! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
Tarjan's Low-Link Bridge Detection Topography:

```
Cycle Component (0-1-2):                     Critical Bridge Edge (1-3):
tin[0]=1, tin[1]=2, tin[2]=3                  tin[1]=2, tin[3]=4
low[0]=1, low[1]=1, low[2]=1                  low[3]=4
  (0) ----- (1) ==========================> (3)
   |         |    low[3] (4) > tin[1] (2)
   +---(2)---+    Edge (1, 3) IS A BRIDGE! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 1192 (Critical Connections in a Network / Bridges) using Tarjan's DFS:

```java
import java.util.*;

// LeetCode 1192: Critical Connections in a Network (Bridges in a Graph)
public class BridgesMaster {

    private int timer = 1;

    // LeetCode 1192 Solution O(V + E) Time, O(V + E) Space
    public List<List<Integer>> criticalConnections(int n, List<List<Integer>> connections) {
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        for (List<Integer> conn : connections) {
            int u = conn.get(0);
            int v = conn.get(1);
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] tin = new int[n];
        int[] low = new int[n];
        boolean[] visited = new boolean[n];
        List<List<Integer>> bridges = new ArrayList<>();

        // Launch Tarjan's DFS from Node 0
        dfsBridges(adj, visited, tin, low, bridges, 0, -1);

        return bridges;
    }

    private void dfsBridges(List<List<Integer>> adj, boolean[] visited, 
                            int[] tin, int[] low, List<List<Integer>> bridges, 
                            int u, int parent) {
        visited[u] = true;
        tin[u] = low[u] = timer++;

        for (int v : adj.get(u)) {
            if (v == parent) continue; // Ignore edge leading back to parent node

            if (visited[v]) {
                // Case 1: Back-Edge encountered! Update low[u] using tin[v]
                low[u] = Math.min(low[u], tin[v]);
            } else {
                // Case 2: Tree-Edge! Recurse DFS
                dfsBridges(adj, visited, tin, low, bridges, v, u);
                low[u] = Math.min(low[u], low[v]); // Update low[u] after child returns

                // Step 3: Check Bridge Condition
                if (low[v] > tin[u]) {
                    bridges.add(Arrays.asList(u, v)); // Edge (u, v) is a critical bridge!
                }
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Tarjan's Bridge Check Line
if (low[v] > tin[u]) bridges.add(Arrays.asList(u, v));
```

---

## 7. Concrete Problem Examples
* **LeetCode 1192 - Critical Connections in a Network**: Primary bridge detection problem.
* **Network Infrastructure Survivability**: Identifying single points of failure.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 1192 `criticalConnections`:

```java
public class BridgesDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 1192 Critical Connections Test ===");
        BridgesMaster solver = new BridgesMaster();

        int n = 4;
        List<List<Integer>> connections = Arrays.asList(
            Arrays.asList(0, 1),
            Arrays.asList(1, 2),
            Arrays.asList(2, 0),
            Arrays.asList(1, 3)
        );

        List<List<Integer>> bridges = solver.criticalConnections(n, connections);
        System.out.println("Critical Network Bridges: " + bridges); 
        // Output: [[1, 3]] ✅
    }
}
```

---

## 9. Complexity Analysis

| Low-Link Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Tarjan's Bridges (1192)**| **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Stack Memory**| Single DFS pass with `tin` / `low` |
| **Articulation Points**    | **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Stack Memory**| `low[v] >= tin[u]` condition |

---

## 10. Edge Cases & Boundary Handling
* **Tree Topology (No Cycles)**: Every single edge in a tree graph is a bridge (`low[v] > tin[u]` holds for all $V-1$ edges).
* **Graph Full of Cycles**: No bridges exist (`bridges` returns empty `[]`).

---

## 11. Common Mistakes & Anti-Patterns
* **Using `low[v]` Instead of `tin[v]` When Processing Back-Edges**:
  - Writing `low[u] = Math.min(low[u], low[v])` for an already-visited back-edge node $v$ propagates stale lowest times incorrectly across multiple back-edges.
  - **ALWAYS use `tin[v]` for back-edges (`low[u] = Math.min(low[u], tin[v])`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Tarjan's Back-Edge Update Rule vs Tree-Edge Update Rule:
> * For a **Tree-Edge** (unvisited neighbor $v$): Recurse DFS, then **`low[u] = Math.min(low[u], low[v])`**.
> * For a **Back-Edge** (already-visited neighbor $v \ne \text{parent}$): **`low[u] = Math.min(low[u], tin[v])`**.
> Distinguishing between `low[v]` for tree edges and `tin[v]` for back-edges is the most critical implementation detail of Tarjan's algorithm! ⚡

> **Memory Trick:** **"Tree-Edge uses low[v]! Back-Edge uses tin[v]! Bridge if low[v] > tin[u]!"**

---

## 13. System & Implementation Comparisons

| Feature | Tarjan's Low-Link DFS Algorithm | Naive Edge-Removal BFS |
| :--- | :--- | :--- |
| **Time Complexity** | **$O(V + E)$ Strict Linear ⚡**| $O(E \cdot (V + E))$ Quadratic ❌ |
| **Pass Count** | **1 Single DFS Pass ⚡** | $E$ Separate BFS Scans |
| **Code Mechanism** | `tin[]` / `low[]` Timestamps | Edge removal and connectivity tests |

---

## 14. How to Recognize This in Questions
* **"Find all critical connections / edges whose removal disconnects the network"** $\rightarrow$ LeetCode 1192 (Tarjan's Bridges).

---

## 15. Frequently Asked Interview Questions
* **Q: What is the mathematical condition for an edge $(u, v)$ to be a bridge?**  
  *A:* $\text{low}[v] > \text{tin}[u]$.
* **Q: Why does a root vertex require $\ge 2$ DFS tree children to be an Articulation Point?**  
  *A:* Because if a root vertex has only 1 DFS tree child, removing the root leaves the child's subtree connected as a single component.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: TARJAN'S BRIDGES (LEETCODE 1192)                      |
+-----------------------------------------------------------------------+
| • Timestamps     : tin[u] = discovery time, low[u] = lowest reachable time|
| • Tree-Edge Rule : low[u] = Math.min(low[u], low[v]);                 |
| • Back-Edge Rule : low[u] = Math.min(low[u], tin[v]);                 |
| • Bridge Check   : if (low[v] > tin[u]) -> Edge (u, v) IS A BRIDGE! ⚡ |
| • Performance    : O(V + E) Linear Time | 1 Single DFS Pass! ⚡         |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 1192 (`Critical Connections in a Network`) in Java.
- [ ] I can state the mathematical condition for bridges (`low[v] > tin[u]`).
- [ ] I know when to use `low[v]` vs `tin[v]`.
- [ ] I can state the condition for Articulation Points (`low[v] >= tin[u]`).
- [ ] I can trace Tarjan's low-link timestamps step by step.
