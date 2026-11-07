# 06. Modular Inverse: Fermat's Little Theorem, Extended GCD & Range Linear Inverses

## 1. Introduction
The **Modular Multiplicative Inverse** of an integer $A$ modulo $M$ (denoted as $A^{-1}$ or $\text{inv}(A)$) is an integer $X$ such that the product $A \cdot X$ is congruent to $1$ modulo $M$:
$$A \times X \equiv 1 \pmod M$$
Modular division $(A / B) \pmod M$ is undefined in integer arithmetic; it is computed by multiplying $A$ by the modular inverse of $B$: $(A \cdot B^{-1}) \pmod M$. The modular inverse $A^{-1} \pmod M$ exists **if and ONLY if $\gcd(A, M) = 1$** (that is, $A$ and $M$ are coprime). Three major algorithmic paradigms compute modular inverses:
1. **Fermat's Little Theorem (Prime Modulus $M$)**: Computes $A^{-1} \equiv A^{M-2} \pmod M$ in **$O(\log M)$ Time** via Fast Exponentiation.
2. **Extended Euclidean Algorithm (Arbitrary Coprime Modulus $M$)**: Computes $A \cdot x + M \cdot y = 1$ in **$O(\log(\min(A, M)))$ Time**.
3. **Linear Pre-computation of Range Inverses ($1 \dots N$)**: Computes modular inverses for ALL numbers from $1$ to $N$ modulo prime $M$ in **$O(N)$ Strict Linear Time** using DP recurrence $inv[i] = M - (M/i) \times inv[M \pmod i] \pmod M$.

> **Important:** The 3 Master Modular Inverse Formulas:
> 1. **Existence Condition**:
>    $$\text{Inverse Exists} \iff \gcd(A, M) = 1$$
> 2. **Fermat's Little Theorem Formula (Prime $M$)**:
>    $$A^{-1} \equiv A^{M-2} \pmod M$$
> 3. **Extended Euclidean Formula (Arbitrary Coprime $M$)**:
>    $$A \cdot x + M \cdot y = 1 \implies A^{-1} = (x \pmod M + M) \pmod M$$
> 4. **Linear Range Inverses DP Recurrence ($1 \dots N \pmod M$)**:
>    $$inv[i] = M - \left\lfloor \frac{M}{i} \right\rfloor \times inv[M \bmod i] \pmod M$$ ⚡

```
Modular Inverse Computation Strategy Topology:

Is Modulus M Prime (e.g. M = 10^9 + 7)?
├── YES! (Prime M)
│   ├── Single Query A ─────────► Fermat's Little Theorem: A^(M-2) % M -> O(log M) ⚡
│   └── Range Query 1..N ───────► Linear DP Array: inv[i] = M - (M/i)*inv[M%i] % M -> O(N) ⚡
└── NO! (Arbitrary Coprime M where gcd(A, M) == 1)
    └── Extended Euclidean ─────► Solve Ax + My = 1 -> x = (x % M + M) % M -> O(log M) ⚡
```

---

## 2. Core Concepts & Modular Inverse Strategy Matrix

