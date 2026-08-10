# 03. Bounding Functions: Admissibility, LP Relaxation & Matrix Reductions

## 1. Introduction
A **Bounding Function** is the mathematical core of Branch & Bound algorithms. It computes a theoretical optimistic limit on the best possible objective value achievable by expanding any candidate state node $x$ in a state space tree. For minimization problems, the Bounding Function computes an **Admissible Lower Bound $\hat{l}(x)$**; for maximization problems, it computes an **Admissible Upper Bound $\hat{u}(x)$**. By guaranteeing that no complete solution in the subtree of node $x$ can beat its bounding function estimate, Branch & Bound safely prunes ("kills") unpromising nodes whenever their optimistic bound cannot improve upon the current global best solution ($C^*$ or $P^*$). Constructing effective Bounding Functions relies on **Problem Relaxation Techniques**, such as **Continuous LP Relaxation**, **Fractional Knapsack Relaxation**, and **Row-Column Matrix Reduction**.

> **Important:** Core Structural Properties of Bounding Functions:
> 1. **Admissibility Condition (No Over-Estimation / Under-Estimation)**:
>    - Minimization: $\hat{l}(x) \le f(S^*_{\text{subtree}(x)})$ (Lower bound MUST NOT overestimate true cost!).
>    - Maximization: $\hat{u}(x) \ge f(S^*_{\text{subtree}(x)})$ (Upper bound MUST NOT underestimate true profit!).
> 2. **Monotonicity Property**:
>    - As search moves deeper down the state space tree from parent $u$ to child $v$, the optimistic bound becomes tighter and monotonically less optimistic:
>      $$\hat{l}(u) \le \hat{l}(v) \quad (\text{Minimization}) \quad \text{or} \quad \hat{u}(u) \ge \hat{u}(v) \quad (\text{Maximization})$$
> 3. **The Tightness vs Speed Trade-off**:
>    - **Tight Bounds**: Prunes more nodes from the tree, but requires more CPU time per node to calculate.
>    - **Loose Bounds**: Fast to compute per node, but expands more total nodes in the tree. ⚡

```
Bounding Function Admissibility & Pruning Topology:

Maximization Objective (Knapsack):
- Current Best Profit P* = 80

Node A: Fractional Bound u_hat(A) = 92  ──► 92 > 80: PROMISING! Keep in Priority Queue! ✅
Node B: Fractional Bound u_hat(B) = 75  ──► 75 <= 80: UNPROMISING! KILLED IMMEDIATELY! ❌

Admissibility guarantees no valid solution with profit > 80 is hidden in Node B! ⚡
```

---

## 2. Core Concepts & Relaxation Techniques Strategy Matrix

### 2.1 Problem Relaxation Strategies Matrix
```
Problem Relaxation Strategies Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Domain        | Original Problem  | Relaxation Method | Bounding Operator | Computation Speed |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **0/1 Knapsack**      | Discrete $x_i \in \{0,1\}$| Continuous Fractional| **Upper Bound $\hat{u}(x)$⚡**| **$O(N \log N)$ ⚡**|
| **Job Assignment**    | Cost Permutation  | Row/Col Min Reduction| **Lower Bound $\hat{l}(x)$⚡**| **$O(N^2)$ Matrix ⚡**|
| **Traveling Salesperson**| Integer Cycle   | Reduced Matrix / 1-Tree| **Lower Bound $\hat{l}(x)$⚡**| **$O(N^2)$ Matrix ⚡**|
| **Integer Programming**| Integer Domain   | Linear Programming (LP)| **Dual Bound $\hat{b}(x)$⚡**| $O(\text{Simplex})$ |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Upper Bound u_hat >= true profit for Maximization; Lower Bound l_hat <= true cost for Minimization! Admissibility prevents false pruning!"**

---

## 3. Characteristics & Bounding Monotonicity Mathematical Proof

### 3.1 Mathematical Proof of Monotonic Bounding
* Let $x$ be a parent node at depth $k$, and $y$ be a child node of $x$ at depth $k+1$.
* In a minimization problem, child node $y$ fixes additional decision variables (e.g. assigning a job to a specific worker), restricting the remaining search space:
  $$\text{Subtree}(y) \subset \text{Subtree}(x)$$
* Because the candidate solution set for $y$ is a strict subset of the candidate solution set for $x$, the minimum cost over $\text{Subtree}(y)$ cannot be smaller than the minimum cost over $\text{Subtree}(x)$:
  $$\min_{S \in \text{Subtree}(y)} f(S) \ge \min_{S \in \text{Subtree}(x)} f(S)$$
* An admissible lower bounding function $\hat{l}$ reflects this set inclusion:
  $$\hat{l}(x) \le \hat{l}(y) \le \dots \le f(S_{\text{leaf}})$$
* **Pruning Guarantee**:
  - If $\hat{l}(x) \ge C^*$, then for all descendants $y$ of $x$, $\hat{l}(y) \ge \hat{l}(x) \ge C^*$.
  - Therefore, killing node $x$ safely eliminates all its descendant nodes $y$ simultaneously! ⚡

---

## 4. Internal Working Mechanics: Row-Column Matrix Reduction Lower Bound

Tracing Row-Column Reduction Lower Bound for $3 \times 3$ Cost Matrix:

```
Original Cost Matrix:
[ 9,  2,  7 ]
[ 6,  4,  3 ]
[ 5,  8,  1 ]

