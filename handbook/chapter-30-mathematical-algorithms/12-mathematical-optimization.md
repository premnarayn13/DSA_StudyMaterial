# 12. Mathematical Optimization: Newton-Raphson Sqrt, Golden Section Search & Continuous Binary Search

## 1. Introduction
**Mathematical Optimization & Numerical Computing** focuses on finding optimal values (roots, minimums, maximums, and continuous roots) for mathematical functions using iterative numerical algorithms. When exact analytical algebraic solutions are impossible or computationally expensive, numerical optimization methods provide rapid, arbitrary-precision convergence. Key foundational algorithms include:
1. **Newton-Raphson Root-Finding Method**: Solves $f(x) = 0$ with **Quadratic Convergence Rate** ($O(\log(\text{precision}))$ iterations). Its prime application is computing square roots (**LeetCode 69 `Sqrt(x)`**) using the recurrence $x_{k+1} = \frac{1}{2} \left( x_k + \frac{N}{x_k} \right)$.
2. **Golden Section Search**: Solves $O(\log(1/\epsilon))$ extremum optimization for **Unimodal Functions** on interval $[L, R]$ using the Golden Ratio $\phi = \frac{\sqrt{5} - 1}{2} \approx 0.618$.
3. **Continuous Real-Domain Binary Search**: Finds continuous function thresholds on $[L, R]$ within precision $\epsilon = 10^{-7}$ in 60-80 iterations.
4. **Fast Fourier Transform (FFT) Concept**: Multiplies two degree-$N$ polynomials in **$O(N \log N)$ Time** instead of naive $O(N^2)$ time.

