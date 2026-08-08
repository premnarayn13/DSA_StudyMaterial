# 12. String Transformation & Edit Distance

## 1. Introduction
String transformation algorithms determine the minimum number of edit operations (insertions, deletions, substitutions) required to transform a source string $S_1$ into a target string $S_2$. In technical coding interviews, **Edit Distance** (LeetCode 72 - Levenshtein Distance) and **One Edit Distance** (LeetCode 161) evaluate dynamic programming state transitions, two-pointer boundary checks, and recursive subproblem optimization.

> **Important:** If the difference in lengths between $S_1$ and $S_2$ is greater than 1 ($||S_1| - |S_2|| > 1$), it is IMPOSSIBLE for $S_1$ and $S_2$ to be One Edit Distance apart!

## 2. Core Concepts
* **Levenshtein Distance Operations**:
  1. **Insert** a character: $DP[i][j-1] + 1$
  2. **Delete** a character: $DP[i-1][j] + 1$
  3. **Replace** a character: $DP[i-1][j-1] + 1$
* **DP Recurrence Relation**:
  $$\text{dp}[i][j] = \begin{cases} \text{dp}[i-1][j-1] & \text{if } S_1[i-1] == S_2[j-1] \\ 1 + \min(\text{dp}[i-1][j], \text{dp}[i][j-1], \text{dp}[i-1][j-1]) & \text{otherwise} \end{cases}$$
* **One Edit Distance Two-Pointer Strategy**: Scanning $S_1$ and $S_2$ using two pointers `i` and `j` in $O(N)$ time and $O(1)$ space.

> **Memory Trick:** **"Same char? Copy diagonal dp[i-1][j-1]! Different char? 1 + min(Insert, Delete, Replace)"**.

## 3. Characteristics / Properties
* **DP Space Optimization**: Standard Edit Distance uses $O(M \cdot N)$ 2D DP matrix. Space can be optimized to **$O(\min(M, N))$** using two 1D rows (`prev` and `curr`).
* **One Edit Distance $O(N)$ Optimization**: Checking if two strings differ by at most 1 edit does NOT require 2D DP! It can be solved in a single pass using Two Pointers in $O(N)$ time and $O(1)$ space.

```
String Transformation Complexity Matrix:
+-----------------------+-------------------+-------------------+-------------------+
| Problem / Algorithm   | Time Complexity   | Space Complexity  | Best Technique    |
+-----------------------+-------------------+-------------------+-------------------+
| One Edit Distance     | O(N) Linear       | O(1) Constant     | Two Pointers ⚡   |
| Edit Distance (2D DP) | O(M * N)          | O(M * N)          | 2D DP Matrix      |
| Edit Distance (1D DP) | O(M * N)          | O(min(M, N))      | 2-Row DP Vector ⚡ |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Edit Distance (Levenshtein) for $S_1 =$ `"horse"`, $S_2 =$ `"ros"` ($M = 5, N = 3$):

```
DP Table Construction (dp[i][j]):
      ""   r   o   s
""     0   1   2   3
h      1   1   2   3
o      2   2   1   2
r      3   2   2   2
s      4   3   3   2
e      5   4   3   3

Step-by-Step Transition at dp[5][3] (e vs s):
- Mismatch 'e' != 's' -> 1 + min(dp[4][3]=2, dp[5][2]=3, dp[4][2]=3) = 1 + 2 = 3

Minimum Edit Operations = 3 ✅ ("horse" -> "rorse" -> "rose" -> "ros")
```

## 5. Visual Diagram
DP Decision State Choices (Insert, Delete, Replace):

```
                     dp[i-1][j-1] (Replace S1[i-1] -> S2[j-1])
                         |
                         v
