# 02. Prime Algorithms: Sieve of Eratosthenes, Segmented Sieve & Miller-Rabin Primality

## 1. Introduction
**Prime Numbers** (integers $P > 1$ divisible ONLY by 1 and $P$) are the fundamental building blocks of integers and modern cryptography. Generating prime numbers and verifying primality are two of the most deeply studied algorithmic challenges in computer science. Algorithms for prime generation and testing span three primary tiers:
1. **Primality Testing**:
   - **Trial Division**: Deterministic check in **$O(\sqrt{N})$ Time**.
   - **Miller-Rabin Primality Test**: Probabilistic (and 64-bit deterministic with fixed bases) primality test in **$O(K \log^3 N)$ Time**, powering RSA key generation for 2048-bit primes!
2. **Prime Generation Sieves**:
   - **Sieve of Eratosthenes**: Generates all primes up to $N$ in **$O(N \log \log N)$ Time** ($O(N)$ Space).
   - **Segmented Sieve**: Generates primes in a range $[L, R]$ in **$O((R - L + 1) \log \log R + \sqrt{R})$ Time** using only **$O(\sqrt{R})$ Space** (fits in CPU L1 cache!).
   - **Linear Sieve of Euler**: Visits every composite number EXACTLY ONCE in **$O(N)$ Strict Linear Time**.

> **Important:** Core Structural Properties of Prime Algorithms:
> 1. **Sieve of Eratosthenes Time Complexity Proof**:
>    $$\sum_{p \le N} \frac{N}{p} = N \sum_{p \le N} \frac{1}{p} = O(N \log \log N)$$
> 2. **Miller-Rabin Fermat's Little Theorem Basis**:
>    - If $P$ is prime, then for any $1 \le a < P$: $a^{P-1} \equiv 1 \pmod P$.
>    - Write $N - 1 = 2^s \cdot d$ (where $d$ is odd). For base $a$: either $a^d \equiv 1 \pmod N$ or $a^{2^r \cdot d} \equiv -1 \pmod N$ for some $0 \le r < s$.
> 3. **Segmented Sieve Memory Advantage**:
>    - Standard Sieve for $R = 10^9$ requires 1 GB RAM ($O(R)$ space).
>    - Segmented Sieve processes range $[L, R]$ in blocks of size $\sqrt{R} \approx 31,622$, requiring **less than 32 KB RAM** ($O(\sqrt{R})$ space)! ⚡

```
Prime Algorithms Strategy & Complexity Topology:

                  [ Prime Algorithms Decision Engine ]
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
 [ Single Integer Primality ]                     [ Range Prime Generation ]
 ├── Small N (N <= 10^12)                         ├── Range 1 ... N (N <= 10^7)
 │   └── Trial Division: O(sqrt(N)) ⚡               │   └── Sieve of Eratosthenes: O(N log log N) ⚡
 └── Huge N (N > 10^12 / 64-bit Int)              ├── Range L ... R (R <= 10^12, R - L <= 10^6)
     └── Miller-Rabin Test: O(K log^3 N) ⚡          │   └── Segmented Sieve: O(SegmentSize + sqrt(R)) ⚡
                                                  └── Strict Linear O(N) Sieve
                                                      └── Linear Sieve of Euler: O(N) Time ⚡
```

---

## 2. Core Concepts & Prime Algorithms Strategy Matrix

