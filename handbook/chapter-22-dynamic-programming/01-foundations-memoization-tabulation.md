# 01. Dynamic Programming Foundations: Optimal Substructure, Overlapping Subproblems & Memoization vs Tabulation

## 1. Introduction
**Dynamic Programming (DP)** is an optimization paradigm that solves complex problems by breaking them down into simpler **Overlapping Subproblems** and storing intermediate sub-results to eliminate redundant calculations. Grounded in Richard Bellman's **Principle of Optimality**, DP applies to any optimization or counting problem exhibiting **Optimal Substructure** (an optimal solution to the problem contains optimal solutions to its subproblems). DP can be executed via two primary approaches: **Top-Down Memoization (Recursion + Caching)** and **Bottom-Up Tabulation (Iterative Table Filling)**.

> **Important:** The 2 Core Prerequisites & 2 Implementation Modes of DP:
> 1. **Optimal Substructure**: The overall optimal solution can be constructed from optimal solutions of its subproblems.
> 2. **Overlapping Subproblems**: The same subproblems are solved repeatedly across different branching paths.
> 3. **Top-Down Memoization**: Recursive traversal with a cache array `memo[]` or `memo[][]` (solves ONLY required subproblems, but incurs recursion call stack overhead).
> 4. **Bottom-Up Tabulation**: Iterative loop filling a `dp[]` table in topological dependency order (eliminates call stack overhead and enables $O(1)$ space optimizations!). ⚡

```
Dynamic Programming Top-Down vs Bottom-Up Pipeline Topology:
Top-Down (Memoization):      fib(5) -> fib(4) -> fib(3) -> Cache Hit! Return memo[3] ⚡
Bottom-Up (Tabulation):      dp[0]=0 -> dp[1]=1 -> dp[2]=1 -> dp[3]=2 -> dp[4]=3 -> dp[5]=5 ⚡
```

---

## 2. Core Concepts & Memoization vs Tabulation Comparison

### 2.1 Top-Down vs Bottom-Up Strategy Matrix
```
Top-Down Memoization vs Bottom-Up Tabulation Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | Top-Down Memoization| Bottom-Up Tabulation| Space-Optimized DP|
+-----------------------+-------------------+-------------------+-------------------+
| **Control Flow**      | Recursion + Cache | Iterative Loops   | $O(1)$ Variables  |
| **Call Stack Memory** | $O(N)$ Recursion  | **Zero Stack ⚡** | **Zero Stack ⚡** |
| **Subproblem Solving**| Evaluates as needed| Evaluates all DP  | Evaluates all DP  |
| **Space Optimization**| Difficult         | **Easy ($O(1)$) ⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Top-Down = Recursion + memo[] cache! Bottom-Up = Iterative dp[] table loop!"**

---

## 3. Characteristics & Time Complexity Reduction Proof

### 3.1 Mathematical Proof of $O(2^N) \to O(N)$ Complexity Reduction
* Un-memoized Fibonacci recursion tree generates $2^N$ nodes, executing in **$O(2^N)$ Exponential Time**.
* With DP, there are only $N$ unique subproblems ($fib(0) \dots fib(N)$).
* Each subproblem is evaluated ONCE and stored in `memo[]` or `dp[]` in $O(1)$ time.
* Total Time Complexity: $N \times O(1) = \mathbf{O(N) \text{ Linear Time}}$! ⚡

---

## 4. Internal Working Mechanics
Tracing Fibonacci DP Transformation from $O(2^N)$ down to $O(N)$ and $O(1)$ Space:

```
Naive Recursion: fib(5) calls fib(4) and fib(3); fib(4) calls fib(3) and fib(2)... fib(3) calculated 2x!

Top-Down Memoization (memo array size 6):
- Call fib(5): memo[5] unvisited -> Call fib(4).
- Call fib(4): memo[4] unvisited -> Call fib(3).
- Call fib(3): memo[3] unvisited -> Returns 2, stores memo[3] = 2.
- Back to fib(4): Calls fib(2) -> Returns 1. Stores memo[4] = 3.
- Back to fib(5): Calls fib(3) -> CACHE HIT! Returns memo[3] (2) in O(1) time!
- Result: 3 + 2 = 5!

Bottom-Up Tabulation:
- Initialize dp = [0, 1, 0, 0, 0, 0].
- Loop i = 2..5: dp[i] = dp[i-1] + dp[i-2].

Space-Optimized Iterative: prev2 = 0, prev1 = 1 -> curr = 1 -> curr = 2 -> curr = 3 -> curr = 5! ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
Overlapping Subproblems Recursion Tree vs Memoized DAG Topography:

```
Naive Exponential Tree:                    Memoized DAG:
          fib(5)                                fib(5)
         /      \                               /     \
    fib(4)      fib(3)                       fib(4) ---> fib(3)
    /    \       /   \                        /           /
 fib(3) fib(2) fib(2) fib(1)               fib(2) -------> fib(1)
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing Top-Down Memoization, Bottom-Up Tabulation, and $O(1)$ Space-Optimized DP:

```java
import java.util.*;

public class DPFoundationsMaster {

    // 1. Top-Down Memoization O(N) Time, O(N) Stack + Cache Space
    public int fibMemo(int n) {
        if (n <= 0) return 0;
        int[] memo = new int[n + 1];
        Arrays.fill(memo, -1); // -1 represents unvisited subproblems
        return fibMemoHelper(n, memo);
    }