dp[i-1][j] (Delete S1[i-1]) ---> [ dp[i][j] ] <--- dp[i][j-1] (Insert S2[j-1])
```

## 6. Operations / Algorithms
LeetCode 72 Edit Distance Master Implementation:

```java
public int minDistance(String word1, String word2) {
    int M = word1.length();
    int N = word2.length();

    int[][] dp = new int[M + 1][N + 1];

    // Base cases: Empty string transformations
    for (int i = 0; i <= M; i++) dp[i][0] = i; // Deletions
    for (int j = 0; j <= N; j++) dp[0][j] = j; // Insertions

    // Fill DP table
    for (int i = 1; i <= M; i++) {
        for (int j = 1; j <= N; j++) {
            if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                dp[i][j] = dp[i - 1][j - 1]; // No edit cost
            } else {
                dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], // Replace
                               Math.min(dp[i - 1][j],     // Delete
                                        dp[i][j - 1]));    // Insert
            }
        }
    }

    return dp[M][N];
}
```

> **Quick Syntax:**
```java
// Space-Optimized 1D Edit Distance (O(min(M,N)) space)
int[] dp = new int[N + 1];
for (int j = 0; j <= N; j++) dp[j] = j;
```

## 7. Examples
* **LeetCode 72 - Edit Distance**: Finding minimum edits to convert `word1` to `word2`.
* **LeetCode 161 - One Edit Distance**: Checking if two strings are exactly 1 edit apart in $O(N)$ time and $O(1)$ space.
* **LeetCode 583 - Delete Operation for Two Strings**: Finding min deletions using LCS (Longest Common Subsequence).

## 8. Java Code
Complete interview-ready Java suite implementing 2D Edit Distance, Space-Optimized 1D Edit Distance, and One Edit Distance:

```java
public class StringTransformationMaster {