### 2.1 Modular Inverse Strategy Matrix
```
Modular Inverse Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Inv Calculation Engine| Target Modulus M  | Time Complexity   | Auxiliary Space   | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Fermat's Theorem**  | Prime $M$         | **$O(\log M)$ Fast ⚡**| **$O(1)$ Memory ⚡**| 2-line implementation|
| **Extended Euclidean**| Arbitrary Coprime | **$O(\log(\min(A,M)))$⚡**| **$O(1)$ Memory ⚡**| Works for NON-primes|
| **Linear Range DP**   | Range $1 \dots N$ | **$O(N)$ Linear ⚡**| **$O(N)$ Array ⚡**| **$O(1)$ per query ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Fermat inverse: A^(M-2) % M for prime M; Extended Euclidean for arbitrary coprime M; Range DP: inv[i] = M - (M/i)*inv[M%i] % M!"**

---

## 3. Characteristics & Linear Range Inverse DP Proof

### 3.1 Mathematical Proof of Linear Range Inverse DP ($inv[i] = M - (M/i) \cdot inv[M \pmod i] \pmod M$)
* Let $M$ be a prime modulus, and $1 \le i < M$.
* Express $M$ using integer division by $i$:
  $$M = k \cdot i + r \quad \text{where } k = \left\lfloor \frac{M}{i} \right\rfloor \text{ and } r = M \bmod i$$
* In modular arithmetic modulo $M$, $M \equiv 0 \pmod M$:
  $$k \cdot i + r \equiv 0 \pmod M$$
* Multiply both sides by $i^{-1} \cdot r^{-1} \pmod M$:
  $$k \cdot r^{-1} + i^{-1} \equiv 0 \pmod M$$
* Rearranging for $i^{-1}$:
  $$i^{-1} \equiv -k \cdot r^{-1} \pmod M$$
* Substituting $k = \left\lfloor \frac{M}{i} \right\rfloor$ and $r = M \bmod i$:
  $$i^{-1} \equiv -\left\lfloor \frac{M}{i} \right\rfloor \cdot (M \bmod i)^{-1} \pmod M$$
* To make the negative term positive in Java modulo arithmetic, add $+M$:
  $$inv[i] = \left( M - \left\lfloor \frac{M}{i} \right\rfloor \times inv[M \bmod i] \pmod M \right) \pmod M$$
* Since $M \bmod i < i$, $inv[M \bmod i]$ has ALREADY been computed in prior loop steps.
* Computes all inverses $1 \dots N$ in **$O(N)$ Strict Linear Time**! ⚡

---

## 4. Internal Working Mechanics: Fermat's Inverse for $A = 3 \pmod 7$

Tracing Fermat's Modular Inverse for $A = 3, M = 7$ ($3 \cdot X \equiv 1 \pmod 7$):

```
Formula: A^(M - 2) % M = 3^(7 - 2) % 7 = 3^5 % 7.

Execution Steps:
3^1 = 3 % 7 = 3
3^2 = 9 % 7 = 2
3^3 = (2 * 3) % 7 = 6
3^4 = (6 * 3) % 7 = 18 % 7 = 4
3^5 = (4 * 3) % 7 = 12 % 7 = 5!

Modular Inverse of 3 Modulo 7 is 5!
Verification: (3 * 5) % 7 = 15 % 7 = 1! ✅ ⚡
```

---

## 5. Visual Diagram: Linear Range Inverse DP Array Construction

```
Linear Range Inverse DP State Flow (M = 7):

Base Case: inv[1] = 1

Compute inv[2] (i = 2):
- k = 7 / 2 = 3, r = 7 % 2 = 1
- inv[2] = (7 - 3 * inv[1]) % 7 = (7 - 3 * 1) % 7 = 4 % 7 = 4! (Verification: 2*4 = 8 = 1 mod 7) ✅

Compute inv[3] (i = 3):
- k = 7 / 3 = 2, r = 7 % 3 = 1
- inv[3] = (7 - 2 * inv[1]) % 7 = (7 - 2 * 1) % 7 = 5 % 7 = 5! (Verification: 3*5 = 15 = 1 mod 7) ✅

Pre-computes full range 1..N in O(N) linear time without single division operation! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Fermat's Little Theorem Inverse ($O(\log M)$), Extended Euclidean Inverse ($O(\log M)$), and Linear Range Inverses Array ($O(N)$).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Modular Inverse Algorithms:
 * Fermat's Little Theorem Inverse, Extended Euclidean Inverse, and O(N) Linear Range Inverses.
 */
public class ModularInverseMaster {

    // =========================================================================
    // 1. FERMAT'S LITTLE THEOREM MODULAR INVERSE (PRIME MODULUS M - O(log M))
    // =========================================================================
    /**
     * Computes modular inverse A^-1 mod primeMod in O(log primeMod) time.
     */
    public long modInverseFermat(long a, long primeMod) {
        if (gcd(a, primeMod) != 1) {
            throw new ArithmeticException("Modular inverse does not exist (A and M are not coprime)!");
        }
        return powerModular(a, primeMod - 2, primeMod); // A^(M-2) % M ⚡
    }

