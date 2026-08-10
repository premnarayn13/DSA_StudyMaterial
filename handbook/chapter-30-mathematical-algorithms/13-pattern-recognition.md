# 13. Pattern Recognition & Mathematical Triggers: 6 Master Archetypes

## 1. Introduction
High-speed problem solving in technical coding interviews requires instant **Mathematical Algorithm Pattern Recognition**. When confronted with complex numerical constraints, modular requirements, prime factorizations, or recurrence relations, experienced engineers map problem descriptions directly to one of **6 Universal Mathematical Master Archetypes**: **Prime Factorization & Divisors Archetype**, **Sieve & Primality Testing Archetype**, **Euclidean & Diophantine Archetype**, **Modular Arithmetic & Fast Power Archetype**, **Recurrence & Combinatorics Archetype**, and **Probabilistic & Numerical Optimization Archetype**. Identifying trigger words in problem statements allows immediate selection of optimal mathematical formulas, sieve arrays, modular inverse guards, and matrix exponentiation engines.

> **Important:** The 6 Universal Mathematical Master Archetypes & Trigger Signals:
> 1. **Pattern 1: Prime Factorization & Divisors**: Trigger = *"Count total divisors, sum of divisors, or prime factors of N"*. Mechanics = Fundamental Theorem $\sigma_0(N) = \prod (e_i+1)$, $\sigma_1(N) = \prod \frac{p_i^{e_i+1}-1}{p_i-1}$, SPF Sieve.
> 2. **Pattern 2: Sieve & Primality Testing**: Trigger = *"Count primes up to N or primes in range [L, R] or test huge 64-bit prime"*. Mechanics = Sieve of Eratosthenes $O(N \log \log N)$, Segmented Sieve $O(\sqrt{R})$ space, Miller-Rabin test.
> 3. **Pattern 3: Euclidean & Diophantine**: Trigger = *"GCD, LCM, solve ax + by = c or modular inverse for non-primes"*. Mechanics = $\gcd(a, b)$, safe LCM $(a/\gcd) \cdot b$, Extended Euclidean.
> 4. **Pattern 4: Modular Arithmetic & Fast Power**: Trigger = *"Return answer modulo 10^9+7 or compute A^N % M for N <= 10^18"*. Mechanics = Negative mod guard `(a - b % M + M) % M`, 64-bit cast `((long) a * b) % M`, Fast Power $O(\log N)$, Fermat's Inverse $A^{M-2}$.
> 5. **Pattern 5: Recurrence & Combinatorics**: Trigger = *"Compute N-th Fibonacci for N <= 10^18, unique BSTs, or combinations C(N, K)"*. Mechanics = Matrix Exponentiation $O(\log N)$, Catalan $C_N = \frac{1}{N+1} \binom{2N}{N}$, Pascal DP.
> 6. **Pattern 6: Probabilistic & Numerical Optimization**: Trigger = *"Random sampling from stream, sqrt without built-in functions, or continuous bisection"*. Mechanics = Reservoir Sampling $P = 1/i$, Newton-Raphson Sqrt $x = 0.5(x + N/x)$, Continuous BS 60 iterations. ⚡

```
Master Mathematical Archetype Decision Flowchart:

Problem Trigger Signal:
├── "Total divisors count / sum or prime factors?" ──► Pattern 1: Prime Factorization (sigma_0, sigma_1, SPF)
├── "Count primes 1..N / range [L,R] / test prime?" ──► Pattern 2: Sieve & Primality (Eratosthenes, Segmented, Miller-Rabin)
├── "GCD / LCM / solve ax + by = c?" ────────────────► Pattern 3: Euclidean & Diophantine (gcd, safe LCM, Ext GCD)
├── "Modulo 10^9+7 / compute A^N % M for N <= 10^18?" ─► Pattern 4: Modular Arithmetic & Fast Power (Fast Pow, Fermat Inv)
├── "N-th Fibonacci N <= 10^18 / unique BSTs?" ──────► Pattern 5: Recurrence & Combinatorics (Matrix Power, Catalan)
└── "Stream random sampling / sqrt without math fn?" ─► Pattern 6: Probabilistic & Optimization (Reservoir, Newton-Raphson) ⚡
```