### 2.1 Prime Algorithms Family Strategy Matrix
```
Prime Algorithms Family Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Algorithm Name        | Target Problem    | Time Complexity   | Auxiliary Space   | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Trial Division**    | Single $N \le 10^{12}$| **$O(\sqrt{N})$ Linear ⚡**| **$O(1)$ Memory ⚡**| Zero setup code   |
| **Miller-Rabin Test** | Single Huge $N$   | **$O(K \log^3 N)$ Fast⚡**| **$O(1)$ Memory ⚡**| RSA 2048-bit primes|
| **Sieve of Eratosthenes**| Primes $1 \dots N$| **$O(N \log \log N)$⚡**| $O(N)$ Array Space| Classical Standard|
| **Segmented Sieve**   | Range $[L, R]$    | **$O((R-L+1)\log \log R)$⚡**| **$O(\sqrt{R})$ Space ⚡**| Fits in CPU Cache |
| **Linear Euler Sieve**| Primes + SPF      | **$O(N)$ Linear ⚡**| $O(N)$ Array Space| Every composite 1x|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Sieve of Eratosthenes = O(N log log N); Segmented Sieve = O(sqrt(R)) space for range [L, R]; Miller-Rabin tests huge 64-bit primes!"**

---

## 3. Characteristics & Miller-Rabin Primality Test Proof

### 3.1 Mathematical Principles of Miller-Rabin Test
* **Fermat's Little Theorem**:
  - If $N$ is prime and $\gcd(a, N) = 1$, then:
    $$a^{N-1} \equiv 1 \pmod N$$
* **Square Root of Modulo Unity**:
  - If $N$ is prime, the only solutions to $x^2 \equiv 1 \pmod N$ are $x \equiv 1 \pmod N$ and $x \equiv -1 \pmod N$.
* **Miller-Rabin Test Sequence**:
  1. Factor out powers of 2 from $N - 1$: write $N - 1 = 2^s \cdot d$, where $d$ is odd.
  2. Pick a witness base $a \in [2, N-2]$.
  3. Compute $x = a^d \bmod N$.
  4. If $x \equiv 1 \pmod N$ or $x \equiv N - 1 \pmod N$, base $a$ passes!
  5. Otherwise, square $x$ repeatedly up to $s-1$ times: $x = x^2 \bmod N$.
  6. If $x$ becomes $N - 1$ during squarings, base $a$ passes!
  7. If $x$ never reaches $N - 1$, $N$ is **DEFINITELY COMPOSITE**!
* **Deterministic 64-Bit Primality**:
  - Testing against 12 fixed prime bases: `a ∈ {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}` guarantees 100% deterministic accuracy for ALL 64-bit integers ($N < 2^{64}$)! ⚡

---

## 4. Internal Working Mechanics: Segmented Sieve Range $[L, R]$

Tracing Segmented Sieve for Range $[L = 10, R = 30]$ ($\sqrt{30} = 5$, Small Primes $= [2, 3, 5]$):

```
Segment Offset Index mapping: Real Number X -> Array Index (X - L) = (X - 10).

Small Primes up to sqrt(30) = 5: [2, 3, 5]

Mark Composites in Segment [10 ... 30] (Boolean array of size 30 - 10 + 1 = 21):

- Prime 2: First multiple >= 10 is 10. Mark 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30.
- Prime 3: First multiple >= 10 is 12. Mark 12, 15, 18, 21, 24, 27, 30.
- Prime 5: First multiple >= 10 is 10. Mark 10, 15, 20, 25, 30.

Unmarked Numbers in Segment [10 ... 30]:
[11, 13, 17, 19, 23, 29] (All 6 Primes Found!) ✅ ⚡
```

---

## 5. Visual Diagram: Segmented Sieve Memory Block Allocation

```
Segmented Sieve CPU Cache-Friendly Memory Pipeline:

Entire Search Space: [ 10^12 .................................... 10^12 + 10^6 ]
                                         │
                   Segment Block Processed in 32 KB L1 Cache
                                         │
┌────────────────────────┬────────────────────────┬────────────────────────┐
│ Block 1 [L ... L+32K]  │ Block 2 [L+32K ... ]   │ Block 3 [ ... R]       │
└────────────────────────┴────────────────────────┴────────────────────────┘

Auxiliary Memory = O(sqrt(R)) = 31,622 Bytes (Fits inside CPU L1 Data Cache!) ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Sieve of Eratosthenes ($O(N \log \log N)$), Segmented Sieve for range $[L, R]$ ($O(\sqrt{R})$ space), Linear Euler Sieve ($O(N)$), and Deterministic Miller-Rabin Test for 64-bit integers.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Prime Algorithms:
 * Sieve of Eratosthenes, Segmented Sieve, Linear Euler Sieve, and 64-Bit Miller-Rabin Test.
 */
public class PrimeAlgorithmsMaster {

