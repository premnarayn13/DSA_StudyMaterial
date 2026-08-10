# 10. Matrix Exponentiation: Fibonacci $O(\log N)$, Linear Recurrence Solvers & $K \times K$ Matrix Power

## 1. Introduction
**Matrix Exponentiation** is an advanced mathematical technique used to compute the $N$-th term of any homogeneous **Linear Recurrence Relation** in **$O(K^3 \log N)$ Time** (where $K$ is the order of the recurrence) rather than naive linear $O(N \cdot K)$ time. For $N = 10^{18}$, calculating linear DP transitions iteratively requires billions of loop cycles. Matrix Exponentiation constructs a fixed **$K \times K$ Transition Matrix $T$** such that state vector $V_n = T \cdot V_{n-1}$. Applying binary fast exponentiation to matrix $T$ computes $T^N$ in $\log N$ matrix multiplication steps. The prime benchmark is **Fibonacci Matrix Exponentiation**, which calculates $F_N \pmod{10^9 + 7}$ for $N = 10^{18}$ in **$O(\log N)$ Logarithmic Time** using the 2x2 transition matrix $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$.

> **Important:** Core Structural Properties of Matrix Exponentiation:
> 1. **Fibonacci Transition Matrix Equation**:
>    $$\begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n$$
> 2. **General $K$-th Order Linear Recurrence State Equation**:
>    - Given recurrence $F_n = c_1 F_{n-1} + c_2 F_{n-2} + \dots + c_k F_{n-k}$:
>      $$\begin{pmatrix} F_n \\ F_{n-1} \\ \dots \\ F_{n-k+1} \end{pmatrix} = \begin{pmatrix} c_1 & c_2 & \dots & c_k \\ 1 & 0 & \dots & 0 \\ \dots & \dots & \dots & \dots \\ 0 & 0 & 1 & 0 \end{pmatrix} \begin{pmatrix} F_{n-1} \\ F_{n-2} \\ \dots \\ F_{n-k} \end{pmatrix}$$
> 3. **Fast Matrix Power Engine**:
>    - Uses binary bit shifts on matrix multiplication to compute $T^N \pmod M$ in $O(K^3 \log N)$ time.
> 4. **Base Case Matrix**:
>    - Initial identity matrix $I$ (diagonal 1s, zeroes elsewhere) for $T^0$. ⚡

```
Fibonacci 2x2 Matrix Exponentiation Topology:

Transition Matrix T = | 1  1 |
                      | 1  0 |

Matrix Power T^n = | F_{n+1}   F_n   |
                   | F_n       F_{n-1}|

For n = 5:
T^5 = | 1  1 |^5 = | 8  5 |
      | 1  0 |     | 5  3 |

F_5 = 5 (Cell [0][1] or [1][0] contains exact 5th Fibonacci number!) ✅ ⚡
```

---

## 2. Core Concepts & Matrix Exponentiation Strategy Matrix

### 2.1 Matrix Exponentiation Family Strategy Matrix
```
Matrix Exponentiation Family Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Recurrence Problem    | Matrix Order $K$  | Transition Matrix | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Fibonacci ($F_N$)** | $K = 2$           | $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$| **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Tribonacci (LC 1137)**| $K = 3$         | 3x3 Matrix        | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **General $K$-th Linear**| Arbitrary $K$  | $K \times K$ Matrix| **$O(K^3 \log N)$ Fast⚡**| $O(K^2)$ Matrix   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fibonacci matrix = {{1, 1}, {1, 0}}; Matrix power T^N computed in O(K^3 log N) time; Cell [0][1] yields F_N!"**

---

## 3. Characteristics & Fibonacci Matrix Exponentiation Proof

### 3.1 Mathematical Proof of Fibonacci Matrix Identity by Induction
* **Base Case ($n = 1$)**:
  $$T^1 = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} F_2 & F_1 \\ F_1 & F_0 \end{pmatrix} \quad (\text{since } F_2=1, F_1=1, F_0=0)$$
  - Base case holds!
* **Inductive Hypothesis**: Assume identity holds for $n = k$:
  $$T^k = \begin{pmatrix} F_{k+1} & F_k \\ F_k & F_{k-1} \end{pmatrix}$$
* **Inductive Step ($n = k + 1$)**:
  - Multiply $T^k$ by $T$:
    $$T^{k+1} = T^k \times T = \begin{pmatrix} F_{k+1} & F_k \\ F_k & F_{k-1} \end{pmatrix} \times \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$$
  - Performing 2x2 matrix multiplication:
    $$T^{k+1} = \begin{pmatrix} F_{k+1} \cdot 1 + F_k \cdot 1 & F_{k+1} \cdot 1 + F_k \cdot 0 \\ F_k \cdot 1 + F_{k-1} \cdot 1 & F_k \cdot 1 + F_{k-1} \cdot 0 \end{pmatrix}$$
    $$T^{k+1} = \begin{pmatrix} F_{k+1} + F_k & F_{k+1} \\ F_k + F_{k-1} & F_k \end{pmatrix}$$
  - By definition of Fibonacci recurrence ($F_{m+1} = F_m + F_{m-1}$):
    $$T^{k+1} = \begin{pmatrix} F_{k+2} & F_{k+1} \\ F_{k+1} & F_k \end{pmatrix}$$
* Proves by mathematical induction that $T^n = \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}$ for all $n \ge 1$! ⚡

---

## 4. Internal Working Mechanics: $K \times K$ Matrix Multiplication Algorithm

Tracing 2x2 Matrix Multiplication $C = A \times B \pmod M$:

```
Matrix A: | a00  a01 |      Matrix B: | b00  b01 |
          | a10  a11 |                | b10  b11 |