---

## 2. Core Concepts & Master Mathematical Strategy Matrix

### 2.1 Master Mathematical Pattern Recognition Matrix
```
Master Mathematical Pattern Recognition Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Pattern Name          | Problem Trigger   | Primary Formula   | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **1. Prime Factor**   | "Divisors count/sum"| $\sigma_0(N) = \prod (e_i+1)$| **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**|
| **2. Sieve Algorithms**| "Primes range 1..N"| Segmented Sieve   | **$O(N \log \log N)$⚡**| **$O(\sqrt{R})$ Space ⚡**|
| **3. Euclidean GCD**  | "GCD / LCM / $ax+by=c$"| $\gcd(a, b) = \gcd(b, a\%b)$| **$O(\log(\min(a,b)))$⚡**| **$O(1)$ Memory ⚡**|
| **4. Modular Fast Pow**| "A^N % M N <= 10^18"| Binary Fast Power | **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **5. Recurrence & Comb**| "F_N N <= 10^18 / BSTs"| Matrix Power / Catalan| **$O(\log N)$ Logarithmic⚡**| **$O(1)$ Memory ⚡**|
| **6. Prob & Optim**   | "Stream sampling / Sqrt"| Reservoir / Newton| **$O(N)$ / $O(\log(\text{prec}))$⚡**| **$O(1)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Pattern 1 = sigma_0; Pattern 2 = Segmented Sieve; Pattern 3 = Euclidean GCD & Safe LCM; Pattern 4 = Fast Power A^N % M; Pattern 5 = Matrix Exponentiation & Catalan; Pattern 6 = Reservoir & Newton-Raphson!"**

---

## 3. Deep Dive into the 6 Mathematical Archetypes & LeetCode Audits

### 3.1 Auditing Top LeetCode Benchmark Problems
```
LeetCode Benchmark Problem Audits:

LeetCode 50  (Pow(x, n))                  ──► Pattern 4: Fast Power (Binary Exponentiation O(log N))
LeetCode 69  (Sqrt(x))                    ──► Pattern 6: Numerical Optimization (Newton-Raphson x = 0.5(x + N/x))
LeetCode 96  (Unique Binary Search Trees) ──► Pattern 5: Combinatorics (Catalan Number C_N = (1/(N+1)) * C(2N, N))
LeetCode 204 (Count Primes)               ──► Pattern 2: Sieve Algorithms (Sieve of Eratosthenes O(N log log N))
LeetCode 231 (Power of Two)               ──► Pattern 4: Modular/Bitwise ((n > 0) && (n & (n-1)) == 0)
LeetCode 382 (Linked List Random Node)    ──► Pattern 6: Probabilistic (Reservoir Sampling P = 1/i)
LeetCode 398 (Random Pick Index)          ──► Pattern 6: Probabilistic (Reservoir Sampling P = 1/count)
LeetCode 509 (Fibonacci Number N=10^18)   ──► Pattern 5: Recurrence (Matrix Exponentiation O(log N))
LeetCode 1979 (Find Greatest Common Div)  ──► Pattern 3: Euclidean GCD (gcd(a, b) O(log min))
```

---

## 4. Internal Working Mechanics: The 6 Master Pattern Code Templates

```java
// PATTERN 1: PRIME FACTORIZATION & DIVISORS
for (long p = 2; p * p <= n; p++) {
    if (n % p == 0) { int e = 0; while (n % p == 0) { e++; n /= p; } totalDivisors *= (e + 1); }
}

// PATTERN 2: SEGMENTED SIEVE FOR RANGE [L, R]
long start = Math.max((long) p * p, ((L + p - 1) / p) * (long) p);
for (long j = start; j <= R; j += p) isPrimeSegment[(int)(j - L)] = false;

// PATTERN 3: EUCLIDEAN GCD & SAFE LCM
long g = gcd(a, b); long lcm = (a / g) * b; // Divide FIRST!

