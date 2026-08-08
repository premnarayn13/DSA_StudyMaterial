# 08. Z-Algorithm for Pattern Matching

## 1. Introduction
The **Z-Algorithm** is a powerful string-processing algorithm that constructs a **Z-Array** in **$O(N)$ linear time and space**. For a string $S$ of length $N$, the entry `Z[i]` stores the length of the longest substring starting at index `i` that is also a **prefix** of $S$. By constructing a concatenated string $S = P + \text{"\$"} + T$, the Z-Algorithm finds all occurrences of pattern $P$ in text $T$ in $O(N + M)$ time.

> **Important:** The Z-Algorithm maintains a **Z-Box $[L, R]$** representing the rightmost substring matching a prefix of $S$ found so far. The Z-Box enables computing `Z[i]` in $O(1)$ time for most indices!

## 2. Core Concepts
* **Z-Array (`Z[i]`)**: For a string $S$, `Z[i]` is the length of the longest common prefix between $S$ and the suffix of $S$ starting at index `i` (with `Z[0] = 0` by convention).
* **Z-Box ($[L, R]$)**: The interval $[L, R]$ defining the substring starting at $L$ and ending at $R$ that matches a prefix of $S$ (where $R$ is maximized).
* **Pattern Matching Setup**: To search for pattern $P$ of length $M$ in text $T$ of length $N$:
  1. Construct concatenated string $S = P + \text{"\$"} + T$ (where `$` is a unique delimiter not present in $P$ or $T$).
  2. Compute Z-array for $S$.
  3. Any index `i` where **`Z[i] == M`** represents a valid match starting at text index `i - M - 1`!

> **Memory Trick:** **"Concatenate P + '$' + T. Wherever Z[i] == M, a full pattern match occurs!"**

## 3. Characteristics / Properties
* **Linear Time Guarantee**: Like KMP, the Z-Algorithm runs in strict $O(N + M)$ linear time because the right boundary $R$ of the Z-Box strictly increases from $0$ to $N+M$.
* **Delimiter Role**: The unique delimiter `$` limits `Z[i]` values from exceeding pattern length $M$, preventing cross-boundary pattern matching.

```
Pattern Matching Comparison: KMP vs Z-Algorithm:
+-----------------------+-------------------+-------------------+-------------------+
| Feature               | KMP Algorithm     | Z-Algorithm       | Comparison        |
+-----------------------+-------------------+-------------------+-------------------+
| Precomputation Table  | LPS Array (O(M))  | Z-Array (O(N+M))  | Z-Array is larger |
| Concatenated String   | Not required      | Uses `P + '$' + T`| Simple syntax     |
| Exact Matches Rule    | `j == M`          | `Z[i] == M`       | Ultra-clean check |
| Complexity            | O(N + M)          | O(N + M)          | Both Linear ⚡     |
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Z-Array for $S =$ `"aab$baabaa"` ($P =$ `"aab"`, $T =$ `"baabaa"`):

```
Index:    0  1  2  3  4  5  6  7  8
Char:     a  a  b  $  b  a  a  b  a  a
Z-Val:   [0, 1, 0, 0, 0, 1, 3, 1, 1]

Step-by-step Z-Array Calculation:
i = 0: Z[0] = 0 (by convention)
i = 1: S[1] 'a' == S[0] 'a', S[2] 'b' != S[1] 'a' -> Z[1] = 1. Z-Box [L=1, R=1]
i = 2: S[2] 'b' != S[0] 'a' -> Z[2] = 0
i = 3: S[3] '$' != S[0] 'a' -> Z[3] = 0
i = 4: S[4] 'b' != S[0] 'a' -> Z[4] = 0
i = 5: S[5] 'a' == S[0] 'a', S[6] 'a' != S[1] 'a' -> Z[5] = 1. Z-Box [L=5, R=5]
i = 6: S[6..8] "aab" == S[0..2] "aab" -> Z[6] = 3! 🎉 (Z[6] == M (3) => MATCH AT TEXT INDEX 6 - 3 - 1 = 2!)
```

## 5. Visual Diagram
Z-Box $[L, R]$ Reuse Mechanics:

```
String S:   a  b  c  x  a  b  c  z  a  b  c  x  a  b  c  y
Index:      0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
                                    ^
                                  i=8 inside Z-Box [L=4, R=14]

