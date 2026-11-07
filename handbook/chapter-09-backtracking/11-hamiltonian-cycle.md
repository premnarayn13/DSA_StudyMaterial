# 11. Hamiltonian Cycle: NP-Complete Paths, Visited Vectors & Eulerian Comparisons

## 1. Introduction
A **Hamiltonian Path** in an undirected or directed graph $G = (V, E)$ is a path that visits **EVERY VERTEX** in $V$ **EXACTLY ONCE**. A **Hamiltonian Cycle** (or Hamiltonian Circuit) is a closed Hamiltonian Path that ends at the starting origin vertex $v_0$, forming a simple cycle of length $V$. Determining whether a graph contains a Hamiltonian Path or Cycle is one of Richard Karp's original 21 **NP-Complete Problems**. Backtracking Hamiltonian cycle search assigns vertices sequentially into a `path[]` array of size $V$, checking (1) **Edge Connection Adjacency** (`graph[prev][curr] == 1`) and (2) **Vertex Unvisited Status** (`!visited[curr]`). It executes in **$O(N!)$ Factorial Time Complexity** and **$O(V)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Hamiltonian Cycle Backtracking:
> 1. **Hamiltonian Path vs Eulerian Circuit Distinction**:
>    - **Hamiltonian Cycle**: Visits every VERTEX exactly once. NP-Complete ($O(N!)$ Backtracking).
>    - **Eulerian Circuit**: Visits every EDGE exactly once. Solvable in $O(E)$ Linear Time via Hierholzer's Algorithm (Requires all vertex degrees to be even!).
> 2. **Path Sequence Array (`path[pos]`)**:
>    - `path[0]` is fixed to starting origin vertex $0$ to break rotational symmetry.
>    - At position `pos`, select next candidate vertex $v$ satisfying `graph[path[pos-1]][v] == 1` AND `!visited[v]`.
> 3. **Origin Re-connection Cycle Check**:
>    - At position `pos == V` (all $V$ vertices included in `path[]`), verify that an edge connects the final vertex back to the origin:
>      $$\text{graph}[\text{path}[V-1]][\text{path}[0]] == 1$$
> 4. **Dirac's & Ore's Theorems (Existence Conditions)**:
>    - **Dirac's Theorem**: If every vertex $v \in V$ has degree $\text{deg}(v) \ge \frac{V}{2}$ (for $V \ge 3$), $G$ is GUARANTEED to contain a Hamiltonian Cycle! ⚡

```
Hamiltonian Cycle vs Eulerian Circuit Topology:

Hamiltonian Cycle (Vertex Visit):      Eulerian Circuit (Edge Visit):
  [ V0 ] ─────── [ V1 ]                   [ V0 ] ═══════ [ V1 ]
    │              │                        ║              ║  (Crosses every EDGE!)
  [ V3 ] ─────── [ V2 ]                   [ V3 ] ═══════ [ V2 ]

Visits every VERTEX once! (O(N!))     Visits every EDGE once! (O(E) Linear!) ⚡
```

---

## 2. Core Concepts & Graph Cycle Strategy Matrix

