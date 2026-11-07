# 08. Subsequence DP: LCS Matrix Alignment, Palindromic Subsequences & Reconstructions

## 1. Introduction
**Subsequence Dynamic Programming** encompasses sequence alignment algorithms operating on non-contiguous subsequences derived by deleting zero or more elements without changing the relative order of remaining elements. The cornerstone of Subsequence DP is the **Longest Common Subsequence (LCS)** pattern, created by Richard Bellman and expanded by Minimum Edit Distance and Bioinformatics Sequence Alignment (Needleman-Wunsch). Subsequence DP addresses major variation benchmarks, including **Longest Common Subsequence (LeetCode 1143)**, **Longest Palindromic Subsequence (LeetCode 516)**, **Shortest Common Supersequence (LeetCode 1092)**, and **Distinct Subsequences (LeetCode 115)**. Subsequence DP executes in **$O(M \cdot N)$ Time Complexity** and can be space-compressed to **$O(N)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of Subsequence DP:
> 1. **LCS 2D State Representation ($DP[i][j]$)**:
>    - $DP[i][j]$ represents the length of the longest common subsequence between prefix $S_1[0 \dots i-1]$ and prefix $S_2[0 \dots j-1]$.
> 2. **LCS Character Match vs Mismatch Recurrence**:
>    - If characters match ($S_1[i-1] == S_2[j-1]$):
>      $$DP[i][j] = 1 + DP[i-1][j-1]$$
>    - If characters mismatch ($S_1[i-1] \neq S_2[j-1]$):
>      $$DP[i][j] = \max\left( DP[i-1][j], \, DP[i][j-1] \right)$$
> 3. **Longest Palindromic Subsequence (LPS) Reduction Invariant (LeetCode 516)**:
>    - The Longest Palindromic Subsequence of string $S$ is mathematically equivalent to the **LCS of $S$ and its Reverse $S^R$**:
>      $$\text{LPS}(S) = \text{LCS}(S, S^R)$$
> 4. **1D Rolling Array Space Compression**:
>    - Compresses $O(M \cdot N)$ 2D matrix down to 1D Array $DP[N]$ using a temporary variable `prevDiag` to store $DP[i-1][j-1]$. ⚡

```
LCS 2D Matrix Alignment Topology (S1 = "abcde", S2 = "ace"):

       ''   a   c   e
  '' [  0   0   0   0 ]
  a  [  0   1   1   1 ]  ──► Match at 'a': 1 + dp[i-1][j-1]!
  b  [  0   1   1   1 ]
  c  [  0   1   2   2 ]  ──► Match at 'c': 1 + dp[i-1][j-1]!
  d  [  0   1   2   2 ]
  e  [  0   1   2   3 ]  ──► Match at 'e': 1 + dp[i-1][j-1] -> LCS = 3 ("ace")! ⚡
```

---

## 2. Core Concepts & Subsequence DP Strategy Matrix

