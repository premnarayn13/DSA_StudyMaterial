# 10. Manacher's Algorithm: Palindromic Radii, Mirror Invariants & Linear Bounds

## 1. Introduction
**Manacher's Algorithm** is an optimal linear-time string-processing algorithm invented by Glenn Glenn Manacher in 1975. While standard expand-around-center algorithms require $O(N^2)$ quadratic time to find the **Longest Palindromic Substring**, Manacher's Algorithm computes the palindromic radius of every center in **$O(N)$ Strict Linear Time Complexity** and **$O(N)$ Auxiliary Space**. By transforming the input string using delimiter sentinels (`"aba"` $\to$ `"^#a#b#a#$"`) to unify odd-length and even-length palindromes, Manacher's Algorithm maintains a **Current Palindrome Center $C$** and **Right Boundary $R$**, reusing previously computed palindrome radii of mirror indices ($i' = 2C - i$) to eliminate redundant character comparisons.

> **Important:** Core Invariants of Manacher's Algorithm:
> 1. **Sentinel String Transformation ($T$)**:
>    - Transforms original string $S$ of length $N$ into $T$ of length $2N + 3$ by inserting `#` between characters and surrounding with start/end sentinels `^` and `$`:
>      $$S = \text{"babad"} \implies T = \text{"^#b#a#b#a#d#\$"}$$
>    - Converts all odd and even palindromes into unified odd-length palindromes centered at characters or `#` delimiters!
> 2. **Palindrome Radius Array ($P[i]$)**:
>    - $P[i]$ stores the radius (half-length) of the longest palindrome centered at $T[i]$.
> 3. **Center $C$ & Right Boundary $R$ Mirror Invariant**:
>    - $[C - P[C] \dots C + P[C]]$ is the rightmost palindrome encountered so far, with right boundary $R = C + P[C]$.
>    - For index $i < R$, its mirror position relative to center $C$ is $i' = 2C - i$.
>    - **Mirror Radius Re-use Rule**:
>      $$P[i] = \min(R - i, P[2C - i])$$
> 4. **Linear Time Complexity**: Character comparisons occur ONLY when expanding beyond right boundary $R$. Since $R$ increases strictly monotonically from $0$ to $2N + 3$, total comparisons $\le 2N$, running in **$O(N)$ Strict Linear Time**. ⚡

```
Manacher's Sentinel Transformation & Radius Topology (S = "aba"):
Transformed T:  ^  #  a  #  b  #  a  #  $
Index i      :  0  1  2  3  4  5  6  7  8
Radius P[i]  :  0  0  1  0  3  0  1  0  0

Center C = 4 ('b'), Right Boundary R = 7 (4 + 3).
Max Radius = 3 at index 4 -> Longest Palindromic Substring = "aba" (Length 3)! ⚡
```

---

## 2. Core Concepts & Palindrome Search Strategy Matrix

### 2.1 Palindrome Search Strategy Matrix
```
Palindrome Search Comparison Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm / Pattern   | Centering Strategy| Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **Expand Center**     | 2N - 1 Centers    | $O(N^2)$ Quadratic| **$O(1)$ In-Place ⚡**|
| **Dynamic Programming**| Table $DP[i][j]$  | $O(N^2)$ Quadratic| $O(N^2)$ Table    |
| **Manacher's Engine** | Mirror Radius Re-use| **$O(N)$ Strict Linear ⚡**| **$O(N)$ Radius Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Manacher's transforms string with # sentinels! Reuses mirror P[i'] = min(R - i, P[2C - i]) in O(N) linear time!"**

---

## 3. Characteristics & $O(N)$ Linear Time Mathematical Proof

### 3.1 Mathematical Proof of $O(N)$ Linear Time Complexity
* Let $T$ be the transformed sentinel string of length $M = 2N + 3$.
* The algorithm maintains palindrome center $C$ and rightmost boundary $R = C + P[C]$.
* For each index $i \in [1 \dots M-2]$:
  - If $i < R$, initial radius $P[i]$ is set to $\min(R - i, P[2C - i])$ in $O(1)$ time without comparisons.
  - Character expansion loop `while (T[i + 1 + P[i]] == T[i - 1 - P[i]])` executes ONLY when $i + 1 + P[i] > R$.
* Each successful character comparison in the `while` loop INCREASES right boundary $R$ by at least 1 position.
* Since $R$ starts at $0$ and increases to at most $M$, total successful comparisons across all loop iterations $\le M$.
* Unsuccessful comparisons happen at most 1 time per index $i$ ($M$ times total).
* Total Comparisons: $\text{Successful} (\le M) + \text{Unsuccessful} (\le M) = \mathbf{O(M) = O(N) \text{ Strict Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Mirror Property $i' = 2C - i$

How does mirror position $i' = 2C - i$ reuse previously computed values?

```
Tracing Mirror Property for T = "^#b#a#b#a#d#$":

Center C = 4 ('b'), Right Boundary R = 7 (Radius P[4] = 3).
Segment covered: T[1...7] "#b#a#b#" is palindromic!

