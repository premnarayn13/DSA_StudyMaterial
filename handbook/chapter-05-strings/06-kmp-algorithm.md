# 06. KMP Algorithm (Knuth-Morris-Pratt)

## 1. Introduction
The **Knuth-Morris-Pratt (KMP)** algorithm is a landmark string-matching algorithm that searches for a pattern $P$ of length $M$ inside a text $T$ of length $N$ in **$O(N + M)$ linear time and $O(M)$ auxiliary space**. Unlike naive search which backtracks the text pointer `i` upon encountering a mismatch, KMP **never backtracks the text pointer `i`**. Instead, it uses a precomputed **Longest Prefix Suffix (LPS)** array to shift the pattern pointer `j` to the longest matching proper prefix.

> **Important:** In KMP, the text pointer `i` moves strictly forward from $0$ to $N-1$ without ever moving backward! When a mismatch occurs, the pattern pointer `j` jumps to `lps[j - 1]`.

## 2. Core Concepts
* **Proper Prefix & Suffix**:
  * **Proper Prefix**: Substring from index 0 to $k < \text{len}-1$ (cannot be the entire string).
  * **Proper Suffix**: Substring from index $k > 0$ to $\text{len}-1$ (cannot be the entire string).
* **LPS Array (`lps[i]`)**: Stores the length of the **Longest Proper Prefix** of $P[0 \dots i]$ that is also a **Proper Suffix** of $P[0 \dots i]$.
* **LPS Building Algorithm**: Built using a 2-pointer approach (`len` and `i`) in $O(M)$ time.
* **KMP Mismatch Jump Rule**: When mismatch occurs at $T[i] \neq P[j]$:
  * If $j > 0$: Jump pattern pointer **`j = lps[j - 1]`** (Do NOT change text pointer `i`!).
  * If $j == 0$: Increment text pointer **`i++`**.

> **Memory Trick:** **"Mismatch at j? Set j = lps[j - 1]! Text pointer i NEVER goes backward!"**

## 3. Characteristics / Properties
* **Linear Time Guarantee**: KMP guarantees strict $O(N + M)$ worst-case execution time, making it immune to worst-case inputs that cause naive algorithms to degrade to $O(N \cdot M)$.
* **LPS Invariant**: `lps[0]` is ALWAYS `0` because a 1-character string has no non-empty proper prefix.

```
KMP vs Naive Comparison:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | Naive Search      | KMP Algorithm     | Benefit of KMP    |
+-----------------------+-------------------+-------------------+-------------------+
| Text Pointer `i`      | Backtracks `i=i+1`| Strictly Forward  | Zero redundant reads|
| Worst-Case Time       | O(N * M)          | O(N + M)          | Guaranteed Linear ⚡|
| Auxiliary Space       | O(1)              | O(M)              | Stores LPS array  |
| Precomputation        | None              | O(M) LPS Array    | Smart Pattern Shift|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing LPS Array Construction for Pattern $P =$ `"AAACAAAA"` ($M = 8$):

```
Index:    0  1  2  3  4  5  6  7
Char:     A  A  A  C  A  A  A  A
LPS:     [0, 1, 2, 0, 1, 2, 3, 3]

Step-by-step LPS Building:
i = 0: lps[0] = 0, len = 0
i = 1: P[1]=='A' == P[len]='A' -> len++, lps[1] = 1 (len=1)
i = 2: P[2]=='A' == P[len]='A' -> len++, lps[2] = 2 (len=2)
i = 3: P[3]=='C' != P[len]='A' -> len = lps[len-1] = lps[1] = 1
       P[3]=='C' != P[0]=='A'   -> len = lps[0] = 0 -> lps[3] = 0
i = 4: P[4]=='A' == P[0]='A'   -> len++, lps[4] = 1 (len=1)
i = 5: P[5]=='A' == P[1]='A'   -> len++, lps[5] = 2 (len=2)
i = 6: P[6]=='A' == P[2]='A'   -> len++, lps[6] = 3 (len=3)
i = 7: P[7]=='A' != P[3]='C'   -> len = lps[len-1] = lps[2] = 2
       P[7]=='A' == P[2]='A'   -> lps[7] = 3
```

## 5. Visual Diagram
KMP Mismatch Jump Mechanics:

```
Text T:     A  A  B  X  A  A  B  A
            |  |  |  x (Mismatch at i=3!)
