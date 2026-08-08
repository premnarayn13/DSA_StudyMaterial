# 03. Asymptotic Analysis

## 1. Introduction
Asymptotic analysis evaluates algorithmic efficiency in the limit—meaning as the input size $n$ approaches infinity ($n \to \infty$). It relies on mathematical notations (Big-O, Big-Omega, Big-Theta) to establish formal upper, lower, and tight execution bounds.

> **Important:** Asymptotic analysis ignores hardware variations, OS scheduling overhead, and minor constants ($c$), allowing direct mathematical comparison between different algorithms.

## 2. Core Concepts
* **Big-O Notation ($O$)**: Asymptotic **Upper Bound**. Represents the absolute worst-case scenario. $f(n) \le c \cdot g(n)$ for all $n \ge n_0$.
* **Big-Omega Notation ($\Omega$)**: Asymptotic **Lower Bound**. Represents the absolute best-case scenario. $f(n) \ge c \cdot g(n)$ for all $n \ge n_0$.
* **Big-Theta Notation ($\Theta$)**: Asymptotic **Tight Bound**. Represents exact growth rate when upper and lower bounds match ($O(f(n)) = \Omega(f(n))$).

> **Memory Trick:** **"O = Over (Upper), Ω = Under (Lower), Θ = Tight (Exact)"**. In tech interviews, when an interviewer asks for "Big-O", they mean worst-case upper bound.

## 3. Characteristics / Properties
* **Transitivity**: If $f(n) = O(g(n))$ and $g(n) = O(h(n))$, then $f(n) = O(h(n))$.
* **Reflexivity**: $f(n) = O(f(n))$.
* **Symmetry**: $f(n) = \Theta(g(n))$ if and only if $g(n) = \Theta(f(n))$.
* **Sum Rule**: $O(f(n) + g(n)) = \max(O(f(n)), O(g(n)))$.
* **Product Rule**: $O(f(n) \cdot g(n)) = O(f(n)) \cdot O(g(n))$.

## 4. Internal Working
Formal mathematical definitions visualized for $n \ge n_0$:

```
Upper Bound Big-O:               Tight Bound Big-Theta:
  Execution Time (T)               Execution Time (T)
    ^                                ^
    |       c*g(n) (Upper)           |       c2*g(n) (Upper)
    |      /                         |      /
    |     /  f(n) (Actual)           |     / f(n) (Actual)
    |    /                           |    / / c1*g(n) (Lower)
    |   /                            |   /_/
    +----+--------------> n          +----+--------------> n
        n0                               n0
```

## 5. Visual Diagram
Notational Relationship Matrix:

```
                      +-------------------+
                      | Asymptotic Bounds |
                      +---------+---------+
                                |
       +------------------------+------------------------+
       |                        |                        |
+------+------+          +------+------+          +------+------+
| Big-O (O)   |          | Big-Theta   |          | Big-Omega   |
| Upper Bound |          | Tight Bound |          | Lower Bound |
| f(n) ≤ c*g  |          | c1*g ≤ f ≤ c2*g        | f(n) ≥ c*g  |
+-------------+          +-------------+          +-------------+
```

## 6. Operations / Algorithms
Determining mathematical bounds step-by-step:
1. Identify the primary operations executing inside loops.
2. Formulate execution step equation: $T(n) = a_k n^k + a_{k-1} n^{k-1} + \dots + a_1 n + a_0$.
3. Drop all constant coefficients $a_i$.
4. Retain only the highest degree polynomial term $n^k$.

> **Quick Syntax:**
```java
// Example: Proving tight bound Theta(n) vs Big-O(n)
public static void analyzeArray(int[] arr) {
    int n = arr.length;
    // T(n) = 2n + 5 operations
    for (int i = 0; i < n; i++) {
        int x = arr[i] * 2; // Operation 1
        int y = x + 5;      // Operation 2
    }
    // T(n) = 2n + 5 <= 3n for all n >= 5 -> O(n) and Theta(n)
}
```

## 7. Examples
* **Quick Sort**:
  * Best Case: $\Omega(n \log n)$ (Pivot splits array evenly).
  * Worst Case: $O(n^2)$ (Pivot is always the smallest or largest element).
  * Average Case: $\Theta(n \log n)$.
* **Linear Search**:
  * Best Case: $\Omega(1)$ (Target at first index).
  * Worst Case: $O(n)$ (Target at last index or absent).
  * Average Case: $\Theta(n)$.

## 8. Java Code
Demonstrating best-case vs worst-case analysis programmatically in Java:

```java
public class AsymptoticAnalysisDemo {

    // Linear Search illustrating Best Case Ω(1) vs Worst Case O(n)
    public static int linearSearch(int[] arr, int target) {
        int comparisons = 0;
        for (int i = 0; i < arr.length; i++) {
            comparisons++;
            if (arr[i] == target) {
                System.out.println("Target found in " + comparisons + " comparison(s).");
                return i;
            }
        }
        System.out.println("Target not found. Total comparisons: " + comparisons);
        return -1;
    }

    public static void main(String[] args) {
        int[] data = {10, 20, 30, 40, 50, 60, 70, 80};

        // Best-Case Scenario: Target at index 0 -> Ω(1)
        linearSearch(data, 10);

        // Worst-Case Scenario: Target absent -> O(n)
        linearSearch(data, 99);
    }
}
```