Step 1: Row Reduction (Subtract row minimum from each element):
- Row 0 min = 2 ──► [7, 0, 5]
- Row 1 min = 3 ──► [3, 1, 0]
- Row 2 min = 1 ──► [4, 7, 0]
Row Reduction Sum = 2 + 3 + 1 = 6.

Step 2: Column Reduction on Reduced Matrix (Subtract col minimum):
- Col 0 min = 3 ──► [4, 0, 5], [0, 1, 0], [1, 7, 0]
- Col 1 min = 0
- Col 2 min = 0
Column Reduction Sum = 3 + 0 + 0 = 3.

Total Root Lower Bound l_hat(Root) = RowSum + ColSum = 6 + 3 = 9!
No assignment solution can cost less than 9! ✅ ⚡
```

---

## 5. Visual Diagram: Monotonic Bounding Tree Progression

```
Monotonic Lower Bound Progression in Minimization Tree:

                 [ Root: l_hat = 9 ]
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
[ Child A: l_hat = 12 ]         [ Child B: l_hat = 15 ]
         │                               │
[ Leaf A1: Cost = 14 ]          [ Leaf B1: Cost = 15 (C* Updated!) ]

Lower bounds increase monotonically (9 <= 12 <= 14)! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Matrix Reduction Lower Bounding (Assignment Problem) and Fractional Knapsack Upper Bounding engines.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Bounding Functions:
 * Matrix Reduction Lower Bounds, Fractional Relaxation Upper Bounds, and Monotonicity Checks.
 */
public class BoundingFunctionsMaster {

    // =========================================================================
    // 1. MATRIX REDUCTION LOWER BOUND CALCULATOR (ASSIGNMENT / TSP)
    // =========================================================================
    /**
     * Computes the initial Row-Column Reduction Lower Bound for a Cost Matrix.
     *
     * @param costMatrix N x N cost matrix
     * @return lower bound sum
     */
    public int calculateMatrixReductionLowerBound(int[][] costMatrix) {
        if (costMatrix == null || costMatrix.length == 0) return 0;
        int n = costMatrix.length;

        int[][] matrix = new int[n][n];
        for (int r = 0; r < n; r++) matrix[r] = costMatrix[r].clone();

        int totalReductionCost = 0;

        // Step 1: Row Reduction
        for (int r = 0; r < n; r++) {
            int rowMin = Integer.MAX_VALUE;
            for (int c = 0; c < n; c++) {
                if (matrix[r][c] < rowMin) rowMin = matrix[r][c];
            }
            if (rowMin > 0 && rowMin != Integer.MAX_VALUE) {
                totalReductionCost += rowMin;
                for (int c = 0; c < n; c++) matrix[r][c] -= rowMin;
            }
        }

        // Step 2: Column Reduction
        for (int c = 0; c < n; c++) {
            int colMin = Integer.MAX_VALUE;
            for (int r = 0; r < n; r++) {
                if (matrix[r][c] < colMin) colMin = matrix[r][c];
            }
            if (colMin > 0 && colMin != Integer.MAX_VALUE) {
                totalReductionCost += colMin;
                for (int r = 0; r < n; r++) matrix[r][c] -= colMin;
            }
        }

        return totalReductionCost; // Admissible Lower Bound l_hat! ⚡
    }

