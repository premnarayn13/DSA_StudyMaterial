# 01. Number Theory: Fundamental Theorem of Arithmetic, Divisibility & Prime Factorization

## 1. Introduction
**Number Theory** is the branch of pure mathematics that studies the properties, relationships, and algebraic structures of integers ($\mathbb{Z}$). In computer science and algorithm design, Number Theory forms the mathematical foundation of modern public-key cryptography (RSA, Elliptic Curve Cryptography), hashing functions, pseudo-random number generators, and high-performance competitive programming algorithms. The cornerstone of number theory is the **Fundamental Theorem of Arithmetic**, which states that every integer $N > 1$ can be uniquely represented as a product of prime numbers $N = p_1^{e_1} \cdot p_2^{e_2} \dots p_k^{e_k}$. From this prime factorization, essential properties like total divisor count $\sigma_0(N)$, sum of divisors $\sigma_1(N)$, and greatest common divisors can be computed in **$O(\sqrt{N})$ Trial Division Time** or **$O(\log N)$ Smallest Prime Factor (SPF) Sieve Time**.

> **Important:** Core Structural Formulas of Number Theory:
> 1. **Fundamental Theorem of Arithmetic (Unique Prime Factorization)**:
>    $$N = p_1^{e_1} \times p_2^{e_2} \times \dots \times p_k^{e_k}$$
> 2. **Total Divisors Count Formula ($\sigma_0(N)$)**:
>    $$\sigma_0(N) = \prod_{i=1}^k (e_i + 1) = (e_1 + 1)(e_2 + 1) \dots (e_k + 1)$$
> 3. **Sum of Divisors Formula ($\sigma_1(N)$)**:
>    $$\sigma_1(N) = \prod_{i=1}^k \frac{p_i^{e_i + 1} - 1}{p_i - 1}$$
> 4. **Trial Division Search Bound ($O(\sqrt{N})$)**:
>    - Any composite number $N$ must have at least one prime factor $p \le \sqrt{N}$. Searching up to $\sqrt{N}$ guarantees complete prime factorization! ⚡

```
Prime Factorization & Divisor Tree Topology (N = 360):

Prime Factorization of 360:
360 = 2^3 * 3^2 * 5^1

Divisor Calculations:
- Total Divisors Count sigma_0(360) = (3+1) * (2+1) * (1+1) = 4 * 3 * 2 = 24 Divisors! ✅
- Sum of Divisors sigma_1(360)     = ((2^4-1)/1) * ((3^3-1)/2) * ((5^2-1)/4)
                                   = 15 * 13 * 6 = 1,170! ✅ ⚡
```

---

## 2. Core Concepts & Number Theory Strategy Matrix

### 2.1 Number Theory Factorization Strategy Matrix
```
Number Theory Factorization Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Factorization Method  | Target Use Case   | Time Complexity   | Auxiliary Space   | Pre-computation   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Trial Division**    | Single Number $N$ | **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**| None Required     |
| **SPF Sieve Factor**  | Multiple Queries  | **$O(\log N)$ Fast ⚡**| **$O(MAX)$ Array ⚡**| $O(MAX \log \log MAX)$|
| **Pollard's Rho**     | Massive $N > 10^{12}$| $O(N^{1/4})$ Fast | $O(1)$ Memory     | None Required     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Total divisors count = (e1+1)(e2+1)...(ek+1); Trial division loops up to sqrt(N); SPF Sieve factorizes in O(log N) time!"**

---

## 3. Characteristics & Fundamental Theorem Mathematical Proof

### 3.1 Mathematical Proof of Trial Division Bound ($p \le \sqrt{N}$)
* Let $N > 1$ be a composite integer.
* By definition of composite numbers, $N$ can be factored into two integers $a$ and $b$ such that $1 < a \le b < N$:
  $$N = a \times b$$
* **Proof by Contradiction**:
  1. Suppose both factors $a$ and $b$ are strictly greater than $\sqrt{N}$ ($a > \sqrt{N}$ and $b > \sqrt{N}$).
  2. Multiplying the two inequalities:
     $$a \times b > \sqrt{N} \times \sqrt{N} \implies N > N$$
  3. Contradiction! ($N > N$ is impossible).
  4. Therefore, at least one factor $a$ must satisfy $a \le \sqrt{N}$.
  5. Since any composite factor $a$ itself has a prime factor $p \le a$, $N$ MUST contain a prime factor $p \le \sqrt{N}$.
* Proves that checking prime factors up to $\sqrt{N}$ guarantees complete factorization! ⚡

---

## 4. Internal Working Mechanics: Smallest Prime Factor (SPF) Sieve Execution

Tracing SPF Sieve Factorization for $N = 60$:

```
Pre-computed SPF Array (Smallest Prime Factor):
SPF[60] = 2
SPF[30] = 2
SPF[15] = 3
SPF[5]  = 5

