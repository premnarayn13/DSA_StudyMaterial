# 02. Naive Pattern Matching: Sliding Window Scanning & Worst-Case Analysis

## 1. Introduction
**Naive Pattern Matching (Brute-Force Substring Search)** is the fundamental baseline pattern-matching algorithm. Given a **Text String $T$** of length $N$ and a **Pattern String $P$** of length $M$ ($M \le N$), Naive Pattern Matching tests all possible alignment offset shifts $i \in [0 \dots N - M]$ by comparing characters $P[j]$ with $T[i + j]$ for $j \in [0 \dots M - 1]$. If a mismatch occurs at $P[j]$, the algorithm resets the text alignment pointer to $i + 1$ and restarts pattern comparison from $j = 0$. While simple to implement in **$O(1)$ Auxiliary Space**, Naive Pattern Matching degrades to **$O(N \cdot M)$ Worst-Case Time Complexity** on repetitive texts.

> **Important:** Core Invariants of Naive Pattern Matching:
> 1. **Alignment Offset Shift Range**: Evaluates exactly $N - M + 1$ possible starting alignment offsets $i \in [0 \dots N - M]$.
> 2. **Character Comparison Loop**: For each offset $i$, compares character-by-character $P[j] == T[i + j]$.
> 3. **Mismatch Reset Invariant**: Upon encountering mismatch $P[j] \neq T[i + j]$, text pointer resets to $i + 1$ and pattern pointer resets to $j = 0$.
> 4. **Unique Character Optimization**: If pattern $P$ contains all distinct characters, upon finding a mismatch at $j$, alignment offset can jump directly to $i + j + 1$, optimizing worst-case time to **$O(N)$ Linear Time**! ⚡

```
Naive Pattern Matching Sliding Alignment Topology:
Text T:    A B C D A B C E X    (N = 9)
Pattern P: A B C E              (M = 4)

Offset 0: T[0..3] "A B C D" vs P "A B C E" ──> Mismatch at j=3 ('D' != 'E') ──> Shift i to 1
Offset 1: T[1..4] "B C D A" vs P "A B C E" ──> Mismatch at j=0 ('B' != 'A') ──> Shift i to 2
Offset 2: T[2..5] "C D A B" vs P "A B C E" ──> Mismatch at j=0 ('C' != 'A') ──> Shift i to 3
Offset 3: T[3..6] "D A B C" vs P "A B C E" ──> Mismatch at j=0 ('D' != 'A') ──> Shift i to 4
Offset 4: T[4..7] "A B C E" vs P "A B C E" ──> MATCH FOUND AT INDEX 4! ⚡
```

---

## 2. Core Concepts & Naive Matching Strategy Matrix

### 2.1 Naive Pattern Matching Strategy Matrix
```
Naive Pattern Matching Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Pattern Type          | Comparison Policy | Worst Case Time   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **Standard Naive**    | Reset $i \to i+1$ | **$O(N \cdot M)$ ❌**| **$O(1)$ In-Place ⚡**|
| **Distinct Pattern**  | Jump $i \to i+j+1$| **$O(N)$ Linear ⚡** | **$O(1)$ In-Place ⚡**|
| **Early Exit Variant**| Terminate on 1st  | $O((N - M + 1) \cdot M)$| **$O(1)$ In-Place ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Naive Search checks all N - M + 1 offsets! Worst case O(N * M) on repetitive text like 'AAAAA' and 'AAAAB'!"**

---

## 3. Characteristics & $O(N \cdot M)$ Worst-Case Complexity Proof

### 3.1 Mathematical Proof of Worst-Case $O(N \cdot M)$ Time
* Consider Text $T = \text{"AAAAAAAAAA"}$ ($N$ 'A's) and Pattern $P = \text{"AAAAB"}$ ($M-1$ 'A's followed by 1 'B').
* At each alignment offset $i \in [0 \dots N - M]$:
  - The algorithm compares $M - 1$ matching 'A' characters before failing on 'B' at index $j = M - 1$.
  - Number of comparisons per offset $= M$.
* Total offsets evaluated $= N - M + 1$.
* Total Character Comparisons:
  $$C_{\max} = (N - M + 1) \times M = \mathbf{O(N \cdot M) \text{ Quadratic Time Complexity}}$$
* Auxiliary Space: $\mathbf{O(1) \text{ Constant Space}}$. ⚡

---

## 4. Internal Working Mechanics: Distinct Pattern Optimization ($O(N)$ Jump)

If all characters in Pattern $P$ are unique (e.g. $P = \text{"ABCD"}$), a mismatch at $P[j]$ proves that no alignment between $i + 1$ and $i + j$ can possibly match $P$:

```
Distinct Pattern Jump Topology:
Text T:    A B C X A B C D
Pattern P: A B C D  (All characters distinct!)

