# 02. 1D Dynamic Programming: House Robber, Climbing Stairs & Circular DP Patterns

## 1. Introduction
**1D Dynamic Programming** is the foundational pattern where the state of the problem at index $i$ depends strictly on a constant number of previous linear subproblem states (typically $i-1$ and $i-2$). Classic benchmark problems include **Climbing Stairs (LeetCode 70)**, **Min Cost Climbing Stairs (LeetCode 746)**, **House Robber (LeetCode 198)**, and **House Robber II (LeetCode 213 - Circular Array)**. Solved via $O(N)$ tabulation and $O(1)$ state variable rolling, 1D DP executes in **$O(N)$ Linear Time** and **$O(1)$ Auxiliary Space**.

> **Important:** Core Invariants of 1D DP & Circular Array Splitting:
> 1. **House Robber I State Transition (LeetCode 198)**:
>    - At house $i$, the robber has 2 options:
>      - Option 1: Skip house $i \implies \text{maxRobbed} = \text{dp}[i-1]$.
>      - Option 2: Rob house $i \implies \text{maxRobbed} = \text{dp}[i-2] + \text{nums}[i]$.
>      $$\text{dp}[i] = \max(\text{dp}[i-1], \, \text{dp}[i-2] + \text{nums}[i])$$
> 2. **House Robber II Circular Array Split (LeetCode 213)**:
>    - First and last houses are adjacent! Robbing house $0$ forbids robbing house $N-1$.
>    - Solution: Split into 2 standard 1D linear subproblems and return the maximum:
>      $$\text{ans} = \max(\text{robLinear}(0 \dots N-2), \, \text{robLinear}(1 \dots N-1))$$
> 3. **$O(1)$ Rolling Variables**: Replace array `dp[N]` with two state variables `prev1` and `prev2`! ⚡

```
House Robber 1D State Transition Topology:
House Index i:                   [ House i-2 ]     [ House i-1 ]     [ House i ]
Option 1 (Skip House i):                           [ dp[i-1]   ] -----------------> dp[i]
Option 2 (Rob House i) :         [ dp[i-2]   ] + [ nums[i]   ] -----------------> dp[i]

dp[i] = max(dp[i-1], dp[i-2] + nums[i]) ⚡
```

---

## 2. Core Concepts & 1D DP Problem Pattern Strategy Matrix

### 2.1 1D DP Strategy Matrix
```
1D DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Variant       | DP State Recurrence| Base Cases       | Space Optimization|
+-----------------------+-------------------+-------------------+-------------------+
| **Climbing Stairs(70)**| `dp[i] = dp[i-1] + dp[i-2]`| `dp[1]=1, dp[2]=2`| **$O(1)$ Space ⚡**|
| **House Robber (198)**| `max(dp[i-1], dp[i-2] + val)`| `dp[0]=val[0]`| **$O(1)$ Space ⚡**|
| **House Robber II(213)**| 2 Line Scans ($0..N-2$, $1..N-1$)| Split Ranges | **$O(1)$ Space ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"House Robber II: First & last adjacent? Run standard 1D Robber on (0..N-2) and (1..N-1), return max!"**

---

## 3. Characteristics & $O(1)$ Space Optimization Proof

### 3.1 Mathematical Proof of $O(1)$ Space Optimization
* The recurrence `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` depends ONLY on the immediately preceding 2 values (`dp[i-1]` and `dp[i-2]`).
* Values prior to `dp[i-2]` are never referenced again.
* Replacing `dp[]` array with `prev2` and `prev1` maintains full state continuity while using **$O(1)$ Auxiliary Space**! ⚡

---

## 4. Internal Working Mechanics
Tracing House Robber I on Array `nums = [2, 7, 9, 3, 1]`:

```
Init: prev2 = 0, prev1 = 0.

House 0 (val 2): curr = max(0, 0 + 2) = 2. Update: prev2 = 0, prev1 = 2.
House 1 (val 7): curr = max(2, 0 + 7) = 7. Update: prev2 = 2, prev1 = 7.
House 2 (val 9): curr = max(7, 2 + 9) = 11. Update: prev2 = 7, prev1 = 11.
House 3 (val 3): curr = max(11, 7 + 3) = 11. Update: prev2 = 11, prev1 = 11.
House 4 (val 1): curr = max(11, 11 + 1) = 12. Update: prev2 = 11, prev1 = 12.

Maximum Robbed Amount = 12! ✅ (O(N) Time, O(1) Space!)
```

---

## 5. Visual Diagram
1D DP Rolling Variable State Machine Topography:

```
Step i:     [ prev2 ] ------ [ prev1 ] ------ [ curr = max(prev1, prev2 + val) ]
               |                |                     |
Shift Next:    +--- prev2       +--- prev1            +--- Next Iteration ⚡
```

---

## 6. Operations & Complete Java Implementation
Production-grade Java suite implementing LeetCode 198 (House Robber) and LeetCode 213 (House Robber II):

```java
import java.util.*;

// LeetCode 198 & 213: House Robber I & II Master Class
public class HouseRobberMaster {

    // 1. LeetCode 198: House Robber I (Linear Array) O(N) Time, O(1) Space
    public int rob(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];

        int prev2 = 0;
        int prev1 = 0;

        for (int num : nums) {
            int curr = Math.max(prev1, prev2 + num);
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }

    // 2. LeetCode 213: House Robber II (Circular Array) O(N) Time, O(1) Space
    public int robCircular(int[] nums) {
        if (nums == null || nums.length == 0) return 0;
        if (nums.length == 1) return nums[0];
        if (nums.length == 2) return Math.max(nums[0], nums[1]);

        int n = nums.length;

        // Subproblem 1: Rob houses from index 0 to N-2 (Excludes last house N-1)
        int option1 = robLinearRange(nums, 0, n - 2);

        // Subproblem 2: Rob houses from index 1 to N-1 (Excludes first house 0)
        int option2 = robLinearRange(nums, 1, n - 1);

        return Math.max(option1, option2);
    }

    // Helper: Linear House Robber for Range [start ... end] O(N) Time, O(1) Space
    private int robLinearRange(int[] nums, int start, int end) {
        int prev2 = 0;
        int prev1 = 0;

        for (int i = start; i <= end; i++) {
            int curr = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = curr;
        }

        return prev1;
    }
}
```

> **Quick Syntax:**
```java
// House Robber 1D Rolling State Line
int curr = Math.max(prev1, prev2 + num); prev2 = prev1; prev1 = curr;
```

---

## 7. Concrete Problem Examples
* **LeetCode 198 - House Robber**: Basic 1D linear DP.
* **LeetCode 213 - House Robber II**: Circular array split 1D DP.
* **LeetCode 746 - Min Cost Climbing Stairs**: Cost-based 1D DP.

---

## 8. Java Code Demonstration & Dry Run
Demonstration testing LeetCode 213 `robCircular`:

```java
public class HouseRobberDemo {

    public static void main(String[] args) {
        System.out.println("=== 1. LeetCode 213 House Robber II Test ===");
        HouseRobberMaster solver = new HouseRobberMaster();

        int[] nums1 = {2, 3, 2};
        System.out.println("Max Robbed [2, 3, 2]: " + solver.robCircular(nums1)); // Output: 3

        int[] nums2 = {1, 2, 3, 1};
        System.out.println("Max Robbed [1, 2, 3, 1]: " + solver.robCircular(nums2)); // Output: 4 ✅
    }
}
```

---

## 9. Complexity Analysis

| Problem Variant | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **House Robber I (198)**| **$O(N)$ Linear ⚡** | **$O(1)$ Constant Space ⚡**| Rolling variables `prev1`, `prev2` |
| **House Robber II (213)**| **$O(N)$ Linear ⚡** | **$O(1)$ Constant Space ⚡**| 2 Range scans ($0..N-2$, $1..N-1$) |

---

## 10. Edge Cases & Boundary Handling
* **$N = 1$ Single House**: Returns `nums[0]` directly.
* **$N = 2$ Two Houses**: Returns `Math.max(nums[0], nums[1])`.

---

## 11. Common Mistakes & Anti-Patterns
* **Attempting to Solve Circular DP (LeetCode 213) in a Single Pass**:
  - A single pass cannot enforce that house 0 and house $N-1$ are not both robbed without storing an extra boolean flag that doubles the state space.
  - **ALWAYS split circular array DP into 2 separate linear passes (`0..N-2` and `1..N-1`)**.

---

## 12. Important Notes & Architectural Rules

> **Interview Reminder:** Why Splitting Circular Arrays into 2 Linear Ranges Is Optimal:
> A circular array constraint (first and last items cannot be selected together) breaks down into 2 mutually exclusive cases:
> Case 1: First item is included $\implies$ Last item MUST be excluded (Range $0 \dots N-2$).
> Case 2: First item is excluded $\implies$ Last item CAN be included (Range $1 \dots N-1$).
> Evaluating both linear cases and taking the maximum solves any circular DP problem in $O(N)$ time! ⚡

> **Memory Trick:** **"Circular array DP = Case 1 (0..N-2) vs Case 2 (1..N-1)!"**

---

## 13. System & Implementation Comparisons

| Feature | 1D DP Array (`dp[N]`) | Rolling Variables (`prev1, prev2`) |
| :--- | :--- | :--- |
| **Auxiliary Space** | $O(N)$ Array Space | **$O(1)$ Constant Space ⚡** |
| **Time Complexity** | **$O(N)$ Linear ⚡** | **$O(N)$ Linear ⚡** |
| **Code Length** | ~15 Lines | **~8 Lines Clean Code ⚡** |

---

## 14. How to Recognize This in Questions
* **"Find maximum value by picking non-adjacent elements in linear or circular array"** $\rightarrow$ LeetCode 198 / 213.

---

## 15. Frequently Asked Interview Questions
* **Q: What is the recurrence relation for House Robber I?**  
  *A:* $\text{dp}[i] = \max(\text{dp}[i-1], \, \text{dp}[i-2] + \text{nums}[i])$.
* **Q: How does House Robber II handle the circular constraint?**  
  *A:* By running linear House Robber twice: once on range $0 \dots N-2$ and once on range $1 \dots N-1$, taking the maximum of both.

---

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: 1D DYNAMIC PROGRAMMING (HOUSE ROBBER)                 |
+-----------------------------------------------------------------------+
| • Recurrence : curr = Math.max(prev1, prev2 + val);                   |
| • Shift State: prev2 = prev1; prev1 = curr;                           |
| • Circular DP: robCircular(nums) = max(rob(0..N-2), rob(1..N-1))     |
| • Performance: O(N) Linear Time | O(1) Auxiliary Space ⚡             |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist
- [ ] I can write LeetCode 198 (`House Robber I`) in $O(1)$ space.
- [ ] I can write LeetCode 213 (`House Robber II`) using range splitting.
- [ ] I can write LeetCode 746 (`Min Cost Climbing Stairs`).
- [ ] I know why circular array DP splits into 2 linear passes.
- [ ] I can trace rolling variable state shifts step by step.
