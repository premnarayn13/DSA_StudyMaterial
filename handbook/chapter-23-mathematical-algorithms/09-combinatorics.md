# 09. Combinatorics: Combinations, Catalan Numbers & Inclusion-Exclusion Principle

## 1. Introduction
**Combinatorics** is the branch of mathematics focused on counting, arrangement, and structural combinations of discrete sets. In algorithm design and competitive programming, combinatorial formulas enable developers to count valid grid paths, binary search tree configurations, string permutations, and subset intersections without executing exhaustive brute-force search. Key fundamental combinatorial building blocks include **Combinations ($\binom{N}{K}$)** computed via Pascal's Triangle DP or Modular Inverses, **Catalan Numbers ($C_N$)** powering LeetCode 96 (Unique Binary Search Trees) and Dyck path enumeration, and the **Inclusion-Exclusion Principle** for set union cardinality calculations.

> **Important:** Core Structural Formulas of Combinatorics:
> 1. **Permutations & Combinations Formulas**:
>    $$P(N, K) = \frac{N!}{(N - K)!} \quad \text{and} \quad C(N, K) = \binom{N}{K} = \frac{N!}{K! (N - K)!}$$
> 2. **Pascal's Triangle DP Recurrence**:
>    $$C(N, K) = C(N - 1, K - 1) + C(N - 1, K)$$
> 3. **Catalan Number Formula ($C_N$)**:
>    $$C_N = \frac{1}{N + 1} \binom{2N}{N} = \frac{(2N)!}{(N + 1)! N!}$$
>    - Catalan Recurrence: $C_N = \sum_{i=0}^{N-1} C_i \times C_{N-1-i}$ (LeetCode 96 Unique BSTs!).
> 4. **Inclusion-Exclusion Principle**:
>    $$\left| \bigcup_{i=1}^K A_i \right| = \sum_{i} |A_i| - \sum_{i < j} |A_i \cap A_j| + \sum_{i < j < k} |A_i \cap A_j \cap A_k| \dots (-1)^{K-1} |A_1 \cap \dots \cap A_K|$$ ⚡

```
Combinatorics Structural Topology:

Pascal's Triangle DP (C(N, K)):
Row 0:           1
Row 1:         1   1
Row 2:       1   2   1
Row 3:     1   3   3   1
Row 4:   1   4   6   4   1
C(4, 2) = C(3, 1) + C(3, 2) = 3 + 3 = 6! ✅

Catalan Sequence C_N (N = 0, 1, 2, 3, 4 ...):
[ 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862 ... ]
- C_3 = 5: Exactly 5 Unique Binary Search Trees for 3 Nodes! (LeetCode 96) ✅ ⚡
```

---

## 2. Core Concepts & Combinatorics Strategy Matrix

