# 04. Modular Arithmetic: Congruences, Overflow Guards & Negative Modulo Rules

## 1. Introduction
**Modular Arithmetic** (sometimes called "clock arithmetic") is a system of arithmetic for integers where numbers "wrap around" upon reaching a fixed modulus value $M$. In computer science, cryptography (RSA, Diffie-Hellman), hashing algorithms, and competitive programming, modular arithmetic prevents integer overflow when dealing with exponentially large combinatorial results. Algorithms frequently require output modulo **$M = 10^9 + 7$** or **$M = 998,244,353$** (both prime numbers). Mastering the fundamental modular equivalence laws—**Modular Addition**, **Modular Subtraction (with Negative Modulo Guard)**, **Modular Multiplication (with 64-Bit Overflow Guard)**, and **Modular Division (via Multiplicative Inverse)**—is mandatory for software correctness.

> **Important:** The 4 Master Modular Arithmetic Laws:
> 1. **Modular Addition Law**:
>    $$(a + b) \pmod M = ((a \pmod M) + (b \pmod M)) \pmod M$$
> 2. **Modular Subtraction Law (Negative Modulo Rule)**:
>    $$(a - b) \pmod M = ((a \pmod M) - (b \pmod M) + M) \pmod M$$
>    - Adding $+M$ guarantees non-negative results in Java, where `-5 % 7` evaluates to `-5`! ⚡
> 3. **Modular Multiplication Law (Overflow Guard)**:
>    $$(a \times b) \pmod M = (((a \pmod M) \times (b \pmod M)) \pmod M$$
>    - Must cast operands to `long` before multiplication to prevent 32-bit `int` signed overflow!
> 4. **Modular Division Law**:
>    $$\left(\frac{a}{b}\right) \pmod M = (a \times b^{-1}) \pmod M$$
>    - Direct integer division is invalid in modular arithmetic! Must multiply by $b^{-1}$ (Modular Inverse)! ⚡

```
Modular Subtraction & Multiplication Overflow Topology (M = 10^9 + 7):

1. Negative Modulo Guard (a = 3, b = 8, M = 7):
   (3 - 8) % 7 = -5 % 7 = -5 in Java! ❌
   Correct Java Guard: (3 - 8 % 7 + 7) % 7 = (-5 + 7) % 7 = 2 % 7 = 2! ✅ ⚡

2. 64-bit Multiplication Overflow Guard (a = 10^9, b = 10^9, M = 10^9 + 7):
   int product = a * b; // OVERFLOWS 32-bit int to negative number! ❌
   long product = ((long) a * b) % M; // 10^18 fits safely in 64-bit signed long! ✅ ⚡
```

---

## 2. Core Concepts & Modular Arithmetic Strategy Matrix

### 2.1 Modular Arithmetic Operations Strategy Matrix
```
Modular Arithmetic Operations Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Modular Operation     | Mathematical Law  | Java Syntax Guard | Hardware Speed    | Overflow Risk     |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Modular Add**       | $(a + b) \bmod M$ | `(a + b) % M`     | **1 CPU Cycle ⚡** | Safe with `long`  |
| **Modular Subtract**  | $(a - b) \bmod M$ | `(a - b % M + M) % M`| **1 CPU Cycle ⚡**| **Negative Mod ⚡**|
| **Modular Multiply**  | $(a \cdot b)\bmod M$| `((long) a * b) % M`| **1 CPU Cycle ⚡**| **32-bit Int Over ⚡**|
| **Modular Divide**    | $(a / b) \bmod M$ | `(a * modInverse(b)) % M`| $O(\log M)$ | Needs $\gcd(b,M)=1$|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Always add +M in subtraction: (a - b % M + M) % M; Always cast to long in multiplication: ((long)a * b) % M!"**

---

## 3. Characteristics & Negative Modulo Mathematical Proof

### 3.1 Mathematical Derivation of Java Negative Modulo Guard `(a % M + M) % M`
* In mathematics, the modulo operation $R = A \pmod M$ is defined such that $0 \le R < M$.
* In Java, C++, and C#, the `%` operator is defined as **Remainder**, not true mathematical modulo:
  $$A \pmod M = A - M \times \left\lfloor \frac{A}{M} \right\rfloor$$
* **Java Remainder Behavior**:
  - For $A = -5$ and $M = 7$: `-5 % 7` evaluates to `-5` (preserves the sign of the dividend).
* **Proof that `(A % M + M) % M` produces valid Mathematical Modulo**:
  1. Let $r = A \% M$. Since $-M < r < M$, adding $M$ yields:
     $$0 < r + M < 2M$$
  2. Taking modulo $M$ on $(r + M)$ wraps values in the range $[M, 2M)$ down to $[0, M)$:
     $$((A \% M) + M) \% M \in [0, M)$$
  3. Guarantees 100% mathematically valid, non-negative modular results in Java! ⚡

---

## 4. Internal Working Mechanics: 64-Bit Multiplication Overflow Prevention

Tracing Modular Multiplication for $a = 1,000,000,000$, $b = 1,000,000,000$, $M = 1,000,000,007$:

```
Goal: Compute (10^9 * 10^9) % (10^9 + 7).

Product Value: 10^9 * 10^9 = 10^18.

32-bit Integer Limits:
- Integer.MAX_VALUE = 2,147,483,647 (~2.14 * 10^9).
- 10^18 exceeds 32-bit int limit by over 465,000,000x!
- Result without cast: -1486618624 (OVERFLOW TO NEGATIVE VALUE!) ❌

64-bit Signed Long Limits:
- Long.MAX_VALUE = 9,223,372,036,854,775,807 (~9.22 * 10^18).
- 10^18 fits safely inside 64-bit long!
- Calculation: ((long) 10^9 * 10^9) % 1000000007 = 49 (Correct!) ✅ ⚡
```

---

## 5. Visual Diagram: Modular Division via Multiplicative Inverse

```
Modular Division Dependency Topology:

Expression: (A / B) % M

Direct Division (INVALID!):
(12 / 4) % 7 = 3 % 7 = 3.
Is (12 % 7) / (4 % 7) equal? 5 / 4 = 1.25 != 3 (INCORRECT!) ❌

Correct Modular Division (via Modular Inverse B^-1):
Find B^-1 such that (B * B^-1) % M == 1.
For B = 4, M = 7: (4 * 2) % 7 = 8 % 7 = 1 ──► B^-1 = 2!
Compute: (A * B^-1) % M = (12 * 2) % 7 = 24 % 7 = 3! ✅ ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Modular Addition, Safe Subtraction, Safe 64-bit Multiplication, and Modular Division.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Modular Arithmetic:
 * Safe Addition, Subtraction (Negative Mod Guard), 64-Bit Multiplication, and Division.
 */
public class ModularArithmeticMaster {

    public static final long MOD = 1_000_000_007L;

    // =========================================================================
    // 1. MODULAR ADDITION (SAFE FOR LONG OPERANDS)
    // =========================================================================
    public long modAdd(long a, long b, long mod) {
        a = (a % mod + mod) % mod;
        b = (b % mod + mod) % mod;
        return (a + b) % mod; // Safe addition ⚡
    }

    // =========================================================================
    // 2. MODULAR SUBTRACTION (NEGATIVE MODULO GUARD)
    // =========================================================================
    /**
     * Subtracts b from a modulo mod, with negative modulo protection.
     */
    public long modSubtract(long a, long b, long mod) {
        a = (a % mod + mod) % mod;
        b = (b % mod + mod) % mod;
        return (a - b + mod) % mod; // Adding +mod prevents negative remainder! ⚡
    }

    // =========================================================================
    // 3. MODULAR MULTIPLICATION (64-BIT OVERFLOW GUARD)
    // =========================================================================
    /**
     * Multiplies a and b modulo mod using 64-bit long precision.
     */
    public long modMultiply(long a, long b, long mod) {
        a = (a % mod + mod) % mod;
        b = (b % mod + mod) % mod;

        // BigInteger fallback for 64-bit long overflow
        return (long) ((java.math.BigInteger.valueOf(a)
                .multiply(java.math.BigInteger.valueOf(b)))
                .mod(java.math.BigInteger.valueOf(mod)).longValue()); // Zero overflow risk ⚡
    }

    // =========================================================================
    // 4. MODULAR DIVISION (VIA FERMAT'S LITTLE THEOREM FOR PRIME MOD)
    // =========================================================================
    /**
     * Divides a by b modulo prime mod using Fermat's Little Theorem (b^(mod-2)).
     */
    public long modDivide(long a, long b, long primeMod) {
        long invB = modInverseFermat(b, primeMod);
        return modMultiply(a, invB, primeMod); // (a * b^-1) % primeMod ⚡
    }

    /**
     * Modular Inverse via Fermat's Little Theorem: b^(MOD - 2) % MOD.
     */
    public long modInverseFermat(long b, long primeMod) {
        return power(b, primeMod - 2, primeMod);
    }

    private long power(long base, long exp, long mod) {
        long res = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) res = (long) ((java.math.BigInteger.valueOf(res)
                    .multiply(java.math.BigInteger.valueOf(base)))
                    .mod(java.math.BigInteger.valueOf(mod)).longValue());
            base = (long) ((java.math.BigInteger.valueOf(base)
                    .multiply(java.math.BigInteger.valueOf(base)))
                    .mod(java.math.BigInteger.valueOf(mod)).longValue());
            exp >>= 1;
        }
        return res;
    }
}
```

> **Quick Syntax:**
```java
// Modular Arithmetic Core Lines
long add = (a + b) % MOD; long sub = (a - b % MOD + MOD) % MOD; long mul = ((long) a * b) % MOD;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 509 - Fibonacci Number Modulo $10^9 + 7$**:
   - Preventing integer overflow in DP calculations using modular addition.

