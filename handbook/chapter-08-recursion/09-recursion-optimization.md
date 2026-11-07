# 09. Recursion Optimization: Memoization, Pruning, Bitmasking & Trampolining

## 1. Introduction
**Recursion Optimization** encompasses a suite of systematic engineering techniques designed to transform naive, inefficient, exponential-time ($O(2^N)$) recursive functions into optimal, stack-safe, production-ready algorithms. While naive recursion often suffers from redundant call stack re-evaluations and memory exhaustion, applying **Top-Down Memoization (Caching)**, **Constraint Pruning**, **Bitmask State Compression**, and **Iterative Loop / Trampoline Transformation** reduces time complexity down to **$O(N)$** or **$O(N \cdot K)$** and stack memory down to **$O(1)$**.

> **Important:** The 4 Pillars of Recursion Optimization:
> 1. **Top-Down Memoization (Caching)**: Store subproblem answers in a lookup table (`memo[]` / `Map`) upon first computation, turning exponential execution trees into linear DAGs ($O(2^N) \to O(N)$).
> 2. **Constraint Branch Pruning**: Evaluate boundary conditions *before* spawning recursive calls, cutting off thousands of hopeless search branches early.
> 3. **Bitmask State Compression**: Represent boolean sets as primitive integers (`int mask`) for instant $O(1)$ state lookups and zero heap allocation.
> 4. **Tail Accumulator / Trampolining**: Convert non-tail operations into tail calls or iterative `while` loops to guarantee $O(1)$ stack memory. ⚡

```
Recursion Optimization Pipeline Topology:
Naive Exponential Tree:        [ fib(5) ] ---> Spawns 15 Calls (Redundant!)
Memoized State Graph:          [ fib(5) ] ---> Cache Hit on fib(3)! -> Spawns 5 Calls (O(N) Time!) ⚡
```

---

## 2. Core Concepts & Optimization Techniques Strategy Matrix

### 2.1 Optimization Taxonomy Matrix
```
Recursion Optimization Techniques Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Optimization Strategy | Target Bottleneck | Complexity Impact | Memory Impact     |
+-----------------------+-------------------+-------------------+-------------------+
| **Memoization Cache** | Redundant Subcalls| **$O(2^N) \to O(N)$ ⚡**| Adds $O(N)$ Table  |
| **Branch Pruning**    | Search Tree Size  | Exponential Cut   | **Saves Stack ⚡** |
| **Bitmasking State**  | Object Allocation | Faster Constants  | **$O(1)$ State ⚡**|
| **Iterative Loop**    | Stack Overflow    | Same Time         | **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Memoization eliminates redundant subcalls; Pruning cuts invalid branches early; Bitmasking replaces object sets!"**

---

## 3. Characteristics & Memoization $O(2^N) \to O(N)$ Reduction Proof

### 3.1 Mathematical Proof of Memoization Speedup
* Consider Fibonacci $F(N) = F(N-1) + F(N-2)$.
* Un-memoized recursion tree has size:
  $$S(N) = S(N-1) + S(N-2) + 1 \implies \mathbf{O(2^N) \text{ Nodes}}$$
* With memoization, each state $k \in [0 \dots N]$ is evaluated **EXACTLY ONCE**. Subsequent requests for $F(k)$ return from `memo[k]` in $O(1)$ time.
* Total Time Complexity: $\mathbf{O(N) \text{ Linear Time}}$. Total Space: $\mathbf{O(N) \text{ Cache Array}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Memoized Subset Sum

Tracing Memoized Subset Sum on Array `[3, 34, 4, 12, 5, 2]`, Target = `9`:

```
Memo Table: memo[index][remainingTarget] initialized to -1 (Unvisited).

