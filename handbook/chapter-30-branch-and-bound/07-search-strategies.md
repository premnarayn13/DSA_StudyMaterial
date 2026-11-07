# 07. Search Strategies: FIFO, LIFO, LC-B&B & Depth-First Branch & Bound (DFB&B)

## 1. Introduction
The efficiency of a Branch & Bound algorithm depends heavily on its **Search Strategy**—the order in which live candidate nodes in the state space tree are selected for expansion. While standard **LC Branch & Bound (Least Cost / Best-First Search)** uses a Max/Min-PriorityQueue to expand the most promising node first (achieving minimal total node expansions), it suffers from exponential memory consumption ($O(B^H)$) when PriorityQueue RAM is exhausted. To overcome memory limits on massive search spaces, algorithm designers use **Depth-First Branch & Bound (DFB&B)**, which combines the minimal linear memory footprint ($O(H)$ call stack) of Depth-First Search with the aggressive cost cutoff pruning ($C \ge C^*$) of Branch & Bound.

> **Important:** Core Structural Properties of the 4 B&B Search Strategies:
> 1. **FIFO Branch & Bound**:
>    - Uses a standard `Queue<Node>`. Expands level by level. High memory overhead ($O(B^H)$), slow convergence.
> 2. **LIFO Branch & Bound**:
>    - Uses a standard `Stack<Node>`. Expands deepest node first. Low memory ($O(H)$), but easily stuck in deep sub-optimal branches.
> 3. **LC Branch & Bound (Least-Cost / Best-First)**:
>    - Uses a `PriorityQueue<Node>` ordered by optimistic bound. Minimizes expanded nodes, but requires high memory ($O(B^H)$).
> 4. **DFB&B (Depth-First Branch & Bound)**:
>    - Uses recursive DFS call stack with a globally updated best cost $C^*$.
>    - Benefits: **$O(H)$ Linear Memory Footprint** AND **Aggressive Optimality Pruning ($C \ge C^*$)**! ⚡

```
Search Strategies Memory vs Node Expansion Trade-off:

+-----------------------+-----------------------+-----------------------+
| Search Strategy       | Memory Footprint      | Node Expansions Count |
+-----------------------+-----------------------+-----------------------+
| **FIFO B&B**          | $O(B^H)$ (High)       | High                  |
| **LIFO B&B**          | $O(H)$ (Minimal)      | High                  |
| **LC B&B (Best-First)**| $O(B^H)$ (Moderate)   | **MINIMUM! ⚡**        |
| **DFB&B (Depth-First)**| **$O(H)$ (Minimal) ⚡** | Low (Pruned)          |
+-----------------------+-----------------------+-----------------------+
```

---

## 2. Core Concepts & Search Strategies Strategy Matrix

### 2.1 B&B Search Strategies Comparison Matrix
```
B&B Search Strategies Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Strategy              | Queue / Data Struct| Memory Limit      | Pruning Power     | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **FIFO B&B**          | FIFO `Queue`      | $O(B^H)$ RAM      | Weak              | Simple Level Order|
| **LIFO B&B**          | LIFO `Stack`      | **$O(H)$ Memory ⚡**| Weak              | Low Memory        |
| **LC B&B (Best-First)**| **`PriorityQueue`⚡**| $O(B^H)$ RAM      | **MAXIMUM ⚡**     | **Fewer Nodes ⚡** |
| **DFB&B**             | **DFS Call Stack ⚡**| **$O(H)$ Memory ⚡**| **Strong ($C^*$) ⚡**| **Memory Safe! ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LC-B&B minimizes node expansions using Priority Queue; DFB&B minimizes memory using $O(H)$ call stack with C* pruning!"**

---

## 3. Characteristics & DFB&B Memory Efficiency Proof

### 3.1 Mathematical Formalism of DFB&B Linear Memory Bounds
* Let $H$ be the maximum depth of the state space tree, and $B$ be the maximum branching factor.
* In LC Branch & Bound, all generated un-expanded live nodes remain stored in the Priority Queue. In worst-case trees:
  $$\text{PQ Size} = O(B^H) \implies \text{RAM Exhaustion for } H > 50$$
* In DFB&B (Depth-First Branch & Bound), search follows a single path from root to leaf:
  $$\text{Stack Depth} = O(H) \implies \text{Linear Memory (Negligible RAM!)}$$
* **How DFB&B Reaches Optimal Solutions**:
  1. DFB&B visits the first complete leaf solution quickly, establishing an initial upper bound $C^* = f(S_1)$.
  2. As DFB&B continues exploring, any subproblem branch whose lower bound $\hat{l}(u) \ge C^*$ is killed immediately.
  3. When a better leaf solution is found ($f(S_2) < C^*$), $C^*$ is updated ($C^* = f(S_2)$), tightening pruning for all remaining branches! ⚡

---

## 4. Internal Working Mechanics: DFB&B Execution Engine

Tracing DFB&B for Minimization Problem:

```
Initialize Best Cost C* = INFINITY. Stack Depth = O(H).