Factorization Query for 60 (Repeatedly divide by SPF[n]):
- Step 1: n = 60, spf = SPF[60] = 2 ──► Factor = 2, n = 60 / 2 = 30
- Step 2: n = 30, spf = SPF[30] = 2 ──► Factor = 2, n = 30 / 2 = 15
- Step 3: n = 15, spf = SPF[15] = 3 ──► Factor = 3, n = 15 / 3 = 5
- Step 4: n = 5,  spf = SPF[5]  = 5 ──► Factor = 5, n = 5 / 5 = 1

Prime Factors of 60: [2, 2, 3, 5] (2^2 * 3^1 * 5^1) in O(log N) Time! ✅ ⚡
```

---

## 5. Visual Diagram: Divisor Function Formulas

```
Divisor Properties Formulas Topology:

Given Prime Factorization: N = p1^e1 * p2^e2 * ... * pk^ek

├── 1. Total Divisors Count sigma_0(N) = (e1 + 1) * (e2 + 1) * ... * (ek + 1)
│
├── 2. Sum of Divisors sigma_1(N)       = ∏ (pi^(ei+1) - 1) / (pi - 1)
│
└── 3. Product of Divisors              = N^(sigma_0(N) / 2) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Trial Division Prime Factorization ($O(\sqrt{N})$), Smallest Prime Factor (SPF) Sieve ($O(\log N)$), Divisor Count $\sigma_0(N)$, and Divisor Sum $\sigma_1(N)$.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Number Theory Foundations:
 * Prime Factorization (Trial Division & SPF Sieve), Divisor Count, and Divisor Sum Formulas.
 */
public class NumberTheoryMaster {

    // =========================================================================
    // 1. TRIAL DIVISION PRIME FACTORIZATION (O(sqrt(N)) Time, O(1) Space)
    // =========================================================================
    /**
     * Computes prime factor map (prime -> exponent) in O(sqrt(N)) time.
     *
     * @param n target positive integer
     * @return map of prime factors to their exponents
     */
    public Map<Long, Integer> primeFactorizationTrialDivision(long n) {
        Map<Long, Integer> factors = new LinkedHashMap<>();
        if (n <= 1) return factors;

        long temp = n;

        // Check prime factor 2
        if (temp % 2 == 0) {
            int count = 0;
            while (temp % 2 == 0) {
                count++;
                temp /= 2;
            }
            factors.put(2L, count);
        }

        // Check odd prime factors p from 3 up to sqrt(temp) ⚡
        for (long p = 3; p * p <= temp; p += 2) {
            if (temp % p == 0) {
                int count = 0;
                while (temp % p == 0) {
                    count++;
                    temp /= p;
                }
                factors.put(p, count);
            }
        }

        // Remaining prime factor > sqrt(N)
        if (temp > 1) {
            factors.put(temp, 1);
        }

        return factors;
    }

