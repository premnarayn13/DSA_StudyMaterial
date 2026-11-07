# 10. Manacher's Algorithm for Longest Palindromic Substring

## 1. Introduction
**Manacher's Algorithm** is an advanced string algorithm that finds the Longest Palindromic Substring in **strict $O(N)$ linear time and $O(N)$ auxiliary space**. While standard center expansion requires $O(N^2)$ time, Manacher's Algorithm achieves $O(N)$ linear time by maintaining a **Center ($C$) and Right Boundary ($R$)** of the furthest right palindrome found so far. It uses palindromic symmetry to reuse previously computed palindrome radii in $O(1)$ time per character.

> **Important:** Manacher's Algorithm transforms any input string by inserting dummy delimiter characters (e.g., `#`) between characters: `"aba"` $\to$ `"^#a#b#a#$"`. This unifies odd and even palindromes into odd-length palindromes!

## 2. Core Concepts
* **Transformed String Format**: Surrounding every character with `#` and placing unique start/end markers (`^` and `$`) converts a string of length $N$ into a string of length $2N + 3$, making ALL palindromes odd-length!
  $$\text{Original: } \text{"aba"} \implies \text{Transformed: } \text{"\^\#a\#b\#a\#\$"}$$
* **Palindrome Radius Array `P[i]`**: Stores the radius (number of characters from center `i` to boundary) of the longest palindrome centered at index `i`.
* **Mirror Index `i_mirror`**: For current center `C` and candidate index `i`, the symmetric mirror index across `C` is:
  $$i_{\text{mirror}} = 2 \cdot C - i$$
* **Symmetry Optimization**: If $i < R$, initial radius `P[i]` is bounded by symmetry:
  $$P[i] = \min(R - i, P[i_{\text{mirror}}])$$

> **Memory Trick:** **"i_mirror = 2*C - i. If i < R, P[i] = Math.min(R - i, P[i_mirror])"**.

## 3. Characteristics / Properties
* **Linear Time Guarantee**: Like KMP and Z-Algorithm, Manacher's Algorithm runs in strict $O(N)$ time because the right boundary pointer $R$ increases monotonically from $0$ to $2N+3$.
* **Radius Property**: The radius `P[i]` in the transformed string equals the **exact length** of the original palindromic substring in the un-transformed string!

```
Manacher's Algorithm Performance Spectrum:
+-----------------------+-------------------+-------------------+-------------------+
| Algorithm / Strategy  | Time Complexity   | Auxiliary Space   | Key Mechanism     |
+-----------------------+-------------------+-------------------+-------------------+
| 2D Dynamic Programming| O(N²)             | O(N²)             | DP Table          |
| Expand Around Center  | O(N²)             | O(1)              | 2N - 1 Centers    |
| Manacher's Algorithm  | O(N) Linear       | O(N) Space        | Mirror Symmetry ⚡|
+-----------------------+-------------------+-------------------+-------------------+
```

## 4. Internal Working
Tracing Manacher's Algorithm on `s = "abaaba"`:

```
Transformed String T: "^ # a # b # a # a # b # a # $"
Index:                0 1 2 3 4 5 6 7 8 9 10 11 12 13 14

Step 1: Process index i = 6 (Char 'a')
        Expands to "#a#b#a#a#b#a#" -> P[6] = 6 (Max Radius!)
        Center C = 6, Right Boundary R = 6 + 6 = 12

Step 2: Process index i = 7 (Char '#')
        i < R (7 < 12) -> i_mirror = 2*6 - 7 = 5
        P[i] = Math.min(R - i, P[5]) = Math.min(12 - 7, 1) = 1! (Computed in O(1) time!)

Step 3: Process index i = 8 (Char 'a')
        i < R (8 < 12) -> i_mirror = 2*6 - 8 = 4
        P[i] = Math.min(R - 8, P[4]) = Math.min(4, 0) = 0 -> Try expansion -> P[8] = 0

Result: Max P[i] = 6 at center 6 -> Original Palindrome = "abaaba" (Length 6!) ✅
```

## 5. Visual Diagram
Manacher Mirror Index & Boundary Reuse Visualized:

```
Center C = 6, Right Boundary R = 12
-------------------------------------------------------
Index:       0  1  2  3  4  5  [6]  7  8  9 10 11  12
Transformed: ^  #  a  #  b  #   a   #  a  #  b  #   a

                         ^          ^
                   i_mirror=4      i=8 (i_mirror = 2*C - i = 12 - 8 = 4)

Because P[i_mirror] (P[4]) is known, P[8] is initialized to min(R - i, P[4]) in O(1) time!
```

