# 07. Euler Totient Function: Product Formula, Euler's Theorem & Totient Sieve

## 1. Introduction
The **Euler Totient Function** (denoted by the Greek letter **$\phi(N)$** or **phi(N)**) is a fundamental multiplicative function in Number Theory that counts the total number of positive integers $k$ in the range $1 \le k \le N$ that are **coprime to $N$** ($\gcd(k, N) = 1$). Euler's Totient function plays a vital role in public-key cryptography (specifically RSA encryption key generation), group theory, modular reduction for huge exponents, and primitive root identification. Using the prime factorization of $N = p_1^{e_1} \cdot p_2^{e_2} \dots p_k^{e_k}$, Euler derived the **Euler Totient Product Formula**, computing $\phi(N)$ in **$O(\sqrt{N})$ Time**. Furthermore, **Euler's Theorem ($A^{\phi(M)} \equiv 1 \pmod M$)** generalizes Fermat's Little Theorem for any arbitrary coprime modulus $M$.

> **Important:** Core Structural Formulas of Euler Totient Function:
> 1. **Euler Totient Definition**:
>    $$\phi(N) = \left| \{ k \in \{1, 2 \dots N\} : \gcd(k, N) = 1 \} \right|$$
> 2. **Euler Totient Product Formula**:
>    $$\phi(N) = N \times \prod_{p \mid N} \left(1 - \frac{1}{p}\right) = N \times \prod_{p \mid N} \frac{p - 1}{p}$$
> 3. **Special Cases**:
>    - For a prime number $P$: $\phi(P) = P - 1$.
>    - For a prime power $P^k$: $\phi(P^k) = P^k - P^{k-1} = P^k \left(1 - \frac{1}{P}\right)$.
>    - For two coprime numbers $\gcd(A, B) = 1$: $\phi(A \times B) = \phi(A) \times \phi(B)$ (Multiplicative property!).
> 4. **Euler's Theorem (Exponent Reduction for Huge Exponents)**:
>    - If $\gcd(A, M) = 1$:
>      $$A^B \pmod M = A^{B \pmod{\phi(M)}} \pmod M$$ ⚡

```
Euler Totient Calculation Topology (N = 12):

Coprime Numbers to 12 in Range 1..12:
- gcd(1, 12) = 1  ✅
- gcd(5, 12) = 1  ✅
- gcd(7, 12) = 1  ✅
- gcd(11, 12) = 1 ✅
Total Coprime Count phi(12) = 4!

Using Euler Product Formula:
- Prime factorization of 12: 12 = 2^2 * 3^1 (Distinct prime factors: 2, 3)
- phi(12) = 12 * (1 - 1/2) * (1 - 1/3)
          = 12 * (1/2) * (2/3) = 4! (Exact Match!) ✅ ⚡
```

---

## 2. Core Concepts & Euler Totient Strategy Matrix