Inside Z-Box: i = 8 sits between L=4 and R=14.
Equivalent Prefix Index: k = i - L = 8 - 4 = 4.
Reuse Z[k] (Z[4]) to set initial Z[8] value without re-comparing characters from scratch! ⚡
```

## 6. Operations / Algorithms
Z-Algorithm Master Implementation:

```java
public class ZAlgorithm {

    // 1. Compute Z-Array for string S in O(N) Time
    public static int[] calculateZ(String s) {
        int n = s.length();
        int[] Z = new int[n];
        int L = 0, R = 0;

        for (int i = 1; i < n; i++) {
            if (i > R) {
                // i is outside current Z-box -> Expand Z-box from scratch
                L = R = i;
                while (R < n && s.charAt(R - L) == s.charAt(R)) {
                    R++;
                }
                Z[i] = R - L;
                R--;
            } else {
                // i is inside current Z-box [L, R]
                int k = i - L;
                // Case A: Z[k] stays strictly inside Z-box
                if (Z[k] < R - i + 1) {
                    Z[i] = Z[k];
                } else {
                    // Case B: Z[k] extends beyond Z-box -> Touch & Expand
                    L = i;
                    while (R < n && s.charAt(R - L) == s.charAt(R)) {
                        R++;
                    }
                    Z[i] = R - L;
                    R--;
                }
            }
        }
        return Z;
    }