    // =========================================================================
    // 2. DIVISOR COUNT SIGMA_0 AND DIVISOR SUM SIGMA_1 FORMULAS
    // =========================================================================
    /**
     * Calculates total number of divisors sigma_0(N) in O(sqrt(N)) time.
     */
    public long countTotalDivisors(long n) {
        Map<Long, Integer> factors = primeFactorizationTrialDivision(n);
        long totalDivisors = 1;

        for (int exponent : factors.values()) {
            totalDivisors *= (exponent + 1); // Formula: (e1 + 1)(e2 + 1)... ⚡
        }

        return totalDivisors;
    }

    /**
     * Calculates sum of all divisors sigma_1(N) in O(sqrt(N)) time.
     */
    public long sumOfDivisors(long n) {
        Map<Long, Integer> factors = primeFactorizationTrialDivision(n);
        long totalSum = 1;

        for (Map.Entry<Long, Integer> entry : factors.entrySet()) {
            long p = entry.getKey();
            int e = entry.getValue();

            // Formula: (p^(e+1) - 1) / (p - 1) ⚡
            long numerator = (long) Math.pow(p, e + 1) - 1;
            long denominator = p - 1;
            totalSum *= (numerator / denominator);
        }

        return totalSum;
    }

    // =========================================================================
    // 3. FAST SPF SIEVE FACTORIZATION (O(log N) Query Time)
    // =========================================================================
    public static class SPFSieve {
        private final int[] spf;

        public SPFSieve(int maxVal) {
            this.spf = new int[maxVal + 1];
            for (int i = 0; i <= maxVal; i++) spf[i] = i;

            for (int i = 2; i * i <= maxVal; i++) {
                if (spf[i] == i) {
                    for (int j = i * i; j <= maxVal; j += i) {
                        if (spf[j] == j) spf[j] = i; // Store smallest prime factor ⚡
                    }
                }
            }
        }

