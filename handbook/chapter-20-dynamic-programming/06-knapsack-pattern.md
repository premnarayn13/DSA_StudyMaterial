# 06. Knapsack Pattern: 0/1 Choice States, Reverse 1D Space Compression & Variations

## 1. Introduction
The **0/1 Knapsack Pattern** is arguably the most ubiquitous dynamic programming design pattern in algorithmic computer science. Given $N$ indivisible items, where each item $i$ has a value $v_i$ and a weight $w_i$, and a knapsack of capacity $W$, the goal is to choose a subset of items ($x_i \in \{0, 1\}$) to maximize total value without exceeding capacity $W$. The 0/1 Knapsack pattern serves as the architectural foundation for numerous variation benchmarks, including **Partition Equal Subset Sum (LeetCode 416)**, **Target Sum (LeetCode 494)**, **Last Stone Weight II (LeetCode 1049)**, and **Subset Sum**. A critical optimization in 0/1 Knapsack is **Right-to-Left (Reverse) 1D Space Compression**, which reduces memory from a 2D table $DP[N+1][W+1]$ down to a single **1D Array $DP[W+1]$** executing in **$O(N \cdot W)$ Pseudo-Polynomial Time Complexity** and **$O(W)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of the 0/1 Knapsack Pattern:
> 1. **2D Recurrence Equation**:
>    - For item $i$ (weight $w_i$, value $v_i$) and capacity $w$:
>      $$DP[i][w] = \begin{cases} \max\left( v_i + DP[i-1][w - w_i], \, DP[i-1][w] \right) & \text{if } w_i \le w \\ DP[i-1][w] & \text{otherwise} \end{cases}$$
> 2. **Right-to-Left (Reverse) 1D Space Compression Invariant**:
>    - When compressing 2D DP to 1D Array $DP[w]$, capacity $w$ MUST be iterated **BACKWARDS (Right-to-Left from $W$ down to $w_i$)**:
>      $$DP[w] = \max\left( v_i + DP[w - w_i], \, DP[w] \right)$$
>    - Why Reverse? Iterating backwards ensures $DP[w - w_i]$ represents the state from the PREVIOUS item $i-1$, preventing item $i$ from being used multiple times in the same step!
> 3. **Target Sum Algebraic Reduction Invariant (LeetCode 494)**:
>    - Splitting elements into positive set $P$ and negative set $N$:
>      $$\text{Sum}(P) - \text{Sum}(N) = \text{Target} \quad \implies \quad \text{Sum}(P) = \frac{\text{TotalSum} + \text{Target}}{2}$$
>    - Reduces Target Sum directly to a Subset Sum 0/1 Knapsack problem! ⚡

```
0/1 Knapsack 1D Reverse Loop Traversal Topology:

Capacity Array DP[w]:   [ 0 | 1 | 2 | ... | w - w_i | ... | W ]
                                                 ▲           │
                                                 └─ Reads PREVIOUS item state (Unmodified!)
                                                    Iterates Right-to-Left (W down to w_i)! ⚡

Forward Loop (w_i to W) ──► UNBOUNDED KNAPSACK (Multi-use item) ❌
Reverse Loop (W down to w_i) ──► 0/1 KNAPSACK (Single-use item) ✅ ⚡
```

---

## 2. Core Concepts & 0/1 Knapsack Pattern Strategy Matrix

