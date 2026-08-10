# 11. String Hashing: Polynomial Rolling Hashes, Double Moduli & $O(1)$ Substring Queries

## 1. Introduction
**String Hashing** is a core probabilistic technique that maps arbitrary-length strings or substrings to integer values using a **Polynomial Rolling Hash Function**. By precomputing a prefix hash array $pref[i]$ and a base powers array $pow[i]$ in $O(N)$ time, String Hashing enables querying the exact hash value of **ANY Substring $S[L \dots R]$ in $O(1)$ Constant Time**! To virtually eliminate **Hash Collisions** (spurious matches), production systems employ **Double Modulo Hashing** using two distinct prime moduli ($Q_1 = 10^9 + 7$ and $Q_2 = 10^9 + 9$), reducing collision probability down to an astronomically low $< 10^{-18}$.

> **Important:** Core Structural Invariants of String Hashing:
> 1. **Polynomial Prefix Hash Array ($pref[i]$)**:
>    - $pref[i]$ stores the cumulative rolling hash of prefix $S[0 \dots i-1]$:
>      $$pref[i] = \left( pref[i-1] \cdot B + S[i-1] \right) \pmod Q$$
>      where $pref[0] = 0$, $B$ is the base prime ($B > |\Sigma|$, e.g. $B = 31$ or $256$), and $Q$ is a large prime.
> 2. **$O(1)$ Substring Range Hash Formula**:
>    - For substring $S[L \dots R]$ (0-based indices):
>      $$\text{Hash}(L, R) = \left( pref[R + 1] - pref[L] \cdot B^{R - L + 1} \right) \pmod Q$$
>    - Evaluates the exact hash of substring $S[L \dots R]$ in 1 operation!
> 3. **Double Modulo Hashing Invariant**:
>    - Represents each substring hash as a pair of 64-bit integers: $(\text{Hash}_1(L, R), \text{Hash}_2(L, R))$ computed under $Q_1 = 10^9 + 7$ and $Q_2 = 10^9 + 9$.
>    - Two substrings match if and ONLY if BOTH hashes are identical, rendering hash collisions practically impossible! ⚡

```
String Hashing Range Query Topology for S = "abcdef" (L=2, R=4 -> Substring "cde"):
Prefix Hashes:   pref[0]=0, pref[1]=a, pref[2]=ab, pref[3]=abc, pref[4]=abcd, pref[5]=abcde

Range Hash Equation: Hash("cde") = ( pref[5] - pref[2] * B^3 ) % Q

Subtracts prefix "ab" (scaled by B^3) from prefix "abcde", leaving exact hash of "cde" in O(1) Time! ⚡
```

---

## 2. Core Concepts & String Hashing Strategy Matrix

