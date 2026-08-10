# 03. KMP Algorithm: Prefix Function (LPS Table), Failure Transitions & Linear Bounds

## 1. Introduction
The **Knuth-Morris-Pratt (KMP) Algorithm** is a landmark string-searching algorithm created by Donald Knuth, Vaughan Pratt, and James H. Morris in 1977. While Naive Pattern Matching resets the text alignment pointer backward upon a character mismatch (taking $O(N \cdot M)$ time), KMP guarantees **Zero Text Pointer Backtracking**. By precomputing a **Longest Proper Prefix which is also a Suffix (LPS) Table** (also known as the **Prefix Function $\pi$**) in $O(M)$ time, KMP uses matching pattern history to shift the pattern pointer $j \leftarrow \text{lps}[j-1]$ upon a mismatch, achieving **Strict $O(N + M)$ Linear Time Complexity** in **$O(M)$ Auxiliary Space**.

> **Important:** Core Invariants of the KMP Algorithm:
> 1. **Zero Text Pointer Backtracking Invariant**: The text pointer $i \in [0 \dots N-1]$ NEVER moves backward. It advances strictly rightward, making KMP ideal for real-world un-seekable data streams!
> 2. **LPS / Prefix Function Definition ($\text{lps}[i]$)**:
>    - $\text{lps}[i]$ is the length of the longest proper prefix of substring $P[0 \dots i]$ that is also a suffix of $P[0 \dots i]$.
> 3. **Mismatch Failure Transition**:
>    - Upon mismatch $T[i] \neq P[j]$ when $j > 0$, set $j \leftarrow \text{lps}[j - 1]$.
>    - If $j = 0$, increment $i \leftarrow i + 1$.
> 4. **Linear Time Complexity Proof**: Evaluated via Potential Method amortized analysis ($\Phi = j$). Increasing $i$ increases $\Phi$ by 1 ($N$ times total). Fallback transitions $j \leftarrow \text{lps}[j-1]$ decrease $\Phi$. Thus, total comparisons $\le 2N$, running in **$O(N + M)$ Strict Linear Time**. ⚡

```
KMP LPS Table & Alignment Shift Topology (Pattern P = "AAACAAAA"):
Index i:   0  1  2  3  4  5  6  7
Char P[i]: A  A  A  C  A  A  A  A
LPS Array: 0  1  2  0  1  2  3  3

Text Matching Step:
Text T:    A  A  A  A  C  A  A  A  A
Pattern P: A  A  A  C  (Mismatch at P[3] 'C' != T[3] 'A')
Shift:     j = lps[2] = 2 -> Resume comparing P[2] 'A' with T[3] 'A' WITHOUT moving text pointer i=3! ⚡
```

---

## 2. Core Concepts & KMP Algorithm Strategy Matrix

### 2.1 KMP Strategy Matrix
```
KMP Algorithm Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Component             | Primary Function  | Time Complexity   | Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+
| **LPS Precomputation**| Compute Prefix Table| **$O(M)$ Linear ⚡**| **$O(M)$ Table ⚡**|
| **KMP Search Engine** | Zero Text Backtrack| **$O(N)$ Linear ⚡**| **$O(M)$ Table ⚡**|
| **Overall KMP Algorithm**| Substring Search| **$O(N + M)$ Strict**| **$O(M)$ Table ⚡**|
+-----------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LPS table stores longest prefix-suffix match! Mismatch fallback sets j = lps[j-1] with ZERO text pointer backtracking!"**

---

## 3. Characteristics & $O(N + M)$ Potential Method Proof

### 3.1 Mathematical Proof of $O(N + M)$ Linear Time Complexity
* Let $\Phi = j$ (the value of the pattern pointer $j$) be our potential function.
* Initial potential $\Phi_0 = 0$. Since $j \ge 0$, potential $\Phi \ge 0$ at all times.
* Text loop runs for $i = 0 \dots N-1$:
  - When $T[i] == P[j]$, $j$ increments ($j \leftarrow j + 1$). Potential $\Phi$ increases by 1.
  - Total potential increases across all $N$ text steps $\le N$.
  - When $T[i] \neq P[j]$, fallback transition $j \leftarrow \text{lps}[j-1]$ strictly decreases $j$ (since $\text{lps}[j-1] < j$).
  - Because potential cannot decrease more times than it increases, the total number of fallback steps across the entire algorithm is bounded by $N$.
* Total Comparisons: $\text{Text Steps} (N) + \text{Fallback Steps} (N) + \text{LPS Precomputation} (2M) \le 2N + 2M = \mathbf{O(N + M) \text{ Strict Linear Time}}$. ⚡

---

## 4. Internal Working Mechanics: LPS Precomputation Routine

How is the LPS table built in $O(M)$ time?

```
Tracing LPS Table Construction for Pattern P = "ABABC":

Init: lps[0] = 0. len = 0 (length of previous longest prefix-suffix), i = 1.

