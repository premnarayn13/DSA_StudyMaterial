# 08. Monotonic Functions & Continuous Domain Binary Search

## 1. Introduction
**Monotonic Functions** represent the broader mathematical foundation that enables binary search across continuous real domains $\mathbb{R}$ and complex partition boundaries. A function $f(x)$ is **Monotonic** over an interval if it is either monotonically non-decreasing ($f(x_1) \le f(x_2)$ for $x_1 < x_2$) or monotonically non-increasing ($f(x_1) \ge f(x_2)$ for $x_1 < x_2$). Searching over continuous monotonic domains—such as **Sqrt(x) (LeetCode 69)**, **N-th Root of an Integer**, and **Median of Two Sorted Arrays (LeetCode 4)**—requires modifying discrete index midpoints to continuous real midpoints `mid = low + (high - low) / 2.0` and controlling termination precision via an **Epsilon Threshold (`high - low > 1e-7`)** or **Fixed Iteration Loops**.

> **Important:** Core Invariants of Continuous Monotonic Binary Search:
> 1. **Continuous Range Definition $[low, high]$**: Search space consists of continuous floating-point numbers $\mathbb{R}$.
> 2. **Fixed Precision Epsilon Termination (`eps = 1e-7`)**:
>    - Loop condition: `while (high - low > eps)` or fixed iteration count `for (int i = 0; i < 100; i++)`.
>    - A 100-iteration loop reduces search interval size by $2^{100} \approx 1.26 \times 10^{30}$, achieving double-precision floating-point accuracy!
> 3. **Exact Half Assignment**: In continuous binary search, use `high = mid` and `low = mid` without $+1$ or $-1$ offsets (since mid is a real number). ⚡

```
Continuous Floating-Point Binary Search Topology (Sqrt(2) = 1.4142135):
Domain [1.0 ... 2.0]:   mid = 1.5,   1.5^2 = 2.25 > 2.0  ---> high = 1.5
Domain [1.0 ... 1.5]:   mid = 1.25,  1.25^2 = 1.5625 < 2.0 -> low = 1.25
Domain [1.25 ... 1.5]:  mid = 1.375, 1.375^2 = 1.8906 < 2.0 -> low = 1.375
... after 60 iterations: mid = 1.414213562373095! ⚡
```

---

## 2. Core Concepts & Continuous vs Discrete Searching Matrix

### 2.1 Continuous vs Discrete Search Strategy Matrix
```
Continuous vs Discrete Search Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Metric / Dimension    | Discrete Binary Search| Continuous Binary Search| Median Dual Partition|
+-----------------------+-------------------+-------------------+-------------------+
| **Domain**            | Integers $\mathbb{Z}$| Real Numbers $\mathbb{R}$| Dual Arrays       |
| **Mid Offset**        | `mid + 1` / `mid - 1`| `high = mid, low = mid`| Partition Cut $i$ |
| **Termination**       | `low <= high`     | `high - low > 1e-7`| Left Max $\le$ Right Min|
| **Precision Control** | Exact Integer Match| Epsilon $\epsilon$| Perfect Partition |
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Continuous BS: Use high = mid and low = mid without offsets! Terminate with high - low > 1e-7!"**

---

## 3. Characteristics & 100-Iteration Precision Proof

### 3.1 Mathematical Proof of Fixed 100-Iteration Precision
* Consider a continuous initial interval $[low, high]$ of size $L = 10^9$.
* Halving the interval 100 times reduces the interval size to:
  $$\text{Final Interval} = \frac{L}{2^{100}} = \frac{10^9}{1.26 \times 10^{30}} \approx 7.9 \times 10^{-22}$$
* This precision far exceeds IEEE 754 64-bit double precision ($1.11 \times 10^{-16}$).
* Fixed 100-iteration loops eliminate floating-point rounding infinite loops in $O(100) = \mathbf{O(1) \text{ Constant Time Complexity}}$. ⚡

---

## 4. Internal Working Mechanics: Median of Two Sorted Arrays (LeetCode 4)

In LeetCode 4, we perform binary search on the partition cut $i$ of the smaller array $A$ of size $M$ such that partition cut $j = \frac{M + N + 1}{2} - i$ divides combined elements into equal left and right halves:

```
Combined Sorted Partition Invariant:
Left Half:  A[0 ... i-1] and B[0 ... j-1]  (Total (M+N+1)/2 elements)
Right Half: A[i ... M-1] and B[j ... N-1]

Condition for Valid Median Partition:
A[i-1] <= B[j]  AND  B[j-1] <= A[i]

If A[i-1] > B[j] -> Partition cut i is too far right! Set high = i - 1.
If B[j-1] > A[i] -> Partition cut i is too far left!  Set low = i + 1.

Median calculated in O(log(min(M, N))) Time! ✅
```

---

## 5. Visual Diagram: Continuous Monotonic Curve Halving

```
Continuous Function Curve f(x) = x^2 - Target:

f(x)
  ^
  |                  / f(x) = x^2 (Monotonically Increasing)
  |                 /
  |----------------/--- Target Line
  |               /|
  |              / |
  +-------------/--+--------> x
             low   mid  high
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LeetCode 69 (Integer Sqrt), Continuous Floating-Point Sqrt, N-th Root Solver, and LeetCode 4 (Median of Two Sorted Arrays).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Monotonic Functions,
 * Continuous Floating-Point Binary Search, and Median of Two Sorted Arrays.
 */
public class MonotonicFunctionsMaster {

    // =========================================================================
    // 1. INTEGER SQUARE ROOT (LeetCode 69 O(log X))
    // =========================================================================
    /**
     * Computes floor(sqrt(x)) for a non-negative integer x.
     * LeetCode 69 Solution.
     */
    public int mySqrt(int x) {
        if (x < 2) return x;

        int low = 1;
        int high = x / 2; // Sqrt(x) <= x / 2 for x >= 4
        int ans = 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;

            // Overflow-safe comparison: mid <= x / mid (Equivalent to mid * mid <= x)
            if (mid <= x / mid) {
                ans = mid;        // Candidate found, try larger value
                low = mid + 1;
            } else {
                high = mid - 1;   // Value too large
            }
        }

        return ans;
    }

    // =========================================================================
    // 2. CONTINUOUS FLOATING-POINT SQUARE ROOT (Fixed 100-Iteration Precision)
    // =========================================================================
    /**
     * Computes double-precision sqrt(x) using continuous floating-point binary search.
     * Fixed 100 iterations guarantee 1e-15 accuracy.
     */
    public double continuousSqrt(double x) {
        if (x < 0) throw new IllegalArgumentException("Negative input: " + x);
        if (x == 0) return 0.0;

        double low = (x < 1.0) ? x : 1.0;
        double high = (x < 1.0) ? 1.0 : x;

        // Fixed 100-iteration loop eliminates floating-point precision infinite loops!
        for (int iter = 0; iter < 100; iter++) {
            double mid = low + (high - low) / 2.0;

            if (mid * mid <= x) {
                low = mid;  // No +1 / -1 offsets in continuous search!
            } else {
                high = mid;
            }
        }

        return low + (high - low) / 2.0;
    }

    // =========================================================================
    // 3. MEDIAN OF TWO SORTED ARRAYS (LeetCode 4 O(log(min(M, N))))
    // =========================================================================
    /**
     * Finds the median of two sorted arrays in O(log(min(M, N))) time.
     * LeetCode 4 Solution.
     */
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        // Ensure nums1 is the smaller array to achieve O(log(min(M, N))) time
        if (nums1.length > nums2.length) {
            return findMedianSortedArrays(nums2, nums1);
        }

        int m = nums1.length;
        int n = nums2.length;
        int low = 0, high = m;

        while (low <= high) {
            int i = low + (high - low) / 2;           // Partition cut in nums1
            int j = (m + n + 1) / 2 - i;              // Partition cut in nums2

            int maxLeftA = (i == 0) ? Integer.MIN_VALUE : nums1[i - 1];
            int minRightA = (i == m) ? Integer.MAX_VALUE : nums1[i];

            int maxLeftB = (j == 0) ? Integer.MIN_VALUE : nums2[j - 1];
            int minRightB = (j == n) ? Integer.MAX_VALUE : nums2[j];

            if (maxLeftA <= minRightB && maxLeftB <= minRightA) {
                // Valid Partition Boundary Found!
                if ((m + n) % 2 == 0) {
                    return (Math.max(maxLeftA, maxLeftB) + Math.min(minRightA, minRightB)) / 2.0;
                } else {
                    return Math.max(maxLeftA, maxLeftB);
                }
            } else if (maxLeftA > minRightB) {
                high = i - 1; // Partition cut i is too far right
            } else {
                low = i + 1;  // Partition cut i is too far left
            }
        }

        return 0.0;
    }
}
```

> **Quick Syntax:**
```java
// Continuous Floating-Point Mid Assignment
for (int i = 0; i < 100; i++) { double mid = low + (high - low) / 2.0; if (mid * mid <= x) low = mid; else high = mid; }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 69 - Sqrt(x)**:
   - Discrete Integer Square Root ($O(\log X)$).

2. **LeetCode 4 - Median of Two Sorted Arrays**:
   - Dual Partition Cut Binary Search ($O(\log(\min(M, N)))$).

