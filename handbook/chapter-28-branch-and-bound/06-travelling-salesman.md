# 06. Travelling Salesman (TSP): Reduced Cost Matrices & Matrix Transformation

## 1. Introduction
The **Travelling Salesperson Problem (TSP)** is the premier NP-hard graph optimization problem where given an $N \times N$ distance cost matrix $D$ representing $N$ cities, the goal is to find a minimum-cost tour that visits **EVERY CITY EXACTLY ONCE** and returns to the starting origin city. While Held-Karp Bitmask DP solves TSP in $O(N^2 \cdot 2^N)$ time (which fails due to memory limits for $N > 22$), **Least-Cost Branch & Bound (LC-B&B)** using **Reduced Cost Matrix Lower Bounds** solves TSP optimization instances for $N = 30+$ cities in practical execution bounds. LC-B&B maintains a Min-PriorityQueue of live search nodes ordered by their reduced matrix lower bound $\hat{l}(x)$, expanding the most promising tour prefix first.

> **Important:** Core Structural Invariants of LC-B&B TSP Matrix Reduction:
> 1. **Initial Matrix Reduction & Root Lower Bound**:
>    - Perform row reduction (subtract row min from each row) and column reduction (subtract col min from each column).
>    - Initial Root Lower Bound $\hat{l}(\text{Root}) = \sum \text{Row Mins} + \sum \text{Col Mins}$.
> 2. **Matrix Transformation Rule for Edge Transition $u \to v$**:
>    - When stepping from city $u$ to city $v$:
>      - Set **Row $u = \infty$** (City $u$ cannot depart to any other city!).
>      - Set **Column $v = \infty$** (City $v$ cannot be entered from any other city!).
>      - Set **Edge $v \to u = \infty$** (Prevents early 2-city sub-tour cycle!).
> 3. **Child Node Lower Bound Formula ($\hat{l}(\text{Child})$)**:
>    $$\hat{l}(\text{Child}) = \hat{l}(\text{Parent}) + \text{ReducedMatrix}[u][v] + \text{New Reduction Cost of Transformed Matrix}$$
> 4. **Min-PriorityQueue Node Ordering**:
>    - Live Nodes are stored in a Min-PriorityQueue ordered by Lower Bound $\hat{l}(x)$, expanding the lowest cost tour prefix first! ⚡

```
TSP Reduced Cost Matrix Edge Transition (City u -> City v):

Original Reduced Matrix M:
- Row u (Depart from u) ──► Set ALL cells in Row u to INFINITY (∞) ⚡
- Col v (Arrive at v)   ──► Set ALL cells in Col v to INFINITY (∞) ⚡
- Cell (v, u)           ──► Set Cell (v, u) to INFINITY (∞) (No return!) ⚡

Reduce Transformed Matrix ──► New Lower Bound = ParentBound + M[u][v] + ReductionCost! ⚡
```

---

## 2. Core Concepts & TSP Strategy Matrix