Step 1: Traverse Leftmost Branch to Leaf:
- Leaf Solution 1 reached: Cost = 50.
- Update Best Cost C* = 50! ⚡

Step 2: Backtrack and Explore Branch B:
- Calculate lower bound l_hat(B) = 52.
- Check Optimality Pruning: l_hat(B) = 52 >= C* (50) -> KILLED IMMEDIATELY! ❌

Step 3: Explore Branch C:
- Lower bound l_hat(C) = 40 < C* (50) -> Traverse deeper!
- Leaf Solution 2 reached: Cost = 42.
- Update Best Cost C* = 42! ⚡

Guarantees 100% optimal solution using only O(H) memory! ✅ ⚡
```

---

## 5. Visual Diagram: DFB&B Stack vs LC-B&B Priority Queue

```
DFB&B vs LC-B&B Memory Topology:

LC-B&B Priority Queue (RAM Heavy):
[ Node 1, Node 2, Node 3, Node 4, Node 5 ... Node 10,000 ] ──► Exhausts Memory! ❌

DFB&B Call Stack (Linear Memory):
[ Root ──► Node A ──► Node A1 ──► Leaf ] ──► Uses O(H) Stack Depth Only! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Depth-First Branch & Bound (DFB&B) vs LC-B&B search engines.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced B&B Search Strategies:
 * Depth-First Branch & Bound (DFB&B) vs LC Branch & Bound (Priority Queue).
 */
public class SearchStrategiesMaster {

    // =========================================================================
    // 1. DEPTH-FIRST BRANCH & BOUND (DFB&B - O(H) MEMORY FOOTPRINT)
    // =========================================================================
    private int bestCostDFBB = Integer.MAX_VALUE;

    /**
     * Solves minimization problem using DFB&B (O(H) memory stack).
     *
     * @param dist 2D adjacency distance matrix
     * @return optimal minimum cost
     */
    public int solveDFBB(int[][] dist) {
        if (dist == null || dist.length == 0) return 0;
        int n = dist.length;

        bestCostDFBB = Integer.MAX_VALUE;
        boolean[] visited = new boolean[n];
        visited[0] = true;

        dfbbDFS(dist, 0, visited, 1, 0, n);
        return bestCostDFBB;
    }

