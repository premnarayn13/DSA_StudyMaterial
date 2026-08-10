# 10. Matrix DP: Chain Multiplication, Interval Splitting & Burst Balloons

## 1. Introduction
**Matrix DP (Interval DP)** addresses parenthesization, matrix chain multiplication, and optimal interval partitioning problems where subproblems are defined over contiguous subarrays or sub-intervals $[i \dots j]$ ($1 \le i \le j \le N$). Unlike standard 1D or 2D grid DP where transitions move linearly left-to-right or top-to-bottom, Matrix DP evaluates subproblem intervals in **Increasing Order of Window Length $L = j - i + 1$** (from $L = 2$ up to $N$). For each interval $[i \dots j]$, an internal split point $k$ ($i \le k < j$) partitions the interval into two optimal sub-intervals $[i \dots k]$ and $[k+1 \dots j]$. Major variation benchmarks include **Matrix Chain Multiplication (MCM)**, **Burst Balloons (LeetCode 312)**, **Minimum Cost Tree From Leaf Values (LeetCode 1130)**, and **Strange Printer (LeetCode 664)**. Matrix DP executes in **$O(N^3)$ Cubic Time Complexity** and **$O(N^2)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Matrix DP:
> 1. **Interval Window Length Invariant ($L = j - i + 1$)**:
>    - The outer loop MUST iterate over increasing interval lengths $L = 2 \dots N$. This guarantees that smaller sub-intervals $[i \dots k]$ and $[k+1 \dots j]$ are fully solved BEFORE computing $DP[i][j]$!
> 2. **Interval Split Recurrence Formula**:
>    - For interval $[i \dots j]$ and split point $k$ ($i \le k < j$):
>      $$DP[i][j] = \min_{i \le k < j} \left( DP[i][k] + DP[k+1][j] + \text{Cost}(i, k, j) \right)$$
> 3. **Matrix Chain Multiplication Scalar Operations**:
>    - Multiplying matrix chain $M_i \dots M_j$ with dimensions $p_{i-1} \times p_i \dots p_{j-1} \times p_j$:
>      $$\text{Cost}(i, k, j) = p_{i-1} \cdot p_k \cdot p_j$$
> 4. **Reverse Thinking Invariant (Burst Balloons - LeetCode 312)**:
>    - Instead of choosing which balloon to burst FIRST, choose which balloon $k$ is burst **LAST** in range $[i \dots j]$! This isolates subproblems $[i \dots k-1]$ and $[k+1 \dots j]$ independently! ⚡

```
Matrix Chain Multiplication Interval Splitting Topology:

Interval Window [ i ........................ j ] (Length L)
                        │
                  Split at Point k (i <= k < j)
                        │
       ┌────────────────┴────────────────┐
       ▼                                 ▼
[ Sub-interval i..k ]          [ Sub-interval k+1..j ]
 (Already Computed!)            (Already Computed!)

Total Cost = DP[i][k] + DP[k+1][j] + p_{i-1} * p_k * p_j ⚡
```

---

## 2. Core Concepts & Matrix DP Strategy Matrix