### 2.1 TSP Implementations Strategy Matrix
```
TSP Implementations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Implementation        | Bounding Engine   | Memory Complexity | Time Complexity   | City Limit $N$    |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Held-Karp Bitmask DP**| Subsets DP Table | $O(N \cdot 2^N)$  | $O(N^2 \cdot 2^N)$| Fails if $N > 22$ ❌|
| **LC Branch & Bound** | **Matrix Reduction⚡**| **$O(N!)$ PriorityQueue⚡**| **Pruned $O(N!)$ ⚡**| **$N = 30+$ Cities ⚡**|
| **2-Opt / 3-Opt**     | Edge Swapping     | $O(N^2)$ Matrix   | $O(N^2)$ Fast     | Heuristic (Approx)|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LC-B&B TSP sets Row u = inf, Col v = inf, Cell(v, u) = inf when stepping u -> v; Pops lowest l_hat from Min-PQ!"**

---

## 3. Characteristics & TSP Matrix Reduction Admissibility Proof

### 3.1 Mathematical Proof of Matrix Reduction Lower Bound Admissibility
* Let $M$ be an $N \times N$ distance cost matrix. Any valid TSP tour must select EXACTLY ONE entry in each row $r$ (departing city $r$) and EXACTLY ONE entry in each column $c$ (arriving city $c$).
* Let $r_i = \min_{j} M[i][j]$ be the minimum element in row $i$.
* Subtracting $r_i$ from all elements in row $i$ reduces the cost matrix, but every valid tour MUST pay at least $r_i$ for leaving city $i$.
* Summing row minimums $\sum r_i$ and column minimums $\sum c_j$ yields total reduction cost $R$.
* For any valid tour $T$:
  $$\text{Cost}(T) = \sum_{(i,j) \in T} M[i][j] = R + \sum_{(i,j) \in T} M_{\text{reduced}}[i][j] \ge R$$
* Since $M_{\text{reduced}}[i][j] \ge 0$ for all cells, $R$ is an **Admissible Lower Bound** on the cost of any complete TSP tour. Admissibility holds! ⚡

---

## 4. Internal Working Mechanics: Step-by-Step Matrix Reduction Execution

Tracing TSP Matrix Reduction for $4 \times 4$ Cost Matrix ($u=0 \to v=1$):

```
Initial Cost Matrix:
[ ∞, 20, 30, 10 ]
[ 15, ∞, 16,  4 ]
[  3,  5, ∞,  2 ]
[ 19,  6, 18, ∞ ]

Step 1: Row Reduction:
Row 0 min = 10 ──► [ ∞, 10, 20,  0 ]
Row 1 min =  4 ──► [ 11, ∞, 12,  0 ]
Row 2 min =  2 ──► [  1,  3, ∞,  0 ]
Row 3 min =  6 ──► [ 13,  0, 12, ∞ ]
Row Minimum Sum = 10 + 4 + 2 + 6 = 22.

Step 2: Column Reduction:
Col 0 min = 1 ──► [ 10,  9,  0, 12 ]
Col 1 min = 0
Col 2 min = 0
Col 3 min = 0
Column Minimum Sum = 1.

Root Lower Bound l_hat(Root) = 22 + 1 = 25!

Step 3: Transition from City 0 -> City 1 (M[0][1] = 10):
- Set Row 0 = ∞, Set Col 1 = ∞, Set Cell(1,0) = ∞.
- Re-reduce transformed matrix ──► Calculates exact Child Lower Bound l_hat(Child)! ✅ ⚡
```

---

## 5. Visual Diagram: Reduced Cost Matrix Transformation Topology

```
Transformed Matrix for Transition (City 0 -> City 1):

     Col 0    Col 1    Col 2    Col 3
Row 0 [  ∞      ∞        ∞        ∞  ] ◄── Row 0 Set to INFINITY! ⚡
Row 1 [  ∞      ∞       12        0  ] ◄── Cell(1,0) Set to INFINITY! ⚡
Row 2 [  1      ∞        ∞        0  ]
Row 3 [ 13      ∞       12        ∞  ]
                ▲
                └── Column 1 Set to INFINITY! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LC Branch & Bound TSP Solver with Matrix Reduction and State Transformations.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Travelling Salesperson Problem (TSP):
 * LC Branch & Bound, Reduced Cost Matrices, Edge Masking, and Min-Priority Queue.
 */
public class TSPBranchAndBoundMaster {

    private static final int INF = 1_000_000_000;

    public static class TSPNode implements Comparable<TSPNode> {
        public final int vertex;    // Current city
        public final int level;     // Visited cities count
        public final int lowerBound;// Lower bound l_hat ⚡
        public final int[][] reducedMatrix; // Transformed cost matrix
        public final List<Integer> path;    // Tour path

        public TSPNode(int vertex, int level, int lowerBound, int[][] reducedMatrix, List<Integer> path) {
            this.vertex = vertex;
            this.level = level;
            this.lowerBound = lowerBound;
            this.reducedMatrix = reducedMatrix;
            this.path = new ArrayList<>(path);
        }

        @Override
        public int compareTo(TSPNode o) {
            return Integer.compare(this.lowerBound, o.lowerBound); // MIN-PRIORITY QUEUE ⚡
        }
    }