    private int fibMemoHelper(int n, int[] memo) {
        if (n <= 0) return 0;
        if (n == 1) return 1;

        // Step 1: Cache Hit Check
        if (memo[n] != -1) {
            return memo[n];
        }

        // Step 2: Compute & Store in Cache
        memo[n] = fibMemoHelper(n - 1, memo) + fibMemoHelper(n - 2, memo);
        return memo[n];
    }

    // 2. Bottom-Up Tabulation O(N) Time, O(N) DP Table Space
    public int fibTabulation(int n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;

        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;

        for (int i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }

        return dp[n];
    }

    // 3. Space-Optimized DP O(N) Time, O(1) Auxiliary Space
    public int fibSpaceOptimized(int n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;

        int prev2 = 0;
        int prev1 = 1;

        for (int i = 2; i <= n; i++) {
            int curr = prev1 + prev2;
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
}
```

> **Quick Syntax:**
```java
// Memoization Cache Check & Store Line
if (memo[n] != -1) return memo[n];
return memo[n] = helper(n - 1) + helper(n - 2);
```

---

## 7. Concrete Problem Examples
* **LeetCode 70 - Climbing Stairs**: Basic 1D DP tabulation.
* **LeetCode 509 - Fibonacci Number**: Primary DP demonstration.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing Memoization, Tabulation, and $O(1)$ Space DP:

```java
public class DPFoundationsDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. DP Foundations Test ===");
        DPFoundationsMaster solver = new DPFoundationsMaster();

        int n = 10;
        System.out.println("Top-Down Memoization (10):  " + solver.fibMemo(n));
        System.out.println("Bottom-Up Tabulation (10):  " + solver.fibTabulation(n));
        System.out.println("Space-Optimized DP (10):    " + solver.fibSpaceOptimized(n));
        // All produce 55! Space-optimized uses O(1) space! ✅
    }
}
```

---

## 9. Complexity Analysis

| DP Implementation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Top-Down Memoization**| **$O(N)$ Linear ⚡** | $O(N)$ Cache + Stack | Cache check `memo[n] != -1` |
| **Bottom-Up Tabulation**| **$O(N)$ Linear ⚡** | $O(N)$ Table Space | Iterative loop `dp[i] = ...` |
| **Space-Optimized DP**  | **$O(N)$ Linear ⚡** | **$O(1)$ Constant Space ⚡**| State variables (`prev1`, `prev2`) |

---

## 10. Edge Cases & Boundary Handling
* **$N = 0$ or $N = 1$**: Handled by initial base case guards.
* **Large $N \ge 47$**: 32-bit signed integer overflow requires `long` or modulo `10^9 + 7`.

---

## 11. Common Mistakes & Anti-Patterns
* **Forgetting to Initialize Memo Cache Array (`Arrays.fill(memo, -1)`)**:
  - Leaving `memo[]` initialized to default `0` causes valid subproblem results of `0` to be treated as unvisited, destroying memoization!
  - **ALWAYS fill `memo[]` with a sentinel value like `-1`**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Top-Down Memoization vs Bottom-Up Tabulation Selection Rule:
> * Use **Top-Down Memoization** when only a small fraction of the total state space needs to be computed (memoization skips unreached states).
> * Use **Bottom-Up Tabulation** when all states must be computed anyway, or when optimizing space from $O(N)$ down to **$O(1)$ space**! ⚡

> **Memory Trick:** **"Top-Down skips unneeded states! Bottom-Up allows O(1) space optimization!"**

---

## 13. System & Implementation Comparisons

| Feature | Top-Down Memoization | Bottom-Up Tabulation |
| :--- | :--- | :--- |
| **State Dependencies** | Solved implicitly via recursion | Solved explicitly in topological order |
| **Call Stack Memory** | $O(N)$ Recursion Stack | **Zero Call Stack Memory ⚡** |
| **Space Optimization**| Not Possible | **Easy ($O(1)$ Variables) ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find max/min value or total ways with repeating sub-choices"** $\rightarrow$ Dynamic Programming.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the Principle of Optimality in Dynamic Programming?**  
  *A:* The property stating that an optimal sequence of decisions has the property that whatever the initial state and decision are, the remaining decisions must constitute an optimal decision sequence.
* **Q: Why does Tabulation eliminate call stack overhead?**  
  *A:* Because Tabulation uses iterative `for` loops instead of recursive function calls.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: DP FOUNDATIONS                                        |
+-----------------------------------------------------------------------+
| • Prerequisites  : Optimal Substructure + Overlapping Subproblems     |
| • Top-Down       : Recursion + Cache (if (memo[n] != -1) return memo[n];)|
| • Bottom-Up      : Iterative loop filling dp[] table in order         |
| • Space Opt      : Replace dp[N] array with prev1, prev2 variables    |
| • Performance    : Reduces exponential O(2^N) to linear O(N) time! ⚡  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write Top-Down Memoization with `-1` cache initialization.
- [ ] I can write Bottom-Up Tabulation for 1D DP.
- [ ] I can optimize 1D DP space from $O(N)$ to $O(1)$.
- [ ] I can state the Principle of Optimality.
- [ ] I can trace DP subproblem execution step by step.
