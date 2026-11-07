# 09. String DP: Edit Distance, Wildcards, Regex Matching & Alignment State Graphs

## 1. Introduction
**String Dynamic Programming** is the algorithmic core of natural language processing, spell-checkers, version control diff engines (`git diff`), and search engine query autocompletion. Operating over two input strings $S_1$ (length $M$) and $S_2$ (length $N$), String DP evaluates state transitions across character insertions, deletions, replacements, and wildcards. The three foundational benchmarks of String DP are:
1. **Edit Distance / Levenshtein Distance (LeetCode 72)**: Finds minimum operations (Insert, Delete, Replace) to convert $S_1$ into $S_2$ ($DP[i][j] = 1 + \min(\text{Insert}, \text{Delete}, \text{Replace})$).
2. **Wildcard Matching (LeetCode 44)**: Matches pattern with `?` (any single char) and `*` (any sequence of 0+ chars).
3. **Regular Expression Matching (LeetCode 10)**: Matches pattern with `.` (any single char) and `*` (zero or more of the PRECEDING element).

String DP algorithms execute in **$O(M \cdot N)$ Time Complexity** and can be space-compressed to **$O(N)$ Auxiliary Space**.

> **Important:** Core Structural Invariants of String DP:
> 1. **Edit Distance 3-Choice Recurrence (LeetCode 72)**:
>    - If $S_1[i-1] == S_2[j-1]$: $DP[i][j] = DP[i-1][j-1]$ (No operation cost).
>    - If $S_1[i-1] \neq S_2[j-1]$:
>      $$DP[i][j] = 1 + \min\begin{cases} DP[i][j-1] & \text{(Insert into } S_1\text{)} \\ DP[i-1][j] & \text{(Delete from } S_1\text{)} \\ DP[i-1][j-1] & \text{(Replace in } S_1\text{)} \end{cases}$$
> 2. **Wildcard Matching '*' Invariant (LeetCode 44)**:
>    - $DP[i][j] = DP[i-1][j] \lor DP[i][j-1]$ (Match 1+ chars vs Match 0 chars).
> 3. **Regex Matching '*' Invariant (LeetCode 10)**:
>    - Match 0 instances of preceding char: $DP[i][j] = DP[i][j-2]$.
>    - Match 1+ instances of preceding char (if match): $DP[i][j] = DP[i-1][j]$. ⚡

```
Edit Distance 3-Choice State Transition Topology:

                    [ Top: Delete (i-1, j) ]
                               │
                               ▼
[ Left: Insert (i, j-1) ] ──► [ Target (i, j) ]
                               ▲
                               │
                [ Top-Left: Replace (i-1, j-1) ]

DP[i][j] = 1 + min( Insert, Delete, Replace ) ⚡
```

---

## 2. Core Concepts & String DP Strategy Matrix

### 2.1 String DP Benchmark Strategy Matrix
```
String DP Strategy Matrix:
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| Problem Archetype     | Pattern Tokens    | Match Condition   | Mismatch / '*' Recurrence| Space Complexity  |
+-----------------------+-------------------+-------------------+-------------------+-------------------+
| **Edit Distance (72)**| Plain Characters  | $DP[i-1][j-1]$    | $1 + \min(\text{Ins, Del, Rep})$| **$O(N)$ 1D Array ⚡**|
| **Wildcard Match (44)**| `?`, `*` (Any 0+) | $DP[i-1][j-1]$    | `*`: $DP[i-1][j] \lor DP[i][j-1]$| **$O(N)$ 1D Array ⚡**|
| **Regex Match (10)**  | `.`, `*` (Prec 0+)| $DP[i-1][j-1]$    | `*`: $DP[i][j-2] \lor DP[i-1][j]$| **$O(N)$ 1D Array ⚡**|
+-----------------------+-------------------+-------------------+-------------------+-------------------+
```

> **Memory Trick:** **"Edit Distance min choices = Ins(left), Del(top), Rep(diag); Wildcard * = match 0 (left) or 1+ (top); Regex * = 0 preceding (j-2) or 1+ (top)!"**

---

## 3. Characteristics & Mathematical Recurrence Formulations

### 3.1 Mathematical Derivation of LeetCode 10 (Regex Matching)
* Given string $S$ (length $M$) and pattern $P$ (length $N$) containing `.` and `*`.
* Let $DP[i][j]$ be boolean validity matching $S[0 \dots i-1]$ with $P[0 \dots j-1]$.
* **Case 1: Standard Match or `.`**:
  If $P[j-1] == S[i-1]$ or $P[j-1] == '.'$:
  $$DP[i][j] = DP[i-1][j-1]$$