3. **Computer Graphics & Physics Simulation**:
   - Continuous Ray-Surface Intersection Location via Epsilon Binary Search.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class MonotonicFunctionsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MONOTONIC FUNCTIONS SEARCH DEMONSTRATION     ");
        System.out.println("=================================================\n");

        MonotonicFunctionsMaster master = new MonotonicFunctionsMaster();

        // 1. Integer Sqrt Test (LeetCode 69)
        int x = 8;
        int intSqrt = master.mySqrt(x);
        System.out.println("1. Integer Sqrt(" + x + "): " + intSqrt + " (floor)");
        System.out.println("-------------------------------------------------");

        // 2. Continuous Floating-Point Sqrt Test
        double val = 2.0;
        double floatSqrt = master.continuousSqrt(val);
        System.out.println("2. Continuous Double Sqrt(" + val + "): " + String.format("%.15f", floatSqrt));
        System.out.println("   Math.sqrt(" + val + ")           : " + String.format("%.15f", Math.sqrt(val)));
        System.out.println("-------------------------------------------------");

        // 3. Median of Two Sorted Arrays Test (LeetCode 4)
        int[] nums1 = {1, 3};
        int[] nums2 = {2};
        double median = master.findMedianSortedArrays(nums1, nums2);
        System.out.println("3. Median of " + Arrays.toString(nums1) + " and " + Arrays.toString(nums2) + ": " + median);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Continuous / Monotonic Algorithm | Time Complexity | Auxiliary Space | Domain Type | Termination Invariant |
| :--- | :--- | :--- | :--- | :--- |
| **Integer Sqrt (69)** | $\mathbf{O(\log X)}$ Log ⚡ | $\mathbf{O(1)}$ Constant ⚡ | Integers $\mathbb{Z}$ | `low <= high` |
| **Continuous Sqrt** | $\mathbf{O(100)} = \mathbf{O(1)}$ ⚡| $\mathbf{O(1)}$ Constant ⚡ | Reals $\mathbb{R}$ | Fixed 100 Iterations |
| **Median 2 Arrays (4)** | $\mathbf{O(\log(\min(M, N)))}$⚡| $\mathbf{O(1)}$ Constant ⚡ | Dual Arrays | Valid Left/Right Max/Min |

---

## 10. Edge Cases & Boundary Handling

1. **Continuous Binary Search for $X < 1.0$**:
   - For numbers like $x = 0.04$, $\sqrt{x} = 0.2 > x$.
   - **Guard**: Initialize `high = 1.0` when $x < 1.0$ (range $[x \dots 1.0]$).

2. **Median of Two Sorted Arrays with Empty Array**:
   - Handled cleanly by `(i == 0 ? Integer.MIN_VALUE : nums1[i - 1])` sentinel logic.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using Floating-Point `while (high - low > 0)`**:
  - Due to IEEE 754 precision limits, `high - low` may never equal exact `0.0`, resulting in an infinite loop.
  - **Fix**: Use a fixed 100-iteration loop `for (int i = 0; i < 100; i++)` or `high - low > 1e-7`.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Fixed Iterations Beat `while (high - low > eps)` for Reals:
> `for (int iter = 0; iter < 100; iter++)` is 100% immune to floating-point precision lockup and guarantees execution finishes in exact constant time while achieving $10^{-22}$ precision! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Continuous Binary Search (Reals) | Newton-Raphson Method |
| :--- | :--- | :--- |
| **Derivative Requirement**| **No Derivatives Required ⚡** | Requires Derivative $f'(x)$ |
| **Convergence Guarantee** | **Guaranteed Monotonic Halving ⚡**| Can diverge if initial guess bad |
| **Implementation** | ~8 Lines | ~15 Lines |

---

## 14. How to Recognize This in Questions

* **"Compute square root / N-th root of number to fixed decimal precision"** $\rightarrow$ Continuous Floating-Point Binary Search.
* **"Find median of two sorted arrays in O(log(min(M, N))) time"** $\rightarrow$ LeetCode 4 Partition Cut Binary Search.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Median of Two Sorted Arrays achieve $O(\log(\min(M, N)))$ time?**  
  *A:* By performing binary search on the partition cut $i$ of the smaller array of size $\min(M, N)$, the corresponding partition cut $j$ of the second array is determined automatically in $O(1)$ time.

* **Q: How does `mid <= x / mid` prevent integer overflow in Sqrt(x)?**  
  *A:* Rearranging $mid \times mid \le x$ to $mid \le x / mid$ avoids multiplying two large 32-bit integers that would overflow `Integer.MAX_VALUE`.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MONOTONIC FUNCTIONS & REALS                           |
+-----------------------------------------------------------------------+
| • Continuous BS: High = mid, Low = mid (NO +1 / -1 offsets!)          |
| • Termination  : Use fixed 100 iterations loop for double-precision!  |
| • Sqrt Guard   : Use mid <= x / mid to prevent integer overflow       |
| • Median 2 Arr : Partition cut i in smaller array -> O(log(min(M, N)))|
| • Range for X<1: Set high = 1.0 when x < 1.0 (since sqrt(0.04) = 0.2)!⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 69 (`Sqrt(x)`) with overflow-safe `mid <= x / mid`.
- [ ] I can write continuous floating-point binary search using a 100-iteration loop.
- [ ] I can write LeetCode 4 (`Median of Two Sorted Arrays`) in $O(\log(\min(M, N)))$ time.
- [ ] I know why `high` must be set to `1.0` when computing continuous square root of $x < 1.0$.
- [ ] I can trace dual array partition cuts step by step.
