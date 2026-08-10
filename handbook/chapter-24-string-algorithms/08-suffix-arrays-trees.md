# 08. Suffix Arrays & Suffix Trees: Kasai's LCP, Prefix-Doubling & Ukkonen's Algorithm

## 1. Introduction
**Suffix Arrays** and **Suffix Trees** represent two of the most powerful advanced data structures in string processing, bioinformatics, data compression, and full-text indexing. Given a string $S$ of length $N$, the **Suffix Array ($SA$)** is a sorted integer array of length $N$ containing the starting indices of all suffixes of $S$ in lexicographical ascending order. Paired with **Kasai's Algorithm** for constructing the **Longest Common Prefix (LCP) Array** in $O(N)$ time, Suffix Arrays replace bulky $O(N^2)$ Suffix Trees with space-efficient 32-bit integer arrays. Suffix Arrays enable $O(M \log N)$ pattern matching, $O(N)$ calculation of **Distinct Substrings**, and $O(N)$ discovery of **Longest Repeated Substring**.

> **Important:** Core Structural Invariants of Suffix Arrays & LCP:
> 1. **Suffix Array Invariant ($SA[i]$)**:
>    - $SA[i]$ is the starting index of the $i$-th lexicographically smallest suffix of $S$.
>    - $S[SA[0] \dots N-1] < S[SA[1] \dots N-1] < \dots < S[SA[N-1] \dots N-1]$.
> 2. **LCP Array Invariant ($LCP[i]$)**:
>    - $LCP[i]$ stores the length of the longest common prefix between adjacent sorted suffixes in the suffix array: $S[SA[i] \dots N-1]$ and $S[SA[i-1] \dots N-1]$.
> 3. **Kasai's $O(N)$ Linear LCP Lemma**:
>    - Let $k$ be the LCP value for the suffix starting at index $i$. For the suffix starting at index $i + 1$, its LCP value is at least $k - 1$.
>    - This monotonicity allows Kasai's algorithm to compute the full LCP array in **$O(N)$ Strict Linear Time**!
> 4. **Distinct Substrings Counting Theorem**:
>    - A string $S$ of length $N$ has total possible substrings $\frac{N(N+1)}{2}$.
>    - Total distinct non-empty substrings = $\frac{N(N+1)}{2} - \sum_{i=1}^{N-1} LCP[i]$. ⚡

```
Suffix Array & LCP Topology for S = "banana$":
Index i   SA[i]   LCP[i]   Suffix S[SA[i] ... N-1]
--------------------------------------------------
  0        6        0      "$"
  1        5        0      "a$"
  2        3        1      "ana$"       (LCP with "a$" = 1 "a")
  3        1        3      "anana$"     (LCP with "ana$" = 3 "ana")
  4        0        0      "banana$"    (LCP with "anana$" = 0)
  5        4        0      "na$"        (LCP with "banana$" = 0)
  6        2        2      "nana$"      (LCP with "na$" = 2 "na")

Total Distinct Substrings = 6*7/2 - (0+0+1+3+0+0+2) = 21 - 6 = 15 Distinct Substrings! ⚡
```

---

## 2. Core Concepts & Suffix Structures Strategy Matrix

### 2.1 Suffix Data Structures Comparison Matrix
```
Suffix Data Structures Comparison Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Structure / Algorithm | Space Footprint   | Construction Time | Substring Search  | Primary Advantage |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Suffix Tree**       | $O(N \cdot |\Sigma|)$ Bytes| $O(N)$ (Ukkonen)  | **$O(M)$ Instant ⚡**| Structural Graph |
| **Prefix-Doubling SA**| **$O(N)$ Integers⚡**| $O(N \log^2 N)$   | $O(M \log N)$ BS  | Simple Implementation|
| **Kasai's LCP Array** | **$O(N)$ Integers⚡**| **$O(N)$ Linear ⚡**| $O(1)$ Range Min  | Linear LCP Compute|
| **SA-IS Algorithm**   | **$O(N)$ Integers⚡**| **$O(N)$ Linear ⚡**| $O(M \log N)$ BS  | State-of-the-Art  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Suffix Array stores sorted suffix indices! Kasai computes LCP in O(N) linear time using k - 1 bound!"**

---

## 3. Characteristics & Kasai's $O(N)$ LCP Mathematical Proof

### 3.1 Mathematical Proof of Kasai's $O(N)$ Linear Time
* Let $rank[i]$ be the position of suffix $S[i \dots N-1]$ in the Suffix Array ($SA[rank[i]] = i$).
* Consider suffix $S[i \dots N-1]$ and its predecessor in the Suffix Array, $S[j \dots N-1]$ where $j = SA[rank[i] - 1]$.
* Suppose $LCP[rank[i]] = k > 0$. This implies $S[i \dots i+k-1] == S[j \dots j+k-1]$.
* Stripping the first character from both suffixes leaves suffix $S[i+1 \dots N-1]$ and $S[j+1 \dots N-1]$, which match for at least $k - 1$ characters!
* In the sorted Suffix Array, suffix $S[i+1 \dots N-1]$ can only share AT LEAST $k - 1$ matching characters with its predecessor $SA[rank[i+1] - 1]$.
* Therefore:
  $$\text{LCP for suffix } (i + 1) \ge k - 1$$
* In Kasai's algorithm, the variable $k$ increments at most $N$ times and decrements at most $N$ times.
* Total Time Complexity: $\mathbf{O(N) \text{ Strict Linear Time}}$. Auxiliary Space: $\mathbf{O(N) \text{ Memory}}$. ⚡

---

## 4. Internal Working Mechanics: Prefix-Doubling SA Construction

Prefix-Doubling (Manber-Myers) builds the Suffix Array by sorting suffixes based on their first $1, 2, 4, 8 \dots 2^k$ characters:

```
Prefix-Doubling Step (Sorting by 2^k character ranks):