    // =========================================================================
    // 2. FRACTIONAL KNAPSACK UPPER BOUND CALCULATOR
    // =========================================================================
    public double calculateKnapsackUpperBound(int capacity, int currentWeight, int currentProfit, int level, int[] weights, int[] values) {
        if (currentWeight >= capacity) return 0;

        double bound = currentProfit;
        int remainingCapacity = capacity - currentWeight;
        int n = weights.length;

        for (int i = level; i < n; i++) {
            if (weights[i] <= remainingCapacity) {
                remainingCapacity -= weights[i];
                bound += values[i];
            } else {
                bound += values[i] * ((double) remainingCapacity / weights[i]); // Continuous LP Relaxation! ⚡
                break;
            }
        }

        return bound; // Admissible Upper Bound u_hat! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Row Reduction Line
int rowMin = Arrays.stream(matrix[r]).min().getAsInt(); totalReductionCost += rowMin;
```

---

## 7. Concrete Problem Examples & Applications

1. **Matrix Reduction Lower Bound**:
   - Primary lower bound engine for Job Assignment Problem and TSP ($O(N^2)$ time).

2. **Fractional Knapsack Relaxation**:
   - Primary upper bound engine for 0/1 Knapsack Branch & Bound ($O(N)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class BoundingFunctionsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   BOUNDING FUNCTIONS BENCHMARK DEMO            ");
        System.out.println("=================================================\n");

        BoundingFunctionsMaster master = new BoundingFunctionsMaster();

        // 1. Matrix Reduction Test
        int[][] costMatrix = {
            {9, 2, 7},
            {6, 4, 3},
            {5, 8, 1}
        };

        int lowerBound = master.calculateMatrixReductionLowerBound(costMatrix);
        System.out.println("1. Matrix Reduction Lower Bound Calculation:");
        System.out.println("   Admissible Lower Bound (l_hat): " + lowerBound + " (Optimal = 9)");
        System.out.println("-------------------------------------------------");

        // 2. Knapsack Upper Bound Test
        int capacity = 10, weight = 4, profit = 40;
        int[] weights = {4, 7, 53};
        int[] values = {40, 42, 25};

        double upperBound = master.calculateKnapsackUpperBound(capacity, weight, profit, 1, weights, values);
        System.out.println("2. Fractional Knapsack Relaxation Upper Bound:");
        System.out.println("   Admissible Upper Bound (u_hat): " + upperBound + " (Optimal = 76.0)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Bounding Function | Target Problem | Time Complexity | Auxiliary Space | Bound Type |
| :--- | :--- | :--- | :--- | :--- |
| **Matrix Reduction** | Job Assignment / TSP | $\mathbf{O(N^2)}$ Matrix ⚡| $O(N^2)$ Matrix Space| Lower Bound $\hat{l}(x)$ |
| **Fractional Knapsack** | 0/1 Knapsack | $\mathbf{O(N)}$ Linear ⚡| $O(1)$ Memory Space | Upper Bound $\hat{u}(x)$ |

---

## 10. Edge Cases & Boundary Handling

1. **Matrix Row/Col Minimum is Zero**:
   - If row or column already contains a 0, reduction cost is 0.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Violating the Admissibility Property (Over-estimating Lower Bounds)**:
  - Constructing a lower bound that exceeds true minimal costs causes Branch & Bound to falsely prune subtrees containing optimal solutions. **ALWAYS ensure $\hat{l}(x) \le \text{True Optimal}$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Admissibility Definition:
> * **Lower Bound $\hat{l}(x)$**: MUST satisfy $\hat{l}(x) \le f(S^*)$ (Never overestimates cost).
> * **Upper Bound $\hat{u}(x)$**: MUST satisfy $\hat{u}(x) \ge f(S^*)$ (Never underestimates profit). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Tight Bound (LP Simplex) | Loose Bound (Matrix Reduction) |
| :--- | :--- | :--- |
| **Pruning Power** | High (Prunes more nodes) | Moderate |
| **Computation Speed** | Slow per node | **Very Fast per node ⚡** |
| **Ideal Application** | Hard Integer Programs | **Job Assignment / TSP ⚡** |

---

## 14. How to Recognize This in Questions

* **"Construct an admissible lower bound for assignment cost matrix"** $\rightarrow$ Matrix Reduction Bounding.

---

## 15. Frequently Asked Interview Questions

* **Q: What is an Admissible Bounding Function?**  
  *A:* A bounding function that never overestimates the minimum cost (in minimization) or underestimates the maximum profit (in maximization), guaranteeing that optimal solutions are never falsely pruned.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: BOUNDING FUNCTIONS                                    |
+-----------------------------------------------------------------------+
| • Lower Bound : l_hat(x) <= True Optimal Cost (Minimization)          |
| • Upper Bound : u_hat(x) >= True Optimal Profit (Maximization)        |
| • Matrix Red  : Subtract row/col minimums -> Sum = Initial Lower Bound|
| • Monotonicity: Bounds become tighter deeper in state space tree      |
| • Performance : Fast bounds enable millions of pruned nodes! ⚡        |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can define the Admissibility property for lower and upper bounds.
- [ ] I can calculate Row-Column Matrix Reduction lower bounds in Java.
- [ ] I can calculate Fractional Knapsack upper bounds in Java.
- [ ] I can explain the monotonicity property of bounding functions.
- [ ] I can state the trade-off between tight bounds and computation speed.
