# 06. Z-Algorithm: Z-Array, Z-Box Segment & Linear String Preprocessing

## 1. Introduction
The **Z-Algorithm** (Linear String Preprocessing) is a fundamental string-processing algorithm created by Dan Gusfield in 1997. Given a string $S$ of length $N$, the Z-Algorithm constructs a **Z-Array** of size $N$ where $Z[i]$ represents the length of the longest substring starting at $S[i]$ that is also a prefix of $S$. By maintaining a **Z-Box Segment $[L, R]$** (the rightmost substring matching a prefix of $S$), the Z-Algorithm reuses previously computed $Z$-values to compute new $Z$-array entries in **$O(N)$ Strict Linear Time** and **$O(N)$ Auxiliary Space**. Concatenating pattern $P$ and text $T$ into string $S = P + \text{'\$'} + T$ allows the Z-Algorithm to solve string matching problems in **$O(N + M)$ Time**.

> **Important:** Core Invariants of the Z-Algorithm:
> 1. **Z-Array Definition ($Z[i]$)**:
>    - $Z[i]$ is the maximum length $k$ such that substring $S[i \dots i + k - 1]$ equals prefix $S[0 \dots k - 1]$. By convention, $Z[0] = 0$.
> 2. **Z-Box Segment $[L, R]$ Invariant**:
>    - $[L, R]$ represents the interval $[L \dots R]$ with the maximum value of $R$ encountered so far such that $S[L \dots R]$ is a prefix of $S$.
> 3. **Z-Box Re-use Rules**:
>    - For index $i > R$: Compute $Z[i]$ naively via character comparisons, then update Z-Box $[L, R] = [i, i + Z[i] - 1]$.
>    - For index $i \le R$: Let $k = i - L$.
>      - If $Z[k] < R - i + 1 \implies Z[i] = Z[k]$ (No new character comparisons needed!).
>      - If $Z[k] \ge R - i + 1 \implies$ Set $L = i$ and extend $R$ rightward via character comparisons!
> 4. **Concatenated Pattern Search ($S = P + \text{'\$'} + T$)**:
>    - Indices $i$ where $Z[i] == M$ (pattern length $M$) correspond to exact pattern occurrences in text $T$! ⚡

```
Z-Array & Z-Box Topology for S = "a a b x a a b a a b c":
Indices: 0  1  2  3  4  5  6  7  8  9 10
Char S:  a  a  b  x  a  a  b  a  a  b  c
Z-Array: 0  1  0  0  3  1  0  4  1  0  0

At index 7: Substring S[7..10] "a a b c" matches Prefix "a a b a" up to length 4!
Z-Box becomes [L=7, R=10]. Linear Construction Completed! ⚡
```

---

## 2. Core Concepts & Z-Algorithm Strategy Matrix

### 2.1 Z-Algorithm Strategy Matrix
```
Z-Algorithm Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Input String S    | Target Invariant  | Time Complexity   |
+-----------------------+-------------------+-------------------+-------------------+
| **Z-Array Construction**| Original String $S$| $Z[i] = \text{Match Prefix}$| **$O(N)$ Linear ⚡**|
| **Pattern Search**    | $S = P + \text{'\$'} + T$| Find $Z[i] == M$| **$O(N + M)$ Strict ⚡**|
| **Longest Palindrome**| $S = P + \text{'\$'} + P^R$| Max $Z$-value match| **$O(N)$ Linear ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Z-Array stores prefix match lengths! Use Z-Box [L, R] to skip redundant character comparisons in O(N) linear time!"**

---

## 3. Characteristics & $O(N)$ Linear Time Proof

### 3.1 Mathematical Proof of $O(N)$ Linear Time Complexity
* In the Z-Algorithm, character comparisons occur ONLY when extending the right boundary $R$ of the Z-box $[L, R]$.
* At each step $i$:
  - If $i > R$, $R$ is initialized to $i$ and increases with every matching character comparison.
  - If $i \le R$ and $Z[k] \ge R - i + 1$, $R$ increases with every successful character comparison beyond $R$.
* Notice that $R$ NEVER decreases. $R$ starts at $0$ and increases at most $N$ times throughout the entire algorithm.
* Therefore, the total number of successful character comparisons across the entire loop is bounded by $N$.
* The number of unsuccessful character comparisons is at most 1 per index $i$ ($N$ total).
* Total Comparisons: $\text{Successful Comparisons} (\le N) + \text{Unsuccessful Comparisons} (\le N) = \mathbf{O(N) \text{ Strict Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: Tracing Z-Box $[L, R]$ Reuse

Tracing Z-Array Construction for $S = \text{"a a b x a a b a a b c"}$:

```
Init: Z = [0, 0, ...], L = 0, R = 0.