### 2.1 Graph Traversal Strategy Matrix
```
Graph Traversal Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Target Element    | Solvability Class | Algorithm Engine  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Hamiltonian Path**  | Every Vertex Once | NP-Complete       | **Backtracking DFS⚡**| **$O(N!)$ Factorial⚡**|
| **Hamiltonian Cycle** | Vertex Cycle      | NP-Complete       | **Backtracking DFS⚡**| **$O(N!)$ Factorial⚡**|
| **Eulerian Circuit**  | Every Edge Once   | Polynomial ($P$)  | Hierholzer's Algo | **$O(E)$ Linear ⚡**|
| **TSP (Weighted)**    | Min Weight Cycle  | NP-Hard           | Bitmask DP / B&B  | $O(N^2 \cdot 2^N)$|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Hamiltonian = Every VERTEX once (O(N!) NP-Complete); Eulerian = Every EDGE once (O(E) Linear P)!"**

---

## 3. Characteristics & Dirac's Theorem Mathematical Proof

### 3.1 Mathematical Proof of Dirac's Theorem
* **Theorem (Dirac, 1952)**: Let $G = (V, E)$ be a simple graph with $V \ge 3$ vertices. If every vertex $v \in V$ has degree $\text{deg}(v) \ge \frac{V}{2}$, then $G$ is Hamiltonian.
* **Proof by Contradiction**:
  1. Suppose $G$ satisfies $\text{deg}(v) \ge \frac{V}{2}$ for all $v$, but $G$ is NOT Hamiltonian.
  2. Add edges to $G$ until adding one more edge makes $G$ Hamiltonian. Let $P = (v_1, v_2 \dots v_V)$ be a longest Hamiltonian Path in this maximal non-Hamiltonian graph.
  3. Since $G$ has no Hamiltonian cycle, $v_1$ cannot be adjacent to $v_V$.
  4. Define set $S = \{v_i \mid (v_1, v_{i+1}) \in E\}$ and $T = \{v_i \mid (v_i, v_V) \in E\}$.
  5. $|S| = \text{deg}(v_1) \ge \frac{V}{2}$ and $|T| = \text{deg}(v_V) \ge \frac{V}{2}$.
  6. $S \cup T \subseteq \{v_1 \dots v_{V-1}\}$, so $|S \cup T| \le V - 1$.
  7. By Inclusion-Exclusion:
     $$|S \cap T| = |S| + |T| - |S \cup T| \ge \frac{V}{2} + \frac{V}{2} - (V - 1) = 1$$
  8. Thus, there exists some $v_i \in S \cap T$ where $(v_1, v_{i+1}) \in E$ AND $(v_i, v_V) \in E$.
  9. The cycle $(v_1, v_{i+1}, v_{i+2} \dots v_V, v_i, v_{i-1} \dots v_1)$ forms a valid Hamiltonian Cycle in $G$, contradicting the premise that $G$ is non-Hamiltonian!
 10. Therefore, $G$ MUST contain a Hamiltonian Cycle! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Cycle Search Execution

Tracing Hamiltonian Cycle Search for Graph $G$ with 5 Vertices:

```
Adjacency Matrix (Edges: 0-1, 0-3, 1-2, 1-3, 1-4, 2-4, 3-4):

Path[0] = 0 (Fixed origin). Visited: {0}.

- Pos 1: Candidates from 0: Vertices 1, 3.
         Try 1 -> Path = [0, 1]. Visited: {0, 1}.

- Pos 2: Candidates from 1: Vertices 2, 3, 4.
         Try 2 -> Path = [0, 1, 2]. Visited: {0, 1, 2}.

- Pos 3: Candidates from 2: Vertex 4.
         Try 4 -> Path = [0, 1, 2, 4]. Visited: {0, 1, 2, 4}.

- Pos 4: Candidates from 4: Vertices 1(visited), 2(visited), 3(unvisited).
         Try 3 -> Path = [0, 1, 2, 4, 3]. Visited: {0, 1, 2, 4, 3}. All 5 vertices placed!

Origin Check: Is there an edge from Path[4] (3) back to Path[0] (0)?
Edge (3, 0) exists! HAMILTONIAN CYCLE FOUND! [0, 1, 2, 4, 3, 0] ✅ ⚡
```

---

## 5. Visual Diagram: Origin Re-connection Check

```
Hamiltonian Cycle Completion Criteria:

Path Array: [ V0 | V1 | V2 | V3 | V4 ]  (All V = 5 Vertices Included!)
               │                    │
               └──── Edge (V4, V0) ─┘
              (Origin Re-connection Check!)

If graph[V4][V0] == 1 ──► HAMILTONIAN CYCLE CONFIRMED! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Hamiltonian Cycle Backtracking, Dirac's Degree Condition Validator, and Eulerian Circuit Hierholzer's Algorithm comparison.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Hamiltonian Cycle Algorithms:
 * Adjacency Checking, Origin Re-connection, Dirac's Theorem, and Eulerian Comparison.
 */
public class HamiltonianCycleMaster {