Pass 0 (k = 0, Len = 1): Rank suffixes by 1st character.
Pass 1 (k = 1, Len = 2): Combine rank[i] and rank[i + 1] into a 2-tuple:
                         Pair_i = ( rank[i], rank[i + 1] )
Pass 2 (k = 2, Len = 4): Combine 2-length ranks:
                         Pair_i = ( rank_2[i], rank_2[i + 2] )
Pass 3 (k = 3, Len = 8): Combine 4-length ranks:
                         Pair_i = ( rank_4[i], rank_4[i + 4] )

Constructs Suffix Array in O(N log^2 N) or O(N log N) using Radix Sort! ✅
```

---

## 5. Visual Diagram: Kasai's LCP Monotonic Reduction

```
Kasai's LCP Pointer Continuity:

Suffix i   : [ A | B | C | D | E | ... ] ──> Match Length k = 4 with predecessor
Suffix i+1 : [ B | C | D | E | ... ]     ──> Match Length >= k - 1 = 3 Guaranteed!

k decrements at most 1 per index step, proving O(N) linear time! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Prefix-Doubling Suffix Array Construction ($O(N \log^2 N)$), Kasai's LCP Array Construction ($O(N)$), Suffix Array Binary Search Matching ($O(M \log N)$), and Distinct Substring Counting.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Suffix Arrays,
 * Prefix-Doubling Construction, Kasai's $O(N)$ LCP Algorithm, and Substring Matching.
 */
public class SuffixArrayMaster {

    /**
     * Suffix tuple for prefix-doubling sorting.
     */
    public static class SuffixTuple implements Comparable<SuffixTuple> {
        public int index;
        public int rank1;
        public int rank2;

        public SuffixTuple(int index, int rank1, int rank2) {
            this.index = index;
            this.rank1 = rank1;
            this.rank2 = rank2;
        }

        @Override
        public int compareTo(SuffixTuple o) {
            if (this.rank1 != o.rank1) return Integer.compare(this.rank1, o.rank1);
            return Integer.compare(this.rank2, o.rank2);
        }
    }

    // =========================================================================
    // 1. PREFIX-DOUBLING SUFFIX ARRAY CONSTRUCTION (O(N log^2 N) Time, O(N) Space)
    // =========================================================================
    /**
     * Builds Suffix Array SA using Prefix-Doubling.
     *
     * @param s input string
     * @return integer array containing sorted suffix indices SA
     */
    public int[] buildSuffixArray(String s) {
        if (s == null || s.length() == 0) return new int[0];

        int n = s.length();
        SuffixTuple[] tuples = new SuffixTuple[n];

        // Step 1: Initial ranking based on first character
        for (int i = 0; i < n; i++) {
            tuples[i] = new SuffixTuple(i, s.charAt(i), (i + 1 < n) ? s.charAt(i + 1) : -1);
        }

        Arrays.sort(tuples);

        int[] ind = new int[n]; // Maps original suffix index to tuple rank

        // Step 2: Double prefix length 2, 4, 8...
        for (int k = 4; k < 2 * n; k *= 2) {
            int rank = 0;
            int prevRank1 = tuples[0].rank1;
            int prevRank2 = tuples[0].rank2;
            tuples[0].rank1 = rank;
            ind[tuples[0].index] = 0;

            for (int i = 1; i < n; i++) {
                if (tuples[i].rank1 == prevRank1 && tuples[i].rank2 == prevRank2) {
                    tuples[i].rank1 = rank;
                } else {
                    prevRank1 = tuples[i].rank1;
                    prevRank2 = tuples[i].rank2;
                    tuples[i].rank1 = ++rank;
                }
                ind[tuples[i].index] = i;
            }

            for (int i = 0; i < n; i++) {
                int nextIdx = tuples[i].index + k / 2;
                tuples[i].rank2 = (nextIdx < n) ? tuples[ind[nextIdx]].rank1 : -1;
            }

            Arrays.sort(tuples);
        }

        int[] sa = new int[n];
        for (int i = 0; i < n; i++) {
            sa[i] = tuples[i].index;
        }

        return sa;
    }