// PATTERN 4: MODULAR FAST EXPONENTIATION (A^N % M)
while (exp > 0) { if ((exp & 1) == 1) res = (res * base) % mod; base = (base * base) % mod; exp >>= 1; }

// PATTERN 5: FIBONACCI MATRIX EXPONENTIATION O(log N)
long[][] T = {{1, 1}, {1, 0}}; long[][] T_pow = powerMatrix(T, n); return T_pow[0][1];

// PATTERN 6: NEWTON-RAPHSON SQRT (LeetCode 69)
while (Math.abs(x - root) > 1e-7) { root = 0.5 * (x + n / x); x = root; }
```

---

## 5. Visual Diagram: The 6 Mathematical Archetypes Map

```
                        [ Mathematical Algorithm Decision Engine ]
                                            │
                 ┌──────────────────────────┴──────────────────────────┐
                 ▼                                                     ▼
    [ Single Integer / Discrete Math ]                       [ System / Continuous Math ]
    /            │            \                              /            │            \
   ▼             ▼             ▼                            ▼             ▼             ▼
Pattern 1     Pattern 2     Pattern 3                   Pattern 4     Pattern 5     Pattern 6
(Factorization)(Sieve Range) (Euclidean GCD)            (Fast Power)  (Matrix Power)(Reservoir/Newton)
sigma_0(N)   Segmented Sieve gcd(a, b)                 A^N % M       T^N O(log N)   P = 1/i & x = 0.5(x+N/x)
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing reference solutions across the 6 Mathematical Master Archetypes.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Demonstrating Reference Implementations
 * Across the 6 Universal Mathematical Master Archetypes.
 */
public class MathematicalPatternRecognitionMaster {

    private static final long MOD = 1_000_000_007L;

    // PATTERN 1: PRIME FACTORIZATION DIVISOR COUNT
    public long pattern1_CountDivisors(long n) {
        long totalDivisors = 1;
        for (long p = 2; p * p <= n; p++) {
            if (n % p == 0) {
                int e = 0;
                while (n % p == 0) { e++; n /= p; }
                totalDivisors *= (e + 1);
            }
        }
        if (n > 1) totalDivisors *= 2;
        return totalDivisors;
    }