### 2.1 Knapsack Variations Comparison Matrix
```
0/1 Knapsack Variations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Variation Problem     | Target Capacity $W$| Item Values $v_i$ | Recurrence Formula| Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Standard 0/1**      | Knapsack Capacity | Item Values $v_i$ | $\max(v_i + dp[w-w_i], dp[w])$| **$O(W)$ 1D Array⚡**|
| **Partition Equal Sum**| $\text{TotalSum} / 2$| Equal to weight $w_i$| $dp[w] = dp[w] \lor dp[w-w_i]$| **$O(W)$ Boolean⚡**|
| **Target Sum (494)**  | $(\text{Total} + T)/2$| Count of ways ($1$)| $dp[w] += dp[w-w_i]$| **$O(W)$ 1D Array⚡**|
| **Last Stone Wt II**  | $\lfloor \text{Total}/2 \rfloor$| Equal to stone weight| $\max(w_i + dp[w-w_i], dp[w])$| **$O(W)$ 1D Array⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"0/1 Knapsack iterates capacity W backwards to enforce single item use! Target Sum reduces to Sum(P) = (Total + Target)/2!"**

---

## 3. Characteristics & 1D Reverse Loop Mathematical Proof

### 3.1 Mathematical Proof of Right-to-Left (Reverse) 1D Compression
* **2D Dependence**: In 2D table $DP[i][w]$, state $(i, w)$ depends on $(i-1, w)$ and $(i-1, w - w_i)$. Both dependencies reside in row $i-1$.
* **1D Array Overwriting Analysis**:
  - Suppose we use a single 1D array $DP[w]$ to represent row $i-1$.
  - **Forward Iteration ($w = w_i \dots W$)**:
    When calculating $DP[w]$, the entry $DP[w - w_i]$ is updated BEFORE $DP[w]$.
    Thus, $DP[w - w_i]$ reflects row $i$ (item $i$ already included). Calculating $DP[w] = \max(v_i + DP[w - w_i], DP[w])$ allows item $i$ to be picked multiple times! (Unbounded Knapsack behavior).
  - **Reverse Iteration ($w = W \dots w_i$)**:
    When calculating $DP[w]$, the entry $DP[w - w_i]$ has NOT YET BEEN UPDATED for row $i$.
    Thus, $DP[w - w_i]$ reflects row $i-1$ (item $i$ not yet included). This guarantees item $i$ is picked AT MOST ONCE!
  - Therefore, Reverse 1D iteration correctly computes 0/1 Knapsack in **$O(W)$ Auxiliary Space**. ⚡

---

## 4. Internal Working Mechanics: Target Sum Algebraic Reduction

Algebraic reduction of LeetCode 494 (Target Sum) to 0/1 Subset Sum Knapsack:

```
Given Array nums = [1, 1, 1, 1, 1], Target = 3:

Assign '+' or '-' signs to each element.
Let P be the subset of elements with '+' sign.
Let N be the subset of elements with '-' sign.

Equations:
1) Sum(P) - Sum(N) = Target
2) Sum(P) + Sum(N) = TotalSum

Add Equation 1 and Equation 2:
2 * Sum(P) = TotalSum + Target
Sum(P) = (TotalSum + Target) / 2

For nums = [1, 1, 1, 1, 1] (TotalSum = 5), Target = 3:
Sum(P) = (5 + 3) / 2 = 4.

Target Sum is REDUCED to: "Count subsets of nums that sum to 4"!
Solved via 0/1 Knapsack Reverse 1D DP in O(N * Target) Time! ✅ ⚡
```

---

## 5. Visual Diagram: 1D Reverse Loop Array Updating

```
1D DP Array Updating Step for Item w_i = 3 (Reverse Loop W=5 down to 3):

Initial Array (Row i-1):  [ dp[0] | dp[1] | dp[2] | dp[3] | dp[4] | dp[5] ]

Step w = 5: dp[5] = max( dp[5], v_i + dp[5 - 3] )  <-- Reads unmodified dp[2]!
Step w = 4: dp[4] = max( dp[4], v_i + dp[4 - 3] )  <-- Reads unmodified dp[1]!
Step w = 3: dp[3] = max( dp[3], v_i + dp[3 - 3] )  <-- Reads unmodified dp[0]!

Reverse loop guarantees items are never reused in same pass! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing 0/1 Knapsack Benchmark Variations: Standard 0/1 Knapsack, LeetCode 416 (Partition Equal Subset Sum), LeetCode 494 (Target Sum), and LeetCode 1049 (Last Stone Weight II).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing 0/1 Knapsack DP Patterns,
 * Reverse 1D Space Compression, Subset Sum, and Algebraic Reductions.
 */
public class KnapsackPatternMaster {

    // =========================================================================
    // 1. STANDARD 0/1 KNAPSACK (Reverse 1D DP O(N * W) Time, O(W) Space)
    // =========================================================================
    /**
     * Solves 0/1 Knapsack using Reverse 1D Space Compressed DP.
     *
     * @param weights array of item weights
     * @param values array of item values
     * @param capacity maximum knapsack weight W
     * @return maximum total value
     */
    public int solve01Knapsack(int[] weights, int[] values, int capacity) {
        if (weights == null || values == null || capacity <= 0) return 0;

        int n = weights.length;
        int[] dp = new int[capacity + 1];

        for (int i = 0; i < n; i++) {
            int w_i = weights[i];
            int v_i = values[i];

            // REVERSE LOOP: Iterate capacity W down to w_i! ⚡
            for (int w = capacity; w >= w_i; w--) {
                dp[w] = Math.max(dp[w], v_i + dp[w - w_i]);
            }
        }

        return dp[capacity];
    }