Offset 0: Compare P "ABCD" with T[0..3] "ABCX".
Mismatch at j = 3 ('X' != 'D').

Because P has all unique characters:
- T[1] is 'B' -> Cannot match P[0] 'A'!
- T[2] is 'C' -> Cannot match P[0] 'A'!

Optimization: Jump offset i directly from 0 to i + j + 1 = 4!
Next comparison evaluates T[4..7] "ABCD" directly!
Runs in O(N) Linear Time! ✅
```

---

## 5. Visual Diagram: Sliding Window Character Alignment

```
Text T:     [ A | B | C | D | A | B | C | E | X ]
              │   │   │   │
Offset 0:   [ A | B | C | E ]   ──> Mismatch at index 3 ('D' != 'E')
                  │
Offset 1:       [ A | B | C | E ] ──> Mismatch at index 0 ('B' != 'A')
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Standard Naive Pattern Matching (all occurrences), Early Exit Matcher, and Distinct Pattern Optimized Matcher.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Naive Pattern Matching Algorithms,
 * All Occurrences Retrieval, and Distinct Pattern Jump Optimizations.
 */
public class NaivePatternMatchingMaster {

    // =========================================================================
    // 1. STANDARD NAIVE PATTERN MATCHING (All Occurrences O(N * M) Time)
    // =========================================================================
    /**
     * Finds all 0-based starting indices of pattern P in text T.
     *
     * @param text input text string T
     * @param pattern pattern string P
     * @return list of starting match indices
     */
    public List<Integer> searchAllOccurrences(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();

        if (m == 0 || m > n) return matches;

        // Slide alignment offset i from 0 to N - M
        for (int i = 0; i <= n - m; i++) {
            int j;

            // Test character-by-character match for current offset i
            for (j = 0; j < m; j++) {
                if (text.charAt(i + j) != pattern.charAt(j)) {
                    break; // Mismatch encountered -> Exit inner loop
                }
            }

            // If pattern pointer reached m, full match found!
            if (j == m) {
                matches.add(i);
            }
        }

        return matches;
    }

    // =========================================================================
    // 2. DISTINCT PATTERN OPTIMIZED MATCHING (O(N) Linear Time)
    // =========================================================================
    /**
     * Optimized search for patterns containing ALL DISTINCT characters.
     * Jumps text alignment offset i directly to i + j upon mismatch.
     */
    public List<Integer> searchDistinctPattern(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();
        if (m == 0 || m > n) return matches;

        int i = 0;
        while (i <= n - m) {
            int j;
            for (j = 0; j < m; j++) {
                if (text.charAt(i + j) != pattern.charAt(j)) {
                    break;
                }
            }

            if (j == m) {
                matches.add(i);
                i += m; // Full match found -> Jump by pattern length M!
            } else if (j == 0) {
                i++;    // Mismatch at first char -> Shift by 1
            } else {
                i += j; // Mismatch at index j -> Jump directly by j positions! ⚡
            }
        }

        return matches;
    }
}
```

> **Quick Syntax:**
```java
// Naive Alignment Shift Loop Line
for (int i = 0; i <= n - m; i++) { int j = 0; while (j < m && text.charAt(i + j) == pattern.charAt(j)) j++; if (j == m) matches.add(i); }
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 28 - Find the Index of the First Occurrence in a String**:
   - Primary string matching benchmark problem.

2. **Small Text File Searching**:
   - Searching short keywords in small documents where $M \le 5$ and $N \le 100$.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.List;