    // =========================================================================
    // 1. LC BRANCH & BOUND TSP SOLVER (MATRIX REDUCTION)
    // =========================================================================
    /**
     * Solves TSP problem returning minimum tour cost.
     *
     * @param distanceMatrix N x N distance matrix (use INF for no edge)
     * @return minimum tour distance cost
     */
    public int solveTSPBranchAndBound(int[][] distanceMatrix) {
        if (distanceMatrix == null || distanceMatrix.length == 0) return 0;
        int n = distanceMatrix.length;

        int[][] initialMatrix = copyMatrix(distanceMatrix, n);
        int rootBound = reduceMatrix(initialMatrix, n);

        List<Integer> initialPath = new ArrayList<>();
        initialPath.add(0); // Start at City 0 ⚡

        PriorityQueue<TSPNode> pq = new PriorityQueue<>();
        pq.add(new TSPNode(0, 1, rootBound, initialMatrix, initialPath));

        int bestCost = INF;

        while (!pq.isEmpty()) {
            TSPNode curr = pq.poll();

            // Optimality Bounding Cutoff ⚡
            if (curr.lowerBound >= bestCost) continue;

            // Base Case: All N cities visited!
            if (curr.level == n) {
                // Return to origin City 0 cost
                int lastVertex = curr.vertex;
                int returnCost = distanceMatrix[lastVertex][0];
                if (returnCost < INF) {
                    int totalTourCost = curr.lowerBound;
                    bestCost = Math.min(bestCost, totalTourCost); // Update best C* ⚡
                }
                continue;
            }

            int u = curr.vertex;

            // Try visiting candidate next city v
            for (int v = 0; v < n; v++) {
                if (curr.reducedMatrix[u][v] < INF) {
                    int[][] nextMatrix = copyMatrix(curr.reducedMatrix, n);

                    int edgeCost = curr.reducedMatrix[u][v];

                    // Transform Matrix for Edge (u -> v): Set Row u = INF, Col v = INF, Cell(v,u) = INF ⚡
                    setEdgeInfinity(nextMatrix, u, v, n);

                    int reductionCost = reduceMatrix(nextMatrix, n);
                    int nextBound = curr.lowerBound + edgeCost + reductionCost;

                    if (nextBound < bestCost) {
                        List<Integer> nextPath = new ArrayList<>(curr.path);
                        nextPath.add(v);
                        pq.add(new TSPNode(v, curr.level + 1, nextBound, nextMatrix, nextPath));
                    }
                }
            }
        }

        return bestCost;
    }

    private int reduceMatrix(int[][] matrix, int n) {
        int reductionSum = 0;

        // Row Reduction
        for (int r = 0; r < n; r++) {
            int rowMin = INF;
            for (int c = 0; c < n; c++) {
                if (matrix[r][c] < rowMin) rowMin = matrix[r][c];
            }
            if (rowMin > 0 && rowMin < INF) {
                reductionSum += rowMin;
                for (int c = 0; c < n; c++) {
                    if (matrix[r][c] < INF) matrix[r][c] -= rowMin;
                }
            }
        }

        // Column Reduction
        for (int c = 0; c < n; c++) {
            int colMin = INF;
            for (int r = 0; r < n; r++) {
                if (matrix[r][c] < colMin) colMin = matrix[r][c];
            }
            if (colMin > 0 && colMin < INF) {
                reductionSum += colMin;
                for (int r = 0; r < n; r++) {
                    if (matrix[r][c] < INF) matrix[r][c] -= colMin;
                }
            }
        }

        return reductionSum;
    }

    private void setEdgeInfinity(int[][] matrix, int u, int v, int n) {
        for (int i = 0; i < n; i++) {
            matrix[u][i] = INF; // Row u = INF ⚡
            matrix[i][v] = INF; // Col v = INF ⚡
        }
        matrix[v][u] = INF; // Edge (v -> u) = INF ⚡
    }