    // PATTERN 2: SIEVE OF ERATOSTHENES
    public int pattern2_CountPrimesSieve(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        int count = 0;
        for (int p = 2; p * p <= n; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= n; i += p) isPrime[i] = false;
            }
        }
        for (int i = 2; i <= n; i++) if (isPrime[i]) count++;
        return count;
    }

    // PATTERN 3: SAFE LCM VIA EUCLIDEAN GCD
    public long pattern3_SafeLCM(long a, long b) {
        long g = gcd(a, b);
        return (a / g) * b; // Divide FIRST! ⚡
    }

    // PATTERN 4: MODULAR FAST EXPONENTIATION (A^N % M)
    public long pattern4_FastPowerModular(long base, long exp, long mod) {
        long res = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) res = (res * base) % mod;
            base = (base * base) % mod;
            exp >>= 1;
        }
        return res;
    }

    // PATTERN 5: LEETCODE 96 CATALAN NUMBER UNIQUE BSTs
    public int pattern5_UniqueBSTs(int n) {
        int[] dp = new int[n + 1];
        dp[0] = 1; dp[1] = 1;
        for (int i = 2; i <= n; i++) {
            for (int j = 0; j < i; j++) dp[i] += dp[j] * dp[i - 1 - j];
        }
        return dp[n];
    }

    // PATTERN 6: NEWTON-RAPHSON SQRT (LeetCode 69)
    public int pattern6_SqrtNewtonRaphson(int n) {
        if (n < 2) return n;
        double x = n, root;
        while (true) {
            root = 0.5 * (x + n / x);
            if (Math.abs(x - root) < 1e-7) break;
            x = root;
        }
        return (int) root;
    }

    private long gcd(long a, long b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b);
    }
}
```

> **Quick Syntax:**
```java
// Master Mathematical Lines
totalDivisors *= (e + 1); long lcm = (a / g) * b; res = (res * base) % mod; root = 0.5 * (x + n / x);
```

---

## 7. Concrete Problem Examples & LeetCode Cross-References

* **Pattern 1 (Prime Factors)**: Total divisor count $\sigma_0(N)$, sum of divisors $\sigma_1(N)$, SPF Sieve.
* **Pattern 2 (Sieve)**: LeetCode 204 (Count Primes), Segmented Sieve range $[L, R]$, Miller-Rabin test.
* **Pattern 3 (Euclidean)**: LeetCode 1979 (Find Greatest Common Divisor), Safe LCM, Extended GCD, Linear Diophantine.
* **Pattern 4 (Modular Fast Power)**: LeetCode 50 (Pow(x, n)), Fermat's Inverse $A^{M-2}$, $A^N \bmod M$.
* **Pattern 5 (Recurrence & Combinatorics)**: LeetCode 96 (Unique BSTs), LeetCode 509 ($O(\log N)$ Matrix Fibonacci), Pascal DP.
* **Pattern 6 (Prob & Optimization)**: LeetCode 382 (Random Node Reservoir), LeetCode 69 (Newton-Raphson Sqrt).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class MathematicalPatternRecognitionDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   6 MASTER MATHEMATICAL ARCHETYPES DEMO         ");
        System.out.println("=================================================\n");

        MathematicalPatternRecognitionMaster master = new MathematicalPatternRecognitionMaster();

        // 1. Pattern 1 (Divisors Count N=360)
        System.out.println("1. Pattern 1 (Divisors Count N=360): " + master.pattern1_CountDivisors(360) + " (Optimal = 24)");

        // 2. Pattern 2 (Count Primes N=30)
        System.out.println("2. Pattern 2 (Count Primes N=30): " + master.pattern2_CountPrimesSieve(30) + " (Optimal = 10)");

        // 3. Pattern 3 (Safe LCM 35, 15)
        System.out.println("3. Pattern 3 (Safe LCM 35, 15): " + master.pattern3_SafeLCM(35, 15) + " (Optimal = 105)");

        // 4. Pattern 4 (Fast Power 3^13 % 10^9+7)
        System.out.println("4. Pattern 4 (Fast Power 3^13 % 10^9+7): " + master.pattern4_FastPowerModular(3, 13, 1_000_000_007L));

        // 5. Pattern 5 (Unique BSTs N=3)
        System.out.println("5. Pattern 5 (Unique BSTs N=3): " + master.pattern5_UniqueBSTs(3) + " (Optimal = 5)");

        // 6. Pattern 6 (Newton-Raphson Sqrt 25)
        System.out.println("6. Pattern 6 (Newton Sqrt 25): " + master.pattern6_SqrtNewtonRaphson(25) + " (Optimal = 5)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Master Mathematical Archetype | Time Complexity | Auxiliary Space | Key Identification Phrase |
| :--- | :--- | :--- | :--- |
| **1. Prime Factor**   | $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| "Total divisors count / sum" |
| **2. Sieve Algorithms**| $\mathbf{O(N \log \log N)}$⚡| $\mathbf{O(\sqrt{R})}$ Space ⚡| "Count primes up to N / range" |
| **3. Euclidean GCD**  | $\mathbf{O(\log(\min(a,b)))}$⚡| $\mathbf{O(1)}$ Memory ⚡| "GCD / LCM / solve ax + by = c" |
| **4. Modular Fast Pow**| $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| "Modulo 10^9+7 / A^N % M" |
| **5. Recurrence & Comb**| $\mathbf{O(\log N)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| "N-th Fibonacci N <= 10^18 / BSTs"|
| **6. Prob & Optim**   | $\mathbf{O(N)}$ / $\mathbf{O(\log(\text{prec}))}$⚡| $\mathbf{O(1)}$ Memory ⚡| "Stream random sampling / Sqrt" |

---

## 10. Edge Cases & Boundary Handling

1. **Selecting Between Standard Sieve and Segmented Sieve**:
   - $N \le 10^7 \to$ **Standard Sieve of Eratosthenes** ($O(N)$ space).
   - $R \le 10^{12}, R - L \le 10^6 \to$ **Segmented Sieve** ($O(\sqrt{R})$ space).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Multiplying Before Dividing in LCM (`(a * b) / gcd`)**:
  - Multiplying $a \times b$ first causes 64-bit `long` integer overflow. **ALWAYS divide first: `(a / gcd) * b`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 10-Second Mathematical Selector Rule:
> 1. Divisor count / sum? $\to$ Pattern 1 ($\sigma_0(N) = \prod (e_i+1)$).
> 2. Range primes $[L, R]$? $\to$ Pattern 2 (Segmented Sieve $O(\sqrt{R})$ space).
> 3. Safe LCM? $\to$ Pattern 3 (`(a / gcd) * b` divide FIRST!).
> 4. $A^N \bmod M$ for $N \le 10^{18}$? $\to$ Pattern 4 (Fast Power $O(\log N)$).
> 5. Fibonacci $N \le 10^{18}$? $\to$ Pattern 5 (Matrix Exponentiation $O(\log N)$).
> 6. Stream random sampling / Sqrt? $\to$ Pattern 6 (Reservoir Sampling / Newton-Raphson). ⚡

---

## 13. System & Implementation Comparisons

| Archetype | Primary Operation | Memory Footprint | Primary Optimization |
| :--- | :--- | :--- | :--- |
| **Pattern 3 (Safe LCM)** | Division First | **$O(1)$ Memory ⚡** | Eliminates 64-bit overflow |
| **Pattern 4 (Fast Power)**| Binary Bit Shifts | **$O(1)$ Memory ⚡** | Reduces $10^{18}$ ops to 60 |
| **Pattern 5 (Matrix Power)**| 2x2 Matrix Power | **$O(1)$ Memory ⚡** | Computes $F_{10^{18}}$ in nanosec |

---

## 14. How to Recognize This in Questions

* **"Compute A^N % 10^9+7 where N <= 10^18"** $\rightarrow$ Pattern 4 (Fast Power).
* **"Compute N-th Fibonacci number where N <= 10^18"** $\rightarrow$ Pattern 5 (Matrix Exponentiation).

---

## 15. Frequently Asked Interview Questions

* **Q: Why is dividing first in LCM `(a / gcd) * b` mandatory?**  
  *A:* Because multiplying $a \times b$ first can overflow 64-bit signed `long` limits ($9.22 \times 10^{18}$). Dividing first keeps intermediate numbers small, preventing integer overflow.

* **Q: How does Newton-Raphson compute square roots in $O(\log(\text{precision}))$ time?**  
  *A:* By using the tangent line update $x = 0.5(x + N/x)$, which exhibits quadratic convergence (the number of accurate decimal digits doubles at every iteration step).

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: 6 MASTER MATHEMATICAL ARCHETYPES                      |
+-----------------------------------------------------------------------+
| • Pattern 1: Divisors Count  -> sigma_0(N) = ∏ (e_i + 1)              |
| • Pattern 2: Segmented Sieve -> Range [L, R] in O(sqrt(R)) Space ⚡    |
| • Pattern 3: Safe LCM        -> (a / gcd(a, b)) * b (Divide FIRST!)   |
| • Pattern 4: Fast Power      -> A^N % M in O(log N) Time              |
| • Pattern 5: Matrix Power    -> F_N in O(log N) Time via 2x2 Matrix ⚡ |
| • Pattern 6: Newton Sqrt     -> x = 0.5 * (x + N / x) (LeetCode 69)   |
| • Performance : Reduces 10^18 operations down to 60 steps! ⚡          |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can match any mathematical problem to one of the 6 Master Archetypes in under 10 seconds.
- [ ] I can write Safe LCM in Java with divide-first protection.
- [ ] I can write Modular Fast Exponentiation $A^N \bmod M$ in Java in $O(\log N)$ time.
- [ ] I can write Fibonacci Matrix Exponentiation in Java in $O(\log N)$ time.
- [ ] I can write Newton-Raphson square root (LeetCode 69) in Java.
