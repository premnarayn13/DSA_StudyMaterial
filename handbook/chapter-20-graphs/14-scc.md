# 14. Strongly Connected Components (SCC): Kosaraju & Tarjan Directed Algorithms

## 1. Introduction
A **Strongly Connected Component (SCC)** in a directed graph $G = (V, E)$ is a maximal subgraph in which **EVERY VERTEX IS REACHABLE FROM EVERY OTHER VERTEX** within the component (path $u \rightsquigarrow v$ and path $v \rightsquigarrow u$ both exist!). Computing SCCs partitions a directed graph into a **Directed Acyclic Graph (DAG) of SCC Components**. Two famous algorithms find all SCCs in **$O(V + E)$ Linear Time**: **Kosaraju's 2-Pass Algorithm** (using graph transposition) and **Tarjan's Single-Pass Stack Algorithm**.

> **Important:** Kosaraju's 2-Pass Algorithm Invariants:
> 1. **Pass 1 (Original Graph DFS)**: Run DFS on original graph $G$, pushing nodes onto a LIFO Stack in order of their **DFS FINISH TIMES**!
> 2. **Graph Transposition ($G^T$)**: Reverse the direction of ALL edges in $G$ to produce transposed graph $G^T$ (if $u \to v$ in $G$, then $v \to u$ in $G^T$).
> 3. **Pass 2 (Transposed Graph DFS)**: Pop nodes from the Stack one by one. If node $u$ is unvisited in $G^T$, launch DFS from $u$ on $G^T$. All nodes reached in this DFS frame form **1 COMPLETE STRONGLY CONNECTED COMPONENT (SCC)**! ⚡

```
Kosaraju's 2-Pass SCC Pipeline Topology:
Original Graph G: (0) ---> (1) ---> (2) ---> (0)   and   (2) ---> (3)
Pass 1 Stack (Finish Order): [3, 2, 1, 0] (Top = 0)

Transposed Graph G^T: (0) <--- (1) <--- (2) <--- (0)   and   (2) <--- (3)
Pass 2 DFS Pops from Top of Stack:
1. Pop 0 -> DFS on G^T reaches {0, 2, 1} --------------> SCC 1 = {0, 1, 2} ⚡
2. Pop 3 -> DFS on G^T reaches {3} --------------------> SCC 2 = {3} ⚡
```

---

## 2. Core Concepts & Kosaraju's vs Tarjan's SCC Algorithms

### 2.1 SCC Algorithm Comparison Matrix
```
Strongly Connected Component Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| SCC Algorithm         | Primary Technique | Pass Count        | Auxiliary Memory  |
+-----------------------+-------------------+-------------------+-------------------+
| **Kosaraju's Algorithm**| Graph Transposition| **2 Passes ⚡**   | $O(V + E)$ Stack/Adj|
| **Tarjan's SCC Algo** | Low-Link Stack    | **1 Pass ⚡**     | $O(V)$ Low-Link   |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Kosaraju's SCC: Pass 1 push finish times to Stack -> Transpose graph -> Pass 2 DFS pops Stack to extract SCCs!"**

---

## 3. Characteristics & Graph Transposition Proof

### 3.1 Mathematical Proof of Kosaraju's Transposition Invariant
* Let $C_1$ and $C_2$ be two distinct SCCs with a directed edge from $C_1 \to C_2$ in $G$.
* In Pass 1 DFS, the highest finish-time node on the Stack will belong to $C_1$ (since $C_1$ can reach $C_2$, but $C_2$ cannot reach back to $C_1$).
* In transposed graph $G^T$, the edge direction is reversed to $C_2 \to C_1$.
* Popping $C_1$'s root from the Stack during Pass 2 DFS on $G^T$ explores ONLY component $C_1$ without bleeding into $C_2$ (since edge $C_1 \to C_2$ is reversed!).
* Thus, **every DFS frame in Pass 2 isolates EXACTLY ONE SCC!** ⚡

---

## 4. Internal Working Mechanics
Tracing Kosaraju's SCC Algorithm on Directed Graph with Edges `(0->1)`, `(1->2)`, `(2->0)`, `(2->3)`:

```
Pass 1: DFS on G (Finish Order Stack):
- DFS(0) -> 1 -> 2 -> 3 (Terminal). Push 3.
- Backtrack to 2. Push 2.
- Backtrack to 1. Push 1.
- Backtrack to 0. Push 0.
Stack (Top to Bottom): [0, 1, 2, 3].