## 9. Complexity Analysis
Asymptotic notation comparison summary:

| Notation | Meaning | Mathematical Condition | Interview Use Case |
| :--- | :--- | :--- | :--- |
| **$O(g(n))$** | Upper Bound (Worst Case) | $0 \le f(n) \le c \cdot g(n)$ | Standard complexity specification |
| **$\Omega(g(n))$** | Lower Bound (Best Case) | $0 \le c \cdot g(n) \le f(n)$ | Establishing minimum work required |
| **$\Theta(g(n))$** | Tight Bound (Exact Growth)| $c_1 g(n) \le f(n) \le c_2 g(n)$ | Complete average-case characterization |
| **$o(g(n))$** | Strictly Smaller Growth | $\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$ | Theoretical comparison |

## 10. Edge Cases
* **Small $n$ Anomalies**: An $O(n^2)$ algorithm with small constant $T(n) = n^2$ may outperform an $O(n \log n)$ algorithm with huge constant $T(n) = 1000 n \log n$ for small inputs ($n < 100$).
* **Amortized Bounds**: Operations like `ArrayList.add()` take $O(n)$ occasionally during re-allocation but have an amortized tight bound of $\Theta(1)$ over $N$ insertions.

## 11. Common Mistakes
* Misinterpreting Big-O as *only* worst-case (Big-O strictly means upper bound; it can technically describe any upper bound, but in interviews it defaults to worst-case).
* Dropping non-dominant terms prematurely when multiple variables exist (e.g., $O(N + M)$ vs $O(N \cdot M)$).
* Neglecting memory layout overhead when comparing space bounds.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** When a question involves **two separate inputs** (e.g., two arrays `A` of size $N$ and `B` of size $M$), NEVER simplify the time complexity to $O(N)$ or $O(N^2)$! Express it clearly as $O(N + M)$ for sequential processing or $O(N \cdot M)$ for nested processing.

> **Memory Trick:** **"O for Worst, Ω for Best, Θ for Exact"**. Always state worst-case $O(n)$ in technical interviews unless asked specifically for best-case $\Omega(n)$ or tight-bound $\Theta(n)$.

## 13. Comparisons
| Algorithm | Best Case ($\Omega$) | Average Case ($\Theta$) | Worst Case ($O$) |
| :--- | :--- | :--- | :--- |
| **Linear Search** | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ |
| **Binary Search** | $\Omega(1)$ | $\Theta(\log n)$ | $O(\log n)$ |
| **Bubble Sort** | $\Omega(n)$ (optimized) | $\Theta(n^2)$ | $O(n^2)$ |
| **Merge Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n \log n)$ |
| **Quick Sort** | $\Omega(n \log n)$ | $\Theta(n \log n)$ | $O(n^2)$ |

## 14. How to Recognize This in Questions
* **Multiple Inputs**: "Given array `A` of length $N$ and matrix `B` of dimensions $R \times C$" $\rightarrow$ Solution must be expressed in terms of $N, R, C$ (e.g., $O(N + R \cdot C)$).
* **Guaranteed Worst-Case Performance**: "Ensure worst-case time bound is $O(N \log N)$" $\rightarrow$ Prefer Merge Sort or Heap Sort over Quick Sort.

## 15. Frequently Asked Interview Questions
* **Q: Is $O(N)$ the same as $\Theta(N)$?**  
  *A:* No. $O(N)$ specifies an upper bound (the growth rate is at most linear), while $\Theta(N)$ specifies a tight bound (the growth rate is strictly linear).
* **Q: Why is Quick Sort preferred over Merge Sort in practice despite its $O(n^2)$ worst case?**  
  *A:* Quick Sort has smaller constant factors, operates in-place ($O(\log n)$ auxiliary stack space), and exhibits superior CPU cache locality compared to Merge Sort ($O(n)$ extra array allocation).

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: ASYMPTOTIC ANALYSIS                                  |
+-----------------------------------------------------------------------+
| • Big-O (O) = Upper Bound (Worst Case)                                |
| • Big-Omega (Ω) = Lower Bound (Best Case)                             |
| • Big-Theta (Θ) = Tight Bound (Exact Match)                           |
| • Two Inputs (N & M): Always preserve both -> O(N + M) or O(N * M)   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the formal definitions for Big-O, Big-Omega, and Big-Theta.
- [ ] I can derive asymptotic bounds from algorithmic pseudo-code or Java code.
- [ ] I know why Quick Sort is $\Theta(n \log n)$ average but $O(n^2)$ worst case.
- [ ] I can express complexity correctly when multiple input variables ($N, M$) are present.
- [ ] I understand the distinction between worst-case Big-O and tight-bound Big-Theta.