- i = 1 (S[1]='a'): Naive scan matches "a" -> Z[1] = 1. Z-Box [L=1, R=1].
- i = 2 (S[2]='b'): S[2] != S[0] -> Z[2] = 0.
- i = 3 (S[3]='x'): S[3] != S[0] -> Z[3] = 0.
- i = 4 (S[4]='a'): Naive scan matches "a a b" -> Z[4] = 3. Z-Box [L=4, R=6].

- i = 5 (S[5]='a'): Inside Z-Box [4, 6]! k = 5 - 4 = 1. Z[k=1] = 1.
  Since Z[1] (1) < R - i + 1 (6 - 5 + 1 = 2):
  Z[5] = Z[1] = 1 WITHOUT ANY CHARACTER COMPARISONS! ⚡

- i = 7 (S[7]='a'): i > R (7 > 6). Naive scan matches "a a b a" -> Z[7] = 4.
  Z-Box updated to [L=7, R=10]!

Z-Array fully constructed in O(N) Linear Time! ✅
```

---

## 5. Visual Diagram: Z-Box Segment Re-use Topology

```
Z-Box Interval [L ................. R]:
Substring S[L ... R] is GUARANTEED identical to Prefix S[0 ... R - L]!

Index i inside Z-Box:   [ L ...... i ...... R ]
Corresponding Prefix:   [ 0 ...... k ...... R - L ]  where k = i - L

If Z[k] fits inside remaining box (Z[k] < R - i + 1) ──> Copy Z[i] = Z[k] instantly! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Z-Array Construction and Pattern Matching using Concatenated String $S = P + \text{'\$'} + T$.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the Z-Algorithm,
 * Z-Box [L, R] Segment Optimization, and Pattern Matching.
 */
public class ZAlgorithmMaster {

    // =========================================================================
    // 1. Z-ARRAY CONSTRUCTION (O(N) Strict Linear Time, O(N) Space)
    // =========================================================================
    /**
     * Constructs the Z-Array for string S in O(N) linear time.
     * Z[i] stores the length of the longest substring starting at S[i] that equals prefix S.
     *
     * @param s input string
     * @return Z-Array
     */
    public int[] calculateZArray(String s) {
        if (s == null || s.length() == 0) return new int[0];

        int n = s.length();
        int[] z = new int[n];
        z[0] = 0; // By convention, Z[0] is 0

        int l = 0; // Left boundary of Z-Box
        int r = 0; // Right boundary of Z-Box

        for (int i = 1; i < n; i++) {
            if (i > r) {
                // Case 1: i is outside current Z-box -> Perform naive scan
                l = i;
                r = i;
                while (r < n && s.charAt(r - l) == s.charAt(r)) {
                    r++;
                }
                z[i] = r - l;
                r--; // Adjust r to last matching index
            } else {
                // Case 2: i is inside current Z-box [L, R]
                int k = i - l; // Corresponding position in prefix

                if (z[k] < r - i + 1) {
                    // Sub-case 2A: Z[k] is strictly within remaining box -> Copy directly!
                    z[i] = z[k];
                } else {
                    // Sub-case 2B: Z[k] extends beyond R -> Extend R rightward via comparisons
                    l = i;
                    while (r < n && s.charAt(r - l) == s.charAt(r)) {
                        r++;
                    }
                    z[i] = r - l;
                    r--;
                }
            }
        }

        return z;
    }