### 2.1 Euler Totient Computation Strategy Matrix
```
Euler Totient Computation Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Computation Method    | Target Use Case   | Time Complexity   | Auxiliary Space   | Key Formula       |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Trial Division**    | Single Integer $N$| **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**| $N \prod \frac{p-1}{p}$|
| **Totient Sieve Array**| Range $1 \dots N$ | **$O(N \log \log N)$⚡**| $O(N)$ Array Space| Sieve modification|
| **Linear Euler Sieve**| Range $1 \dots N$ | **$O(N)$ Linear ⚡**| $O(N)$ Array Space| Prime multiplicative|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Euler Product Formula: phi(N) = N * (p1-1)/p1 * (p2-1)/p2 ...; For prime P, phi(P) = P - 1; Reduces huge exponents A^B % M = A^(B % phi(M)) % M!"**

---

## 3. Characteristics & Euler's Theorem Mathematical Proof

### 3.1 Mathematical Proof of Euler's Theorem ($A^{\phi(M)} \equiv 1 \pmod M$)
* Let $S = \{r_1, r_2 \dots r_{\phi(M)}\}$ be the set of $\phi(M)$ positive integers less than $M$ that are coprime to $M$.
* Multiply every element in $S$ by $A$ (where $\gcd(A, M) = 1$):
  $$S' = \{A \cdot r_1, A \cdot r_2 \dots A \cdot r_{\phi(M)}\}$$
* **Claim**: The elements of $S'$ modulo $M$ are distinct and form a permutation of the set $S$.
  - *Proof of Distinctness*: If $A \cdot r_i \equiv A \cdot r_j \pmod M$, multiplying by $A^{-1}$ yields $r_i \equiv r_j \pmod M$. Thus, all $\phi(M)$ elements in $S'$ are distinct modulo $M$.
  - *Proof of Coprimality*: Since $\gcd(A, M) = 1$ and $\gcd(r_i, M) = 1$, $\gcd(A \cdot r_i, M) = 1$.
* Multiplying all elements of $S'$ together:
  $$\prod_{i=1}^{\phi(M)} (A \cdot r_i) \equiv \prod_{i=1}^{\phi(M)} r_i \pmod M$$
  $$A^{\phi(M)} \times \left( \prod_{i=1}^{\phi(M)} r_i \right) \equiv \left( \prod_{i=1}^{\phi(M)} r_i \right) \pmod M$$
* Since $\prod r_i$ is coprime to $M$, we can divide both sides by $\prod r_i$:
  $$A^{\phi(M)} \equiv 1 \pmod M$$
* Proves Euler's Theorem for all coprime integers $A$ and $M$! ⚡

---

## 4. Internal Working Mechanics: Totient Sieve $1 \dots N$ Array

Tracing Totient Sieve Array for $N = 10$:

```
Initial Array: phi[i] = i for i = 0..10.
phi = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

Processing Prime 2:
- For i = 2, 4, 6, 8, 10: phi[i] = phi[i] - phi[i]/2 = phi[i] / 2.
- phi = [0, 1, 1, 3, 2, 5, 3, 7, 4, 9, 5]

Processing Prime 3:
- For i = 3, 6, 9: phi[i] = phi[i] - phi[i]/3.
- phi[3] = 3 - 1 = 2; phi[6] = 3 - 1 = 2; phi[9] = 9 - 3 = 6.
- phi = [0, 1, 1, 2, 2, 5, 2, 7, 4, 6, 5]

Processing Prime 5:
- For i = 5, 10: phi[5] = 4; phi[10] = 5 - 1 = 4.
- phi = [0, 1, 1, 2, 2, 4, 2, 7, 4, 6, 4]

Processing Prime 7:
- phi[7] = 6.

Final phi Array [1..10]: [1, 1, 2, 2, 4, 2, 6, 4, 6, 4] in O(N log log N) Time! ✅ ⚡
```

---

## 5. Visual Diagram: RSA Cryptography Key Generation via Euler Totient

```
RSA Public-Key Encryption Pipeline:

Select Two Large Primes: P = 61, Q = 53
- Modulus N = P * Q = 61 * 53 = 3,233.
- Compute Euler Totient phi(N) = (P - 1) * (Q - 1) = 60 * 52 = 3,120! ⚡

Select Public Exponent E (Coprime to phi(N)): E = 17 (gcd(17, 3120) = 1)
Compute Private Key D: D = E^-1 mod phi(N) = 17^-1 mod 3120 = 2,753! ⚡

Encryption: Cipher = (Message^E) % N
Decryption: Message = (Cipher^D) % N ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Single Value Euler Totient $\phi(N)$ ($O(\sqrt{N})$), Range Totient Sieve $\phi(1) \dots \phi(N)$ ($O(N \log \log N)$), and Exponent Reduction Engine using Euler's Theorem.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Euler Totient Function:
 * Trial Division Phi(N), Range Totient Sieve Array, and Euler Exponent Reduction Engine.
 */
public class EulerTotientMaster {