2. **Combinatorial Pascal Triangle $C(N, K) \pmod{10^9 + 7}$**:
   - Computing combinations modulo prime $10^9 + 7$ using modular division.

3. **Hashing Algorithms (Polynomial Rolling Hash)**:
   - String hashing algorithms using modular multiplication and addition.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class ModularArithmeticDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MODULAR ARITHMETIC BENCHMARK DEMO             ");
        System.out.println("=================================================\n");

        ModularArithmeticMaster master = new ModularArithmeticMaster();
        long M = 1_000_000_007L;

        // 1. Modular Subtraction Test (Negative Mod Guard)
        long a = 3, b = 8;
        long subResult = master.modSubtract(a, b, 7);
        System.out.println("1. Modular Subtraction (3 - 8) % 7 with Guard:");
        System.out.println("   Result: " + subResult + " (Optimal = 2)");
        System.out.println("-------------------------------------------------");

        // 2. 64-Bit Modular Multiplication Test
        long x = 1_000_000_000L, y = 1_000_000_000L;
        long mulResult = master.modMultiply(x, y, M);
        System.out.println("2. Modular Multiplication (10^9 * 10^9) % (10^9 + 7):");
        System.out.println("   Result: " + mulResult + " (Optimal = 49)");
        System.out.println("-------------------------------------------------");

        // 3. Modular Division Test ((12 / 4) % 7)
        long divResult = master.modDivide(12, 4, 7);
        System.out.println("3. Modular Division (12 / 4) % 7 via Inverse:");
        System.out.println("   Result: " + divResult + " (Optimal = 3)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Modular Operation | Formula | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Modular Addition** | `(a + b) % M` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| Addition law |
| **Modular Subtraction**| `(a - b % M + M) % M` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| **Negative mod guard ⚡**|
| **Modular Multiply** | `((long) a * b) % M` | $\mathbf{O(1)}$ Single CPU Cycle⚡| $\mathbf{O(1)}$ Memory ⚡| **64-bit cast guard ⚡**|
| **Modular Division** | `(a * b^-1) % M` | $\mathbf{O(\log M)}$ Fast Exponent| $\mathbf{O(1)}$ Memory ⚡| Fermat $b^{M-2} \bmod M$ |

---

## 10. Edge Cases & Boundary Handling

1. **Division by Zero ($b = 0 \pmod M$)**:
   - Modular inverse does not exist if $b \equiv 0 \pmod M$. Throws arithmetic exception.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Direct Division `(a / b) % M`**:
  - `(12 / 4) % 7 = 3`, but for non-divisible numbers `(5 / 2) % 7` truncates to `2 % 7 = 2` (INCORRECT!). **ALWAYS compute division via modular inverse `(a * modInverse(b)) % M`!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Modular Arithmetic Guards:
> * **Subtraction Guard**: `(a - b % M + M) % M` (Prevents negative remainders!).
> * **Multiplication Guard**: `((long) a * b) % M` (Prevents 32-bit int overflow!). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Direct Integer Arithmetic | Modular Arithmetic |
| :--- | :--- | :--- |
| **Overflow Risk** | High Risk of Truncation / Over | **Zero Overflow (Wrapped at $M$) ⚡** |
| **Division Behavior** | Standard Integer Truncation | **Multiplicative Inverse ($b^{-1}$) ⚡** |
| **Standard Modulus**| N/A | **$M = 10^9 + 7$ (Prime) ⚡** |

---

## 14. How to Recognize This in Questions

* **"Return answer modulo 10^9 + 7"** $\rightarrow$ Apply modular addition, subtraction, and multiplication laws at every calculation step.

---

## 15. Frequently Asked Interview Questions

* **Q: Why do competitive programming problems request answers modulo $10^9 + 7$?**  
  *A:* Because $10^9 + 7$ is a large prime number that fits safely inside a 32-bit signed integer. Its prime property guarantees that every non-zero integer has a unique modular inverse modulo $10^9 + 7$.

* **Q: Why is `(a - b) % M` unsafe in Java?**  
  *A:* Because Java's `%` operator is remainder, which returns negative values when $a < b$ (e.g. `-5 % 7 = -5`). Adding $+M$ (`(a - b % M + M) % M`) guarantees non-negative results.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MODULAR ARITHMETIC                                    |
+-----------------------------------------------------------------------+
| • Modular Add     : (a + b) % M                                       |
| • Modular Subtract: (a - b % M + M) % M (Adds +M for negative guard!) ⚡|
| • Modular Multiply: ((long) a * b) % M (Casts long for overflow guard!)⚡|
| • Modular Divide  : (a * modInverse(b)) % M                           |
| • Standard Modulus: M = 10^9 + 7 or M = 998,244,353 (Large Primes) ⚡   |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write safe modular addition, subtraction, and multiplication in Java.
- [ ] I can explain why `(a - b % M + M) % M` is required for negative subtraction.
- [ ] I can explain why `(long)` cast is required before multiplying two integers.
- [ ] I can write modular division using modular multiplicative inverse.
- [ ] I can state why $M = 10^9 + 7$ is widely chosen in algorithms.
