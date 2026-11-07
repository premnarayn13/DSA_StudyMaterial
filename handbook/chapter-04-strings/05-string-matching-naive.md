# 05. Naive String Matching & Brute Force Substring Search

## 1. Introduction
**Naive String Matching** (or Brute Force Substring Search) checks if a pattern string $P$ of length $M$ exists within a text string $T$ of length $N$ by testing all possible alignment index shifts. In technical coding interviews (LeetCode 28 "Find the Index of the First Occurrence in a String"), understanding the worst-case **$O((N - M + 1) \cdot M) \approx O(N \cdot M)$** time bound of naive searching motivates why linear-time advanced algorithms like KMP, Rabin-Karp, and Z-Algorithm are necessary.

> **Important:** The outer loop of naive substring matching only needs to iterate up to index **`i <= N - M`**. Sliding past `N - M` is impossible because there are fewer than $M$ characters remaining in text $T$!

## 2. Core Concepts
* **Alignment Index Shift**: Trying every starting index `i` from $0$ to $N - M$ in text $T$.
* **Character Matching Loop**: For each index `i`, matching characters $T[i + j]$ against $P[j]$ for $j = 0 \dots M-1$.
* **Backtracking Reset**: If a character mismatch occurs at $P[j]$, the search resets text pointer `i` to `i + 1` and pattern pointer `j` to `0`, discarding all matched prefix progress.
* **Worst-Case Trigger**: Occurs when text $T$ consists of repeated matching prefixes followed by a mismatching character (e.g., $T =$ `"AAAAAAAAAB"`, $P =$ `"AAAB"`).

> **Memory Trick:** **"Outer loop limit is N - M, NOT N!"**

## 3. Characteristics / Properties
* **Zero Auxiliary Space**: Naive matching requires **$O(1)$ space** because it compares characters in-place using dual pointers (`i`, `j`) without allocating auxiliary tables.
* **Average vs Worst-Case Performance**:
  * **Average Case**: $O(N)$ for natural language texts (mismatches usually occur on character 1 or 2).
  * **Worst Case**: $O(N \cdot M)$ for repetitive text patterns.

```
Substring Matching Performance Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Search Algorithm      | Time Complexity   | Space Complexity  | Precomputation    |
+-----------------------+-------------------+-------------------+-------------------+
| Naive Brute Force     | O(N * M) worst    | O(1)              | None (O(0))       |
| KMP Algorithm         | O(N + M)          | O(M)              | O(M) (LPS Array)  |
| Rabin-Karp (Rolling Hash)| O(N + M) avg   | O(1)              | O(M) Hash         |
| Z-Algorithm           | O(N + M)          | O(N + M)          | O(N + M) Z-Array  |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Naive String Matching for Text $T =$ `"AABAACAADAABAABA"` ($N = 16$), Pattern $P =$ `"AABA"` ($M = 4$):

```
Shift 0 (i = 0):
T: A A B A A C A A D A A B A A B A
   | | | |
P: A A B A  -> MATCH FOUND AT INDEX 0! 🎉

Shift 1 (i = 1):
T: A A B A A C A A D A A B A A B A
     |
P:   A A B A  -> Mismatch at T[1]='A', P[0]='A' -> Wait, T[1]=='A', T[2]=='B' != P[2]=='A' -> Shift!

Shift 9 (i = 9):
T: A A B A A C A A D A A B A A B A
                     | | | |
P:                   A A B A  -> MATCH FOUND AT INDEX 9! 🎉
```

## 5. Visual Diagram
Naive Backtracking Pointer Reset Mechanism:

```
Text T:     A  A  A  A  A  B
            ^
            i=0
Pattern P:  A  A  A  B
            ^  ^  ^  x (Mismatch at j=3!)

Naive Action: Reset text pointer i = i + 1 (i=1), pattern pointer j = 0.
Discards the fact that we ALREADY know T[1..2] == "AA"! (Wasteful re-comparison!)
```

## 6. Operations / Algorithms
LeetCode 28 Naive Search Implementation:

```java
public int strStrNaive(String haystack, String needle) {
    int N = haystack.length();
    int M = needle.length();

    if (M == 0) return 0;
    if (M > N) return -1;

    // Outer loop limit: N - M (inclusive)
    for (int i = 0; i <= N - M; i++) {
        int j = 0;
        // Inner loop: Check if needle matches starting at haystack[i]
        while (j < M && haystack.charAt(i + j) == needle.charAt(j)) {
            j++;
        }
        // If all M characters matched, return starting index
        if (j == M) {
            return i;
        }
    }
    return -1; // Pattern not found
}
```

> **Quick Syntax:**
```java
// Standard Java Built-in Method (Uses optimized SIMD / vector search in JVM)
int index = haystack.indexOf(needle);
```

## 7. Examples
* **LeetCode 28 - Find the Index of the First Occurrence in a String**: Implementing `strStr()` without library calls.
* **Repeated Substring Pattern (LeetCode 459)**: Checking string periodicity using brute force sliding windows.

## 8. Java Code
Complete interview-ready Java suite demonstrating Naive String Matching, All Matches Index Finder, and Performance Benchmarking:

```java
import java.util.ArrayList;
import java.util.List;

public class NaiveStringMatchingMaster {