> **Important:** Core Structural Formulas of Mathematical Optimization:
> 1. **Newton-Raphson Root Recurrence**:
>    $$x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$$
>    - For Square Root $f(x) = x^2 - N = 0$ ($f'(x) = 2x$):
>      $$x_{k+1} = \frac{1}{2} \left( x_k + \frac{N}{x_k} \right)$$
> 2. **Golden Section Search Ratio**:
>    $$\phi = \frac{\sqrt{5} - 1}{2} \approx 0.6180339887...$$
>    - Probe points: $x_1 = R - \phi (R - L)$ and $x_2 = L + \phi (R - L)$.
> 3. **Continuous Real Binary Search Loop**:
>    - Loop for fixed 60-80 iterations or while $(R - L) > 10^{-7}$ to avoid floating-point infinite loops! ⚡

```
Newton-Raphson Square Root Tangent Convergence Topology (N = 25):

Goal: Compute sqrt(25). Initial Guess x_0 = 25.

Iteration 1: x_1 = 0.5 * (25 + 25/25) = 0.5 * (25 + 1) = 13.0
Iteration 2: x_2 = 0.5 * (13 + 25/13) = 0.5 * (13 + 1.923) = 7.461
Iteration 3: x_3 = 0.5 * (7.461 + 25/7.461) = 0.5 * (7.461 + 3.350) = 5.406
Iteration 4: x_4 = 0.5 * (5.406 + 25/5.406) = 0.5 * (5.406 + 4.624) = 5.015
Iteration 5: x_5 = 0.5 * (5.015 + 25/5.015) = 5.000002!
Iteration 6: x_6 = 5.000000000000000!

Achieves double-precision 15-decimal accuracy in ONLY 6 iterations! ✅ ⚡
```

---

## 2. Core Concepts & Mathematical Optimization Strategy Matrix

### 2.1 Mathematical Optimization Strategy Matrix
```
Mathematical Optimization Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Optimization Engine   | Target Problem    | Time Complexity   | Precision Rate    | Primary Requirement|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Newton-Raphson**    | Root $f(x) = 0$   | **$O(\log(\text{prec}))$ ⚡**| **Quadratic Rate ⚡**| Differentiable $f'(x)$|
| **Golden Section**    | Max/Min $f(x)$    | **$O(\log(1/\epsilon))$⚡**| Linear Rate ($\phi$)| **Unimodal Function⚡**|
| **Continuous BS**     | Monotonic Threshold| **$O(\log(1/\epsilon))$⚡**| Binary Bisection  | Monotonic Function|
| **Fast Fourier (FFT)**| Poly Multiply     | **$O(N \log N)$ Fast⚡**| Complex Roots $e^{i\theta}$| Complex numbers   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Newton-Raphson Sqrt: x = 0.5 * (x + N / x); Golden Section probes with golden ratio 0.618 for unimodal functions; Continuous BS uses fixed 60-80 iterations!"**

---

## 3. Characteristics & Newton-Raphson Quadratic Convergence Proof

### 3.1 Mathematical Derivation of Newton-Raphson Quadratic Convergence
* Let $r$ be the true root of $f(x) = 0$ ($f(r) = 0$).
* Let $x_k$ be the estimate at iteration $k$, and $\epsilon_k = x_k - r$ be the error.
* Expand $f(r)$ using Taylor's Theorem around $x_k$:
  $$0 = f(r) = f(x_k - \epsilon_k) = f(x_k) - \epsilon_k f'(x_k) + \frac{\epsilon_k^2}{2} f''(c) \quad \text{for some } c \text{ between } r \text{ and } x_k$$
* Rearranging for $f(x_k)$:
  $$f(x_k) = \epsilon_k f'(x_k) - \frac{\epsilon_k^2}{2} f''(c)$$
* Substitute into Newton-Raphson update equation $x_{k+1} = x_k - \frac{f(x_k)}{f'(x_k)}$:
  $$x_{k+1} = x_k - \frac{\epsilon_k f'(x_k) - \frac{\epsilon_k^2}{2} f''(c)}{f'(x_k)} = (x_k - \epsilon_k) + \frac{\epsilon_k^2}{2} \frac{f''(c)}{f'(x_k)}$$
* Since $r = x_k - \epsilon_k$, the new error $\epsilon_{k+1} = x_{k+1} - r$ is:
  $$\epsilon_{k+1} = \left( \frac{f''(c)}{2 f'(x_k)} \right) \cdot \epsilon_k^2 = M \cdot \epsilon_k^2$$
* **Quadratic Convergence**: The error at step $k+1$ is proportional to the **SQUARE** of the error at step $k$. The number of correct decimal digits **DOUBLES** at every iteration! ⚡

---

## 4. Internal Working Mechanics: Golden Section Search Engine

Tracing Golden Section Minimum Search on Unimodal Function $f(x) = (x - 3)^2 + 5$ on $[L = 0, R = 10]$:

```
Golden Ratio phi = (sqrt(5) - 1) / 2 ≈ 0.618034.

Iteration 1:
- Probe x1 = R - phi * (R - L) = 10 - 0.618034 * 10 = 3.81966.
- Probe x2 = L + phi * (R - L) = 0 + 0.618034 * 10  = 6.18034.
- Evaluate f(x1) = (3.81966 - 3)^2 + 5 = 5.6718.
- Evaluate f(x2) = (6.18034 - 3)^2 + 5 = 15.114.

Since f(x1) < f(x2):
Minimum must lie in left sub-interval [0, 6.18034]! Update R = x2 = 6.18034! ⚡

Shrinks interval by factor phi = 0.618 at every step until precision eps is reached! ✅ ⚡
```

---

## 5. Visual Diagram: Continuous Real Domain Binary Search

```
Continuous Real Domain Binary Search Interval Reduction:

Search Space: [ L = 0.0 ........................................ R = 100.0 ]
                                         │
Iterative Bisection (60 Fixed Iterations):
- Step 1:  Interval = 50.0
- Step 2:  Interval = 25.0
- Step 10: Interval = 0.0976
- Step 30: Interval = 9.31 * 10^-8
- Step 60: Interval = 8.67 * 10^-17 (Double Precision Machine Limit!) ⚡

Eliminates floating-point comparison errors (`R - L > eps`) completely! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Newton-Raphson Square Root (LeetCode 69), Golden Section Unimodal Search, and Continuous Real Domain Binary Search.

```java
import java.util.*;
import java.util.function.DoubleUnaryOperator;

/**
 * Production-Grade Master Suite Implementing Mathematical Optimization:
 * Newton-Raphson Sqrt (LeetCode 69), Golden Section Search, and Continuous Real Binary Search.
 */
public class MathematicalOptimizationMaster {

    // =========================================================================
    // 1. LEETCODE 69: NEWTON-RAPHSON SQUARE ROOT (O(log(prec)) Quadratic Rate)
    // =========================================================================
    /**
     * Solves LeetCode 69 mySqrt(n) for integer n using Newton-Raphson method.
     *
     * @param n target non-negative integer
     * @return truncated integer square root
     */
    public int mySqrtNewtonRaphson(int n) {
        if (n < 2) return n;

        double x = n; // Initial guess ⚡
        double root;

        while (true) {
            root = 0.5 * (x + n / x); // Newton-Raphson Sqrt Recurrence ⚡
            if (Math.abs(x - root) < 1e-7) { // Double precision convergence ⚡
                break;
            }
            x = root;
        }

        return (int) root;
    }

    /**
     * Computes double-precision square root using Newton-Raphson method.
     */
    public double sqrtDouble(double n) {
        if (n < 0) return Double.NaN;
        if (n == 0) return 0.0;

        double x = n;
        for (int i = 0; i < 20; i++) { // 20 iterations achieves 15-decimal precision! ⚡
            x = 0.5 * (x + n / x);
        }

        return x;
    }

    // =========================================================================
    // 2. GOLDEN SECTION SEARCH FOR UNIMODAL FUNCTIONS (O(log(1/eps)) Time)
    // =========================================================================
    private static final double PHI = (Math.sqrt(5.0) - 1.0) / 2.0; // 0.6180339887 ⚡

    /**
     * Finds x in [left, right] that MINIMIZES unimodal function f(x).
     */
    public double findMinimumGoldenSection(DoubleUnaryOperator f, double left, double right, double eps) {
        double x1 = right - PHI * (right - left);
        double x2 = left + PHI * (right - left);
        double f1 = f.applyAsDouble(x1);
        double f2 = f.applyAsDouble(x2);

        while ((right - left) > eps) {
            if (f1 < f2) {
                right = x2;
                x2 = x1;
                f2 = f1;
                x1 = right - PHI * (right - left);
                f1 = f.applyAsDouble(x1);
            } else {
                left = x1;
                x1 = x2;
                f1 = f2;
                x2 = left + PHI * (right - left);
                f2 = f.applyAsDouble(x2);
            }
        }

        return (left + right) / 2.0;
    }

    // =========================================================================
    // 3. CONTINUOUS REAL DOMAIN BINARY SEARCH (FIXED 60 ITERATIONS)
    // =========================================================================
    /**
     * Solves monotonic function f(x) = target on [left, right] using fixed 60 iterations.
     */
    public double binarySearchContinuous(DoubleUnaryOperator f, double target, double left, double right) {
        // Fixed 60 iterations guarantees 10^-17 precision without floating loops! ⚡
        for (int iter = 0; iter < 60; iter++) {
            double mid = left + (right - left) / 2.0;
            double val = f.applyAsDouble(mid);

            if (val < target) {
                left = mid;
            } else {
                right = mid;
            }
        }

        return left + (right - left) / 2.0;
    }
}
```

> **Quick Syntax:**
```java
// Mathematical Optimization Core Lines
x = 0.5 * (x + n / x); // Newton-Raphson Sqrt Recurrence
for (int iter = 0; iter < 60; iter++) { double mid = left + (right - left) / 2.0; ... } // Real BS
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 69 - Sqrt(x)**:
   - Newton-Raphson integer square root benchmark ($O(\log(\text{prec}))$ time).

2. **LeetCode 367 - Valid Perfect Square**:
   - Newton-Raphson square convergence verification.

3. **Optimal Search in Physics / Machine Learning**:
   - Golden Section Search for parameter tuning on unimodal loss functions.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class MathematicalOptimizationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MATHEMATICAL OPTIMIZATION BENCHMARK DEMO      ");
        System.out.println("=================================================\n");

        MathematicalOptimizationMaster master = new MathematicalOptimizationMaster();

        // 1. LeetCode 69 Newton-Raphson Sqrt Test
        int n = 2147395600; // Sqrt = 46340
        int sqrtInt = master.mySqrtNewtonRaphson(n);

        System.out.println("1. Newton-Raphson Sqrt for 2,147,395,600 (LeetCode 69):");
        System.out.println("   Truncated Sqrt Result: " + sqrtInt + " (Optimal = 46340)");
        System.out.println("-------------------------------------------------");

        // 2. Golden Section Search Minimum Test (f(x) = (x - 3)^2 + 5)
        double minX = master.findMinimumGoldenSection(x -> (x - 3) * (x - 3) + 5, 0.0, 10.0, 1e-7);
        System.out.println("2. Golden Section Search for Min of f(x) = (x - 3)^2 + 5:");
        System.out.println("   Minimizing X Value: " + String.format("%.6f", minX) + " (Optimal = 3.000000)");
        System.out.println("-------------------------------------------------");

        // 3. Continuous Real Binary Search Test (Find x where x^3 = 27)
        double cubeRoot = master.binarySearchContinuous(x -> x * x * x, 27.0, 0.0, 10.0);
        System.out.println("3. Continuous Real Binary Search (Cube Root of 27):");
        System.out.println("   Cube Root Result: " + String.format("%.6f", cubeRoot) + " (Optimal = 3.000000)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Optimization Engine | Target Function Type | Time Complexity | Convergence Rate | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Newton-Raphson** | Differentiable $f(x)=0$ | $\mathbf{O(\log(\text{prec}))}$ ⚡| **Quadratic ($E_{k+1} \propto E_k^2$)⚡**| $x = 0.5(x + N/x)$ |
| **Golden Section** | Unimodal Min/Max | $\mathbf{O(\log(1/\epsilon))}$⚡| Linear ($\phi \approx 0.618$) | Probe ratio $\phi$ |
| **Continuous BS** | Monotonic Threshold| $\mathbf{O(\log(1/\epsilon))}$⚡| Bisection (Fixed 60) | Fixed 60 iterations |

---

## 10. Edge Cases & Boundary Handling

1. **Input $N = 0$ in Sqrt**:
   - Returns 0.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using While Loop Condition `while (right - left > eps)` for Real Binary Search**:
  - Continuous floating-point subtraction can cause infinite loops due to double precision rounding limits. **ALWAYS use a fixed loop `for (int iter = 0; iter < 60; iter++)` for continuous real binary search!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Real Domain Binary Search Rule:
> When performing Binary Search on real floating-point numbers (`double`), ALWAYS use a fixed loop of **60 to 80 iterations**, preventing infinite loops caused by machine precision bounds! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Search Step | Newton-Raphson |
| :--- | :--- | :--- |
| **Convergence Rate** | Linear | **Quadratic (Digits Double Each Step!) ⚡** |
| **Iterations for 15 Digits**| Millions of steps | **6 Iterations ⚡** |
| **Speedup** | Slow | **Instant Precision ⚡** |

---

## 14. How to Recognize This in Questions

* **"Compute integer square root without built-in sqrt functions"** $\rightarrow$ LeetCode 69 (Newton-Raphson `x = 0.5 * (x + n / x)`).
* **"Find maximum/minimum of a unimodal continuous function"** $\rightarrow$ Golden Section Search.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Newton-Raphson compute square roots so quickly?**  
  *A:* By using the tangent line update $x_{k+1} = \frac{1}{2} \left( x_k + \frac{N}{x_k} \right)$, which exhibits quadratic convergence (the number of accurate decimal digits doubles at every step).

* **Q: Why are fixed 60 iterations preferred over `while (right - left > eps)` for continuous real binary search?**  
  *A:* Because `60` iterations reduces the search interval by $2^{60} \approx 1.15 \times 10^{18}$, which reaches double-precision floating-point machine epsilon ($10^{-16}$) without risk of infinite loops.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATHEMATICAL OPTIMIZATION                             |
+-----------------------------------------------------------------------+
| • Newton-Raphson Sqrt: x = 0.5 * (x + N / x) (LeetCode 69 O(log prec))|
| • Convergence Rate   : Quadratic (Correct decimal digits double!) ⚡   |
| • Golden Section     : Unimodal min/max search using phi = 0.618       |
| • Continuous BS      : Use fixed 60 iterations for double binary search|
| • Safety Rule        : Prevents floating-point infinite loops! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Newton-Raphson integer square root (LeetCode 69) in Java.
- [ ] I can write Golden Section search for unimodal functions in Java.
- [ ] I can write continuous real domain binary search using fixed 60 iterations.
- [ ] I can explain why Newton-Raphson exhibits quadratic convergence.
- [ ] I can state why fixed 60 iterations prevents floating-point infinite loops.