    // 2. Search Pattern P in Text T using Z-Algorithm
    public static List<Integer> search(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (pattern.length() == 0 || text.length() < pattern.length()) return matches;

        // Construct concatenated string: P + "$" + T
        String concat = pattern + "$" + text;
        int[] Z = calculateZ(concat);
        int M = pattern.length();

        // Scan Z-array for entries equal to M
        for (int i = M + 1; i < concat.length(); i++) {
            if (Z[i] == M) {
                matches.add(i - M - 1); // Text index offset
            }
        }
        return matches;
    }
}
```

> **Quick Syntax:**
```java
// Match Condition in Z-Algorithm
String concat = pattern + "$" + text;
int[] Z = calculateZ(concat);
if (Z[i] == pattern.length()) {
    int textIndex = i - pattern.length() - 1;
}
```

## 7. Examples
* **LeetCode 28 - Find the Index of the First Occurrence in a String**: Optimal Z-Algorithm solution.
* **Longest Palindromic Prefix**: Using Z-Algorithm on `S + "$" + reverse(S)`.
* **String Compression / Periodicity**: Finding prefix-suffix overlaps.

## 8. Java Code
Complete interview-ready Java suite implementing Z-Array calculation, Substring Search, and Dry Run demonstrations:

```java
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class ZAlgorithmMaster {

    // Calculate Z-Array O(N) Time, O(N) Space
    public static int[] calculateZ(String s) {
        if (s == null) return new int[0];
        int n = s.length();
        int[] Z = new int[n];
        int L = 0, R = 0;

        for (int i = 1; i < n; i++) {
            if (i > R) {
                L = R = i;
                while (R < n && s.charAt(R - L) == s.charAt(R)) {
                    R++;
                }
                Z[i] = R - L;
                R--;
            } else {
                int k = i - L;
                if (Z[k] < R - i + 1) {
                    Z[i] = Z[k];
                } else {
                    L = i;
                    while (R < n && s.charAt(R - L) == s.charAt(R)) {
                        R++;
                    }
                    Z[i] = R - L;
                    R--;
                }
            }
        }

        return Z;
    }

    // Pattern Search using Z-Algorithm O(N + M) Time
    public static List<Integer> searchPattern(String text, String pattern) {
        List<Integer> matches = new ArrayList<>();
        if (text == null || pattern == null) return matches;
        int N = text.length(), M = pattern.length();

        if (M == 0 || M > N) return matches;

        // Concatenate Pattern + Delimiter + Text
        String concat = pattern + "$" + text;
        int[] Z = calculateZ(concat);

        // Find all indices where Z[i] == M
        for (int i = M + 1; i < concat.length(); i++) {
            if (Z[i] == M) {
                matches.add(i - M - 1);
            }
        }

        return matches;
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String text = "baabaa";
        String pattern = "aab";

        System.out.println("Text: " + text);
        System.out.println("Pattern: " + pattern);

        String concat = pattern + "$" + text;
        int[] Z = calculateZ(concat);
        System.out.println("Concatenated String: " + concat);
        System.out.println("Z-Array: " + Arrays.toString(Z));

        List<Integer> matches = searchPattern(text, pattern);
        System.out.println("Pattern Match Text Indices: " + matches); // Output: [1]
    }
}
```

## 9. Complexity Analysis
| Phase | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **Z-Array Construction** | **$O(N + M)$** | **$O(N + M)$** | $R$ boundary moves strictly forward |
| **Pattern Search Pass** | **$O(N + M)$** | $O(1)$ auxiliary | Scans Z-array for values equal to $M$ |
| **Total Z-Algorithm** | **$O(N + M)$** | **$O(N + M)$** | Guaranteed linear runtime ⚡ |

## 10. Edge Cases
* **Delimiter Selection**: The delimiter character (e.g., `$`) MUST NOT appear in either pattern $P$ or text $T$. If `$` can appear in text, use ASCII `\0` or `\u0000`.
* **Pattern Length $M > N$**: Returns empty list immediately.
* **`Z[0]` Convention**: `Z[0]` is set to `0` by convention because prefix comparison starting at index 0 against itself is trivial ($N$).

## 11. Common Mistakes
* Choosing a delimiter character that exists inside text $T$ (allows `Z[i]` to cross the delimiter boundary, corrupting match lengths!).
* Forgetting `R--` after the while loop expansion in `calculateZ` (causes $R$ pointer off-by-one errors).
* Confusing `Z[i]` (stores prefix matches starting at `i`) with KMP `LPS[i]` (stores prefix-suffix matches ending at `i`).

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why does Z-Algorithm require a special delimiter (like `$`)?
> The delimiter prevents `Z[i]` from matching past the pattern boundary into the text! Without `$`, `Z[i]` could count matching characters extending into text $T$, exceeding pattern length $M$.

> **Memory Trick:** **"Concat P + '$' + T -> Z[i] == M means Match!"**

## 13. Comparisons
| Metric | Z-Algorithm | KMP Algorithm |
| :--- | :--- | :--- |
| **Concatenation Pattern** | `P + "$" + T` | Not required |
| **Matching Logic** | Simple `Z[i] == M` check | Dual pointer jump `j = lps[j-1]` |
| **Auxiliary Space** | $O(N + M)$ (Stores full Z-array) | **$O(M)$ (Stores pattern LPS array only)** |
| **Implementation** | Easy to remember Z-box | Slightly more complex pointer jumps |

## 14. How to Recognize This in Questions
* **"Find all occurrences of pattern P in text T using Z-array"** $\rightarrow$ Z-Algorithm ($O(N + M)$).
* **"Find longest palindromic prefix"** $\rightarrow$ Z-Algorithm on `S + "$" + reverse(S)`.

## 15. Frequently Asked Interview Questions
* **Q: Why is Z-Algorithm $O(N)$ time despite having a nested while loop inside?**  
  *A:* Because in each iteration of the inner while loop, the right boundary $R$ of the Z-Box increases by at least 1. Since $R$ can increase at most $N$ times, the inner loop executes at most $N$ total times across all iterations $\implies O(N)$ time overall.
* **Q: What is the main difference between KMP's LPS array and Z-Array?**  
  *A:* KMP's `LPS[i]` stores the longest prefix-suffix length for prefix ending at index $i$. Z-Array's `Z[i]` stores the longest prefix match for suffix starting at index $i$.

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: Z-ALGORITHM FOR PATTERN MATCHING                      |
+-----------------------------------------------------------------------+
| • Pattern Setup: Concatenate S = P + "$" + T                          |
| • Z[i] Definition: Length of longest substring starting at i = prefix |
| • Z-Box [L, R]: Maintains rightmost matching prefix window            |
| • Match Condition: Z[i] == pattern.length() => Match at (i - M - 1)   |
| • Complexity: O(N + M) Time | O(N + M) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can define what `Z[i]` represents in a string.
- [ ] I can construct a Z-array by hand for a short string.
- [ ] I know why a unique delimiter `$` is mandatory in `P + "$" + T`.
- [ ] I can implement Z-Algorithm search in under 5 minutes.
- [ ] I can compare space complexities between KMP ($O(M)$) and Z-Algorithm ($O(N+M)$).