    // =========================================================================
    // 1. SIEVE OF ERATOSTHENES (O(N log log N) Time, O(N) Space)
    // =========================================================================
    /**
     * Generates boolean array isPrime where isPrime[i] is true if i is prime.
     */
    public boolean[] sieveOfEratosthenes(int n) {
        boolean[] isPrime = new boolean[n + 1];
        Arrays.fill(isPrime, true);
        if (n >= 0) isPrime[0] = false;
        if (n >= 1) isPrime[1] = false;

        for (int p = 2; p * p <= n; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= n; i += p) { // Start marking at p^2 ⚡
                    isPrime[i] = false;
                }
            }
        }

        return isPrime;
    }

    // =========================================================================
    // 2. SEGMENTED SIEVE FOR RANGE [L, R] (O((R-L+1) log log R) Time, O(sqrt(R)) Space)
    // =========================================================================
    /**
     * Finds all prime numbers in range [L, R] inclusive.
     */
    public List<Long> segmentedSieve(long L, long R) {
        List<Long> primesInRange = new ArrayList<>();
        if (L > R || R < 2) return primesInRange;
        L = Math.max(L, 2);

        int limit = (int) Math.sqrt(R);
        boolean[] smallSieve = sieveOfEratosthenes(limit);
        List<Integer> smallPrimes = new ArrayList<>();
        for (int i = 2; i <= limit; i++) {
            if (smallSieve[i]) smallPrimes.add(i);
        }

        int segmentSize = (int) (R - L + 1);
        boolean[] isPrimeSegment = new boolean[segmentSize];
        Arrays.fill(isPrimeSegment, true);

        for (int p : smallPrimes) {
            // First multiple of p >= L ⚡
            long start = Math.max((long) p * p, ((L + p - 1) / p) * (long) p);
            for (long j = start; j <= R; j += p) {
                isPrimeSegment[(int) (j - L)] = false;
            }
        }

        for (int i = 0; i < segmentSize; i++) {
            if (isPrimeSegment[i]) {
                primesInRange.add(L + i);
            }
        }

        return primesInRange;
    }

    // =========================================================================
    // 3. DETERMINISTIC 64-BIT MILLER-RABIN PRIMALITY TEST (O(K log^3 N) Time)
    // =========================================================================
    private static final long[] MILLER_RABIN_BASES = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};

    public boolean isPrimeMillerRabin(long n) {
        if (n < 2) return false;
        if (n == 2 || n == 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;

        // Write n - 1 = 2^s * d
        long d = n - 1;
        int s = 0;
        while ((d & 1) == 0) {
            d >>= 1;
            s++;
        }

        for (long a : MILLER_RABIN_BASES) {
            if (n <= a) break;
            if (!millerRabinWitness(a, d, s, n)) return false; // Composite! ⚡
        }

        return true; // Prime! ⚡
    }

    private boolean millerRabinWitness(long a, long d, int s, long n) {
        long x = modularExponentiation(a, d, n);
        if (x == 1 || x == n - 1) return true;

        for (int r = 1; r < s; r++) {
            x = modularMultiply(x, x, n);
            if (x == n - 1) return true;
        }

        return false;
    }

    private long modularExponentiation(long base, long exp, long mod) {
        long res = 1;
        base %= mod;
        while (exp > 0) {
            if ((exp & 1) == 1) res = modularMultiply(res, base, mod);
            base = modularMultiply(base, base, mod);
            exp >>= 1;
        }
        return res;
    }

    private long modularMultiply(long a, long b, long mod) {
        return (long) ((java.math.BigInteger.valueOf(a)
                .multiply(java.math.BigInteger.valueOf(b)))
                .mod(java.math.BigInteger.valueOf(mod)).longValue());
    }
}
```

> **Quick Syntax:**
```java
// Sieve & Miller-Rabin Lines
long start = Math.max((long) p * p, ((L + p - 1) / p) * (long) p); // Segmented Sieve start offset
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 204 - Count Primes**:
   - Prime counting benchmark solved using Sieve of Eratosthenes in $O(N \log \log N)$ time.

2. **RSA Cryptographic Key Generation**:
   - 2048-bit prime testing using Miller-Rabin primality engine.