    // =========================================================================
    // 1. TRIAL DIVISION EULER TOTIENT PHI(N) (O(sqrt(N)) Time, O(1) Space)
    // =========================================================================
    /**
     * Computes Euler Totient phi(n) using Product Formula in O(sqrt(N)) time.
     *
     * @param n target positive integer
     * @return count of integers <= n coprime to n
     */
    public long getEulerTotient(long n) {
        if (n <= 0) return 0;
        long result = n; // Start with result = N ⚡
        long temp = n;

        // Check prime factor 2
        if (temp % 2 == 0) {
            while (temp % 2 == 0) temp /= 2;
            result -= result / 2; // Multiply by (1 - 1/2) ⚡
        }

        // Check odd prime factors p from 3 up to sqrt(temp)
        for (long p = 3; p * p <= temp; p += 2) {
            if (temp % p == 0) {
                while (temp % p == 0) temp /= p;
                result -= result / p; // Multiply by (1 - 1/p) ⚡
            }
        }

        // Remaining prime factor > sqrt(N)
        if (temp > 1) {
            result -= result / temp;
        }

        return result;
    }

    // =========================================================================
    // 2. RANGE TOTIENT SIEVE ARRAY 1 ... N (O(N log log N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates array phi where phi[i] is Euler Totient of i for 1 <= i <= n.
     */
    public int[] computeTotientSieve(int n) {
        int[] phi = new int[n + 1];
        for (int i = 0; i <= n; i++) phi[i] = i;

        for (int p = 2; p <= n; p++) {
            if (phi[p] == p) { // p is prime ⚡
                for (int j = p; j <= n; j += p) {
                    phi[j] -= phi[j] / p; // Update all multiples of p ⚡
                }
            }
        }

        return phi;
    }

    // =========================================================================
    // 3. EULER'S THEOREM EXPONENT REDUCTION (A^B mod M = A^(B mod phi(M)) mod M)
    // =========================================================================
    /**
     * Computes A^B mod M for huge exponent B using Euler's Theorem.
     */
    public long powerEulerReduction(long a, long b, long mod) {
        if (gcd(a, mod) == 1) {
            long phiM = getEulerTotient(mod);
            b = b % phiM; // Reduce exponent modulo phi(M)! ⚡
        }
        return powerModular(a, b, mod);
    }

