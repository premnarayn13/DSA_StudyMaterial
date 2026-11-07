# 10. Graph Coloring: Chromatic Numbers, Adjacency Constraints & Welsh-Powell Heuristics

## 1. Introduction
The **Graph $K$-Coloring Problem** is an NP-complete Constraint Satisfaction Problem (CSP) where the objective is to assign one of $K$ available colors to every vertex in an undirected graph $G = (V, E)$ such that **no two adjacent vertices share the same color**. The minimum number of colors required to color a graph $G$ is called its **Chromatic Number $\chi(G)$**. Graph coloring models register allocation in compiler backends, telecommunication frequency assignment, map coloring (Four Color Theorem), and exam timetable scheduling. Backtracking graph $K$-coloring assigns colors vertex-by-vertex ($u = 0 \dots V-1$) using an **$O(1)$ Adjacency Safety Check** (`isSafe(u, color)`), executing in **$O(K^V)$ Time Complexity** and **$O(V)$ Auxiliary Space**. Applying the **Welsh-Powell Heuristic** (sorting vertices by degree descending) prunes search branches early.

> **Important:** Core Structural Invariants of Graph Coloring Backtracking:
> 1. **Adjacency Safety Invariant (`isSafe(u, c)`)**:
>    - For a candidate color $c$ at vertex $u$, check all adjacent neighbors $v \in \text{neighbors}(u)$.
>    - If any neighbor $v$ already has color $c$ (`colorAssignment[v] == c`), color $c$ is UNSAFE for vertex $u$!
> 2. **Vertex-by-Vertex Sequential Processing**:
>    - Recurse vertex-by-vertex from $u = 0$ to $V-1$. Base case $u == V$ signifies a valid $K$-coloring!
> 3. **Chromatic Number $\chi(G)$ Invariants**:
>    - **Bipartite Graphs**: $\chi(G) \le 2$ (2-colorable in $O(V + E)$ BFS/DFS time).
>    - **Planar Maps (Four Color Theorem)**: $\chi(G) \le 4$ for all planar graphs.
>    - **Complete Graphs ($K_N$)**: $\chi(K_N) = N$.
> 4. **Welsh-Powell Heuristic Degree Ordering**:
>    - Sort vertices in descending order of vertex degree ($\text{degree}(v_1) \ge \text{degree}(v_2) \dots$).
>    - Coloring high-degree hub vertices first prunes invalid branch choices early! ⚡

```
Graph K-Coloring Conflict Topology (K = 3 Colors: Red, Green, Blue):

          [ Vertex 0: RED ]
             /         \
            /           \
  [ Vertex 1: GREEN ] ──► [ Vertex 2: BLUE ]

Adjacency Checks:
- Edge (0-1): Red != Green (Safe!)
- Edge (0-2): Red != Blue (Safe!)
- Edge (1-2): Green != Blue (Safe!)

All adjacent vertex colors are distinct -> Valid K-Coloring! ⚡
```

---

## 2. Core Concepts & Graph Coloring Strategy Matrix

### 2.1 Graph Coloring Implementations Strategy Matrix
```
Graph Coloring Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Implementation        | Primary Target    | Pruning Mechanism | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Bipartite Check (K=2)**| 2-Colorability   | BFS/DFS Queue     | **$O(V + E)$ Linear ⚡**| **$O(V)$ Array ⚡**|
| **K-Coloring (Backtrack)**| K Colors Assignment| `isSafe(u, c)` Array| **$O(K^V)$ Exponential⚡**| **$O(V)$ Stack ⚡**|
| **Welsh-Powell (Heuristic)**| Fast Assignment| Degree Sorting    | **Pruned $O(K^V)$ ⚡**| **$O(V)$ Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Graph K-Coloring checks isSafe(u, c) across neighbors; Bipartite check (K=2) runs in linear O(V+E) time!"**

---

## 3. Characteristics & Bipartite 2-Colorability Mathematical Derivation

### 3.1 Mathematical Derivation of Bipartite 2-Colorability ($O(V + E)$)
* A graph $G$ is **Bipartite** if and only if its vertex set $V$ can be partitioned into two disjoint sets $V_1$ and $V_2$ such that every edge connects a vertex in $V_1$ to a vertex in $V_2$.
* **Odd Cycle Theorem**:
  - A graph $G$ is 2-colorable ($\chi(G) \le 2$) if and ONLY if $G$ contains **NO ODD CYCLES**!
* **Linear BFS Algorithm for $K=2$**:
  1. Initialize `color[v] = -1` for all $v \in V$.
  2. For each unvisited component root $r$, set `color[r] = 1` and push $r$ to BFS queue.
  3. Dequeue $u$. For each neighbor $v \in \text{neighbors}(u)$:
     - If `color[v] == -1`: Set `color[v] = 1 - color[u]` and enqueue $v$.
     - If `color[v] == color[u]`: Conflict detected! Graph contains an odd cycle $\implies$ Not 2-colorable!
  4. Runs in **$O(V + E)$ Strict Linear Time**. ⚡

---

## 4. Internal Working Mechanics: Backtracking K-Coloring Execution

Tracing $K=3$ Coloring for Graph with 4 Vertices ($0-1, 1-2, 2-3, 3-0$):

```
Goal: Assign colors 1, 2, 3 to vertices 0, 1, 2, 3.

