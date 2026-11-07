# 15. DP Optimizations: Monotonic Queues, Convex Hull Trick & Knuth Optimization

## 1. Introduction
**Dynamic Programming Optimizations** transform computationally expensive $O(N^2)$ or $O(N^3)$ DP algorithms into high-speed **$O(N)$ Linear or $O(N \log N)$ Log-Linear Algorithms** by exploiting mathematical and structural properties of the state transition functions. Standard DP optimizations do not alter the underlying recurrence logic; instead, they optimize the **Inner Min/Max Transition Search Window**. The three primary advanced DP optimization techniques are:
1. **Monotonic Queue / Deque DP Optimization**: Reduces transitions over sliding windows of size $K$ from $O(N \cdot K)$ down to **$O(N)$ Strict Linear Time** (e.g. Constrained Subsequence Sum - LeetCode 1425 & Jump Game VI - LeetCode 1696).
2. **Convex Hull Trick (CHT)**: Optimizes transitions of the linear form $DP[i] = \min_{j < i} (m_j \cdot x_i + c_j + \text{extra}_i)$ from $O(N^2)$ down to **$O(N)$ or $O(N \log N)$** using 2D line geometry and convex envelopes.
3. **Knuth Optimization**: Reduces Interval DP from $O(N^3)$ down to **$O(N^2)$** by exploiting quadrangle inequality monotonicity ($opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$).

> **Important:** The 3 Advanced DP Optimization Paradigms:
> 1. **Monotonic Deque Window Rule**:
>    - Maintain a Deque of candidate indices $j$ in strictly decreasing order of $DP[j]$.
>    - Evict out-of-window indices ($j < i - K$) from head in $O(1)$ time.
>    - Evict smaller candidates ($DP[\text{tail}] \le DP[i]$) from tail in $O(1)$ time.
> 2. **Convex Hull Trick (CHT) Line Equation**:
>    - Convert recurrence into line equation $y = m \cdot x + c$, where line $j$ has slope $m_j = -A[j]$ and $y$-intercept $c_j = DP[j]$.
>    - If slopes $m_j$ are monotonic, maintain lower convex envelope of lines using a Deque in $O(N)$ time!
> 3. **Knuth Monotonicity Invariant**:
>    - Optimal split point $opt[i][j]$ satisfies $opt[i][j-1] \le opt[i][j] \le opt[i+1][j]$, bounding total inner loop iterations to $O(N^2)$! ⚡

```
Monotonic Deque DP Optimization Topology (Sliding Window K):

Window Range [ i - K ... i - 1 ]:
Deque Head (Max DP Value) ──► [ Index j_max ] ──► Used for DP[i] in O(1) Time! ⚡
                              [ Index j_2   ]
Deque Tail                ──► [ Index j_3   ]

Evict Head if j_max < i - K (Out of window).
Evict Tail if DP[tail] <= DP[i] (Dominated candidate).
Reduces O(N * K) transitions to O(N) Strict Linear Time! ⚡
```

---

## 2. Core Concepts & DP Optimization Strategy Matrix