    // =========================================================================
    // 2. PATTERN MATCHING VIA CONCATENATED STRING S = P + '$' + T (O(N + M))
    // =========================================================================
    /**
     * Finds all starting indices of pattern P in text T using Z-Algorithm.
     */
    public List<Integer> searchPattern(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int m = pattern.length();
        int n = text.length();
        if (m == 0 || m > n) return matches;

        // Step 1: Form concatenated string S = P + '$' + T
        String concat = pattern + "$" + text;
        int concatLen = concat.length();

        // Step 2: Compute Z-Array for concatenated string
        int[] z = calculateZArray(concat);

        // Step 3: Check Z-values corresponding to text indices
        for (int i = m + 1; i < concatLen; i++) {
            if (z[i] == m) {
                // Match Found! Map index back to original text index
                int textIdx = i - (m + 1);
                matches.add(textIdx);
            }
        }

        return matches;
    }
}
```

> **Quick Syntax:**
```java
// Z-Box Re-use Condition Line
if (z[k] < r - i + 1) z[i] = z[k]; else { l = i; while (r < n && s.charAt(r-l) == s.charAt(r)) r++; z[i] = r - l; r--; }
```

---

## 7. Concrete Problem Examples & Applications

1. **Pattern Matching via $S = P + \text{'\$'} + T$**:
   - Equivalent to KMP algorithm ($O(N + M)$ time).

2. **Longest Palindromic Prefix (LeetCode 214 - Shortest Palindrome)**:
   - Construct $S = P + \text{'\$'} + P^R$. The Z-value gives the longest palindromic prefix in $O(N)$ time!

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class ZAlgorithmDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     Z-ALGORITHM LINEAR PREPROCESSING DEMO       ");
        System.out.println("=================================================\n");

        ZAlgorithmMaster master = new ZAlgorithmMaster();

        // 1. Z-Array Calculation Test
        String str = "aabxaab aabc";
        int[] z = master.calculateZArray(str);
        System.out.println("1. Input String: \"" + str + "\"");
        System.out.println("   Calculated Z-Array: " + Arrays.toString(z));
        System.out.println("-------------------------------------------------");

        // 2. Pattern Search Test
        String text = "baabaaab";
        String pattern = "aab";
        List<Integer> matches = master.searchPattern(text, pattern);
        System.out.println("2. Text   : \"" + text + "\"");
        System.out.println("   Pattern: \"" + pattern + "\"");
        System.out.println("   Z-Algorithm Matches Found at Indices: " + matches);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Z-Algorithm Task | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Z-Array Construction** | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Array ⚡| Z-Box $[L, R]$ Reuse |
| **Pattern Search Engine** | $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(N + M)}$ ⚡| $O(N + M)$ Array| Concatenated $S = P+\$+T$ |

---

## 10. Edge Cases & Boundary Handling

1. **Delimiter Character Choice ('$')**:
   - Delimiter char MUST be a character that does NOT appear in pattern $P$ or text $T$ to prevent Z-values from extending across the boundary!

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Re-starting Scan from $i$ Instead of $R$ in Sub-Case 2B**:
  - In sub-case 2B ($Z[k] \ge R - i + 1$), re-comparing characters from $i$ up to $R$ wastes time. **Start comparing from $R + 1$ rightward!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** KMP vs Z-Algorithm Comparison:
> * KMP builds **LPS Array** based on proper prefix-suffix matches of pattern $P$ ($O(M)$ space).
> * Z-Algorithm builds **Z-Array** over concatenated string $S = P + \text{'\$'} + T$ ($O(N + M)$ space).
> Both execute in **Strict $O(N + M)$ Linear Time**! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Z-Algorithm | KMP Algorithm | Naive Search |
| :--- | :--- | :--- | :--- |
| **Input Structure** | $S = P + \text{'\$'} + T$ | Precomputed LPS Table | Direct Text & Pattern |
| **Worst-Case Time** | **$O(N + M)$ Strict ⚡** | **$O(N + M)$ Strict ⚡** | $O(N \cdot M)$ Quadratic |
| **Auxiliary Memory** | $O(N + M)$ Array | **$O(M)$ Table ⚡**| **$O(1)$ Constant Space ⚡**|

---

## 14. How to Recognize This in Questions

* **"Compute length of longest substring starting at each index that matches prefix"** $\rightarrow$ Z-Algorithm.
* **"Find longest palindromic prefix in string"** $\rightarrow$ Z-Algorithm on $S = P + \text{'\$'} + P^R$.

---

## 15. Frequently Asked Interview Questions

* **Q: What is a Z-Box $[L, R]$?**  
  *A:* The segment $[L \dots R]$ with the maximum value of $R$ encountered so far such that $S[L \dots R]$ is a prefix of $S$.

* **Q: Why does the Z-Algorithm run in strict $O(N)$ linear time?**  
  *A:* Because the right boundary $R$ of the Z-Box strictly increases and never moves backward, bounding total successful character comparisons to at most $N$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: Z-ALGORITHM                                           |
+-----------------------------------------------------------------------+
| • Z-Array Def  : Z[i] = length of longest substring at S[i] matching prefix|
| • Z-Box [L, R] : Rightmost match segment S[L..R] == S[0..R-L]         |
| • Case 1 (i > R): Naive scan from i, update [L, R]                    |
| • Case 2 (i <= R): If Z[k] < R-i+1 -> Z[i] = Z[k]; else extend from R+1|
| • Pattern Match: S = P + '$' + T -> Find Z[i] == M -> O(N + M) Time ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write $O(N)$ Z-Array construction in Java.
- [ ] I can write pattern matching using $S = P + \text{'\$'} + T$.
- [ ] I can prove why the Z-Algorithm runs in $O(N)$ linear time.
- [ ] I can explain Z-Box $[L, R]$ re-use rules.
- [ ] I can solve LeetCode 214 (`Shortest Palindrome / Longest Palindromic Prefix`) using the Z-Algorithm.
