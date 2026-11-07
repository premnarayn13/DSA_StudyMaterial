# 07. Bipartite Graph Verification, 2-Coloring Mechanics & Odd-Cycle Invariants

## 1. Introduction
A **Bipartite Graph** is a graph whose vertices can be partitioned into two independent disjoint sets $U$ and $V$ such that **EVERY EDGE $(u, v)$ CONNECTS A VERTEX IN $U$ TO A VERTEX IN $V$** (no edge exists between two vertices in the same set!). Determining **Is Graph Bipartite? (LeetCode 785)** is equivalent to solving the **2-Coloring Problem**: color every vertex using two colors (e.g. Color `1` and Color `-1`) such that no two adjacent vertices share the same color. This check executes via **2-Coloring BFS or DFS** in **$O(V + E)$ Linear Time**.

> **Important:** The Odd-Length Cycle Theorem of Bipartite Graphs:
> 1. **Odd-Cycle Invariant Theorem**: A graph is Bipartite IF AND ONLY IF it contains **NO ODD-LENGTH CYCLES**! (Even-length cycles are fully 2-colorable).
> 2. **2-Color State Assignment**:
>    - `color[i] = 0`: Uncolored / Unvisited.
>    - `color[i] = 1`: Color Red.
>    - `color[i] = -1`: Color Blue.
> 3. **Color Conflict Rule**: If an edge $(u, v)$ connects to a neighbor $v$ already colored with the SAME color (`color[v] == color[u]`), a **COLOR CONFLICT** occurs! The graph is NOT Bipartite! ⚡

```
2-Coloring Bipartite Graph Topology (Colors: 1 [Red] vs -1 [Blue]):
Set U (Color 1 - Red):               Set V (Color -1 - Blue):
      (0) [Color 1]   --------------->   (1) [Color -1]
       |                                      |
       v                                      v
      (2) [Color 1]   --------------->   (3) [Color -1]

All edges connect Color 1 to Color -1! Valid 2-Colorable Bipartite Graph! ⚡
```

---

## 2. Core Concepts & 2-Coloring BFS vs DFS Architecture

### 2.1 Bipartite Verification Strategy Matrix
```
Bipartite Verification Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| 2-Coloring Variant    | Target Color      | Conflict Rule     | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **2-Coloring BFS**    | `color[v] = -color[u]`| `color[v] == color[u]`| **$O(V + E)$ Linear ⚡**|
| **2-Coloring DFS**    | `color[v] = -color[u]`| `color[v] == color[u]`| **$O(V + E)$ Linear ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Is Bipartite: Color neighbor with OPPOSITE color (-color[u])! If neighbor has SAME color -> NOT Bipartite!"**

---

## 3. Characteristics & Mathematical Proof of Odd-Length Cycle Invariant

### 3.1 Mathematical Proof of Odd-Length Cycle Invariant
* **Claim**: A graph containing an odd-length cycle of length $2k + 1$ CANNOT be 2-colored.
* **Proof**:
  - Start at vertex $v_0$ with Color 1.
  - Alternating colors along the path gives: $v_1 \to -1, v_2 \to 1, v_3 \to -1, \dots, v_{2k} \to 1$.
  - The closing cycle edge connects $v_{2k}$ (Color 1) back to $v_0$ (Color 1).
  - Both endpoints $v_{2k}$ and $v_0$ have Color 1 $\implies$ **Color Conflict! Cannot be 2-colored!** ⚡

---

## 4. Internal Working Mechanics
Tracing LeetCode 785 (Is Graph Bipartite?) on Graph with Edges `[[1,3], [0,2], [1,3], [0,2]]` (0-1, 0-3, 1-2, 2-3):

```
Graph nodes 0, 1, 2, 3. Init: color = [0, 0, 0, 0].

Outer Loop i = 0 (Uncolored):
1. Color 0 with 1: color[0] = 1. Enqueue 0.
2. Pop 0. Neighbors: 1 and 3.
   - Neighbor 1: color[1] = 0 -> Set color[1] = -color[0] = -1. Enqueue 1.
   - Neighbor 3: color[3] = 0 -> Set color[3] = -color[0] = -1. Enqueue 3.
3. Pop 1. Neighbors: 0 (color 1) and 2.
   - Neighbor 2: color[2] = 0 -> Set color[2] = -color[1] = 1. Enqueue 2.
4. Pop 3. Neighbors: 0 (color 1) and 2 (color 1).
   - Neighbor 2 has color 1 (opposite of color[3] = -1). NO CONFLICT!

All nodes colored without conflict! Returns true (Is Bipartite)! ✅ (O(V + E) Time!)
```

---

## 5. Visual Diagram
2-Coloring Conflict Topography (Odd-Length Cycle 3):

```
                  (0) [Color 1]
                 /   \
        [Color -1] (1)---(2) [Color -1]  <--- CONFLICT! Edge (1, 2) connects Color -1 to Color -1!
                                             Odd Cycle 0-1-2 -> NOT BIPARTITE! ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of LeetCode 785 (Is Graph Bipartite? using 2-Coloring BFS and DFS):

