# 02. Recursion to DP: Systematic 4-Step Transformation & Space Reduction

## 1. Introduction
The journey from a **Naive Recursive Brute-Force Solution** to an **Optimal $O(1)$ Space Dynamic Programming Solution** is a core technical competency evaluated in algorithmic engineering. While naive recursion builds an exponential decision tree ($O(2^N)$ or $O(3^N)$ time) due to repeated evaluation of overlapping subproblems, systematic DP transformation refines the solution across 4 distinct evolutionary phases: (1) **Naive Backtracking Recursion**, (2) **Top-Down Memoization** (caching recursive states in $O(N)$ time), (3) **Bottom-Up Tabulation** (eliminating call stack overhead via iterative arrays), and (4) **Space-Optimized DP** (reducing memory footprint from $O(N)$ down to **$O(1)$ Constant Space**).

> **Important:** The 4 Evolutionary Phases of Recursion-to-DP Transformation:
> 1. **Phase 1: Naive Recursive Solution**:
>    - Express problem as a pure recursive function $f(\text{state})$. Exponential time $O(2^N)$ due to duplicate call branches.
> 2. **Phase 2: Top-Down Memoized Solution**:
>    - Add a memoization array/table `memo[state]`. Return cached result if `memo[state] != UNVISITED`. Reduces time to $O(N)$.
> 3. **Phase 3: Bottom-Up Tabulated Solution**:
>    - Invert control flow into an iterative loop. Populate `dp[state]` array in topological order. Eliminates $O(N)$ recursion call stack!
> 4. **Phase 4: Space-Optimized DP Solution**:
>    - Identify state dependency distance $K$. Replace the full $O(N)$ DP array with $K$ primitive variables, achieving **$O(1)$ Auxiliary Space**! ⚡

```
The 4-Phase Transformation Pipeline (House Robber Example):

Phase 1: Naive Recursion ──► rob(i) = max(nums[i] + rob(i-2), rob(i-1))  [O(2^N) Time, O(N) Stack]
                                 │
                                 ▼ Add Memoization Array
Phase 2: Top-Down Memo   ──► if (memo[i] != -1) return memo[i];          [O(N) Time, O(N) Space]
                                 │
                                 ▼ Convert to Iterative Loop
Phase 3: Bottom-Up Tab   ──► dp[i] = max(nums[i] + dp[i-2], dp[i-1])      [O(N) Time, O(N) Space]
                                 │
                                 ▼ Replace Array with 2 Variables
Phase 4: O(1) Space Opt  ──► curr = max(nums[i] + prev2, prev1)          [O(N) Time, O(1) Space!] ⚡
```

---

## 2. Core Concepts & Transformation Strategy Matrix

### 2.1 Transformation Phases Strategy Matrix
```
Transformation Phases Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Transformation Phase  | Control Flow      | Call Stack Cost   | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. Naive Recursion**| Top-Down Call Tree| $O(N)$ Stack Depth| $O(2^N)$ Exponential| $O(N)$ Stack      |
| **2. Top-Down Memo**  | Top-Down Caching  | $O(N)$ Stack Depth| **$O(N)$ Linear ⚡**| $O(N)$ Memo + Stack|
| **3. Bottom-Up Tab**  | Bottom-Up Iterative| **$O(0)$ Zero Stack⚡**| **$O(N)$ Linear ⚡**| $O(N)$ DP Array   |
| **4. Space-Optimized**| Bottom-Up Sliding | **$O(0)$ Zero Stack⚡**| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Phase 1: Naive Recursion -> Phase 2: Add Memo Array -> Phase 3: Iterative DP Array -> Phase 4: O(1) Variable Shift!"**

---

## 3. Characteristics & Step-by-Step Code Transformation Mechanics

### 3.1 Step-by-Step Transformation Walkthrough (House Robber - LeetCode 198)

```
Phase 1: Naive Recursion (O(2^N) Time):
public int rob(int[] nums, int i) {
    if (i < 0) return 0;
    return Math.max(nums[i] + rob(nums, i - 2), rob(nums, i - 1));
}

Phase 2: Add Top-Down Memoization (O(N) Time, O(N) Space):
public int robMemo(int[] nums, int i, int[] memo) {
    if (i < 0) return 0;
    if (memo[i] != -1) return memo[i]; // Return memoized cache!
    memo[i] = Math.max(nums[i] + robMemo(nums, i - 2, memo), robMemo(nums, i - 1, memo));
    return memo[i];
}

Phase 3: Convert to Bottom-Up Tabulation (O(N) Time, O(N) Space):
public int robTab(int[] nums) {
    if (nums.length == 0) return 0;
    int[] dp = new int[nums.length + 1];
    dp[0] = 0;
    dp[1] = nums[0];
    for (int i = 1; i < nums.length; i++) {
        dp[i + 1] = Math.max(nums[i] + dp[i - 1], dp[i]);
    }
    return dp[nums.length];
}

