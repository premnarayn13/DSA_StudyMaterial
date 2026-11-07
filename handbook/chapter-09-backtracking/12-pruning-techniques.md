# 12. Pruning Techniques: Feasibility Bounding, Symmetry Breaking & Constraint Propagation

## 1. Introduction
**Backtracking Pruning Techniques** represent the single most impactful optimization paradigm for reducing the worst-case exponential time complexity ($O(2^N)$ or $O(N!)$) of combinatorial search algorithms down to practical execution times. Rather than blindly exploring all branches of a State Space Tree, Pruning evaluates mathematical and logical **Bounding Functions** to detect "dead-end" states early and terminate ("prune") entire subtrees. The five primary pruning strategies are:
1. **Feasibility Bounding / Constraint Pruning**: Kills candidate branches that violate problem constraints BEFORE allocating a new recursive stack frame.
2. **Optimality Bounding / Cost Pruning**: Kills candidate branches whose accumulated cost (or theoretical best completion lower bound) already exceeds the cost of the best solution found so far ($C_{\text{accumulated}} \ge C^*$).
3. **Symmetry Breaking**: Eliminates duplicate symmetric search branches (e.g. fixing rotation, reflection, or permutation order).
4. **Equivalence Class Pruning**: Groups identical candidate values at the same decision depth (`if (i > startIndex && nums[i] == nums[i-1]) continue;`).
5. **Constraint Propagation / Minimum Remaining Values (MRV)**: Greedily selects the **Most Constrained Decision Variable** first (the variable with the FEWEST remaining valid choices).

> **Important:** Core Structural Rules of Pruning:
> 1. **Pre-Call Evaluation Rule**:
>    - ALWAYS check `isValid(choice)` BEFORE calling `backtrack(child)` to avoid unnecessary function stack allocations!
> 2. **Optimality Cutoff Invariant ($C \ge C^*$)**:
>    - Maintain a global or passed minimum cost $C^*$. If `currentCost >= C*`, prune branch immediately (`return`).
> 3. **Minimum Remaining Values (MRV / Most Constrained Variable)**:
>    - In Sudoku or Map Coloring, select the empty cell with the FEWEST valid digit candidates first. This prunes dead ends at shallow depths! ⚡

```
Pruning Strategy Classification Topology:

State Tree Pruning Techniques:
├── 1. Feasibility Bounding    ──► Kills branches violating constraints (e.g., N-Queens threat check)
├── 2. Optimality Bounding     ──► Kills branches exceeding current best cost C* (e.g., Traveling Salesperson)
├── 3. Symmetry Breaking       ──► Eliminates rotation/reflection symmetry (e.g., Fix root = 0)
├── 4. Equivalence Classing    ──► Skips duplicate values at same level (e.g., Subsets II / Comb Sum II)
└── 5. Constraint Propagation  ──► Chooses Most Constrained Variable (MRV) first! ⚡
```

---

## 2. Core Concepts & Pruning Strategy Matrix

### 2.1 Pruning Techniques Strategy Matrix
```
Pruning Techniques Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pruning Technique     | Core Mechanism    | Trigger Condition | Time Reduction    | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Feasibility Bound** | Pre-Call Validation| Constraint Violated| **$O(B^H) \to O(\text{Pruned})$⚡**| **$O(1)$ Extra ⚡**|
| **Optimality Bound**  | Cost Threshold    | $C_{\text{curr}} \ge C^*$| **$O(N!) \to O(2^N)$⚡**| $O(1)$ Best Var   |
| **Symmetry Breaking** | Fix Base Index    | Rotational Match  | **Eliminates $K\times$ ⚡**| $O(1)$ Extra      |
| **Equivalence Class** | Sort + Skip Equal | $i > \text{startIndex}$| Eliminates Dupes  | $O(1)$ Extra      |
| **MRV Variable Pick** | Smallest Candidates| Minimum Options   | **Shallow Pruning ⚡**| $O(V)$ Array      |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Feasibility prunes invalid choices; Optimality prunes costs >= C*; MRV picks most constrained variable first!"**

---

## 3. Characteristics & Optimality Bounding Proof

### 3.1 Mathematical Formalism of Optimality Bounding
* Let $P$ be a minimization problem with objective function $f(S)$.
* Let $C^*$ be the best valid solution cost found so far during search ($C^* = \min_{S \in \text{Found}} f(S)$).
* At search node $u$ at depth $k$, let $c_{\text{accumulated}}(u)$ be the exact cost incurred so far, and $h(u)$ be a admissible lower bound cost to complete the solution from $u$.
* Estimated completion cost:
  $$f_{\text{est}}(u) = c_{\text{accumulated}}(u) + h(u)$$
* **Optimality Pruning Rule**:
  - If $f_{\text{est}}(u) \ge C^*$, then NO descendant solution of node $u$ can possibly beat $C^*$.
  - Node $u$ and its ENTIRE subtree can be safely killed (`return`) without losing global optimality!
* Reduces search time dramatically in weighted graph and assignment problems! ⚡

---

## 4. Internal Working Mechanics: MRV Constraint Propagation (Sudoku Example)

How Minimum Remaining Values (MRV) selects the most constrained empty cell:

```
Sudoku Board Cell Candidate Option Counts:

- Cell A at (0, 2): Valid digit options remaining = [1, 5, 8] (3 Options)
- Cell B at (3, 4): Valid digit options remaining = [7]       (1 Option - MOST CONSTRAINED!) ⚡
- Cell C at (6, 1): Valid digit options remaining = [2, 4, 9] (3 Options)

MRV Strategy: Select Cell B (1 Option) first!
- If Cell B is filled with '7', it immediately updates constraints for its row, col, and box.
- Detects contradictions at depth 1 instead of exploring depth 5! ✅ ⚡
```

---

## 5. Visual Diagram: Optimality Bounding Pruning Tree

```
Optimality Bounding Tree (Current Best Cost C* = 25):

                             [ Root (Cost = 0) ]
                            /         |         \
                           /          |          \
                 [ Node A (10) ] [ Node B (26) ] [ Node C (15) ]
                        │             │                │
               Explore Deeper...   PRUNED! ❌   Explore Deeper...
                              (Cost 26 >= C* 25)

Saves exploring millions of sub-optimal solution branches! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Optimality Bounding (TSP Cost Pruning), MRV Constraint Propagation, and Equivalence Class Pruning.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced Backtracking Pruning Techniques:
 * Feasibility Bounding, Optimality Bounding, MRV Variable Selection, and Symmetry Breaking.
 */
public class PruningTechniquesMaster {

    // =========================================================================
    // 1. OPTIMALITY BOUNDING: TSP BACKTRACKING WITH COST CUTOFF (O(N!) Pruned)
    // =========================================================================
    private int bestTSPCost = Integer.MAX_VALUE;

    /**
     * Solves Traveling Salesperson Problem using Optimality Bounding Pruning.
     *
     * @param dist 2D adjacency matrix of distances
     * @return minimum tour distance cost
     */
    public int solveTSPOptimalityPruning(int[][] dist) {
        if (dist == null || dist.length == 0) return 0;
        int n = dist.length;

        bestTSPCost = Integer.MAX_VALUE;
        boolean[] visited = new boolean[n];
        visited[0] = true; // Fix origin (Symmetry Breaking!) ⚡

        tspPruningDFS(dist, 0, visited, 1, 0, n);
        return bestTSPCost;
    }

    private void tspPruningDFS(int[][] dist, int u, boolean[] visited, int count, int currentCost, int n) {
        // OPTIMALITY BOUNDING PRUNING LINE ⚡
        if (currentCost >= bestTSPCost) {
            return; // Prune branch immediately! ⚡
        }

        if (count == n) {
            // Check return edge to origin 0
            if (dist[u][0] > 0) {
                int totalCost = currentCost + dist[u][0];
                bestTSPCost = Math.min(bestTSPCost, totalCost); // Update best C* ⚡
            }
            return;
        }

        for (int v = 0; v < n; v++) {
            if (!visited[v] && dist[u][v] > 0) {
                // Feasibility Check
                if (currentCost + dist[u][v] >= bestTSPCost) continue; // Pre-call prune! ⚡

                visited[v] = true;
                tspPruningDFS(dist, v, visited, count + 1, currentCost + dist[u][v], n);
                visited[v] = false; // Unchoose
            }
        }
    }

    // =========================================================================
    // 2. MRV CONSTRAINT PROPAGATION: MOST CONSTRAINED VARIABLE SELECTOR
    // =========================================================================
    public static class MRVCell {
        public final int r, c, candidateCount;
        public MRVCell(int r, int c, int candidateCount) {
            this.r = r; this.c = c; this.candidateCount = candidateCount;
        }
    }