Now processing index i = 6 (character 'a'):
- i is inside box! (i < R -> 6 < 7).
- Calculate Mirror Index i':
  i' = 2 * C - i = 2 * 4 - 6 = 2!

- Look up P[i'] = P[2] = 1 (Radius at mirror index 2).
- Calculate remaining distance to right boundary: R - i = 7 - 6 = 1.
- Initialized Radius: P[6] = min(R - i, P[i']) = min(1, 1) = 1!

- Try expanding beyond R: T[6 + 1 + 1] vs T[6 - 1 - 1] -> '#' vs 'b' -> Mismatch!
- Final P[6] = 1 computed in 0 CHARACTER COMPARISONS! ✅
```

---

## 5. Visual Diagram: Manacher's Center & Mirror Symmetry

```
Palindromic Boundary Box [ C - P[C] ......... C ......... C + P[C] (R) ]:

Symmetric Mirror Pairs:
            [ Mirror i' ] <────── Center C ──────> [ Current i ]

Mirror Index Equation: i' = C - (i - C) = 2C - i

Since left side is mirror symmetric to right side around C:
Palindrome centered at i MUST match palindrome centered at i' up to boundary R! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Manacher's Algorithm, Sentinel String Transformation, Longest Palindromic Substring extraction, and Palindrome Query Engines.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Manacher's Algorithm,
 * Palindromic Radii Re-use, and O(N) Linear Substring Extraction.
 */
public class ManachersMaster {

    // =========================================================================
    // 1. MANACHER'S ALGORITHM (O(N) Strict Linear Time, O(N) Space)
    // =========================================================================
    /**
     * Finds the Longest Palindromic Substring in O(N) strict linear time.
     * LeetCode 5 Solution.
     *
     * @param s input string
     * @return longest palindromic substring
     */
    public String longestPalindrome(String s) {
        if (s == null || s.length() <= 1) return s;

        // Step 1: Transform string with sentinels ^, #, and $
        char[] t = transformString(s);
        int m = t.length;
        int[] p = new int[m]; // Palindrome Radius Array

        int c = 0; // Current palindrome center
        int r = 0; // Current right boundary

        int maxLen = 0;
        int centerIndex = 0;

        // Step 2: Loop through transformed string
        for (int i = 1; i < m - 1; i++) {
            int iMirror = 2 * c - i; // Mirror index of i relative to center C

            if (i < r) {
                p[i] = Math.min(r - i, p[iMirror]); // Mirror Re-use Rule! ⚡
            } else {
                p[i] = 0;
            }

            // Expand palindrome centered at i
            while (t[i + 1 + p[i]] == t[i - 1 - p[i]]) {
                p[i]++;
            }

            // Update center C and right boundary R if palindrome expanded past R
            if (i + p[i] > r) {
                c = i;
                r = i + p[i];
            }

            // Track maximum palindrome radius found
            if (p[i] > maxLen) {
                maxLen = p[i];
                centerIndex = i;
            }
        }

        // Step 3: Map back to original string substring indices
        int start = (centerIndex - maxLen) / 2;
        return s.substring(start, start + maxLen);
    }

    /**
     * Transforms string S into "^#c1#c2#...#cn#$" format.
     */
    private char[] transformString(String s) {
        int n = s.length();
        char[] t = new char[2 * n + 3];
        t[0] = '^';
        t[1] = '#';
        int idx = 2;

        for (int i = 0; i < n; i++) {
            t[idx++] = s.charAt(i);
            t[idx++] = '#';
        }

        t[idx] = '$';
        return t;
    }

    // =========================================================================
    // 2. ALL PALINDROMIC SUBSTRINGS COUNT (O(N) Time via Radius Array)
    // =========================================================================
    /**
     * Counts total number of palindromic substrings in string S in O(N) time.
     * LeetCode 647 Solution.
     */
    public int countSubstrings(String s) {
        if (s == null || s.length() == 0) return 0;

        char[] t = transformString(s);
        int m = t.length;
        int[] p = new int[m];

        int c = 0, r = 0;
        int totalPalindromes = 0;

        for (int i = 1; i < m - 1; i++) {
            int iMirror = 2 * c - i;

            if (i < r) {
                p[i] = Math.min(r - i, p[iMirror]);
            }

            while (t[i + 1 + p[i]] == t[i - 1 - p[i]]) {
                p[i]++;
            }

            if (i + p[i] > r) {
                c = i;
                r = i + p[i];
            }

            // Add number of palindromes centered at i: (P[i] + 1) / 2
            totalPalindromes += (p[i] + 1) / 2;
        }

        return totalPalindromes;
    }
}
```

> **Quick Syntax:**
```java
// Manacher Mirror Re-use Line
int iMirror = 2 * c - i; if (i < r) p[i] = Math.min(r - i, p[iMirror]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 5 - Longest Palindromic Substring**:
   - Primary Manacher's Algorithm benchmark ($O(N)$ strict linear time).

2. **LeetCode 647 - Palindromic Substrings**:
   - Count all palindromic substrings in $O(N)$ time by summing $(P[i] + 1) / 2$.

3. **DNA Genome Palindromic Hairpin Structure Analysis**:
   - Locating reverse-complement palindromic sequences in DNA strands in linear time.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class ManachersDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   MANACHER'S LINEAR PALINDROME ALGORITHM DEMO   ");
        System.out.println("=================================================\n");

        ManachersMaster master = new ManachersMaster();

        // 1. Longest Palindromic Substring Test (LeetCode 5)
        String s1 = "babad";
        String longest1 = master.longestPalindrome(s1);
        System.out.println("1. Input String: \"" + s1 + "\"");
        System.out.println("   Longest Palindromic Substring: \"" + longest1 + "\" (O(N) Time)");
        System.out.println("-------------------------------------------------");

        String s2 = "cbbd";
        String longest2 = master.longestPalindrome(s2);
        System.out.println("2. Input String: \"" + s2 + "\"");
        System.out.println("   Longest Palindromic Substring: \"" + longest2 + "\" (Even Palindrome)");
        System.out.println("-------------------------------------------------");

        // 3. Count Palindromic Substrings Test (LeetCode 647)
        String s3 = "aaa";
        int count = master.countSubstrings(s3);
        System.out.println("3. Input String: \"" + s3 + "\"");
        System.out.println("   Total Palindromic Substrings: " + count + " Palindromes");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Palindrome Algorithm | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Expand Around Center**| $O(N)$ Linear | $O(N^2)$ Quadratic | $O(N^2)$ Quadratic | $\mathbf{O(1)}$ In-Place ⚡| 2N - 1 Center Scans |
| **Dynamic Programming** | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ | $O(N^2)$ DP Table | Table $DP[i][j]$ |
| **Manacher's Engine**   | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Transformed| Mirror Re-use $P[i']$ |

---

## 10. Edge Cases & Boundary Handling

1. **Entire String is Palindrome (`"racecar"`)**:
   - Center at middle `'e'` expands radius across full string. Handled cleanly in $O(N)$ time.

2. **Single Character String (`"a"`)**:
   - `longestPalindrome` returns `"a"` immediately.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Forgetting Start/End Sentinels `^` and `$`**:
  - Omitting start/end sentinels requires array bound checking inside the `while` expansion loop, adding unnecessary conditional checks. Sentinels terminate expansion automatically!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Manacher's Beats Expand Around Center:
> Expand Around Center re-checks characters from scratch at every center ($O(N^2)$ time).
> Manacher's uses **Mirror Symmetry $i' = 2C - i$** to skip re-checking characters inside the right boundary $R$, running in **Strict $O(N)$ Linear Time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Manacher's Algorithm | Dynamic Programming | Expand Around Center |
| :--- | :--- | :--- | :--- |
| **Time Complexity** | **$O(N)$ Strict Linear ⚡**| $O(N^2)$ Quadratic | $O(N^2)$ Quadratic |
| **Space Complexity**| $O(N)$ Radius Array | $O(N^2)$ Table | **$O(1)$ Constant Space ⚡**|
| **Even/Odd Support** | Unified via `#` | Unified via Indices | Separate Odd/Even loops |

---

## 14. How to Recognize This in Questions

* **"Find longest palindromic substring in strict O(N) linear time"** $\rightarrow$ Manacher's Algorithm.
* **"Count total palindromic substrings in string S in O(N) time"** $\rightarrow$ Manacher's Radius Sum.

---

## 15. Frequently Asked Interview Questions

* **Q: Why does Manacher's Algorithm insert `#` between characters?**  
  *A:* To convert even-length palindromes (e.g. `"abba"` $\to$ `"#a#b#b#a#"`) into odd-length palindromes, unifying odd and even palindrome processing under a single loop.

* **Q: How does $P[i']$ compute the initial radius at index $i$?**  
  *A:* Since $i$ lies within right boundary $R$ of center $C$, the palindrome centered at $i$ is symmetric to the palindrome centered at mirror index $i' = 2C - i$, allowing initial radius $P[i] = \min(R - i, P[i'])$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: MANACHER'S ALGORITHM                                  |
+-----------------------------------------------------------------------+
| • Sentinel String : Transformed into "^#c1#c2#...#cn#$" (Length 2N+3) |
| • Mirror Index    : iMirror = 2 * C - i                               |
| • Initial Radius  : If i < R -> P[i] = min(R - i, P[iMirror])         |
| • Expand Loop     : while (T[i + 1 + P[i]] == T[i - 1 - P[i]]) P[i]++ |
| • Performance     : Strict O(N) Linear Time | O(N) Auxiliary Space ⚡ |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write string sentinel transformation (`"^#c1#c2#...#cn#$"`) in Java.
- [ ] I can calculate mirror index $i' = 2C - i$.
- [ ] I can write Manacher's $O(N)$ linear-time longest palindromic substring algorithm.
- [ ] I can count all palindromic substrings in $O(N)$ time using Manacher's radius array.
- [ ] I can prove why Manacher's algorithm runs in strict $O(N)$ linear time.