```java
import java.util.*;

// LeetCode 785: Is Graph Bipartite? (2-Coloring Algorithm)
public class BipartiteGraphMaster {

    // 1. 2-Coloring BFS Algorithm (LeetCode 785 Primary Solution) O(V + E) Time
    public boolean isBipartiteBFS(int[][] graph) {
        if (graph == null || graph.length == 0) return true;

        int numVertices = graph.length;
        int[] color = new int[numVertices]; // 0 = Uncolored, 1 = Color A, -1 = Color B

        // Outer loop to handle disconnected graph components
        for (int i = 0; i < numVertices; i++) {
            if (color[i] == 0) { // If uncolored, start 2-coloring BFS
                if (!checkBipartiteBFS(graph, color, i)) {
                    return false; // Color conflict detected! Not Bipartite.
                }
            }
        }

        return true; // Fully 2-colorable! Is Bipartite.
    }

    private boolean checkBipartiteBFS(int[][] graph, int[] color, int startNode) {
        Queue<Integer> queue = new LinkedList<>();

        color[startNode] = 1; // Assign initial Color 1
        queue.offer(startNode);

        while (!queue.isEmpty()) {
            int u = queue.poll();

            for (int v : graph[u]) {
                if (color[v] == 0) {
                    // Assign OPPOSITE color to neighbor
                    color[v] = -color[u];
                    queue.offer(v);
                } else if (color[v] == color[u]) {
                    return false; // Color conflict! Adjacent nodes have SAME color.
                }
            }
        }

        return true;
    }

    // 2. 2-Coloring DFS Algorithm Alternative O(V + E) Time
    public boolean isBipartiteDFS(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];

        for (int i = 0; i < n; i++) {
            if (color[i] == 0) {
                if (!dfsColor(graph, color, i, 1)) {
                    return false;
                }
            }
        }

        return true;
    }

    private boolean dfsColor(int[][] graph, int[] color, int u, int targetColor) {
        color[u] = targetColor;

        for (int v : graph[u]) {
            if (color[v] == 0) {
                if (!dfsColor(graph, color, v, -targetColor)) {
                    return false; // Conflict deeper in DFS
                }
            } else if (color[v] == color[u]) {
                return false; // Color conflict!
            }
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// 2-Coloring BFS Assignment & Conflict Line
if (color[v] == 0) { color[v] = -color[u]; queue.offer(v); }
else if (color[v] == color[u]) return false; // Conflict!
```

---

## 7. Concrete Problem Examples
* **LeetCode 785 - Is Graph Bipartite?**: Primary problem.
* **LeetCode 886 - Possible Bipartition**: Grouping people into 2 disjoint groups without dislikes.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 785 `isBipartiteBFS`:

```java
public class BipartiteGraphDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 785 Is Graph Bipartite Test ===");
        BipartiteGraphMaster solver = new BipartiteGraphMaster();

        int[][] graph1 = {{1,3}, {0,2}, {1,3}, {0,2}}; // Valid Bipartite Graph
        System.out.println("Is graph1 Bipartite? " + solver.isBipartiteBFS(graph1)); // Output: true

        int[][] graph2 = {{1,2,3}, {0,2}, {0,1,3}, {0,2}}; // Odd Cycle (0-1-2)
        System.out.println("Is graph2 Bipartite? " + solver.isBipartiteBFS(graph2)); // Output: false ✅
    }
}
```

---

## 9. Complexity Analysis

| Bipartite Verification | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **2-Coloring BFS** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Color Array & Queue**| Color assignment `color[v] = -color[u]` |
| **2-Coloring DFS** | **$O(V + E)$ Linear ⚡** | **$O(V)$ Color Array & Stack**| Recursive opposite color assignment |

---

## 10. Edge Cases & Boundary Handling
* **Disconnected Graphs**: Handled safely by outer loop `for (int i = 0; i < V; i++)`.
* **Graph with No Edges ($E = 0$)**: Trivially 2-colorable, returning `true`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting Outer Loop for Disconnected Components**:
  - Running 2-coloring from node 0 only evaluates 1 component, returning `true` for a graph with an odd cycle in component 2!
  - **ALWAYS loop through all vertices $0 \dots V-1$ to check all disconnected components**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Bipartite Graph Real-World Utility:
> Bipartite Graphs model two-sided matching markets (e.g. Job Applicants to Job Openings, Users to Advertisements, Drivers to Riders).
> Testing if a graph is Bipartite confirms whether items can be strictly split into 2 non-conflicting categories! ⚡

> **Memory Trick:** **"Bipartite = No Odd Cycles = 2-Colorable with colors 1 and -1!"**

---

## 13. System & Implementation Comparisons

| Feature | 2-Coloring BFS | 2-Coloring DFS |
| :--- | :--- | :--- |
| **Data Structure** | FIFO Queue | Call Stack Recursion |
| **Conflict Signal** | `color[v] == color[u]` | `color[v] == color[u]` |
| **Time Complexity** | **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Linear ⚡** |

---

## 14. How to Recognize This in Questions
* **"Split graph nodes into 2 groups such that no two adjacent nodes are in the same group"** $\rightarrow$ Bipartite Verification (LeetCode 785).

---

## 15. Frequently Asked Interview Questions
* **Q: What graph property makes a graph non-bipartite?**  
  *A:* The presence of at least one odd-length cycle.
* **Q: Why are colors represented as 1 and -1 in 2-coloring?**  
  *A:* Because negating `-color[u]` flips between Color 1 and Color -1 in a single arithmetic operation!

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: BIPARTITE GRAPH VERIFICATION                          |
+-----------------------------------------------------------------------+
| • Definition   : Vertices split into 2 sets; all edges cross between sets|
| • Odd Cycles   : Bipartite IF AND ONLY IF graph has NO odd cycles!    |
| • Color Values : 0 = Uncolored, 1 = Color A, -1 = Color B             |
| • Color Rule   : Set color[v] = -color[u]; if (color[v] == color[u]) false|
| • Time Bounds  : O(V + E) Linear Time | O(V) Color Array Memory ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 785 (`Is Graph Bipartite?`) using BFS in Java.
- [ ] I can write 2-coloring DFS verification.
- [ ] I know why odd-length cycles destroy bipartiteness.
- [ ] I can explain why `-color[u]` flips between colors 1 and -1.
- [ ] I can trace 2-coloring step by step.