Step 2: Transpose Graph G^T:
- Edges: (1->0), (2->1), (0->2), (3->2).

Pass 2: Pop Stack and run DFS on G^T:
1. Pop 0: unvisited in G^T -> Launch DFS^T(0).
   - Reaches 0, 2, 1. Mark visited.
   - SCC 1 = [0, 2, 1].
2. Pop 1, 2: already visited -> Skip.
3. Pop 3: unvisited in G^T -> Launch DFS^T(3).
   - Reaches 3. Mark visited.
   - SCC 2 = [3].

Extracted 2 SCCs in O(V + E) time! ✅
```

---

## 5. Visual Diagram
Kosaraju's Graph Transposition Topography:

```
Original Graph G:                   Transposed Graph G^T:
   (0) ---> (1)                        (0) <--- (1)
    ^        |                          |        ^
    |        v                          v        |
   (2) <----+                          (2) ----->+
     \                                   ^
      v                                   \
     (3)                                  (3)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java implementation of Kosaraju's 2-Pass Strongly Connected Components Algorithm:

```java
import java.util.*;

public class SCCMaster {

    // Kosaraju's 2-Pass SCC Algorithm O(V + E) Time, O(V + E) Space
    public List<List<Integer>> getStronglyConnectedComponents(int n, List<List<Integer>> adj) {
        Deque<Integer> stack = new ArrayDeque<>();
        boolean[] visited = new boolean[n];

        // Pass 1: Run DFS on original graph G to populate finish-time stack
        for (int i = 0; i < n; i++) {
            if (!visited[i]) {
                dfsFinishTime(adj, visited, stack, i);
            }
        }

        // Step 2: Build Transposed Graph G^T (Reverse all edges)
        List<List<Integer>> transposeAdj = new ArrayList<>();
        for (int i = 0; i < n; i++) transposeAdj.add(new ArrayList<>());

        for (int u = 0; u < n; u++) {
            for (int v : adj.get(u)) {
                transposeAdj.get(v).add(u); // Reverse edge direction u -> v to v -> u
            }
        }

        // Pass 3: Run DFS on transposed graph G^T in stack pop order
        Arrays.fill(visited, false);
        List<List<Integer>> sccs = new ArrayList<>();

        while (!stack.isEmpty()) {
            int u = stack.pop();
            if (!visited[u]) {
                List<Integer> currentSCC = new ArrayList<>();
                dfsCollectSCC(transposeAdj, visited, currentSCC, u);
                sccs.add(currentSCC);
            }
        }

        return sccs;
    }

    // Pass 1 DFS: Push nodes to stack in order of finish times
    private void dfsFinishTime(List<List<Integer>> adj, boolean[] visited, Deque<Integer> stack, int u) {
        visited[u] = true;
        for (int v : adj.get(u)) {
            if (!visited[v]) {
                dfsFinishTime(adj, visited, stack, v);
            }
        }
        stack.push(u); // Push node to stack AFTER all descendants finish!
    }

    // Pass 2 DFS: Collect all nodes in current SCC on transposed graph G^T
    private void dfsCollectSCC(List<List<Integer>> transposeAdj, boolean[] visited, List<Integer> currentSCC, int u) {
        visited[u] = true;
        currentSCC.add(u);
        for (int v : transposeAdj.get(u)) {
            if (!visited[v]) {
                dfsCollectSCC(transposeAdj, visited, currentSCC, v);
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// Kosaraju's Pass 1 Stack Push Line
stack.push(u); // Push to stack in post-order finish time!
```

---

## 7. Concrete Problem Examples
* **Directed Graph Decomposition**: Partitioning web pages or microservices into mutually reachable clusters.
* **2-SAT Problem Resolution**: Solving 2-Satisfiability boolean logic via SCCs.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Kosaraju's `getStronglyConnectedComponents`:

```java
public class SCCDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. Kosaraju's SCC Algorithm Test ===");
        SCCMaster solver = new SCCMaster();

        int n = 5;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        // Edges: 0->1, 1->2, 2->0, 1->3, 3->4
        adj.get(0).add(1);
        adj.get(1).add(2);
        adj.get(2).add(0);
        adj.get(1).add(3);
        adj.get(3).add(4);

        List<List<Integer>> sccs = solver.getStronglyConnectedComponents(n, adj);

        System.out.println("Strongly Connected Components:");
        for (List<Integer> scc : sccs) {
            System.out.println(scc);
        }
        // Output:
        // [0, 2, 1] (SCC 1)
        // [3]       (SCC 2)
        // [4]       (SCC 3) ✅
    }
}
```

---

## 9. Complexity Analysis

| SCC Algorithm | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Kosaraju's 2-Pass**| **$O(V + E)$ Linear ⚡** | **$O(V + E)$ Transpose/Stack**| Pass 1 Stack + Pass 2 Transpose DFS |
| **Tarjan's SCC**     | **$O(V + E)$ Linear ⚡** | **$O(V)$ Low-Link Stack**   | Single pass with low-link values |

---

## 10. Edge Cases & Boundary Handling
* **Directed Acyclic Graph (DAG)**: Every vertex forms a separate 1-element SCC ($V$ total SCCs).
* **Graph Full of Cycles**: Single SCC containing all $V$ vertices.

---

## 11. Common Mistakes & Anti-Patterns
* **Pushing Nodes to Stack BEFORE Recursing Subtrees in Pass 1**:
  - Pushing nodes before subtree completion pushes entry times instead of finish times, ruining component isolation during Pass 2.
  - **ALWAYS push `stack.push(u)` AFTER the recursive loop over neighbors completes**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Kosaraju's Algorithm Is Favored in Coding Rounds:
> Tarjan's SCC algorithm requires managing `tin[]`, `low[]`, an explicit in-stack boolean array, and component extraction loops.
> Kosaraju's algorithm uses standard DFS twice (Pass 1 finish stack, Pass 2 transposed DFS), making it much easier to write bug-free under interview pressure! ⚡

> **Memory Trick:** **"Kosaraju's is 2 standard DFS passes: Pass 1 finish stack -> Reverse graph -> Pass 2 collect SCCs!"**

---

## 13. System & Implementation Comparisons

| Feature | Kosaraju's Algorithm | Tarjan's SCC Algorithm |
| :--- | :--- | :--- |
| **Pass Count** | 2 Passes | **1 Single Pass ⚡** |
| **Graph Transposition**| Required ($G^T$) | Not Required |
| **Code Simplicity** | **High (Standard DFS calls) ⚡**| Moderate (Low-link stack logic) |

---

## 14. How to Recognize This in Questions
* **"Find clusters of mutually reachable web pages or microservices in a directed graph"** $\rightarrow$ Strongly Connected Components (Kosaraju / Tarjan).

---

## 15. Frequently Asked Interview Questions
* **Q: What is a Strongly Connected Component (SCC)?**  
  *A:* A maximal directed subgraph where every vertex is reachable from every other vertex within the component.
* **Q: Why does Kosaraju's algorithm transpose the graph edges in Pass 2?**  
  *A:* To prevent Pass 2 DFS from bleeding into downstream SCC components, isolating each SCC perfectly.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRONGLY CONNECTED COMPONENTS (KOSARAJU)              |
+-----------------------------------------------------------------------+
| • Definition   : Maximal directed subgraph where all pairs are mutually reachable|
| • Pass 1 (DFS) : Push nodes to Stack in order of finish times (stack.push(u))|
| • Step 2 (Trans): Reverse all edge directions to form G^T             |
| • Pass 2 (DFS) : Pop Stack; for unvisited u, DFS on G^T extracts 1 SCC!|
| • Performance  : O(V + E) Linear Time | O(V + E) Auxiliary Memory Space ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Kosaraju's 2-Pass SCC algorithm in Java.
- [ ] I know why nodes MUST be pushed to the stack in post-order finish times.
- [ ] I can write graph transposition code ($G \to G^T$).
- [ ] I can contrast Kosaraju's algorithm with Tarjan's SCC algorithm.
- [ ] I can trace Kosaraju's 2-pass execution step by step.