## 6. Operations / Algorithms
Manacher's Algorithm Master Implementation:

```java
public String longestPalindromeManacher(String s) {
    if (s == null || s.length() == 0) return "";

    // 1. Transform string: "aba" -> "^#a#b#a#$"
    StringBuilder sb = new StringBuilder("^");
    for (int i = 0; i < s.length(); i++) {
        sb.append("#").append(s.charAt(i));
    }
    sb.append("#$");
    String T = sb.toString();

    int N = T.length();
    int[] P = new int[N];
    int C = 0, R = 0;

    // 2. Compute P[i] radii using symmetry
    for (int i = 1; i < N - 1; i++) {
        int i_mirror = 2 * C - i; // Symmetric mirror of i around C

        if (R > i) {
            P[i] = Math.min(R - i, P[i_mirror]);
        } else {
            P[i] = 0;
        }

        // Attempt to expand palindrome centered at i
        while (T.charAt(i + 1 + P[i]) == T.charAt(i - 1 - P[i])) {
            P[i]++;
        }

        // Update Center C and Right Boundary R if palindrome expands past R
        if (i + P[i] > R) {
            C = i;
            R = i + P[i];
        }
    }

    // 3. Find maximum radius in P array
    int maxLen = 0, centerIndex = 0;
    for (int i = 1; i < N - 1; i++) {
        if (P[i] > maxLen) {
            maxLen = P[i];
            centerIndex = i;
        }
    }

    // Extract original substring from transformed index
    int start = (centerIndex - maxLen) / 2;
    return s.substring(start, start + maxLen);
}
```

> **Quick Syntax:**
```java
// Manacher Mirror Index Syntax
int i_mirror = 2 * C - i;
if (R > i) P[i] = Math.min(R - i, P[i_mirror]);
```

## 7. Examples
* **LeetCode 5 - Longest Palindromic Substring**: Manacher's $O(N)$ linear time solution.
* **LeetCode 214 - Shortest Palindrome**: Finding longest palindromic prefix using Manacher's.
* **LeetCode 1745 - Palindrome Partitioning IV**: Checking 3-way palindrome splits in $O(N^2)$ precomputation.

## 8. Java Code
Complete interview-ready Java suite implementing Manacher's Algorithm, String Transformation, and Dry Run verification:

```java
public class ManachersAlgorithmMaster {

    // Manacher's Algorithm O(N) Time, O(N) Space
    public static String longestPalindrome(String s) {
        if (s == null || s.length() == 0) return "";

        // Step 1: Pre-process string with dummy delimiters
        // Example: "aba" -> "^#a#b#a#$"
        StringBuilder sb = new StringBuilder("^");
        for (int i = 0; i < s.length(); i++) {
            sb.append("#").append(s.charAt(i));
        }
        sb.append("#$");
        String T = sb.toString();

        int N = T.length();
        int[] P = new int[N];
        int C = 0, R = 0;

        // Step 2: Calculate Palindrome Radii
        for (int i = 1; i < N - 1; i++) {
            int i_mirror = 2 * C - i;

            if (R > i) {
                P[i] = Math.min(R - i, P[i_mirror]);
            }

            // Expand palindrome centered at i
            while (T.charAt(i + 1 + P[i]) == T.charAt(i - 1 - P[i])) {
                P[i]++;
            }

            // Adjust Center C and Right Boundary R
            if (i + P[i] > R) {
                C = i;
                R = i + P[i];
            }
        }

        // Step 3: Extract Longest Palindromic Substring
        int maxLen = 0;
        int centerIndex = 0;

        for (int i = 1; i < N - 1; i++) {
            if (P[i] > maxLen) {
                maxLen = P[i];
                centerIndex = i;
            }
        }

        int start = (centerIndex - maxLen) / 2;
        return s.substring(start, start + maxLen);
    }

    // Dry Run Demonstration
    public static void main(String[] args) {
        String s1 = "babad";
        System.out.println("Original: " + s1);
        System.out.println("Manacher's Result: \"" + longestPalindrome(s1) + "\""); // "bab" or "aba"

        String s2 = "cbbd";
        System.out.println("\nOriginal: " + s2);
        System.out.println("Manacher's Result: \"" + longestPalindrome(s2) + "\""); // "bb"
    }
}
```