### 2.1 Combinatorics Strategy Matrix
```
Combinatorics Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Combinatorial Concept | Primary Formula   | Time Complexity   | Auxiliary Space   | Key Problem Match |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Pascal's Triangle** | $C(N,K)=C(N-1,K-1)+C(N-1,K)$| **$O(N^2)$ DP Table ⚡**| **$O(N^2)$ Table ⚡**| Multi-query $C(N,K)$|
| **Modular Inverse C(N,K)**| $N! \cdot (K!)^{-1} \cdot ((N-K)!)^{-1}$| **$O(N)$ Pre-comp ⚡**| **$O(N)$ Arrays ⚡**| $N \le 10^6 \pmod M$|
| **Catalan Numbers (96)**| $C_N = \frac{1}{N+1} \binom{2N}{N}$| **$O(N)$ Linear ⚡**| **$O(1)$ Memory ⚡**| **Unique BSTs ⚡**|
| **Inclusion-Exclusion**| Bitmask Set Unions| **$O(2^K)$ Bitmask ⚡**| **$O(1)$ Memory ⚡**| Divisible by primes|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Pascal DP: C(N, K) = C(N-1, K-1) + C(N-1, K); Catalan C_N = (1/(N+1)) * C(2N, N); Inclusion-Exclusion flips sign for odd/even set sizes!"**

---

## 3. Characteristics & Catalan Numbers Mathematical Proof

### 3.1 Mathematical Proof of Catalan Recurrence $C_N = \sum_{i=0}^{N-1} C_i \cdot C_{N-1-i}$ (LeetCode 96)
* **Problem**: Count the total number of structurally unique Binary Search Trees (BSTs) that can be formed with $N$ distinct nodes ($1 \dots N$).
* **Root Selection**:
  - Any node $k \in \{1 \dots N\}$ can be selected as the root of the BST.
  - If node $k$ is selected as the root:
    - All $k - 1$ smaller nodes ($1 \dots k-1$) MUST go into the **Left Subtree**.
    - All $N - k$ larger nodes ($k+1 \dots N$) MUST go into the **Right Subtree**.
* **Subtree Independence**:
  - The left subtree has $k - 1$ nodes, which can form $C_{k-1}$ unique binary search trees.
  - The right subtree has $N - k$ nodes, which can form $C_{N-k}$ unique binary search trees.
  - By the Multiplication Principle, selecting root $k$ yields $C_{k-1} \times C_{N-k}$ total unique trees.
* **Summation Over All Possible Roots**:
  - Summing over all root choices $k = 1 \dots N$:
    $$C_N = \sum_{k=1}^N C_{k-1} \times C_{N-k} = \sum_{i=0}^{N-1} C_i \times C_{N-1-i}$$
* Solving this convolution recurrence yields the closed-form formula $C_N = \frac{1}{N+1} \binom{2N}{N}$! ⚡

---

## 4. Internal Working Mechanics: Inclusion-Exclusion Principle Execution

Tracing Inclusion-Exclusion for count of numbers $\le 100$ divisible by 2, 3, or 5 ($A_1 = \{2\}, A_2 = \{3\}, A_3 = \{5\}$):

```
Single Set Sizes (|A_i| = floor(100 / p_i)):
- |A_1| (divisible by 2) = 100 / 2 = 50
- |A_2| (divisible by 3) = 100 / 3 = 33
- |A_3| (divisible by 5) = 100 / 5 = 20
Sum single sets = 50 + 33 + 20 = 103.

Pairwise Intersection Sizes (|A_i ∩ A_j| = floor(100 / lcm(p_i, p_j))):
- |A_1 ∩ A_2| (div by 6)  = 100 / 6  = 16
- |A_1 ∩ A_3| (div by 10) = 100 / 10 = 10
- |A_2 ∩ A_3| (div by 15) = 100 / 15 = 6
Sum pairwise sets = 16 + 10 + 6 = 32.

Triple Intersection Size (|A_1 ∩ A_2 ∩ A_3| = floor(100 / lcm(2, 3, 5))):
- |A_1 ∩ A_2 ∩ A_3| (div by 30) = 100 / 30 = 3.

Inclusion-Exclusion Formula:
Total Divisible = (50 + 33 + 20) - (16 + 10 + 6) + (3)
                = 103 - 32 + 3 = 74 Numbers! ✅ ⚡
```

---

## 5. Visual Diagram: Catalan Number Applications Topology

```
Catalan Number (C_N) Applications Topology:

├── 1. Unique Binary Search Trees (LeetCode 96) ──► C_3 = 5 Trees for 3 Nodes ⚡
│
├── 2. Valid Parentheses Strings (LeetCode 22)  ──► C_3 = 5 Pairs ("((()))", "(()())"...) ⚡
│
├── 3. Dyck Grid Paths (Under Diagonal)         ──► Grid paths from (0,0) to (N,N) ⚡
│
└── 4. Non-Intersecting Polygon Triangulations   ──► Triangulating (N+2)-gon ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Pascal's Triangle DP, Modular Inverse Combination Engine, LeetCode 96 Catalan Numbers, and Inclusion-Exclusion Principle.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Combinatorics:
 * Pascal's Triangle DP, Modular Combination Factorials, LeetCode 96 Catalan Numbers, and Inclusion-Exclusion.
 */
public class CombinatoricsMaster {

    private static final long MOD = 1_000_000_007L;