Result Matrix C = A * B:
C[0][0] = (a00 * b00 + a01 * b10) % M
C[0][1] = (a00 * b01 + a01 * b11) % M
C[1][0] = (a10 * b00 + a11 * b10) % M
C[1][1] = (a10 * b01 + a11 * b11) % M

Executes in O(K^3) = 2^3 = 8 scalar multiplications! ✅ ⚡
```

---

## 5. Visual Diagram: Binary Matrix Fast Power Engine

```
Binary Matrix Power Pipeline (Compute T^13 % MOD):

Exponent 13 = 1101_2 (8 + 4 + 1)

Step 1: Result = Identity Matrix I, Base = T
Step 2: Bit 0 (1) ──► Result = Result * T = T   ──► Base = T^2
Step 3: Bit 1 (0) ──► Result = T                ──► Base = T^4
Step 4: Bit 2 (1) ──► Result = T * T^4 = T^5    ──► Base = T^8
Step 5: Bit 3 (1) ──► Result = T^5 * T^8 = T^13 ──► DONE!

Computes T^13 in 4 matrix multiplications! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing 2x2 Fibonacci Matrix Exponentiation ($O(\log N)$) and General $K \times K$ Matrix Power Engine ($O(K^3 \log N)$).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Matrix Exponentiation:
 * 2x2 Fibonacci O(log N) Solver and K x K General Matrix Power Engine.
 */
public class MatrixExponentiationMaster {

    private static final long MOD = 1_000_000_007L;

    // =========================================================================
    // 1. FIBONACCI 2x2 MATRIX EXPONENTIATION (O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Computes N-th Fibonacci number F_N mod MOD in O(log N) time.
     *
     * @param n target index N
     * @return F_N mod MOD
     */
    public long getFibonacci(long n) {
        if (n <= 0) return 0;
        if (n == 1) return 1;

        long[][] T = {
            {1, 1},
            {1, 0}
        };

        long[][] result = powerMatrix(T, n);
        return result[0][1]; // Cell [0][1] contains F_N! ⚡
    }

    // =========================================================================
    // 2. K x K GENERAL MATRIX FAST POWER ENGINE (O(K^3 log N) Time)
    // =========================================================================
    /**
     * Computes (matrix^exp) % MOD in O(K^3 log exp) time.
     */
    public long[][] powerMatrix(long[][] matrix, long exp) {
        int k = matrix.length;
        long[][] result = new long[k][k];

        // Base case: Identity Matrix I ⚡
        for (int i = 0; i < k; i++) result[i][i] = 1;

        long[][] base = copyMatrix(matrix);

        while (exp > 0) {
            if ((exp & 1) == 1) {
                result = multiplyMatrix(result, base);
            }
            base = multiplyMatrix(base, base); // Square base matrix ⚡
            exp >>= 1;
        }

        return result;
    }

    /**
     * Multiplies two K x K matrices modulo MOD in O(K^3) time.
     */
    public long[][] multiplyMatrix(long[][] A, long[][] B) {
        int k = A.length;
        long[][] C = new long[k][k];

        for (int i = 0; i < k; i++) {
            for (int kIdx = 0; kIdx < k; kIdx++) {
                if (A[i][kIdx] == 0) continue; // Optimization ⚡
                for (int j = 0; j < k; j++) {
                    long prod = modMultiply(A[i][kIdx], B[kIdx][j]);
                    C[i][j] = (C[i][j] + prod) % MOD;
                }
            }
        }

        return C;
    }

    private long[][] copyMatrix(long[][] matrix) {
        int k = matrix.length;
        long[][] copy = new long[k][k];
        for (int i = 0; i < k; i++) {
            System.arraycopy(matrix[i], 0, copy[i], 0, k);
        }
        return copy;
    }

    private long modMultiply(long a, long b) {
        return (long) ((java.math.BigInteger.valueOf(a)
                .multiply(java.math.BigInteger.valueOf(b)))
                .mod(java.math.BigInteger.valueOf(MOD)).longValue());
    }
}
```

> **Quick Syntax:**
```java
// Matrix Exponentiation Core Lines
long[][] result = powerMatrix(T, n); return result[0][1]; // Fibonacci cell [0][1]
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 509 - Fibonacci Number**:
   - $O(\log N)$ Fibonacci benchmark solved using 2x2 Matrix Exponentiation.