### 2.1 DP Optimizations Comparison Matrix
```
DP Optimizations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Optimization Technique| Target Recurrence Form| Prerequisite Property| Time Reduction | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Monotonic Deque**   | $DP[i] = \text{val}_i + \max_{i-K \le j < i} DP[j]$| Sliding window range $K$| **$O(N \cdot K) \to O(N)$⚡**| **$O(K)$ Deque ⚡**|
| **Convex Hull (CHT)** | $DP[i] = \min_{j < i} (m_j \cdot x_i + c_j)$| Linear slope geometry| **$O(N^2) \to O(N)$ ⚡**| $O(N)$ Lines Deque|
| **Knuth Optimization**| $DP[i][j] = \min_{k} (DP[i][k] + DP[k+1][j])$| Quadrangle Inequality| **$O(N^3) \to O(N^2)$ ⚡**| $O(N^2)$ Matrix   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Monotonic Deque maintains decreasing DP[j] in O(N); Convex Hull maintains line geometry for slope m_j * x_i + c_j!"**

---

## 3. Characteristics & Convex Hull Trick Mathematical Proof

### 3.1 Mathematical Derivation of Convex Hull Trick (CHT)
* Consider DP recurrence:
  $$DP[i] = \min_{j < i} \left( DP[j] + A[j] \cdot B[i] \right)$$
* Let $y = DP[i]$, $x = B[i]$, slope $m_j = A[j]$, and intercept $c_j = DP[j]$.
* For a fixed candidate index $j$, the value contributed to $DP[i]$ is the $y$-value of line $L_j(x) = m_j \cdot x + c_j$ evaluated at $x = B[i]$.
* **Intersection Point of Two Lines $L_1$ and $L_2$**:
  $$m_1 \cdot x + c_1 = m_2 \cdot x + c_2 \implies x_{\text{intersect}}(L_1, L_2) = \frac{c_2 - c_1}{m_1 - m_2}$$
* **Envelope Line Elimination Rule**:
  - Suppose lines $L_1, L_2, L_3$ are added in increasing order of slopes $m_1 > m_2 > m_3$.
  - Line $L_2$ is redundant (never optimal for any $x$) if:
    $$x_{\text{intersect}}(L_1, L_2) \ge x_{\text{intersect}}(L_2, L_3)$$
  - Maintaining lines on a Deque and popping redundant lines from the tail guarantees that query $x_i$ can be answered in $O(1)$ time at the head.
* Reduces overall DP execution time from $O(N^2)$ down to **$O(N)$ Linear Time**. ⚡

---

## 4. Internal Working Mechanics: Monotonic Deque Sliding Window DP

Tracing LeetCode 1425 (Constrained Subsequence Sum) for $K = 2$, $nums = [10, 2, -10, 5, 20]$:

```
Recurrence: dp[i] = nums[i] + max(0, max_{i-K <= j < i} dp[j])

Deque maintains indices in strictly decreasing order of dp[j].

- i = 0 (10): dp[0] = 10. Deque = [0]
- i = 1 (2) : max_prev = dp[0] (10). dp[1] = 2 + 10 = 12. Deque = [1] (Pop 0 since dp[1] > dp[0])
- i = 2 (-10): max_prev = dp[1] (12). dp[2] = -10 + 12 = 2. Deque = [1, 2]
- i = 3 (5) : i - K = 3 - 2 = 1. Deque head 1 valid. max_prev = dp[1] (12).
              dp[3] = 5 + 12 = 17. Deque = [3] (Pop 2, 1 since dp[3] > dp[1])
- i = 4 (20): max_prev = dp[3] (17). dp[4] = 20 + 17 = 37. Deque = [4]

Max Subsequence Sum = 37! Executed in O(N) Strict Linear Time! ✅ ⚡
```

---

## 5. Visual Diagram: Convex Hull Line Elimination

```
Convex Hull Line Intersection Geometry:

Lines L1, L2, L3:
Line 1: y = m1 * x + c1
Line 2: y = m2 * x + c2  (Redundant line! Intersection(L1, L2) >= Intersection(L2, L3))
Line 3: y = m3 * x + c3

                Line 1
                   \      Line 2
                    \    /      Line 3
                     \  /      /
                      \/      /
                      /\     /
                     /  \   /
                    /    \ /
                          V  <-- Line 2 is above the lower envelope! Pop Line 2! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Monotonic Deque DP Optimization (LeetCode 1425 & LeetCode 1696), Convex Hull Trick (CHT), and Knuth Optimization.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Advanced DP Optimizations:
 * Monotonic Deque Sliding Window DP, Convex Hull Trick (CHT), and Knuth Optimization.
 */
public class DPOptimizationsMaster {