public class NaivePatternMatchingDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   NAIVE PATTERN MATCHING DEMONSTRATION          ");
        System.out.println("=================================================\n");

        NaivePatternMatchingMaster master = new NaivePatternMatchingMaster();

        // 1. Standard Naive Match Test
        String text1 = "AABCCAABAAABCA";
        String pattern1 = "AABC";
        List<Integer> matches1 = master.searchAllOccurrences(text1, pattern1);
        System.out.println("1. Text   : \"" + text1 + "\"");
        System.out.println("   Pattern: \"" + pattern1 + "\"");
        System.out.println("   Matches Found at Indices: " + matches1);
        System.out.println("-------------------------------------------------");

        // 2. Distinct Pattern Jump Test
        String text2 = "ABCEABCDABCFABCD";
        String pattern2 = "ABCD";
        List<Integer> matches2 = master.searchDistinctPattern(text2, pattern2);
        System.out.println("2. Text (Distinct Pattern Search): \"" + text2 + "\"");
        System.out.println("   Pattern                       : \"" + pattern2 + "\"");
        System.out.println("   Matches Found (O(N) Jump)    : " + matches2);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Naive Pattern Variant | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard Naive** | $\mathbf{O(N)}$ Linear | $\mathbf{O(N)}$ Average | $O(N \cdot M)$ ❌| $\mathbf{O(1)}$ In-Place ⚡| Mismatch at $j=0$ |
| **Distinct Pattern**| $\mathbf{O(N / M)}$ | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(1)}$ In-Place ⚡| Jump $i \leftarrow i + j$ |

---

## 10. Edge Cases & Boundary Handling

1. **Pattern Length Greater Than Text ($M > N$)**:
   - Loop `i <= n - m` condition fails immediately, returning an empty match list safely.

2. **Pattern Equals Text ($M = N$)**:
   - Evaluates single offset $i = 0$.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Loop Bound `i < n - m` Instead of `i <= n - m`**:
  - Writing `i < n - m` misses checking the final possible match position at index $N - M$.

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why Naive Search Performs Well on Random English Text:
> For natural English language text, characters mismatch almost immediately at $j = 0$ or $j = 1$ with probability $\approx 1 - 1/26 \approx 96\%$.
> Thus, average comparisons per offset is $\approx 1.08$, running in **$O(N)$ Average Time** on natural text! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Naive Pattern Matching | KMP Algorithm | Rabin-Karp Algorithm |
| :--- | :--- | :--- | :--- |
| **Worst-Case Time** | $O(N \cdot M)$ Quadratic | **$O(N + M)$ Linear ⚡** | $O(N \cdot M)$ Worst |
| **Pre-processing Time**| **$O(0)$ Zero Overhead ⚡**| $O(M)$ LPS Table | $O(M)$ Hash Compute |
| **Auxiliary Memory** | **$O(1)$ Constant Space ⚡**| $O(M)$ LPS Table | $O(1)$ Constant Space |

---

## 14. How to Recognize This in Questions

* **"Implement strStr() / substring search without advanced string tables"** $\rightarrow$ Naive Pattern Matching.

---

## 15. Frequently Asked Interview Questions

* **Q: When does Naive Pattern Matching degrade to worst-case $O(N \cdot M)$ time?**  
  *A:* When both text and pattern contain repetitive character sequences (e.g. Text = `"AAAAAA"`, Pattern = `"AAAB"`), forcing $M$ comparisons at every single offset.

* **Q: Why does a pattern with all distinct characters allow jumping $i \leftarrow i + j$?**  
  *A:* Because matching $j$ distinct characters proves that none of the intermediate text positions $i+1 \dots i+j-1$ can match the pattern's starting character $P[0]$.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: NAIVE PATTERN MATCHING                                |
+-----------------------------------------------------------------------+
| • Search Range  : Slide offset i from 0 to N - M                      |
| • Outer Condition: Must use i <= n - m (inclusive boundary!)          |
| • Worst Case    : O(N * M) on repetitive text (e.g. "AAAA" & "AAAB")    |
| • Average Case  : O(N) on natural text due to fast j=0 mismatches     |
| • Distinct Opt  : Jump offset i += j when all pattern chars unique! ⚡|
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write standard Naive Pattern Matching returning all match indices in Java.
- [ ] I can write the Distinct Pattern $O(N)$ jump optimization.
- [ ] I can state the worst-case text and pattern inputs that trigger $O(N \cdot M)$ time.
- [ ] I can explain why Naive search runs in $O(N)$ average time on natural language text.
- [ ] I can state the exact outer loop boundary condition (`i <= n - m`).
