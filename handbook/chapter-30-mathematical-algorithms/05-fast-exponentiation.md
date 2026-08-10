# 05. Fast Exponentiation: Binary Exponentiation, Squaring & LeetCode 50 Pow(x, n)

## 1. Introduction
**Fast Exponentiation** (also known as **Binary Exponentiation** or **Exponentiation by Squaring**) is an algorithmic technique designed to compute $A^N \pmod M$ (or floating-point power $x^n$) in **$O(\log N)$ Logarithmic Time** rather than linear $O(N)$ time. Computing $A^N$ naively via repeated multiplication requires $N - 1$ multiplication operations. For $N = 10^{18}$, linear iteration takes over 31 years of computation! Fast Exponentiation reduces the total multiplications to at most $2 \lfloor \log_2 N \rfloor$ by expressing exponent $N$ as a binary integer $\sum b_i \cdot 2^i$ and repeatedly squaring the base ($A^{2^i}$). Fast Exponentiation forms the core execution engine of Matrix Exponentiation, Modular Inverses, RSA Encryption, and **LeetCode 50 (`Pow(x, n)`)**.

> **Important:** Core Structural Properties of Fast Exponentiation:
> 1. **Binary Exponentiation Recurrence Identity**:
>    $$A^N = \begin{cases} 1 & \text{if } N = 0 \\ (A^2)^{N/2} & \text{if } N \text{ is even} \\ A \times (A^2)^{(N-1)/2} & \text{if } N \text{ is odd} \end{cases}$$
> 2. **Binary Bit Shift Iterative Engine**:
>    - Scan bits of exponent $N$ from right to left (LSB to MSB):
>      - If LSB bit is 1 (`(N & 1) == 1`): `result = (result * base) % M`.
>      - Square base at every step: `base = (base * base) % M`.
>      - Shift exponent right: `N >>= 1`.
> 3. **LeetCode 50 Negative Exponent Handling**:
>    - For negative exponent $N < 0$: $x^N = \left(\frac{1}{x}\right)^{-N}$.
>    - Guard against `Integer.MIN_VALUE` overflow ($-(-2^{31}) = 2^{31}$ exceeds signed 32-bit int) by casting exponent to 64-bit `long`! ⚡

```
Fast Exponentiation Execution Topology (Compute 3^13 % MOD):

Exponent 13 in Binary: 1101_2 (13 = 8 + 4 + 1)

Step-by-Step Bit Scan (LSB to MSB):
- Initial: result = 1, base = 3, exp = 13 (1101_2)

Bit 0 (LSB = 1): result = (1 * 3) = 3 ──► base = 3^2 = 9,   exp = 6 (0110_2)
Bit 1 (LSB = 0): result = 3           ──► base = 9^2 = 81,  exp = 3 (0011_2)
Bit 2 (LSB = 1): result = (3 * 81) = 243 ──► base = 81^2 = 6561, exp = 1 (0001_2)
Bit 3 (LSB = 1): result = (243 * 6561) % MOD = 1,594,323!

Computed 3^13 in EXACTLY 4 squarings instead of 13 multiplications! ⚡
```

---

## 2. Core Concepts & Fast Exponentiation Strategy Matrix

### 2.1 Fast Exponentiation Family Strategy Matrix
```
Fast Exponentiation Family Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Variant       | Target Data Type  | Core Mechanism    | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Modular Fast Power**| $A^N \pmod M$     | Binary Bit Shifts | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Floating Pow(x, n)**| `double x^n`      | Binary Squaring   | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **Matrix Fast Power** | Matrix $M^N$      | Binary Matrix Mul | **$O(K^3 \log N)$ Fast⚡**| **$O(K^2)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fast power: while (exp > 0) { if ((exp & 1) == 1) res = (res * base) % M; base = (base * base) % M; exp >>= 1; }!"**

---

## 3. Characteristics & Logarithmic Time Complexity Proof

### 3.1 Mathematical Proof of $O(\log N)$ Time Complexity
* Let $N$ be a positive integer exponent.
* The binary representation of $N$ has length $L = \lfloor \log_2 N \rfloor + 1$ bits.
* In each iteration of the while loop (`exp >>= 1`), the exponent $N$ is divided by 2.
* **Loop Iterations Count**:
  - The loop terminates when $N = 0$, executing exactly $L = \lfloor \log_2 N \rfloor + 1$ iterations.
* **Multiplications Per Iteration**:
  - Exactly 1 base squaring operation (`base = base * base`).
  - At most 1 result multiplication operation (`if ((N & 1) == 1) res = res * base`).
* **Total Multiplication Operations**:
  $$\text{Total Multiplications} \le 2 \times (\lfloor \log_2 N \rfloor + 1) = O(\log N)$$
* For $N = 10^{18}$: $\log_2(10^{18}) \approx 60$ iterations.
* Speedup Factor: Over $16,000,000,000,000,000\times$ FASTER than naive iteration! ⚡

---

## 4. Internal Working Mechanics: LeetCode 50 `Pow(x, n)` Negative Exponent Handling

Tracing LeetCode 50 for $x = 2.0$, $n = -2147483648$ (`Integer.MIN_VALUE`):

```
Target: Compute 2.0^(-2147483648).