Phase 4: Space Optimization (O(N) Time, O(1) Space!):
public int robOptimized(int[] nums) {
    int prev2 = 0, prev1 = 0;
    for (int num : nums) {
        int curr = Math.max(num + prev2, prev1);
        prev2 = prev1;
        prev1 = curr;
    }
    return prev1;
}
```

---

## 4. Internal Working Mechanics: State Dependency & Sliding Window Compression

Why Space Optimization works for 1D and 2D DP problems:

```
State Dependence Distance Analysis:

If State DP[i] depends ONLY on:
- DP[i-1] and DP[i-2] ──► Requires 2 Primitive Variables (prev1, prev2) -> O(1) Space!
- DP[i-1], DP[i-2] ... DP[i-K] ──► Requires Ring Buffer array of size K -> O(K) Space!

For 2D Grid DP (DP[i][j] depends on DP[i-1][j] and DP[i][j-1]):
- Depends only on previous row (i-1) ──► Compress 2D Array DP[N][M] to 1D Array DP[M]! ⚡
```

---

## 5. Visual Diagram: 4-Phase Transformation Pipeline

```
Visual State Evolution:

[ Naive Call Tree (Exponential) ] ──► Add Caching ──► [ Memoization Array ]
                                                              │
                                                      Invert Control Flow
                                                              │
                                                              ▼