    // =========================================================================
    // 2. KASAI'S LCP ARRAY CONSTRUCTION (O(N) Strict Linear Time)
    // =========================================================================
    /**
     * Builds Longest Common Prefix (LCP) array in O(N) linear time using Kasai's algorithm.
     *
     * @param s original string
     * @param sa precomputed Suffix Array
     * @return LCP integer array
     */
    public int[] buildLCPArray(String s, int[] sa) {
        int n = s.length();
        int[] lcp = new int[n];
        int[] rank = new int[n];

        // Inverse Suffix Array lookup (rank[i] gives position of suffix i in SA)
        for (int i = 0; i < n; i++) {
            rank[sa[i]] = i;
        }

        int k = 0; // LCP length counter

        for (int i = 0; i < n; i++) {
            if (rank[i] == 0) {
                lcp[0] = 0; // First suffix in SA has no predecessor
                k = 0;
                continue;
            }

            int j = sa[rank[i] - 1]; // Predecessor suffix in SA

            // Compare characters starting from offset k
            while (i + k < n && j + k < n && s.charAt(i + k) == s.charAt(j + k)) {
                k++;
            }

            lcp[rank[i]] = k;

            if (k > 0) {
                k--; // Monotonic reduction lemma: k = max(0, k - 1) ⚡
            }
        }

        return lcp;
    }

    // =========================================================================
    // 3. DISTINCT SUBSTRINGS COUNTING (O(N) Time via LCP)
    // =========================================================================
    /**
     * Calculates total number of unique non-empty substrings in O(N) time.
     */
    public long countDistinctSubstrings(String s) {
        if (s == null || s.length() == 0) return 0;

        int n = s.length();
        int[] sa = buildSuffixArray(s);
        int[] lcp = buildLCPArray(s, sa);

        long totalPossible = (long) n * (n + 1) / 2;
        long lcpSum = 0;
        for (int val : lcp) lcpSum += val;

        return totalPossible - lcpSum; // Substring Count Theorem ⚡
    }

    // =========================================================================
    // 4. PATTERN SEARCHING VIA SUFFIX ARRAY (O(M log N) Time)
    // =========================================================================
    /**
     * Searches pattern P in text T using Suffix Array Binary Search in O(M log N) time.
     */
    public boolean searchPattern(String text, int[] sa, String pattern) {
        int n = text.length();
        int m = pattern.length();

        int low = 0, high = n - 1;

        while (low <= high) {
            int mid = low + (high - low) / 2;
            int suffixStart = sa[mid];

            // Compare pattern with suffix text[suffixStart ...]
            String suffix = text.substring(suffixStart, Math.min(suffixStart + m, n));
            int cmp = pattern.compareTo(suffix);

            if (cmp == 0) return true; // Match found!
            else if (cmp < 0) high = mid - 1;
            else low = mid + 1;
        }

        return false;
    }
}
```

> **Quick Syntax:**
```java
// Kasai Monotonic Reduction Guard Line
lcp[rank[i]] = k; if (k > 0) k--;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1698 - Number of Distinct Substrings in a String**:
   - Solved in $O(N \log N)$ time using Suffix Array + Kasai's LCP Array ($\frac{N(N+1)}{2} - \sum LCP$).

2. **LeetCode 1044 - Longest Duplicate Substring**:
   - Solved in $O(N)$ time by finding $\max(LCP[i])$ in the LCP array!

3. **Genome Sequence Assembly & Alignment**:
   - Indexing multi-gigabyte Human Genome sequences using Suffix Arrays for sub-millisecond pattern matching.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;