Danger Zone:
If we try N = -n on 32-bit signed int:
N = -(-2147483648) = 2147483648 (EXCEEDS Integer.MAX_VALUE 2147483647!).
Causes 32-bit Integer Overflow back to -2147483648! ❌

Production Fix (Cast to 64-bit long):
long exp = n; // exp = -2147483648L
if (exp < 0) {
    x = 1.0 / x;   // Base becomes 0.5
    exp = -exp;    // exp becomes 2147483648L (Fits safely in 64-bit long!) ✅ ⚡
}

Result = 0.0 (Underflows to 0.0 accurately in O(31) squarings!) ✅ ⚡
```

---

## 5. Visual Diagram: Binary Exponentiation Bit Scanning

```
Binary Bit Scanning Pipeline for Exp = 25 (11001_2):

Bits:         Bit 4 (1) ──► Bit 3 (1) ──► Bit 2 (0) ──► Bit 1 (0) ──► Bit 0 (1)
Square Base:   base^16       base^8        base^4        base^2        base^1
Multiply Res:  YES           YES           NO            NO            YES

Result = base^1 * base^8 * base^16 = base^(1 + 8 + 16) = base^25! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Modular Fast Exponentiation ($O(\log N)$) and LeetCode 50 (`Pow(x, n)`).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Fast Exponentiation:
 * Modular Binary Exponentiation, LeetCode 50 Pow(x, n), and Overflow Protection.
 */
public class FastExponentiationMaster {

    // =========================================================================
    // 1. MODULAR FAST EXPONENTIATION (O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Computes (base^exp) % mod in O(log exp) time.
     *
     * @param base base integer
     * @param exp exponent non-negative integer
     * @param mod modulus integer
     * @return (base^exp) % mod
     */
    public long powerModular(long base, long exp, long mod) {
        if (mod <= 0) return 0;
        long res = 1;
        base = (base % mod + mod) % mod; // Non-negative base ⚡

        while (exp > 0) {
            // If LSB of exp is 1, multiply base into result
            if ((exp & 1) == 1) {
                res = (long) ((java.math.BigInteger.valueOf(res)
                        .multiply(java.math.BigInteger.valueOf(base)))
                        .mod(java.math.BigInteger.valueOf(mod)).longValue());
            }

            // Square base for next bit position ⚡
            base = (long) ((java.math.BigInteger.valueOf(base)
                    .multiply(java.math.BigInteger.valueOf(base)))
                    .mod(java.math.BigInteger.valueOf(mod)).longValue());

            exp >>= 1; // Shift exponent right by 1 bit ⚡
        }

        return res;
    }

    // =========================================================================
    // 2. LEETCODE 50: POW(X, N) DOUBLE PRECISION (O(log N) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves LeetCode 50 Pow(x, n) for floating point x and signed 32-bit int n.
     */
    public double myPow(double x, int n) {
        long N = n; // Cast to long to handle Integer.MIN_VALUE (-2^31) ⚡
        if (N < 0) {
            x = 1.0 / x;
            N = -N;
        }

        double res = 1.0;
        double currentProduct = x;

        while (N > 0) {
            if ((N & 1) == 1) {
                res = res * currentProduct;
            }
            currentProduct = currentProduct * currentProduct; // Square base ⚡
            N >>= 1;
        }

        return res;
    }
}
```

> **Quick Syntax:**
```java
// Fast Exponentiation Core Lines
while (exp > 0) { if ((exp & 1) == 1) res = (res * base) % mod; base = (base * base) % mod; exp >>= 1; }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 50 - Pow(x, n)**:
   - Floating-point binary exponentiation benchmark ($O(\log N)$ time).

2. **Fermat's Little Theorem Modular Inverse ($A^{M-2} \bmod M$)**:
   - Computing modular inverse in $O(\log M)$ time using fast exponentiation.