### 2.1 Subsequence DP Variants Comparison Matrix
```
Subsequence DP Variants Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Subsequence Variant   | Target Output     | Key State Recurrence| Time Complexity | Auxiliary Space   |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **LCS (LeetCode 1143)**| Longest LCS Length| Match: $1+dp[i-1][j-1]$, Mismatch: $\max$| **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
| **LPS (LeetCode 516)** | Longest Palindrome| $\text{LCS}(S, S^R)$| **$O(N^2)$ ⚡**   | **$O(N)$ 1D Array⚡**|
| **SCS (LeetCode 1092)**| Shortest Superseq | Length $= M + N - \text{LCS}$| **$O(M \cdot N)$ ⚡**| $O(M \cdot N)$ Table|
| **Distinct Subseq (115)**| Total Subseq Ways| Match: $dp[i-1][j-1] + dp[i-1][j]$| **$O(M \cdot N)$ ⚡**| **$O(N)$ 1D Array⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"LCS match = 1 + dp[i-1][j-1]; mismatch = max(dp[i-1][j], dp[i][j-1]); LPS(S) = LCS(S, S^R)!"**

---

## 3. Characteristics & Shortest Common Supersequence Mathematical Proof

### 3.1 Mathematical Proof of Shortest Common Supersequence (SCS) Length
* **Definition**: A supersequence of $S_1$ and $S_2$ is a string that contains BOTH $S_1$ and $S_2$ as subsequences.
* **Length Formula Theorem**:
  $$\text{Length}(\text{SCS}(S_1, S_2)) = |S_1| + |S_2| - \text{LCS}(S_1, S_2)$$
* **Proof**:
  1. Concatenating $S_1$ and $S_2$ yields a valid supersequence of length $|S_1| + |S_2|$.
  2. However, characters belonging to the Longest Common Subsequence $\text{LCS}(S_1, S_2)$ appear in BOTH $S_1$ and $S_2$ in identical relative order.
  3. We can merge these $\text{LCS}$ characters to appear ONCE instead of twice.
  4. Merging $\text{LCS}(S_1, S_2)$ reduces the total required supersequence length by exactly $\text{LCS}(S_1, S_2)$ characters.
  5. Thus, the shortest possible supersequence has length $|S_1| + |S_2| - \text{LCS}(S_1, S_2)$! ⚡

---

## 4. Internal Working Mechanics: LCS Backtracking Path Reconstruction

How to reconstruct the actual LCS string from 2D DP matrix $DP[M+1][N+1]$:

```
Reconstruction Algorithm starting at DP[M][N]:

1. If S1[i-1] == S2[j-1]:
   - Character is part of LCS! Prepend S1[i-1] to result.
   - Move diagonally up-left: i = i - 1, j = j - 1.

2. Else if DP[i-1][j] > DP[i][j-1]:
   - Move UP: i = i - 1.

3. Else:
   - Move LEFT: j = j - 1.

Repeat until i == 0 or j == 0! Reconstructs LCS string in O(M + N) time! ✅ ⚡
```

---

## 5. Visual Diagram: 2D Matrix Diagonal Space Compression

```
1D Array Space Compression Topology (LCS Row-by-Row Update):

Previous Row i-1: [ ... | prevDiag (i-1, j-1) | dp[j] (i-1, j) | ... ]
Current Row i  : [ ... | dp[j-1] (i, j-1)     | NEW dp[j] (i, j)| ... ]

Variable prevDiag holds dp[i-1][j-1] before dp[j] is overwritten!
Compresses 2D matrix DP[M+1][N+1] to 1D Array DP[N+1]! ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Longest Common Subsequence (LeetCode 1143), Longest Palindromic Subsequence (LeetCode 516), Shortest Common Supersequence Reconstruction (LeetCode 1092), and 1D Space Compression.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing Subsequence DP Algorithms:
 * LCS Matrix Alignment, LPS Reduction, Shortest Common Supersequence, and Space Compression.
 */
public class SubsequenceDPMaster {

    // =========================================================================
    // 1. LEETCODE 1143: LONGEST COMMON SUBSEQUENCE (O(M * N) Time, O(N) Space)
    // =========================================================================
    /**
     * Calculates length of Longest Common Subsequence between text1 and text2.
     *
     * @param text1 first string
     * @param text2 second string
     * @return LCS length
     */
    public int longestCommonSubsequence(String text1, String text2) {
        if (text1 == null || text2 == null || text1.isEmpty() || text2.isEmpty()) return 0;

        int m = text1.length();
        int n = text2.length();

        int[] dp = new int[n + 1];

        for (int i = 1; i <= m; i++) {
            int prevDiag = 0; // Holds dp[i-1][j-1] ⚡

            for (int j = 1; j <= n; j++) {
                int temp = dp[j]; // Save dp[i-1][j] for next column's prevDiag

                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[j] = 1 + prevDiag; // Character match!
                } else {
                    dp[j] = Math.max(dp[j], dp[j - 1]); // Mismatch: max(top, left)
                }

                prevDiag = temp; // Shift prevDiag
            }
        }