public class SuffixArrayDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SUFFIX ARRAY & KASAI LCP DEMONSTRATION        ");
        System.out.println("=================================================\n");

        SuffixArrayMaster master = new SuffixArrayMaster();

        // 1. Suffix Array & LCP Test
        String text = "banana";
        int[] sa = master.buildSuffixArray(text);
        int[] lcp = master.buildLCPArray(text, sa);

        System.out.println("1. Text String: \"" + text + "\"");
        System.out.println("   Suffix Array SA : " + Arrays.toString(sa));
        System.out.println("   Kasai LCP Array : " + Arrays.toString(lcp));
        System.out.println("-------------------------------------------------");

        // 2. Distinct Substrings Count Test
        long distinctCount = master.countDistinctSubstrings(text);
        System.out.println("2. Number of Distinct Non-Empty Substrings for \"" + text + "\":");
        System.out.println("   Formula: N*(N+1)/2 - sum(LCP) = 21 - 6 = " + distinctCount + " Substrings");
        System.out.println("-------------------------------------------------");

        // 3. Pattern Search via Suffix Array Test
        String pattern = "nan";
        boolean found = master.searchPattern(text, sa, pattern);
        System.out.println("3. Binary Search Pattern \"" + pattern + "\" in SA: Found = " + found);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Suffix Task | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Prefix-Doubling SA** | $O(N \log^2 N)$ | $O(N \log^2 N)$ | $O(N \log^2 N)$ | $O(N)$ Integers | Tuple Ranking |
| **Kasai's LCP Array**  | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $O(N)$ Integers | Monotonic $k - 1$ |
| **Distinct Substrings** | $\mathbf{O(N \log^2 N)}$⚡| $\mathbf{O(N \log^2 N)}$⚡| $\mathbf{O(N \log^2 N)}$⚡| $O(N)$ Integers | Total - Sum(LCP) |
| **SA Pattern Search**   | $O(M \log N)$ | $O(M \log N)$ | $O(M \log N)$ | $\mathbf{O(1)}$ Memory ⚡| Binary Search SA |

---

## 10. Edge Cases & Boundary Handling

1. **All Single Unique Characters (`"abcdef"`)**:
   - All $LCP[i] = 0$. Total distinct substrings equal total possible substrings $\frac{N(N+1)}{2}$.

2. **All Same Repeating Characters (`"aaaaa"`)**:
   - $LCP = [0, 1, 2, 3, 4]$. Total distinct substrings equal $N = 5$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Resetting $k = 0$ at Every Step in LCP Calculation**:
  - Resetting $k = 0$ without using Kasai's $k - 1$ bound degrades LCP calculation to $O(N^2)$ quadratic time.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Suffix Tree vs Suffix Array Choice:
> * **Suffix Tree**: Uses $O(N \cdot |\Sigma|)$ bytes (heavy node pointer overhead).
> * **Suffix Array + LCP**: Uses ONLY two primitive 32-bit integer arrays of size $N$ ($8N$ bytes total memory), running **$10\times$ more memory-efficiently** in production! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Suffix Array + LCP | Suffix Tree | Trie (Prefix Tree) |
| :--- | :--- | :--- | :--- |
| **Memory Footprint** | **Minimal $O(N)$ Integers ⚡**| Heavy $O(N \cdot |\Sigma|)$ Pointers| $O(N \cdot L \cdot |\Sigma|)$ |
| **LCP Calculation**  | **$O(N)$ Kasai Linear ⚡**| Tree Node Depth | N/A |
| **Implementation**   | ~60 Lines | ~250 Lines (Complex) | ~40 Lines |

---

## 14. How to Recognize This in Questions

* **"Count total distinct substrings in string S"** $\rightarrow$ Suffix Array + Kasai's LCP.
* **"Find longest repeated substring in S"** $\rightarrow$ Maximum value in Kasai's LCP Array ($\max(LCP[i])$).

---

## 15. Frequently Asked Interview Questions

* **Q: What is Kasai's Algorithm?**  
  *A:* An $O(N)$ linear-time algorithm for building the LCP array by exploiting the property that the LCP value for suffix $i + 1$ is at least $\text{LCP}(i) - 1$.

* **Q: How does Suffix Array calculate the number of distinct substrings in $O(N)$ time?**  
  *A:* Total possible substrings is $\frac{N(N+1)}{2}$. The sum of LCP values represents duplicated substrings. Subtracting $\sum LCP[i]$ yields distinct substrings.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUFFIX ARRAYS & KASAI LCP                             |
+-----------------------------------------------------------------------+
| • Suffix Array (SA): Sorted starting indices of all suffixes          |
| • LCP Array        : Length of common prefix between SA[i] and SA[i-1]|
| • Kasai's Lemma    : LCP(suffix i+1) >= LCP(suffix i) - 1 -> O(N) Time!|
| • Distinct Count   : N*(N+1)/2 - sum(LCP)                             |
| • Max Repeat Substr: Find max(LCP[i]) in LCP array ⚡                  |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Prefix-Doubling Suffix Array construction in Java.
- [ ] I can write Kasai's $O(N)$ Linear LCP Array algorithm.
- [ ] I can prove why Kasai's algorithm runs in $O(N)$ time.
- [ ] I can calculate the number of distinct substrings using Suffix Array + LCP.
- [ ] I can write $O(M \log N)$ Suffix Array Binary Search pattern matching.