Call solve(index = 0, target = 9):
- Item 0 (val 3):
  - Option 1: Include 3 -> Recurse solve(index = 1, target = 6):
    - Item 1 (val 34): 34 > 6 -> Pruned!
    - Item 2 (val 4): Include 4 -> Recurse solve(index = 3, target = 2):
      - Item 3 (val 12): 12 > 2 -> Pruned!
      - Item 4 (val 5): 5 > 2 -> Pruned!
      - Item 5 (val 2): Include 2 -> Recurse solve(index = 6, target = 0):
        - Target == 0! BASE CASE MET! Returns true!

Unwinding Phase:
- Stores memo[3][2] = 1 (true), memo[1][6] = 1 (true), memo[0][9] = 1 (true).

Subsequent calls for remaining target 2 or 6 hit memo cache in O(1) time! ✅ (O(N * Target) Time!)
```

---

## 5. Visual Diagram: Unoptimized Tree vs. Memoized DAG

```
1. Un-memoized Call Tree (Redundant Computations):
                     solve(0, 9)
                    /           \
           solve(1, 6)         solve(1, 9)
          /           \         /          \
     solve(2, 2)  solve(2, 6) solve(2, 5)  solve(2, 9)
      /      \
  solve(3,0) ... (Duplicate subproblems evaluated repeatedly!)