    // 1. Edit Distance (LeetCode 72) 2D DP O(M * N) Time, O(M * N) Space
    public static int minDistance(String word1, String word2) {
        if (word1 == null || word2 == null) return 0;
        int M = word1.length(), N = word2.length();

        int[][] dp = new int[M + 1][N + 1];

        for (int i = 0; i <= M; i++) dp[i][0] = i;
        for (int j = 0; j <= N; j++) dp[0][j] = j;

        for (int i = 1; i <= M; i++) {
            for (int j = 1; j <= N; j++) {
                if (word1.charAt(i - 1) == word2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j - 1], 
                                   Math.min(dp[i - 1][j], dp[i][j - 1]));
                }
            }
        }

        return dp[M][N];
    }

    // 2. One Edit Distance (LeetCode 161) O(N) Time, O(1) Space
    public static boolean isOneEditDistance(String s, String t) {
        int M = s.length();
        int N = t.length();

        if (Math.abs(M - N) > 1) return false;

        for (int i = 0; i < Math.min(M, N); i++) {
            if (s.charAt(i) != t.charAt(i)) {
                if (M == N) {
                    // Replace case: Remainder of both strings must match
                    return s.substring(i + 1).equals(t.substring(i + 1));
                } else if (M < N) {
                    // Insert into s (or Delete from t): s[i..] must match t[i+1..]
                    return s.substring(i).equals(t.substring(i + 1));
                } else {
                    // Delete from s: s[i+1..] must match t[i..]
                    return s.substring(i + 1).equals(t.substring(i));
                }
            }
        }

        // If no mismatches found in loop, check if lengths differ by exactly 1
        return Math.abs(M - N) == 1;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        // Test Edit Distance
        System.out.println("Edit Distance ('horse', 'ros'): " + minDistance("horse", "ros")); // Output: 3
        System.out.println("Edit Distance ('intention', 'execution'): " + minDistance("intention", "execution")); // Output: 5

        // Test One Edit Distance
        System.out.println("Is One Edit ('ab', 'acb')? " + isOneEditDistance("ab", "acb")); // true
        System.out.println("Is One Edit ('cab', 'ad')? "  + isOneEditDistance("cab", "ad"));  // false
    }
}
```

## 9. Complexity Analysis
| Algorithm | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Standard 2D Edit Distance**| $O(M \cdot N)$ | $O(M \cdot N)$ | Standard DP matrix |
| **Space-Optimized Edit Distance**| $O(M \cdot N)$ | **$O(\min(M, N))$** | Uses 2 1D DP rows |
| **One Edit Distance** | **$O(N)$ Linear** | **$O(1)$ Constant** | Single pass comparison |

## 10. Edge Cases
* **Length Difference $> 1$ in One Edit Distance**: Immediately return `false` in $O(1)$ time.
* **Identical Strings**: `s.equals(t)` in One Edit Distance returns `false` (requires EXACTLY 1 edit, not 0 edits!).
* **One String Empty (`""`)**: Min edits equals length of non-empty string.

## 11. Common Mistakes
* Using 2D DP for One Edit Distance instead of the optimal $O(N)$ Two-Pointer algorithm.
* Forgetting to initialize DP base cases (`dp[i][0] = i` and `dp[0][j] = j`).
* Off-by-one errors in character indexing (`word1.charAt(i - 1)` vs `dp[i][j]`).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Never use 2D Dynamic Programming for One Edit Distance (LeetCode 161)!
> DP takes $O(N^2)$ time/space, whereas Two-Pointers solves it in **$O(N)$ time and $O(1)$ space**.

> **Memory Trick:** **"Edit Distance Base Cases: Empty string requires i deletions or j insertions!"**

## 13. Comparisons
| Feature | One Edit Distance (LeetCode 161) | Full Edit Distance (LeetCode 72) |
| :--- | :--- | :--- |
| **Target Answer** | Boolean (`true`/`false`) | Minimum integer edit count |
| **Allowed Edits** | Strictly 1 Edit | $0 \dots \max(M, N)$ Edits |
| **Time Complexity** | **$O(N)$ Linear** | $O(M \cdot N)$ Quadratic |
| **Space Complexity**| **$O(1)$ Constant** | $O(M \cdot N)$ or $O(\min(M,N))$ |

## 14. How to Recognize This in Questions
* **"Find minimum insertions, deletions, and replacements to convert S1 to S2"** $\rightarrow$ 2D Edit Distance DP.
* **"Check if two strings differ by at most 1 edit operation"** $\rightarrow$ One Edit Distance ($O(N)$ time).

## 15. Frequently Asked Interview Questions
* **Q: How can 2D Edit Distance space complexity be optimized to $O(\min(M, N))$?**  
  *A:* Because `dp[i][j]` only depends on values from the current row `dp[i]` and previous row `dp[i-1]`, we can maintain just two 1D DP arrays (`prev` and `curr`) of length $\min(M, N) + 1$, swapping references after each row iteration.
* **Q: How does One Edit Distance achieve $O(N)$ time and $O(1)$ space?**  
  *A:* On the first mismatch character at index `i`, we test 3 cases: (1) Replace (`s.substring(i+1) == t.substring(i+1)`), (2) Insert (`s.substring(i) == t.substring(i+1)`), or (3) Delete (`s.substring(i+1) == t.substring(i)`). If the remaining substrings match, return `true`; else `false`.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: STRING TRANSFORMATION & EDIT DISTANCE                |
+-----------------------------------------------------------------------+
| • Recurrence: if S1[i-1]==S2[j-1] dp[i][j] = dp[i-1][j-1]             |
|   else dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])       |
| • Operations: dp[i-1][j-1]=Replace, dp[i-1][j]=Delete, dp[i][j-1]=Insert|
| • One Edit Distance: Length diff > 1 => false; Single mismatch pass O(N)|
| • Base Cases: dp[i][0] = i (deletions), dp[0][j] = j (insertions)     |
| • Space Optimization: 2-Row DP Vector reduces space to O(min(M, N))   |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the 3-term DP recurrence formula for Edit Distance.
- [ ] I can initialize base cases (`dp[i][0]` and `dp[0][j]`).
- [ ] I can optimize 2D DP matrix to $O(\min(M, N))$ 1D space.
- [ ] I can implement One Edit Distance in $O(N)$ time and $O(1)$ space.
- [ ] I can solve LeetCode 72 (Edit Distance) from memory.