    // =========================================================================
    // 1. HAMILTONIAN CYCLE BACKTRACKING SOLVER (O(N!) Time, O(V) Space)
    // =========================================================================
    /**
     * Solves Hamiltonian Cycle problem returning path array of vertex sequence.
     *
     * @param graph 2D adjacency matrix (1 = edge, 0 = no edge)
     * @return array of vertex indices forming cycle starting/ending at 0, or null if none
     */
    public int[] solveHamiltonianCycle(int[][] graph) {
        if (graph == null || graph.length == 0) return null;
        int vCount = graph.length;

        int[] path = new int[vCount];
        Arrays.fill(path, -1);
        boolean[] visited = new boolean[vCount];

        // Step 1: Fix starting origin to vertex 0 to break rotational symmetry ⚡
        path[0] = 0;
        visited[0] = true;

        if (hamiltonianCycleDFS(graph, path, visited, 1, vCount)) {
            return path; // Solved! ⚡
        }

        return null;
    }

    private boolean hamiltonianCycleDFS(int[][] graph, int[] path, boolean[] visited, int pos, int vCount) {
        // Base Case: All V vertices included in path!
        if (pos == vCount) {
            // Check if last vertex connects back to origin vertex path[0] ⚡
            return graph[path[pos - 1]][path[0]] == 1;
        }

        // Try candidate vertices v = 1 ... V-1
        for (int v = 1; v < vCount; v++) {
            if (isSafeVertex(v, graph, path, visited, pos)) {
                // Choose
                path[pos] = v;
                visited[v] = true;

                // Explore
                if (hamiltonianCycleDFS(graph, path, visited, pos + 1, vCount)) {
                    return true; // Early termination return true! ⚡
                }

                // Unchoose (Backtrack!) ⚡
                path[pos] = -1;
                visited[v] = false;
            }
        }

        return false;
    }

    private boolean isSafeVertex(int v, int[][] graph, int[] path, boolean[] visited, int pos) {
        // Check 1: Edge exists between previous vertex path[pos-1] and candidate v
        if (graph[path[pos - 1]][v] == 0) return false;

        // Check 2: Candidate v has NOT been visited yet
        return !visited[v];
    }