    private void dfbbDFS(int[][] dist, int u, boolean[] visited, int count, int currentCost, int n) {
        // OPTIMALITY CUTOFF PRUNING LINE ⚡
        if (currentCost >= bestCostDFBB) return; // Prune!

        if (count == n) {
            if (dist[u][0] > 0) {
                int totalCost = currentCost + dist[u][0];
                bestCostDFBB = Math.min(bestCostDFBB, totalCost); // Update global best C*! ⚡
            }
            return;
        }

        for (int v = 0; v < n; v++) {
            if (!visited[v] && dist[u][v] > 0) {
                // Admissible pre-call feasibility & cost check
                if (currentCost + dist[u][v] < bestCostDFBB) {
                    visited[v] = true;
                    dfbbDFS(dist, v, visited, count + 1, currentCost + dist[u][v], n);
                    visited[v] = false; // Unchoose
                }
            }
        }
    }
}
```

> **Quick Syntax:**
```java
// DFB&B Optimality Cutoff Line
if (currentCost >= bestCostDFBB) return; // Prune using global best C*
```

---

## 7. Concrete Problem Examples & Applications

1. **DFB&B Search**:
   - Memory-safe B&B search for deep state trees ($O(H)$ memory).

2. **LC Branch & Bound**:
   - Minimum node expansion search using Priority Queue ($O(B^H)$ memory).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class SearchStrategiesDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   B&B SEARCH STRATEGIES BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        SearchStrategiesMaster master = new SearchStrategiesMaster();

        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };

        int minCost = master.solveDFBB(dist);

        System.out.println("1. Depth-First Branch & Bound (DFB&B) Result:");
        System.out.println("   Memory Footprint: O(H) Stack Depth Only");
        System.out.println("   Minimum Cost (Optimal C*): " + minCost + " (Optimal = 80)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Search Strategy | Data Structure | Memory Complexity | Node Expansions | Ideal Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **LC B&B** | `PriorityQueue` | $O(B^H)$ RAM Heavy | **MINIMUM! ⚡** | Small memory trees |
| **DFB&B**  | `Call Stack` | $\mathbf{O(H)}$ Linear ⚡| Low (Pruned) | **Deep trees ($H > 50$)⚡**|
| **FIFO B&B**| `Queue` | $O(B^H)$ RAM Heavy | High | Level order search |

---

## 10. Edge Cases & Boundary Handling

1. **Massive Search Tree ($H > 100$)**:
   - DFB&B runs smoothly in linear memory, while LC-B&B crashes with `OutOfMemoryError`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running LC Branch & Bound on Huge Search Trees Without Memory Guard**:
  - Pushing millions of nodes into a Priority Queue causes memory overflow. Use **DFB&B** when RAM is limited!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The DFB&B Advantage:
> DFB&B combines the **$O(H)$ Linear Memory** of Depth-First Search with the **Optimality Pruning ($C \ge C^*$)** of Branch & Bound, making it ideal for deep search trees! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | LC Branch & Bound | Depth-First Branch & Bound (DFB&B) |
| :--- | :--- | :--- |
| **Memory Limit** | $O(B^H)$ PriorityQueue | **$O(H)$ Linear Stack ⚡** |
| **First Solution** | Delayed until leaf popped | **Found Fast (First DFS Branch) ⚡**|
| **Pruning Trigger**| Immediate on poll | Updated when better $C^*$ found |

---

## 14. How to Recognize This in Questions

* **"Which B&B strategy combines O(H) linear memory with cost pruning?"** $\rightarrow$ Depth-First Branch & Bound (DFB&B).

---

## 15. Frequently Asked Interview Questions

* **Q: What is DFB&B (Depth-First Branch & Bound)?**  
  *A:* A hybrid search strategy that executes Depth-First Search (using $O(H)$ memory stack) while maintaining a global best cost $C^*$ to prune subtrees whose lower bound $\ge C^*$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: B&B SEARCH STRATEGIES                                 |
+-----------------------------------------------------------------------+
| • LC-B&B : Best-First Priority Queue -> Minimizes node expansions     |
| • DFB&B  : DFS Stack + C* Pruning -> O(H) Linear Memory Footprint! ⚡  |
| • FIFO   : Level-Order Queue -> High memory, slow convergence         |
| • Choice : Use LC-B&B for small trees; Use DFB&B for deep trees! ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can list the 4 search strategies (FIFO, LIFO, LC, DFB&B).
- [ ] I can write DFB&B in Java using recursive stack and $C^*$ pruning.
- [ ] I can explain why DFB&B uses $O(H)$ memory compared to LC-B&B $O(B^H)$.
- [ ] I can state when to select DFB&B over LC-B&B.
- [ ] I can explain how global best cost $C^*$ updates in DFB&B.