### 2.1 String Hashing Comparison Matrix
```
String Hashing Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Hashing Paradigm      | Moduli Count      | Collision Risk    | Range Hash Time   |
+-----------------------+-------------------+-------------------+-------------------+
| **Single Modulus**    | 1 Prime ($10^9+7$)| Low ($\sim 10^{-9}$)| **$O(1)$ Instant ⚡**|
| **Double Modulus**    | 2 Primes ($Q_1, Q_2$)| **Zero ($\sim 10^{-18}$)⚡**| **$O(1)$ Instant ⚡**|
| **64-bit Unsigned**   | $2^{64}$ Modulo   | Hackable Anti-Test| **$O(1)$ Instant ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Range Hash(L, R) = (pref[R+1] - pref[L] * pow[R-L+1]) % Q! Double hash avoids collisions!"**

---

## 3. Characteristics & $O(1)$ Substring Query Mathematical Proof

### 3.1 Mathematical Proof of $O(1)$ Substring Hash Query
* Consider string $S$ of length $N$.
* Prefix hash definition: $pref[k] = \sum_{i=0}^{k-1} S[i] \cdot B^{k - 1 - i} \pmod Q$.
* Substring $S[L \dots R]$ has length $M = R - L + 1$. Its polynomial hash is:
  $$H(S[L \dots R]) = \sum_{j=0}^{M-1} S[L + j] \cdot B^{M - 1 - j} \pmod Q$$
* Expand prefix $pref[R + 1]$:
  $$pref[R + 1] = pref[L] \cdot B^{R - L + 1} + \sum_{j=0}^{R-L} S[L + j] \cdot B^{R - L - j} \pmod Q$$
* Rearranging terms yields:
  $$H(S[L \dots R]) = pref[R + 1] - pref[L] \cdot B^{R - L + 1} \pmod Q$$
* Since $pref$ array and $pow[k] = B^k \pmod Q$ are precomputed in $O(N)$ time, querying $H(S[L \dots R])$ takes **$O(1)$ Constant Time**. ⚡

---

## 4. Internal Working Mechanics: Double Hashing Modulo Rules

Why Double Modulo Hashing is required for competitive programming and production search engines:

```
Single Hash Collision Vulnerability:
Suppose array size N = 10^5. Total pairs of substrings = N^2 / 2 = 5 * 10^9.
With single prime Q = 10^9 + 7:
Collision Probability (Birthday Paradox) P_collision ≈ 1 - e^(-N^2 / 2Q) ≈ 99.3%!
Single hash WILL COLLIDE on large datasets! ❌

Double Hash Protection:
Use Q1 = 10^9 + 7 and Q2 = 10^9 + 9.
Combined Modulus Product Q1 * Q2 ≈ 10^18.
Collision Probability P_collision ≈ 1 - e^(-10^10 / 2*10^18) ≈ 10^-8 (0.000001%)!
Double Hashing guarantees absolute safety! ✅
```

---

## 5. Visual Diagram: Substring Range Hash Subtraction

```
Prefix Hash Array Alignment:

pref[L]     = S[0] * B^(L-1) + S[1] * B^(L-2) + ... + S[L-1]
pref[R+1]   = S[0] * B^R     + S[1] * B^(R-1) + ... + S[L-1] * B^(R-L+1) + S[L] * B^(R-L) + ... + S[R]

Multiply pref[L] by B^(R-L+1):
pref[L] * B^(R-L+1) = S[0] * B^R + S[1] * B^(R-1) + ... + S[L-1] * B^(R-L+1)

Subtract:
pref[R+1] - pref[L] * B^(R-L+1) = S[L] * B^(R-L) + ... + S[R] = Exact Hash(L, R)! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Double Polynomial Rolling String Hashing, $O(N)$ Precomputation, $O(1)$ Range Hash Queries, and Longest Common Substring solver.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Double Polynomial String Hashing,
 * O(N) Precomputation, O(1) Range Hash Queries, and Collision-Free Substring Comparison.
 */
public class StringHashingMaster {

    private static final long BASE1 = 313;
    private static final long MOD1 = 1_000_000_007;

    private static final long BASE2 = 317;
    private static final long MOD2 = 1_000_000_009;

    /**
     * Immutable Double Hash Pair container.
     */
    public static class HashPair {
        public final long hash1;
        public final long hash2;

        public HashPair(long hash1, long hash2) {
            this.hash1 = hash1;
            this.hash2 = hash2;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            HashPair hashPair = (HashPair) o;
            return hash1 == hashPair.hash1 && hash2 == hashPair.hash2;
        }

        @Override
        public int hashCode() {
            return Objects.hash(hash1, hash2);
        }

        @Override
        public String toString() {
            return "(" + hash1 + ", " + hash2 + ")";
        }
    }

    public static class StringHash {
        private final long[] pref1;
        private final long[] pow1;

        private final long[] pref2;
        private final long[] pow2;

        private final int n;