* **Case 2: Pattern Contains `*` at $P[j-1]$**:
  Preceding pattern character is $P[j-2]$.
  - **Sub-case 2A: Match 0 instances of $P[j-2]$**:
    $$DP[i][j] = DP[i][j-2]$$
  - **Sub-case 2B: Match 1+ instances of $P[j-2]$**:
    If $S[i-1] == P[j-2]$ or $P[j-2] == '.'$:
    $$DP[i][j] = DP[i][j] \lor DP[i-1][j]$$
* Base Cases: $DP[0][0] = \text{true}$. For empty string $S$, $DP[0][j] = DP[0][j-2]$ if $P[j-1] == '*'$. ⚡

---

## 4. Internal Working Mechanics: Edit Distance State Grid Walkthrough

Tracing LeetCode 72 (Edit Distance) for $S_1 = \text{"horse"}$, $S_2 = \text{"ros"}$:

```
Matrix Layout (DP[i][j] = Min edits to make S1[0..i-1] equal S2[0..j-1]):

       ''   r   o   s
  '' [  0   1   2   3 ]
  h  [  1   1   2   3 ]  ──► 'h' != 'r': 1 + min(Ins:1, Del:1, Rep:0) = 1
  o  [  2   2   1   2 ]  ──► 'o' == 'o': Match! Take diag (1)
  r  [  3   2   2   2 ]  ──► 'r' == 'r': Match! Take diag (2)
  s  [  4   3   3   2 ]  ──► 's' == 's': Match! Take diag (2)
  e  [  5   4   4   3 ]  ──► 'e' != 's': 1 + min(Ins:3, Del:2, Rep:3) = 3!

Final Min Edit Distance = 3! (horse -> rorse -> rose -> ros) ✅ ⚡
```

---

## 5. Visual Diagram: Regular Expression '*' Decision Branching

```
Regex '*' Token Decision Tree (Pattern P[j-1] = '*'):

                        [ Regex State (i, j) ]
                              /        \
                             /          \
     (Match 0 Instances)    /            \    (Match 1+ Instances)
                           /              \    [Requires S[i-1] == P[j-2]]
                          ▼                ▼
                [ Check State (i, j-2) ]  [ Check State (i-1, j) ] ⚡
```

---

## 6. Operations & Complete Java Implementation

Below is a production-grade Java suite implementing Edit Distance (LeetCode 72), Wildcard Matching (LeetCode 44), Regular Expression Matching (LeetCode 10), and 1D Space Compression.