Pattern P:  A  A  B  A
            |  |  |  |
Index:      0  1  2  3  (j=3)
LPS:       [0, 1, 0, 1]

Action: Mismatch at P[3] (j=3).
Jump:   j = lps[j - 1] = lps[2] = 0.
Text pointer i STAYS AT 3!
Next Check: Compare T[3] ('X') with P[0] ('A') -> Mismatch -> i++ (i=4).
```

## 6. Operations / Algorithms
Complete KMP Master Implementation:

```java
// 1. Build LPS (Longest Prefix Suffix) Array in O(M) Time
public int[] buildLPS(String pattern) {
    int M = pattern.length();
    int[] lps = new int[M];
    int len = 0; // Length of previous longest prefix suffix
    int i = 1;

    lps[0] = 0; // lps[0] is always 0

    while (i < M) {
        if (pattern.charAt(i) == pattern.charAt(len)) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1]; // Fall back to previous match
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
    return lps;
}

// 2. Main KMP Search Algorithm in O(N + M) Time
public int kmpSearch(String text, String pattern) {
    if (pattern.length() == 0) return 0;
    if (text.length() < pattern.length()) return -1;

    int[] lps = buildLPS(pattern);
    int N = text.length();
    int M = pattern.length();

    int i = 0; // Text pointer
    int j = 0; // Pattern pointer

    while (i < N) {
        if (text.charAt(i) == pattern.charAt(j)) {
            i++;
            j++;
        }

        if (j == M) {
            return i - j; // Match found at index (i - j)
            // To find all matches: j = lps[j - 1];
        } else if (i < N && text.charAt(i) != pattern.charAt(j)) {
            if (j != 0) {
                j = lps[j - 1]; // Jump pattern pointer
            } else {
                i++; // Text pointer advances only when j == 0
            }
        }
    }

    return -1; // Pattern not found
}
```

> **Quick Syntax:**
```java
// KMP Jump Rule Syntax
if (j != 0) {
    j = lps[j - 1];
} else {
    i++;
}
```

## 7. Examples
* **LeetCode 28 - Find the Index of the First Occurrence in a String**: Optimal $O(N + M)$ solution using KMP.
* **LeetCode 459 - Repeated Substring Pattern**: String $S$ has periodic repeat if `n % (n - lps[n-1]) == 0 && lps[n-1] > 0`.
* **LeetCode 214 - Shortest Palindrome**: Using KMP LPS array on `S + "#" + reverse(S)`.

## 8. Java Code
Complete interview-ready Java suite implementing KMP Search, LPS Generation, and Periodic Pattern Validation:

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class KMPMaster {

    // Build LPS Array O(M) Time, O(M) Space
    public static int[] buildLPS(String pattern) {
        int M = pattern.length();
        int[] lps = new int[M];
        int len = 0;
        int i = 1;

        lps[0] = 0;

        while (i < M) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    // KMP Search: Returns ALL Starting Indices of Matches O(N + M) Time
    public static List<Integer> kmpSearchAll(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;
        int N = text.length();
        int M = pattern.length();

        if (M == 0 || M > N) return matches;

        int[] lps = buildLPS(pattern);
        int i = 0, j = 0;

        while (i < N) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }

            if (j == M) {
                matches.add(i - j); // Found match at index (i - j)
                j = lps[j - 1];     // Prepare for next potential match
            } else if (i < N && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }

        return matches;
    }

    // LeetCode 459: Check if string is composed of repeated substrings using LPS
    public static boolean repeatedSubstringPattern(String s) {
        if (s == null || s.length() == 0) return false;
        int n = s.length();
        int[] lps = buildLPS(s);
        int lpsLen = lps[n - 1];

        // Periodicity condition using LPS
        return lpsLen > 0 && (n % (n - lpsLen) == 0);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String text = "ABABDABACDABABCABAB";
        String pattern = "ABABCABAB";

        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);

        int[] lps = buildLPS(pattern);
        System.out.println("LPS Array: " + Arrays.toString(lps));

        List<Integer> matches = kmpSearchAll(text, pattern);
        System.out.println("Pattern Matches Found At Indices: " + matches); // Output: [10]

        // Test Repeated Substring Pattern
        System.out.println("Is 'abab' periodic? " + repeatedSubstringPattern("abab")); // true
        System.out.println("Is 'aba' periodic? "  + repeatedSubstringPattern("aba"));  // false
    }
}
```