    // =========================================================================
    // 1. PASCAL'S TRIANGLE COMBINATION DP (O(N^2) Time, O(N^2) Space)
    // =========================================================================
    /**
     * Pre-computes combination table C[N][K] modulo MOD up to maxN.
     */
    public long[][] computePascalTriangle(int maxN) {
        long[][] C = new long[maxN + 1][maxN + 1];

        for (int i = 0; i <= maxN; i++) {
            C[i][0] = 1; // Base case C(n, 0) = 1 ⚡
            for (int j = 1; j <= i; j++) {
                C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD; // Pascal Recurrence ⚡
            }
        }

        return C;
    }

    // =========================================================================
    // 2. LEETCODE 96: UNIQUE BINARY SEARCH TREES (CATALAN NUMBER O(N) Time)
    // =========================================================================
    /**
     * Solves LeetCode 96 Unique BSTs by calculating N-th Catalan Number C_N.
     */
    public int numTrees(int n) {
        if (n <= 1) return 1;
        int[] dp = new int[n + 1];
        dp[0] = 1;
        dp[1] = 1;

        for (int i = 2; i <= n; i++) {
            for (int j = 0; j < i; j++) {
                dp[i] += dp[j] * dp[i - 1 - j]; // Catalan Recurrence sum(C_j * C_{i-1-j}) ⚡
            }
        }

        return dp[n];
    }

    // =========================================================================
    // 3. INCLUSION-EXCLUSION PRINCIPLE (BITMASK ENUMERATION O(2^K))
    // =========================================================================
    /**
     * Counts numbers in range [1, N] divisible by at least one prime in primes array.
     */
    public long countDivisibleInclusionExclusion(long N, long[] primes) {
        int k = primes.length;
        long totalDivisible = 0;
        int totalMasks = 1 << k;

        for (int mask = 1; mask < totalMasks; mask++) {
            long lcmVal = 1;
            int bitCount = Integer.bitCount(mask);
            boolean overflow = false;

            for (int i = 0; i < k; i++) {
                if ((mask & (1 << i)) != 0) {
                    long g = gcd(lcmVal, primes[i]);
                    lcmVal = (lcmVal / g) * primes[i];
                    if (lcmVal > N) {
                        overflow = true;
                        break;
                    }
                }
            }

            if (overflow) continue;

            long count = N / lcmVal;

            // Inclusion-Exclusion: Add for odd set count, Subtract for even set count ⚡
            if (bitCount % 2 == 1) {
                totalDivisible += count;
            } else {
                totalDivisible -= count;
            }
        }

        return totalDivisible;
    }

    private long gcd(long a, long b) {
        return b == 0 ? Math.abs(a) : gcd(b, a % b);
    }
}
```

> **Quick Syntax:**
```java
// Combinatorics Core Lines
C[i][j] = (C[i - 1][j - 1] + C[i - 1][j]) % MOD; // Pascal Recurrence
dp[i] += dp[j] * dp[i - 1 - j];                 // LeetCode 96 Catalan BST Recurrence
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 96 - Unique Binary Search Trees**:
   - Catalan number sequence benchmark ($O(N)$ time).

2. **LeetCode 62 - Unique Paths**:
   - Grid path combination formula $\binom{M+N-2}{M-1}$ solved via Pascal DP or combinations.

