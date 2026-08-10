# 08. Chinese Remainder Theorem: Simultaneous Congruences, CRT Formula & Non-Coprime Merging

## 1. Introduction
The **Chinese Remainder Theorem (CRT)** is a foundational theorem in Number Theory first recorded by 3rd-century Chinese mathematician Sunzi in *Sunzi Suanjing*. CRT provides a constructive method to solve a system of **Simultaneous Modular Congruences** of the form $X \equiv a_i \pmod{m_i}$ for $i = 1 \dots k$, where the moduli $m_1, m_2 \dots m_k$ are pairwise coprime ($\gcd(m_i, m_j) = 1$ for $i \neq j$). CRT guarantees that a unique solution $X$ exists modulo the total product modulus $M = m_1 \times m_2 \dots \times m_k$. Applications of CRT include high-speed big-integer arithmetic, secret sharing schemes (Shamir's Secret Sharing), parallel RSA signature acceleration, and calendar calculation algorithms.

> **Important:** Core Structural Formulas of Chinese Remainder Theorem:
> 1. **System of Simultaneous Congruences**:
>    $$\begin{cases} X \equiv a_1 \pmod{m_1} \\ X \equiv a_2 \pmod{m_2} \\ \dots \\ X \equiv a_k \pmod{m_k} \end{cases}$$
> 2. **Pairwise Coprime Condition**:
>    $$\gcd(m_i, m_j) = 1 \quad \forall i \neq j$$
> 3. **CRT Explicit Construction Formula**:
>    - Total Modulus Product: $M = \prod_{i=1}^k m_i$.
>    - Sub-product for index $i$: $M_i = \frac{M}{m_i}$.
>    - Modular Inverse of $M_i$: $Y_i = M_i^{-1} \pmod{m_i}$ (such that $M_i \times Y_i \equiv 1 \pmod{m_i}$).
>    - Unique Solution $X$:
>      $$X = \left( \sum_{i=1}^k a_i \times M_i \times Y_i \right) \pmod M$$ ⚡

```
Chinese Remainder Theorem System Topology:

Solve Congruence System:
- X ≡ 2 (mod 3)
- X ≡ 3 (mod 5)
- X ≡ 2 (mod 7)

Pairwise Coprime Check: gcd(3,5)=1, gcd(5,7)=1, gcd(3,7)=1 ✅

1. Total Modulus M = 3 * 5 * 7 = 105.
2. Sub-products M_i:
   - M_1 = 105 / 3 = 35;  Y_1 = 35^-1 mod 3 = 2^-1 mod 3 = 2!
   - M_2 = 105 / 5 = 21;  Y_2 = 21^-1 mod 5 = 1^-1 mod 5 = 1!
   - M_3 = 105 / 7 = 15;  Y_3 = 15^-1 mod 7 = 1^-1 mod 7 = 1!

3. Construct Solution X:
   X = (2*35*2 + 3*21*1 + 2*15*1) % 105
     = (140 + 63 + 30) % 105 = 233 % 105 = 23!

Unique Solution X = 23 (mod 105)! ✅ ⚡
```

---

## 2. Core Concepts & CRT Strategy Matrix

### 2.1 Chinese Remainder Theorem Strategy Matrix
```
Chinese Remainder Theorem Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| CRT Archetype         | Moduli Condition  | Solver Method     | Time Complexity   | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Standard CRT**      | Pairwise Coprime  | Direct Construction| **$O(K \log M)$ Fast ⚡**| **$O(K)$ Memory ⚡**|
| **Non-Coprime CRT**   | Arbitrary Moduli  | Extended GCD Merge| **$O(K \log M)$ Fast ⚡**| **$O(1)$ Memory ⚡**|
| **Garner's CRT**      | Pairwise Coprime  | Mixed-Radix Array | **$O(K^2)$ Fast ⚡**| **$O(K)$ Memory ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"CRT Construction: M = prod(m_i); M_i = M / m_i; Y_i = inverse(M_i, m_i); X = sum(a_i * M_i * Y_i) % M!"**

---

## 3. Characteristics & CRT Mathematical Proof

### 3.1 Mathematical Proof of CRT Construction Formula
* **Existence of Solution $X = \sum_{i=1}^k a_i \cdot M_i \cdot Y_i \pmod M$**:
  - Consider evaluating $X \pmod{m_j}$ for a specific index $j \in \{1 \dots k\}$.
  - For any term $i \neq j$:
    $$M_i = \frac{M}{m_i} = m_1 \dots m_{j} \dots m_k$$
    - Thus, $M_i$ contains $m_j$ as a factor, so $M_i \equiv 0 \pmod{m_j}$.
  - For the matching term $i = j$:
    $$M_j \times Y_j \equiv 1 \pmod{m_j} \quad (\text{by definition of modular inverse } Y_j = M_j^{-1} \bmod m_j)$$
  - Substituting into the sum modulo $m_j$:
    $$X \equiv \sum_{i=1}^k a_i \cdot M_i \cdot Y_i \equiv 0 + 0 \dots + a_j \cdot (M_j \cdot Y_j) + \dots + 0 \equiv a_j \cdot 1 \equiv a_j \pmod{m_j}$$
  - $X$ satisfies every congruence $X \equiv a_j \pmod{m_j}$ simultaneously!
* **Uniqueness Modulo $M$**:
  - Suppose two solutions $X_1$ and $X_2$ exist. Then $X_1 - X_2 \equiv 0 \pmod{m_i}$ for all $i$.
  - Since $m_i$ are pairwise coprime, $X_1 - X_2 \equiv 0 \pmod M$, so $X_1 \equiv X_2 \pmod M$.
  - Proves the solution $X$ is unique modulo $M$! ⚡

---

## 4. Internal Working Mechanics: Non-Coprime CRT Iterative Merger

Tracing Non-Coprime CRT Merger for 2 Congruences ($X \equiv a_1 \pmod{m_1}$ and $X \equiv a_2 \pmod{m_2}$):

```
Equivalence:
X = a_1 + k_1 * m_1
X = a_2 + k_2 * m_2

Equating the two expressions:
a_1 + k_1 * m_1 = a_2 + k_2 * m_2
m_1 * k_1 - m_2 * k_2 = (a_2 - a_1)

This is a Linear Diophantine Equation in (k_1, k_2)!
- Check Solvability: g = gcd(m_1, m_2).
- Solvable if and ONLY if (a_2 - a_1) % g == 0! ⚡

Merged Congruence:
- New Modulus m_new = lcm(m_1, m_2) = (m_1 / g) * m_2.
- New Remainder a_new = (a_1 + k_1 * m_1) % m_new.

Merges any 2 congruences into 1 combined congruence in O(log M) time! ✅ ⚡
```

---

## 5. Visual Diagram: Chinese Remainder Theorem Summation Layout

```
CRT Summation Component Pipeline:

For Congruence i: (a_i, m_i)
  ├── Sub-product M_i = M / m_i  ──► Divisible by ALL OTHER m_j (j != i)!
  ├── Modular Inverse Y_i       ──► Makes (M_i * Y_i) = 1 (mod m_i)
  └── Term = a_i * M_i * Y_i     ──► Evaluates to a_i (mod m_i) and 0 (mod m_j)!

Summing all K terms gives simultaneous solution X % M! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Standard Chinese Remainder Theorem ($O(K \log M)$) and Non-Coprime CRT Merger ($O(K \log M)$).

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Chinese Remainder Theorem:
 * Standard Pairwise Coprime CRT and Non-Coprime Extended GCD Congruence Merger.
 */
public class ChineseRemainderTheoremMaster {

    // =========================================================================
    // 1. STANDARD PAIRWISE COPRIME CRT SOLVER (O(K log M) Time, O(1) Space)
    // =========================================================================
    /**
     * Solves system X ≡ a[i] (mod m[i]) for pairwise coprime moduli m[i].
     *
     * @param a remainders array
     * @param m pairwise coprime moduli array
     * @return unique solution X modulo total product M
     */
    public long solveStandardCRT(long[] a, long[] m) {
        if (a == null || m == null || a.length != m.length || a.length == 0) return -1;
        int k = a.length;

        // Step 1: Calculate total product M = prod(m[i]) ⚡
        long M = 1;
        for (int i = 0; i < k; i++) {
            M *= m[i];
        }

        // Step 2: Sum terms (a_i * M_i * Y_i) % M ⚡
        long X = 0;
        for (int i = 0; i < k; i++) {
            long Mi = M / m[i]; // Sub-product ⚡
            long Yi = modInverse(Mi, m[i]); // Modular inverse Yi = Mi^-1 mod m[i] ⚡

            long term = modMultiply(a[i], modMultiply(Mi, Yi, M), M);
            X = (X + term) % M;
        }

        return (X % M + M) % M; // Non-negative guard ⚡
    }

    // =========================================================================
    // 2. NON-COPRIME CRT MERGER (O(K log M) Time, O(1) Space)
    // =========================================================================
    public static class Congruence {
        public final long a; // remainder
        public final long m; // modulus

        public Congruence(long a, long m) {
            this.a = (a % m + m) % m;
            this.m = m;
        }
    }

    /**
     * Merges two congruences (a1, m1) and (a2, m2) into single merged congruence.
     */
    public Congruence mergeCongruence(Congruence c1, Congruence c2) {
        long a1 = c1.a, m1 = c1.m;
        long a2 = c2.a, m2 = c2.m;

        long[] ext = extendedGCD(m1, m2);
        long g = ext[0];
        long x1 = ext[1];

        // Solvability check: (a2 - a1) MUST be divisible by g = gcd(m1, m2)! ⚡
        if ((a2 - a1) % g != 0) {
            return null; // Incompatible system!
        }

        long step = m2 / g;
        long k1 = modMultiply((a2 - a1) / g, x1, step);
        k1 = (k1 % step + step) % step;

        long mNew = (m1 / g) * m2; // New Modulus = lcm(m1, m2) ⚡
        long aNew = (a1 + k1 * m1) % mNew;

        return new Congruence(aNew, mNew);
    }

    /**
     * Solves system of arbitrary congruences (possibly non-coprime).
     */
    public Congruence solveNonCoprimeCRT(long[] a, long[] m) {
        if (a == null || m == null || a.length != m.length || a.length == 0) return null;

        Congruence current = new Congruence(a[0], m[0]);
        for (int i = 1; i < a.length; i++) {
            current = mergeCongruence(current, new Congruence(a[i], m[i]));
            if (current == null) return null; // System unsolvable!
        }

        return current;
    }

    // Helper utilities
    private long modInverse(long a, long m) {
        long[] ext = extendedGCD(a, m);
        if (ext[0] != 1) throw new ArithmeticException("Not coprime!");
        return (ext[1] % m + m) % m;
    }

    private long[] extendedGCD(long a, long b) {
        if (b == 0) return new long[]{a, 1, 0};
        long[] child = extendedGCD(b, a % b);
        long x = child[2];
        long y = child[1] - (a / b) * child[2];
        return new long[]{child[0], x, y};
    }

    private long modMultiply(long a, long b, long mod) {
        return (long) ((java.math.BigInteger.valueOf(a)
                .multiply(java.math.BigInteger.valueOf(b)))
                .mod(java.math.BigInteger.valueOf(mod)).longValue());
    }
}
```

> **Quick Syntax:**
```java
// CRT Core Lines
long Mi = M / m[i]; long Yi = modInverse(Mi, m[i]); X = (X + a[i] * Mi * Yi) % M;
```

---

## 7. Concrete Problem Examples & Applications

1. **Classic Sunzi Suanjing Problem**:
   - Finding smallest $X$ such that $X \equiv 2 \pmod 3$, $X \equiv 3 \pmod 5$, $X \equiv 2 \pmod 7$ ($X = 23$).

2. **Parallel RSA Signature Acceleration**:
   - RSA CRT speedup: Computing signature $S \pmod N$ by computing $S_p \pmod P$ and $S_q \pmod Q$ separately and combining via CRT ($4\times$ speedup!).

3. **Shamir's Secret Sharing Scheme**:
   - Reconstructing secret keys from polynomial evaluation remainders.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class ChineseRemainderTheoremDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   CHINESE REMAINDER THEOREM DEMO                ");
        System.out.println("=================================================\n");

        ChineseRemainderTheoremMaster master = new ChineseRemainderTheoremMaster();

        // 1. Classic Sunzi Suanjing Problem (X ≡ 2 mod 3, X ≡ 3 mod 5, X ≡ 2 mod 7)
        long[] a1 = {2, 3, 2};
        long[] m1 = {3, 5, 7};
        long x1 = master.solveStandardCRT(a1, m1);

        System.out.println("1. Standard CRT Solver for Sunzi Problem:");
        System.out.println("   Congruences: X ≡ 2 (mod 3), X ≡ 3 (mod 5), X ≡ 2 (mod 7)");
        System.out.println("   Unique Solution X = " + x1 + " (mod 105) (Optimal = 23)");
        System.out.println("   Verifications:");
        System.out.println("     23 % 3 = " + (x1 % 3) + " (Expected 2)");
        System.out.println("     23 % 5 = " + (x1 % 5) + " (Expected 3)");
        System.out.println("     23 % 7 = " + (x1 % 7) + " (Expected 2)");
        System.out.println("-------------------------------------------------");

        // 2. Non-Coprime CRT Merger Test
        long[] a2 = {2, 4};
        long[] m2 = {6, 8}; // gcd(6, 8) = 2 != 1 (Non-Coprime!)
        ChineseRemainderTheoremMaster.Congruence merged = master.solveNonCoprimeCRT(a2, m2);

        System.out.println("2. Non-Coprime CRT Merger for X ≡ 2 (mod 6), X ≡ 4 (mod 8):");
        System.out.println("   Merged Solution X ≡ " + merged.a + " (mod " + merged.m + ") (Optimal = 20 mod 24)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| CRT Variant | Moduli Condition | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Standard CRT** | Pairwise Coprime | $\mathbf{O(K \log M)}$ Fast ⚡| $\mathbf{O(K)}$ Memory ⚡| Direct $M_i \cdot Y_i$ sum |
| **Non-Coprime CRT**| Arbitrary Moduli | $\mathbf{O(K \log M)}$ Fast ⚡| $\mathbf{O(1)}$ Memory ⚡| Diophability check |

---

## 10. Edge Cases & Boundary Handling

1. **Incompatible Non-Coprime System**:
   - `solveNonCoprimeCRT` returns `null` if $(a_2 - a_1) \% \gcd(m_1, m_2) \neq 0$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Applying Standard CRT Formula to Non-Coprime Moduli**:
  - Applying $M_i = M / m_i$ when $\gcd(m_i, m_j) \neq 1$ causes $M_i$ and $m_i$ to share common factors, breaking the modular inverse $Y_i = M_i^{-1} \pmod{m_i}$. **ALWAYS check coprimality or use Non-Coprime Extended GCD Merger!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 CRT Rules:
> * **Standard CRT**: Use $X = \sum a_i M_i Y_i \pmod M$ ONLY when moduli $m_i$ are pairwise coprime.
> * **Non-Coprime CRT**: Merge pairs iteratively using Extended GCD, checking $(a_2 - a_1) \pmod{\gcd(m_1, m_2)} == 0$. ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard Big Integer Arithmetic | CRT Modular Parallelization |
| :--- | :--- | :--- |
| **Operations** | Multiplications on 2048-bit numbers | **Parallel Operations on 1024-bit primes ⚡** |
| **RSA Speedup** | $O(N^3)$ Big Int Mul | **$4\times$ RSA Decryption Speedup ⚡** |

---

## 14. How to Recognize This in Questions

* **"Find X satisfying simultaneous remainders X % m1 = a1, X % m2 = a2"** $\rightarrow$ Chinese Remainder Theorem.

---

## 15. Frequently Asked Interview Questions

* **Q: What is the primary condition for Standard CRT to apply?**  
  *A:* All moduli $m_1, m_2 \dots m_k$ MUST be pairwise coprime ($\gcd(m_i, m_j) = 1$ for all $i \neq j$).

* **Q: How does RSA CRT speed up decryption?**  
  *A:* Instead of computing $M = C^D \pmod N$ (where $N$ is 2048-bit), RSA CRT computes $M_p = C^{D_p} \pmod P$ and $M_q = C^{D_q} \pmod Q$ (on 1024-bit primes $P$ and $Q$) and merges them via CRT, running $4\times$ faster.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: CHINESE REMAINDER THEOREM                             |
+-----------------------------------------------------------------------+
| • System      : X ≡ a_i (mod m_i) for i = 1..k                        |
| • Condition   : Moduli m_i MUST be pairwise coprime!                  |
| • Formula     : M = prod(m_i); M_i = M / m_i; Y_i = inverse(M_i, m_i);|
|                 X = sum(a_i * M_i * Y_i) % M                          |
| • Non-Coprime : Merge pairs via Diophantine m1*k1 - m2*k2 = a2 - a1 ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the Standard CRT solver in Java.
- [ ] I can write the Non-Coprime CRT Merger in Java.
- [ ] I can prove why $X = \sum a_i M_i Y_i \pmod M$ satisfies all congruences.
- [ ] I can state the condition for non-coprime congruence solvability.
- [ ] I can explain how RSA CRT speeds up decryption by $4\times$.