    private int[][] copyMatrix(int[][] src, int n) {
        int[][] dest = new int[n][n];
        for (int i = 0; i < n; i++) dest[i] = src[i].clone();
        return dest;
    }
}
```

> **Quick Syntax:**
```java
// TSP Edge Transformation Line
for (int i = 0; i < n; i++) { matrix[u][i] = INF; matrix[i][v] = INF; } matrix[v][u] = INF;
```

---

## 7. Concrete Problem Examples & Applications

1. **TSP Matrix Reduction Solver**:
   - Primary 30+ city TSP solver benchmark ($O(N!)$ pruned).

2. **Robotic Delivery Route Optimization**:
   - Optimizing drone delivery stop sequence with distance matrices.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class TSPDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   TSP BRANCH & BOUND BENCHMARK DEMO            ");
        System.out.println("=================================================\n");

        TSPBranchAndBoundMaster master = new TSPBranchAndBoundMaster();
        int INF = 1_000_000_000;

        int[][] dist = {
            {INF, 10, 15, 20},
            {10, INF, 35, 25},
            {15, 35, INF, 30},
            {20, 25, 30, INF}
        };

        int minTourCost = master.solveTSPBranchAndBound(dist);

        System.out.println("1. TSP LC Branch & Bound Result:");
        System.out.println("   Minimum Tour Distance Cost: " + minTourCost + " (Optimal = 80)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| TSP Solving Paradigm | Time Complexity | Auxiliary Space | City Limit $N$ |
| :--- | :--- | :--- | :--- |
| **Held-Karp Bitmask DP**| $O(N^2 \cdot 2^N)$ Exponential | $O(N \cdot 2^N)$ DP Table | Fails if $N > 22$ ❌ |
| **LC Branch & Bound**   | $\mathbf{O(N!)}$ Pruned ⚡| $\mathbf{O(N!)}$ PriorityQueue| **$N = 30+$ Cities ⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **Unreachable City Pair ($M[u][v] = \infty$)**:
   - Skipped immediately during neighbor exploration loop.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Set Edge `Cell(v, u) = INF` After Stepping `u -> v`**:
  - Failing to set `matrix[v][u] = INF` permits early 2-city back-and-forth cycles before all $N$ cities are visited. **ALWAYS set `matrix[v][u] = INF`**!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 3 TSP Matrix Transformation Steps for Edge $u \to v$:
> 1. Set **Row $u = \infty$**.
> 2. Set **Column $v = \infty$**.
> 3. Set **Cell $(v, u) = \infty$**. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Held-Karp Bitmask DP | LC Branch & Bound TSP |
| :--- | :--- | :--- |
| **Memory Bottleneck** | Exhausts RAM at $N=23$ | **Handles $N=30+$ Cities ⚡** |
| **Data Structure** | 2D Memory Matrix | Min-Priority Queue |
| **Execution Speed** | Fixed $O(N^2 \cdot 2^N)$ | **Pruned Fast Execution ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find shortest TSP tour visiting all N cities using Branch & Bound"** $\rightarrow$ TSP LC-B&B Matrix Reduction.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does LC Branch & Bound handle more cities than Bitmask DP for TSP?**  
  *A:* Because Bitmask DP requires storing $N \cdot 2^N$ states in memory regardless of edge weights, whereas LC-B&B prunes up to 99% of subtrees using tight lower bounds.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: TSP BRANCH & BOUND                                    |
+-----------------------------------------------------------------------+
| • Root Bound  : Row min sum + Col min sum                             |
| • Edge Step   : Step u -> v -> Set Row u = INF, Col v = INF, (v,u)=INF⚡|
| • Child Bound : ParentBound + M[u][v] + NewReductionCost              |
| • PriorityQueue: Min-PQ ordered by lowerBound -> Pops lowest l_hat    |
| • Performance : Handles N = 30+ cities where Bitmask DP fails! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write TSP LC Branch & Bound in Java using Priority Queue.
- [ ] I can state the 3 matrix transformation rules for edge $u \to v$.
- [ ] I can write the row and column matrix reduction helper function.
- [ ] I can explain why Bitmask DP fails for $N > 22$ while B&B succeeds.
- [ ] I can state why `Cell(v, u) = INF` prevents early cycle creation.