3. **Matrix Exponentiation for $N$-th Fibonacci ($O(\log N)$ time)**:
   - Computing Fibonacci numbers for $N = 10^{18}$ using 2x2 matrix fast power.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class FastExponentiationDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   FAST EXPONENTIATION BENCHMARK DEMO            ");
        System.out.println("=================================================\n");

        FastExponentiationMaster master = new FastExponentiationMaster();
        long M = 1_000_000_007L;

        // 1. Modular Fast Exponentiation Test (3^13 % MOD)
        long base = 3, exp = 13;
        long modPow = master.powerModular(base, exp, M);
        System.out.println("1. Modular Fast Power (3^13) % 10^9+7:");
        System.out.println("   Result: " + modPow + " (Optimal = 1594323)");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 50 Pow(x, n) Test
        double x = 2.0;
        int n = 10;
        double powResult = master.myPow(x, n);
        System.out.println("2. LeetCode 50 Pow(2.0, 10):");
        System.out.println("   Result: " + powResult + " (Optimal = 1024.0)");
        System.out.println("-------------------------------------------------");

        // 3. LeetCode 50 Negative Exponent & MIN_VALUE Test
        double negPow = master.myPow(2.0, -2);
        System.out.println("3. LeetCode 50 Pow(2.0, -2):");
        System.out.println("   Result: " + negPow + " (Optimal = 0.25)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Fast Exponentiation Task | Algorithm Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Modular Fast Power** | Binary Bit Shift | $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| `exp >>= 1` & squaring |
| **LeetCode 50 Pow(x, n)**| Floating Squaring| $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| `long N = n` cast guard |
| **Matrix Fast Power** | Matrix Multiplication| $\mathbf{O(K^3 \log N)}$ Fast⚡| $\mathbf{O(K^2)}$ Matrix | $K \times K$ Matrix Dim |

---

## 10. Edge Cases & Boundary Handling

1. **Exponent $N = \text{Integer.MIN_VALUE}$ ($-2,147,483,648$)**:
   - Casting `long N = n` prevents overflow when computing `N = -N`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running Linear `for (int i = 0; i < N; i++)` Loop**:
  - Running a linear loop takes $O(N)$ time, causing TLE (Time Limit Exceeded) for $N \ge 10^9$. **ALWAYS use Binary Exponentiation to achieve $O(\log N)$ time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** LeetCode 50 MIN_VALUE Rule:
> In LeetCode 50 `Pow(x, n)`, ALWAYS cast `int n` to `long N = n` BEFORE negating `N = -N`, preventing 32-bit signed overflow when `n = Integer.MIN_VALUE`! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Linear Iteration ($O(N)$) | Fast Exponentiation ($O(\log N)$) |
| :--- | :--- | :--- |
| **Multiplications ($N=10^{18}$)**| $10^{18}$ Multiplications (Slow!) | **~60 Multiplications (Instant!) ⚡** |
| **Time Complexity** | $O(N)$ Linear | **$O(\log N)$ Logarithmic ⚡** |
| **Execution Time** | Years | **Nanoseconds ⚡** |

---

## 14. How to Recognize This in Questions

* **"Compute A^N % M where N <= 10^18"** $\rightarrow$ Fast Exponentiation ($O(\log N)$ time).
* **"Implement pow(x, n)"** $\rightarrow$ LeetCode 50.

---

## 15. Frequently Asked Interview Questions

* **Q: How does Fast Exponentiation achieve $O(\log N)$ time?**  
  *A:* By scanning the binary bit representation of exponent $N$. Squaring the base at each step doubles the exponent power, processing 1 bit of $N$ per iteration for $\lfloor \log_2 N \rfloor + 1$ total steps.

* **Q: Why is `long N = n` required in LeetCode 50?**  
  *A:* Because `Integer.MIN_VALUE` is $-2^{31}$. Negating $-(-2^{31})$ yields $+2^{31}$, which exceeds `Integer.MAX_VALUE` ($2^{31}-1$) and overflows back to $-2^{31}$ in 32-bit signed arithmetic.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: FAST EXPONENTIATION                                   |
+-----------------------------------------------------------------------+
| • Recurrence : A^N = (A^2)^(N/2) if even | A * (A^2)^((N-1)/2) if odd |
| • Core Loop  : while(exp>0) { if((exp&1)==1) res=(res*base)%M;        |
|                base=(base*base)%M; exp >>= 1; }                       |
| • LeetCode 50: Cast long N = n before N = -N for Integer.MIN_VALUE! ⚡ |
| • Speedup    : Reduces 10^18 multiplications down to 60 steps! ⚡      |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Modular Fast Exponentiation in $O(\log N)$ time in Java.
- [ ] I can write LeetCode 50 (`Pow(x, n)`) in Java with negative exponent handling.
- [ ] I can explain why `long N = n` is required for `Integer.MIN_VALUE`.
- [ ] I can prove why binary exponentiation takes $O(\log N)$ time.
- [ ] I can state how binary bit shifts scan exponent $N$ from LSB to MSB.