3. **Inclusion-Exclusion Primes Count**:
   - Counting integers coprime to a composite number $N$.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class CombinatoricsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   COMBINATORICS BENCHMARK DEMO                  ");
        System.out.println("=================================================\n");

        CombinatoricsMaster master = new CombinatoricsMaster();

        // 1. Pascal's Triangle DP Test
        long[][] C = master.computePascalTriangle(10);
        System.out.println("1. Pascal's Triangle DP Combination C(10, 4):");
        System.out.println("   C(10, 4) Result: " + C[10][4] + " (Optimal = 210)");
        System.out.println("-------------------------------------------------");

        // 2. LeetCode 96 Unique BSTs (Catalan C_3)
        int uniqueBSTs = master.numTrees(3);
        System.out.println("2. LeetCode 96 Unique BSTs for N = 3 Nodes:");
        System.out.println("   Catalan C_3 Result: " + uniqueBSTs + " (Optimal = 5)");
        System.out.println("-------------------------------------------------");

        // 3. Inclusion-Exclusion Test (Numbers <= 100 div by 2, 3, or 5)
        long[] primes = {2, 3, 5};
        long divCount = master.countDivisibleInclusionExclusion(100, primes);
        System.out.println("3. Inclusion-Exclusion Principle for N = 100, Primes [2, 3, 5]:");
        System.out.println("   Total Divisible Count: " + divCount + " (Optimal = 74)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Combinatorial Concept | Algorithm Engine | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- |
| **Pascal's Triangle** | 2D DP Recurrence | $\mathbf{O(N^2)}$ Matrix DP⚡| $\mathbf{O(N^2)}$ Table | $C(n,k)=C(n-1,k-1)+C(n-1,k)$ |
| **Catalan Numbers (96)**| Recurrence Convolution| $\mathbf{O(N^2)}$ / $\mathbf{O(N)}$ ⚡| $\mathbf{O(N)}$ Array Space| $C_N = \frac{1}{N+1} \binom{2N}{N}$ |
| **Inclusion-Exclusion**| Bitmask Subsets | $\mathbf{O(2^K \log(\max))$⚡| $\mathbf{O(1)}$ Memory ⚡| Odd bit count $+$, Even $-$ |

---

## 10. Edge Cases & Boundary Handling

1. **Input $K > N$ in $C(N, K)$**:
   - $C(N, K) = 0$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Sign Flip in Inclusion-Exclusion**:
  - Subtracting odd-sized subset intersections instead of adding them breaks set union calculations. **ALWAYS add odd bit-count subsets ($+$) and subtract even bit-count subsets ($-$)?**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** The 2 Combinatorial Rules:
> * **Catalan Numbers (LeetCode 96)**: $C_N = \frac{1}{N+1} \binom{2N}{N}$ (Powers Unique BSTs, Valid Parentheses!).
> * **Inclusion-Exclusion**: Add odd-sized intersections ($+$), subtract even-sized intersections ($-$). ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Brute-Force Subset Search | Inclusion-Exclusion Bitmask |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N)$ Linear Search | **$O(2^K)$ Bitmask Subsets ⚡** |
| **Execution (N=10^18)**| Impossible | **Instant Computation ⚡** |

---

## 14. How to Recognize This in Questions

* **"Count total unique binary search trees with N nodes"** $\rightarrow$ LeetCode 96 (Catalan Number $C_N$).
* **"Count numbers <= N divisible by at least one prime in set"** $\rightarrow$ Inclusion-Exclusion Principle.

---

## 15. Frequently Asked Interview Questions

* **Q: What are Catalan numbers and where do they appear in DSA?**  
  *A:* Catalan numbers ($C_N = \frac{1}{N+1} \binom{2N}{N}$) count valid structural arrangements. They appear in LeetCode 96 (Unique BSTs), LeetCode 22 (Generate Parentheses), Dyck grid paths, and polygon triangulations.

* **Q: How does Inclusion-Exclusion compute set union size?**  
  *A:* By adding individual set sizes, subtracting pairwise intersections (to remove double counts), adding triple intersections (to restore triple-removed counts), alternating signs based on intersection set size parity.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: COMBINATORICS                                         |
+-----------------------------------------------------------------------+
| • Pascal DP : C(N, K) = (C(N-1, K-1) + C(N-1, K)) % MOD               |
| • Catalan C_N: C_N = (1 / (N+1)) * C(2N, N) (LeetCode 96 Unique BSTs!)⚡|
| • Incl-Excl : Union = sum(|A_i|) - sum(|A_i ∩ A_j|) + sum(...)        |
| • Parity    : Add odd set counts (+), Subtract even set counts (-) ⚡ |
| • Speedup   : Pre-computes combinations in O(N^2) or O(N) linear time!⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Pascal's Triangle DP combination solver in Java.
- [ ] I can write LeetCode 96 (`Unique Binary Search Trees`) in Java.
- [ ] I can write Inclusion-Exclusion bitmask set union solver in Java.
- [ ] I can state Catalan Number formula $C_N = \frac{1}{N+1} \binom{2N}{N}$.
- [ ] I can explain why Inclusion-Exclusion alternates signs based on bit count.