2. Memoized Call Graph (Subproblem Answers Reused):
                     solve(0, 9)
                    /           \
           solve(1, 6)         solve(1, 9)
          /           \            │
     solve(2, 2)  solve(2, 6) ─────┘ (Cache Hit! Returns memo[2][5] in O(1)!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Memoization, Branch Pruning, Bitmask State Compression, and Iterative Loop Conversion.

```java
import java.util.*;

/**
 * Production-Grade Suite Implementing Recursion Optimization Techniques:
 * Memoization Caching, Constraint Pruning, Bitmasking, and Iterative Conversions.
 */
public class RecursionOptimizationMaster {

    // =========================================================================
    // 1. TOP-DOWN MEMOIZATION (Subproblem Caching O(N * Target))
    // =========================================================================
    /**
     * Solves Subset Sum Target search using Top-Down Memoization.
     * Reduces complexity from O(2^N) to O(N * Target).
     *
     * @param arr positive integer array
     * @param target sum target
     * @return true if subset exists
     */
    public boolean subsetSumMemo(int[] arr, int target) {
        if (arr == null || target < 0) return false;

        int n = arr.length;
        // memo[index][target]: -1 = unvisited, 0 = false, 1 = true
        int[][] memo = new int[n + 1][target + 1];
        for (int[] row : memo) Arrays.fill(row, -1);

        return memoHelper(arr, 0, target, memo);
    }

    private boolean memoHelper(int[] arr, int index, int target, int[][] memo) {
        // Base Case Guards
        if (target == 0) return true;
        if (index >= arr.length || target < 0) return false;

        // Step 1: Cache Hit Check
        if (memo[index][target] != -1) {
            return memo[index][target] == 1;
        }

        // Step 2: Branch Pruning & Subproblem Evaluation
        boolean include = false;
        if (arr[index] <= target) { // Pruning guard!
            include = memoHelper(arr, index + 1, target - arr[index], memo);
        }

        boolean exclude = memoHelper(arr, index + 1, target, memo);
        boolean result = include || exclude;

        // Step 3: Cache Store
        memo[index][target] = result ? 1 : 0;
        return result;
    }

    // =========================================================================
    // 2. BITMASK STATE COMPRESSION (O(1) Set Operations)
    // =========================================================================
    /**
     * Solves Traveling Salesperson Problem (TSP) / Path State Search using Bitmask DP.
     * Replaces HashSet<Integer> with a primitive 32-bit integer mask.
     *
     * @param n total number of cities (N <= 20)
     * @param dist 2D distance matrix
     * @return minimum path cost visiting all cities
     */
    public int tspBitmask(int n, int[][] dist) {
        if (n <= 0 || dist == null) return 0;

        int finalState = (1 << n) - 1; // All n bits set to 1
        int[][] memo = new int[n][1 << n];
        for (int[] row : memo) Arrays.fill(row, -1);

        return tspHelper(0, 1, n, finalState, dist, memo); // Start at city 0 with mask 1
    }

    private int tspHelper(int u, int mask, int n, int finalState, int[][] dist, int[][] memo) {
        // Base Case: All cities visited
        if (mask == finalState) {
            return dist[u][0]; // Return to origin city 0
        }

        if (memo[u][mask] != -1) return memo[u][mask];

        int minCost = 1000000000;

        for (int v = 0; v < n; v++) {
            // Bitmask Guard: Check if city v has NOT been visited yet ((mask & (1 << v)) == 0)
            if ((mask & (1 << v)) == 0) {
                int newMask = mask | (1 << v); // Set bit v
                int cost = dist[u][v] + tspHelper(v, newMask, n, finalState, dist, memo);
                minCost = Math.min(minCost, cost);
            }
        }

        return memo[u][mask] = minCost;
    }

    // =========================================================================
    // 3. ITERATIVE CONVERSION (Stack-Safe O(1) Memory Execution)
    // =========================================================================
    /**
     * Converts a tail-recursive function to a stack-safe iterative loop.
     * Eliminates call stack memory consumption completely.
     */
    public long tailToIterativeGCD(long a, long b) {
        while (b != 0) {
            long temp = b;
            b = a % b; // Subproblem reduction
            a = temp;  // State update
        }
        return a;
    }
}
```

> **Quick Syntax:**
```java
// Bitmask Check & Set Lines
boolean isVisited = (mask & (1 << v)) != 0;
int nextMask = mask | (1 << v); // Set bit v
```

---

## 7. Concrete Problem Examples & Applications

1. **Top-Down Memoization**:
   - Longest Common Subsequence (LCS): $O(M \cdot N)$ memo table.
   - Coin Change Problem: $O(N \cdot \text{Amount})$ memo table.

2. **Branch Pruning**:
   - Alpha-Beta Pruning in Minimax Game Search (Chess / Tic-Tac-Toe).
   - N-Queens Constraint Checks.

3. **Bitmasking State Compression**:
   - Shortest Path Visiting All Nodes (LeetCode 847).
   - Traveling Salesperson Problem ($O(N^2 \cdot 2^N)$).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class RecursionOptimizationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   RECURSION OPTIMIZATION & SPEEDUP DEMO         ");
        System.out.println("=================================================\n");

        RecursionOptimizationMaster master = new RecursionOptimizationMaster();

        // 1. Memoized Subset Sum Test
        int[] set = {3, 34, 4, 12, 5, 2};
        int target = 9;
        boolean memoResult = master.subsetSumMemo(set, target);
        System.out.println("1. Memoized Subset Sum (Target = " + target + "): " + memoResult);
        System.out.println("-------------------------------------------------");

        // 2. Bitmask TSP Test (4 Cities)
        int n = 4;
        int[][] dist = {
            {0, 10, 15, 20},
            {10, 0, 35, 25},
            {15, 35, 0, 30},
            {20, 25, 30, 0}
        };
        int minTspCost = master.tspBitmask(n, dist);
        System.out.println("2. Bitmask TSP Min Tour Cost (4 Cities): " + minTspCost);
        System.out.println("-------------------------------------------------");

        // 3. Iterative Stack-Safe GCD Test
        long a = 48, b = 18;
        long gcdVal = master.tailToIterativeGCD(a, b);
        System.out.println("3. Stack-Safe Iterative GCD(" + a + ", " + b + "): " + gcdVal);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Optimization Technique | Time Complexity (Before) | Time Complexity (After) | Auxiliary Space Impact | Primary Benefit |
| :--- | :--- | :--- | :--- | :--- |
| **Top-Down Memoization**| $\mathbf{O(2^N)}$ Exponential | $\mathbf{O(N \cdot K)}$ Polynomial ⚡| Adds $O(N \cdot K)$ Table | Eliminates Redundancy |
| **Branch Pruning** | $\mathbf{O(M^N)}$ Full Tree | $\mathbf{O(M^K)}$ Pruned ($K \ll N$)| Saves Stack Memory | Cuts Invalid Branches |
| **Bitmasking State** | $O(N \cdot 2^N \cdot \text{SetOps})$| $\mathbf{O(N \cdot 2^N)}$ (Fast Bitwise)⚡| $\mathbf{O(1)}$ Primitive Mask | 100x Memory Speedup |
| **Iterative Loop** | $O(N)$ Call Stack Depth| $O(N)$ Execution | $\mathbf{O(1)}$ Zero Stack ⚡| Immune to StackOverflow|

---

## 10. Edge Cases & Boundary Handling

1. **Unvisited Sentinel Values in Memo Tables**:
   - Always initialize `memo[]` with a sentinel value like `-1` (or `null` for objects). If valid results can be `0` or negative, initializing `memo[]` to `0` destroys caching.

2. **Bitmask Shift Overflow (`N >= 32`)**:
   - `1 << N` overflows signed 32-bit `int` when $N \ge 32$.
   - **Fix**: Use `1L << N` for up to 64 state bits.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Memoizing Mutable Parameters Without Encoding**:
  - Attempting to use a mutable `List<Integer>` directly as a Map cache key creates heavy object hashing overhead and breaks when list elements are modified.

* **Anti-Pattern 2: Late Pruning (Pruning After Deep Calls)**:
  - Performing constraint checks *inside* the child frame instead of *before* calling the child frame wastes stack frame allocation overhead.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Golden Rule of Top-Down Memoization Setup:
> 1. Formulate the naive recursive solution first and verify correctness.
> 2. Identify the changing state parameters (e.g. `index` and `remainingTarget`).
> 3. Create a lookup cache table `memo[maxIndex][maxTarget]` sized to cover all valid state parameter ranges.
> 4. Insert cache lookup check at the top of the function and cache store before returning. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive Recursion | Top-Down Memoization | Bottom-Up Tabulation |
| :--- | :--- | :--- | :--- |
| **Time Bounds** | $O(2^N)$ Exponential | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Space Bounds** | $O(N)$ Stack | $O(N)$ Stack + Cache | **$O(1)$ Space (Optimized) ⚡**|
| **Ease of Discovery** | High | **High (Direct Wrap) ⚡** | Moderate (Loop order required)|

---

## 14. How to Recognize This in Questions

* **"Naive recursive solution takes exponential time due to repeating subproblems"** $\rightarrow$ Memoization.
* **"State involves tracking set of up to 20 visited elements"** $\rightarrow$ Bitmask DP.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the difference between Top-Down Memoization and Bottom-Up Tabulation?**  
  *A:* Memoization solves subproblems recursively on-demand (top-down) and caches results. Tabulation builds subproblem answers iteratively in topological dependency order (bottom-up), enabling $O(1)$ space optimizations.

* **Q: How does Bitmasking replace set data structures in recursion?**  
  *A:* A primitive integer represents a set of up to 32 elements. The $i$-th bit being 1 means element $i$ is included in the set. Checking membership is `(mask & (1 << i)) != 0`, and adding element $i$ is `mask | (1 << i)`.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RECURSION OPTIMIZATION                                |
+-----------------------------------------------------------------------+
| • Memoization : Cache subproblem results -> O(2^N) to O(N) speedup!   |
| • Memo Rule   : Init memo table with sentinel -1; check memo[i][j] != -1|
| • Early Pruning: Check candidate validity BEFORE making self-call     |
| • Bitmasking  : (mask & (1 << i)) == 0 (Unvisited); mask | (1 << i) (Set)|
| • Loop Opt    : Convert tail recursion to while loop for O(1) stack! ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can apply Top-Down Memoization to an exponential recursive function.
- [ ] I can initialize memoization tables with safe sentinel values like `-1`.
- [ ] I can write bitmask state checks (`mask & (1 << i)`) and bitwise updates (`mask | (1 << i)`).
- [ ] I can implement early branch pruning before making recursive calls.
- [ ] I can convert a tail-recursive function into an $O(1)$ space iterative loop.
