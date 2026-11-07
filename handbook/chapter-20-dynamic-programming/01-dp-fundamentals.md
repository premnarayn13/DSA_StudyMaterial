# 01. DP Fundamentals: Overlapping Subproblems, State Transitions & Space Invariants

## 1. Introduction
**Dynamic Programming (DP)** is a powerful algorithmic paradigm introduced by Richard Bellman in 1953. Designed to solve complex optimization, counting, and decision problems, Dynamic Programming breaks a problem down into a collection of simpler subproblems, solves each subproblem **EXACTLY ONCE**, and stores its answer in a memory table (memoization array or tabulation table). By eliminating the redundant exponential re-computations of naive recursion, Dynamic Programming reduces time complexities from **Exponential $O(2^N)$ down to Polynomial Bounds $O(N)$, $O(N^2)$, or $O(N \cdot W)$**. To apply Dynamic Programming, a problem MUST satisfy two strict mathematical invariants: **Overlapping Subproblems** and **Optimal Substructure**.

> **Important:** The 4 Structural Invariants of Dynamic Programming:
> 1. **Overlapping Subproblems Invariant**:
>    - The recursive search space repeatedly evaluates the EXACT SAME subproblems over identical parameter inputs.
> 2. **Optimal Substructure Invariant**:
>    - An optimal solution to the problem of size $N$ can be constructed directly from optimal solutions to its smaller subproblems.
> 3. **State Space Definition ($DP[\text{state}]$)**:
>    - A minimal tuple of variables (e.g. `dp[i]`, `dp[i][w]`, `dp[mask]`) that uniquely identifies a subproblem state.
> 4. **State Transition Recurrence Equation**:
>    - A mathematical formula defining how state $DP[\text{state}]$ is computed from previously solved smaller states (e.g. $DP[i] = DP[i-1] + DP[i-2]$). ⚡

```
Dynamic Programming State Graph Topology (Fibonacci Overlapping Subproblems):

                             fib(5)
                           /        \
                    fib(4)           fib(3) ──► OVERLAP! (Re-computed in Naive Recursion!)
                   /      \          /     \
              fib(3)     fib(2)   fib(2)  fib(1)
             /      \
        fib(2)     fib(1)

Naive Recursion: O(2^N) Exponential Duplicate Computations ❌
DP Memoization / Tabulation: Solves fib(3) and fib(2) EXACTLY ONCE -> O(N) Linear Time! ✅ ⚡
```

---

## 2. Core Concepts & DP vs Other Paradigms Strategy Matrix

### 2.1 Algorithmic Paradigms Comparison Matrix
```
Algorithmic Paradigms Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Paradigm              | Subproblem Choice | Memoization Table?| Backtracking?     | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Dynamic Programming**| **Evaluates All ⚡**| **REQUIRED (Table)⚡**| Never             | **Polynomial $O(N^k)$⚡**|
| **Greedy Paradigm**   | 1 Local Best      | Not Needed        | Never             | $O(N \log N)$     |
| **Divide & Conquer**  | Disjoint Splits   | Not Needed        | Never             | $O(N \log N)$     |
| **Backtracking**      | Exhaustive Search | Not Needed        | **ALWAYS ⚡**      | Exponential $O(2^N)$|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"DP stores subproblem answers in a table to avoid duplicate work! Requires Overlapping Subproblems & Optimal Substructure!"**

---

## 3. Characteristics & Mathematical Complexity Proofs

### 3.1 Mathematical Proof of $O(N)$ DP Time vs $O(2^N)$ Naive Recursion
* Consider computing $Fib(N)$ defined by $F_N = F_{N-1} + F_{N-2}$ with base cases $F_0 = 0, F_1 = 1$.
* **Naive Recursion Analysis**:
  - Tree depth $= N$. Number of leaf nodes in call tree $T(N) = T(N-1) + T(N-2) + 1 \approx \Phi^N = \left(\frac{1 + \sqrt{5}}{2}\right)^N \approx 1.618^N$.
  - Time Complexity: $\mathbf{O(2^N) \text{ Exponential Time}}$.
* **Dynamic Programming Analysis**:
  - Distinct states to compute: $N + 1$ states ($0, 1, 2 \dots N$).
  - Computation time per state $DP[i] = DP[i-1] + DP[i-2]$: $O(1)$ constant addition.
  - Total DP Time Complexity: $\mathbf{O(N) \text{ Strict Linear Time}}$.
  - Speedup Factor for $N = 50$: Naive $\approx 10^{10}$ operations vs DP $\approx 50$ operations ($200,000,000\times$ FASTER!). ⚡

---

## 4. Internal Working Mechanics: The 5-Step DP Formulation Framework

Every Dynamic Programming problem can be systematically solved using the **5-Step DP Framework**:

```
The 5-Step DP Formulation Framework:

Step 1: Define the DP State
        Identify state parameters. (e.g. dp[i] = Min cost to reach step i).

Step 2: Formulate the State Transition Equation
        Express dp[state] in terms of smaller states.
        (e.g. dp[i] = cost[i] + min(dp[i-1], dp[i-2])).

Step 3: Identify Base Cases & Boundaries
        Set initial values for smallest subproblems. (e.g. dp[0] = cost[0], dp[1] = cost[1]).

Step 4: Determine Evaluation Topological Order
        Decide iteration direction (Left-to-Right 0..N, or Right-to-Left N..0).

Step 5: Optimize Auxiliary Space Footprint
        If state depends only on previous K values, compress space from O(N) to O(1)! ⚡
```

---

## 5. Visual Diagram: DP State Transition & Space Compression

```
State Dependence Pipeline for Climbing Stairs / Fibonacci:

Full Array DP (O(N) Space):
[ dp[0] ] ──► [ dp[1] ] ──► [ dp[2] ] ──► ... ──► [ dp[N] ]

Space-Compressed DP (O(1) Memory):
[ prev2 ] ──► [ prev1 ] ──► [ curr = prev1 + prev2 ]
  (Shift: prev2 = prev1, prev1 = curr for next iteration!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing DP Fundamentals across Fibonacci (LeetCode 509), Climbing Stairs (LeetCode 70), and Min Cost Climbing Stairs (LeetCode 746) using Memoization, Tabulation, and $O(1)$ Space Compression.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing DP Fundamentals,
 * 5-Step State Formulation, Memoization, Tabulation, and O(1) Space Compression.
 */
public class DPFundamentalsMaster {

    // =========================================================================
    // 1. LEETCODE 70: CLIMBING STAIRS (3 Approaches: Memo, Tab, O(1) Space)
    // =========================================================================
    
    // Approach A: Top-Down Memoization (O(N) Time, O(N) Space)
    public int climbStairsMemo(int n) {
        if (n <= 2) return n;
        int[] memo = new int[n + 1];
        Arrays.fill(memo, -1);
        return climbStairsMemoHelper(n, memo);
    }

    private int climbStairsMemoHelper(int n, int[] memo) {
        if (n <= 2) return n;
        if (memo[n] != -1) return memo[n]; // Return cached result! ⚡

        memo[n] = climbStairsMemoHelper(n - 1, memo) + climbStairsMemoHelper(n - 2, memo);
        return memo[n];
    }

    // Approach B: Bottom-Up Tabulation (O(N) Time, O(N) Space)
    public int climbStairsTabulation(int n) {
        if (n <= 2) return n;

        int[] dp = new int[n + 1];
        dp[1] = 1;
        dp[2] = 2;

        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2]; // State transition!
        }

        return dp[n];
    }

    // Approach C: Space-Optimized DP (O(N) Time, O(1) Auxiliary Space)
    public int climbStairsSpaceOptimized(int n) {
        if (n <= 2) return n;

        int prev2 = 1;
        int prev1 = 2;

        for (int i = 3; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // =========================================================================
    // 2. LEETCODE 746: MIN COST CLIMBING STAIRS (O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Finds minimum cost to reach top of floor.
     * State Transition: dp[i] = cost[i] + min(dp[i-1], dp[i-2]).
     */
    public int minCostClimbingStairs(int[] cost) {
        if (cost == null || cost.length == 0) return 0;
        int n = cost.length;

        int prev2 = cost[0];
        int prev1 = cost[1];

        for (int i = 2; i < n; i++) {
            int curr = cost[i] + Math.min(prev1, prev2);
            prev2 = prev1;
            prev1 = curr;
        }

        return Math.min(prev1, prev2); // Top can be reached from n-1 or n-2! ⚡
    }
}
```

> **Quick Syntax:**
```java
// Space Optimization Variable Shift Lines
int curr = prev1 + prev2; prev2 = prev1; prev1 = curr;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 70 - Climbing Stairs**:
   - Fundamental DP state transition ($dp[i] = dp[i-1] + dp[i-2]$).

2. **LeetCode 746 - Min Cost Climbing Stairs**:
   - Min cost path with choice of 1 or 2 steps ($O(1)$ space).

3. **LeetCode 509 - Fibonacci Number**:
   - Benchmark problem comparing $O(2^N)$ naive recursion vs $O(N)$ DP vs $O(\log N)$ Matrix Exponentiation.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class DPFundamentalsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   DYNAMIC PROGRAMMING FUNDAMENTALS DEMO        ");
        System.out.println("=================================================\n");

        DPFundamentalsMaster master = new DPFundamentalsMaster();

        // 1. LeetCode 70 Climbing Stairs Test
        int n = 10;
        int memoAns = master.climbStairsMemo(n);
        int tabAns = master.climbStairsTabulation(n);
        int optAns = master.climbStairsSpaceOptimized(n);

        System.out.println("1. Climbing Stairs for N = " + n + " Steps:");
        System.out.println("   Memoization Result     : " + memoAns + " Ways");
        System.out.println("   Tabulation Result      : " + tabAns + " Ways");
        System.out.println("   O(1) Space Opt Result  : " + optAns + " Ways");
        System.out.println("   All Approaches Match   : " + (memoAns == tabAns && tabAns == optAns));
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 746 Min Cost Climbing Stairs Test
        int[] cost = {10, 15, 20};
        int minCost = master.minCostClimbingStairs(cost);
        System.out.println("2. Min Cost Climbing Stairs for Cost = [10, 15, 20]:");
        System.out.println("   Minimum Total Cost: " + minCost + " (Optimal)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| DP Approach | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Naive Recursion** | $O(2^N)$ Exponential ❌| $O(N)$ Stack Depth | Duplicate computations |
| **Top-Down Memo**  | $\mathbf{O(N)}$ Linear ⚡| $O(N)$ Array + Stack | Cache array lookup |
| **Bottom-Up Tab**   | $\mathbf{O(N)}$ Linear ⚡| $O(N)$ DP Array | Iterative loop |
| **Space-Optimized** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| 2 State variables |

---

## 10. Edge Cases & Boundary Handling

1. **Smallest N Boundaries ($N=0, 1, 2$)**:
   - Handled directly in base case checks (`if (n <= 2) return n;`).

2. **32-Bit Integer Overflow in Large DP Sums**:
   - Use `long` or modulo arithmetic ($10^9 + 7$) when DP values exceed `Integer.MAX_VALUE`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting to Fill Memoization Array with Sentinel Values**:
  - Failing to initialize `memo` with `-1` causes valid computed 0 results to be re-evaluated repeatedly.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Top-Down Memoization vs Bottom-Up Tabulation:
> * **Top-Down (Memoization)**: Recursive, solves subproblems lazily on demand. Uses call stack.
> * **Bottom-Up (Tabulation)**: Iterative, solves all subproblems systematically in topological order. Prevents StackOverflow! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Top-Down Memoization | Bottom-Up Tabulation | Space-Optimized DP |
| :--- | :--- | :--- | :--- |
| **Execution Model** | Recursive | Iterative | Iterative |
| **Subproblem Order**| Lazy / On-Demand | Strict Topological | Strict Topological |
| **Auxiliary Memory**| $O(N)$ Memo + Stack | $O(N)$ Array | **$O(1)$ Memory ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count total number of ways to reach target N"** $\rightarrow$ DP Addition ($dp[i] = dp[i-1] + dp[i-2]$).
* **"Find minimum/maximum cost to achieve goal"** $\rightarrow$ DP Min/Max ($dp[i] = \text{cost} + \min(dp[i-1], dp[i-2])$).

---

## 15. Frequently Asked Interview Questions

* **Q: What are the two necessary conditions for Dynamic Programming?**  
  *A:* Overlapping Subproblems and Optimal Substructure.

* **Q: How do you optimize DP space from $O(N)$ to $O(1)$?**  
  *A:* By recognizing that computing state $DP[i]$ depends only on a fixed number of previous states (e.g. $DP[i-1]$ and $DP[i-2]$), allowing us to replace the full DP array with variables.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: DYNAMIC PROGRAMMING FUNDAMENTALS                      |
+-----------------------------------------------------------------------+
| • 2 Requirements : Overlapping Subproblems & Optimal Substructure     |
| • 5-Step Method  : State -> Recurrence -> Base Case -> Order -> Space Opt|
| • Space Opt Rule : Replace DP array with variables if dp[i] uses dp[i-1..k]|
| • Speedup        : Reduces O(2^N) exponential time to O(N) linear time!⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can state the 2 requirements for Dynamic Programming.
- [ ] I can write the 5-Step DP Formulation Framework.
- [ ] I can write Climbing Stairs (LeetCode 70) in Top-Down, Bottom-Up, and $O(1)$ Space.
- [ ] I can solve LeetCode 746 (`Min Cost Climbing Stairs`).
- [ ] I can explain why DP reduces $O(2^N)$ naive recursion to $O(N)$ linear time.