```java
import java.util.*;

/**
 * Production-Grade Master Suite Implementing String DP Algorithms:
 * Edit Distance, Wildcard Matching, Regex Matching, and 1D Space Compression.
 */
public class StringDPProblemsMaster {

    // =========================================================================
    // 1. LEETCODE 72: EDIT DISTANCE (O(M * N) Time, O(N) 1D Space)
    // =========================================================================
    /**
     * Calculates minimum edit operations (Insert, Delete, Replace) to transform word1 to word2.
     *
     * @param word1 source string
     * @param word2 target string
     * @return minimum operations count
     */
    public int minDistance(String word1, String word2) {
        if (word1 == null || word2 == null) return 0;

        int m = word1.length();
        int n = word2.length();

        int[] dp = new int[n + 1];

        // Base case: word1 is empty -> require j insertions
        for (int j = 0; j <= n; j++) dp[j] = j;

        for (int i = 1; i <= m; i++) {
            int prevDiag = dp[0]; // Holds dp[i-1][0]
            dp[0] = i;           // First column base case (i deletions)

            for (int j = 1; j <= n; j++) {
                int temp = dp[j]; // Save dp[i-1][j] for next column's prevDiag

                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[j] = prevDiag; // Character match! No edit cost ⚡
                } else {
                    int insertCost = dp[j - 1]; // Left
                    int deleteCost = dp[j];     // Top
                    int replaceCost = prevDiag; // Top-Left

                    dp[j] = 1 + Math.min(replaceCost, Math.min(insertCost, deleteCost));
                }

                prevDiag = temp; // Shift prevDiag
            }
        }

        return dp[n];
    }

    // =========================================================================
    // 2. LEETCODE 44: WILDCARD MATCHING (O(M * N) Time, O(N) Space)
    // =========================================================================
    /**
     * Matches string s against pattern p containing '?' and '*'.
     */
    public boolean isMatchWildcard(String s, String p) {
        if (s == null || p == null) return false;

        int m = s.length();
        int n = p.length();

        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;

        // Base case: pattern containing '*' can match empty string
        for (int j = 1; j <= n; j++) {
            if (p.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 1];
            }
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char pChar = p.charAt(j - 1);

                if (pChar == '?' || pChar == s.charAt(i - 1)) {
                    dp[i][j] = dp[i - 1][j - 1]; // Match single char
                } else if (pChar == '*') {
                    dp[i][j] = dp[i - 1][j] || dp[i][j - 1]; // Match 1+ vs Match 0 ⚡
                }
            }
        }

        return dp[m][n];
    }

    // =========================================================================
    // 3. LEETCODE 10: REGULAR EXPRESSION MATCHING (O(M * N) Time, O(N) Space)
    // =========================================================================
    /**
     * Matches string s against pattern p containing '.' and '*'.
     */
    public boolean isMatchRegex(String s, String p) {
        if (s == null || p == null) return false;

        int m = s.length();
        int n = p.length();

        boolean[][] dp = new boolean[m + 1][n + 1];
        dp[0][0] = true;

        // Base case: Empty string matching pattern with '*'
        for (int j = 2; j <= n; j++) {
            if (p.charAt(j - 1) == '*') {
                dp[0][j] = dp[0][j - 2];
            }
        }

        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                char pChar = p.charAt(j - 1);

                if (pChar == '.' || pChar == s.charAt(i - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else if (pChar == '*') {
                    // Option A: Match 0 instances of preceding char
                    dp[i][j] = dp[i][j - 2];

                    // Option B: Match 1+ instances of preceding char (if match)
                    char prevPatternChar = p.charAt(j - 2);
                    if (prevPatternChar == '.' || prevPatternChar == s.charAt(i - 1)) {
                        dp[i][j] = dp[i][j] || dp[i - 1][j]; // ⚡
                    }
                }
            }
        }

        return dp[m][n];
    }
}
```

> **Quick Syntax:**
```java
// Edit Distance 3-Choice State Line
dp[j] = 1 + Math.min(prevDiag, Math.min(dp[j - 1], dp[j])); // Replace, Insert, Delete
```

---

## 7. Concrete Problem Examples & Applications

1. **LeetCode 72 - Edit Distance**:
   - Primary spell-checking and DNA alignment benchmark ($O(M \cdot N)$ time, $O(N)$ space).

2. **LeetCode 44 - Wildcard Matching**:
   - File glob matching (`*.txt`, `image?.png`) solved in $O(M \cdot N)$ time.

3. **LeetCode 10 - Regular Expression Matching**:
   - Compiler lexer and regex engine execution solved in $O(M \cdot N)$ time.

---

## 8. Java Code Demonstration & Execution Suite

```java
public class StringDPProblemsDemo {

    public static void main(String[] args) {
        System.out.println("=================================================");
        System.out.println("   STRING DYNAMIC PROGRAMMING BENCHMARK DEMO     ");
        System.out.println("=================================================\n");

        StringDPProblemsMaster master = new StringDPProblemsMaster();

        // 1. Edit Distance Test (LeetCode 72)
        String w1 = "horse", w2 = "ros";
        int edits = master.minDistance(w1, w2);
        System.out.println("1. LeetCode 72 Edit Distance for \"" + w1 + "\" -> \"" + w2 + "\":");
        System.out.println("   Minimum Edit Operations (1D Space): " + edits + " Operations (Optimal = 3)");
        System.out.println("-------------------------------------------------");

        // 2. Wildcard Matching Test (LeetCode 44)
        String s1 = "adceb", p1 = "*a*b";
        boolean matchWild = master.isMatchWildcard(s1, p1);
        System.out.println("2. LeetCode 44 Wildcard Matching for \"" + s1 + "\" vs \"" + p1 + "\":");
        System.out.println("   Is Match: " + matchWild + " (Optimal)");
        System.out.println("-------------------------------------------------");

        // 3. Regex Matching Test (LeetCode 10)
        String s2 = "aab", p2 = "c*a*b";
        boolean matchRegex = master.isMatchRegex(s2, p2);
        System.out.println("3. LeetCode 10 Regex Matching for \"" + s2 + "\" vs \"" + p2 + "\":");
        System.out.println("   Is Match: " + matchRegex + " (Optimal)");
        System.out.println("=================================================");
    }
}
```