### 2.1 Matrix DP Problem Strategy Matrix
```
Matrix DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Matrix DP Variant     | Outer Loop        | Split Variable $k$| Cost Term         | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Matrix Chain Mult** | Window Length $L$ | $i \le k < j$     | $p_{i-1} \cdot p_k \cdot p_j$| **$O(N^3)$ Cubic ⚡**|
| **Burst Balloons (312)**| Window Length $L$| $k$ burst LAST    | $A[i-1] \cdot A[k] \cdot A[j+1]$| **$O(N^3)$ Cubic ⚡**|
| **Min Cost Tree (1130)**| Window Length $L$| $i \le k < j$     | $\max(L) \cdot \max(R)$| **$O(N^3)$ Cubic ⚡**|
| **Strange Printer**   | Window Length $L$ | $i \le k < j$     | $dp[i][k] + dp[k+1][j]$| **$O(N^3)$ Cubic ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Matrix DP loops by window length L=2..N; inner split k partitions interval into dp[i][k] + dp[k+1][j] + cost!"**

---

## 3. Characteristics & Reverse Thinking Mathematical Proof (Burst Balloons)

### 3.1 Mathematical Proof of Reverse Thinking in LeetCode 312 (Burst Balloons)
* Given $N$ balloons with coins $A[1 \dots N]$. Bursting balloon $k$ yields $A[k-1] \cdot A[k] \cdot A[k+1]$ coins.
* **Why Forward Choice Fails**:
  If we pick balloon $k$ to burst FIRST, balloons $k-1$ and $k+1$ become adjacent. The remaining left subproblem $[i \dots k-1]$ and right subproblem $[k+1 \dots j]$ become DEPENDENT because bursting balloons in the left subproblem alters neighbor values for the right subproblem! (Violates Subproblem Independence).
* **Reverse Choice Invariant (Pick Last Balloon)**:
  Assume balloon $k$ is the **LAST balloon burst** in interval $[i \dots j]$.
  - Since $k$ is burst LAST, all other balloons in $[i \dots j]$ are already burst.
  - Therefore, the boundary balloons remaining adjacent to $k$ when $k$ is burst are precisely **$A[i-1]$ on the left and $A[j+1]$ on the right**!
  - Coins earned from bursting $k$ last:
    $$\text{Coins} = A[i-1] \cdot A[k] \cdot A[j+1]$$
  - Subproblems $[i \dots k-1]$ and $[k+1 \dots j]$ are completely INDEPENDENT!
* Dynamic Programming Recurrence:
  $$DP[i][j] = \max_{i \le k \le j} \left( DP[i][k-1] + DP[k+1][j] + A[i-1] \cdot A[k] \cdot A[j+1] \right)$$
* Evaluated over window length $L = 1 \dots N$ in **$O(N^3)$ Time and $O(N^2)$ Space**! ⚡

---

## 4. Internal Working Mechanics: Matrix Chain Multiplication Execution

Tracing MCM for dimensions array $P = [10, 20, 30, 40, 30]$ ($N = 4$ matrices):

```
Matrices: M1 (10x20), M2 (20x30), M3 (30x40), M4 (40x30).

Window Length L = 2 (Subproblems of size 2):
- dp[1][2] (M1*M2) = 10 * 20 * 30 = 6000.
- dp[2][3] (M2*M3) = 20 * 30 * 40 = 24000.
- dp[3][4] (M3*M4) = 30 * 40 * 30 = 36000.

Window Length L = 3 (Subproblems of size 3):
- dp[1][3] (M1*M2*M3):
  k = 1: (M1)*(M2*M3) = dp[1][1] + dp[2][3] + 10*20*40 = 0 + 24000 + 8000 = 32000.
  k = 2: (M1*M2)*(M3) = dp[1][2] + dp[3][3] + 10*30*40 = 6000 + 0 + 12000 = 18000! (Min = 18000).

Window Length L = 4 (Full Chain dp[1][4]):
- Evaluates k = 1, 2, 3 -> Optimal Cost = 30,000 Scalar Multiplications! ✅ ⚡
```

---

## 5. Visual Diagram: Burst Balloons Reverse Choice Independence

```
Burst Balloons (Reverse Choice - Balloon k Burst LAST):

Boundaries:  [ A[i-1] ]  ... [ Sub-interval i..k-1 ] ... (Balloon k) ... [ Sub-interval k+1..j ] ... [ A[j+1] ]
                               (All Burst!)                            (All Burst!)

When Balloon k is burst LAST:
Coins Earned = A[i-1] * A[k] * A[j+1]!
Left and Right sub-intervals stay completely independent! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Matrix Chain Multiplication, LeetCode 312 (Burst Balloons), and LeetCode 1130 (Minimum Cost Tree From Leaf Values).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Matrix DP (Interval DP):
 * Matrix Chain Multiplication, Burst Balloons (Reverse Choice), and Leaf Tree Cost.
 */
public class MatrixDPProblemsMaster {