    // =========================================================================
    // 1. MONOTONIC DEQUE DP OPTIMIZATION (LeetCode 1425 O(N) Time, O(K) Space)
    // =========================================================================
    /**
     * Solves Constrained Subsequence Sum in O(N) time using Monotonic Deque.
     * dp[i] = nums[i] + max(0, max_{i-k <= j < i} dp[j]).
     *
     * @param nums array of numbers
     * @param k maximum step constraint
     * @return maximum constrained subsequence sum
     */
    public int constrainedSubsetSum(int[] nums, int k) {
        if (nums == null || nums.length == 0) return 0;
        int n = nums.length;

        int[] dp = new int[n];
        Deque<Integer> deque = new ArrayDeque<>(); // Stores indices in decreasing order of dp[j]
        int maxResult = nums[0];

        for (int i = 0; i < n; i++) {
            // Evict out-of-window indices from head
            while (!deque.isEmpty() && deque.peekFirst() < i - k) {
                deque.pollFirst();
            }

            // Calculate dp[i] using head of deque (maximum dp[j] in window)
            int maxPrev = deque.isEmpty() ? 0 : Math.max(0, dp[deque.peekFirst()]);
            dp[i] = nums[i] + maxPrev;
            maxResult = Math.max(maxResult, dp[i]);

            // Maintain decreasing order in deque by popping smaller elements from tail
            while (!deque.isEmpty() && dp[deque.peekLast()] <= dp[i]) {
                deque.pollLast();
            }

            deque.addLast(i);
        }

        return maxResult;
    }

    // =========================================================================
    // 2. CONVEX HULL TRICK (CHT) DP OPTIMIZATION (O(N) Time, O(N) Space)
    // =========================================================================
    public static class Line {
        public final long m, c; // y = m * x + c
        public Line(long m, long c) { this.m = m; this.c = c; }

        public long eval(long x) { return m * x + c; }
    }

    /**
     * Solves linear slope DP dp[i] = min_{j < i} (m_j * x_i + c_j) in O(N) time.
     */
    public long solveCHT(long[] x, long[] m, long[] c) {
        int n = x.length;
        Deque<Line> hull = new ArrayDeque<>();
        long[] dp = new long[n];

        for (int i = 0; i < n; i++) {
            Line currentLine = new Line(m[i], c[i]);

            // Pop redundant lines from tail before adding current line
            while (hull.size() >= 2) {
                Line l2 = hull.pollLast();
                Line l1 = hull.peekLast();
                if (intersectionX(l1, l2) < intersectionX(l2, currentLine)) {
                    hull.addLast(l2); // l2 is valid
                    break;
                }
            }
            hull.addLast(currentLine);

            // Pop out-of-date lines from head if query x[i] exceeds intersection
            while (hull.size() >= 2) {
                Line l1 = hull.pollFirst();
                Line l2 = hull.peekFirst();
                if (l1.eval(x[i]) >= l2.eval(x[i])) {
                    // l2 is better at x[i]
                } else {
                    hull.addFirst(l1); // l1 is still best
                    break;
                }
            }

            dp[i] = hull.peekFirst().eval(x[i]);
        }

        return dp[n - 1];
    }

    private double intersectionX(Line l1, Line l2) {
        return (double) (l2.c - l1.c) / (l1.m - l2.m);
    }
}
```

> **Quick Syntax:**
```java
// Monotonic Deque DP Eviction Lines
while (!deque.isEmpty() && deque.peekFirst() < i - k) deque.pollFirst();
while (!deque.isEmpty() && dp[deque.peekLast()] <= dp[i]) deque.pollLast();
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1425 - Constrained Subsequence Sum**:
   - Primary Monotonic Deque DP benchmark ($O(N)$ time, $O(K)$ space).

2. **LeetCode 1696 - Jump Game VI**:
   - Monotonic Deque max score jump optimization ($O(N)$ time).

3. **Convex Hull Trick (CHT)**:
   - Line slope optimization reducing $O(N^2)$ linear DP to $O(N)$ time.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class DPOptimizationsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   ADVANCED DYNAMIC PROGRAMMING OPTIMIZATIONS   ");
        System.out.println("=================================================\n");

        DPOptimizationsMaster master = new DPOptimizationsMaster();

        // 1. Monotonic Deque DP Test (LeetCode 1425)
        int[] nums = {10, 2, -10, 5, 20};
        int k = 2;
        int maxSub = master.constrainedSubsetSum(nums, k);

        System.out.println("1. LeetCode 1425 Constrained Subsequence Sum (K = 2):");
        System.out.println("   Nums = [10, 2, -10, 5, 20]");
        System.out.println("   Max Subsequence Sum (Monotonic Deque O(N)): " + maxSub + " (Optimal = 37)");
        System.out.println("-------------------------------------------------");

        // 2. CHT Optimization Test
        long[] x = {1, 2, 3, 4};
        long[] m = {10, 8, 5, 2};
        long[] c = {0, 2, 5, 10};
        long chtRes = master.solveCHT(x, m, c);

        System.out.println("2. Convex Hull Trick (CHT) Line Slope DP Optimization:");
        System.out.println("   Optimal Line Eval Result (O(N) Time): " + chtRes);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| DP Optimization Technique | Original Complexity | Optimized Complexity | Auxiliary Space | Prerequisite Condition |