---

## 9. Complexity Analysis Table

| String DP Problem | Time Complexity | Auxiliary Space | Key Factor |
| :--- | :--- | :--- | :--- |
| **Edit Distance (LC 72)**| $\mathbf{O(M \cdot N)}$ ⚡| $\mathbf{O(N)}$ 1D Array ⚡| `1 + min(Ins, Del, Rep)` |
| **Wildcard Match (LC 44)**| $\mathbf{O(M \cdot N)}$ ⚡| $O(M \cdot N)$ Table | `*` matches 0+ chars |
| **Regex Match (LC 10)**  | $\mathbf{O(M \cdot N)}$ ⚡| $O(M \cdot N)$ Table | `*` matches 0+ preceding char |

---

## 10. Edge Cases & Boundary Handling

1. **Empty Pattern or Empty String**:
   - Base case checks `dp[0][0] = true` handle empty inputs cleanly.

2. **Multiple Consecutives Stars (`"a***b"`)**:
   - Handled smoothly in Wildcard base case loop.

---

## 11. Common Mistakes & Anti-Patterns

* **Anti-Pattern 1: Confusing Wildcard '*' (LeetCode 44) with Regex '*' (LeetCode 10)**:
  - Wildcard `*` matches ANY sequence of 0+ characters ($DP[i-1][j] \lor DP[i][j-1]$).
  - Regex `*` matches 0 or more of the PRECEDING character ($DP[i][j-2] \lor DP[i-1][j]$). **Do not interchange them!**

---

## 12. Important Notes & Architectural Rules

> **Interview Requirement:** Distinction Between Wildcard and Regex '*':
> * **Wildcard '*'**: Standalone wildcard matching ANY sequence.
> * **Regex '*'**: Postfix modifier acting on the PRECEDING character $P[j-2]$. Requires checking $DP[i][j-2]$ for 0 matches! ⚡

---

## 13. System & Implementation Comparisons

| Metric / Dimension | Wildcard Matching (LC 44) | Regex Matching (LC 10) |
| :--- | :--- | :--- |
| **Token Action** | Independent token `*` | Modifies preceding token `P[j-2]` |
| **Match 0 Option** | Check left cell $DP[i][j-1]$ | Check 2 cells left $DP[i][j-2]$ |
| **Space Complexity** | **$O(N)$ 1D Array ⚡** | $O(M \cdot N)$ Table |

---

## 14. How to Recognize This in Questions

* **"Find minimum insertions, deletions, replacements to convert word1 into word2"** $\rightarrow$ LeetCode 72.
* **"Match string against pattern with '.' and '*'"** $\rightarrow$ LeetCode 10 (Regex DP).

---

## 15. Frequently Asked Interview Questions

* **Q: What are the three choices in Edit Distance when characters mismatch?**  
  *A:* (1) Insert into $S_1$ ($DP[i][j-1]$), (2) Delete from $S_1$ ($DP[i-1][j]$), (3) Replace in $S_1$ ($DP[i-1][j-1]$). Take $1 + \min$ of these three choices.

* **Q: How does Regex '*' handle 0 instances of the preceding character?**  
  *A:* By referencing $DP[i][j-2]$, which effectively skips the preceding character and the `*` token entirely.

---

## 16. Quick Revision Box

```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING DP PROBLEMS                                    |
+-----------------------------------------------------------------------+
| • Edit Distance: Match -> dp[i-1][j-1]; Mismatch -> 1 + min(Ins,Del,Rep)|
| • Wildcard '*' : dp[i][j] = dp[i-1][j] || dp[i][j-1]                   |
| • Regex '*'    : dp[i][j] = dp[i][j-2] || (match ? dp[i-1][j] : false)  |
| • Performance  : O(M * N) Time | O(N) Auxiliary Space ⚡              |
+-----------------------------------------------------------------------+
```

---

## 17. Practice Checklist

- [ ] I can write Edit Distance (LeetCode 72) with 1D space compression in Java.
- [ ] I can write Wildcard Matching (LeetCode 44) in Java.
- [ ] I can write Regular Expression Matching (LeetCode 10) in Java.
- [ ] I can explain the difference between Wildcard `*` and Regex `*`.
- [ ] I can state the 3 Edit Distance subproblem choices.