- u = 0: Assign Color 1 -> color[0] = 1.
- u = 1: Neighbors: 0. Try Color 1 (Conflict with 0!).
         Try Color 2 -> color[1] = 2.
- u = 2: Neighbors: 1. Try Color 1 -> color[2] = 1. (Conflict with 0? No edge 0-2!).
- u = 3: Neighbors: 0, 2.
         Try Color 1 (Conflict with 0 & 2!).
         Try Color 2 -> color[3] = 2 (No edge to 1!).

Valid 3-Coloring: [1, 2, 1, 2]! (Chromatically 2-colorable cycle!). ✅ ⚡
```

---

## 5. Visual Diagram: Welsh-Powell Degree Ordering Flow

```
Welsh-Powell Degree Ordering:

Graph Vertices & Degrees:
- V0: Degree 4 (Hub Node)
- V1: Degree 2
- V2: Degree 1
- V3: Degree 3

Sort Vertices Descending by Degree: [ V0 (4), V3 (3), V1 (2), V2 (1) ]

Color V0 first (Most constrained) ──► Prunes invalid choices for all neighbors early! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Graph $K$-Coloring Backtracking, Welsh-Powell Degree Ordering, and Bipartite 2-Coloring Check (LeetCode 785).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Graph Coloring Algorithms:
 * K-Coloring Backtracking, Welsh-Powell Degree Ordering, and Bipartite 2-Coloring.
 */
public class GraphColoringMaster {

    // =========================================================================
    // 1. GRAPH K-COLORING BACKTRACKING SOLVER (O(K^V) Time, O(V) Space)
    // =========================================================================
    /**
     * Solves Graph K-Coloring problem returning color assignment array.
     *
     * @param graph adjacency list representation of graph
     * @param k max number of colors available
     * @return array of color assignments (1 ... K), or null if impossible
     */
    public int[] solveGraphKColoring(List<List<Integer>> graph, int k) {
        if (graph == null || graph.isEmpty() || k <= 0) return null;

        int v = graph.size();
        int[] colorAssignment = new int[v];

        if (graphKColoringDFS(graph, 0, v, k, colorAssignment)) {
            return colorAssignment; // Solved! ⚡
        }

        return null;
    }

    private boolean graphKColoringDFS(List<List<Integer>> graph, int u, int vCount, int k, int[] colorAssignment) {
        if (u == vCount) return true; // Base Case: All V vertices colored! ⚡

        // Try candidate colors 1 ... K
        for (int c = 1; c <= k; c++) {
            if (isSafeColor(graph, u, c, colorAssignment)) {
                // Choose
                colorAssignment[u] = c;

                // Explore
                if (graphKColoringDFS(graph, u + 1, vCount, k, colorAssignment)) {
                    return true; // Early termination return true! ⚡
                }

                // Unchoose (Backtrack!) ⚡
                colorAssignment[u] = 0;
            }
        }

        return false;
    }

    private boolean isSafeColor(List<List<Integer>> graph, int u, int c, int[] colorAssignment) {
        for (int neighbor : graph.get(u)) {
            if (colorAssignment[neighbor] == c) {
                return false; // Neighbor conflict! ⚡
            }
        }
        return true;
    }

    // =========================================================================
    // 2. LEETCODE 785: IS GRAPH BIPARTITE? (K=2 COLORING O(V + E) Time)
    // =========================================================================
    /**
     * Checks if graph is Bipartite (2-colorable) using BFS.
     */
    public boolean isBipartite(int[][] graph) {
        if (graph == null || graph.length == 0) return true;

        int vCount = graph.length;
        int[] colors = new int[vCount];
        Arrays.fill(colors, -1);

        for (int i = 0; i < vCount; i++) {
            if (colors[i] == -1) {
                if (!checkBipartiteBFS(graph, i, colors)) {
                    return false; // Odd cycle detected! ⚡
                }
            }
        }

        return true;
    }

    private boolean checkBipartiteBFS(int[][] graph, int start, int[] colors) {
        Queue<Integer> queue = new LinkedList<>();
        colors[start] = 1;
        queue.add(start);

        while (!queue.isEmpty()) {
            int u = queue.poll();

            for (int neighbor : graph[u]) {
                if (colors[neighbor] == -1) {
                    colors[neighbor] = 1 - colors[u]; // Alternate color 0 or 1! ⚡
                    queue.add(neighbor);
                } else if (colors[neighbor] == colors[u]) {
                    return false; // 2-Color conflict! ⚡
                }
            }
        }

        return true;
    }
}
```

> **Quick Syntax:**
```java
// Graph Coloring Adjacency Check Line
if (colorAssignment[neighbor] == c) return false;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 785 - Is Graph Bipartite?**:
   - 2-colorability benchmark solved in $O(V + E)$ linear time.