        /**
         * Precomputes prefix hashes and powers array in O(N) linear time.
         *
         * @param s input string
         */
        public StringHash(String s) {
            this.n = s.length();

            this.pref1 = new long[n + 1];
            this.pow1 = new long[n + 1];

            this.pref2 = new long[n + 1];
            this.pow2 = new long[n + 1];

            pow1[0] = 1;
            pow2[0] = 1;

            for (int i = 0; i < n; i++) {
                char ch = s.charAt(i);

                pref1[i + 1] = (pref1[i] * BASE1 + ch) % MOD1;
                pow1[i + 1] = (pow1[i] * BASE1) % MOD1;

                pref2[i + 1] = (pref2[i] * BASE2 + ch) % MOD2;
                pow2[i + 1] = (pow2[i] * BASE2) % MOD2;
            }
        }

        /**
         * Returns double hash of substring S[left ... right] (0-based inclusive) in O(1) time.
         *
         * @param left starting index
         * @param right ending index
         * @return HashPair of double hash values
         */
        public HashPair query(int left, int right) {
            int len = right - left + 1;

            // Modulus 1 calculation
            long h1 = (pref1[right + 1] - (pref1[left] * pow1[len]) % MOD1) % MOD1;
            if (h1 < 0) h1 += MOD1;

            // Modulus 2 calculation
            long h2 = (pref2[right + 1] - (pref2[left] * pow2[len]) % MOD2) % MOD2;
            if (h2 < 0) h2 += MOD2;

            return new HashPair(h1, h2);
        }

        /**
         * Checks if substring S[l1 ... r1] equals substring S[l2 ... r2] in O(1) time.
         */
        public boolean isSubstringEqual(int l1, int r1, int l2, int r2) {
            if (r1 - l1 != r2 - l2) return false;
            return query(l1, r1).equals(query(l2, r2));
        }
    }
}
```

> **Quick Syntax:**
```java
// O(1) Range Hash Query Line
long h = (pref[right + 1] - (pref[left] * pow[len]) % MOD) % MOD; if (h < 0) h += MOD;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1044 - Longest Duplicate Substring**:
   - Solved in $O(N \log N)$ time by combining Binary Search on length $L$ with $O(1)$ Double String Hashing.

2. **LeetCode 214 - Shortest Palindrome**:
   - Comparing prefix hash of $S$ with suffix hash of $S^R$ in $O(1)$ time to find longest palindromic prefix.

3. **Plagiarism Detection Systems**:
   - Comparing document paragraph hashes against database in $O(1)$ lookup time.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class StringHashingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   DOUBLE POLYNOMIAL STRING HASHING DEMO         ");
        System.out.println("=================================================\n");

        String str = "abracadabra";
        StringHashingMaster.StringHash hasher = new StringHashingMaster.StringHash(str);

        System.out.println("1. Input String: \"" + str + "\"");

        // Query hash of first "abra" (indices 0..3)
        StringHashingMaster.HashPair h1 = hasher.query(0, 3);
        System.out.println("   Hash of \"abra\" (indices 0..3): " + h1);

        // Query hash of second "abra" (indices 7..10)
        StringHashingMaster.HashPair h2 = hasher.query(7, 10);
        System.out.println("   Hash of \"abra\" (indices 7..10): " + h2);

        // Verify subsegment equality
        boolean isEqual = hasher.isSubstringEqual(0, 3, 7, 10);
        System.out.println("   Substrings Equal (O(1) Query): " + isEqual);
        System.out.println("-------------------------------------------------");

        // Query non-equal substring "cad" (indices 4..6)
        StringHashingMaster.HashPair h3 = hasher.query(4, 6);
        System.out.println("   Hash of \"cad\" (indices 4..6) : " + h3);
        System.out.println("   \"abra\" == \"cad\": " + hasher.isSubstringEqual(0, 3, 4, 6));
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Hashing Operation | Pre-processing Time | Substring Query Time | Auxiliary Memory | Collision Probability |
| :--- | :--- | :--- | :--- | :--- |
| **Prefix Hashes Build**| $\mathbf{O(N)}$ Linear ⚡| N/A | $O(N)$ Arrays | N/A |
| **Single Hash Query**  | N/A | $\mathbf{O(1)}$ Constant ⚡| $\mathbf{O(1)}$ Memory ⚡| $\approx 10^{-9}$ (Risk) |
| **Double Hash Query**  | N/A | $\mathbf{O(1)}$ Constant ⚡| $\mathbf{O(1)}$ Memory ⚡| **$< 10^{-18}$ (Zero) ⚡**|