        return dp[n];
    }

    // =========================================================================
    // 2. LEETCODE 516: LONGEST PALINDROMIC SUBSEQUENCE (O(N^2) Time, O(N) Space)
    // =========================================================================
    /**
     * Solves Longest Palindromic Subsequence by reducing to LCS(S, Reverse(S)).
     */
    public int longestPalindromeSubseq(String s) {
        if (s == null || s.isEmpty()) return 0;

        String sReverse = new StringBuilder(s).reverse().toString();
        return longestCommonSubsequence(s, sReverse); // LPS(S) = LCS(S, S^R)! ⚡
    }

    // =========================================================================
    // 3. LEETCODE 1092: SHORTEST COMMON SUPERSEQUENCE (O(M * N) Time & Build)
    // =========================================================================
    /**
     * Reconstructs the Shortest Common Supersequence string for str1 and str2.
     */
    public String shortestCommonSupersequence(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();

        // Step 1: Build full 2D LCS table
        int[][] dp = new int[m + 1][n + 1];

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }

        // Step 2: Backtrack from dp[m][n] to reconstruct supersequence
        StringBuilder sb = new StringBuilder();
        int i = m, j = n;

        while (i > 0 && j > 0) {
            if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                sb.append(str1.charAt(i - 1)); // Common LCS char added ONCE!
                i--;
                j--;
            } else if (dp[i - 1][j] > dp[i][j - 1]) {
                sb.append(str1.charAt(i - 1));
                i--;
            } else {
                sb.append(str2.charAt(j - 1));
                j--;
            }
        }

        // Append remaining characters
        while (i > 0) sb.append(str1.charAt(--i));
        while (j > 0) sb.append(str2.charAt(--j));

        return sb.reverse().toString();
    }
}
```

> **Quick Syntax:**
```java
// LCS 1D Space Compression Transition Line
if (s1.charAt(i-1) == s2.charAt(j-1)) dp[j] = 1 + prevDiag; else dp[j] = Math.max(dp[j], dp[j-1]);
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 1143 - Longest Common Subsequence**:
   - Standard 2D sequence alignment benchmark ($O(M \cdot N)$ time, $O(N)$ space).

2. **LeetCode 516 - Longest Palindromic Subsequence**:
   - Solved via reduction $\text{LPS}(S) = \text{LCS}(S, S^R)$ ($O(N^2)$ time).

3. **LeetCode 1092 - Shortest Common Supersequence**:
   - 2D LCS table backtracking reconstruction ($O(M \cdot N)$ time).

---

## 8. Java Code Demonstration & Execution Suite