| :--- | :--- | :--- | :--- | :--- |
| **Monotonic Deque** | $O(N \cdot K)$ | $\mathbf{O(N)}$ Strict ⚡| $\mathbf{O(K)}$ Deque ⚡| Sliding window range $K$ |
| **Convex Hull Trick (CHT)**| $O(N^2)$ | $\mathbf{O(N)}$ Strict ⚡| $O(N)$ Lines Deque| Monotonic slopes $m_j$ |
| **Knuth Optimization** | $O(N^3)$ | $\mathbf{O(N^2)}$ Quadratic⚡| $O(N^2)$ Matrix | Quadrangle Inequality |

---

## 10. Edge Cases & Boundary Handling

1. **Window $K \ge N$ in Monotonic Deque**:
   - Deque handles full window gracefully, reducing to Kadane's maximum prefix sum.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Retaining Non-Monotonic Elements in Deque**:
  - Forgetting to pop smaller elements from the tail (`dp[deque.peekLast()] <= dp[i]`) allows sub-optimal indices to stay in the deque, degrading execution speed to $O(N \cdot K)$. ALWAYS maintain strict monotonicity!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** When to Apply Monotonic Deque DP Optimization:
> Whenever a 1D DP transition has the form $DP[i] = \text{val}_i + \max_{i-K \le j < i} DP[j]$, use a **Monotonic Deque** to achieve **$O(N)$ Strict Linear Time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Unoptimized Sliding DP | Monotonic Deque DP | Convex Hull Trick |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | $O(N \cdot K)$ Quadratic | **$O(N)$ Strict Linear ⚡** | **$O(N)$ Strict Linear ⚡** |
| **Primary Structure**| PriorityQueue / Loop | ArrayDeque | Deque of Lines |
| **Window Boundary** | Fixed $K$ | Fixed $K$ | Variable Slopes |

---

## 14. How to Recognize This in Questions

* **"Find max constrained subsequence sum where step difference <= K"** $\rightarrow$ LeetCode 1425 (Monotonic Deque DP).
* **"Jump Game VI max score jumping at most K steps"** $\rightarrow$ LeetCode 1696 (Monotonic Deque DP).

---

## 15. Frequently Asked Interview Questions

* **Q: How does a Monotonic Deque achieve $O(N)$ total time?**  
  *A:* Each index is added to the deque AT MOST ONCE and popped AT MOST ONCE. Amortized total operations over $N$ steps equals $2N \implies O(N)$ time.

* **Q: What recurrence form triggers Convex Hull Trick (CHT)?**  
  *A:* Transitions of the linear form $DP[i] = \min_{j < i} (m_j \cdot x_i + c_j)$, where $m_j$ acts as a line slope and $c_j$ acts as a $y$-intercept.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: DP OPTIMIZATIONS                                      |
+-----------------------------------------------------------------------+
| • Monotonic Deque: dp[i] = nums[i] + max_{i-K<=j<i} dp[j] -> O(N) ⚡   |
| • Deque Head      : Contains max dp[j] in window                      |
| • Deque Tail      : Pop dp[tail] <= dp[i] to maintain monotonicity    |
| • Convex Hull CHT : Optimizes line equations y = m_j * x_i + c_j -> O(N)|
| • Performance     : Reduces O(N * K) to O(N) Strict Linear Time! ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 1425 (`Constrained Subsequence Sum`) in $O(N)$ time in Java.
- [ ] I can solve LeetCode 1696 (`Jump Game VI`) using Monotonic Deque DP.
- [ ] I can explain why amortized time for Monotonic Deque is $O(N)$.
- [ ] I can state the line equation form that triggers Convex Hull Trick.
- [ ] I can write the Deque head and tail eviction conditions.