Step 1 (i = 1, P[1]='B'): Compare P[1] 'B' with P[len=0] 'A'.
        Mismatch & len == 0 -> Set lps[1] = 0, i = 2.

Step 2 (i = 2, P[2]='A'): Compare P[2] 'A' with P[len=0] 'A'.
        Match! len++ (len = 1), Set lps[2] = 1, i = 3.

Step 3 (i = 3, P[3]='B'): Compare P[3] 'B' with P[len=1] 'B'.
        Match! len++ (len = 2), Set lps[3] = 2, i = 4.

Step 4 (i = 4, P[4]='C'): Compare P[4] 'C' with P[len=2] 'A'.
        Mismatch & len > 0 -> Fallback len = lps[len-1] = lps[1] = 0.
        Retry P[4] 'C' with P[0] 'A' -> Mismatch & len == 0 -> Set lps[4] = 0, i = 5.

Final LPS Array for "ABABC": [ 0, 0, 1, 2, 0 ]! ✅ (Built in O(M) Time!)
```

---

## 5. Visual Diagram: Zero Text Backtracking & LPS Shift Alignment

```
Text T:     A B A B C A B A B C A B A B D
            │ │ │ │ │
Pattern P:  A B A B D  (Mismatch at P[4] 'D' != T[4] 'C')
LPS P:    [ 0,0,1,2,0 ]

Fallback:   j = lps[3] = 2 (Do NOT change text pointer i = 4!)
Resume:     Compare P[2] 'A' with T[4] 'C'!

Alignment shift avoids re-comparing matched prefix "AB"! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing LPS Table Construction, KMP Substring Search (retrieving all match starting indices), and String Periodicity Analysis.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing the KMP (Knuth-Morris-Pratt) Algorithm,
 * LPS Table Precomputation, and Zero Text Backtracking Search.
 */
public class KMPMaster {

    // =========================================================================
    // 1. LPS TABLE PRECOMPUTATION (O(M) Time, O(M) Space)
    // =========================================================================
    /**
     * Builds the Longest Proper Prefix which is also a Suffix (LPS) table.
     *
     * @param pattern pattern string P
     * @return integer array containing lps values
     */
    public int[] computeLPSArray(String pattern) {
        if (pattern == null || pattern.length() == 0) return new int[0];

        int m = pattern.length();
        int[] lps = new int[m];
        lps[0] = 0; // Base case: Proper prefix of single char is empty

        int len = 0; // Length of previous longest prefix-suffix
        int i = 1;

        while (i < m) {
            if (pattern.charAt(i) == pattern.charAt(len)) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    // Fallback to previous longest prefix-suffix length
                    len = lps[len - 1]; // Do NOT increment i here! ⚡
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }

        return lps;
    }

    // =========================================================================
    // 2. KMP SEARCH ENGINE (O(N + M) Time, O(M) Space - All Matches)
    // =========================================================================
    /**
     * Finds all 0-based starting indices of pattern P in text T using KMP algorithm.
     * Guarantees zero text pointer backtracking!
     *
     * @param text input text string T
     * @param pattern search pattern P
     * @return list of starting indices where pattern occurs in text
     */
    public List<Integer> kmpSearch(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;

        int n = text.length();
        int m = pattern.length();

        if (m == 0 || m > n) return matches;

        // Step 1: Precompute LPS table in O(M) time
        int[] lps = computeLPSArray(pattern);

        int i = 0; // Text pointer (NEVER moves backward!)
        int j = 0; // Pattern pointer

        while (i < n) {
            if (text.charAt(i) == pattern.charAt(j)) {
                i++;
                j++;
            }

            if (j == m) {
                // Match Found! Record starting index
                matches.add(i - j);
                j = lps[j - 1]; // Reset pattern pointer to lps[m-1] to find overlapping matches! ⚡
            } else if (i < n && text.charAt(i) != pattern.charAt(j)) {
                // Character mismatch
                if (j != 0) {
                    j = lps[j - 1]; // Fallback using LPS table (i stays unchanged!)
                } else {
                    i++; // j is 0, advance text pointer
                }
            }
        }

        return matches;
    }
}
```

> **Quick Syntax:**
```java
// KMP Mismatch Fallback Lines
if (j != 0) j = lps[j - 1]; else i++;
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 28 - Find the Index of the First Occurrence in a String**:
   - Standard KMP application ($O(N + M)$ time).

2. **LeetCode 459 - Repeated Substring Pattern**:
   - Solved in $O(N)$ time using KMP LPS table property: If $N \% (N - \text{lps}[N-1]) == 0$ and $\text{lps}[N-1] > 0$, string is repeated!

3. **Un-Seekable Network Data Streams**:
   - Matching patterns in TCP/UDP byte streams where moving back in text is physically impossible.

---

## 8. Java Code Demonstration & Execution Suite