3. **Segmented Sieve Range Queries ($10^{12}$ limits)**:
   - Finding primes in range $[10^{12}, 10^{12} + 10^6]$ using $O(\sqrt{R})$ space.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class PrimeAlgorithmsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   PRIME ALGORITHMS BENCHMARK DEMO               ");
        System.out.println("=================================================\n");

        PrimeAlgorithmsMaster master = new PrimeAlgorithmsMaster();

        // 1. Sieve of Eratosthenes Test (N = 30)
        int n = 30;
        boolean[] isPrime = master.sieveOfEratosthenes(n);
        int primeCount = 0;
        for (boolean b : isPrime) if (b) primeCount++;

        System.out.println("1. Sieve of Eratosthenes for N = 30:");
        System.out.println("   Total Primes Count (<= 30): " + primeCount + " (Optimal = 10)");
        System.out.println("-------------------------------------------------");

        // 2. Segmented Sieve Test (Range [10, 30])
        List<Long> rangePrimes = master.segmentedSieve(10, 30);
        System.out.println("2. Segmented Sieve for Range [10, 30]:");
        System.out.println("   Primes List: " + rangePrimes + " (Optimal = [11, 13, 17, 19, 23, 29])");
        System.out.println("-------------------------------------------------");

        // 3. Deterministic 64-Bit Miller-Rabin Test
        long hugePrime = 1_000_000_007L;
        long hugeComposite = 1_000_000_009L; // 7 * 142857144...

        System.out.println("3. 64-Bit Deterministic Miller-Rabin Test:");
        System.out.println("   Is 1,000,000,007 Prime: " + master.isPrimeMillerRabin(hugePrime) + " (Optimal = true)");
        System.out.println("   Is 1,000,000,009 Prime: " + master.isPrimeMillerRabin(hugeComposite) + " (Optimal = false)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Prime Algorithm | Target Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Sieve of Eratosthenes**| Range $1 \dots N$ | $\mathbf{O(N \log \log N)}$ ⚡| $O(N)$ Array Space| Mark starting at $p^2$ |
| **Segmented Sieve**   | Range $[L, R]$ | $\mathbf{O((R-L+1)\log \log R)}$⚡| $\mathbf{O(\sqrt{R})}$ Space ⚡| Fits in CPU L1 Cache |
| **Linear Euler Sieve**| Range $1 \dots N$ | $\mathbf{O(N)}$ Linear ⚡| $O(N)$ Array Space| Every composite 1x |
| **Miller-Rabin Test** | Single Huge $N$ | $\mathbf{O(K \log^3 N)}$ Fast⚡| $\mathbf{O(1)}$ Memory ⚡| 12 Fixed Bases for 64-bit |

---

## 10. Edge Cases & Boundary Handling

1. **Input Range $L = 1$ in Segmented Sieve**:
   - Enforce `L = Math.max(L, 2)` to avoid marking 1 as prime.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Starting Inner Sieve Marking Loop at $2p$ Instead of $p^2$**:
  - Starting loop at $2p$ redundantly re-marks multiples already cleared by smaller prime factors. **ALWAYS start inner sieve loop at $p * p$!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Segmented Sieve Memory Rule:
> Use Segmented Sieve whenever range limit $R \ge 10^9$ or range $[L, R]$ is specified, reducing space from $O(R)$ (1 GB RAM) to **$O(\sqrt{R})$ (32 KB RAM)**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Standard Sieve ($O(N)$ Space) | Segmented Sieve ($O(\sqrt{R})$ Space) |
| :--- | :--- | :--- |
| **Memory ($R = 10^9$)**| 1 GB Heap Memory (OOM Risk) | **32 KB L1 Cache Memory ⚡** |
| **Cache Locality** | Poor Pointer / Large Vector | **Optimal L1 Cache Hits ⚡** |
| **Range Flexibility**| Only $1 \dots N$ | **Arbitrary Range $[L, R]$ ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count total primes up to N"** $\rightarrow$ LeetCode 204 (Sieve of Eratosthenes).
* **"Find all primes in range [L, R] where R <= 10^12 and R - L <= 10^6"** $\rightarrow$ Segmented Sieve.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Sieve of Eratosthenes start marking multiples at $p^2$?**  
  *A:* Because all smaller multiples of $p$ ($2p, 3p \dots (p-1)p$) have already been marked by smaller prime factors ($2, 3 \dots p-1$).

* **Q: Why is Segmented Sieve faster in practice than standard Sieve for large $N$?**  
  *A:* Because Segmented Sieve processes small array blocks ($O(\sqrt{R})$) that fit entirely inside the CPU L1 data cache, eliminating main RAM bus latency.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: PRIME ALGORITHMS                                      |
+-----------------------------------------------------------------------+
| • Sieve of Eratosthenes: O(N log log N) time | Starts loop at p * p   |
| • Segmented Sieve      : O((R-L+1) log log R) time | O(sqrt(R)) Space ⚡|
| • Miller-Rabin Test    : O(K log^3 N) deterministic 64-bit int test ⚡|
| • Segmented Start Offset: start = max(p*p, ((L + p - 1)/p)*p)         |
| • Performance          : Fits in 32 KB CPU L1 Cache! ⚡                |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Sieve of Eratosthenes in $O(N \log \log N)$ time in Java.
- [ ] I can write Segmented Sieve for range $[L, R]$ using $O(\sqrt{R})$ memory.
- [ ] I can write Miller-Rabin primality test for 64-bit integers.
- [ ] I can state why inner sieve marking starts at $p^2$.
- [ ] I can explain why Segmented Sieve optimizes CPU L1 cache hits.