    // =========================================================================
    // 2. LEETCODE 416: PARTITION EQUAL SUBSET SUM (O(N * W) Time, O(W) Space)
    // =========================================================================
    /**
     * Checks if array can be partitioned into two subsets with equal sum.
     */
    public boolean canPartition(int[] nums) {
        if (nums == null || nums.length == 0) return false;

        int totalSum = 0;
        for (int num : nums) totalSum += num;

        // If total sum is odd, cannot partition into 2 equal integer subsets!
        if (totalSum % 2 != 0) return false;

        int target = totalSum / 2;
        boolean[] dp = new boolean[target + 1];
        dp[0] = true; // Base case: 0 sum is always achievable

        for (int num : nums) {
            // REVERSE LOOP for 0/1 boolean subset sum
            for (int w = target; w >= num; w--) {
                dp[w] = dp[w] || dp[w - num];
            }
        }

        return dp[target];
    }

    // =========================================================================
    // 3. LEETCODE 494: TARGET SUM (O(N * Target) Time, O(Target) Space)
    // =========================================================================
    /**
     * Solves LeetCode 494: Target Sum via Algebraic Reduction to Subset Sum.
     * Target Sum P = (TotalSum + Target) / 2.
     */
    public int findTargetSumWays(int[] nums, int target) {
        if (nums == null || nums.length == 0) return 0;

        int totalSum = 0;
        for (int num : nums) totalSum += num;

        // Check feasibility of Target Reduction
        if (Math.abs(target) > totalSum || (totalSum + target) % 2 != 0) return 0;

        int subsetTarget = (totalSum + target) / 2;
        if (subsetTarget < 0) return 0;

        int[] dp = new int[subsetTarget + 1];
        dp[0] = 1; // Base case: 1 way to form sum 0 (empty subset)

        for (int num : nums) {
            // REVERSE LOOP to count subset combinations
            for (int w = subsetTarget; w >= num; w--) {
                dp[w] += dp[w - num];
            }
        }

        return dp[subsetTarget];
    }
}
```

> **Quick Syntax:**
```java
// 0/1 Knapsack Reverse 1D Loop Line
for (int w = capacity; w >= weight; w--) dp[w] = Math.max(dp[w], value + dp[w - weight]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 416 - Partition Equal Subset Sum**:
   - Equal subset partition benchmark solved via Reverse 1D Boolean DP ($O(N \cdot W)$ time).

2. **LeetCode 494 - Target Sum**:
   - Algebraic reduction to Subset Sum Knapsack ($O(N \cdot W)$ time).

3. **LeetCode 1049 - Last Stone Weight II**:
   - Minimizing stone difference reduced to Subset Sum targeting $\lfloor \text{TotalSum} / 2 \rfloor$.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class KnapsackPatternDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   0/1 KNAPSACK PATTERN BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        KnapsackPatternMaster master = new KnapsackPatternMaster();

        // 1. Standard 0/1 Knapsack Test
        int[] weights = {10, 20, 30};
        int[] values = {60, 100, 120};
        int capacity = 50;
        int maxVal = master.solve01Knapsack(weights, values, capacity);

        System.out.println("1. Standard 0/1 Knapsack (Cap = 50):");
        System.out.println("   Weights = [10, 20, 30], Values = [60, 100, 120]");
        System.out.println("   Max Value (Reverse 1D DP): " + maxVal + " (Optimal = 220)");
        System.out.println("-------------------------------------------------");

        // 2. Partition Equal Subset Sum Test (LeetCode 416)
        int[] nums1 = {1, 5, 11, 5};
        boolean canPart1 = master.canPartition(nums1);
        System.out.println("2. LeetCode 416 Partition Equal Subset Sum for [1, 5, 11, 5]:");
        System.out.println("   Can Partition: " + canPart1 + " (Subsets: [1,5,5] and [11])");
        System.out.println("-------------------------------------------------");

        // 3. Target Sum Test (LeetCode 494)
        int[] nums2 = {1, 1, 1, 1, 1};
        int target = 3;
        int targetWays = master.findTargetSumWays(nums2, target);
        System.out.println("3. LeetCode 494 Target Sum for [1,1,1,1,1], Target = " + target + ":");
        System.out.println("   Total Ways (Algebraic Subset Sum): " + targetWays + " Ways");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| 0/1 Knapsack Variation | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Standard 0/1 Knapsack** | $\mathbf{O(N \cdot W)}$ Pseudo ⚡| $\mathbf{O(W)}$ 1D Array ⚡| Reverse loop $W \to w_i$ |
| **Partition Equal Sum (416)**| $\mathbf{O(N \cdot \text{Target})}$| $\mathbf{O(\text{Target})}$ Boolean⚡| Target = $\text{TotalSum} / 2$ |
| **Target Sum (494)** | $\mathbf{O(N \cdot \text{Target})}$| $\mathbf{O(\text{Target})}$ Array ⚡| Target = $(\text{Total} + T) / 2$ |

---

## 10. Edge Cases & Boundary Handling

1. **Odd Total Sum in Partition Equal Subset Sum (`totalSum % 2 != 0`)**:
   - Returns `false` immediately since an odd integer cannot split into two equal integer halves.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forward Iteration (`w = w_i ... W`) in 0/1 Knapsack**:
  - Forward iteration overwrites $DP[w - w_i]$ in the current step, allowing items to be reused multiple times. **ALWAYS iterate $w$ BACKWARDS from $W$ down to $w_i$ for 0/1 Knapsack!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 1D Knapsack Loop Rule:
> * **Reverse Loop (`for w = W down to w_i`)**: 0/1 Knapsack (Single-use items).
> * **Forward Loop (`for w = w_i up to W`)**: Unbounded Knapsack (Infinite-use items). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | 0/1 Knapsack (Reverse 1D Loop) | Unbounded Knapsack (Forward 1D Loop) |
| :--- | :--- | :--- |
| **Capacity Loop Order** | **$W \to w_i$ (Reverse) ⚡** | $w_i \to W$ (Forward) |
| **Item Re-use** | Single Use Only ($x_i \in \{0, 1\}$) | Infinite Re-use ($x_i \in \mathbb{Z}_{\ge 0}$) |
| **Space Complexity** | **$O(W)$ 1D Array ⚡** | **$O(W)$ 1D Array ⚡** |

---

## 14. How to Recognize This in Questions

* **"Can array be partitioned into two subsets with equal sum?"** $\rightarrow$ LeetCode 416 (0/1 Knapsack Target $=\text{Total}/2$).
* **"Find ways to assign + and - signs to reach target"** $\rightarrow$ LeetCode 494 (Subset Sum Reduction).

---

## 15. Frequently Asked Interview Questions

* **Q: Why MUST capacity $W$ be iterated backwards in 0/1 Knapsack 1D DP?**  
  *A:* To ensure $DP[w - w_i]$ represents the state from the previous item $i-1$, preventing item $i$ from being used multiple times in the same pass.

* **Q: How is Target Sum reduced to Subset Sum?**  
  *A:* By expressing $P - N = \text{Target}$ and $P + N = \text{TotalSum}$, leading to $2P = \text{TotalSum} + \text{Target} \implies P = (\text{TotalSum} + \text{Target}) / 2$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 0/1 KNAPSACK PATTERN                                  |
+-----------------------------------------------------------------------+
| • 0/1 Recurrence: dp[w] = max(v_i + dp[w - w_i], dp[w])                |
| • 1D Loop Order : MUST iterate W down to w_i BACKWARDS (Reverse Loop) |
| • Partition 416 : Target = TotalSum / 2 (If TotalSum is odd -> false) |
| • Target Sum 494: Reduced to Subset Sum P = (TotalSum + Target) / 2   |
| • Performance   : O(N * W) Pseudo-Polynomial Time | O(W) 1D Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write standard 0/1 Knapsack with Reverse 1D Space Compression in Java.
- [ ] I can solve LeetCode 416 (`Partition Equal Subset Sum`).
- [ ] I can solve LeetCode 494 (`Target Sum`) using algebraic subset sum reduction.
- [ ] I can prove why reverse iteration prevents item reuse.
- [ ] I can state the difference between 0/1 Knapsack and Unbounded Knapsack 1D loops.