## 9. Complexity Analysis
| Phase | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **LPS Array Construction** | **$O(M)$** | **$O(M)$** | 2-pointer pattern self-match |
| **Text Matching Pass** | **$O(N)$** | $O(1)$ auxiliary | Text pointer `i` never decreases |
| **Total KMP Algorithm** | **$O(N + M)$** | **$O(M)$** | Guaranteed linear runtime ⚡ |

## 10. Edge Cases
* **Empty Pattern ($M == 0$)**: Return `0` immediately.
* **Pattern Longer Than Text ($M > N$)**: Return `-1` / empty list immediately.
* **Pattern with No Repeating Prefixes** (e.g., `"ABCDE"`): `lps` array contains all `0`s; KMP gracefully behaves like linear scan.

## 11. Common Mistakes
* Writing `len = len - 1` when mismatch occurs in LPS construction instead of **`len = lps[len - 1]`** (causes incorrect prefix length calculation!).
* Incrementing `i` when `j != 0` on mismatch (violates the KMP principle that text pointer `i` must stay fixed while `j` jumps).
* Forgetting to set `j = lps[j - 1]` after finding a match when searching for **ALL** pattern occurrences.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Key lines to memorize for KMP:
> 1. **LPS Mismatch**: `len = lps[len - 1];`
> 2. **KMP Search Mismatch**: `if (j != 0) j = lps[j - 1]; else i++;`

> **Memory Trick:** **"LPS Mismatch? Jump to lps[len - 1]!"**

## 13. Comparisons
| Metric | Naive Matching | KMP Algorithm |
| :--- | :--- | :--- |
| **Text Pointer `i`** | Backtracks (`i = i - j + 1`) | **Strictly Monotonic Forward (`i++`)** |
| **Worst-Case Time** | $O(N \cdot M)$ | **$O(N + M)$ (Optimal)** |
| **Auxiliary Space** | **$O(1)$** | $O(M)$ (Stores `lps[]`) |
| **Streaming Text Support**| NO (Requires full text in RAM) | **YES (Processes text stream in O(1) per char)** |

## 14. How to Recognize This in Questions
* **"Find first occurrence of pattern in text in linear O(N + M) time"** $\rightarrow$ KMP Algorithm.
* **"Check if string is constructed by repeating a sub-pattern"** $\rightarrow$ KMP LPS Array Trick (`n % (n - lps[n-1]) == 0`).
* **"Find shortest palindrome by adding characters in front"** $\rightarrow$ KMP LPS Array on `S + "#" + reverse(S)`.

## 15. Frequently Asked Interview Questions
* **Q: Why does the text pointer `i` never backtrack in KMP?**  
  *A:* Because the LPS array tells us the length of the longest pattern prefix that matches the text suffix we just read. Since that prefix is already matched, we skip redundant comparisons by jumping `j` directly to `lps[j - 1]`.
* **Q: How does KMP achieve $O(N + M)$ time complexity?**  
  *A:* Building LPS takes $O(M)$ steps. During matching, `i` increases by 1 in every step where $T[i] == P[j]$ or $j == 0$. When $T[i] \neq P[j]$, `j` decreases by at least 1 via `j = lps[j - 1]`. Since `j` can increase at most $N$ times, it can decrease at most $N$ times $\implies O(N + M)$ total operations.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: KMP ALGORITHM                                         |
+-----------------------------------------------------------------------+
| • LPS Definition: Longest Proper Prefix which is also a Proper Suffix |
| • LPS Mismatch Rule: len = lps[len - 1]                               |
| • Search Mismatch Rule: if (j != 0) j = lps[j - 1] else i++           |
| • Match Found: Record index (i - j), then j = lps[j - 1]              |
| • Complexity: O(N + M) Time | O(M) Auxiliary Space                     |
| • Periodicity Trick: n % (n - lps[n - 1]) == 0                        |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can define Proper Prefix and Proper Suffix.
- [ ] I can build an LPS array by hand for any pattern string.
- [ ] I can implement KMP Search in under 5 minutes.
- [ ] I know why text pointer `i` never moves backward in KMP.
- [ ] I can solve LeetCode 459 (Repeated Substring Pattern) using LPS.