    private long powerModular(long base, long exp, long mod) {
        long res = 1;
        base = (base % mod + mod) % mod;
        while (exp > 0) {
            if ((exp & 1) == 1) {
                res = (long) ((java.math.BigInteger.valueOf(res)
                        .multiply(java.math.BigInteger.valueOf(base)))
                        .mod(java.math.BigInteger.valueOf(mod)).longValue());
            }
            base = (long) ((java.math.BigInteger.valueOf(base)
                    .multiply(java.math.BigInteger.valueOf(base)))
                    .mod(java.math.BigInteger.valueOf(mod)).longValue());
            exp >>= 1;
        }
        return res;
    }

    private long gcd(long a, long b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b);
    }

    // =========================================================================
    // 2. EXTENDED EUCLIDEAN MODULAR INVERSE (ARBITRARY COPRIME MODULUS M)
    // =========================================================================
    /**
     * Computes A^-1 mod mod for arbitrary coprime mod in O(log mod) time.
     */
    public long modInverseExtendedGCD(long a, long mod) {
        long[] result = extendedGCD(a, mod);
        long g = result[0];
        long x = result[1];

        if (g != 1) {
            throw new ArithmeticException("Modular inverse does not exist (A and M are not coprime)!");
        }

        return (x % mod + mod) % mod; // Non-negative guard ⚡
    }

    private long[] extendedGCD(long a, long b) {
        if (b == 0) return new long[]{a, 1, 0};
        long[] child = extendedGCD(b, a % b);
        long x = child[2];
        long y = child[1] - (a / b) * child[2];
        return new long[]{child[0], x, y};
    }

    // =========================================================================
    // 3. LINEAR RANGE INVERSES PRE-COMPUTATION 1 ... N (O(N) Time, O(N) Space)
    // =========================================================================
    /**
     * Pre-computes modular inverses for all numbers from 1 to n modulo primeMod.
     */
    public long[] computeRangeInverses(int n, long primeMod) {
        long[] inv = new long[n + 1];
        if (n >= 1) inv[1] = 1;

        for (int i = 2; i <= n; i++) {
            // Recurrence: inv[i] = primeMod - (primeMod / i) * inv[primeMod % i] % primeMod ⚡
            inv[i] = primeMod - (primeMod / i) * inv[(int) (primeMod % i)] % primeMod;
        }

        return inv;
    }
}
```

> **Quick Syntax:**
```java
// Modular Inverse Core Lines
long invFermat = powerModular(a, primeMod - 2, primeMod);
inv[i] = primeMod - (primeMod / i) * inv[(int)(primeMod % i)] % primeMod; // Linear Range DP Line
```

---

## 7. Concrete Problem Examples & Applications

1. **Combinatorial $C(N, K) \pmod{10^9 + 7}$**:
   - $C(N, K) = \frac{N!}{K! (N - K)!} \pmod M = (N! \cdot (K!)^{-1} \cdot ((N - K)!)^{-1}) \pmod M$.

2. **Modular Division Engine**:
   - Computing $(A / B) \bmod M$ using $B^{-1}$.

3. **Multi-Query Combination Benchmarks**:
   - Pre-computing factorials and range inverse factorials in $O(N)$ linear time.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class ModularInverseDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MODULAR INVERSE BENCHMARK DEMO                ");
        System.out.println("=================================================\n");

        ModularInverseMaster master = new ModularInverseMaster();
        long M = 1_000_000_007L;

        // 1. Fermat's Inverse Test (A = 3, M = 7)
        long invFermat = master.modInverseFermat(3, 7);
        System.out.println("1. Fermat's Modular Inverse for 3 mod 7:");
        System.out.println("   Inverse Result: " + invFermat + " (Verification (3*5)%7 = " + ((3 * invFermat) % 7) + ")");
        System.out.println("-------------------------------------------------");

        // 2. Extended Euclidean Inverse Test (A = 3, M = 10 - Non-Prime!)
        long invExt = master.modInverseExtendedGCD(3, 10);
        System.out.println("2. Extended GCD Modular Inverse for 3 mod 10 (Non-Prime!):");
        System.out.println("   Inverse Result: " + invExt + " (Verification (3*7)%10 = " + ((3 * invExt) % 10) + ")");
        System.out.println("-------------------------------------------------");

        // 3. Linear Range Inverses Test (1 ... 6 mod 7)
        long[] rangeInv = master.computeRangeInverses(6, 7);
        System.out.println("3. Linear Range Inverses for 1...6 mod 7 (O(N) Time):");
        System.out.println("   Range Inverses Array: " + Arrays.toString(rangeInv));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Modular Inverse Method | Target Modulus $M$ | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Fermat's Theorem** | Prime Modulus $M$ | $\mathbf{O(\log M)}$ Logarithmic⚡| $\mathbf{O(1)}$ Memory ⚡| $A^{M-2} \bmod M$ |
| **Extended GCD** | Arbitrary Coprime $M$| $\mathbf{O(\log(\min(A,M)))}$⚡| $\mathbf{O(1)}$ Memory ⚡| Solves $Ax + My = 1$ |
| **Linear Range DP** | Range $1 \dots N$ | $\mathbf{O(N)}$ Strict Linear⚡| $\mathbf{O(N)}$ Array Space| $inv[M \% i]$ recurrence |

---

## 10. Edge Cases & Boundary Handling

1. **Non-Coprime $A$ and $M$ ($\gcd(A, M) \neq 1$)**:
   - Throws `ArithmeticException` because inverse does not exist.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Fermat's Little Theorem When Modulus $M$ is Composite**:
  - Fermat's formula $A^{M-2} \pmod M$ is ONLY valid when $M$ is prime. For composite $M$ (e.g. $M = 10$), Fermat yields incorrect results. **ALWAYS use Extended Euclidean Inverse for composite $M$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Modular Inverse Rule:
> * Use **Fermat's Little Theorem ($A^{M-2} \bmod M$)** when modulus $M$ is Prime (e.g. $10^9 + 7$).
> * Use **Extended Euclidean Algorithm** when modulus $M$ is Composite/Arbitrary.
> * Use **Linear Range DP** for range queries $1 \dots N$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Fermat's Inverse ($O(\log M)$) | Linear Range Inverse DP ($O(N)$) |
| :--- | :--- | :--- |
| **Per-Query Time** | $O(\log M)$ | **$O(1)$ Instant Array Lookup ⚡** |
| **Total Time (N Queries)**| $O(N \log M)$ | **$O(N)$ Total ⚡** |
| **Ideal Application** | Single Query | **Combinatorial Factorials / Multi-Queries ⚡**|

---

## 14. How to Recognize This in Questions

* **"Compute (A / B) % M where M is 10^9 + 7"** $\rightarrow$ Fermat's Inverse $A \cdot B^{M-2} \bmod M$.
* **"Pre-compute inverses for all numbers from 1 to N in O(N) time"** $\rightarrow$ Linear Range DP.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does $A^{M-2} \pmod M$ compute the modular inverse of $A$ when $M$ is prime?**  
  *A:* By Fermat's Little Theorem, $A^{M-1} \equiv 1 \pmod M$. Factoring out $A$: $A \cdot (A^{M-2}) \equiv 1 \pmod M$. Thus, $A^{M-2}$ is the multiplicative inverse $A^{-1} \pmod M$.

* **Q: How does the Linear Range DP recurrence `inv[i] = M - (M/i) * inv[M%i] % M` achieve $O(N)$ time?**  
  *A:* By expressing $M = k \cdot i + r$ and rearranging $k \cdot i + r \equiv 0 \pmod M$, $i^{-1}$ is computed from the previously stored inverse of smaller remainder $r = M \bmod i < i$ in $O(1)$ time per step.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MODULAR INVERSE                                       |
+-----------------------------------------------------------------------+
| • Existence Condition: Modular inverse exists IF AND ONLY IF gcd(A,M)=1|
| • Fermat's Inverse  : A^(M-2) % M (Strictly for PRIME modulus M!)     |
| • Extended GCD Inv  : Solves Ax + My = 1 -> x = (x % M + M) % M       |
| • Linear Range DP   : inv[i] = M - (M / i) * inv[M % i] % M -> O(N) ⚡|
| • Combinatorics     : C(N, K) % M = (N! * inv(K!) * inv((N-K)!)) % M  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Fermat's modular inverse $A^{M-2} \bmod M$ in Java.
- [ ] I can write Extended Euclidean modular inverse in Java for arbitrary coprime $M$.
- [ ] I can write the $O(N)$ Linear Range Inverse DP array generator in Java.
- [ ] I can prove why $A$ and $M$ must be coprime for an inverse to exist.
- [ ] I can write combination calculation $C(N, K) \pmod{10^9 + 7}$ using modular inverses.