        public List<Integer> getPrimeFactorsFast(int n) {
            List<Integer> factors = new ArrayList<>();
            while (n > 1) {
                factors.add(spf[n]);
                n /= spf[n]; // Divide by smallest prime factor in O(1) ⚡
            }
            return factors;
        }
    }
}
```

> **Quick Syntax:**
```java
// Divisor Formulas Lines
totalDivisors *= (exponent + 1); totalSum *= ((long) Math.pow(p, e + 1) - 1) / (p - 1);
```

---

## 7. Concrete Problem Examples & Applications

1. **Prime Factorization**:
   - RSA public-key encryption security benchmark ($O(\sqrt{N})$ time).

2. **Divisor Counting ($\sigma_0(N)$)**:
   - Calculating number of factors for grid and tile arrangement problems.

3. **Fast SPF Sieve Queries**:
   - Multi-query prime factorization for competitive programming ($O(\log N)$ time per query).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;
import java.util.Map;

public class NumberTheoryDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   NUMBER THEORY BENCHMARK DEMO                 ");
        System.out.println("=================================================\n");

        NumberTheoryMaster master = new NumberTheoryMaster();

        long n = 360;
        Map<Long, Integer> primeFactors = master.primeFactorizationTrialDivision(n);
        long countDiv = master.countTotalDivisors(n);
        long sumDiv = master.sumOfDivisors(n);

        System.out.println("1. Number Theory Analysis for N = " + n + ":");
        System.out.println("   Prime Factorization (p -> e): " + primeFactors + " (2^3 * 3^2 * 5^1)");
        System.out.println("   Total Divisors Count (sigma_0): " + countDiv + " Divisors (Optimal = 24)");
        System.out.println("   Sum of Divisors      (sigma_1): " + sumDiv + " (Optimal = 1170)");
        System.out.println("-------------------------------------------------");

        // 2. Fast SPF Sieve Factorization Test
        int maxLimit = 1000;
        NumberTheoryMaster.SPFSieve spfSieve = new NumberTheoryMaster.SPFSieve(maxLimit);
        List<Integer> fastFactors = spfSieve.getPrimeFactorsFast(60);

        System.out.println("2. Fast SPF Sieve Query for N = 60 (O(log N) Time):");
        System.out.println("   Prime Factors List: " + fastFactors + " (Optimal = [2, 2, 3, 5])");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Number Theory Task | Algorithm Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Prime Factorization** | Trial Division | $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| Loop up to $\sqrt{N}$ |
| **Fast SPF Factorization**| SPF Sieve Array | $\mathbf{O(\log N)}$ Query ⚡| $O(MAX)$ Array Space| Pre-computed SPF array |
| **Divisor Count $\sigma_0$** | Prime Exponent Product| $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| $\prod (e_i + 1)$ |
| **Divisor Sum $\sigma_1$** | Prime Geometric Series| $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| $\prod \frac{p_i^{e_i+1}-1}{p_i-1}$ |

---

## 10. Edge Cases & Boundary Handling

1. **Prime Input Number $N$**:
   - `primeFactorizationTrialDivision` returns `{N -> 1}`, `sigma_0(N) = 2`, `sigma_1(N) = N + 1`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running Trial Division Up to $N$ Instead of $\sqrt{N}$**:
  - Looping up to $N$ takes $O(N)$ linear time. For $N = 10^{12}$, $10^{12}$ iterations freeze the program. **ALWAYS loop up to $\sqrt{N}$ (`p * p <= temp`)!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Divisor Formulas:
> * **Total Divisors $\sigma_0(N)$**: $(e_1 + 1)(e_2 + 1) \dots (e_k + 1)$.
> * **Sum of Divisors $\sigma_1(N)$**: $\prod \frac{p_i^{e_i + 1} - 1}{p_i - 1}$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Trial Division ($O(\sqrt{N})$) | Fast SPF Sieve ($O(\log N)$) |
| :--- | :--- | :--- |
| **Pre-computation** | **None Required ⚡** | $O(MAX \log \log MAX)$ Array |
| **Query Speed** | $O(\sqrt{N})$ | **$O(\log N)$ Ultra Fast ⚡** |
| **Ideal Application** | Single Query / Huge $N$ | **Multiple Queries (Competitive Prog) ⚡**|

---

## 14. How to Recognize This in Questions

* **"Compute total number of divisors or sum of divisors for integer N"** $\rightarrow$ Fundamental Theorem $\sigma_0(N)$ and $\sigma_1(N)$.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Trial Division only need to check factors up to $\sqrt{N}$?**  
  *A:* Because if $N = a \times b$, both factors cannot be greater than $\sqrt{N}$ simultaneously (otherwise $a \times b > N$). Thus, at least one prime factor must be $\le \sqrt{N}$.

* **Q: What is the Fundamental Theorem of Arithmetic?**  
  *A:* The theorem stating that every integer $N > 1$ can be uniquely factored into a product of prime numbers $N = p_1^{e_1} \cdot p_2^{e_2} \dots p_k^{e_k}$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: NUMBER THEORY                                         |
+-----------------------------------------------------------------------+
| • Prime Factorization: N = p1^e1 * p2^e2 * ... * pk^ek                |
| • Divisor Count sigma_0(N): (e1 + 1) * (e2 + 1) * ... * (ek + 1)     |
| • Divisor Sum   sigma_1(N): ∏ (pi^(ei+1) - 1) / (pi - 1)              |
| • Trial Division Search    : Loop prime p while p * p <= N -> O(sqrt(N))|
| • SPF Fast Factorization   : Divide by spf[N] repeatedly -> O(log N) ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Trial Division Prime Factorization in $O(\sqrt{N})$ time in Java.
- [ ] I can write total divisor count $\sigma_0(N)$ and divisor sum $\sigma_1(N)$ in Java.
- [ ] I can write SPF Sieve for $O(\log N)$ multi-query prime factorization.
- [ ] I can prove why trial division stops at $\sqrt{N}$.
- [ ] I can state the Fundamental Theorem of Arithmetic.