```java
import java.util.Arrays;
import java.util.List;

public class KMPDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("     KMP STRING MATCHING ALGORITHM DEMO          ");
        System.out.println("=================================================\n");

        KMPMaster master = new KMPMaster();

        // 1. LPS Table Precomputation Test
        String pattern = "AAACAAAA";
        int[] lps = master.computeLPSArray(pattern);
        System.out.println("1. Pattern: \"" + pattern + "\"");
        System.out.println("   Computed LPS Table: " + Arrays.toString(lps));
        System.out.println("-------------------------------------------------");

        // 2. KMP Search Engine Test (All Matches)
        String text = "ABABDABACDABABCABAB";
        String pattern2 = "ABABCABAB";
        List<Integer> matches = master.kmpSearch(text, pattern2);
        System.out.println("2. Text   : \"" + text + "\"");
        System.out.println("   Pattern: \"" + pattern2 + "\"");
        System.out.println("   KMP Matches Found at Indices: " + matches);
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| KMP Subroutine | Best Case Time | Average Case Time | Worst Case Time | Auxiliary Space | Key Invariant |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **LPS Precomputation**| $\mathbf{O(M)}$ Linear ⚡| $\mathbf{O(M)}$ Linear ⚡| $\mathbf{O(M)}$ Linear ⚡| $\mathbf{O(M)}$ Table ⚡| Proper Prefix-Suffix |
| **KMP Search Engine**  | $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(N)}$ Linear ⚡| $\mathbf{O(M)}$ Table ⚡| Zero Text Backtrack |
| **Overall KMP Algorithm**| $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(N + M)}$ ⚡| $\mathbf{O(M)}$ Table ⚡| Strict Linear Guarantee |

---

## 10. Edge Cases & Boundary Handling

1. **Pattern Not Present**:
   - Text loop terminates when $i = N$, returning an empty match list cleanly.

2. **Overlapping Pattern Matches (e.g. Text `"AAAA"`, Pattern `"AA"`)**:
   - Setting $j = \text{lps}[j-1]$ upon finding a match captures overlapping occurrences (indices 0, 1, 2).

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Incrementing Text Pointer `i++` During LPS Fallback**:
  - Incrementing $i$ during `j = lps[j - 1]` fallback skips character comparisons, causing false negative search results. **Text pointer $i$ MUST remain unchanged during fallback!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Why KMP Beats Rabin-Karp & Naive for Streaming Data:
> Network sockets and data pipes stream bytes sequentially without random disk access (`seek()`).
> Because KMP **NEVER moves text pointer $i$ backward**, KMP processes un-seekable network streams in a single forward pass! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | KMP Algorithm | Naive Pattern Matching | Rabin-Karp Algorithm |
| :--- | :--- | :--- | :--- |
| **Worst-Case Time** | **$O(N + M)$ Strict ⚡** | $O(N \cdot M)$ Quadratic | $O(N \cdot M)$ Hash Collision |
| **Text Backtracking** | **Zero Backtracking ⚡** | Resets $i \to i + 1$ | Zero Backtracking |
| **Auxiliary Memory** | $O(M)$ LPS Table | **$O(1)$ In-Place ⚡**| **$O(1)$ In-Place ⚡**|

---

## 14. How to Recognize This in Questions

* **"Search pattern in text with strict O(N + M) worst-case time guarantee"** $\rightarrow$ KMP Algorithm.
* **"Check if string S is a repeated concatenation of a smaller substring"** $\rightarrow$ KMP LPS Property ($N \% (N - \text{lps}[N-1]) == 0$).

---

## 15. Frequently Asked Interview Questions

* **Q: What does $\text{lps}[i]$ represent in KMP?**  
  *A:* The length of the longest proper prefix of $P[0 \dots i]$ that is also a suffix of $P[0 \dots i]$.

* **Q: Why does text pointer $i$ never move backward in KMP?**  
  *A:* Because the LPS table tells KMP exactly how much of the pattern's prefix already matches the text suffix before the mismatch, shifting the pattern alignment rightward without re-reading text characters.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: KMP ALGORITHM                                         |
+-----------------------------------------------------------------------+
| • LPS Definition: Longest proper prefix that is also a suffix         |
| • LPS Computation: If mismatch & len > 0 -> len = lps[len - 1]        |
| • Search Fallback: If mismatch & j > 0   -> j = lps[j - 1] (i SAME!)  |
| • Full Match Gate: If j == m -> match at i - m, then j = lps[m - 1]   |
| • Performance   : Strict O(N + M) Time | Zero Text Backtracking ⚡     |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write the $O(M)$ LPS Table Precomputation routine in Java.
- [ ] I can write KMP Search Engine with zero text pointer backtracking.
- [ ] I can prove why KMP runs in strict $O(N + M)$ time using potential method amortized analysis.
- [ ] I can solve LeetCode 459 (`Repeated Substring Pattern`) using the LPS table.
- [ ] I can explain why text pointer $i$ does NOT advance during LPS fallback.