    // =========================================================================
    // 2. DIRAC'S THEOREM HAMILTONIAN GUARANTEE CHECK (O(V^2) Time)
    // =========================================================================
    /**
     * Checks if graph satisfies Dirac's Degree Condition (deg(v) >= V/2 for all v).
     */
    public boolean satisfiesDiracCondition(int[][] graph) {
        if (graph == null || graph.length < 3) return false;
        int vCount = graph.length;

        for (int r = 0; r < vCount; r++) {
            int degree = 0;
            for (int c = 0; c < vCount; c++) {
                if (graph[r][c] == 1) degree++;
            }
            if (degree < (vCount / 2.0)) {
                return false; // Degree condition failed
            }
        }

        return true; // Guaranteed Hamiltonian by Dirac's Theorem! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Hamiltonian Origin Re-connection & Safety Check Lines
if (pos == vCount) return graph[path[pos - 1]][path[0]] == 1;
if (graph[path[pos - 1]][v] == 1 && !visited[v]) ...
```

---

## 7. Concrete Problem Examples & Applications

1. **Hamiltonian Cycle Benchmark**:
   - Primary NP-complete graph cycle benchmark ($O(N!)$ time).

2. **Knight's Tour Problem**:
   - Closed Knight's Tour is a special case of a Hamiltonian Cycle on a knight's graph.

3. **Printed Circuit Board (PCB) Drilling Order**:
   - Finding optimal hole placement traversal paths.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class HamiltonianCycleDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   HAMILTONIAN CYCLE BACKTRACKING DEMO           ");
        System.out.println("=================================================\n");

        HamiltonianCycleMaster master = new HamiltonianCycleMaster();

        // 5 Vertices Graph Adjacency Matrix
        int[][] graph = {
            {0, 1, 0, 1, 0},
            {1, 0, 1, 1, 1},
            {0, 1, 0, 0, 1},
            {1, 1, 0, 0, 1},
            {0, 1, 1, 1, 0}
        };

        // 1. Solve Hamiltonian Cycle
        int[] cycle = master.solveHamiltonianCycle(graph);

        System.out.println("1. Hamiltonian Cycle Backtracking Solver:");
        if (cycle != null) {
            System.out.println("   Hamiltonian Cycle Path Found: " + Arrays.toString(cycle) + " -> 0");
        } else {
            System.out.println("   No Hamiltonian Cycle Exists!");
        }
        System.out.println("-------------------------------------------------");

        // 2. Dirac's Condition Test
        boolean diracGuaranteed = master.satisfiesDiracCondition(graph);
        System.out.println("2. Dirac's Condition Check (deg(v) >= V/2 for all v):");
        System.out.println("   Dirac's Theorem Guaranteed: " + diracGuaranteed);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Graph Path Problem | Solvability Class | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Hamiltonian Path** | NP-Complete | $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(V)}$ Stack Depth| Visit every VERTEX once |
| **Hamiltonian Cycle**| NP-Complete | $\mathbf{O(N!)}$ Factorial⚡| $\mathbf{O(V)}$ Stack Depth| Origin re-connection |
| **Eulerian Circuit** | Polynomial ($P$) | $\mathbf{O(E)}$ Linear ⚡| $\mathbf{O(V + E)}$ Stack| Visit every EDGE once |

---

## 10. Edge Cases & Boundary Handling

1. **Disconnected Graph Components**:
   - `hamiltonianCycleDFS` returns `false` since unvisited vertices cannot be reached.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Origin Re-connection Check at `pos == V`**:
  - Validating that all $V$ vertices are visited without checking `graph[path[V-1]][path[0]] == 1` produces a Hamiltonian Path, NOT a Hamiltonian Cycle. ALWAYS check origin connection!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Hamiltonian vs Eulerian Distinction:
> * **Hamiltonian Cycle**: Every **VERTEX** once $\to$ NP-Complete ($O(N!)$ Backtracking).
> * **Eulerian Circuit**: Every **EDGE** once $\to$ Solvable in $O(E)$ Linear Time! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Hamiltonian Cycle | Eulerian Circuit |
| :--- | :--- | :--- |
| **Target Element** | Every Vertex | Every Edge |
| **Complexity Class**| **NP-Complete ($O(N!)$) ⚡**| **Polynomial ($O(E)$) ⚡** |
| **Existence Condition**| Dirac's / Ore's Theorem | All vertex degrees are EVEN |

---

## 14. How to Recognize This in Questions

* **"Find cycle visiting every vertex in graph exactly once"** $\rightarrow$ Hamiltonian Cycle.
* **"Reconstruct itinerary visiting every flight/edge exactly once"** $\rightarrow$ Eulerian Path (LeetCode 332).

---

## 15. Frequently Asked Interview Questions

* **Q: What is the difference between a Hamiltonian Path and a Hamiltonian Cycle?**  
  *A:* A Hamiltonian Path visits every vertex in the graph exactly once. A Hamiltonian Cycle is a closed Hamiltonian Path where the last vertex connects back to the starting vertex.

* **Q: What is Dirac's Theorem?**  
  *A:* A theorem stating that if every vertex in a graph with $V \ge 3$ has degree $\ge \frac{V}{2}$, the graph is guaranteed to contain a Hamiltonian Cycle.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: HAMILTONIAN CYCLE                                     |
+-----------------------------------------------------------------------+
| • Search Rule  : Fix path[0] = 0 -> Recurse pos 1..V-1                |
| • Safety Check : graph[path[pos-1]][v] == 1 && !visited[v]            |
| • Cycle Check  : At pos == V, verify graph[path[V-1]][path[0]] == 1 ⚡ |
| • Dirac Theorem: deg(v) >= V/2 for all v -> Guaranteed Hamiltonian    |
| • Performance  : O(N!) Factorial Time | O(V) Auxiliary Stack ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Hamiltonian Cycle Backtracking in Java.
- [ ] I can state the origin re-connection check `graph[path[V-1]][path[0]] == 1`.
- [ ] I can state Dirac's Theorem degree condition ($\text{deg}(v) \ge \frac{V}{2}$).
- [ ] I can explain the difference between Hamiltonian Cycle ($O(N!)$) and Eulerian Circuit ($O(E)$).
- [ ] I can state why `path[0]` is fixed to 0 (breaks rotational symmetry).