    /**
     * Finds the empty Sudoku cell with the Minimum Remaining Values (MRV).
     */
    public MRVCell findMRVCell(char[][] board, boolean[][] rows, boolean[][] cols, boolean[][] boxes) {
        int minCandidates = 10;
        MRVCell bestCell = null;

        for (int r = 0; r < 9; r++) {
            for (int c = 0; c < 9; c++) {
                if (board[r][c] == '.') {
                    int b = (r / 3) * 3 + (c / 3);
                    int count = 0;

                    for (int d = 1; d <= 9; d++) {
                        if (!rows[r][d] && !cols[c][d] && !boxes[b][d]) {
                            count++;
                        }
                    }

                    if (count < minCandidates) {
                        minCandidates = count;
                        bestCell = new MRVCell(r, c, count);
                    }
                }
            }
        }

        return bestCell; // Most constrained cell! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Optimality Bounding Pruning Line
if (currentCost >= bestCost) return; // Prune sub-optimal branch
```

---

## 7. Concrete Problem Examples & Applications

1. **TSP Backtracking with Optimality Bounding**:
   - Pruning sub-optimal paths exceeding `bestCost` ($O(N!)$ pruned).

2. **Sudoku Solver with MRV Variable Selection**:
   - Selecting the cell with fewest valid candidate digits first.

3. **Combination Sum II Duplicate Pruning (LeetCode 40)**:
   - Equivalence class pruning (`if (i > startIndex && nums[i] == nums[i-1]) continue;`).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class PruningTechniquesDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BACKTRACKING PRUNING TECHNIQUES DEMO          ");
        System.out.println("=================================================\n");

        PruningTechniquesMaster master = new PruningTechniquesMaster();

        // 1. Optimality Bounding TSP Test
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };

        int minCost = master.solveTSPOptimalityPruning(dist);
        System.out.println("1. TSP Backtracking with Optimality Bounding Pruning:");
        System.out.println("   Minimum Tour Cost (C* Pruned): " + minCost + " Cost (Optimal = 80)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Pruning Technique | Primary Mechanism | Time Complexity Reduction | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **Feasibility Bounding** | Pre-Call Validation | $O(B^H) \to O(\text{Pruned})$ | $\mathbf{O(1)}$ Memory ⚡|
| **Optimality Bounding**  | $C_{\text{curr}} \ge C^*$ Cutoff | $O(N!) \to O(2^N)$ | $\mathbf{O(1)}$ Memory ⚡|
| **Symmetry Breaking**    | Fix Root / Order | Eliminates $K\times$ branches | $\mathbf{O(1)}$ Memory ⚡|
| **MRV Variable Pick**    | Smallest Candidates | Shallow Subtree Pruning | $O(V)$ Array |

---

## 10. Edge Cases & Boundary Handling

1. **No Valid Initial Candidate Solutions Found**:
   - `bestCost` remains `Integer.MAX_VALUE`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Evaluating Optimality Bounding AFTER Adding Child Cost**:
  - Waiting until the child recursive call executes before checking `currentCost >= bestCost` wastes stack frame allocations. **ALWAYS check `currentCost + edgeCost >= bestCost` BEFORE calling DFS!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 5 Pruning Strategies to Name:
> 1. **Feasibility Bounding** (`isValid()`).
> 2. **Optimality Bounding** ($C \ge C^*$).
> 3. **Symmetry Breaking** (Fix origin).
> 4. **Equivalence Classing** (`i > startIndex`).
> 5. **MRV Variable Selection** (Most constrained variable first). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Unpruned Search | Optimality Pruned Search |
| :--- | :--- | :--- |
| **Branch Evaluated** | All Candidate Branches | **Prunes if $C \ge C^*$ ⚡** |
| **Execution Time** | Hours (Freeze) | **< 10 Milliseconds ⚡** |
| **Correctness** | Guaranteed | **100% Guaranteed Optimal ⚡** |

---

## 14. How to Recognize This in Questions

* **"Optimize backtracking search to find minimum cost tour or assignment"** $\rightarrow$ Optimality Bounding ($C \ge C^*$).
* **"Select decision variable with fewest valid choices first"** $\rightarrow$ MRV Constraint Propagation.

---

## 15. Frequently Asked Interview Questions

* **Q: What is Optimality Bounding?**  
  *A:* A pruning technique that terminates search along a candidate branch if the current accumulated cost (or lower bound cost) is $\ge$ the cost of the best solution found so far.

* **Q: What is MRV (Minimum Remaining Values)?**  
  *A:* A heuristic that selects the decision variable with the fewest remaining valid choices first, forcing failures and dead ends to occur at shallow depths in the search tree.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRUNING TECHNIQUES                                    |
+-----------------------------------------------------------------------+
| • Feasibility : Pre-call check isValid(choice) -> Avoid stack frames  |
| • Optimality  : If currentCost >= bestCost -> Prune branch immediately|
| • Symmetry    : Fix root origin (e.g. path[0] = 0) -> Kx reduction    |
| • Equivalence : Skip duplicates if (i > startIndex && nums[i] == prev)|
| • MRV Pick    : Choose empty cell with FEWEST candidate options first |
| • Performance : Prunes exponential state trees by 99%+ ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the 5 major pruning strategies.
- [ ] I can write TSP Backtracking with Optimality Bounding in Java.
- [ ] I can write MRV Variable Selector for Sudoku.
- [ ] I can explain why optimality bounding is 100% mathematically safe.
- [ ] I can state why pre-call feasibility checks save memory.