    // 1. Naive Substring Search: Returns First Match Index O(N * M) Worst Case, O(1) Space
    public static int findFirstMatch(String text, String pattern) {
        if (pattern == null || text == null) return -1;
        int N = text.length();
        int M = pattern.length();

        if (M == 0) return 0;
        if (M > N) return -1;

        // Outer loop limit: N - M
        for (int i = 0; i <= N - M; i++) {
            int j = 0;
            // Compare pattern against text window starting at i
            while (j < M && text.charAt(i + j) == pattern.charAt(j)) {
                j++;
            }
            if (j == M) {
                return i; // Found match at index i
            }
        }

        return -1; // No match found
    }

    // 2. Naive Substring Search: Returns List of ALL Occurrence Indices
    public static List<Integer> findAllMatches(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (pattern == null || text == null) return matches;
        int N = text.length();
        int M = pattern.length();

        if (M == 0 || M > N) return matches;

        for (int i = 0; i <= N - M; i++) {
            int j = 0;
            while (j < M && text.charAt(i + j) == pattern.charAt(j)) {
                j++;
            }
            if (j == M) {
                matches.add(i);
            }
        }

        return matches;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String text = "AABAACAADAABAABA";
        String pattern = "AABA";

        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);

        int firstIndex = findFirstMatch(text, pattern);
        System.out.println("First Match Index: " + firstIndex); // Output: 0

        List<Integer> allIndices = findAllMatches(text, pattern);
        System.out.println("All Match Indices: " + allIndices); // Output: [0, 9, 12]
    }
}
```

## 9. Complexity Analysis
| Operation | Time Complexity (Best) | Time Complexity (Worst) | Auxiliary Space |
| :--- | :--- | :--- | :--- |
| **First Match Search** | $\Omega(M)$ (Match at index 0) | $O((N - M + 1) \cdot M)$ | **$O(1)$ Constant** |
| **Find All Matches** | $\Omega(N)$ (Mismatch on 1st char)| $O(N \cdot M)$ | $O(K)$ for matches list |
| **Space Complexity** | $O(1)$ | $O(1)$ | No tables allocated |

## 10. Edge Cases
* **Pattern Length Greater than Text ($M > N$)**: Return `-1` immediately.
* **Empty Pattern ($M == 0$)**: Return `0` (Standard Java `indexOf` behavior).
* **Empty Text ($N == 0$)**: If $M > 0$, return `-1`.
* **Pattern Equals Text ($M == N$)**: Loops exactly once at `i = 0`.

## 11. Common Mistakes
* Writing `i < N` in outer loop instead of `i <= N - M` (causes out of bounds `StringIndexOutOfBoundsException` when `i + j` exceeds `N`).
* Forgetting to reset `j = 0` inside the inner loop for each new shift `i`.
* Creating substrings `text.substring(i, i + M).equals(pattern)` inside the loop, which allocates $O(N)$ garbage objects on the heap.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never use `text.substring(i, i + M).equals(pattern)` inside a loop to check for matching substrings! Calling `.substring()` inside an $N$-step loop allocates $N$ temporary heap objects ($O(N \cdot M)$ memory garbage!). Use dual character comparison pointers `i + j` and `j` to maintain **$O(1)$ space**.

> **Memory Trick:** **"Outer loop limit: i <= N - M"**.

## 13. Comparisons
| Metric | Dual Pointer Naive Search | `text.substring().equals()` |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N \cdot M)$ worst case | $O(N \cdot M)$ worst case |
| **Auxiliary Space** | **$O(1)$ (Zero Object Garbage)** | $O(N \cdot M)$ Garbage Objects |
| **Early Termination**| Stops on 1st mismatching char | Compares full $M$ chars every time |
| **Interview Recommendation** | **PREFERRED BRUTE FORCE** | AVOID |

## 14. How to Recognize This in Questions
* **"Find index of first occurrence of needle in haystack without built-ins"** $\rightarrow$ Dual-pointer Naive Search or KMP.
* **"Check if pattern exists in text in small/constrained inputs (N, M <= 1000)"** $\rightarrow$ Naive Search ($O(N \cdot M)$ acceptable).

## 15. Frequently Asked Interview Questions
* **Q: Why does Naive String Matching take $O(N \cdot M)$ in the worst case?**  
  *A:* Because for each of the $N - M + 1$ starting positions in text $T$, the inner loop compares up to $M$ characters before encountering a mismatch, resulting in $(N - M + 1) \cdot M \approx O(N \cdot M)$ total character comparisons.
* **Q: Why is `indexOf()` in Java JDK faster than naive Java loops in practice?**  
  *A:* Modern JVMs vectorize `indexOf()` using SIMD (Single Instruction Multiple Data) AVX-512 CPU instructions to scan multiple characters in parallel in hardware.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: NAIVE STRING MATCHING                                 |
+-----------------------------------------------------------------------+
| • Outer Loop Bound: for (int i = 0; i <= N - M; i++)                  |
| • Inner Loop Check: while (j < M && text[i+j] == pattern[j]) j++      |
| • Match Condition: if (j == M) return i;                              |
| • Worst-Case Complexity: O(N * M) Time | O(1) Auxiliary Space          |
| • Avoid substring() in loops to prevent O(N * M) object allocation GC  |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the outer loop limit `i <= N - M` from memory.
- [ ] I can implement dual-pointer naive string search in under 3 minutes.
- [ ] I know why `.substring()` in loops creates heap garbage.
- [ ] I know the worst-case inputs for naive matching ($T=$ `"AAAAAB"`, $P=$ `"AAAB"`).
- [ ] I can return all matching indices of a pattern in a text.