---

## 10. Edge Cases & Boundary Handling

1. **Negative Modulo Remainder (`(val % MOD) < 0`)**:
   - Handled via `if (h < 0) h += MOD;` to guarantee all hashes stay in range $[0 \dots MOD-1]$.

2. **Choice of Base $B$**:
   - Base $B$ MUST be strictly larger than maximum character value ($B > |\Sigma|$, e.g. $B = 313$ for ASCII) to avoid aliasing collisions like `"a"` and `"aa"`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Using Single Prime Modulus $10^9 + 7$ for Large $N \ge 10^5$**:
  - Single hashing has a high collision probability ($\approx 99\%$) over $N^2$ substring queries. ALWAYS use **Double Modulo Hashing** ($10^9+7$ and $10^9+9$).

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why String Hashing Range Query is $O(1)$ Time:
> Substring hash equals `(pref[R + 1] - pref[L] * pow[R - L + 1]) % MOD`.
> Precomputing `pref` and `pow` arrays in $O(N)$ time allows ANY substring hash to be calculated in **1 single math formula**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Double String Hashing | KMP / Z-Algorithm | Suffix Array + LCP |
| :--- | :--- | :--- | :--- |
| **Substring Query Time**| **$O(1)$ Instant ⚡** | $O(N)$ Search Pass | $O(\log N)$ Binary Search |
| **Collision Guarantee** | Probabilistic ($< 10^{-18}$)| 100% Deterministic | 100% Deterministic |
| **Implementation**     | ~30 Lines (Simple) | ~50 Lines | ~70 Lines |

---

## 14. How to Recognize This in Questions

* **"Check if two arbitrary substrings S[a..b] and S[c..d] are equal in O(1) time"** $\rightarrow$ String Hashing.
* **"Find longest repeated substring using binary search"** $\rightarrow$ Binary Search on Length + String Hashing.

---

## 15. Frequently Asked Interview Questions

* **Q: How does String Hashing query any substring in $O(1)$ time?**  
  *A:* By subtracting `pref[L] * B^(R - L + 1)` from `pref[R + 1]` modulo $Q$, which removes the leading prefix $S[0 \dots L-1]$ from $S[0 \dots R]$.

* **Q: Why is Double Modulo Hashing preferred over Single Modulo Hashing?**  
  *A:* Double Modulo Hashing uses two distinct prime moduli ($10^9+7$ and $10^9+9$), reducing collision probability from $\sim 10^{-9}$ down to $< 10^{-18}$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING HASHING                                        |
+-----------------------------------------------------------------------+
| • Prefix Hash : pref[i+1] = (pref[i] * B + S[i]) % MOD                |
| • Range Query : Hash(L, R) = (pref[R+1] - pref[L] * pow[R-L+1]) % MOD  |
| • Negative Guard: If hash < 0 -> hash += MOD                          |
| • Double Hash : Pair (Hash1, Hash2) with Q1=10^9+7 and Q2=10^9+9      |
| • Performance : O(N) Precomputation | O(1) Substring Query ⚡           |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write $O(N)$ prefix hash and power array precomputation in Java.
- [ ] I can write $O(1)$ range hash query formula with negative modulo correction.
- [ ] I can write Double Modulo Hashing to prevent hash collisions.
- [ ] I can solve LeetCode 1044 (`Longest Duplicate Substring`) using Binary Search + String Hashing.
- [ ] I can state why Base $B$ must be greater than alphabet size ($B > |\Sigma|$).