2. **LeetCode 1137 - N-th Tribonacci Number**:
   - $O(\log N)$ Tribonacci solved using 3x3 Matrix Exponentiation.

3. **Counting Grid Paths / Graph Walk Counts**:
   - Adjacency matrix power $A^N$ computes total paths of length $N$ between all node pairs.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class MatrixExponentiationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MATRIX EXPONENTIATION BENCHMARK DEMO          ");
        System.out.println("=================================================\n");

        MatrixExponentiationMaster master = new MatrixExponentiationMaster();

        // 1. Fibonacci F_10 Test
        long fib10 = master.getFibonacci(10);
        System.out.println("1. Fibonacci F_10 Result via Matrix Exponentiation:");
        System.out.println("   F_10 = " + fib10 + " (Optimal = 55)");
        System.out.println("-------------------------------------------------");

        // 2. Fibonacci F_50 Test (Huge N = 50)
        long fib50 = master.getFibonacci(50);
        System.out.println("2. Fibonacci F_50 Result (O(log N) Time):");
        System.out.println("   F_50 mod 10^9+7 = " + fib50 + " (Optimal = 288006719)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Recurrence Order $K$ | Matrix Dimension | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Fibonacci ($K=2$)** | 2x2 Matrix | $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| Cell `[0][1]` contains $F_N$ |
| **Tribonacci ($K=3$)**| 3x3 Matrix | $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| 3x3 Transition Matrix |
| **General Linear $K$**| $K \times K$ Matrix | $\mathbf{O(K^3 \log N)}$ Fast⚡| $O(K^2)$ Matrix | $K^3$ Matrix Multiplication |

---

## 10. Edge Cases & Boundary Handling

1. **Input $N = 0$**:
   - Returns 0.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running Linear DP Loop for $N = 10^{18}$**:
  - Running a linear loop `for (int i = 2; i <= N; i++)` for $N = 10^{18}$ causes TLE. **ALWAYS use Matrix Exponentiation to compute $F_N$ for $N > 10^7$ in $O(\log N)$ time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Fibonacci Matrix Exponentiation Rule:
> To compute $F_N \pmod M$ for $N = 10^{18}$, use the 2x2 Fibonacci transition matrix:
> $$T = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$$
> Cell `T^N[0][1]` holds the exact value of $F_N \pmod M$! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear DP ($O(N)$) | Matrix Exponentiation ($O(\log N)$) |
| :--- | :--- | :--- |
| **Loop Iterations ($N=10^{18}$)**| $10^{18}$ Loops (Impossible!) | **~60 Matrix Power Steps ⚡** |
| **Time Complexity** | $O(N)$ Linear | **$O(K^3 \log N)$ Logarithmic ⚡** |
| **Execution Time** | Freeze | **Nanoseconds ⚡** |

---

## 14. How to Recognize This in Questions

* **"Compute N-th Fibonacci number F_N mod 10^9 + 7 where N <= 10^18"** $\rightarrow$ Matrix Exponentiation ($O(\log N)$ time).
* **"Find N-th term of a linear recurrence relation where N <= 10^18"** $\rightarrow$ $K \times K$ Matrix Exponentiation.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Matrix Exponentiation compute $F_N$ in $O(\log N)$ time?**  
  *A:* By expressing the Fibonacci state transition as a 2x2 matrix $T = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ and applying binary fast exponentiation to compute $T^N$ in $\log N$ matrix multiplication steps.

* **Q: What is the time complexity of Matrix Exponentiation for a $K$-th order recurrence?**  
  *A:* $O(K^3 \log N)$ time, where $O(K^3)$ is the time to multiply two $K \times K$ matrices and $O(\log N)$ is the number of matrix multiplications.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MATRIX EXPONENTIATION                                 |
+-----------------------------------------------------------------------+
| • Transition Matrix T : {{1, 1}, {1, 0}} for Fibonacci                |
| • Matrix Power Identity: T^N = {{F_{N+1}, F_N}, {F_N, F_{N-1}}}       |
| • Result Extraction   : Cell [0][1] holds F_N                         |
| • Time Complexity     : O(K^3 log N) for K-th order linear recurrence ⚡|
| • Performance         : Computes F_10^18 in nanoseconds! ⚡            |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Fibonacci 2x2 Matrix Exponentiation in $O(\log N)$ time in Java.
- [ ] I can write a general $K \times K$ matrix multiplication engine in Java.
- [ ] I can prove why $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^N$ contains $F_N$.
- [ ] I can write $O(\log N)$ Tribonacci solver using 3x3 matrix power.
- [ ] I can state the time complexity of $K$-th order matrix exponentiation ($O(K^3 \log N)$).