[ O(1) Space Variables ] ◄── Strip Array ──► [ Tabulation Loop Array ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing all 4 transformation phases for LeetCode 198 (House Robber) and LeetCode 213 (House Robber II - Circular Array).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating the 4-Phase Transformation Pipeline:
 * Naive Recursion -> Memoization -> Tabulation -> O(1) Space Optimization.
 */
public class RecursionToDPMaster {

    // =========================================================================
    // 1. LEETCODE 198: HOUSE ROBBER (ALL 4 TRANSFORMATION PHASES)
    // =========================================================================

    // Phase 1: Naive Recursion (O(2^N) Time, O(N) Stack)
    public int robPhase1_Naive(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        return robNaiveHelper(nums, nums.length - 1);
    }

    private int robNaiveHelper(int[] nums, int i) {
        if (i < 0) return 0;
        return Math.max(nums[i] + robNaiveHelper(nums, i - 2), robNaiveHelper(nums, i - 1));
    }

    // Phase 2: Top-Down Memoization (O(N) Time, O(N) Space)
    public int robPhase2_Memo(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int[] memo = new int[nums.length];
        Arrays.fill(memo, -1);
        return robMemoHelper(nums, nums.length - 1, memo);
    }

    private int robMemoHelper(int[] nums, int i, int[] memo) {
        if (i < 0) return 0;
        if (memo[i] != -1) return memo[i]; // Cache return! ⚡

        memo[i] = Math.max(nums[i] + robMemoHelper(nums, i - 2, memo), 
                           robMemoHelper(nums, i - 1, memo));
        return memo[i];
    }

    // Phase 3: Bottom-Up Tabulation (O(N) Time, O(N) Space)
    public int robPhase3_Tabulation(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        int n = nums.length;
        if (n == 1) return nums[0];

        int[] dp = new int[n];
        dp[0] = nums[0];
        dp[1] = Math.max(nums[0], nums[1]);

        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(nums[i] + dp[i - 2], dp[i - 1]);
        }

        return dp[n - 1];
    }

    // Phase 4: Space-Optimized DP (O(N) Time, O(1) Auxiliary Space)
    public int robPhase4_SpaceOptimized(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int prev2 = 0;
        int prev1 = 0;

        for (int num : nums) {
            int curr = Math.max(num + prev2, prev1);
            prev2 = prev1;
            prev1 = curr; // Shift sliding window variables! ⚡
        }

        return prev1;
    }

    // =========================================================================
    // 2. LEETCODE 213: HOUSE ROBBER II (CIRCULAR ARRAY O(N) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves House Robber II where first and last houses are connected circularly.
     * Splitted into 2 linear subproblems: rob(0 ... N-2) vs rob(1 ... N-1).
     */
    public int robCircular(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];

        // Case 1: Rob houses 0 to N-2 (Exclude last house)
        int max1 = robRangeOptimized(nums, 0, nums.length - 2);
        // Case 2: Rob houses 1 to N-1 (Exclude first house)
        int max2 = robRangeOptimized(nums, 1, nums.length - 1);

        return Math.max(max1, max2);
    }

    private int robRangeOptimized(int[] nums, int start, int end) {
        int prev2 = 0;
        int prev1 = 0;

        for (int i = start; i <= end; i++) {
            int curr = Math.max(nums[i] + prev2, prev1);
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
}
```

> **Quick Syntax:**
```java
// House Robber Space Optimization Line
int curr = Math.max(num + prev2, prev1); prev2 = prev1; prev1 = curr;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 198 - House Robber**:
   - Standard 4-phase transformation benchmark ($O(N)$ time, $O(1)$ space).

2. **LeetCode 213 - House Robber II**:
   - Circular array DP reduced to 2 linear subproblems ($O(N)$ time, $O(1)$ space).

3. **LeetCode 746 - Min Cost Climbing Stairs**:
   - Transforming min cost recursion into space-optimized DP.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class RecursionToDPDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   RECURSION TO DP TRANSFORMATION DEMO           ");
        System.out.println("=================================================\n");

        RecursionToDPMaster master = new RecursionToDPMaster();

        int[] houses = {2, 7, 9, 3, 1};

        System.out.println("1. House Robber Test Array: [2, 7, 9, 3, 1]");

        int p1 = master.robPhase1_Naive(houses);
        int p2 = master.robPhase2_Memo(houses);
        int p3 = master.robPhase3_Tabulation(houses);
        int p4 = master.robPhase4_SpaceOptimized(houses);

        System.out.println("   Phase 1 (Naive Recursion) : Max Loot = " + p1);
        System.out.println("   Phase 2 (Top-Down Memo)   : Max Loot = " + p2);
        System.out.println("   Phase 3 (Bottom-Up Tab)   : Max Loot = " + p3);
        System.out.println("   Phase 4 (O(1) Space Opt)  : Max Loot = " + p4);
        System.out.println("   All 4 Phases Match        : " + (p1 == p2 && p2 == p3 && p3 == p4));
        System.out.println("-------------------------------------------------");

        // House Robber II Circular Test
        int[] circularHouses = {2, 3, 2};
        int maxCircular = master.robCircular(circularHouses);
        System.out.println("2. House Robber II (Circular Array) Test for [2, 3, 2]:");
        System.out.println("   Max Loot (O(1) Space): " + maxCircular + " (Optimal)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Phase | Time Complexity | Auxiliary Memory | Call Stack Overhead | Conversion Difficulty |
| :--- | :--- | :--- | :--- | :--- |
| **1. Naive Recursion**| $O(2^N)$ Exponential ❌| $O(N)$ Stack Depth | Heavy $O(N)$ Stack | Natural Baseline |
| **2. Top-Down Memo**  | $\mathbf{O(N)}$ Linear ⚡| $O(N)$ Memo + Stack | Heavy $O(N)$ Stack | Add Memo Array |
| **3. Bottom-Up Tab**   | $\mathbf{O(N)}$ Linear ⚡| $O(N)$ DP Array | **Zero $O(0)$ Stack ⚡**| Invert Loop Flow |
| **4. Space-Optimized** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| **Zero $O(0)$ Stack ⚡**| Replace Array with Vars |

---

## 10. Edge Cases & Boundary Handling

1. **Array Length 1 or 2**:
   - `robCircular` handles $N=1$ explicitly (`return nums[0];`).

2. **Negative Values in Inputs**:
   - Handled cleanly via base initialization `prev2 = 0, prev1 = 0`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Jumping Straight to Space Optimization Without Writing Recurrence First**:
  - Attempting $O(1)$ variable shifts without deriving the state transition equation causes variable assignment bugs. ALWAYS write Phase 2/3 first!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Golden Rule of DP Space Optimization:
> If $DP[i]$ depends only on $DP[i-1]$ and $DP[i-2]$, replace the full array with two variables (`prev1`, `prev2`) to achieve **$O(1)$ Auxiliary Space**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Phase 2 (Memoization) | Phase 3 (Tabulation) | Phase 4 (Space Opt) |
| :--- | :--- | :--- | :--- |
| **Recursion Stack** | Present ($O(N)$) | **None ($O(0)$) ⚡** | **None ($O(0)$) ⚡** |
| **Memory Table** | $O(N)$ Memo Array | $O(N)$ DP Array | **$O(1)$ Variables ⚡** |
| **Code Length** | ~15 Lines | ~10 Lines | **~6 Lines ⚡** |

---

## 14. How to Recognize This in Questions

* **"Maximize profit picking non-adjacent elements in array"** $\rightarrow$ House Robber (LeetCode 198).
* **"Maximize profit in circular array where first and last collide"** $\rightarrow$ House Robber II (LeetCode 213).

---

## 15. Frequently Asked Interview Questions

* **Q: Why is Tabulation preferred over Memoization in production systems?**  
  *A:* Because Tabulation uses iterative loops, eliminating function call overhead and risking no `StackOverflowError` on large $N$.

* **Q: How does House Robber II solve the circular array constraint?**  
  *A:* By running two separate linear DP passes: one excluding the last house (`0 ... N-2`) and one excluding the first house (`1 ... N-1`), taking the maximum of both.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: RECURSION TO DP TRANSFORMATION                        |
+-----------------------------------------------------------------------+
| • Phase 1: Naive Recursion (O(2^N) Time, O(N) Stack)                  |
| • Phase 2: Top-Down Memo (Add memo[] array -> O(N) Time, O(N) Space)  |
| • Phase 3: Bottom-Up Tabulation (Invert loop -> O(N) Time, O(N) Space)|
| • Phase 4: Space Optimization (Use prev1, prev2 -> O(N) Time, O(1) Space)⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write all 4 transformation phases for House Robber (LeetCode 198) in Java.
- [ ] I can solve House Robber II (LeetCode 213) in $O(1)$ space.
- [ ] I can explain why space optimization reduces memory to $O(1)$.
- [ ] I can state the difference between Memoization and Tabulation.
- [ ] I can convert any top-down memoized DP solution to bottom-up tabulation.