## 9. Complexity Analysis
| Phase | Time Complexity | Auxiliary Space | Key Note |
| :--- | :--- | :--- | :--- |
| **String Transformation** | **$O(N)$** | $O(N)$ | Inserts `#` delimiters and markers |
| **Radius Array `P[i]` Pass**| **$O(N)$** | $O(N)$ | $R$ boundary moves strictly right |
| **Total Execution Time** | **$O(N)$ Linear** | **$O(N)$ Space** | Absolute fastest palindrome algorithm ⚡ |

## 10. Edge Cases
* **Start/End Sentinel Markers (`^` and `$`)**: Must be unique characters NOT present in the input string to prevent out-of-bounds array checks during while loop expansion.
* **Empty Input String**: Returns `""` immediately.
* **All Same Characters (`"aaaaa"`)**: $R$ boundary advances cleanly to the end of the transformed string in linear $O(N)$ time.

## 11. Common Mistakes
* Omitting the sentinel markers `^` and `$` (causes `StringIndexOutOfBoundsException` during outward while-loop expansion!).
* Writing `i_mirror = C - i` instead of **`i_mirror = 2 * C - i`** (incorrect symmetric mirror calculation).
* Forgetting to divide `(centerIndex - maxLen) / 2` when extracting the starting index in the original string.

## 12. Important Notes & Tricks (Mandatory)

> **Interview Reminder:** Why are `^` and `$` sentinel markers added to the transformed string?
> `^` at index 0 and `$` at index $N-1$ act as automatic loop-termination guards! When the expansion while loop hits `^` or `$`, `T.charAt(i + 1 + P[i]) == T.charAt(i - 1 - P[i])` evaluates to `false` automatically, eliminating array index boundary checks!

> **Memory Trick:** **"Transform: ^#a#b#a#$, i_mirror = 2*C - i, start = (center - maxLen) / 2"**.

## 13. Comparisons
| Feature | Expand Around Center | Manacher's Algorithm |
| :--- | :--- | :--- |
| **Time Complexity** | $O(N^2)$ | **$O(N)$ Linear (Optimal)** |
| **Space Complexity**| **$O(1)$ Constant** | $O(N)$ Auxiliary Array |
| **Code Complexity** | Low ($\approx 20$ lines) | High ($\approx 40$ lines) |
| **Interview Recommendation** | Default choice | Mention as optimal theoretical upgrade |

## 14. How to Recognize This in Questions
* **"Find longest palindromic substring in linear O(N) time"** $\rightarrow$ Manacher's Algorithm.
* **"Check multiple palindrome queries in O(1) time after O(N) precomputation"** $\rightarrow$ Manacher's $P[i]$ Array.

## 15. Frequently Asked Interview Questions
* **Q: Why does Manacher's Algorithm execute in linear $O(N)$ time?**  
  *A:* Because in each step of the expansion while-loop, the right boundary $R$ increases by at least 1. Since $R$ can increase at most $2N+3$ times, the inner while-loop executes at most $2N+3$ total times across all iterations $\implies O(N)$ total operations.
* **Q: What does `P[i]` represent in terms of the original string?**  
  *A:* The radius `P[i]` in the transformed string equals the **exact length** of the palindrome in the original string!

## 16. Quick Revision Box
```
+-----------------------------------------------------------------------+
| QUICK REVISION: MANACHER'S ALGORITHM                                  |
+-----------------------------------------------------------------------+
| • Transform: Add ^ at start, # between chars, $ at end                |
| • Mirror Index: i_mirror = 2 * C - i                                  |
| • Min Bounded Radius: if (R > i) P[i] = Math.min(R - i, P[i_mirror])  |
| • Original Substring Start Index: start = (centerIndex - maxLen) / 2  |
| • Complexity: O(N) Linear Time | O(N) Auxiliary Space                 |
+-----------------------------------------------------------------------+
```

## 17. Practice Checklist
- [ ] I can write the transformed string formatter (`"^#a#b#a#$"`).
- [ ] I can derive the mirror index formula `i_mirror = 2 * C - i`.
- [ ] I can write the bounded radius initial value `Math.min(R - i, P[i_mirror])`.
- [ ] I know why `^` and `$` prevent array index out of bounds errors.
- [ ] I can derive the original string start index formula `(centerIndex - maxLen) / 2`.