```java
public class SubsequenceDPDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   SUBSEQUENCE DYNAMIC PROGRAMMING DEMO          ");
        System.out.println("=================================================\n");

        SubsequenceDPMaster master = new SubsequenceDPMaster();

        // 1. LCS Test (LeetCode 1143)
        String text1 = "abcde", text2 = "ace";
        int lcsLen = master.longestCommonSubsequence(text1, text2);
        System.out.println("1. LeetCode 1143 LCS for \"" + text1 + "\" and \"" + text2 + "\":");
        System.out.println("   LCS Length (1D Space): " + lcsLen + " (\"ace\")");
        System.out.println("-------------------------------------------------");

        // 2. LPS Test (LeetCode 516)
        String s = "bbbab";
        int lpsLen = master.longestPalindromeSubseq(s);
        System.out.println("2. LeetCode 516 LPS for \"" + s + "\":");
        System.out.println("   Longest Palindromic Subsequence Length: " + lpsLen + " (\"bbbb\")");
        System.out.println("-------------------------------------------------");

        // 3. SCS Reconstruction Test (LeetCode 1092)
        String str1 = "abac", str2 = "cab";
        String scsStr = master.shortestCommonSupersequence(str1, str2);
        System.out.println("3. LeetCode 1092 SCS Reconstruction for \"" + str1 + "\" and \"" + str2 + "\":");
        System.out.println("   Shortest Common Supersequence: \"" + scsStr + "\" (Length = " + scsStr.length() + ")");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| Subsequence DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **LCS (LeetCode 1143)**| $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| `1 + prevDiag` on match |
| **LPS (LeetCode 516)** | $\mathbf{O(N^2)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| Reduced to $\text{LCS}(S, S^R)$ |
| **SCS (LeetCode 1092)**| $\mathbf{O(M \cdot N)}$ ⚡| $O(M \cdot N)$ Table | Backtracking reconstruction |

---

## 10. Edge Cases & Boundary Handling

1. **No Common Characters Between Strings (`text1 = "abc", text2 = "def"`)**:
   - `longestCommonSubsequence` returns `0`.

2. **Strings Are Identical (`text1 = text2`)**:
   - Returns full string length `text1.length()`.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Re-instantiating Reverse String Manually Without Building LCS Table**:
  - Attempting to compute LPS via separate 2D DP matrix without reducing to $\text{LCS}(S, S^R)$ doubles code complexity. ALWAYS reduce LPS to $\text{LCS}(S, S^R)$!

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Longest Palindromic Subsequence Reduction:
> The Longest Palindromic Subsequence of string $S$ is mathematically IDENTICAL to the **Longest Common Subsequence of $S$ and its Reverse $S^R$**:
> $$\text{LPS}(S) = \text{LCS}(S, S^R)$$ ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | LCS Alignment | Substring Matching | Subarray Matching |
| :--- | :--- | :--- | :--- |
| **Continuity** | **Discontiguous Subsequence ⚡**| Contiguous Substring | Contiguous Subarray |
| **Mismatch Handling**| $\max(dp[i-1][j], dp[i][j-1])$| Reset to 0 | Reset to 0 |
| **Time Complexity** | **$O(M \cdot N)$ ⚡** | $O(M \cdot N)$ | $O(M \cdot N)$ |

---

## 14. How to Recognize This in Questions

* **"Find length of longest common subsequence between two strings"** $\rightarrow$ LeetCode 1143.
* **"Find longest palindromic subsequence in string S"** $\rightarrow$ LeetCode 516 ($\text{LCS}(S, S^R)$).

---

## 15. Frequently Asked Interview Questions

* **Q: How is Longest Palindromic Subsequence reduced to LCS?**  
  *A:* By reversing string $S$ to form $S^R$. The longest subsequence common to both $S$ and $S^R$ is guaranteed to read identically forwards and backwards, forming the LPS of $S$.

* **Q: How does 1D space compression work in LCS?**  
  *A:* By maintaining a 1D array $DP[N+1]$ and a single variable `prevDiag` holding $DP[i-1][j-1]$ before $DP[j]$ is overwritten.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: SUBSEQUENCE DP                                        |
+-----------------------------------------------------------------------+
| • LCS Recurrence : Match -> 1 + dp[i-1][j-1]; Mismatch -> max(top,left)|
| • LPS Reduction  : LPS(S) = LCS(S, Reverse(S)) ⚡                     |
| • SCS Formula    : SCS Length = |S1| + |S2| - LCS(S1, S2)             |
| • Space Opt      : 1D Array DP[N] using prevDiag for (i-1, j-1)         |
| • Performance    : O(M * N) Time | O(N) Auxiliary Space ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write LeetCode 1143 (`LCS`) with 1D space compression in Java.
- [ ] I can write LeetCode 516 (`LPS`) using reduction to $\text{LCS}(S, S^R)$.
- [ ] I can reconstruct the Shortest Common Supersequence string (LeetCode 1092).
- [ ] I can prove why SCS Length $= |S_1| + |S_2| - \text{LCS}(S_1, S_2)$.
- [ ] I can explain how `prevDiag` stores $DP[i-1][j-1]$ during 1D LCS space compression.