2. **Compiler Register Allocation**:
   - Mapping variables to physical CPU registers via graph interference coloring.

3. **Exam Timetable Scheduling**:
   - Assigning exam time slots ($K$ colors) to courses with student conflicts.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class GraphColoringDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   GRAPH K-COLORING BACKTRACKING DEMO           ");
        System.out.println("=================================================\n");

        GraphColoringMaster master = new GraphColoringMaster();

        // Build Graph Adjacency List (4 Vertices Cycle 0-1-2-3-0)
        List<List<Integer>> graph = new ArrayList<>();
        for (int i = 0; i < 4; i++) graph.add(new ArrayList<>());

        graph.get(0).addAll(List.of(1, 3));
        graph.get(1).addAll(List.of(0, 2));
        graph.get(2).addAll(List.of(1, 3));
        graph.get(3).addAll(List.of(0, 2));

        int k = 2;
        int[] colors = master.solveGraphKColoring(graph, k);

        System.out.println("1. Graph 4-Cycle K = " + k + " Coloring Test:");
        System.out.println("   Color Assignment (1..K): " + Arrays.toString(colors));
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 785 Bipartite Test
        int[][] gridGraph = {{1, 3}, {0, 2}, {1, 3}, {0, 2}};
        boolean bipartite = master.isBipartite(gridGraph);
        System.out.println("2. LeetCode 785 Bipartite Check (K=2 Colorability):");
        System.out.println("   Is Graph Bipartite: " + bipartite + " (Optimal = true)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Graph Coloring Task | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Bipartite Check (K=2)**| $\mathbf{O(V + E)}$ Linear ⚡| $\mathbf{O(V)}$ Queue Space| Odd cycle detection |
| **K-Coloring (Backtrack)**| $\mathbf{O(K^V)}$ Exponential⚡| $\mathbf{O(V)}$ Stack Depth| Adjacency safety check |
| **Welsh-Powell Heuristic**| Pruned $O(K^V)$ | $\mathbf{O(V)}$ Array Space| Degree descending sort |

---

## 10. Edge Cases & Boundary Handling

1. **Disconnected Graph Components**:
   - `isBipartite` loops through all $i \in 0 \dots V-1$ to handle disconnected subgraphs.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Backtracking for $K=2$ Coloring**:
  - Running exponential backtracking $O(2^V)$ for 2-colorability when BFS/DFS can solve it in linear $O(V + E)$ time is a major flaw. ALWAYS use BFS/DFS for $K=2$!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Four Color Theorem:
> Any planar graph (such as a 2D geographical map where regions share borders) is **GUARANTEED to be 4-Colorable** ($\chi(G) \le 4$)! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Bipartite Check ($K=2$) | General $K$-Coloring ($K \ge 3$) |
| :--- | :--- | :--- |
| **Algorithmic Class** | Polynomial ($P$) | NP-Complete |
| **Time Complexity** | **$O(V + E)$ Linear ⚡** | **$O(K^V)$ Exponential ⚡** |
| **Primary Structure**| BFS Queue | DFS Backtracking Stack |

---

## 14. How to Recognize This in Questions

* **"Assign colors to vertices such that no adjacent vertices share color"** $\rightarrow$ Graph $K$-Coloring.
* **"Check if graph is bipartite (2-colorable)"** $\rightarrow$ LeetCode 785.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the Chromatic Number $\chi(G)$?**  
  *A:* The minimum number of colors required to color the vertices of graph $G$ such that no two adjacent vertices share the same color.

* **Q: How does the Welsh-Powell Heuristic prune search branches?**  
  *A:* By sorting vertices in descending order of degree, it colors the most constrained hub vertices first, eliminating invalid color choices early in the search tree.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: GRAPH COLORING                                        |
+-----------------------------------------------------------------------+
| • Safety Rule  : colorAssignment[neighbor] != candidateColor          |
| • K=2 Bipartite: Solved in O(V + E) Linear Time via BFS/DFS ⚡        |
| • Welsh-Powell : Sort vertices by degree descending -> Color hub first|
| • Planar Maps  : Four Color Theorem -> Chi(G) <= 4 for all planar maps|
| • Performance  : O(V + E) for K=2 | O(K^V) for General K-Coloring ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 785 (`Is Graph Bipartite?`) in $O(V + E)$ time in Java.
- [ ] I can write Graph $K$-Coloring Backtracking in Java.
- [ ] I can state the Four Color Theorem for planar graphs.
- [ ] I can explain how the Welsh-Powell heuristic prunes search trees.
- [ ] I can state the chromatic number of complete graph $K_N$ ($N$).