    // =========================================================================
    // 1. MATRIX CHAIN MULTIPLICATION (O(N^3) Time, O(N^2) Space)
    // =========================================================================
    /**
     * Calculates minimum scalar multiplications to multiply chain of matrices.
     * Dimensions of Matrix i are p[i-1] x p[i].
     *
     * @param p array of matrix dimensions
     * @return minimum scalar multiplications count
     */
    public int matrixChainOrder(int[] p) {
        if (p == null || p.length <= 2) return 0;

        int n = p.length - 1; // Total matrices
        int[][] dp = new int[n + 1][n + 1];

        // Outer Loop 1: Window Length L (from 2 up to n)
        for (int L = 2; L <= n; L++) {
            for (int i = 1; i <= n - L + 1; i++) {
                int j = i + L - 1;
                dp[i][j] = Integer.MAX_VALUE;

                // Inner Loop 3: Split Point k (i <= k < j)
                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + p[i - 1] * p[k] * p[j];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }

        return dp[1][n];
    }

    // =========================================================================
    // 2. LEETCODE 312: BURST BALLOONS (REVERSE CHOICE O(N^3) Time, O(N^2) Space)
    // =========================================================================
    /**
     * Maximizes coins earned bursting balloons using Reverse Thinking (Pick Last Burst).
     */
    public int maxCoins(int[] nums) {
        if (nums == null || nums.length == 0) return 0;

        int n = nums.length;
        // Pad array with boundary 1s
        int[] A = new int[n + 2];
        A[0] = 1;
        A[n + 1] = 1;
        for (int i = 0; i < n; i++) A[i + 1] = nums[i];

        int[][] dp = new int[n + 2][n + 2];

        // Outer Loop: Window Length L from 1 to n
        for (int L = 1; L <= n; L++) {
            for (int i = 1; i <= n - L + 1; i++) {
                int j = i + L - 1;

                // Inner Loop: Balloon k is burst LAST in range [i..j] ⚡
                for (int k = i; k <= j; k++) {
                    int coins = dp[i][k - 1] + dp[k + 1][j] + A[i - 1] * A[k] * A[j + 1];
                    dp[i][j] = Math.max(dp[i][j], coins);
                }
            }
        }

        return dp[1][n];
    }

    // =========================================================================
    // 3. LEETCODE 1130: MIN COST TREE FROM LEAF VALUES (O(N^3) Time)
    // =========================================================================
    /**
     * Calculates minimum non-leaf node sum for binary tree constructed from leaves.
     */
    public int mctFromLeafValues(int[] arr) {
        if (arr == null || arr.length <= 1) return 0;

        int n = arr.length;
        int[][] dp = new int[n][n];

        // Precompute max leaf values for range [i..j]
        int[][] maxLeaf = new int[n][n];
        for (int i = 0; i < n; i++) {
            maxLeaf[i][i] = arr[i];
            for (int j = i + 1; j < n; j++) {
                maxLeaf[i][j] = Math.max(maxLeaf[i][j - 1], arr[j]);
            }
        }

        for (int L = 2; L <= n; L++) {
            for (int i = 0; i <= n - L; i++) {
                int j = i + L - 1;
                dp[i][j] = Integer.MAX_VALUE;

                for (int k = i; k < j; k++) {
                    int cost = dp[i][k] + dp[k + 1][j] + maxLeaf[i][k] * maxLeaf[k + 1][j];
                    dp[i][j] = Math.min(dp[i][j], cost);
                }
            }
        }

        return dp[0][n - 1];
    }
}
```

> **Quick Syntax:**
```java
// Burst Balloons Reverse Choice Line
int coins = dp[i][k - 1] + dp[k + 1][j] + A[i - 1] * A[k] * A[j + 1]; dp[i][j] = Math.max(dp[i][j], coins);
```

---

## 7. Concrete Problem Examples & Applications

1. **Matrix Chain Multiplication**:
   - Primary matrix multiplication optimization benchmark ($O(N^3)$ time).

2. **LeetCode 312 - Burst Balloons**:
   - Reverse choice selection benchmark ($O(N^3)$ time).

3. **LeetCode 1130 - Min Cost Tree From Leaf Values**:
   - Binary tree construction optimization ($O(N^3)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class MatrixDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MATRIX DP & INTERVAL SPLITTING DEMO           ");
        System.out.println("=================================================\n");

        MatrixDPProblemsMaster master = new MatrixDPProblemsMaster();

        // 1. MCM Test
        int[] dims = {10, 20, 30, 40, 30};
        int minMults = master.matrixChainOrder(dims);
        System.out.println("1. Matrix Chain Multiplication for Dimensions [10, 20, 30, 40, 30]:");
        System.out.println("   Minimum Scalar Multiplications: " + minMults + " Multiplications (Optimal = 30000)");
        System.out.println("-------------------------------------------------");

        // 2. Burst Balloons Test (LeetCode 312)
        int[] balloons = {3, 1, 5, 8};
        int maxCoins = master.maxCoins(balloons);
        System.out.println("2. LeetCode 312 Burst Balloons for [3, 1, 5, 8]:");
        System.out.println("   Max Coins Earned (Reverse Choice DP): " + maxCoins + " Coins (Optimal = 167)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Matrix DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Matrix Chain Order** | $\mathbf{O(N^3)}$ Cubic ⚡| $O(N^2)$ Table | $p_{i-1} \cdot p_k \cdot p_j$ |
| **Burst Balloons (312)**| $\mathbf{O(N^3)}$ Cubic ⚡| $O(N^2)$ Table | Balloon $k$ burst LAST |
| **Min Cost Tree (1130)**| $\mathbf{O(N^3)}$ Cubic ⚡| $O(N^2)$ Table | $\max(L) \cdot \max(R)$ |

---

## 10. Edge Cases & Boundary Handling

1. **Single Matrix or Single Balloon ($N=1$)**:
   - MCM returns 0 multiplications; Burst Balloons returns $1 \cdot A[1] \cdot 1$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Choosing First Balloon Burst in Burst Balloons**:
  - Picking the first balloon creates dependencies between left and right subproblems. ALWAYS pick the balloon burst **LAST**!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The Matrix DP Loop Order Rule:
> Matrix DP problems MUST iterate the outer loop by **Increasing Window Length $L$ ($2 \dots N$)** to guarantee smaller sub-intervals are computed before larger intervals! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard 2D DP | Matrix / Interval DP |
| :--- | :--- | :--- |
| **Subproblem Unit** | Cell $(i, j)$ | Subarray Interval $[i \dots j]$ |
| **Outer Loop Variable**| Row index $i$ | **Window Length $L = j - i + 1$ ⚡** |
| **Time Complexity** | $O(M \cdot N)$ Quadratic | **$O(N^3)$ Cubic ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find optimal parenthesization to multiply chain of matrices"** $\rightarrow$ MCM ($O(N^3)$ DP).
* **"Maximize coins bursting balloons where neighbors change"** $\rightarrow$ LeetCode 312 (Reverse choice $k$ last).

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Burst Balloons require Reverse Thinking (picking balloon $k$ burst LAST)?**  
  *A:* Because picking balloon $k$ last guarantees that the neighbors of $k$ when it bursts are $A[i-1]$ and $A[j+1]$, making left subproblem $[i \dots k-1]$ and right subproblem $[k+1 \dots j]$ completely independent.

* **Q: Why does Matrix DP iterate by window length $L$?**  
  *A:* To ensure that sub-intervals of smaller lengths are fully computed before computing larger intervals that depend on them.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATRIX DP & INTERVAL SPLITTING                        |
+-----------------------------------------------------------------------+
| • MCM Formula   : dp[i][j] = min(dp[i][k] + dp[k+1][j] + p[i-1]*p[k]*p[j])|
| • Burst Balloons: Balloon k burst LAST -> coins = A[i-1]*A[k]*A[j+1]  |
| • Outer Loop    : MUST iterate by Window Length L from 2 up to N      |
| • Performance   : O(N^3) Cubic Time | O(N^2) Auxiliary Matrix Space ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Matrix Chain Multiplication in $O(N^3)$ time in Java.
- [ ] I can write Burst Balloons (LeetCode 312) using Reverse Choice DP.
- [ ] I can write Minimum Cost Tree From Leaf Values (LeetCode 1130).
- [ ] I can prove why Burst Balloons requires picking balloon $k$ burst LAST.
- [ ] I can state the 3 nested loops required for Matrix DP.