    private long gcd(long a, long b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b);
    }

    private long powerModular(long base, long exp, long mod) {
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
// Euler Totient Product Formula Line
if (temp % p == 0) { while (temp % p == 0) temp /= p; result -= result / p; }
```

---

## 7. Concrete Problem Examples & Applications

1. **RSA Encryption Key Generation**:
   - Computing $\phi(N) = (P - 1)(Q - 1)$ for prime factors $P$ and $Q$.

2. **Huge Exponent Reduction ($A^B \pmod M$)**:
   - Reducing exponents $B \approx 10^{18}$ using $B \pmod{\phi(M)}$.

3. **Multi-Query Totient Benchmarks**:
   - Range totient sieve generation for competitive programming ($O(N \log \log N)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class EulerTotientDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   EULER TOTIENT FUNCTION BENCHMARK DEMO         ");
        System.out.println("=================================================\n");

        EulerTotientMaster master = new EulerTotientMaster();

        // 1. Single Phi(N) Test (N = 12, N = 360)
        System.out.println("1. Trial Division Euler Totient Phi(N):");
        System.out.println("   phi(12)  : " + master.getEulerTotient(12) + " (Optimal = 4)");
        System.out.println("   phi(360) : " + master.getEulerTotient(360) + " (Optimal = 96)");
        System.out.println("-------------------------------------------------");

        // 2. Range Totient Sieve Test (1 ... 10)
        int[] phiArray = master.computeTotientSieve(10);
        System.out.println("2. Range Totient Sieve Array for 1...10:");
        System.out.println("   phi[1..10]: " + Arrays.toString(Arrays.copyOfRange(phiArray, 1, 11)));
        System.out.println("-------------------------------------------------");

        // 3. Exponent Reduction via Euler's Theorem (3^1000000 mod 7)
        long reducedPow = master.powerEulerReduction(3, 1_000_000, 7);
        System.out.println("3. Huge Exponent Reduction (3^1000000) % 7:");
        System.out.println("   Result: " + reducedPow + " (Optimal = 1)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Euler Totient Task | Algorithm Engine | Time Complexity | Auxiliary Space | Key Formula |
| :--- | :--- | :--- | :--- | :--- |
| **Trial Division Phi(N)**| Prime Factorization| $\mathbf{O(\sqrt{N})}$ Linear ⚡| $\mathbf{O(1)}$ Memory ⚡| $N \prod \frac{p-1}{p}$ |
| **Totient Sieve Array**| Sieve Array Update| $\mathbf{O(N \log \log N)}$⚡| $O(N)$ Array Space| `phi[j] -= phi[j]/p` |
| **Euler Exponent Reduc**| Euler's Theorem | $\mathbf{O(\log M)}$ Fast Power| $\mathbf{O(1)}$ Memory ⚡| $B \pmod{\phi(M)}$ |

---

## 10. Edge Cases & Boundary Handling

1. **Input $N = 1$**:
   - $\phi(1) = 1$ (1 is coprime to itself).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Running $O(N \log N)$ Loop Checking `gcd(i, N) == 1`**:
  - Running a loop checking `gcd(i, N)` for every integer $1 \dots N$ takes $O(N \log N)$ time. **ALWAYS use Euler's Product Formula `result -= result / p` to achieve $O(\sqrt{N})$ time!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Euler's Exponent Reduction Rule:
> For any base $A$ and coprime modulus $M$ ($\gcd(A, M) = 1$), reduce huge exponents $B$ using Euler's Totient $\phi(M)$:
> $$A^B \pmod M = A^{B \pmod{\phi(M)}} \pmod M$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive GCD Count Loop | Euler Product Formula |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \log N)$ (Slow!) | **$O(\sqrt{N})$ Fast ⚡** |
| **Operations (N=10^12)**| $10^{12}$ GCD Calls | **$10^6$ Factor Operations ⚡** |
| **RSA Suitability** | Impossible | **Instant Computation ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count numbers <= N coprime to N"** $\rightarrow$ Euler Totient Function $\phi(N)$.
* **"Compute A^B % M for massive exponent B"** $\rightarrow$ Euler Exponent Reduction $B \pmod{\phi(M)}$.

---

## 15. Frequently Asked Interview Questions

* **Q: What is Euler's Product Formula for $\phi(N)$?**  
  *A:* $\phi(N) = N \times \prod_{p \mid N} \left(1 - \frac{1}{p}\right)$.

* **Q: Why is $\phi(P) = P - 1$ for a prime number $P$?**  
  *A:* Because every integer $1, 2 \dots P-1$ is strictly less than $P$ and shares no common factors with prime $P$, so all $P-1$ numbers are coprime to $P$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: EULER TOTIENT FUNCTION                                |
+-----------------------------------------------------------------------+
| • Definition   : phi(N) = count of integers 1..N coprime to N         |
| • Product Form : phi(N) = N * ∏ (p - 1) / p for distinct primes p     |
| • Prime Rule   : phi(P) = P - 1 for prime P; phi(P^k) = P^k - P^(k-1)  |
| • Totient Sieve: phi[j] -= phi[j] / p for all multiples j of prime p ⚡|
| • Euler Theorem: A^B % M = A^(B % phi(M)) % M for gcd(A, M) = 1 ⚡    |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write single-value Euler Totient $\phi(N)$ in $O(\sqrt{N})$ time in Java.
- [ ] I can write Totient Sieve $\phi(1) \dots \phi(N)$ in $O(N \log \log N)$ time in Java.
- [ ] I can explain Euler's Product Formula $\phi(N) = N \prod \frac{p-1}{p}$.
- [ ] I can write Exponent Reduction using Euler's Theorem $B \pmod{\phi(M)}$.
- [ ] I can explain how RSA encryption uses $\phi(N) = (P - 1)(Q - 1)$.
